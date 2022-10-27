import pygame
import os
import GlobalPosition

WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小

plane01_img = pygame.image.load(os.path.join("image", "plane01.png")).convert()
plane01R_img = pygame.image.load(os.path.join("image", "plane01_R30.png")).convert()
plane01L_img = pygame.image.load(os.path.join("image", "plane01_L30.png")).convert()
enemy_img = pygame.image.load(os.path.join("image",'plane03.png')).convert()
enemyL_img = pygame.image.load(os.path.join("image",'plane03_L30.png')).convert()
enemyR_img = pygame.image.load(os.path.join("image",'plane03_R30.png')).convert()

GlobalPosition.initial()
originx = GlobalPosition.ServerX
enemyx = GlobalPosition.ServerEnemy

#玩家
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        global originx
        pygame.sprite.Sprite.__init__(self)     #呼叫初始函式
        self.image = pygame.transform.scale(plane01_img, (140, 100)) #調整圖片大小
        self.image.set_colorkey(BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = originx
        self.rect.centery = y
        self.radius = 35   #圓型碰撞範圍半徑
        pygame.draw.circle(self.image, WHITE, self.rect.center, self.radius)    #畫出圓形
        self.speedx = 7                         #圖片移動速度

    def update(self, x, y):
        global originx
        self.image = pygame.transform.scale(plane01_img, (140, 100)) #調整圖片大小
        self.image.set_colorkey(BLACK)    #圖片去背
        self.rect = self.image.get_rect()       #圖片定位(外框)
        self.rect.centerx = originx
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.centerx < 0:
            self.rect.centerx = 0.1
        if self.rect.centerx >= WIDTH:
            self.rect.centerx = WIDTH
        if self.rect.centery < 0:
            self.rect.centery = 0.1
        if self.rect.centery >= HEIGHT:
            self.rect.centery = HEIGHT

    def animate(self, x, y):
        global originx
        if(x > originx):
            self.image = pygame.transform.scale(plane01R_img, (140, 100)) #調整圖片大小
            self.image.set_colorkey(BLACK)    #圖片去背
            self.rect = self.image.get_rect()       #圖片定位(外框)
            self.rect.centerx = x
            self.rect.centery = y
            originx = x
        elif(x < originx):
            self.image = pygame.transform.scale(plane01L_img, (140, 100)) #調整圖片大小
            self.image.set_colorkey(BLACK)    #圖片去背
            self.rect = self.image.get_rect()       #圖片定位(外框)
            self.rect.centerx = x
            self.rect.centery = y
            originx = x  
        GlobalPosition.ServerX = originx
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (200,120))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.radius = 10
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 8

    def update(self, x,  y):
        self.image = pygame.transform.scale(enemy_img, (200,120))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # 防止飛船超出視窗
        if self.rect.centerx <= 0:
            self.rect.centerx = 0
        if self.rect.centerx >= WIDTH:
            self.rect.centerx = WIDTH
        if self.rect.centery <= 0:
            self.rect.centery = 0
        if self.rect.centery >= HEIGHT:
            self.rect.centery = HEIGHT

    def animate(self, x, y):
        global enemyx
        if(x > enemyx):
            self.image = pygame.transform.scale(enemyL_img, (200, 120)) #調整圖片大小
            self.image.set_colorkey(BLACK)    #圖片去背
            self.rect = self.image.get_rect()       #圖片定位(外框)
            self.rect.centerx = x
            self.rect.centery = y
            enemyx = x
        elif(x < enemyx):
            self.image = pygame.transform.scale(enemyR_img, (200, 120)) #調整圖片大小
            self.image.set_colorkey(BLACK)    #圖片去背
            self.rect = self.image.get_rect()       #圖片定位(外框)
            self.rect.centerx = x
            self.rect.centery = y
            enemyx = x  
        GlobalPosition.ServerEnemy = enemyx