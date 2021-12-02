# 파이어볼 곡선이동, 충돌처리, 탄환추가, 파워가 변해도 유지 추가 필요

from pico2d import *
import time
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 5.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

ACCEL_KMPH = 0.5
ACCEL_MPM = (ACCEL_KMPH * 1000.0 / 60.0)
ACCEL_MPS = (ACCEL_MPM / 60.0)
ACCEL_PPS = (ACCEL_MPS * PIXEL_PER_METER)

MAX_SPEED_KMPH = 25
MAX_SPEED_MPM = (MAX_SPEED_KMPH * 1000.0 / 60.0)
MAX_SPEED_MPS = (MAX_SPEED_MPM / 60.0)
MAX_SPEED_PPS = (MAX_SPEED_MPS * PIXEL_PER_METER)


JUMP_SPEED_KMPH = 60.0
JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

GRAVITY_SPEED_KMPH = 30.0
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)

BALL_SPEED_KMPH = 60.0
BALL_SPEED_MPM = (BALL_SPEED_KMPH * 1000.0 / 60.0)
BALL_SPEED_MPS = (BALL_SPEED_MPM / 60.0)
BALL_SPEED_PPS = (BALL_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

#Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE, UP_DOWN, DOWN_DOWN, DOWN_UP = range(8)
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP
}

class IdleState:
    def enter(player, event):
        if player.power == 0: player.h = 30
        elif player.power ==1 or player.power == 2: player.h = 60

        if event == RIGHT_DOWN:
            player.dir += 1
            player.idle_dir = 1
        elif event == LEFT_DOWN:
            player.dir -= 1
            player.idle_dir = -1
        elif event == RIGHT_UP:
            player.dir -= 1
        elif event == LEFT_UP:
            player.dir += 1
        elif event == UP_DOWN and player.gravity == 0:
            player.jumping = 1
            player.mark = player.y
            player.maxjump = 150
            player.y += JUMP_SPEED_PPS * game_framework.frame_time

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if player.speed < 0:
            player.accel += ACCEL_PPS
        elif player.speed > 0:
            player.accel -= ACCEL_PPS
        player.speed = (player.dir*RUN_SPEED_PPS + player.accel) * game_framework.frame_time
        if -0.1 < player.speed < 0.1: player.speed = 0
        if player.move: player.distance += player.speed
        if player.distance < 400 or player.distance > 2600 or player.move == 0:
            player.x += player.speed
            player.gap = 0
        else:
            player.gap = player.speed
        if player.jumping:
            if player.y >= player.mark + player.maxjump:
                player.jumping = 0
            else:
                player.y += JUMP_SPEED_PPS * game_framework.frame_time
        player.y -= player.gravity
        if time.time() - player.hitTimer > 2: player.hitTimer = 0

    def draw(player):
        if player.hitTimer != 0 and (int)(player.frame) % 2 == 0:
            player.image.clip_draw(0,0,0,0,player.x,player.y)
        elif player.h == 40:
            if player.idle_dir == 1: player.image.clip_draw(330, 500, player.w, player.h, player.x, player.y)
            elif player.idle_dir == -1: player.image.clip_draw(300, 500, player.w, player.h, player.x, player.y)
        elif player.h == 50:
            if player.idle_dir == 1: player.image.clip_draw(330, 450, player.w, player.h, player.x, player.y)
            elif player.idle_dir == -1: player.image.clip_draw(300, 450, player.w, player.h, player.x, player.y)
        else:
            if player.power == 0:
                if player.idle_dir == 1: player.image.clip_draw(150, 0, player.w, player.h, player.x, player.y)
                elif player.idle_dir == -1: player.image.clip_draw(0, 0, player.w, player.h, player.x, player.y)
            elif player.power == 1:
                if player.idle_dir == 1: player.image.clip_draw(0, 600-60, player.w, player.h, player.x, player.y)
                elif player.idle_dir == -1: player.image.clip_draw(60, 600-60, player.w, player.h, player.x, player.y)
            elif player.power == 2:
                if player.idle_dir == 1: player.image.clip_draw(120, 600 - 240, player.w, player.h, player.x, player.y)
                elif player.idle_dir == -1: player.image.clip_draw(60, 600 - 180, player.w, player.h, player.x, player.y)



