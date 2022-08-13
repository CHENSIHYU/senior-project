import pygame
import os
from Bullet import Bullet

WIDTH = 1280
HEIGHT = 800

# 建立遊戲視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)

# color
BLACK = (0,0,0)

# 載入圖片
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []

for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f'expl{i}.png')).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (40, 40)))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center  = center
        self.frame = 0  #更新到第幾張圖片
        self.last_update = pygame.time.get_ticks()  #紀錄最後更新圖片的時間
        self.frame_rate = 50  #經過幾毫秒更新圖片

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center