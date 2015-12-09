
import sys
import random
import json
import os

import game_framework
import title_state
import stage2
from pico2d import *

from Land import Land

name = "MainState"
is_goal = True
isMouseClicked = False
isButtonClicked = False
# 마우스 좌표 저장에 대한 리스트
MouseList = []
ColorList = [[217, 65, 197], [165, 102, 255], [71, 200, 62], [92, 209, 229]]
LandBoxList = []
MainCharacterList = []
class Background:
    def __init__(self):
        self.image = load_image('resource/game_background.png')

    def draw(self):
        self.image.draw(400,300)


class Main_character:
    image = None
    MOVER_PER_SEC = 70

    def __init__(self):
        self.x, self.y = 50, 220
        self.width, self.height = 50, 50
        if self.image == None:
            self.image = load_image('resource/main_character.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def handle_go_right(self):
        pass

    def handle_stand(self):
        pass

    def bb2bb(self, get_bb):
        if(self.x + (self.width / 2) < get_bb[0] or
           self.x - (self.width / 2) > get_bb[2] or
           self.y + (self.height / 2) < get_bb[1] or
           self.y - (self.height / 2) > get_bb[3]):
            return False
        else:
            return True

    def update(self, frame_time, get_boxList, get_stargoal):
        if(isButtonClicked):
            # x축으로 이동 후 충돌 체크 후 충돌하였다면 다시 x축으로 돌아온다
            self.x += frame_time * self.MOVER_PER_SEC
            # LandBox 리스트의 각 원소에 대하여
            for d in get_boxList:
                # 충돌 박스를 가져와서 바운딩 박스와 바운딩 박스끼리의 충돌 처리를 수행한다
                if(self.bb2bb(d.get_collisionBox())):
                    self.x -= frame_time * self.MOVER_PER_SEC

            # 마찬가지로 y축으로 이동 후 충돌 체크 후 충돌하였다면 다시 y축으로 돌아온다
            self.y -= frame_time * self.MOVER_PER_SEC
            # LandBox 리스트의 각 원소에 대하여
            for d in get_boxList:
                if(self.bb2bb(d.get_collisionBox())):
                    self.y += frame_time * self.MOVER_PER_SEC
        if(self.bb2bb(stargoal.get_collisionBox())):
            game_framework.change_state(stage2)

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

    def __init__(self, gx, gy, gw, gh):
        self.x, self.y = gx, gy
        self.width, self.height = gw, gh
        self.frame = random.randint(0,7)
        self.total_frames = 0.0
        if self.image == None:
            self.image = load_image('resource/stargoal_animation.png')

    def bb2bb(self, get_bb):
        if(self.x + (self.width / 2) < get_bb[0] or
           self.x - (self.width / 2) > get_bb[2] or
           self.y + (self.height / 2) < get_bb[1] or
           self.y - (self.height / 2) > get_bb[3]):
            return False
        else:
            return True

    def update(self, frame_time):
        distance = stargoal.RUN_SPEED_PPS * frame_time
        self.total_frames += stargoal.FRAME_PER_ACTION * stargoal.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % 8

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

    def get_collisionBox(self):
        return ([self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height])

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

class LandBox:
    def __init__(self, lbX, lbY, rtX, rtY):
        self.leftBottomX = lbX
        self.leftBottomY = lbY
        self.rightTopX = rtX
        self.rightTopY = rtY

    def draw(self):
        draw_fill_rectangle(self.leftBottomX, self.leftBottomY, self.rightTopX - self.leftBottomX, self.rightTopY - self.leftBottomY)
    def update(self):
        pass

    def get_collisionBox(self):
        return ([self.leftBottomX, self.leftBottomY, self.rightTopX, self.rightTopY])

def enter():
    global maincharacter, background, startbutton, land, stargoal
    global current_time
    global LandBoxList

    maincharacter = Main_character()
    background = Background()
    startbutton = Start_button()
    stargoal = Stargoal(700, 210, 50, 50)

    # Landbox 리스트 내용 초기화
    LandBoxList.append(LandBox(0, 0, 800, 160))
    #LandBoxList.append(LandBox(460, 0, 800, 160))

    current_time = get_time()           # 새로 추가 (시간 개념)

def exit():
    global maincharacter, background, startbutton, land
    global LandBoxList, Stargoal
    del(maincharacter)
    del(background)
    del(startbutton)
    del(Stargoal)
    del(LandBoxList)
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
    global isMouseClicked, isButtonClicked, MouseList, maincharacter, stargoal, is_goal, frame
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
            if((10 < event.x < 90) or (515 < event.y < 585)):
                startbutton.image = load_image('resource/start_button2.png')
                startbutton.draw()
                isButtonClicked = True
            print(event.x, 600 - event.y)
        elif (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
            isMouseClicked = False



def update():
    global LandBoxList, MainCharacterList, stargoal
    frame_time = get_frame_time()       # 새로 추가 (시간 개념)
    maincharacter.update(frame_time, LandBoxList, stargoal)
    stargoal.update(frame_time)

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

    for d in LandBoxList:
        d.draw()


    update_canvas()


def main():
    pass

if __name__ == '__main__':
    main()