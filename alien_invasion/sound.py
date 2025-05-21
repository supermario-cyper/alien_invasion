import pygame.mixer

class Sound:
    def __init__(self):
        # 优先设置混音器参数（可选但推荐）
        pygame.mixer.init()
        
        try:
            # 加载背景音乐
            pygame.mixer.music.load("bgm.mp3")
            pygame.mixer.music.set_volume(0.5)
        except pygame.error as e:
            print(f"Warning: Background music failed to load. Error: {e}")

        try:
            # 射击音效
            self.shot_sound = pygame.mixer.Sound("shot_sound.wav")
            self.shot_sound.set_volume(0.5)
        except pygame.error as e:
            print(f"Warning: Shot sound failed to load. Using default sound. Error: {e}")
            self.shot_sound = None  # 设置为 None 表示没有音效

    def play_bgm(self):
            pygame.mixer.music.play(-1)

    def play_sound(self):
        if self.shot_sound:  # 检查是否成功加载了音效
            self.shot_sound.play(0)
        else:
            print("No shot sound available.")  # 提供默认行为