class RunState:
    def enter(player, event):
        if player.gravity == 0 and player.h == 40:
            player.y += 20
        if player.power == 0: player.h = 30
        elif player.power ==1 or player.power == 2: player.h = 60

        if event == RIGHT_DOWN:
            player.dir += 1
            player.idle_dir = 1
            #player.speed += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            player.dir -= 1
            player.idle_dir = -1
            #player.speed -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            player.dir -= 1
            #player.speed -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            player.dir += 1
            #player.speed += RUN_SPEED_PPS
        elif event == UP_DOWN and player.gravity == 0:
            player.jumping = 1
            player.maxjump = 150
            player.mark = player.y
            player.y += JUMP_SPEED_PPS * game_framework.frame_time

    def exit(player, event):
        if event == SPACE:
            player.fire_ball()
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if -MAX_SPEED_PPS < player.speed/game_framework.frame_time < MAX_SPEED_PPS:
            if player.dir == 1: player.accel += ACCEL_PPS
            elif player.dir == -1: player.accel -= ACCEL_PPS

        player.speed = (player.dir*RUN_SPEED_PPS + player.accel) * game_framework.frame_time
        if player.move: player.distance += player.speed
        if player.distance < 400 or player.distance > 2600 or player.move == 0:
            player.x += player.speed
            player.gap = 0
        else:
            player.gap = player.speed
        if player.jumping:
            if player.y >= player.mark + player.maxjump: player.mark = -150
            else: player.y += JUMP_SPEED_PPS * game_framework.frame_time
        player.y -= player.gravity
        if time.time() - player.hitTimer > 2: player.hitTimer = 0

    def draw(player):
        if player.hitTimer != 0 and (int)(player.frame) % 2 == 0:
            player.image.clip_draw(0,0,0,0,player.x,player.y)
        elif player.h == 40:
            if player.idle_dir == 1: player.image.clip_draw(330, 500, player.w, player.h, player.x, player.y)
            elif player.idle_dir == -1: player.image.clip_draw(300, 500, player.w, player.h, player.x, player.y)
        elif player.h == 50:
            if player.idle_dir == 1: player.image.clip_draw(330, 450, player.w, player.h, player.x, player.y)
            elif player.idle_dir == -1: player.image.clip_draw(300, 450, player.w, player.h, player.x, player.y)
        else:
            if player.power == 0:
                if player.dir == 1: player.image.clip_draw(180+30*(int)(player.frame), 60, player.w, player.h, player.x, player.y)
                elif player.dir == -1: player.image.clip_draw(30*(int)(player.frame), 60, player.w, player.h, player.x, player.y)
            elif player.power == 1:
                if player.idle_dir == 1: player.image.clip_draw(30 * (int)(player.frame), 600-120, player.w, player.h, player.x, player.y)
                elif player.idle_dir == -1: player.image.clip_draw(270 - 30*(int)(player.frame), 600-120, player.w, player.h, player.x, player.y)
            elif player.power == 2:
                if player.idle_dir == 1: player.image.clip_draw(30 * (int)(player.frame), 600 - 240, player.w, player.h, player.x, player.y)
                elif player.idle_dir == -1: player.image.clip_draw(270 - 30 * (int)(player.frame), 600 - 240, player.w, player.h, player.x, player.y)

class SitState:
    def enter(player, event):
        player.speed = 0
        player.gap = 0
        player.accel = 0
        player.jumping = 0
        if player.h == 60:
            player.h = 40
        pass

    def exit(player, event):
        player.jumping = 0
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        if player.gravity != 0:
            player.y -= player.gravity * 2
        pass

    def draw(player):
        if player.hitTimer != 0 and (int)(player.frame) % 2 == 0:
            player.image.clip_draw(0,0,0,0,player.x,player.y)

        elif player.idle_dir == -1:
            if player.power == 0: player.image.clip_draw(360-60, 0, player.w, player.h, player.x, player.y)
            elif player.power == 1:player.image.clip_draw(360-90, 600-40, player.w, player.h, player.x, player.y)
            elif player.power == 2:player.image.clip_draw(600-30, 600-40, player.w, player.h, player.x, player.y)

        elif player.idle_dir == 1:
            if player.power == 0: player.image.clip_draw(360-30, 0, player.w, player.h, player.x, player.y)
            elif player.power == 1:player.image.clip_draw(360-60, 600-40, player.w, player.h, player.x, player.y)
            elif player.power == 2:player.image.clip_draw(360-60, 600-40, player.w, player.h, player.x, player.y)



class EndState:
    def enter(player, event):
        player.gap = 0
        pass

    def exit(player, event):
        pass

    def do(player):
        if player.gravity != 0:
            player.y -= player.gravity /2

        else:
            player.x += RUN_SPEED_PPS * game_framework.frame_time * 2
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(player):
        if player.gravity != 0:
            if player.power == 0:
                player.image.clip_draw(150, 90, 30, 30, player.x, player.y)
            elif player.power == 1:
                player.image.clip_draw(330,540,30,60,player.x,player.y)
            elif player.power == 1:
                player.image.clip_draw(330,540,30,60,player.x,player.y)
        else:
            if player.power == 0:
                player.image.clip_draw(180 + 30 * (int)(player.frame), 60, player.w, player.h, player.x, player.y)
            elif player.power == 1:
                player.image.clip_draw(30 * (int)(player.frame), 600 - 120, player.w, player.h, player.x, player.y)
            elif player.power == 2:
                player.image.clip_draw(30 * (int)(player.frame), 600 - 240, player.w, player.h, player.x, player.y)


