import pygame
import random
import os
import time

# 物件導入
from Background import Background
from Bullet import Bullet
from Enemy_Bullet import Enemy_Bullet
from Player import Player
from Enemy import Enemy
from Explosion import Explosion

pygame.init()

# 設定好就不會輕易改變的變數用大寫
FPS = 60
WIDTH = 1280
HEIGHT = 800
deduction = 1
enemy_number = 2000

# 敵人不射子彈
# enemy_number = 10000000 => 電腦完全掛掉
# enemy_number = 1000000 => 要跑很久畫面才會出現
# enemy_number = 100000 => 飛機 lag
# enemy_number = 10000 => 子彈 lag
# enemy_number = 3000 => 子彈速度雖有拖，但還能接受
# enemy_number = 2000 => 完全正常

# 敵人射子彈
# enemy_number = 10000000 => 電腦完全掛掉
# enemy_number = 1000000 => 電腦完全掛掉
# enemy_number = 100000 => 要跑很久畫面才會出現
# enemy_number = 10000 => 飛機 lag
# enemy_number = 3000 => 子彈 lag
# enemy_number = 1500 => 完全正常

enemy_shoot_time = 100
score = [600, 600]
coll = 0
delay = 0

# color
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("B12_手部辨識飛機射擊遊戲")

clock = pygame.time.Clock()
running = True

# 鼠標顯示設定
#pygame.mouse.set_visible(False)
#pygame.event.set_grab(True)

# 引入字體 => 從目前程式執行之電腦尋找
font_name = pygame.font.match_font('Calibri')

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)  # 改字體大小
    text_surface = font.render(text, True, WHITE)  # 製作文字圖片
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #將文字畫到屏幕上

def player_control():
    if event.type == pygame.KEYDOWN:     #按下鍵盤鍵
        if event.key == pygame.K_SPACE:
            player_bullet = Bullet(player.rect.centerx, player.rect.top)
            all_sprites.add(player_bullet)
            player_bullets.add(player_bullet)
        #if event.key == pygame.K_p:
        #    enemy.shoot()
    elif event.type == pygame.MOUSEBUTTONDOWN:    #滑鼠
        pressed_array = pygame.mouse.get_pressed()
        for index in range(len(pressed_array)):
            if pressed_array[index]:
                if index == 0:
                    player_bullet = Bullet(player.rect.centerx, player.rect.top)
                    all_sprites.add(player_bullet)
                    player_bullets.add(player_bullet)
                elif index == 1:
                    print('The mouse wheel Pressed!')
                elif index == 2:
                    print('Pressed RIGHT Button!')

def getHit(score):

    # draw_text(screen, str("now is hitting"), 18, 100, 10)
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_circle) # False：不要刪掉 player
   
    for i in range(enemy_number):
        if i == 0:
            enemy_hits = pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)
        else: enemy_hits += pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)

    ## 分數
    for hit in player_hits:
        score[1] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    for hit in enemy_hits:
        score[0] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)

    return score

def getColl(coll):
    close_hits = pygame.sprite.spritecollide(player, enemy_group, True, pygame.sprite.collide_circle)
    if close_hits:
        expl = Explosion(close_hits[0].rect.center, 'lg')
        all_sprites.add(expl)
        coll = 1;

    return coll


# 建立 sprit 群組
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# 建立物件
bg1 = Background()
bg2 = Background(is_alt=True)
player = Player()
enemy = [0]*enemy_number
for i in range(enemy_number):
    enemy[i] = Enemy(WIDTH-100*i/10, 50)
background = Background()

# 加入群組
all_sprites.add(bg1,bg2)
all_sprites.add(background)
all_sprites.add(player)
for i in range(enemy_number):
    all_sprites.add(enemy[i])
enemy_group.add(enemy)

while running:
    clock.tick(FPS)
    delay += 1
    enemy_shoot_time -= 1
    if coll == 0:
        if enemy_shoot_time <= 0:
            for i in range(enemy_number):
                enemy_bullet = Enemy_Bullet(enemy[i].rect.centerx, enemy[i].rect.bottom)
                all_sprites.add(enemy_bullet)
                enemy_bullets.add(enemy_bullet)
            enemy_shoot_time = 100

    # 取得玩家輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:     #按X
            running = False
        player_control()


    # 更新遊戲
    all_sprites.update()
    #Player.animate(player)  #角色移動動畫

    # 渲染/顯示遊戲畫面
    all_sprites.draw(screen)
    score = getHit(score)
    coll = getColl(coll)
    if coll == 1:
        delay = -40
        coll = 2
    if delay == -1:
        running = False
        
    draw_text(screen, str(score[0]), 18, WIDTH/2, 10)
    draw_text(screen, str(score[1]), 18, WIDTH/2, HEIGHT-20)

    pygame.display.update()

pygame.quit()