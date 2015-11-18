__author__ = 'Min'

from pico2d import *

name = "Land"

leftBottomX = 0
leftBottomY = 0
width = 0
height = 0

class Land:
    def draw(leftBottomX, leftBottomY, width, height):
        draw_fill_rectangle(leftBottomX, leftBottomY, width, height)

