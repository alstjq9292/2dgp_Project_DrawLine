__author__ = 'Min'
'''
from pico2d import *

is_goal = True
frame = 0
class Stargoal:
    def __init__(self):
        self.x, self.y = 750, 200
        self.frame = 0
        self.image = load_image('stargoal_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


def handle_events():
    global is_goal, frame

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            is_goal = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            is_goal = False

    while (is_goal):
       clear_canvas()
       update_canvas()
       frame = (frame + 1) % 8
       delay(0.05)
       handle_events()
'''
