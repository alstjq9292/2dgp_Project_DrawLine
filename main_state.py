
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
        self.state = None
        if self.image == None:
            self.image = load_image('resource/main_character.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def handle_go_right(self):
        if self.state == self.GO_RIGHT:
            self.x += 5
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

class Dot:
    image = None
    global x, y
    def __init__(self):
        self.x, self.y = 400 + x, 300 + y
        if self.image == None:
            self.image = load_image('resource/dot.png')

    def draw(self):
        self.image.draw(x, y)

    def update(self):
        self.image.draw(x, y)
""" 시작 버튼
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
"""
def enter():
    global maincharacter, background, startbutton, dot, ground
    maincharacter = Main_character()
    background = Background()
    #startbutton = Start_button()
    dot = Dot()
    ground = Ground()


def exit():
    global maincharacter, background, startbutton, dot, ground
    del(maincharacter)
    del(background)
    #del(startbutton)
    del(dot)
    del(ground)

def pause():
    pass


def resume():
    pass

def handle_events():
    global running
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            maincharacter.x += 5
        elif event.type == SDL_MOUSEBUTTONDOWN and event.type == SDL_MOUSEMOTION:
            dot.x, dot.y = event.x, event.y
            dot.image.draw()





def update():
    pass


def draw():
    clear_canvas()
    background.draw()
    maincharacter.draw()
    #startbutton.draw()
    ground.draw()
    update_canvas()

def main():

    open_canvas()

    maincharacter = Main_character()
    background = Background()
    #startbutton = Start_button()
    ground = Ground()
    global running
    running = True

    while running:
        handle_events()

        maincharacter.update()

        clear_canvas()
        background.draw()
        maincharacter.draw()
        dot.draw()
        ground.draw()
       # startbutton.draw()
        update_canvas()

        delay(0.04)

    close_canvas()


if __name__ == '__main__':
    main()