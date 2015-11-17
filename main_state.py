
import sys
import random
import json
import os

import game_framework
import title_state
from pico2d import *

name = "MainState"
running = None
x, y = 0, 0
isMouseClicked = False

PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# 마우스 좌표 저장에 대한 리스트
MouseList = []

class Background:
    def __init__(self):
        self.image = load_image('resource/game_background.png')

    def draw(self):
        self.image.draw(400,300)



class Main_character:
    image = None

    STAND, GO_RIGHT = 0, 1

    def __init__(self):


        self.x, self.y = 50, 183
        self.state = self.STAND
        if self.image == None:
            self.image = load_image('resource/main_character.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def handle_go_right(self):
        if self.state == self.GO_RIGHT:
            self.x += RUN_SPEED_PPS
            if self.x > 800:
                self.x = 800

    def handle_stand(self):
        if self.state == self.STAND:
            self.x += 0

    handle_state = {
        GO_RIGHT: handle_go_right,
        STAND: handle_stand
    }
    def update(self):
        self.handle_state[self.state](self)

class Ground:
    def __init__(self):
        self.image = load_image('resource/ground.png')

    def draw(self):
        self.image.draw(400,300)

class Start_button:
    image = None

    def __init__(self):
        self.x, self.y = 50, 550
        if self.image == None:
            self.image = load_image('resource/start_button.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

def enter():
    global maincharacter, background, startbutton, ground
    maincharacter = Main_character()
    background = Background()
    startbutton = Start_button()
    ground = Ground()

def exit():
    global maincharacter, background, startbutton, ground
    del(maincharacter)
    del(background)
    del(startbutton)
    del(ground)

def pause():
    pass

def resume():
    pass

def handle_events():
    global isMouseClicked, MouseList, maincharacter
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            if(isMouseClicked) :
                MouseList.append([event.x, 600 - event.y])
                print("마우스 이동 중", event.x, 600 - event.y)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            print("마우스 버튼 누름", event.x, 600 - event.y)
            isMouseClicked = True
            #dot_drawing()
        elif (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
            print("마우스 버튼 업", event.x, 600 - event.y)
            isMouseClicked = False

def update():
    maincharacter.update()


def draw():
    global MouseList

    clear_canvas()
    background.draw()
    maincharacter.draw()
    startbutton.draw()
    ground.draw()

    for d in MouseList:
        draw_rectangle(d[0], d[1], d[0] + 1, d[1] + 1)


    update_canvas()

