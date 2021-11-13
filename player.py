# 파이어볼 곡선이동, 충돌처리, 탄환추가, 파워가 변해도 유지 추가 필요

from pico2d import *
import game_world

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

#Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE = range(4)
key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE) : SPACE
}

class IdleState:
    def enter(player, event):
        if event == RIGHT_DOWN:
            player.dir += 1
            player.idle_dir = 1
        elif event == LEFT_DOWN:
            player.dir -= 1
            player.idle_dir = 1
        elif event == RIGHT_UP:
            player.dir -= 1
        elif event == LEFT_UP:
            player.dir += 1
        player.runcnt = 0

    def exit(player, event):
        pass

    def do(player):
        player.frame = (player.frame+1) % 4
        if player.speed < 0: player.speed += 1
        elif player.speed > 0: player.speed -= 1
        player.x += player.speed
        player.y -= 5

    def draw(player):
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
        if event == RIGHT_DOWN:
            player.dir = 1
            player.idle_dir = 1
        elif event == LEFT_DOWN:
            player.dir = -1
            player.idle_dir = -1
        elif event == RIGHT_UP:
            player.dir -= 1
        elif event == LEFT_UP:
            player.dir += 1

    def exit(player, event):
        pass

    def do(player):
        player.frame = (player.frame + 1) % 4
        if player.dir == -1 and player.speed > - 10: player.speed -= 1
        elif player.dir == 1 and player.speed < 10: player.speed += 1
        player.x += player.speed
        player.y -= 5


    def draw(player):
        if player.power == 0:
            if player.dir == 1: player.image.clip_draw(180+30*player.frame, 60, player.w, player.h, player.x, player.y)
            elif player.dir == -1: player.image.clip_draw(30*player.frame, 60, player.w, player.h, player.x, player.y)
        elif player.power == 1:
            if player.idle_dir == 1: player.image.clip_draw(30 * player.frame, 600-120, player.w, player.h, player.x, player.y)
            elif player.idle_dir == -1: player.image.clip_draw(270 - 30*player.frame, 600-120, player.w, player.h, player.x, player.y)
        elif player.power == 2:
            if player.idle_dir == 1: player.image.clip_draw(30 * player.frame, 600 - 240, player.w, player.h, player.x, player.y)
            elif player.idle_dir == -1: player.image.clip_draw(270 - 30 * player.frame, 600 - 240, player.w, player.h, player.x, player.y)




next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState,
                RIGHT_DOWN: RunState, LEFT_DOWN:RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState,
               LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState}
}



