import pygame
import os
import Bullet

WIDTH = 1280
HEIGHT = 800

# 建立遊戲視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)

# color
BLACK = (0,0,0)

# 載入圖片
enemy_img = pygame.image.load(os.path.join("img",'enemy.png')).convert()
plane01R_img = pygame.image.load(os.path.join("img", "plane01_R30.png")).convert()    #飛機右轉
plane01L_img = pygame.image.load(os.path.join("img", "plane01_L30.png")).convert()    #飛機左轉


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        if size == "sm":
            self.image = pygame.transform.scale(enemy_img, (60,90))
        if size == "mid":
            self.image = pygame.transform.scale(enemy_img, (100,130))
        if size == "lg":
            self.image = pygame.transform.scale(enemy_img, (140,170))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 10
        #pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        self.rect.center = (x, y)
        self.speed = 8

    def update(self):
        # if self.rect.right > WIDTH:       # 防止飛船超出視窗
        #     self.rect.right = WIDTH
        # if self.rect.left < 0:
        #     self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.bottom > HEIGHT/2:
            self.rect.bottom = HEIGHT/2

    # def shoot(self):
    #     bullet = Enemy_Bullet(self.rect.centerx, self.rect.bottom)
    #     all_sprites.add(bullet)
    #     enemy_bullets.add(bullet)