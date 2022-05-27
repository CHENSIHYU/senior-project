import pygame
import random
import os

pygame.init()

# 設定好就不會輕易改變的變數用大寫
FPS = 60
WIDTH = 500
HEIGHT = 600
player_score = 1000
enemy_score = 1000
deduction = 1

# color
WHITE = (255,255,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

Background_Color = WHITE
screen = pygame.display.set_mode( (WIDTH,HEIGHT) )
screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)
pygame.display.set_caption("PyGame Test")

clock = pygame.time.Clock()
running = True

# 載入圖片
bg_img = pygame.image.load(os.path.join("img",'background.jpg')).convert()
player_img = pygame.image.load(os.path.join("img",'player.png')).convert()
enemy_img = pygame.image.load(os.path.join("img",'enemy.png')).convert()

# 引入字體
font_name = pygame.font.match_font('Calibri')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)  #將文字渲染出來
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #將文字畫到屏幕上

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
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20  #碰撞判斷半徑(不可改名)
        #pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)  #測試飛船的碰撞半徑大小
        self.rect.center = (WIDTH/2, HEIGHT-45)
        self.speed = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()     # 判斷按鍵是否被按
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed

        if self.rect.right > WIDTH:       # 防止飛船超出視窗
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.bottom < HEIGHT/2:
            self.rect.bottom = HEIGHT/2
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        player_bullets.add(bullet)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        self.rect.center = (WIDTH/2, 50)
        self.speed = 8

    def update(self):
        key_pressed = pygame.key.get_pressed()     # 判斷按鍵是否被按
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speed
        if key_pressed[pygame.K_s]:
            self.rect.y -= self.speed
        if key_pressed[pygame.K_w]:
            self.rect.y += self.speed

        if self.rect.right > WIDTH:       # 防止飛船超出視窗
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.bottom > HEIGHT/2:
            self.rect.bottom = HEIGHT/2

    def shoot(self):
        bullet = Enemy_Bullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface( (10,20) )
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:     #如果子彈超出螢幕視窗，就把該子彈刪掉
            self.kill()
class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface( (10,20) )
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:     #如果子彈超出螢幕視窗，就把該子彈刪掉
            self.kill()

# 建立 sprit 群組
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# 建立物件
bg1 = Background()
bg2 = Background(is_alt=True)
player = Player()
enemy = Enemy()
background = Background()

all_sprites.add(bg1,bg2)
all_sprites.add(background)
all_sprites.add(player)
all_sprites.add(enemy)
enemy_group.add(enemy)

while running:
    clock.tick(FPS)

    # 取得玩家輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     #按X
            running = False
        elif event.type == pygame.KEYDOWN:     #按下鍵盤鍵
            if event.key == pygame.K_SPACE:
                player.shoot()
            elif event.key == pygame.K_p:
                enemy.shoot()


    # 更新遊戲
    all_sprites.update()
    
    ## 碰撞判斷
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, False, pygame.sprite.collide_circle) # False：不要刪掉 player
    enemy_hits = pygame.sprite.spritecollide(enemy, player_bullets, False, pygame.sprite.collide_circle)
    tie_hits = pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_circle)

    ## 分數
    for hit in player_hits:
        player_score -= deduction
    for hit in enemy_hits:
        enemy_score -= deduction

    ## 關閉視窗 => 之後是平手判斷
    if tie_hits:
        running = False


    # 渲染/顯示遊戲畫面
    all_sprites.draw(screen)
    draw_text(screen, str(enemy_score), 18, WIDTH/2, 10)
    draw_text(screen, str(player_score), 18, WIDTH/2, HEIGHT-20)

    pygame.display.update()

pygame.quit()