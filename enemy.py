from pico2d import *

class goomba:
    def __init__(self):
        self.image = load_image('goomba.png')
        self.x, self.y
        self.width, self.height = 30,30
        self.dir = -1
        self.speed = 3
        self.frame = 0
        self.condition = 0 #1: 죽음 0: 생존
        self.deathcnt = 0

    def draw(self):
        if self.condition: self.image.clip_draw(0,0,30,30,self.x,self.y)
        else: self.image.clip_draw(0,270-self.frame*30,30,30,self.x,self.y)

    def update(self):
        if self.condition:
            self.deathcnt += 1
            if self.deatcnt == 3:
                self.x, self.y = -10, -10
        else:
            self.frame = (self.frame + 1) % 8
            self.x += self.speed


class turtle:
    def __init__(self):
        self.image = load_image('troopa.png')
        self.x, self.y
        self.width, self.height = 30, 40
        self.dir = -1
        self.speed = 2
        self.frame = 0
        self.condition = 1 #0 : 등껍질 1: 정상 2: 날개
        self.boundary = 400

    def draw(self):
        #상태에 맞는 그리기 필요


    def update(self):
        if self.condition == 0:
            self.x += self.speed
            self.height = 30
        elif self.condition == 1:
            self.x += self.speed
        elif self.condition == 2:
            if self.y >= self.boundary:
                self.boundary = 0
                self.y -= 3
            elif self.y <= self.boundary:
                self.boundary = 400
                self.y += 3