class DeathState:

    def enter(player, event):
        pass

    def exit(player, event):
        pass

    def do(player):
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if time.time() - player.hitTimer < 0.5:
            player.y += JUMP_SPEED_PPS * game_framework.frame_time
        player.y -= GRAVITY_SPEED_PPS * game_framework.frame_time



    def draw(player):
        # if player.power <= 0:
        #     player.image.clip_draw((int)(player.frame)*30,150,30,30,player.x,player.y)
        # elif player.power == 1:
        #     player.image.clip_draw((int)(player.frame)*60,300,60,60,player.x,player.y)
        # elif player.power == 2:

        player.image.clip_draw((int)(player.frame) * 30, 150, 30, 30, player.x, player.y)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN:RunState,
                SPACE: IdleState, UP_DOWN: IdleState,
                DOWN_DOWN: SitState, DOWN_UP: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SPACE: RunState, UP_DOWN: RunState,
               DOWN_DOWN: SitState, DOWN_UP:RunState},
    EndState: {RIGHT_UP: EndState, LEFT_UP: EndState,
               LEFT_DOWN: EndState, RIGHT_DOWN: EndState,
               SPACE: EndState, UP_DOWN: EndState,
               DOWN_DOWN: EndState, DOWN_UP: EndState},
    DeathState:{RIGHT_UP: DeathState, LEFT_UP: DeathState,
               LEFT_DOWN: DeathState, RIGHT_DOWN: DeathState,
               SPACE: DeathState, UP_DOWN: DeathState,
                DOWN_DOWN: DeathState, DOWN_UP: DeathState},
    SitState:{RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: RunState, RIGHT_DOWN: RunState,
               SPACE: SitState, UP_DOWN: IdleState,
                DOWN_DOWN: SitState, DOWN_UP: SitState}
}


class Player:
    speed = 0
    x = 15
    y = 200
    def __init__(self):
        self.image = load_image('mini30.png')
        self.w, self.h = 30, 30
        self.power = 0
        self.accel = ACCEL_PPS
        self.frame = 0
        self.idle_dir = 1
        self.dir = 0  # -1 left +1 right
        self.move = 1
        self.trans = 0
        self.transTimer = 0
        self.jumping = 0
        self.maxjump = 150
        self.gap = 0
        self.mark = 0
        self.gravity = 0
        self.distance = 0
        self.onAir = 1
        self.hitTimer = 0
        self.sit = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self,None)


    def get_bb(self):
        if self.sit:
            return self.x-15, self.y-20, self.x+15, self.y + 20
        if self.power == 0:
            return self.x-15, self.y - 15, self.x + 15, self.y + 15
        elif self.power == 1 or self.power == 2:
            return self.x - 15, self.y - self.h/2, self.x + 15, self.y + self.h/2
        else:
            return -100,-100,-100,-100

    def stop(self):
        self.gravity = 0
        self.onAir = 0

    def attack(self):
        self.jumping = 1
        self.mark = self.y
        self.maxjump = 60

    def meetwall(self):
        self.x -= self.speed
        self.accel = 0
        self.move = 0

    def hit(self):
        if self.hitTimer == 0 and self.power > -1:
            self.power -= 1
            self.hitTimer = time.time()
            if self.power == 0:
                self.h = 30
            else: self.h = 60

    def upgrade(self, type=-1):
        if type == 0 and self.power == 0:
            self.power = 1
            self.trans = 1
        elif type == 1:
            self.power = 2
            self.trans = 1
        if type == -1:
            if self.h == 30 and time.time() - self.transTimer < 0.3: self.h = 40; self.y += 5
            elif self.h == 40 and 0.3 < time.time() - self.transTimer < 0.6: self.h = 50; self.y += 5
            elif self.h == 50 and 0.6 < time.time() - self.transTimer < 0.9: self.h = 60; self.y += 5
        if self.h == 60: self.trans = 0
        

    def draw(self):
        self.cur_state.draw(self)

    def update(self, speed):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self,event)

    def fire_ball(self):
        if self.power == 2 and time.time() - self.transTimer > 0.5:
            self.fb[self.fbcnt].x, self.fb[self.fbcnt].y, self.fb[self.fbcnt] = self.x, self.y, self.dir
            self.fbcnt = (self.fbcnt + 1) % 10
            pass

    def warp(self):
        if self.x < self.goalpipe:
            self.speed = RUN_SPEED_PPS * game_framework.frame_time * 2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    pass


class FireBall:
    image = None
    def __init__(self):
        if FireBall.image == None:
            self.image = load_image('fireball.png')
        self.x, self.y = 100, -100
        self.dir = dir
        self.speed = BALL_SPEED_PPS
        self.upspeed = 0
        self.condition = 0
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame*20,0,20,20,self.x,self.y)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def update(self, speed):
        self.x += speed
        self.x += BALL_SPEED_PPS * game_framework.frame_time * self.dir
        self.y -= GRAVITY_SPEED_PPS * game_framework.frame_time
        self.frame = (int)(self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        pass