import pygame
import numpy as np
import sys
import os
from pygame.locals import *

def yaw(deg):# 入力はロボット角度系
    deg = float(deg) if deg!='-' else 0
    #print((450- deg)%360)
    # 360度表記にして逆転、90度足す
    return (450- deg if deg<0 else deg+360)%360