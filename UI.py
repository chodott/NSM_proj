from pico2d import *
import time

import game_framework
import server


class UI:
    image = None
    def __init__(self, name):
        if UI.image == None:
            UI.image = load_image('ui.png')
        self.value = 3
        self.coin = 0
        self.alarm = 400
        self.gameclear = 0
        self.y = 700
        self.pos = name
        self.time = time.time()

    def update(self):
        self.value = game_framework.Life
        self.coin = game_framework.Coin
        if self.alarm > 0 and self.pos == "MainState":
            self.alarm = 400 - (int)(time.time()-self.time)
        if game_framework.Coin == 10:
            server.items[9].case = 2
            server.items[9].timer = time.time()
            game_framework.Coin -= 10
        if self.gameclear:
            if self.y >= 350:
                self.y -= game_framework.GRAVITY_SPEED_PPS * game_framework.frame_time

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

            if self.gameclear:
                self.image.clip_draw(400,0,400,300,400,self.y)