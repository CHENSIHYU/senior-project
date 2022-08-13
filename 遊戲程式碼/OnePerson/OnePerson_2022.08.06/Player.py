import pygame
import os
from Bullet import Bullet
import pyautogui

WIDTH = 1280
HEIGHT = 800
mX, mY = pyautogui.position()


# 建立遊戲視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)

# color
BLACK = (0,0,0)

# 載入圖片
player_img = pygame.image.load(os.path.join("img",'player.png')).convert()
plane01R_img = pygame.image.load(os.path.join("img", "plane01_R30.png")).convert()    #飛機右轉
plane01L_img = pygame.image.load(os.path.join("img", "plane01_L30.png")).convert()    #飛機左轉

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (100,80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18  #碰撞判斷半徑(不可改名)
        #pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)  #測試飛船的碰撞半徑大小
        self.rect.center = (WIDTH/2, HEIGHT-75)
        self.speed = 8
        self.direction = 0
        pos = pygame.mouse.get_pos()
        self.mousex_now = pos[0]
        

    def update(self):
        self.direction = 0  #預設圖片為正向
        
        # # 鍵盤控制
        # key_pressed = pygame.key.get_pressed()     # 判斷按鍵是否被按
        # if key_pressed[pygame.K_RIGHT]:
        #    self.direction = 1     # 按下右鍵圖片改成右轉
        #    self.rect.x += self.speed
        # if key_pressed[pygame.K_LEFT]:
        #    self.direction = -1
        #    self.rect.x -= self.speed
        # if key_pressed[pygame.K_UP]:
        #    self.rect.y -= self.speed
        # if key_pressed[pygame.K_DOWN]:
        #    self.rect.y += self.speed

        # 滑鼠控制
        pos = pygame.mouse.get_pos()
        mousex = pos[0]
        mousey = pos[1]
        if mousex - self.mousex_now > 0:
            self.direction = 1
        elif mousex - self.mousex_now < 0:
            self.direction = -1
        else:
            self.direction = 0
        mousex_now = mousex
        self.rect.center = (mousex, mousey)

        if self.rect.right > WIDTH:       # 防止飛船超出視窗
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
    #角色移動動畫
    def animate(self,newPo, oldPo):
        if oldPo>newPo: #向左
            self.image = pygame.transform.scale(plane01L_img, (100,80))
            self.image.set_colorkey(BLACK)
        elif oldPo<newPo:   #向右
            self.image = pygame.transform.scale(plane01R_img, (100,80))
            self.image.set_colorkey(BLACK)
        else:   #回到原圖片
            self.image = pygame.transform.scale(player_img, (100,80))
            self.image.set_colorkey(BLACK)

    # def shoot(self):
    #     bullet = Bullet(self.rect.centerx, self.rect.top)
    #     all_sprites.add(bullet)
    #     player_bullets.add(bullet)