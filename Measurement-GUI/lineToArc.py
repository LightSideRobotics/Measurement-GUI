import pygame
import sys
import math

# 初期化
pygame.init()

# ウィンドウ設定
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Arc Based on Line Example")

# 色設定
background_color = (255, 255, 255)
line_color = (0, 0, 0)
arc_color = (0, 0, 255)

# 直線の開始点と終了点
start_point = (200, 300)
end_point = (600, 300)

# 半径と角度
radius = 100
start_angle = 0  # 開始角度 (度)
end_angle = 180  # 終了角度 (度)

# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 背景を塗りつぶし
    screen.fill(background_color)

    # 直線を描画
    pygame.draw.line(screen, line_color, start_point, end_point, 5)

    # 直線の中心を計算
    center_x = (start_point[0] + end_point[0]) // 2
    center_y = start_point[1] - radius  # 弧を上に描く

    # 弧を描画
    start_angle_rad = math.radians(start_angle)  # ラジアンに変換
    end_angle_rad = math.radians(end_angle)      # ラジアンに変換
    pygame.draw.arc(screen, arc_color, (center_x - radius, center_y - radius, radius * 2, radius * 2),
                     start_angle_rad, end_angle_rad, 5)

    # 画面を更新
    pygame.display.flip()