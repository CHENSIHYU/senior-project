import pygame
import os
import time
import pyautogui
import random
import Draw as fuc

# 物件導入
from Background import Background
from Bullet import Bullet
from Enemy_Bullet import Enemy_Bullet
from Player import Player
from Enemy import Enemy
from Explosion import Explosion

pygame.init()

# 設定好就不會輕易改變的變數用大寫
FPS = 80
WIDTH = 1280
HEIGHT = 800
deduction = 10
enemy_number = 5
enemy_shoot_time = 100
enemy_right_time = 0
enemy_left_time = 200
score = [100, 50, 50, 50, 50, 50]
coll = 0
delay = 0
oM = 0
Story_Game = True
End_Game = False
result = '無'
once_win = False

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
    # for i in range(enemy_number):
    #     if i == 0:
    #         enemy_hits = pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)
    #     else: enemy_hits += pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)
    enemy0_hits = pygame.sprite.spritecollide(enemy[0], player_bullets, True, pygame.sprite.collide_circle)
    enemy1_hits = pygame.sprite.spritecollide(enemy[1], player_bullets, True, pygame.sprite.collide_circle)
    enemy2_hits = pygame.sprite.spritecollide(enemy[2], player_bullets, True, pygame.sprite.collide_circle)
    enemy3_hits = pygame.sprite.spritecollide(enemy[3], player_bullets, True, pygame.sprite.collide_circle)
    enemy4_hits = pygame.sprite.spritecollide(enemy[4], player_bullets, True, pygame.sprite.collide_circle)

    IsBreak = False
    if score[0] == 0 or (score[1] == 0 and score[2] == 0 and score[3] == 0 and score[4] == 0 and score[5] == 0):
        IsBreak = True

    ## 分數
    for hit in player_hits:
        if IsBreak: break
        score[0] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    for hit in enemy0_hits:
        if IsBreak: break
        score[1] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    for hit in enemy1_hits:
        if IsBreak: break
        score[2] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    for hit in enemy2_hits:
        if IsBreak: break
        score[3] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    for hit in enemy3_hits:
        if IsBreak: break
        score[4] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    for hit in enemy4_hits:
        if IsBreak: break
        score[5] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)

    # 使分數不小於 0
    for i in range(enemy_number+1):
        if score[i] <= 0:
            score[i] = 0

    return score

def getColl(coll):
    close_hits = pygame.sprite.spritecollide(player, enemy_group, True, pygame.sprite.collide_circle)
    if close_hits:
        expl = Explosion(close_hits[0].rect.center, 'lg')
        all_sprites.add(expl)
        coll = 1;

    return coll

def enemy_shoot():
    for i in range(enemy_number):
        delay =  random.randint(10,50)
        if delay%10 > 5:
            #continue
            enemy_bullet = Enemy_Bullet(enemy[i].rect.centerx, enemy[i].rect.bottom)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)
        else:
            enemy_bullet = Enemy_Bullet(enemy[i].rect.centerx+15, enemy[i].rect.bottom)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)
            enemy_bullet = Enemy_Bullet(enemy[i].rect.centerx-15, enemy[i].rect.bottom)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

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
enemy[0] = Enemy(WIDTH/2-385, 105, "mid")
enemy[1] = Enemy(WIDTH/2-200, 105, "mid")
enemy[2] = Enemy(WIDTH/2, 105, "mid")
enemy[3] = Enemy(WIDTH/2+200, 105, "mid")
enemy[4] = Enemy(WIDTH/2+385, 105, "mid")

# 加入群組
all_sprites.add(bg1,bg2)
all_sprites.add(player)
for i in range(enemy_number):
    all_sprites.add(enemy[i])
enemy_group.add(enemy)

