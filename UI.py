from pico2d import *
import time

import game_framework


class UI:
    image = None
    def __init__(self, name):
        if UI.image == None:
            UI.image = load_image('ui.png')
        self.value = 3
        self.coin = 0
        self.alarm = 400
        self.pos = name
        self.time = time.time()

    def update(self):
        self.value = game_framework.Life
        if self.alarm > 0 and self.pos == "MainState":
            self.alarm = 400 - (int)(time.time()-self.time)

    def draw(self):
        #life 출력
        if self.pos == "LoadState":
            self.image.clip_draw(200, 0, 60, 40, 380, 300)
            self.image.clip_draw(15 * self.value, 40, 15, 30, 420, 300)
        else:
            self.image.clip_draw(200,0,60,40,30,500)
            self.image.clip_draw(15*self.value,40,15,30,70,500)
        if self.pos == "MainState":
            #coin 출력
            self.image.clip_draw(150, 40, 60, 30, 40, 470)
            self.image.clip_draw(15 * (self.coin//10), 40, 15, 30, 60, 470)
            self.image.clip_draw(15 * (self.coin % 10 // 1), 40, 15, 30, 75, 470)
            #alarm 출력
            self.image.clip_draw(0,70,50,30,700,550)
            self.image.clip_draw(15 * (self.alarm//100), 40, 15, 30, 740, 550)
            self.image.clip_draw(15 * (self.alarm % 100 // 10), 40, 15, 30, 755, 550)
            self.image.clip_draw(15 * (self.alarm % 100 % 10 // 1), 40, 15, 30, 770, 550)