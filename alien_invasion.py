import sys

import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from  ship import Ship
from  alien import  Alien
import game_functions as gf

def run_game():
    #初始化游戏，创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings,screen,"Play")

    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    #创建飞船
    ship = Ship(ai_settings,screen)
    # 创建存储子弹的组
    bullets = Group()
    # 创建外星人组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    #主循环
    while True:
        gf.check_events(ai_settings,screen,stats,play_button,ship,
                        aliens,bullets) #监听事件

        if stats.game_active :
            ship.update()      #监听飞船位置变化
            gf.update_bullets(ai_settings, screen, stats, sb,
                              ship, aliens, bullets)  #监听子弹和外星人的碰撞、刷新外星人
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
                    #↑↑监听外星人移动，放在子弹后，需要检测子弹与外星人碰撞

        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,
                         bullets,play_button) #监听屏幕


run_game()
#运行游戏