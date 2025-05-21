import pygame
from bullet import Bullet
from alien import Alien
import sys
import time


def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sound, sb):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type in (pygame.KEYDOWN, pygame.KEYUP):
            handle_keyboard_event(event, ai_settings, screen, ship, bullets, sound)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb)

def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb):
    play_button.rect.collidepoint(mouse_x, mouse_y)
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        #重置游戏信息
        stats.reset_stats()
        stats.game_active = True
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)

        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        #重置记分牌
        sb.prep_score()
        sb.prep_ships()
        sb.prep_high_score()

def check_high_scores(stats, sb):
    if stats.score >= stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def handle_keyboard_event(event, ai_settings, screen, ship, bullets, sound):
    """处理键盘事件"""
    if event.type == pygame.KEYDOWN:
        handle_keydown_event(event, ai_settings, screen, ship, bullets, sound)
    elif event.type == pygame.KEYUP:
        handle_keyup_event(event, ship)

def handle_keydown_event(event, ai_settings, screen, ship, bullets, sound):
    """处理按下键事件"""
    # 成了一部字典的键值对
    key_actions = {
        pygame.K_RIGHT: lambda: setattr(ship, 'moving_right', True),
        pygame.K_LEFT: lambda: setattr(ship, 'moving_left', True),
        pygame.K_SPACE: lambda: (
            fire_bullet(ai_settings, screen, ship, bullets),
            sound.play_sound()
        ),
        pygame.K_q: sys.exit
    }
    action = key_actions.get(event.key)
    if action:
        action()

def handle_keyup_event(event, ship):
    """处理释放键事件"""
    key_actions = {
        pygame.K_RIGHT: lambda: setattr(ship, 'moving_right', False),
        pygame.K_LEFT: lambda: setattr(ship, 'moving_left', False)
    }
    action = key_actions.get(event.key)
    if action:
        action()

def update_screen(ai_settings, screen, ship, bullets, aliens, stats, text_button, sb):
    """更新屏幕上的图像，并切换到新屏幕"""
    screen.fill(ai_settings.bg_color)
    
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not stats.game_active:
       text_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def change_fleet_direction(aliens, ai_settings):
    """改变外星人群的方向并向下移动"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed_factor
    ai_settings.fleet_direction *= -1

def check_fleet_edges(aliens, ai_settings):
    """检查外星人群是否到达屏幕边缘"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(aliens, ai_settings)
            break

def update_aliens(aliens, ai_settings, ship, stats, bullets, screen, sb):
    """更新外星人群中所有外星人的位置"""
    check_fleet_edges(aliens, ai_settings)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, aliens, bullets, ai_settings, screen, ship, sb)

def ship_hit(stats, aliens, bullets, ai_settings, screen, ship, sb):
    if stats.ship_left >= 0:
        stats.ship_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        time.sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_bullets(ai_settings, screen, aliens, ship, bullets, stats, sb):
    """更新子弹的位置并删除已消失的子弹"""
    bullets.update()

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullets_alien_collision(ai_settings, screen, aliens, ship, bullets, stats, sb)

def check_bullets_alien_collision(ai_settings, screen, aliens, ship, bullets, stats, sb):
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_scores(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, aliens, ship)

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果未达到限制，则发射一颗子弹"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def calculate_aliens_per_row(ai_settings, alien_width):
    """
    计算每行可以容纳的外星人数。
    :param ai_settings: 游戏设置对象
    :param alien_width: 单个外星人的宽度
    :return: 每行可容纳的外星人数
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行/列"""
    alien = Alien(ai_settings, screen)
    alien_width, alien_height = alien.rect.size
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.x, alien.rect.y = alien.x, alien.y
    aliens.add(alien)

def get_number_rows(ai_settings, alien_height, ship_height):
    """
    计算屏幕可以容纳多少行外星人。
    :param ai_settings: 游戏设置对象
    :param alien_height: 单个外星人的高度
    :param ship_height: 飞船的高度
    :return: 屏幕可容纳的行数
    """
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    return int(available_space_y / (2 * alien_height))

def create_fleet(ai_settings, screen, aliens, ship):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = calculate_aliens_per_row(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
    
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


