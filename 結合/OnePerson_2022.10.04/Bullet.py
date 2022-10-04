import pygame
import os

WIDTH = 1280
HEIGHT = 800

# 建立遊戲視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)

BLACK = (0,0,0)

bullet_img = [0]*3

# 載入圖片
for i in range(3):
    bullet_img[i] = pygame.image.load(os.path.join("img",f'bullet{i}.png')).convert()
    bullet_img[i].set_colorkey(BLACK)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img[0], (30,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed

        #如果子彈超出螢幕視窗，就把該子彈刪掉
        if self.rect.bottom < 0:
            self.kill()