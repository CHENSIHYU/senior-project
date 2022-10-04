import pygame
import os
import time
import pyautogui
import Draw as fuc
import cv2
import math
import autopy
import numpy as np
import HTMtest as htm
import mediapipe as mp

# 物件導入
from Background import Background
from Bullet import Bullet
from Enemy_Bullet import Enemy_Bullet
from Player import Player
from Enemy import Enemy
from Explosion import Explosion
from pynput.keyboard import Key, Controller
from google.protobuf.json_format import MessageToDict

detector = htm.HandDetector(detectionCon=0.8, maxHands=2)
pTime = 0
mpHands = mp.solutions.hands
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

wScr, hScr = autopy.screen.size()

fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 印出文字的字型
lineType = cv2.LINE_AA

pTime = 0
wCam, hCam = 640, 480
frameR = 100
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0

keyboard = Controller()

pygame.init()

# 設定好就不會輕易改變的變數用大寫
FPS = 60
WIDTH = 1280
HEIGHT = 800
deduction = 10
enemy_number = 3
score = [100, 50, 50, 50]
coll = 0
delay = 0
oM = 0
Start_Game = True
Story_Game = False
End_Game = False
result = '無'
once_win = False
Keyboard = "Null"
Keyboard_Space_Speed = 0

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("B12_手部辨識飛機射擊遊戲")

clock = pygame.time.Clock()
running = True

# 鼠標顯示設定
# pygame.mouse.set_visible(False)
# pygame.event.set_grab(True)




def player_shoot(Keyboard):
    if Keyboard == "Space":
        player_bullet = Bullet(player.rect.centerx, player.rect.top)
        all_sprites.add(player_bullet)
        player_bullets.add(player_bullet)
        Keyboard = "Null"
        return Keyboard

def player_control_Keyboard_and_Mouse():
    if event.type == pygame.KEYDOWN:  # 按下鍵盤鍵
        if event.key == pygame.K_SPACE:
            player_bullet = Bullet(player.rect.centerx, player.rect.top)
            all_sprites.add(player_bullet)
            player_bullets.add(player_bullet)
        # if event.key == pygame.K_p:
        #    enemy.shoot()
    elif event.type == pygame.MOUSEBUTTONDOWN:  # 滑鼠
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

def getHit(score, enemy_is_exist):
    # draw_text(screen, str("now is hitting"), 18, 100, 10)
    player_hits = pygame.sprite.spritecollide(player, enemy_bullets, True,
                                              pygame.sprite.collide_circle)  # False：不要刪掉 player
    # for i in range(enemy_number):
    #     if i == 0:
    #         enemy_hits = pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)
    #     else: enemy_hits += pygame.sprite.spritecollide(enemy[i], player_bullets, True, pygame.sprite.collide_circle)

    IsBreak = False
    if score[0] == 0 or (score[1] == 0 and score[2] == 0 and score[3] == 0):
        IsBreak = True

    ## 分數
    for hit in player_hits:
        if IsBreak: break
        score[0] -= deduction
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
    if enemy_is_exist[0]:
        enemy0_hits = pygame.sprite.spritecollide(enemy[0], player_bullets, True, pygame.sprite.collide_circle)
        for hit in enemy0_hits:
            if IsBreak: break
            score[1] -= deduction
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
    if enemy_is_exist[1]:
        enemy1_hits = pygame.sprite.spritecollide(enemy[1], player_bullets, True, pygame.sprite.collide_circle)
        for hit in enemy1_hits:
            if IsBreak: break
            score[2] -= deduction
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
    if enemy_is_exist[2]:
        enemy2_hits = pygame.sprite.spritecollide(enemy[2], player_bullets, True, pygame.sprite.collide_circle)
        for hit in enemy2_hits:
            if IsBreak: break
            score[3] -= deduction
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)

    # 使分數不小於 0
    for i in range(enemy_number + 1):
        if score[i] <= 0:
            score[i] = 0

    return score

def getColl(coll):
    close_hits = pygame.sprite.spritecollide(player, enemy_group, True, pygame.sprite.collide_circle)
    if close_hits:
        expl = Explosion(close_hits[0].rect.center, 'lg')
        all_sprites.add(expl)
        coll = 1
    return coll

