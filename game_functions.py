import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应飞船碰撞,死一条命，然后刷新游戏"""
    if stats.ships_left > 0 :
        stats.ships_left -= 1

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 刷新到游戏初始状态
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #缓个神
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

#create系列
def get_number_alien_x(ai_settings, alien_width):
    """计算每行外星人数目"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width ))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算可以容纳多少行外星人"""
    avaiable_space_y = (ai_settings.screen_height -
                        (3 * alien_height) - ship_height)
    number_rows = int(avaiable_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    numer_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    #创外星人群
    for row_number in range(number_rows):
        for alien_number in range(numer_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


#check系列
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings,screen, ship, bullets):
    """没有达到子弹限制就发射一颗子弹"""
     # 创建一个子弹并加入编组中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_enents(event,ship):
    """响应松开"""
    if  event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,play_button,ship,aliens,
                 bullets):
    """"响应鼠标和按键"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_enents(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,
                              aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,
                      bullets,mouse_x,mouse_y):
    """单击Play开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏信息
        stats.reset_stats()
        stats.game_active = True

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 刷新到游戏初始状态
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_alien_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检测外星人触底没有"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 如果飞船底部比屏幕底部y值大
            ship_hit(ai_settings,stats, screen, ship, aliens, bullets)
            break

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边界时采取措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """整体下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

#update系列
def update_aliens(ai_settings,stats, screen, ship, aliens, bullets):
    """检查边缘触碰，更新外星人位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        print("你娃的飞船被撞到了！！！")

    # 检测是否有外星人到底了
    check_alien_bottom(ai_settings,stats,screen,ship,aliens,bullets)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,
                  play_button):
    """更新屏幕上的图像，并刷新屏幕"""
    # 每次循环重绘屏幕
    screen.fill(ai_settings.bg_color)

    # 在飞船和外星人跟后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏非活跃状态就绘制play
    if not stats.game_active:
        play_button.draw_button()

    # 让屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship,
                   aliens, bullets):
    """删除已经消失的子弹"""
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets)

    bullets.update()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    """响应子弹和外星人碰撞，删除碰撞的物体"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        # 删除子弹并新建一群外星人,还他妈的给你提个速，让你爽一爽
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        print(len(bullets))

def check_high_score(stats,sb):
    """检查最高得分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
