__author__ = 'Min'
import game_framework
import main_state
from pico2d import *

name = "TitleState"
image = None
title_menu = None

def enter():
    global image
    global title_menu
    image = load_image('resource/title.png') # 여기에 첫 메인 게임 화면 넣기
    title_menu = load_image('resource/title_menu.png')

def exit():
    global image
    global title_menu
    del(image)
    del(title_menu)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)

def draw():
    clear_canvas()
    image.draw(400, 300)
    title_menu.draw(400, 400)
    update_canvas()

def update():
    global boy
    boy.draw()

def pause():
    pass

def resume():
    pass
