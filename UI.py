from pico2d import *

class UI:
    image = None
    def __init__(self, name):
        if UI.image == None:
            UI.image = load_image('ui.png')
        self.value = 3
        self.coin = 0
        self.alarm = 400
        self.pos = name

    def update(self):
        self.value = Life
        if self.alarm > 0:
            self.alarm -= 1

    def draw(self):
        #life 출력
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




Life = 5
getCoin = 0