while running:
    if Story_Game:
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        fuc.draw_story("Level_4")
        Story_Game = False
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
    if End_Game:
        End_Game = False
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        # 初始化
        score = [100, 50, 50, 50, 50, 50]
        coll = 0
        delay = 0
        oM = 0
        Story_Game = False
        End_Game = False
        result = '無'
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
        enemy[0] = Enemy(WIDTH/2-385, 105, "mid")
        enemy[1] = Enemy(WIDTH/2-200, 105, "mid")
        enemy[2] = Enemy(WIDTH/2, 105, "mid")
        enemy[3] = Enemy(WIDTH/2+200, 105, "mid")
        enemy[4] = Enemy(WIDTH/2+385, 105, "mid")
        # 加入群組
        all_sprites.add(bg1,bg2)
        all_sprites.add(player)
        for i in range(enemy_number):
            all_sprites.add(enemy[i])
        enemy_group.add(enemy)

    clock.tick(FPS)
    delay += 1

    # Enemy 固定移動
    if enemy_left_time >= 0:
        for i in range(enemy_number):
            enemy[i].rect.centerx += 1
        enemy_left_time -= 1
        if enemy_left_time == 0:
            enemy_right_time = 400
    elif enemy_right_time >= 0:
        for i in range(enemy_number):
            enemy[i].rect.centerx -= 1
        enemy_right_time -= 1
        if enemy_right_time == 0:
            enemy_left_time = 400

    enemy_shoot_time -= 1
    if coll == 0:
        if enemy_shoot_time <= 0:
            enemy_shoot()
            enemy_shoot_time = random.randint(0,1000)%110

    if result == '無':
        # 取得玩家輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     #按X
                running = False
            player_control()
        # 左右轉移動動畫
        mX, mY = pyautogui.position()  # 滑鼠目前位置
        player.animate(mX, oM)

    # 分數判斷
    score = getHit(score)
    # 互撞判斷
    coll = getColl(coll)
    
    # Ending
    enemy_total_score = 0
    for i in range(1,enemy_number+1):
        enemy_total_score += score[i]
    if enemy_total_score == 0 and result != 'Win':
            result = 'Win'
            delay = -40
    if str(score[0]) == "0" and result != 'Fail':
            result = 'Fail'
            delay = -40
    if coll == 1 and result != 'Tie':
            result = 'Tie'
            delay = -40
    if delay == -1 and result == 'Win':
        End_Game = True
        once_win = True
        fuc.draw_end(result, score[0], score[1], "Level_5.py", once_win)
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        delay = 0
    if delay == -1 and result == 'Fail':
        End_Game = True
        fuc.draw_text(screen, "Fail", 64, WIDTH/2, HEIGHT/2)
        fuc.draw_end(result, score[0], score[1], "Level_5.py", once_win)
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        delay = 0
    if delay == -1 and result == 'Tie':
        End_Game = True
        fuc.draw_text(screen, "Tie", 64, WIDTH/2, HEIGHT/2)
        fuc.draw_end(result, score[0], score[1], "Level_5.py", once_win)
        screen = pygame.display.set_mode((WIDTH,HEIGHT))
        delay = 0

    # 更新遊戲
    all_sprites.update()

    # 渲染/顯示遊戲畫面
    if End_Game == False and Story_Game == False:
        all_sprites.draw(screen)
        # 0:player，1:enemy
        fuc.draw_health(screen, 100, score[0], WIDTH - 180, HEIGHT - 40)
        fuc.draw_text(screen, str(score[0]), 25, WIDTH - 210, HEIGHT - 48)
        fuc.draw_health(screen, 50, score[1], 20, 20)
        fuc.draw_text(screen, str(score[1]), 25, 210, 13)
        fuc.draw_health(screen, 50, score[2], 20, 60)
        fuc.draw_text(screen, str(score[2]), 25, 210, 53)
        fuc.draw_health(screen, 50, score[3], 20, 100)
        fuc.draw_text(screen, str(score[3]), 25, 210, 93)
        fuc.draw_health(screen, 50, score[4], 20, 140)
        fuc.draw_text(screen, str(score[4]), 25, 210, 133)
        fuc.draw_health(screen, 50, score[5], 20, 180)
        fuc.draw_text(screen, str(score[5]), 25, 210, 173)

    # 更新遊戲
    pygame.display.update()

    oM = mX  # 儲存舊滑鼠位置

pygame.quit()