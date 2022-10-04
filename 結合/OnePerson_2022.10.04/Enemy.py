import pygame
import os
import Bullet
import pyautogui

WIDTH = 1280
HEIGHT = 800
newX, newY = pyautogui.position()

# 建立遊戲視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)

# color
BLACK = (0,0,0)
WHITE=(255, 255,255)
YELLOW = (255,255,0)
# 載入圖片
enemy_img = pygame.image.load(os.path.join("img",'newPlaneColor.png')).convert()
plane01R_img = pygame.image.load(os.path.join("img", "newPlaneColor_R30.png")).convert()    #飛機右轉
plane01L_img = pygame.image.load(os.path.join("img", "newPlaneColor_L45.png")).convert()    #飛機左轉
boss_img = pygame.image.load(os.path.join("img",'boss01.png')).convert()
bossUp_img = pygame.image.load(os.path.join("img",'boss02.png')).convert()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        if size == "sm":
            self.image = pygame.transform.scale(enemy_img, (120,80))
            self.image.set_colorkey(BLACK)
            self.radius = 10
        if size == "mid":
            self.image = pygame.transform.scale(enemy_img, (200,130))
            self.image.set_colorkey(BLACK)
            self.radius = 15
        # if size == "lg":
        #     self.image = pygame.transform.scale(enemy_img, (260,170))
        #     self.image.set_colorkey(BLACK)
        #     self.radius = 20
        if size == "boss":
            self.image = pygame.transform.scale(boss_img, (260,170))
            self.image.set_colorkey(WHITE)
            self.radius = 50
        self.rect = self.image.get_rect()
        # pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
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

    #角色移動動畫
    def animate(self,position):
        if position == 1: #向左
            self.image = pygame.transform.scale(plane01L_img, (200,130))
            self.image.set_colorkey(BLACK)
        elif position == 2:   #向右
            self.image = pygame.transform.scale(plane01R_img, (200,130))
            self.image.set_colorkey(BLACK)
        elif position % 2 == 0:
            self.image = pygame.transform.scale(boss_img, (350,240))
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH/2, 105)
            # pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        elif position % 2 == 1:
            self.image = pygame.transform.scale(bossUp_img, (350,240))
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()
            self.rect.center = (WIDTH/2, 105)
            # pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        # else:   #回到原圖片
        #     self.image = pygame.transform.scale(enemy_img, (200,130))
        #     self.image.set_colorkey(BLACK)   
        
    # def shoot(self):
    #     bullet = Enemy_Bullet(self.rect.centerx, self.rect.bottom)
    #     all_sprites.add(bullet)
    #     enemy_bullets.add(bullet)