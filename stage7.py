__author__ = 'Min'

import sys
import random
import json
import os
import math

import game_framework
import title_state
import stage8
from pico2d import *
from Land import Land

name = "stage6"
is_goal = True
isMouseClicked = False
isButtonClicked = False

vecX = 1.0
vecY = 0.0
intersectionX = None
intersectionY = None
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

def GetVectorSize(vecX, vecY):
    return math.sqrt((vecX * vecX) + (vecY * vecY))

def IntersectionEX(px1_begin, py1_begin, px1_end, py1_end, px2_begin, py2_begin, px2_end, py2_end):
    global intersectionX, intersectionY
    under = (py2_end - py2_begin)*(px1_end - px1_begin) - (px2_end - px2_begin)*(py1_end - py1_begin)
    if(under == 0):
       return False

    _t = (px2_end - px2_begin)*(py1_begin - py2_begin) - (py2_end - py2_begin)*(px1_begin - px2_begin)
    _s = (px1_end - px1_begin)*(py1_begin - py2_begin) - (py1_end - py1_begin)*(px1_begin - px2_begin)

    t = _t / under
    s = _s / under
    if(t < 0.0 or t > 1.0 or s < 0.0 or s > 1.0):
        return False
    if(_t == 0 and _s == 0):
        return False

    intersectionX = px1_begin + t * (px1_end - px1_begin)
    intersectionY = py1_begin + t * (py1_end - py1_begin) + 25

    return True

class Main_character:
    image = None
    MOVER_PER_SECX = 70
    MOVER_PER_SECY = 70

    def __init__(self, x, y):
        self.x, self.y = x, y
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
        global MouseList, intersectionX, intersectionY, vecX, vecY, newVecX
        if(isButtonClicked):
            # x축으로 이동 후 충돌 체크 후 충돌하였다면 다시 x축으로 돌아온다
            self.postX = self.x
            self.x += frame_time * self.MOVER_PER_SECX
            # LandBox 리스트의 각 원소에 대하여
            for d in get_boxList:
                # 충돌 박스를 가져와서 바운딩 박스와 바운딩 박스끼리의 충돌 처리를 수행한다
                if(self.bb2bb(d.get_collisionBox())):
                    self.x -= frame_time * self.MOVER_PER_SECX

            # 마찬가지로 y축으로 이동 후 충돌 체크 후 충돌하였다면 다시 y축으로 돌아온다
            self.postY = self.y
            self.y -= frame_time * self.MOVER_PER_SECY
            # LandBox 리스트의 각 원소에 대하여
            for d in get_boxList:
                if(self.bb2bb(d.get_collisionBox())):
                    self.y += frame_time * self.MOVER_PER_SECY
            for i, d in enumerate(MouseList):
                if (i > 0):
                    if(IntersectionEX(self.postX, self.postY-25, self.x, self.y-25, MouseList[i - 1][0], MouseList[i-1][1], MouseList[i][0], MouseList[i][1])):
                        dist = GetVectorSize(self.x - intersectionX, self.y - intersectionY)
                        newVecX = MouseList[i-1][0] - MouseList[i][0]
                        newVecY = MouseList[i-1][1] - MouseList[i][1]
                        if(intersectionY <= self.y):
                            if(MouseList[i-1][0] <= MouseList[i][0]):
                                temp = newVecX
                                newVecX = -newVecY
                                newVecY = temp
                            else:
                                temp = -newVecX
                                newVecX = newVecY
                                newVecY = temp
                        else:
                            if(MouseList[i-1][0] <= MouseList[i][0]):
                                temp = -newVecX
                                newVecX = newVecY
                                newVecY = temp
                            else:
                                temp = newVecX
                                newVecX = -newVecY
                                newVecY = temp

                        newVecSize = GetVectorSize(newVecX, newVecY)
                        newVecX /= newVecSize
                        newVecY /= newVecSize

                        interpolatedVecX = vecX - (((vecX * newVecX) + (vecY * newVecY)) / ((newVecX * newVecX) + (newVecY * newVecY)) * newVecX)
                        interpolatedVecY = vecY - (((vecX * newVecX) + (vecY * newVecY)) / ((newVecX * newVecX) + (newVecY * newVecY)) * newVecY)
                        interpolatedVecSize = GetVectorSize(interpolatedVecX, interpolatedVecY)
                        if(interpolatedVecSize < 0.000001):
                            interpolatedVecSize = 0.000001
                        interpolatedVecX /= interpolatedVecSize
                        interpolatedVecY /= interpolatedVecSize

                        self.x = intersectionX
                        self.y = intersectionY

                        vecX = interpolatedVecX
                        vecY = interpolatedVecY

                        self.x += (interpolatedVecX * dist * 1) + (newVecX * 1)
                        self.y += (interpolatedVecY * dist * 1) + (newVecY * 1)
        if(self.bb2bb(stargoal.get_collisionBox())):
            background.image = load_image('resource/last.png')
            background.draw()
            update_canvas()
            delay(3)
            game_framework.push_state(stage8)

        if(self.bb2bb(left.get_collisionBox())):
            self.MOVER_PER_SECX *= -1
            vecX *= -1

        if(self.bb2bb(right.get_collisionBox())):
            self.MOVER_PER_SECX *= -1
            vecX *= -1


