# region import
from ast import Global
from cProfile import run
from ctypes import memset, sizeof
from json import load
from time import sleep
from turtle import left, pos
import pygame
import os
import socket
import threading
from threading import Timer
from ServerPlayers import Player
from ServerPlayers import Enemy
from PrintOnScreen import write_text
import GlobalPosition
# endregion
# region 參數
# 遊戲參數
FPS = 60    #一秒內遊戲更新的次數
WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
cx = 0
cy = 0
# 連線參數
HEADER = 1024
PORT = 888
# SERVER = ""
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
GlobalPosition.initial()
#endregion
clock = pygame.time.Clock() #管理遊戲的時間
#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小
pygame.display.set_caption("ServerGame")   #視窗名稱
# region 載入背景圖片
background_img = pygame.image.load(os.path.join("image", "background.png")).convert()    #convert轉換成pygame容易讀取的格式
background02_img = pygame.image.load(os.path.join("image", "background.png")).convert()
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 0, -700    #背景2初始位置
# endregion
# region sprite群組 可以放進sprite的物件
all_sprites = pygame.sprite.Group()
player = Player(GlobalPosition.ServerX, 650)
enemy = Enemy(int(cx), int(cy))
all_sprites.add(player) #把物件放進group裡
all_sprites.add(enemy) #把物件放進group裡
# endregion

#server傳送
def handle_client(conn, addr):
    global cx, cy
    print(f"-----[NEW CONNECTION] {addr} connected.-----")
    conn.send(f"-----{addr}Connect success-----".encode(FORMAT))

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        planex = player.rect.centerx
        planey = player.rect.centery
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            print(f"client msg: {msg}")
            print("type", type(msg))
            newMsg = msg.split(',')
            print("Clientpos:" , newMsg)
            print("type", type(newMsg))

            conn.send(f"{planex} , {planey}".encode(FORMAT))

            cx = newMsg[0]
            cy = newMsg[1]

        sleep(0.01) #0.01傳送一次
    
    conn.close()

def start():
    global cx, cy #clientPos
    global x0, x1, y0, y1 #背景初始位置
    
    server.listen()
    print(f"[LISTENING] Server is listening on {PORT}")
    conn, addr = server.accept()     
    
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

    #遊戲迴圈
    running = True
    while running:
        clock.tick(FPS)  #一秒內最多的執行次數

        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                running = False

        pos = pygame.mouse.get_pos()
        #更新遊戲
        if(pos[0] != 0 or pos[1] != 0):
            player.update(pos[0], pos[1])
            player.animate(pos[0], pos[1])
        enemy.update(int(cx), int(cy))
        enemy.animate(int(cx), int(cy))

        planex = player.rect.centerx
        planey = player.rect.centery

        #背景移動
        y1 += 5
        y0 += 5
        screen.blit(pygame.transform.scale(background_img, (500, 700)), (x0, y0))
        screen.blit(pygame.transform.scale(background_img, (500, 700)), (x1, y1))
        if y0 > 700:    y0 = -700   #圖片到底就重新放回上方
        if y1 > 700:    y1 = -700

        all_sprites.draw(screen)    #把sprites的東西都畫到screen上
        write_text(screen, "mx: " + str(planex), 22, 70, 30)
        write_text(screen, "my: " + str(planey), 22, 70, 50)
        write_text(screen,"ClientPosx:" + str(cx), 22, 100, 70)
        write_text(screen,"ClientPosy:" + str(cy), 22, 100, 90)
        write_text(screen,"GlobalSX:" + str(GlobalPosition.ServerX), 22, 100, 110)
        write_text(screen,"GlobalCX:" + str(GlobalPosition.ServerEnemy), 22, 100, 130)
        
        pygame.display.flip()
        pygame.display.update()
        
    pygame.quit()
        
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
print("ADDR:", ADDR)
print("[STARTING] server is starting...")
start()