# 手部辨識
# 根據兩點的座標，計算角度
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 180
    return angle_


# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        (((hand_[0][0]) - (hand_[2][0])), ((hand_[0][1]) - (hand_[2][1]))),
        (((hand_[3][0]) - (hand_[4][0])), ((hand_[3][1]) - (hand_[4][1])))
    )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        (((hand_[0][0]) - (hand_[6][0])), ((hand_[0][1]) - (hand_[6][1]))),
        (((hand_[7][0]) - (hand_[8][0])), ((hand_[7][1]) - (hand_[8][1])))
    )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        (((hand_[0][0]) - (hand_[10][0])), ((hand_[0][1]) - (hand_[10][1]))),
        (((hand_[11][0]) - (hand_[12][0])), ((hand_[11][1]) - (hand_[12][1])))
    )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        (((hand_[0][0]) - (hand_[14][0])), ((hand_[0][1]) - (hand_[14][1]))),
        (((hand_[15][0]) - (hand_[16][0])), ((hand_[15][1]) - (hand_[16][1])))
    )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        (((hand_[0][0]) - (hand_[18][0])), ((hand_[0][1]) - (hand_[18][1]))),
        (((hand_[19][0]) - (hand_[20][0])), ((hand_[19][1]) - (hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list


# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(finger_angle):
    f1 = finger_angle[0]  # 大拇指角度
    f2 = finger_angle[1]  # 食指角度
    f3 = finger_angle[2]  # 中指角度
    f4 = finger_angle[3]  # 無名指角度
    f5 = finger_angle[4]  # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1 >= 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return '0'
    elif f1 >= 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return ' '
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return '2'
    elif f1 >= 50 and f2 >= 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return 'ok'
    elif f1 < 50 and f2 >= 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return 'ok'
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 > 50:
        return '3'
    elif f1 >= 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return '4'
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 < 50:
        return '5'
    elif f1 < 50 and f2 >= 50 and f3 >= 50 and f4 >= 50 and f5 < 50:
        return '6'
    elif f1 < 50 and f2 < 50 and f3 >= 50 and f4 >= 50 and f5 >= 50:
        return '7'
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 >= 50 and f5 >= 50:
        return '8'
    elif f1 < 50 and f2 < 50 and f3 < 50 and f4 < 50 and f5 >= 50:
        return '9'
    else:
        return ''


# 手部辨識

# 建立 sprit 群組
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# 建立物件
bg1 = Background()
bg2 = Background(is_alt=True)
player = Player()
enemy = [0] * enemy_number
enemy[0] = Enemy(WIDTH / 4, 75, "mid")
enemy[1] = Enemy(WIDTH / 2, 75, "mid")
enemy[2] = Enemy(WIDTH * 3 / 4, 75, "mid")

# 加入群組
all_sprites.add(bg1, bg2)
all_sprites.add(player)
enemy_is_exist = [0] * enemy_number
for i in range(enemy_number):
    all_sprites.add(enemy[i])
    enemy_is_exist[i] = True
enemy_group.add(enemy)

while running:
    if Start_Game:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        fuc.draw_start(Keyboard)
        Start_Game = False
        Story_Game = True
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    if Story_Game:
        fuc.draw_story("Level_1", Keyboard)
        Story_Game = False
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    if End_Game:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # 初始化
        score = [100, 50, 50, 50]
        coll = 0
        delay = 0
        oM = 0
        Start_Game = True
        Story_Game = False
        End_Game = False
        result = '無'
        Keyboard = "Null"
        Keyboard_Space_Speed = 0
        # 建立 sprit 群組
        all_sprites = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        enemy_bullets = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        # 建立物件
        bg1 = Background()
        bg2 = Background(is_alt=True)
        player = Player()
        enemy = [0] * 3
        enemy[0] = Enemy(WIDTH / 4, 75, "mid")
        enemy[1] = Enemy(WIDTH / 2, 75, "mid")
        enemy[2] = Enemy(WIDTH * 3 / 4, 75, "mid")
        # 加入群組
        all_sprites.add(bg1, bg2)
        all_sprites.add(player)
        enemy_is_exist = [0] * enemy_number
        for i in range(enemy_number):
            all_sprites.add(enemy[i])
            enemy_is_exist[i] = True
        enemy_group.add(enemy)

    clock.tick(FPS)

    # 手勢辨識
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    detector.results = detector.hands.process(imgRGB)

    if detector.results.multi_hand_landmarks:
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 0), 2)
        # for handLms in detector.results.multi_hand_landmarks:
        # if draw:
        # detector.mpDraw.draw_landmarks(img, handLms, detector.mpHands.HAND_CONNECTIONS)

        if len(detector.results.multi_handedness) == 2:
            # cv2.putText(img, 'Both Hands', (250, 50), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 255, 0), 2)
            # else:
            for i in detector.results.multi_handedness:
                lmList, bbox = detector.findPosition(img)
                x1, y1 = lmList[8][1:]
                # Return whether it is Right or Left Hand
                label = MessageToDict(i)['classification'][0]['label']
                if label == 'Right':
                    if detector.results.multi_hand_landmarks:
                        for hand_landmarks in detector.results.multi_hand_landmarks:
                            finger_points = []  # 記錄手指節點座標的串列
                            for i in hand_landmarks.landmark:
                                # 將 21 個節點換算成座標，記錄到 finger_points
                                x = i.x * wCam
                                y = i.y * hCam
                                finger_points.append((x, y))
                            if finger_points:
                                finger_angle = hand_angle(finger_points)  # 計算手指角度，回傳長度為 5 的串列
                                # print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                                text = hand_pos(finger_angle)  # 取得手勢所回傳的內容
                                #cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10, lineType)  # 印出文字

                if label == 'Left':
                    fingers = detector.fingersUp()
                    if fingers[1] == 1 and fingers[2] == 0:
                        # 5. Convert Coordinates

                        x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                        y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                        # 6. Smooth Values
                        clocX = plocX + (x3 - plocX) / smoothening
                        clocY = plocY + (y3 - plocY) / smoothening
                        # 7. Move Mouse
                        autopy.mouse.move(wScr - clocX, clocY)
                        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
                        plocX, plocY = clocX, clocY
                    if fingers[1] == 1 and fingers[3] == 0 and fingers[4] == 1:
                        # keyboard.press(Key.space)
                        Keyboard = "Space"

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    img = cv2.flip(img, 1)
    cv2.putText(img, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow('Image', img)

        #手勢辨識

    if result == '無':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 按X
                running = False
            player_control_Keyboard_and_Mouse()
        # 取得玩家輸入 & Space 控制
        if Keyboard_Space_Speed >= 7:
            Keyboard = player_shoot(Keyboard)
            Keyboard_Space_Speed = 0
        # 左右轉移動動畫
        mX, mY = pyautogui.position()  # 滑鼠目前位置
        player.animate(mX, oM)

    delay += 1
    Keyboard_Space_Speed += 1

    # 敵人分數 == 0 => 刪掉敵人物件
    for i in range(enemy_number):
        if score[i + 1] == 0:
            enemy[i].kill()
            enemy_is_exist[i] = False

    # 分數判斷
    score = getHit(score, enemy_is_exist)
    # 互撞判斷
    coll = getColl(coll)

    # Ending
    enemy_total_score = 0
    for i in range(1, enemy_number + 1):
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
        fuc.draw_end(result, score[0], enemy_total_score, "Level_2.py", Keyboard, once_win)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        delay = 0
        cap.release()
        cv2.destroyAllWindows()
    if delay == -1 and result == 'Fail':
        End_Game = True
        fuc.draw_text(screen, "Fail", 64, WIDTH / 2, HEIGHT / 2)
        fuc.draw_end(result, score[0], enemy_total_score, "Level_2.py", Keyboard, once_win)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        delay = 0
        cap.release()
        cv2.destroyAllWindows()
    if delay == -1 and result == 'Tie':
        End_Game = True
        fuc.draw_text(screen, "Tie", 64, WIDTH / 2, HEIGHT / 2)
        fuc.draw_end(result, score[0], enemy_total_score, "Level_2.py", Keyboard, once_win)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        delay = 0
        cap.release()
        cv2.destroyAllWindows()

    # 更新遊戲
    all_sprites.update()

    # 渲染/顯示遊戲畫面
    if End_Game == False and Start_Game == False and Story_Game == False:
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

    # 更新遊戲
    pygame.display.update()

    oM = mX  # 儲存舊滑鼠位置
