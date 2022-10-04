import pygame
import os
import cv2
import math
import autopy
import numpy as np
import HTMtest as htm
import mediapipe as mp
# 物件導入
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

def draw_start(Keyboard):
    draw_text(screen, "B12_手部辨識飛機射擊遊戲", 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "手指移動飛機......", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "手比 XX 動作 -> 下一頁", 18, WIDTH/2, HEIGHT*3/4)
    waiting = True
    pygame.display.update()
    while waiting:
        # 手勢辨識
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detector.results = detector.hands.process(imgRGB)

        if detector.results.multi_hand_landmarks:
            if len(detector.results.multi_handedness) == 2:
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
                                    cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10,
                                                lineType)  # 印出文字

                    if label == 'Left':
                        fingers = detector.fingersUp()
                        if fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                            print("OK")
                            Keyboard = "Z"

        img = cv2.flip(img, 1)

        cv2.imshow('Image', img)
        # 手勢辨識
        clock.tick(FPS)
        if Keyboard == "Z":
            waiting = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     #按X
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
            elif event.type == pygame.KEYUP:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:    #滑鼠
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            waiting = False

def draw_story(level, Keyboard):
    draw_text(screen, level, 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, "劇情", 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, "手比 XX 動作 -> 下一頁", 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        # 手勢辨識
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detector.results = detector.hands.process(imgRGB)

        if detector.results.multi_hand_landmarks:
            if len(detector.results.multi_handedness) == 2:
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
                                    cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10,
                                                lineType)  # 印出文字

                    if label == 'Left':
                        fingers = detector.fingersUp()
                        if fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                            print("OK")
                            Keyboard = "Z"

        img = cv2.flip(img, 1)

        cv2.imshow('Image', img)
        # 手勢辨識
        clock.tick(FPS)
        if Keyboard == "A":
            waiting = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:     #按X
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
            elif event.type == pygame.KEYUP:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN:    #滑鼠
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            waiting = False

def draw_end(result, player_score, enemy_score, level, Keyboard, once_win):
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
        if Keyboard == "A":
            once_win = True
            waiting = False
        elif Keyboard == "Z" and level != "Level_6.py" and (once_win or result == 'Win'):
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            if level != "Level_6.py":
                os.system(level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:     #按X
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
            elif event.type == pygame.KEYUP:     #按下鍵盤鍵
                if event.key == pygame.K_a:
                    once_win = True
                    waiting = False
                if event.key == pygame.K_z and level != "Level_6.py" and (once_win or result == 'Win'):
                    pygame.quit()
                    cap.release()
                    cv2.destroyAllWindows()
                    if level != "Level_6.py":
                        os.system(level)
            # elif event.type == pygame.MOUSEBUTTONDOWN:    #滑鼠
            #     pressed_array = pygame.mouse.get_pressed()
            #     for index in range(len(pressed_array)):
            #         if pressed_array[index]:
            #             if index == 0:
            #                 waiting = False
            #                 if result == 'Win':
            #                     pygame.quit()
            #                     if level != "Level_5.py":  os.system(level)
        # 手勢辨識
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detector.results = detector.hands.process(imgRGB)

        if detector.results.multi_hand_landmarks:
            if len(detector.results.multi_handedness) == 2:
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
                                    cv2.putText(img, text, (30, 120), fontFace, 5, (255, 255, 255), 10,
                                                lineType)  # 印出文字

                    if label == 'Left':
                        fingers = detector.fingersUp()
                        if fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                            print("OK")
                            Keyboard = "Z"

        img = cv2.flip(img, 1)

        cv2.imshow('Image', img)
        # 手勢辨識