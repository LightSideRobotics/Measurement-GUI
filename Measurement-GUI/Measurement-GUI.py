import pygame
import numpy as np
import sys
import os
from pygame.locals import *
from src.onMap import map
from src.typeIn import box

# 変数
offset = 132
ACTUAL_SIZE = [2362,1143]
MAP_SIZE = (980+offset,538)
SIZE = (MAP_SIZE[0]+200, MAP_SIZE[1]) 
W_TIME = 10   # 待ち時間
THICK  = 5    # 線分の太さ
flag = 0      # ボタン押下フラグ
line = []     # 線分リスト
dist = []     # 線分距離リスト
clock = pygame.time.Clock()
fps = 60

# 初期化
pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.scrap.init()
font = pygame.font.SysFont('Courier New', 16)
title = pygame.font.SysFont('Courier New', 30)
num = pygame.font.SysFont(None, 30)
pygame.display.set_caption("Measuring FLL 2024-2025 Field (mm)")
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

reset = pygame.Rect(SIZE[0]-180, 20, 160, 50)
resetTxt = font.render("RESET", True, (0,0,0))
undo = pygame.Rect(SIZE[0]-180,80, 60, 50)
undoTxt = font.render("UNDO", True, (0,0,0))

while True:
    #loading
    field = pygame.transform.scale(pygame.image.load("img\submargedMap.png"), MAP_SIZE)

    #display
    screen.fill((0, 0, 0))
    screen.blit(field, (0, 0)) # Image
        # Button
    pygame.draw.rect(screen, (194, 32, 71), reset)
    pygame.draw.rect(screen, (255, 200, 71), undo)
    screen.blit(resetTxt, (SIZE[0]-128, 37))
    screen.blit(undoTxt, (SIZE[0]-172, 97))
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
        screen.blit(num.render(str(i) , True, (255,0,255)),(pos[0],pos[1]))
    pygame.display.update()

    for event in pygame.event.get(): # INPUT
        # DOWN
        if event.type == MOUSEBUTTONDOWN:
            posM = event.pos
            if event.button == 1: # LEFT
                x1,y1 = posM
                if map.check(x1):
                    # 記録
                    flag = 1
                    # リストに追加
                    line.append([x1,y1,x1,y1])
                    dist.append(0)
            if event.button == 3 and flag==1: # LEFT
                x2,y2 = event.pos
                if map.check(x2):
                    # 記録
                    if x1 != x2 and y1 != y2:
                        line[-1] = ([x1,y1,x2,y2])
                        pixel = np.sqrt((line[i][2]-line[i][0])**2+(line[i][3]-line[i][1])**2)
                        dist[-1] = ACTUAL_SIZE[1]/MAP_SIZE[1]*pixel
                    else:
                        line.pop()
                        dist.pop()
                x1,y1 = posM
                if map.check(x1):
                    # 記録
                    # リストに追加
                    line.append([x1,y1,x1,y1])
                    dist.append(0)
            if reset.collidepoint(posM):
                line.clear()
                dist.clear()
            if undo.collidepoint(posM): # UNDO
                try:
                    line.pop()
                    dist.pop()
                except IndexError:pass
            if SIZE[0]-posM[0] < 200 and posM[1]>SIZE[1]/3:
                print((posM[1] - SIZE[1]/3)//20)
                pygame.scrap.put(SCRAP_TEXT, str(dist[int((posM[1] - SIZE[1]/3)//20)]).encode())

        # MOTION
        if flag == 1 and event.type == MOUSEMOTION:
            x2,y2 = event.pos
            if x2 > MAP_SIZE[0]:
                pygame.mouse.set_pos((MAP_SIZE[0], y2))
                x2 = MAP_SIZE[0]
            try:
                line[-1] = [x1,y1,x2,y2]
            except IndexError:pass
        # UP
        if event.type == MOUSEBUTTONUP and event.button == 1:
            x2,y2 = event.pos
            if map.check(x2):
                # 記録
                flag = 0
                if x1 != x2 and y1 != y2:
                    line[-1] = ([x1,y1,x2,y2])
                    pixel = np.sqrt((line[i][2]-line[i][0])**2+(line[i][3]-line[i][1])**2)
                    dist[-1] = ACTUAL_SIZE[1]/MAP_SIZE[1]*pixel
                else:
                    line.pop()
                    dist.pop()

        if event.type == KEYDOWN:
            if event.key == K_z and pygame.key.get_mods() & KMOD_LCTRL:
                try:
                    line.pop()
                    dist.pop()
                except IndexError:pass
        # FINISH
        if event.type == QUIT:  
            pygame.quit()
            sys.exit()
    clock.tick(fps)