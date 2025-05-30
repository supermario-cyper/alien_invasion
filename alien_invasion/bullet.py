import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen

        #在（0，0）处创建一个子弹的矩形，再设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #存储用小数存储的子弹的位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
         #更新表示子弹位置的小数值
        self.y -= self.speed_factor
         #更新表示子弹rect的位置
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
