from pico2d import *
from random import *


class Block:
    def __init__(self):
        self.image = load_image('block30.png')
        self.x, self.y = 200, 150
        self.frame = 0
        self.broke = 0
        self.case = 0

    def draw(self):
        if self.broke == 0:
            if self.case == 0: self.image.clip_draw(30*self.frame, 60, 30, 30, self.x, self.y)
            elif self.case == 1: self.image.clip_draw(30*self.frame, 30, 30, 30, self.x, self.y)
        else:
            self.image.clip_draw(0, 0, 30, 30, self.x, self.y)

    def update(self):
        self.frame = (self.frame+1) % 4

    pass


class Platform:
    def __init__(self):
        self.x, self.y = 50, 50
        self.image = load_image('tiles.png')
        self.case = 0

    def draw(self):
        if self.case == 0:
            self.image.clip_draw(30, 30, 30, 30, self.x, self.y)

    pass


class Item:
    def __init__(self):
        self.x, self.y = -10, -10
        self.image = load_image('Item.png')
        self.case = 0
        self.direction = -1
        self.onAir = 1
        self.active = 0

    def draw(self):
        if self.case == 0:
            self.image.clip_draw(0,30,30,30,self.x,self.y)
        elif self.case == 1:
            self.image.clip_draw(0,0,30,30,self.x,self.y)

    def update(self):
        if self.active == 1:
            if self.direction == 0:
                self.x -= 1
            elif self.direction == 1:
                self.x += 1
            if self.onAir == 1:
                self.y -= 5

    pass


class Coin:
    def __init__(self):
        self.x, self.y = -1, -1
        self.image = load_image('coin.png')
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame*30, 0, 30, 30, self.x, self.y)

    def update(self):
        self.frame = (self.frame+1) % 3


class Background:
    def __init__(self):
        self.x, self.y = 400, 300
        self.image = load_image('bg-grassland.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    pass