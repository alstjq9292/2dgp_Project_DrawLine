
__author__ = 'Min'

import sys
import random
import json
import os

import game_framework
import title_state
from pico2d import *

name = "MainState"
running = None
class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)


class Boy:
    image = None

    LEFT_RUN, RIGHT_RUN, LEFT_STAND, RIGHT_STAND = 0, 1, 2, 3


    def handle_left_run(boy):
        boy.x -= 5
        boy.run_frames += 1
        if boy.x < 0:
            boy.state = boy.RIGHT_RUN
            boy.x = 0
        if boy.run_frames == 50:
            boy.state = boy.LEFT_STAND


    def handle_left_stand(boy):
        boy.stand_frames += 1
        if boy.stand_frames == 25:
            boy.state = boy.LEFT_RUN



    def handle_right_run(boy):
        boy.x += 5
        boy.run_frames += 1
        if boy.x > 800:
            boy.state = boy.LEFT_RUN
            boy.x = 800
        if boy.run_frames == 50:
            boy.state = boy.RIGHT_STAND

    def handle_right_stand(boy):
        boy.stand_frames += 1
        if boy.stand_frames == 25:
            boy.state = boy.RIGHT_RUN

    handle_state = {
                LEFT_RUN: handle_left_run,
                RIGHT_RUN: handle_right_run,
                LEFT_STAND: handle_left_stand,
                RIGHT_STAND: handle_right_stand
    }


    def update(boy):
         boy.frame = (boy.frame + 1) % 8
         boy.handle_state[boy.state](boy)



    def __init__(boy):
        boy.x, boy.y = random.randint(100, 700), 90
        boy.frame = random.randint(0, 7)
        boy.run_frames = 0
        boy.stand_frames = 0
        boy.state = boy.RIGHT_RUN
        if Boy.image == None:
            Boy.image = load_image('animation_sheet.png')

    def draw(self):
        boy.image.clip_draw(self.frame * 100, self.state * 100, 100, 100, self.x, self.y)


def enter():
    global boy, grass
    boy = Boy()
    grass = Grass()


def exit():
    global boy, grass
    del(boy)
    del(grass)

def pause():
    pass


def resume():
    pass

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
        elif(event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            if boy.state == boy.RIGHT_RUN:
                boy.run_frames = 0
                boy.state = boy.LEFT_RUN
            elif boy.state == boy.LEFT_RUN:
                boy.run_frames = 0
                boy.state = boy.RIGHT_RUN
            elif boy.state == boy.RIGHT_STAND:
                boy.stand_frames = 0
                boy.state = boy.RIGHT_RUN
            elif boy.state == boy.LEFT_STAND:
                boy.stand_frames = 0
                boy.state = boy.LEFT_RUN




def update():
    boy.update()
    delay(0.05)


def draw():
    clear_canvas()
    grass.draw()
    boy.draw()
    update_canvas()

def main():

    open_canvas()

    boy = Boy()
    grass = Grass()

    global running
    running = True

    while running:
        handle_events()

        boy.update()

        clear_canvas()
        grass.draw()
        boy.draw()
        update_canvas()

        delay(0.04)

    close_canvas()


if __name__ == '__main__':
    main()
