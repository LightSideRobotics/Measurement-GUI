import sys
import pygame
from pygame.locals import *

class map(object):
    def __init__(self):
        pass
    
    def check(pos,limit=1112):
        if pos < 1112:
            return True
        else:
            return False