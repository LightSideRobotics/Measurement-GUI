import pygame
import sys
import math
from src.measure import yaw


# 初期化
pygame.init()

# ウィンドウ設定
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arc Example")

# 色設定
background_color = (255, 255, 255)
arc_color = (0, 0, 255)

# 半径と角度
radius = 100
start = math.radians(yaw(0))  # 開始角度 (度)
end = math.radians(yaw(-180))  # 終了角度 (度)

# 座標を中心に設定
center = (width // 2, height // 2)

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 背景を塗りつぶし
    screen.fill(background_color)

    # 弧を描画
    pygame.draw.arc(screen, arc_color, (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                     start,end, 5)

    # 画面を更新
    pygame.display.flip()


'''描く
メモ
ニュートン・ラフソン法を用いて直線から弧を描く
'''