class Player:
    def __init__(self):
        self.image = load_image('mini30.png')
        self.x, self.y = (50,200)
        self.w, self.h = 30, 30
        self.power = 1
        self.speed = 0
        self.frame = 0
        self.idle_dir = 1
        self.dir = 0  # -1 left +1 right
        self.jumping = 0
        self.jumpcnt = 0
        self.onAir = 1
        self.hitTimer = 0
        self.attack = 0
        self.fb = FireBall()
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self,None)

    def draw(self):
        self.cur_state.draw(self)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self,event)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)


    # def draw(self):
    #     self.cur_state.draw(self)
    #     # 꼬마 마리오
    #     if self.power == 0:
    #         if self.dir == -1:
    #             if self.jumping == 1:
    #                 if self.jumpCnt <= 6: self.image.clip_draw(150 - 30*self.frame, 120, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(0, 120, self.w, self.h, self.x, self.y)
    #
    #             else: self.image.clip_draw(30*self.frame, 60, self.w, self.h, self.x, self.y)
    #         elif self.dir == 0:
    #             if self.idle_dir == -1:
    #                 if self.jumping == 1:
    #                     if self.jumpCnt <= 6: self.image.clip_draw(150 - 30*self.frame, 120, self.w, self.h, self.x, self.y)
    #                     else: self.image.clip_draw(0, 120, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(0, 0, self.w, self.h, self.x, self.y)
    #             elif self.idle_dir == 1:
    #                 if self.jumping == 1:
    #                     if self.jumpCnt <= 6: self.image.clip_draw(180 + 30 * self.frame, 120, self.w, self.h, self.x, self.y)
    #                     else: self.image.clip_draw(180, 120, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(150, 0, self.w, self.h, self.x, self.y)
    #
    #         elif self.dir == 1:
    #             if self.jumping == 1:
    #                 if self.jumpCnt <= 6: self.image.clip_draw(180 + 30 * self.frame, 120, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(180, 120, self.w, self.h, self.x, self.y)
    #             else: self.image.clip_draw(180+30*self.frame, 60, self.w, self.h, self.x, self.y)
    #     # 슈퍼 마리오
    #     elif self.power == 1:
    #         # 왼쪽 뜀박질
    #         if self.dir == -1:
    #             if self.jumping == 1:
    #                 if self.jumpCnt <= 6: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
    #             else: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
    #         # 정지
    #         elif self.dir == 0:
    #             if self.idle_dir == -1:
    #                 if self.jumping == 1:
    #                     if self.jumpCnt <= 6: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
    #                     else: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(60, 600-60, self.w, self.h, self.x, self.y)
    #             elif self.idle_dir == 1:
    #                 if self.jumping == 1:
    #                     if self.jumpCnt <= 6: self.image.clip_draw(30 * self.frame, 600-120, self.w, self.h, self.x, self.y)
    #                     else: self.image.clip_draw(120, 600-120, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(0, 600-60, self.w, self.h, self.x, self.y)
    #         #오른쪽 뜀박질
    #         elif self.dir == 1:
    #             if self.jumping == 1:
    #                 if self.jumpCnt <= 6: self.image.clip_draw(30 * self.frame, 600-120, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(0, 600-120, self.w, self.h, self.x, self.y)
    #             else: self.image.clip_draw(30 * self.frame, 600-120, self.w, self.h, self.x, self.y)
    #
    #     # 짱쎈 마리오
    #     elif self.power == 2:
    #         # 왼쪽 뜀박질
    #         if self.dir == -1:
    #             if self.jumping == 1:
    #                 if self.jumpCnt <= 6:
    #                     self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
    #             else: self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
    #         # 정지
    #         elif self.dir == 0:
    #             if self.idle_dir == -1:
    #                 if self.jumping == 1:
    #                     if self.jumpCnt <= 6: self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
    #                     else: self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(60, 600 - 180, self.w, self.h, self.x, self.y)
    #             elif self.idle_dir == 1:
    #                 if self.jumping == 1:
    #                     if self.jumpCnt <= 6: self.image.clip_draw(30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
    #                     else: self.image.clip_draw(120, 600 - 240, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(0, 600 - 180, self.w, self.h, self.x, self.y)
    #         # 오른쪽 뜀박질
    #         elif self.dir == 1:
    #             if self.jumping == 1:
    #                 if self.jumpCnt <= 6: self.image.clip_draw(30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
    #                 else: self.image.clip_draw(0, 600 - 240, self.w, self.h, self.x, self.y)
    #             else: self.image.clip_draw(30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
    #
    #         # 파이어볼
    #         if self.fb.condition == 1:
    #             self.fb.draw()
    #
    #         pass

    # def update(self):
    #     if self.power != 0: self.h = 60
    #     else: self.h = 30
    #     # 점프
    #     if self.jumping == 1:
    #         if self.jumpCnt <= 10: self.y += 20
    #         self.jumpCnt += 1
    #         self.onAir = 1
    #     else: self.jumpCnt = 0
    #
    #     # 중력
    #     if self.onAir:
    #         self.y -= 10
    #
    #     # 달리기
    #     if self.running:
    #         if self.dir == 1:
    #             if self.speed < 10:
    #                 self.speed += 1
    #         elif self.dir == -1:
    #             if self.speed > -10:
    #                 self.speed -= 1
    #         else:
    #             if self.speed < 0:
    #                 self.speed += 2
    #             elif self.speed > 0:
    #                 self.speed -= 2
    #             if self.speed == -1 or self.speed == 1:
    #                 self.speed = 0
    #         self.x += self.speed
    #
    #     self.frame += 1
    #     self.frame = self.frame % 4
    #
    #     # 공격
    #     if self.attack:
    #         self.fb.condition = 1
    #         if self.idle_dir == 1:
    #             self.fb.x , self.fb.y = self.x + 30, self.y - 10
    #         elif self.idle_dir == -1:
    #             self.fb.x, self.fb.y = self.x - 30, self.y - 10
    #         self.fb.dir = self.idle_dir
    #         self.attack = 0
    #
    #     if self.fb.condition == 1:
    #         self.fb.update()

    pass


class FireBall:
    image = None
    def __init__(self):
        if FireBall.image == None:
            self.image = load_image('fireball.png')
        self.x, self.y = -100, -100
        self.dir = 0
        self.speed = 10
        self.bounce = 0
        self.condition = 0
        self.bounceTimer = 4
        self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame*20,0,20,20,self.x,self.y)

    def update(self):
        if self.bounce:
            self.y += 6
            self.bounceTimer -= 1
        else:
            self.y -= 6
            self.bounceTimer = 4

        if self.bounceTimer == 0:
            self.bounce = 0

        self.x += self.dir * self.speed
        self.frame = (self.frame + 1) % 4

        pass