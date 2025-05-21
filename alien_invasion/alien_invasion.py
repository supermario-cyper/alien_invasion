import pygame
import game_functions as gf
from settings import Settings
from ship import Ship
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound import Sound


def run_game():
    pygame.init()
    #基础设置
    bgm = Sound()
    shot_sound = Sound()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('决战外星人')
    #创建按钮
    play_button = Button(ai_settings,screen,msg='Play')
    #创建一艘飞船
    ship = Ship(ai_settings,screen)
    #创建一个用于管理子弹//外星人的编组
    bullets=Group()
    aliens = Group()
    #创建外星人人群
    gf.create_fleet(ai_settings,screen,aliens,ship)
    #创建一个存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    #创建一个计分板
    sb = Scoreboard(screen, ai_settings, stats )
    #播放背景音乐
    bgm.play_bgm()

    while True:
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, shot_sound ,sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, aliens, ship, bullets, stats, sb)
            gf.update_aliens(aliens, ai_settings, ship, stats, bullets, screen, sb)
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb)



run_game()