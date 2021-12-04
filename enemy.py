# 엉금엉금 condition==0 충돌 시 상호작용 필요

from pico2d import *
from time import *
from player import *
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 5.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# Gravity
GRAVITY_SPEED_KMPH = 30.0
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 1.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



class Goomba:
    image = None
    def __init__(self):
        if Goomba.image == None:
            Goomba.image = load_image('goomba.png')
        self.x, self.y = 0,0
        self.w, self.h = 30,30
        self.speed = RUN_SPEED_PPS * game_framework.frame_time
        self.gravity = 5
        self.dir = -1
        self.frame = 1
        self.condition = 0 #1: 죽음 0: 생존 -1: 죽음(불)
        self.deathtime = 0

    def get_bb(self):
        if self.condition == 1 or self.condition == -1: return 0,0,0,0
        return self.x-15, self.y-15, self.x+15, self.y+15

    def draw(self):
        if self.condition == 1: self.image.clip_draw(0,0,30,15,self.x,self.y)
        elif self.condition == -1: self.image.clip_draw(0,30,30,30,self.x,self.y)
        else:
            if self.dir == -1: self.image.clip_draw(0,270-(int)(self.frame)*30,30,30,self.x,self.y)
            elif self.dir == 1: self.image.clip_draw(30,270-(int)(self.frame)*30,30,30,self.x,self.y)

    def stop(self):
        self.gravity = 0

    def update(self, speed):
        self.x += speed
        if self.condition == 1:
            if time.time() - self.deathtime > 1:
                self.x, self.y = -10, -10
                del(self)

        elif self.condition == -1:
            self.y -= self.gravity
            del(self)
        else:
            self.y -= self.gravity
            self.frame = (self.frame + + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7
            self.x += self.speed * self.dir

    def hit(self, type):
        self.deathtime = time.time()
        if type == 0:
            self.condition = 1
            self.y -= 15

        elif type == 1:
            self.condition = -1



class Troopa:
    image = None
    def __init__(self):
        if Troopa.image == None:
            Troopa.image = load_image('troopa.png')
        self.x, self.y = 0, 0
        self.w, self.h = 30, 50
        self.dir = -1
        self.speed = RUN_SPEED_PPS * game_framework.frame_time
        self.gravity = 1
        self.frame = 0
        self.condition = 1 #0 : 등껍질 1: 정상 2: 날개
        self.goal = 200

    def get_bb(self):
        if self.condition == 0:
            return self.x-15, self.y-15, self.x+15, self.y+15
        elif self.condition == 1 or self.condition == 2:
            return self.x - 15, self.y - 25, self.x + 15, self.y + 25
        elif self.condition == -1:
            return -100, -100, -100, -100

    def stop(self):
        self.gravity = 0

    def hit(self, px):
        if self.condition > 0:
            self.condition -= 1
            if self.condition == 0:
                self.frame = 0
        if self.condition == 0 and self.speed == 0:
            self.speed = RUN_SPEED_PPS * game_framework.frame_time * 5
            if px > self.x: self.dir = -1
            else: self.dir = 1
            self.x += self.speed
        elif self.condition == 0 and self.speed != 0:
            self.speed = 0

    def death(self):
        self.condition = -1

    def draw(self):
        #상태에 맞는 그리기 필요
        if self.condition == 0:
            self.image.clip_draw(30,0 + (int)(self.frame) * 30,self.w,self.h, self.x, self.y);
        elif self.condition == -1:
            self.image.clip_draw(30, 90, self.w, self.h, self.x, self.y);
        elif self.condition == 1:
            self.image.clip_draw(0,800 - 50 - (int)(self.frame) * 50,self.w,self.h, self.x, self.y);
        elif self.condition == 2:
            self.image.clip_draw(0, 800 - 50 - (int)(self.frame) * 50, self.w, self.h, self.x, self.y);


    def update(self, speed):
        if self.condition == 0:
            self.x += self.speed * self.dir
            self.h = 30
            if self.speed != 0: self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        elif self.condition == -1:
            self.h = 30
        elif self.condition == 1:
            self.x += self.speed * self.dir
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
        elif self.condition == 2:
            self.gravity = 0
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 13
            if self.y <= self.goal:
                self.goal = 300
                self.y += game_framework.frame_time * GRAVITY_SPEED_PPS / 2
            elif self.y >= self.goal:
                self.goal = 150
                self.y -= game_framework.frame_time * GRAVITY_SPEED_PPS / 2
        self.y -= self.gravity
        self.x += speed


class Boo:
    image = None
    def __init__(self):
        if Boo.image == None:
            Boo.image = load_image('ghost.png')
        self.x, self.y = 0, 0
        self.w, self.h = 30, 30
        self.dir = -1
        self.speed = 2
        self.frame = 0
        self.t = 0
        self.condition = 1  # 0 : 정지 1: 추격
        self.boundary = 400

    def get_bb(self):
        return self.x-15, self.y-15, self.x+15, self.y+15

    def draw(self):
        #상태에 맞는 그리기 필요
        if self.condition == 0 and self.dir > 0:
            self.image.clip_draw(30,60,self.w,self.h,self.x,self.y);

        elif self.condition == 0 and self.dir < 0:
            self.image.clip_draw(0, 60, self.w, self.h, self.x, self.y);

        elif self.condition == 1 and self.dir > 0:
            self.image.clip_draw(30, 150 - (int)(self.frame) * 30, self.w, self.h, self.x, self.y);

        elif self.condition == 1 and self.dir < 0:
            self.image.clip_draw(0, 150 - (int)(self.frame) * 30, self.w, self.h, self.x, self.y);

    def update(self, px, py, pdir, idir, speed):
        self.frame = (self.frame + + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        self.x += speed
        if self.x < px: self.dir = 1
        elif self.x > py: self.dir = -1
        #플레이어와 부끄의 방향이 같을 때 부끄 정지
        if self.dir != pdir and self.dir != idir:
            self.condition = 0
            self.t = 0

        #방향이 다를 때 부끄 캐릭터 방향으로
        elif self.dir == pdir or self.dir == idir:
            self.condition = 1

        if self.condition == 1 and -500 < px - self.x < 500:
            self.t += 1
            t = self.t/1000000
            self.x = (1-t) * self.x + t * px
            self.y = (1-t) * self.y + t * py

class Koopa:
    image = None
    def __init__(self):
        if Koopa.image == None:
            Koopa.image = load_image('koopa.png')
        self.x, self.y = 600, 200
        self.w, self.h = 100, 100
        self.speed = RUN_SPEED_PPS * game_framework.frame_time
        self.power = 0
        self.dir = -1
        self.frame = 0
        self.condition = 0 #0 == idle 1 == attack
        self.gravity = 0
        self.timer = 0
        self.hitTimer = 0

    def get_bb(self):
        if self.condition == 1:
            if time.time() - self.timer <= 0.4: return self.x - 50, self.y - 50, self.x + 50, self.y + 50
            else:
                return self.x - 30, self.y - 30, self.x + 30, self.y + 30
        else:
            return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def draw(self):
        if (int)(self.hitTimer) != 0 and (int)(self.frame) % 2 == 0:
            self.image.clip_draw(0,0,0,0,self.x,self.y)
        elif self.condition == 0:
            self.image.clip_draw((int)(self.frame) * 100, 0, 100, 100, self.x, self.y)
        elif self.condition == 1:
            if time.time() - self.timer <= 0.4: self.image.clip_draw(self.power*100, 100, 100, 100, self.x, self.y)
            elif time.time() - self.timer <= 0.6: self.image.clip_draw(0, 200, 100, 100, self.x, self.y)
            elif time.time() - self.timer <= 0.8: self.image.clip_draw(100, 200, 70, 70, self.x, self.y)
            elif time.time() - self.timer <= 1.0: self.image.clip_draw(170, 200, 60, 60, self.x, self.y)
            else: self.image.clip_draw((int)(self.frame) * 60 + 240, 200, 60, 60, self.x, self.y)
        elif self.condition == 2:
            self.image.clip_draw(0, 400, 100, 100, self.x, self.y)


    def stop(self):
        self.gravity = 0

    def update(self,speed):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        if self.condition == 0: self.rest()
        elif self.condition == 1: self.attack()
        self.y -= self.gravity

        #무적 처리
        if time.time() - self.hitTimer >= 1.0:
            self.hitTimer = 0
        pass

    def attack(self):
        print("공격 접근")
        if self.timer == 0: self.timer = time.time()
        elif 1.0 < time.time() - self.timer <= 5:
            self.x += self.speed * self.dir * 25
            if 2 < time.time() - self.timer <= 3 and self.power > 1:
                self.y += GRAVITY_SPEED_PPS * game_framework.frame_time * 2
        elif time.time() - self.timer > 5:
            self.condition = 0
            self.y += 20
            self.timer = 0
        if self.x <= 30:
            self.x = 50
            self.dir = 1
        elif self.x >= 770:
            self.x = 750
            self.dir = -1
        #self.x = clamp(30,self.x, 770)

    def rest(self):
        print("휴식 중")
        if self.timer == 0: self.timer = time.time()
        elif time.time() - self.timer >= 2:
            self.condition = 1
            self.timer = 0

    def hit(self):
        print("아야")
        if self.hitTimer == 0:
            self.hitTimer = time.time()
            self.power += 1








