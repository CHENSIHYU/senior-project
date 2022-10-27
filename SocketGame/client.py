# region import
import socket
from threading import Timer
from cProfile import run
from json import load
from turtle import left
import pygame
import os
from ClientPlayers import Player
from ClientPlayers import Enemy
from PrintOnScreen import write_text
import GlobalPosition
#endregion

# region 參數
# 遊戲參數
FPS = 60    #一秒內遊戲更新的次數
WIDTH = 500
HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
sx = 0
sy = 0
# 連線參數
HEADER = 1024
PORT = 888
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = ""
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
GlobalPosition.initial()
# endregion

clock = pygame.time.Clock() #管理遊戲的時間
#初始化&創建視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))   #設定視窗大小
pygame.display.set_caption("ClientWindow")   #視窗名稱

# region 載入背景圖片
background_img = pygame.image.load(os.path.join("image", "background.png")).convert()    #convert轉換成pygame容易讀取的格式
background02_img = pygame.image.load(os.path.join("image", "background.png")).convert()
background_size = background_img.get_size()
background_rect = background_img.get_rect()
x0, y0 = 0, 0   #背景1初始位置
x1, y1 = 0, -700    #背景2初始位置
# endregion

#region sprite群組 可以放進sprite的物件
all_sprites = pygame.sprite.Group()
player = Player(GlobalPosition.ClientX, 70)
enemy = Enemy(int(sx), int(sy))
all_sprites.add(player) #把物件放進group裡
all_sprites.add(enemy) #把物件放進group裡
# endregion

#client傳送
def send(msg):
    global sx, sy
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    servermsg = client.recv(HEADER).decode(FORMAT)

    print("Serverpos:" + servermsg)
    print("type", type(servermsg))
    newMsg = servermsg.split(',')
    print("Serverpos:" , newMsg)
    print("type", type(newMsg))
    
    sx = newMsg[0]
    sy = newMsg[1]
    
def gmaeRun():
    global sx, sy  #serverPos
    global x0, x1, y0, y1 #背景初始位置

    # pos = pygame.mouse.get_pos()
    send(f"250, 70") #遊戲前傳送一次座標
    
    #遊戲迴圈
    run = True
    while run:
        clock.tick(FPS)  #一秒內最多的執行次數

        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #關閉視窗
                run = False

        pos = pygame.mouse.get_pos()
        #更新遊戲
        if(pos[0] != 0 or pos[1] != 0):
            player.update(pos[0], pos[1])
            player.animate(pos[0], pos[1])
        enemy.update(int(sx), int(sy))
        enemy.animate(int(sx), int(sy))
        
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
        write_text(screen, "serverPosx: " + str(sx) , 22, 100, 70)
        write_text(screen, "serverPosy: " + str(sy) , 22, 100, 90)
        write_text(screen,"GlobalSX:" + str(GlobalPosition.ClientEnemy), 22, 100, 110)
        write_text(screen,"GlobalCX:" + str(GlobalPosition.ClientX), 22, 100, 130)
        
        pygame.display.flip()
        pygame.display.update()
        send(f"{planex}, {planey}") #遊戲內持續傳送
    
    pygame.quit()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print(client.recv(HEADER).decode(FORMAT))
gmaeRun()