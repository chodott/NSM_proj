# 파이어볼 곡선이동, 충돌처리, 탄환추가, 파워가 변해도 유지 추가 필요


from pico2d import *


class Player:
    def __init__(self):
        self.image = load_image('mini30.png')
        self.x, self.y = (50,200)
        self.w, self.h = 30, 30
        self.power = 2
        self.speed = 0
        self.frame = 0
        self.idle_dir = 1
        self.dir = 0  # -1 left +1 right
        self.jumping = 0
        self.running = 0
        self.runCnt = 0
        self.jumpCnt = 0
        self.onAir = 1
        self.hitTimer = 0
        self.attack = 0
        self.fb = FireBall()

    def draw(self):
        # 꼬마 마리오
        if self.power == 0:
            if self.dir == -1:
                if self.jumping == 1:
                    if self.jumpCnt <= 6: self.image.clip_draw(150 - 30*self.frame, 120, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(0, 120, self.w, self.h, self.x, self.y)

                else: self.image.clip_draw(30*self.frame, 60, self.w, self.h, self.x, self.y)
            elif self.dir == 0:
                if self.idle_dir == -1:
                    if self.jumping == 1:
                        if self.jumpCnt <= 6: self.image.clip_draw(150 - 30*self.frame, 120, self.w, self.h, self.x, self.y)
                        else: self.image.clip_draw(0, 120, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(0, 0, self.w, self.h, self.x, self.y)
                elif self.idle_dir == 1:
                    if self.jumping == 1:
                        if self.jumpCnt <= 6: self.image.clip_draw(180 + 30 * self.frame, 120, self.w, self.h, self.x, self.y)
                        else: self.image.clip_draw(180, 120, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(150, 0, self.w, self.h, self.x, self.y)

            elif self.dir == 1:
                if self.jumping == 1:
                    if self.jumpCnt <= 6: self.image.clip_draw(180 + 30 * self.frame, 120, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(180, 120, self.w, self.h, self.x, self.y)
                else: self.image.clip_draw(180+30*self.frame, 60, self.w, self.h, self.x, self.y)
        # 슈퍼 마리오
        elif self.power == 1:
            # 왼쪽 뜀박질
            if self.dir == -1:
                if self.jumping == 1:
                    if self.jumpCnt <= 6: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
                else: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
            # 정지
            elif self.dir == 0:
                if self.idle_dir == -1:
                    if self.jumping == 1:
                        if self.jumpCnt <= 6: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
                        else: self.image.clip_draw(270 - 30*self.frame, 600-120, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(60, 600-60, self.w, self.h, self.x, self.y)
                elif self.idle_dir == 1:
                    if self.jumping == 1:
                        if self.jumpCnt <= 6: self.image.clip_draw(30 * self.frame, 600-120, self.w, self.h, self.x, self.y)
                        else: self.image.clip_draw(120, 600-120, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(0, 600-60, self.w, self.h, self.x, self.y)
            #오른쪽 뜀박질
            elif self.dir == 1:
                if self.jumping == 1:
                    if self.jumpCnt <= 6: self.image.clip_draw(30 * self.frame, 600-120, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(0, 600-120, self.w, self.h, self.x, self.y)
                else: self.image.clip_draw(30 * self.frame, 600-120, self.w, self.h, self.x, self.y)

        # 짱쎈 마리오
        elif self.power == 2:
            # 왼쪽 뜀박질
            if self.dir == -1:
                if self.jumping == 1:
                    if self.jumpCnt <= 6:
                        self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
                else: self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
            # 정지
            elif self.dir == 0:
                if self.idle_dir == -1:
                    if self.jumping == 1:
                        if self.jumpCnt <= 6: self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
                        else: self.image.clip_draw(270 - 30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(60, 600 - 180, self.w, self.h, self.x, self.y)
                elif self.idle_dir == 1:
                    if self.jumping == 1:
                        if self.jumpCnt <= 6: self.image.clip_draw(30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
                        else: self.image.clip_draw(120, 600 - 240, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(0, 600 - 180, self.w, self.h, self.x, self.y)
            # 오른쪽 뜀박질
            elif self.dir == 1:
                if self.jumping == 1:
                    if self.jumpCnt <= 6: self.image.clip_draw(30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)
                    else: self.image.clip_draw(0, 600 - 240, self.w, self.h, self.x, self.y)
                else: self.image.clip_draw(30 * self.frame, 600 - 240, self.w, self.h, self.x, self.y)

            # 파이어볼
            if self.fb.condition == 1:
                self.fb.draw()

            pass

    def move(self):
        if self.power != 0: self.h = 60
        else: self.h = 30
        # 점프
        if self.jumping == 1:
            if self.jumpCnt <= 10: self.y += 20
            self.jumpCnt += 1
            self.onAir = 1
        else: self.jumpCnt = 0

        # 중력
        if self.onAir:
            self.y -= 10

        # 달리기
        if self.running:
            if self.dir == 1:
                if self.speed < 10:
                    self.speed += 1
            elif self.dir == -1:
                if self.speed > -10:
                    self.speed -= 1
            else:
                if self.speed < 0:
                    self.speed += 2
                elif self.speed > 0:
                    self.speed -= 2
                if self.speed == -1 or self.speed == 1:
                    self.speed = 0
            self.x += self.speed

        self.frame += 1
        self.frame = self.frame % 4

        # 공격
        if self.attack:
            self.fb.condition = 1
            if self.idle_dir == 1:
                self.fb.x , self.fb.y = self.x + 30, self.y - 10
            elif self.idle_dir == -1:
                self.fb.x, self.fb.y = self.x - 30, self.y - 10
            self.fb.dir = self.idle_dir
            self.attack = 0

        if self.fb.condition == 1:
            self.fb.update()

    pass


class FireBall:
    def __init__(self):
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