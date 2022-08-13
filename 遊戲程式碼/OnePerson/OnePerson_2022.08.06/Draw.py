import pygame
import os
# 物件導入
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
BAR_LENGTH = 160
BAR_HEIGHT = 20
result = '無'
level = 0

# color
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

# 引入字體 => 從目前程式執行之電腦尋找
# font_name = pygame.font.match_font('Calibri')
font_name = os.path.join("font.ttf")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)  # 改字體大小
    text_surface = font.render(text, True, WHITE)  # 製作文字圖片
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)  #將文字畫到屏幕上

def draw_health(surf, score_org, hp, x, y):
    if hp < 0:    hp = 0
    fill = (hp/score_org) * BAR_LENGTH    # 剩餘的生命條
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)    # 生命條內框
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)    # 生命條外框
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)    # 2 是像素

def draw_start():
    draw_text(screen, "B12_手部辨識飛機射擊遊戲", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "手指移動飛機......", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "手比 XX 動作 -> 下一頁", 18, WIDTH/2, HEIGHT*3/4)
    waiting = True
    pygame.display.update()
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     #按X
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:    #滑鼠
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            waiting = False

def draw_story(level):
    draw_text(screen, level, 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "劇情", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "手比 XX 動作 -> 下一頁", 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     #按X
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:    #滑鼠
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            waiting = False

def draw_end(result, player_score, enemy_score, level, once_win):
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    screen_rect = pygame.Rect(0,0,WIDTH,HEIGHT)
    player_score = 'Player' + str(player_score)
    enemy_score = 'Enemy' + str(enemy_score)
    draw_text(screen, player_score, 64, WIDTH/2, HEIGHT/6)
    draw_text(screen, enemy_score, 64, WIDTH/2, HEIGHT/4)
    if result == 'Win':
        draw_text(screen, "Win", 64, WIDTH/2, HEIGHT/2)
    elif result == 'Fail':
        draw_text(screen, "Fail", 64, WIDTH/2, HEIGHT/2)
    elif result == 'Tie':
        draw_text(screen, "Tie", 64, WIDTH/2, HEIGHT/2)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     #按X
                pygame.quit()
            elif event.type == pygame.KEYUP:     #按下鍵盤鍵
                if event.key == pygame.K_a:
                    once_win = True
                    waiting = False
                if event.key == pygame.K_z and level != "Level_6.py" and (once_win or result == 'Win'):
                    pygame.quit()
                    os.system(level)
                if level == "Level_6.py":
                    pygame.quit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:    #滑鼠
            #     pressed_array = pygame.mouse.get_pressed()
            #     for index in range(len(pressed_array)):
            #         if pressed_array[index]:
            #             if index == 0:
            #                 waiting = False
            #                 if result == 'Win':
            #                     pygame.quit()
            #                     if level != "Level_5.py":  os.system(level)