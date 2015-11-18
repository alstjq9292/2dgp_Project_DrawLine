
import sys
import random
import json
import os

import game_framework
import title_state
import stargoal
from pico2d import *

from Land import Land

name = "MainState"
is_goal = True
frame = 0
x, y = 0, 0
isMouseClicked = False
'''
#속도 관련 변수
PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#시간 관련 변수
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAME_PER_ACTION = 8
'''
# 마우스 좌표 저장에 대한 리스트 
MouseList = []
ColorList = [[217, 65, 197], [165, 102, 255], [71, 200, 62], [92, 209, 229]]

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
            #self.x += RUN_SPEED_PPS
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

class Stargoal:
    image = None

    PIXEL_PER_METER = (10.0 / 0.1) # 10 pixel 10 cm
    RUN_SPEED_KMPH = 20.0
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAME_PER_ACTION = 8

    def __init__(self):
        self.x, self.y = 750, 200
        self.frame = random.randint(0,7)
        self.total_frames = 0.0
        if self.image == None:
            self.image = load_image('resource/stargoal_animation.png')

    def update(self, frame_time):
        distance = stargoal.RUN_SPEED_PPS * frame_time
        self.total_frames += stargoal.FRAME_PER_ACTION * stargoal.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8


    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


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
    global maincharacter, background, startbutton, land, stargoal
    maincharacter = Main_character()
    background = Background()
    startbutton = Start_button()
    stargoal = Stargoal()

def exit():
    global maincharacter, background, startbutton, land, stargoal
    del(maincharacter)
    del(background)
    del(startbutton)
    del(stargoal)

current_time = 0.0

def get_frame_time():

    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time

def pause():
    pass

def resume():
    pass

def handle_events():
    global isMouseClicked, MouseList, maincharacter, stargoal, is_goal, frame
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
            is_goal = False
        elif event.type == SDL_MOUSEMOTION:
            if(isMouseClicked) :
                MouseList.append([event.x, 600 - event.y, random.randint(0, 3)])
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.change_state(title_state)
        elif (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
            isMouseClicked = True
            print(event.x, 600 - event.y)
        elif (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
            isMouseClicked = False


def update():
    maincharacter.update()
    stargoal.update(get_frame_time())

def draw():
    global MouseList

    clear_canvas()
    background.draw()
    maincharacter.draw()
    startbutton.draw()
    stargoal.draw()

    for i, d in enumerate(MouseList):
        if (i > 0):
            drawLine(MouseList[i - 1][0], MouseList[i-1][1], MouseList[i][0], MouseList[i][1],
                     ColorList[MouseList[i][2]][0], ColorList[MouseList[i][2]][1], ColorList[MouseList[i][2]][2])

    Land.draw_rect(0, 0, 340, 160)
    Land.draw_rect(460, 0, 340, 160)

    update_canvas()


def main():

    global running
    global current_time

    running = True
    current_time = get_time()

    while running:
        frame_time = get_frame_time()
        handle_events()
        stargoal.update(frame_time)

        clear_canvas()
        stargoal.draw()
        update_canvas()

if __name__ == '__main__':
    main()