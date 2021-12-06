# 파이어볼 곡선이동, 충돌처리, 탄환추가, 파워가 변해도 유지 추가 필요

from pico2d import *
import time
import game_world
import game_framework

import select_state
import over_state
import load_state
import server

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

BALL_SPEED_KMPH = 50.0
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
        player.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
        player.collide_check()
        if player.jumping == 1: pass
        elif player.speed < 0:
            player.accel += ACCEL_PPS
        elif player.speed > 0:
            player.accel -= ACCEL_PPS
        #떨림 멈춤
        if -0.1 < player.speed < 0.1:
            player.speed = 0
        else:
            player.speed = (player.dir*RUN_SPEED_PPS + player.accel) * game_framework.frame_time
        #움직이는 중이면 거리 증가
        if player.move: player.distance += player.speed
        if game_framework.cur_level == 4:
            player.x += player.speed
        elif player.move == 0:
            player.x += player.speed
            player.gap = 0
        elif player.distance < 400 or player.distance > 2600:
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
        player.death_check()

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
        elif event == LEFT_DOWN:
            player.dir -= 1
            player.idle_dir = -1
        elif event == RIGHT_UP:
            player.dir -= 1
        elif event == LEFT_UP:
            player.dir += 1
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
        player.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
        player.move = 1
        if -MAX_SPEED_PPS < player.speed/game_framework.frame_time < MAX_SPEED_PPS:
            if player.dir == 1: player.accel += ACCEL_PPS
            elif player.dir == -1: player.accel -= ACCEL_PPS
        player.speed = (player.dir*RUN_SPEED_PPS + player.accel) * game_framework.frame_time
        player.collide_check()
        if player.move: player.distance += player.speed
        if game_framework.cur_level == 4:
            player.x += player.speed
        elif player.distance < 400 or player.distance > 2600:
            player.x += player.speed
            player.gap = 0
        elif player.move == 0:
            player.x += player.speed
            player.gap = 0
            pass
        else:
            player.gap = player.speed
        if player.jumping:
            if player.y >= player.mark + player.maxjump: player.mark = -150
            else: player.y += JUMP_SPEED_PPS * game_framework.frame_time
        player.y -= player.gravity
        if time.time() - player.hitTimer > 2: player.hitTimer = 0
        player.death_check()

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
        player.collide_check()
        if player.gravity != 0:
            player.y -= player.gravity * 2
        player.death_check()

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
        player.collide_check()
        if player.gravity != 0:
            player.y -= player.gravity /2

        else:
            player.x += RUN_SPEED_PPS * game_framework.frame_time * 2
            player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        player.death_check()

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
        player.death_check()



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
        self.power = 2
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
        self.hitTimer = 0
        self.sit = 0
        self.cnt = 0
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

    def attack(self):
        self.jumping = 1
        self.mark = self.y
        self.maxjump = 80

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

    def collide_check(self):
        # 쿠파 충돌
        if game_framework.cur_level == 4:
            if server.collide(self, server.koopa):
                if self.y - self.h / 2 >= server.koopa.y + 20 and server.koopa.condition == 0:
                    self.attack()
                    server.koopa.hit(0)
                else:
                    self.hit()

            # 아레나 충돌
            if server.collide(self, server.arena):
                self.stop()
        else:
            #깃발 충돌
            if server.collide(self, server.flag):
                self.cur_state = EndState
                self.x = server.flag.x
                server.flag.condi = 1
                return

            #토관 충돌
            for pipe in server.pipes:
                if server.collide(self, pipe):
                    if self.y - self.h/2 >= pipe.y + pipe.h/2 - 5:
                        self.stop()
                        break
                        #여기 토관 이동 추가해야해
                    elif pipe.x < self.x - 15 < pipe.x + 30:
                        self.meetwall()
                        break
                    elif pipe.x - 30 < self.x + 15 < pipe.x:
                        self.meetwall()
                        break

            #플랫폼 충돌
            for grass in server.grassTile1:
                if server.collide(self,grass):
                    if self.y - self.h / 2 > grass.y + 10:
                        self.stop()
                    else:
                        self.meetwall()
                    break

            #비행정 충돌
            if game_framework.cur_level == 2 or game_framework.cur_level == 3:
                if server.collide(self, server.aircraft):
                    self.stop()
                    if game_framework.cur_level == 3:
                        server.aircraft.active = 1
                    elif game_framework.cur_level == 2:
                        self.y += server.aircraft.speed * 2

            #아이템 블록 충돌
            jumped = 0
            for ib in server.ibs:
                if server.collide(self, ib):
                    if self.y - self.h / 2 > ib.y + 10:
                        self.stop()
                        break
                    elif self.y + self.h / 2 <= ib.y - 10 and (self.jumping == 1 or jumped):
                        if ib.broke != 1:
                            server.items[server.ibs.index(ib)].x = ib.x
                            server.items[server.ibs.index(ib)].y = ib.y + 3
                            server.items[server.ibs.index(ib)].hit()
                            ib.broke = 1;
                        self.jumping = 0
                        jumped = 1
                        break
                    elif ib.x + 10 < self.x - 15 < ib.x + 15:
                        self.meetwall()
                        break
                    elif ib.x - 15 < self.x + 15 < ib.x - 10:
                        self.meetwall()
                        break

            #노멀 블록 충돌
            for nb in server.nbs:
                if server.collide(self, nb):
                    if self.y - self.h / 2 >= nb.y + 10:
                        self.stop()
                        break
                    elif self.y + self.h / 2 <= nb.y - 10 and (self.jumping == 1 or jumped):
                        if self.power >= 1:
                            nb.broke = 1
                            server.nbs.remove(nb)
                            game_world.remove_object(nb)
                        self.jumping = 0
                        break
                    elif nb.x + 10 <= self.x - 15 < nb.x + 15:
                        self.meetwall()
                        break
                    elif nb.x - 15 <= self.x + 15 < nb.x - 10:
                        self.meetwall()
                        break

            #엔딩 블록 충돌
            for eb in server.ebs:
                if server.collide(self, eb):
                    if self.y - self.h / 2 >= eb.y + 12:
                        self.stop()
                    elif eb.x + 10 <= self.x - 15 < eb.x + 15:
                        self.meetwall()
                        break
                    elif eb.x - 15 <= self.x + 15 < eb.x - 10:
                        self.meetwall()
                        break

            #엉금엉금 충돌
            for troopa in server.troopas:
                if server.collide(self, troopa):
                    if self.y - self.h / 2 >= troopa.y + 10:
                        self.attack()
                        troopa.hit(self.x)
                        break
                    else:
                        if troopa.speed == 0:
                            troopa.hit(self.x)
                            break
                        else:
                            self.hit()
                            break

            #굼바 충돌
            for goomba in server.goombas:
                if server.collide(self, goomba):
                    if self.y - self.h / 2 >= goomba.y + 10:
                        self.attack()
                        goomba.hit(0)
                        break
                    elif goomba.condition == 0:
                        self.hit()
                        break

            #코인 충돌
            for coin in server.coins:
                if server.collide(self,coin):
                    server.ui.coin += 1
                    game_world.remove_object(coin)
                    server.coins.remove(coin)
                    break


            #아이템 충돌
            for item in server.items:
                if server.collide(self,item):
                    self.transTimer = time.time()
                    self.upgrade(item.case)
                    game_world.remove_object(item)
                    server.items.remove(item)
                    break

    def death_check(self):
        if server.ui.alarm <= 0: self.power = -1
        if self.y <= 10 and self.power != 4:
            self.power = -1
        if self.power == -1:
            game_framework.Life -= 1
            self.power = 4
            self.gap = 0
            self.speed = 0
            self.frame = 0
            self.hitTimer = time.time()
            if game_framework.Life == -1:
                self.cur_state = DeathState
            else:
                self.cur_state = DeathState

        if self.power == 4:
            if game_framework.Life == -1 and self.y <= -10:
                game_framework.change_state(over_state)
                game_world.remove_object(server.player)
            if game_framework.Life >= 0 and self.y <= -10:
                game_framework.change_state(load_state)
                game_world.remove_object(server.player)

        if self.x >= 700 and game_framework.cur_level != 4:
            game_framework.clear_level += 1
            game_framework.change_state(select_state)


    def draw(self):
        self.cur_state.draw(self)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self,event)

    def fire_ball(self):
        if self.power == 2 and time.time() - self.transTimer > 0.3:
            self.transTimer = time.time()
            server.fbs[self.cnt].active = 1
            server.fbs[self.cnt].x = self.x; server.fbs[self.cnt].y = self.y; server.fbs[self.cnt].dir = self.idle_dir
            self.cnt = (self.cnt + 1) % 10
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
        self.x, self.y = -100, -100
        self.dir = 0
        self.active = 0
        self.speed = 0
        self.timer = 0
        self.frame = 0

    def draw(self):
        if self.active == 1:
            self.image.clip_draw(self.frame*20,0,20,20,self.x,self.y)

    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def update(self):
        if self.active == 1:
            self.x -= server.player.gap
            self.x += BALL_SPEED_PPS * game_framework.frame_time * self.dir
            if self.timer != 0:
                self.y += GRAVITY_SPEED_PPS * game_framework.frame_time
                if time.time() - self.timer >= 0.1:
                    self.timer = 0
            else: self.y -= GRAVITY_SPEED_PPS * game_framework.frame_time
            self.frame = (int)(self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
            self.collide_check()
        pass

    def collide_check(self):
        if game_framework.cur_level == 4:
            if server.collide(self, server.koopa):
                self.active = 0
                if server.koopa.condition == 0:
                    server.koopa.hit(1)
                return

            elif server.collide(self,server.arena):
                self.timer = time.time()
                return

        if self.y == 10:
            self.active = 0
            return


        for grass in server.grassTile1:
            if server.collide(self,grass):
                self.timer = time.time()
                return

        for pipe in server.pipes:
            if server.collide(self,pipe):
                if self.y - 10 >= pipe.y + 10:
                    self.timer = time.time()
                else:
                    self.active = 0
                    return

        for ib in server.ibs:
            if server.collide(self,ib):
                if self.y - 10 >= ib.y + 10:
                    self.timer = time.time()
                else:
                    self.active = 0
                    return

        for nb in server.nbs:
            if server.collide(self,nb):
                if self.y - 10 >= nb.y + 10:
                    self.timer = time.time()
                else:
                    self.active = 0
                    return

        for eb in server.ebs:
            if server.collide(self,eb):
                if self.y - 10 >= eb.y + 10:
                    self.timer = time.time()
                else:
                    self.active = 0
                    return

        for goomba in server.goombas:
            if server.collide(self,goomba):
                goomba.hit(1)
                self.active = 0
                return

        for troopa in server.troopas:
            if server.collide(self,troopa):
                troopa.death()
                self.active = 0
                return