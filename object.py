from pico2d import *
from random import *
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Block:
    image = None
    def __init__(self):
        if Block.image == None:
            Block.image = load_image('block30.png')
        self.x, self.y = 0, 0
        self.frame = 0
        self.broke = 0
        self.case = 0

    def get_bb(self):
        return self.x-15, self.y-15, self.x+15, self.y+15

    def draw(self):
        if self.broke == 0:
            if self.case == 0:
                if self.frame < 3:
                    self.image.clip_draw(30*0, 60, 30, 30, self.x, self.y)
                elif 3 <= self.frame < 6:
                    self.image.clip_draw(30*1, 60, 30, 30, self.x, self.y)
                elif 6 <= self.frame < 9:
                    self.image.clip_draw(30*2, 60, 30, 30, self.x, self.y)
                elif 9 <= self.frame < 12:
                    self.image.clip_draw(30*3, 60, 30, 30, self.x, self.y)

            elif self.case == 1:
                if self.frame < 3:
                    self.image.clip_draw(30*0, 30, 30, 30, self.x, self.y)
                elif 3 <= self.frame < 6:
                    self.image.clip_draw(30*1, 30, 30, 30, self.x, self.y)
                elif 6 <= self.frame < 9:
                    self.image.clip_draw(30*2, 30, 30, 30, self.x, self.y)
                elif 9 <= self.frame < 12:
                    self.image.clip_draw(30*3, 30, 30, 30, self.x, self.y)

            elif self.case == 2:
                self.image.clip_draw(30, 0, 30, 30, self.x, self.y)
        else:
            self.image.clip_draw(0, 0, 30, 30, self.x, self.y)

    def update(self, speed):
        self.x += speed
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12

    pass


class Platform:
    image = None
    def __init__(self):
        self.x, self.y = 0, 0
        if Platform.image == None:
            Platform.image = load_image('tiles.png')
        self.case = 0

    def get_bb(self):
        return self.x-15, self.y-15, self.x+15, self.y+15

    def draw(self):
        if game_framework.cur_level == 1 or game_framework.cur_level == 3:
            if self.case == 0:
                self.image.clip_draw(30, 30, 30, 30, self.x, self.y)
            elif self.case == 1:
                self.image.clip_draw(30,0,30,30,self.x,self.y)
        elif game_framework.cur_level == 2:
            if self.case == 0:
                self.image.clip_draw(60, 30, 30, 30, self.x, self.y)
            elif self.case == 1:
                self.image.clip_draw(60,0,30,30,self.x,self.y)

    def update(self, speed):
        self.x += speed
        pass


class Item:
    image = None
    def __init__(self):
        if Item.image == None:
            Item.image = load_image('Item.png')
        self.x, self.y = -10, -10
        self.gravity = 1
        self.case = 0
        self.direction = -1
        self.onAir = 1
        self.active = 0
        self.show = 0
        self.maxh = 0

    def get_bb(self):
        return self.x-15, self.y-15, self.x+15, self.y+15

    def stop(self):
        self.gravity = 0

    def hit(self):
        self.show = 1
        self.maxh = self.y+30

    def draw(self):
        if self.case == 0:
            self.image.clip_draw(0,30,30,30,self.x,self.y)
        elif self.case == 1:
            self.image.clip_draw(0,0,30,30,self.x,self.y)

    def update(self, speed):
        if self.show and self.y < self.maxh: self.y += RUN_SPEED_PPS * game_framework.frame_time
        elif self.show and self.y > self.maxh: self.y = self.maxh; self.active = 1
        if self.case == 0 and self.direction == -1: self.direction = randint(0,1)
        if self.active == 1 and self.case == 0:
            if self.direction == 0:
                self.x -= RUN_SPEED_PPS * game_framework.frame_time
            elif self.direction == 1:
                self.x += RUN_SPEED_PPS * game_framework.frame_time
            self.y -= self.gravity
        self.x += speed

    pass


class Coin:
    image = None
    def __init__(self):
        self.x, self.y = 0, 0
        if Coin.image == None:
            Coin.image = load_image('coin.png')
        self.frame = 0

    def get_bb(self):
        return self.x-15, self.y-15, self.x+15, self.y+15

    def draw(self):
        if self.frame <2:
            self.image.clip_draw(0, 0, 30, 30, self.x, self.y)
        elif 2<=self.frame <4:
            self.image.clip_draw(30, 0, 30, 30, self.x, self.y)
        elif 4<=self.frame <6:
            self.image.clip_draw(60, 0, 30, 30, self.x, self.y)

    def update(self, speed):
        self.x += speed
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6


class Background:
    image = None
    def __init__(self):
        self.x, self.y = 1500, 300
        if Background.image == None:
            Background.image = load_image('bg-grassland.png')

    def draw(self):
        self.image.clip_draw(0,2400 - 600*game_framework.cur_level, 3000, 600, self.x, self.y)

    def update(self, speed):
        if game_framework.cur_level != 4: self.x += speed
        pass

class Flag:
    image = None
    def __init__(self):
        self.x, self.y = 2700, 160
        self.condi = 0
        if Flag.image == None:
            Flag.image = load_image('flag.png')

    def get_bb(self):
        if self.condi == 0:
            return self.x-15, self.y-105, self.x+15, self.y+105
        else: return 0,0,0,0

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self, speed):
        self.x += speed
        pass

class Pipe:
    image = None
    def __init__(self):
        self.x, self.y = 0,0
        self.active = 0
        self.h = 60
        if Pipe.image == None:
            Pipe.image = load_image('pipe.png')

    def get_bb(self):
        return self.x - 30, self.y - self.h/2, self.x + 30, self.y + self.h/2

    def draw(self):
        if self.h == 60:
            self.image.clip_draw(0,0,60,60,self.x, self.y)
        elif self.h == 90:
            self.image.clip_draw(60, 0, 60, 90, self.x, self.y)
        elif self.h == 120:
            self.image.clip_draw(120, 0, 60, 120, self.x, self.y)

    def update(self, speed):
        self.x += speed
        pass

class Arena:
    def __init__(self):
        self.x, self.y = 0, 0

    def get_bb(self):
        return self.x, self.y, self.x + 800, self.y + 100

    def update(self, speed):
        pass

    def draw(self):
        pass


class Aircraft:
    image = None
    def __init__(self):
        if Aircraft.image == None:
            Aircraft.image = load_image('aircraft.png')
        self.x, self.y = 0,0
        self.w = 390
        self.active = 0
        self.speed = RUN_SPEED_PPS * game_framework.frame_time
        self.boundary = 1740
        self.distance = 0

    def get_bb(self):
        return self.x - self.w/2, self.y-15, self.x + self.w/2, self.y + 15

    def update(self, speed):
        self.x += speed
        if self.active == 2:
            self.y += self.speed * 2
            if self.y >= 600: self.y = 0
        elif self.active == 1:

            if self.distance > self.boundary:
                self.y -= self.speed * 2
            else:
                self.x += self.speed
                self.distance += self.speed
        pass

    def draw(self):
        self.image.clip_draw(0,370,390,30,self.x,self.y)
        pass