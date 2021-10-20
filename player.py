from pico2d import *

class Player:
    def __init__(self):
        self.image = load_image('mini30.png')
        self.x, self.y = (50,200)
        self.w, self.h = 30, 30
        self.power = 0
        self.speed = 0
        self.frame = 0
        self.idle_dir = 1
        self.dir = 0  # -1 left +1 right
        self.jumping = 0
        self.running = 0
        self.runCnt = 0
        self.jumpCnt = 0
        self.onAir = 1

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
        self.frame = self.frame % 3
    pass

