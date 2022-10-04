import pygame
import os

WIDTH = 1280
HEIGHT = 800

# 建立遊戲視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)

# 載入圖片
bg_img = pygame.image.load(os.path.join("img",'bg1.png')).convert()

class Background(pygame.sprite.Sprite):
    def __init__(self,is_alt=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = bg_img
        self.rect = self.image.get_rect()
        self.speed = 1

        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= screen_rect.height:
            self.rect.y = -self.rect.height