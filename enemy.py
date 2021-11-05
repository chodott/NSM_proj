from pico2d import *
# enemy 중력 + 캐릭터 상호작용 필요
class Goomba:
    def __init__(self):
        self.image = load_image('goomba.png')
        self.x, self.y = -10,-10
        self.width, self.height = 30,30
        self.dir = -1
        self.speed = -3
        self.frame = 1
        self.condition = 0 #1: 죽음 0: 생존
        self.deathcnt = 0

    def draw(self):
        if self.condition: self.image.clip_draw(0,0,30,30,self.x,self.y)
        else: self.image.clip_draw(0,240-self.frame*30,30,30,self.x,self.y)

    def update(self):
        self.y -= 10
        if self.condition:
            self.deathcnt += 1
            if self.deatcnt == 3:
                self.x, self.y = -10, -10
        else:
            self.frame = (self.frame + 1) % 8
            self.x += self.speed


class Troopa:
    def __init__(self):
        self.image = load_image('troopa.png')
        self.x, self.y = -10, -10
        self.width, self.height = 30, 50
        self.dir = -1
        self.speed = -2
        self.frame = 0
        self.condition = 1 #0 : 등껍질 1: 정상 2: 날개
        self.boundary = 400

    def draw(self):
        #상태에 맞는 그리기 필요
        if self.condition==0:
            self.image.clip_draw(30,0,self.width,self.height, self.x, self.y);
        elif self.condition == 1:
            self.image.clip_draw(0,800 - 50 - self.frame * 50,self.width,self.height, self.x, self.y);
        elif self.condition == 2:
            self.image.clip_draw(0, 800 - 50 - self.frame * 50, self.width, self.height, self.x, self.y);


    def update(self):
        self.y -= 5
        if self.condition == 0:
            self.x += self.speed
            self.height = 30
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


class Ghost:
    def __init__(self):
        self.image = load_image('ghost.png')
        self.x, self.y = -10, -10
        self.width, self.height = 30, 30
        self.dir = -1
        self.speed = 2
        self.frame = 0
        self.condition = 1  # 0 : 정지 1: 추격
        self.boundary = 400

    def draw(self):
        #상태에 맞는 그리기 필요
        if self.condition == 0 and self.dir > 0:
            self.image.clip_draw(0, 800 - 50 - self.frame * 50, self.width, self.height, self.x, self.y);

        elif self.condition == 0 and self.dir < 0:
            self.image.clip_draw(0, 800 - 50 - self.frame * 50, self.width, self.height, self.x, self.y);

        elif self.condition == 1 and self.dir > 0:
            self.image.clip_draw(0, 800 - 50 - self.frame * 50, self.width, self.height, self.x, self.y);

        elif self.condition == 1 and self.dir < 0:
            self.image.clip_draw(0, 800 - 50 - self.frame * 50, self.width, self.height, self.x, self.y);

    def update(self):
        #플레이어와 부끄의 방향이 같을 때 부끄 정지
        self.condition = 0
        self.frame = 0

        #방향이 다를 때 부끄 캐릭터 방향으로
        self.condition = 1
        self.frame = 1
