import pygame
import numpy as np
import math,sys,os
from pygame.locals import *
from src.onMap import map
from src.measure import yaw

import pygame.freetype as freetype

# 変数
offset = 0#132
ACTUAL_SIZE = [2362,1143]
MAP_SIZE = (980+offset,538)
SIZE = (MAP_SIZE[0]+200, MAP_SIZE[1]) 
W_TIME = 10   # 待ち時間
THICK  = 3    # 線分の太さ
flag = False      # 線を引いているときTrue
line = []     # 線分リスト
dist = []     # 線分距離リスト
active = False
erase = False
deg = ''
txtBoxColor = (255,255,255)
clock = pygame.time.Clock()
messageTick = pygame.time.get_ticks()
fps = 60

# 初期化
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.scrap.init()
font = pygame.font.SysFont('Courier New', 16)
messageFont = pygame.font.SysFont('Courier New', 14)
title = pygame.font.SysFont('Courier New', 30)
num = pygame.font.SysFont(None, 30)
pygame.display.set_caption("Measuring FLL 2024-2025 Field (mm)")
icon =  pygame.image.load('img\icon.png')
pygame.display.set_icon(icon)
    # Button
reset = pygame.Rect(SIZE[0]-180, 20, 160, 30)
resetTxt = font.render("RESET", True, (0,0,0))
undo = pygame.Rect(SIZE[0]-180,60, 70, 30)
undoTxt = font.render("UNDO", True, (0,0,0))
degTxt = font.render("degrees",True,SIZE[0]-180, 110)
iptDeg = pygame.Rect(SIZE[0]-180, 110, 70, 30) # 角度入力
message = font.render("", False, (255,0,0))


while True:
    # LOADING
    field = pygame.transform.scale(pygame.image.load("img\submargedMap.png"), MAP_SIZE)
    if (pygame.time.get_ticks()-messageTick) > 1000:message = font.render("", False, (255,0,0))

    # DISPLAY
    screen.fill((0, 0, 0))
    screen.blit(field, (0, 0)) # Image
        # Button
    pygame.draw.rect(screen, (194, 32, 71), reset)
    pygame.draw.rect(screen, (255, 200, 71), undo)
    screen.blit(resetTxt, (SIZE[0]-128, 27))
    screen.blit(undoTxt, (SIZE[0]-167, 67))
        # Distance
    for i in range(len(dist)):
        txt = font.render(str(i) + " | " + str(dist[i] if dist[i] != 0 else ACTUAL_SIZE[1]/MAP_SIZE[1]*(np.sqrt((line[i][2]-line[i][0])**2+(line[i][3]-line[i][1])**2)))[:12] , True, (255,255,255))
        screen.blit(txt, (SIZE[0]-180,SIZE[1]/3+i*20))
        # Line
    for pos in line:
        pygame.draw.line(screen, (50,150,0), (pos[0],pos[1]), (pos[2],pos[3]), THICK)
        # Number
    for i in range(len(line)):
        pos = line[i]
        screen.blit(num.render(str(i) , True, (255,0,0)),(pos[0],pos[1]))
        # TextBox
    pygame.draw.rect(screen, (0,255,0) if active else (255,255,255), iptDeg, 2)
    if deg:
        screen.blit(font.render(deg, True, (255,255,255)), (iptDeg.x + 5, iptDeg.y + 5))
    screen.blit(message,message.get_rect(center=(SIZE[0]-100,155)))
    
    pygame.display.update()

    # INPUT
    for event in pygame.event.get():
        # DOWN
        if event.type == MOUSEBUTTONDOWN:
            posM = event.pos
            if event.button == 1 and not posM[0] > MAP_SIZE[0]: # LEFT  開始 and 継続
                if flag:#marking
                    if map.check(x2):
                        # 記録
                        if x1 == x2 and y1 == y2:
                            print(x1,x2,y1,y2)
                            line.pop()
                            dist.pop()
                        else:
                            line[-1] = ([x1,y1,x2,y2])
                            pixel = np.sqrt((line[i][2]-line[i][0])**2+(line[i][3]-line[i][1])**2)
                            dist[-1] = ACTUAL_SIZE[1]/MAP_SIZE[1]*pixel
                    if deg:
                        if math.tan(math.radians(int(yaw(deg)))) > 1:
                            pygame.mouse.set_pos(x2,y1-round(1/math.tan(math.radians(yaw(deg)))*(x2-x1),3))
                        else:
                            pygame.mouse.set_pos(x1-round(math.tan(math.radians(yaw(deg)))*(y2-y1),3),y2)
                    x1,y1 = x2,y2
                    flag = True
                    if map.check(x1):
                        # 記録
                        # リストに追加
                        line.append([x1,y1,x1,y1])
                        dist.append(0)
                else:
                    x1,y1 = posM
                    flag = True
                    if map.check(x1):
                        # 記録
                        # リストに追加
                        line.append([x1,y1,x1,y1])
                        dist.append(0)
            if event.button == 3 and flag: # RIGHT 終了
                if map.check(x2):
                    # 記録
                    flag = False
                    if x1 != x2 and y1 != y2:
                        line[-1] = ([x1,y1,x2,y2])
                        pixel = np.sqrt((line[i][2]-line[i][0])**2+(line[i][3]-line[i][1])**2)
                        dist[-1] = ACTUAL_SIZE[1]/MAP_SIZE[1]*pixel
                    else:
                        line.pop()
                        dist.pop()
            if reset.collidepoint(posM):#CLEAR
                line.clear()
                dist.clear()
            if undo.collidepoint(posM): # UNDO
                try:
                    line.pop()
                    dist.pop()
                except IndexError:pass
            if SIZE[0]-posM[0] < 200 and posM[1]>SIZE[1]/3: # COPY distance
                try:
                    pygame.scrap.put(SCRAP_TEXT, str(dist[int((posM[1] - SIZE[1]/3)//20)]).encode())
                    print((posM[1] - SIZE[1]/3)//20,str(dist[int((posM[1] - SIZE[1]/3)//20)]))
                except IndexError:
                    message = messageFont.render("There's noting there", True, (255,0,0))
                    messageTick = pygame.time.get_ticks()
            active = not active if iptDeg.collidepoint(event.pos) else False

        # MOTION
        if flag and event.type == MOUSEMOTION:
            x2,y2 = event.pos
            if deg:#マウス角度制限
                if math.tan(math.radians(float(yaw(deg)))) > 1:
                    x2,y2 = x2,y1-round(1/math.tan(math.radians(yaw(deg)))*(x2-x1),3)
                else:
                    x2,y2 = x1-round(math.tan(math.radians(yaw(deg)))*(y2-y1),3),y2
            if x2 > MAP_SIZE[0]:
                pygame.mouse.set_pos((MAP_SIZE[0], y2))
                x2 = MAP_SIZE[0]
            if line:line[-1] = [x1,y1,x2,y2]

        # Keyboard
        # DOWN 
        if event.type == KEYDOWN:
            if event.key == K_z and pygame.key.get_mods() & KMOD_LCTRL:
                try:
                    line.pop()
                    dist.pop()
                except IndexError:pass
            if active:
                if event.key == K_BACKSPACE:
                    deg = deg[:-1]
                elif (event.unicode.isdigit() or event.key == K_MINUS) and len(str(abs(int(deg if deg.isdigit() else 0)))) < 3:
                    deg += event.unicode
            if event.key == K_TAB:
                if not active:deg = ''
                active = not active
            if event.key == K_KP_ENTER:
                active = False
        # FINISH
        if event.type == QUIT:  
            pygame.quit()
            sys.exit()
    clock.tick(fps)