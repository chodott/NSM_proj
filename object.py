from pico2d import *
from random import *
import game_framework
import server
import time

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
        if self.x != 0 and self.y != 0:
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

    def update(self):
        if self.x != 0 and self.y != 0:
            self.x += -server.player.gap
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
        if self.x != 0 and self.y != 0:
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

    def update(self):
        if self.x != 0 and self.y != 0:
            self.x += -server.player.gap
        pass


class Item:
    image = None
    def __init__(self):
        if Item.image == None:
            Item.image = load_image('Item.png')
        self.x, self.y = -10, -10
        self.gravity = 1
        self.case = 0
        self.dir = 1
        self.onAir = 1
        self.active = 0
        self.show = 0
        self.maxh = 0
        self.timer = 0

    def get_bb(self):
        return self.x-15, self.y-15, self.x+15, self.y+15

    def stop(self):
        self.gravity = 0

    def hit(self):
        self.show = 1
        self.maxh = self.y+30
        if server.player.power < 1:
            self.case = 0
        else: self.case = 1

    def draw(self):
        if self.show == 1:
            if self.case == 0:
                self.image.clip_draw(0,30,30,30,self.x,self.y)
            elif self.case == 1:
                self.image.clip_draw(0,0,30,30,self.x,self.y)
            elif self.case == 2:
                self.image.clip_draw(30, 0, 30, 30, self.x, self.y)

    def update(self):
        if self.active == 1:
            self.gravity = game_framework.GRAVITY_SPEED_PPS * game_framework.frame_time
            self.collide_check()
            if self.case == 0:
                if self.dir == -1:
                    self.x -= RUN_SPEED_PPS * game_framework.frame_time
                elif self.dir == 1:
                    self.x += RUN_SPEED_PPS * game_framework.frame_time
                self.y -= self.gravity
            elif self.case == 2:
                if self.gravity != 0:
                    self.y -= self.gravity
                else:
                    if self.dir == -1:
                        self.x -= RUN_SPEED_PPS * game_framework.frame_time
                    elif self.dir == 1:
                        self.x += RUN_SPEED_PPS * game_framework.frame_time
        else:
            if self.case == 2:
                self.show = 1
                self.x, self.y = server.player.x, 585
                if time.time() - self.timer > 2:
                    self.active = 1; self.timer = 0
            else:
                if self.show and self.y < self.maxh:
                    self.y += RUN_SPEED_PPS * game_framework.frame_time
                elif self.show and self.y > self.maxh:
                    self.y = self.maxh; self.active = 1
        self.x += -server.player.gap

    def collide_check(self):
        # ?????? ??????
        for pipe in server.pipes:
            if server.collide(self, pipe):
                if self.y - 15 >= pipe.y + 10:
                    self.stop()
                elif pipe.x <= self.x - 15 < pipe.x + 30:
                    self.dir = 1
                    self.x = pipe.x + 45
                elif pipe.x - 40 <= self.x + 15 < pipe.x:
                    self.dir = -1
                    self.x = pipe.x - 45

        for grass in server.grassTile1:
            if server.collide(self, grass):
                self.stop()
                break

        for ib in server.ibs:
            if server.collide(self, ib):
                self.stop()
                break

        for nb in server.nbs:
            if server.collide(self, nb):
                if self.y - 15 >= nb.y + 10:
                    self.stop()
                elif nb.x <= self.x - 15 < nb.x + 15:
                    self.dir = 1
                    self.x = nb.x + 30

                elif nb.x - 15 <= self.x + 15 < nb.x:
                    self.dir = -1
                    self.x = nb.x - 30


        for eb in server.ebs:
            if server.collide(self, eb):
                self.stop()
                break

        if game_framework.cur_level == 2 or game_framework.cur_level == 3:
            for cb in server.aircraft:
                if server.collide(self, cb):
                    self.stop()


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
        if self.x != 0 and self.y != 0:
            if self.frame <2:
                self.image.clip_draw(0, 0, 30, 30, self.x, self.y)
            elif 2<=self.frame <4:
                self.image.clip_draw(30, 0, 30, 30, self.x, self.y)
            elif 4<=self.frame <6:
                self.image.clip_draw(60, 0, 30, 30, self.x, self.y)

    def update(self):
        if self.x != 0 and self.y != 0:
            self.x += -server.player.gap
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6


class Background:
    image = None
    def __init__(self):
        self.x, self.y = 1500, 300
        self.bk_sound = None
        if Background.image == None:
            Background.image = load_image('bg-grassland.png')
        if game_framework.cur_level == 1:
            self.bk_sound = load_wav('stage1.wav')
        elif game_framework.cur_level == 2:
            self.bk_sound = load_wav('stage2.wav')
        elif game_framework.cur_level == 3:
            self.bk_sound = load_wav('stage3.wav')
        elif game_framework.cur_level == 4:
            self.bk_sound = load_wav('stage4.wav')
        self.bk_sound.set_volume(32)
        self.bk_sound.repeat_play()

    def draw(self):
        self.image.clip_draw(0,2400 - 600*game_framework.cur_level, 3000, 600, self.x, self.y)

    def update(self):
        if game_framework.cur_level != 4: self.x += -server.player.gap
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
        else:
            return 0,0,0,0

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        self.x += -server.player.gap
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
        if self.x != 0 and self.y != 0:
            if self.h == 60:
                self.image.clip_draw(0,0,60,60,self.x, self.y)
            elif self.h == 90:
                self.image.clip_draw(60, 0, 60, 90, self.x, self.y)
            elif self.h == 120:
                self.image.clip_draw(120, 0, 60, 120, self.x, self.y)

    def update(self):
        if self.x != 0 and self.y != 0:
            self.x += -server.player.gap
        pass

class Arena:
    def __init__(self):
        self.x, self.y = 0, 0

    def get_bb(self):
        return self.x, self.y, self.x + 800, self.y + 100

    def update(self):
        pass

    def draw(self):
        pass


class Aircraft:
    image = None
    def __init__(self):
        if Aircraft.image == None:
            Aircraft.image = load_image('aircraft.png')
        self.x, self.y = 0,0
        self.w = 0
        self.active = 0
        self.speed = RUN_SPEED_PPS * game_framework.frame_time
        self.boundary = 880
        self.distance = 0

    def get_bb(self):
        return self.x - self.w/2, self.y-15, self.x + self.w/2, self.y + 15

    def update(self):
        self.x += -server.player.gap
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
        if self.w == 390:
            self.image.clip_draw(0,370,390,30,self.x,self.y)
        elif self.w == 210:
            self.image.clip_draw(0, 340, 210, 30, self.x, self.y)