class Left:
    image = None

    def __init__(self, gx, gy):
        self.x, self.y = gx, gy
        self.width, self.height = 1, 1

        if self.image == None:
            self.image = load_image('resource/return.png')

    def bb2bb(self, get_bb):
        if(self.x + (self.width / 2) < get_bb[0] or
           self.x - (self.width / 2) > get_bb[2] or
           self.y + (self.height / 2) < get_bb[1] or
           self.y - (self.height / 2) > get_bb[3]):
            return False
        else:
            return True

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_collisionBox(self):
        return ([self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height])

class Right:
    image = None

    def __init__(self, gx, gy):
        self.x, self.y = gx, gy
        self.width, self.height = 1, 1

        if self.image == None:
            self.image = load_image('resource/return2.png')

    def bb2bb(self, get_bb):
        if(self.x + (self.width / 2) < get_bb[0] or
           self.x - (self.width / 2) > get_bb[2] or
           self.y + (self.height / 2) < get_bb[1] or
           self.y - (self.height / 2) > get_bb[3]):
            return False
        else:
            return True

    def draw(self):
        self.image.draw(self.x, self.y)

    def get_collisionBox(self):
        return ([self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height])

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

    def __init__(self, gx, gy):
        self.x, self.y = gx, gy
        self.width, self.height = 50, 50
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

    def __init__(self, x, y):
        self.x, self.y = x, y
        if self.image == None:
            self.image = load_image('resource/start_button.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

class Again_button:
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        if self.image == None:
            self.image = load_image('resource/again_button.png')

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
    global maincharacter, background, startbutton,  land, stargoal, againbutton, left, right
    global current_time
    global LandBoxList

    maincharacter = Main_character(400, 210)
    background = Background()

    startbutton = Start_button(50, 550)
    againbutton = Again_button(750, 550)
    stargoal = Stargoal(400, 550)
    left = Left(750, 300)
    right = Right(50, 400)
    # Landbox 리스트 내용 초기화
    LandBoxList.append(LandBox(300, 0, 500, 160))

    current_time = get_time()           # 새로 추가 (시간 개념)

def exit():
    global maincharacter, background, startbutton, land, againbutton, left, right
    global LandBoxList, Stargoal
    del(maincharacter)
    del(background)
    del(startbutton)
    del(againbutton)
    del(Stargoal)
    del(LandBoxList)
    del(left)
    del(right)
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
    global isMouseClicked, isButtonClicked, MouseList, maincharacter, stargoal, is_goal, frame, main_state
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
            mx = event.x
            my = 600 - event.y
            if((10 < mx < 90) and (515 < my < 585)):
                startbutton.image = load_image('resource/start_button2.png')
                startbutton.draw()
                isButtonClicked = True
            if((710 < mx < 785) and (515 < my < 585)):
                isButtonClicked = False
                MouseList = []
                enter()

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
    left.draw()
    right.draw()
    maincharacter.draw()
    startbutton.draw()
    againbutton.draw()
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

if __name__ == '__stage7__':
    main()