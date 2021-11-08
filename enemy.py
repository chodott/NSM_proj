# 엉금엉금 condition==0 충돌 시 상호작용 필요

from pico2d import *


class Goomba:
    def __init__(self):
        self.image = load_image('goomba.png')
        self.x, self.y = -10,-10
        self.w, self.h = 30,30
        self.dir = -1
        self.speed = -3
        self.frame = 1
        self.condition = 0 #1: 죽음 0: 생존 -1: 죽음(불)
        self.deathcnt = 0

    def draw(self):
        if self.condition==1: self.image.clip_draw(0,0,30,15,self.x,self.y)
        elif self.condition==-1: self.image.clip_draw(0,30,30,30,self.x,self.y)
        else: self.image.clip_draw(0,270-self.frame*30,30,30,self.x,self.y)

    def update(self):

        if self.condition == 1:
            self.deathcnt += 1
            if self.deathcnt == 5:
                self.x, self.y = -10, -10
        elif self.condition == -1:
            self.y += -10
        else:
            self.y -= 10
            self.frame = (self.frame + 1) % 7
            self.x += self.speed

    def death(self, type):
        if type == 0:
            self.condition = 1
            self.y -= 15

        elif type == 1:
            self.condition = -1





class Troopa:
    def __init__(self):
        self.image = load_image('troopa.png')
        self.x, self.y = -10, -10
        self.w, self.h = 30, 50
        self.dir = -1
        self.speed = -2
        self.frame = 0
        self.condition = 1 #0 : 등껍질 1: 정상 2: 날개
        self.boundary = 400

    def draw(self):
        #상태에 맞는 그리기 필요
        if self.condition == 0:
            self.image.clip_draw(30,0 + self.frame * 30,self.w,self.h, self.x, self.y);
        elif self.condition == -1:
            self.image.clip_draw(30, 90, self.w, self.h, self.x, self.y);
        elif self.condition == 1:
            self.image.clip_draw(0,800 - 50 - self.frame * 50,self.w,self.h, self.x, self.y);
        elif self.condition == 2:
            self.image.clip_draw(0, 800 - 50 - self.frame * 50, self.w, self.h, self.x, self.y);


    def update(self):
        self.y -= 5
        if self.condition == 0:
            self.x += self.speed
            self.h = 30
            if self.speed != 0: self.frame = (self.frame+1) % 3
        elif self.condition == -1:
            self.y -= 10
            self.h = 30
        elif self.condition == 1:
            self.x += self.speed
            self.frame = (self.frame+1) % 13
        elif self.condition == 2:
            if self.y >= self.boundary:
                self.boundary = 0
                self.y -= 3
            elif self.y <= self.boundary:
                self.boundary = 400
                self.y += 3


class Boo:
    def __init__(self):
        self.image = load_image('ghost.png')
        self.x, self.y = -10, -10
        self.w, self.h = 30, 30
        self.dir = -1
        self.speed = 2
        self.frame = 0
        self.t = 0
        self.condition = 1  # 0 : 정지 1: 추격
        self.boundary = 400

    def draw(self):
        #상태에 맞는 그리기 필요
        if self.condition == 0 and self.dir > 0:
            self.image.clip_draw(30,60,self.w,self.h,self.x,self.y);

        elif self.condition == 0 and self.dir < 0:
            self.image.clip_draw(0, 60, self.w, self.h, self.x, self.y);

        elif self.condition == 1 and self.dir > 0:
            self.image.clip_draw(30, 150 - self.frame * 30, self.w, self.h, self.x, self.y);

        elif self.condition == 1 and self.dir < 0:
            self.image.clip_draw(0, 150 - self.frame * 30, self.w, self.h, self.x, self.y);

    def update(self, px, py, pdir, idir):
        self.frame = (self.frame + 1) % 3
        if self.x < px: self.dir = 1
        elif self.x > px: self.dir = -1
        #플레이어와 부끄의 방향이 같을 때 부끄 정지
        if self.dir != pdir and self.dir != idir:
            self.condition = 0
            self.t = 0

        #방향이 다를 때 부끄 캐릭터 방향으로
        elif self.dir == pdir or self.dir == idir:
            self.condition = 1

        if self.condition == 1:
            self.t += 1
            t = self.t/1000
            self.x = (1-t) * self.x + t * px
            self.y = (1-t) * self.y + t * py



