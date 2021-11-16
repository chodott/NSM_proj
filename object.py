from pico2d import *
from random import *
import game_framework

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Block:
    image = None
    def __init__(self):
        if Block.image == None:
            Block.image = load_image('block30.png')
        self.x, self.y = 200, 150
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
        else:
            self.image.clip_draw(0, 0, 30, 30, self.x, self.y)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12

    pass


class Platform:
    image = None
    def __init__(self):
        self.x, self.y = 50, 50
        if Platform.image == None:
            Platform.image = load_image('tiles.png')
        self.case = 0

    def get_bb(self):
        return self.x-15, self.y-15, self.x+15, self.y+15

    def draw(self):
        if self.case == 0:
            self.image.clip_draw(30, 30, 30, 30, self.x, self.y)

    def update(self):
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

    def get_bb(self):
        return self.x-15, self.y-15, self.x+15, self.y+15

    def stop(self):
        self.gravity = 0

    def draw(self):
        if self.case == 0:
            self.image.clip_draw(0,30,30,30,self.x,self.y)
        elif self.case == 1:
            self.image.clip_draw(0,0,30,30,self.x,self.y)

    def update(self):
        if self.case == 0 and self.direction == -1: self.direction = randint(0,1)
        if self.active == 1 and self.case == 0:
            if self.direction == 0:
                self.x -= 2
            elif self.direction == 1:
                self.x += 2
            self.y -= self.gravity

    pass


class Coin:
    image = None
    def __init__(self):
        self.x, self.y = -1, -1
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

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6


class Background:
    image = None
    def __init__(self):
        self.x, self.y = 400, 300
        if Background.image == None:
            Background.image = load_image('bg-grassland.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x, self.y = 400, 300
        pass


