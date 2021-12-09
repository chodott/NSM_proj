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
        if self.condition == 1 or self.condition == -1: return -100,-100,-100,-100
        return self.x-15, self.y-15, self.x+15, self.y+15

    def draw(self):
        if self.x !=0 and self.y != 0:
            if self.condition == 1: self.image.clip_draw(0,0,30,15,self.x,self.y)
            elif self.condition == -1: self.image.clip_draw(0,30,30,30,self.x,self.y)
            else:
                if self.dir == -1: self.image.clip_draw(0,270-(int)(self.frame)*30,30,30,self.x,self.y)
                elif self.dir == 1: self.image.clip_draw(30,270-(int)(self.frame)*30,30,30,self.x,self.y)

    def stop(self):
        self.gravity = 0

    def update(self):
        if self.x != 0 and self.y != 0:
            self.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
            self.x += -server.player.gap
            self.collide_check()
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

    def collide_check(self):

        for grass in server.grassTile1:
            if server.collide(self, grass):
                self.stop()

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

        for ib in server.ibs:
            if server.collide(self, ib) and self.condition != -1:
                self.stop()
                break

        for nb in server.nbs:
            if server.collide(self, nb) and self.condition != -1:
                self.stop()
                break

        for eb in server.ebs:
            if server.collide(self, eb) and self.condition != -1:
                self.stop()
                break

        if game_framework.cur_level == 2 or game_framework.cur_level == 3:
            for ac in server.aircraft:
                if server.collide(self, ac):
                    if ac.active == 1: self.x += ac.speed
                    if self.x <= ac.x - ac.w / 2 + 20: self.dir = 1
                    elif self.x >= ac.x + ac.w / 2 - 20: self.dir = -1
                    self.stop()

        for troopa in server.troopas:
            if troopa.condition == 0 and troopa.speed != 0 :
                if server.collide(self, troopa):
                    self.hit(1)
                    server.player.attack_sound.play()



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
        if self.x != 0 and self.y != 0:
            if self.dir == -1:
                if self.condition == 0:
                    self.image.clip_draw(30,0 + (int)(self.frame) * 30,self.w,self.h, self.x, self.y);
                elif self.condition == -1:
                    self.image.clip_draw(30, 90, self.w, self.h, self.x, self.y);
                elif self.condition == 1:
                    self.image.clip_draw(0,800 - 50 - (int)(self.frame) * 50,self.w,self.h, self.x, self.y);
                elif self.condition == 2:
                    self.image.clip_draw(30, 800 - 50 - (int)(self.frame) * 50, self.w, self.h, self.x, self.y);
            else:
                if self.condition == 0:
                    self.image.clip_draw(30,0 + (int)(self.frame) * 30,self.w,self.h, self.x, self.y);
                elif self.condition == -1:
                    self.image.clip_draw(30, 90, self.w, self.h, self.x, self.y);
                elif self.condition == 1:
                    self.image.clip_draw(60,800 - 50 - (int)(self.frame) * 50,self.w,self.h, self.x, self.y);


    def update(self):
        if self.x != 0 and self.y != 0:
            self.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
            self.collide_check()
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
                self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
                if self.y <= self.goal:
                    self.goal = 300
                    self.y += game_framework.frame_time * GRAVITY_SPEED_PPS / 2
                elif self.y >= self.goal:
                    self.goal = 150
                    self.y -= game_framework.frame_time * GRAVITY_SPEED_PPS / 2
            self.y -= self.gravity
            self.x += -server.player.gap

    def collide_check(self):

        for grass in server.grassTile1:
            if server.collide(self, grass):
                self.stop()

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

        for ib in server.ibs:
            if server.collide(self, ib) and self.condition != -1:
                self.stop()
                break

        for nb in server.nbs:
            if server.collide(self,nb):
                if self.y - 15 >= nb.y + 10 and self.condition != -1:
                    self.stop()
                    break
                elif nb.x <= self.x - 15 < nb.x + 15:
                    self.dir = 1
                    self.x = nb.x + 15
                    if self.condition == 0:
                        server.player.block_sound.play()
                        nb.broke = 1
                        server.nbs.remove(nb)
                        game_world.remove_object(nb)
                elif nb.x - 15 <= self.x + 15 < nb.x:
                    self.dir = -1
                    self.x = nb.x - 15
                    if self.condition == 0:
                        server.player.block_sound.play()
                        nb.broke = 1
                        server.nbs.remove(nb)
                        game_world.remove_object(nb)

        for eb in server.ebs:
            if server.collide(self, eb) and self.condition != -1:
                self.stop()
                break

        if game_framework.cur_level == 2 or game_framework.cur_level == 3:
            for ac in server.aircraft:
                if server.collide(self, ac):
                    if ac.active == 1: self.x += ac.speed
                    if self.condition != 0:
                        if self.x <= ac.x - ac.w / 2 + 20: self.dir = 1
                        elif self.x >= ac.x + ac.w / 2 - 20: self.dir = -1
                    self.stop()

        for troopa in server.troopas:
            if server.collide(self, troopa) and self != troopa and self.condition == 0:
                troopa.death()


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
        if self.x != 0 and self.y != 0:
            if self.condition == 0 and self.dir > 0:
                self.image.clip_draw(30,60,self.w,self.h,self.x,self.y);

            elif self.condition == 0 and self.dir < 0:
                self.image.clip_draw(0, 60, self.w, self.h, self.x, self.y);

            elif self.condition == 1 and self.dir > 0:
                self.image.clip_draw(30, 150 - (int)(self.frame) * 30, self.w, self.h, self.x, self.y);

            elif self.condition == 1 and self.dir < 0:
                self.image.clip_draw(0, 150 - (int)(self.frame) * 30, self.w, self.h, self.x, self.y);

    def update(self):
        if self.x != 0 and self.y != 0:
            self.frame = (self.frame + + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
            self.x += -server.player.gap
            if self.x < server.player.x: self.dir = 1
            elif self.x > server.player.y: self.dir = -1
            #플레이어와 부끄의 방향이 같을 때 부끄 정지
            if self.dir != server.player.idle_dir and self.dir != server.player.idle_dir:
                self.condition = 0
                self.t = 0

            #방향이 다를 때 부끄 캐릭터 방향으로
            elif self.dir == server.player.idle_dir or self.dir == server.player.idle_dir:
                self.condition = 1

            if self.condition == 1 and -500 < server.player.x - self.x < 500:
                self.t += 1
                t = self.t/1000000
                self.x = (1-t) * self.x + t * server.player.x
                self.y = (1-t) * self.y + t * server.player.y

class Koopa:
    image = None
    def __init__(self):
        if Koopa.image == None:
            Koopa.image = load_image('koopa.png')
        self.x, self.y = 600, 600
        self.w, self.h = 100, 100
        self.speed = RUN_SPEED_PPS * game_framework.frame_time
        self.power = 2
        self.dir = -1
        self.frame = 0
        self.condition = 0 #0 == idle 1 == attack 2 == death
        self.hitcnt = 0
        self.gravity = 0
        self.timer = 0
        self.hitTimer = 0
        self.sound = load_wav('bowser.wav')
        self.sound.set_volume(200)

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
            if self.dir == -1: self.image.clip_draw((int)(self.frame) * 100, 0, 100, 100, self.x, self.y)
            else: self.image.clip_draw((int)(self.frame) * 100, 100, 100, 100, self.x, self.y)
        elif self.condition == 1:
            if self.dir == -1:
                if time.time() - self.timer <= 0.4: self.image.clip_draw(self.power*100, 200, 100, 100, self.x, self.y)
                elif time.time() - self.timer <= 0.6: self.image.clip_draw(0, 300, 100, 100, self.x, self.y)
                elif time.time() - self.timer <= 0.8: self.image.clip_draw(100, 310, 70, 70, self.x, self.y)
                elif time.time() - self.timer <= 1.0: self.image.clip_draw(170, 310, 60, 60, self.x, self.y)
                else: self.image.clip_draw((int)(self.frame) * 60 + 240, 300, 60, 60, self.x, self.y)
            else:
                if time.time() - self.timer <= 0.4: self.image.clip_draw(500 - self.power*100, 200, 100, 100, self.x, self.y)
                elif time.time() - self.timer <= 0.6: self.image.clip_draw(500, 400, 100, 100, self.x, self.y)
                elif time.time() - self.timer <= 0.8: self.image.clip_draw(430, 420, 70, 70, self.x, self.y)
                elif time.time() - self.timer <= 1.0: self.image.clip_draw(370, 420, 60, 60, self.x, self.y)
                else: self.image.clip_draw((int)(self.frame) * 60 + 240, 300, 60, 60, self.x, self.y)
        elif self.condition == 2:
            if self.dir == -1: self.image.clip_draw(0, 400, 115, 100, self.x, self.y)
            else: self.image.clip_draw(115, 400, 115, 100, self.x, self.y)


    def stop(self):
        self.gravity = 0

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
        if self.condition != 2:
            self.collide_check()
        if self.condition == 0: self.rest()
        elif self.condition == 1: self.attack()
        elif self.condition == 2: server.ui.gameclear = 1
        self.y -= self.gravity

        #무적 처리
        if time.time() - self.hitTimer >= 1.0:
            self.hitTimer = 0
        pass

    def attack(self):
        if self.timer == 0:
            self.timer = time.time()
            self.sound.play()
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

    def rest(self):
        if self.timer == 0: self.timer = time.time()
        elif time.time() - self.timer >= 2:
            self.condition = 1
            self.timer = 0
        if server.player.x < self.x:
            self.dir = -1
        else:
            self.dir = 1

    def hit(self, case):
        if case == 1:
            self.hitcnt += 1
        if self.hitTimer == 0 and (case == 0 or self.hitcnt == 5):
            self.hitTimer = time.time()
            self.power += 1
            self.hitcnt = 0
        if self.power == 3:
            self.condition = 2

    def collide_check(self):
        if server.collide(self,server.arena):
            self.stop()





