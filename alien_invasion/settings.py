class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (55,61,65)
        #子弹设置
        self.bullet_speed_factor = 1
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = 101,78,163
        self.bullets_allowed = 4
        #飞船的设置
        self.ship_speed_factor = 1.5
        self.ship_limit = 3
        #外星人设置
        self.alien_speed_factor = 1.0
        self.alien_drop_speed_factor = 10
        #fleet_direction为一表示向右移，负一表示向左移
        self.fleet_direction = 1
        #以什么样的速度加快游戏
        self.speedup_scale = 1.1
        #外星人点数的提高速度
        self.score_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.bullet_speed_factor = 1
        self.alien_speed_factor = 1
        self.ship_speed_factor = 1.5
        self.fleet_direction = 1
        #计分
        self.alien_points = 50

    def increase_speed(self):
        self.alien_speed_factor *= self.speedup_scale
        self.alien_drop_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)