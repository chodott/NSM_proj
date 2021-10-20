from player import *

from pico2d import *
from random import *



class Background:
    def __init__(self):
        self.x, self.y = 400, 300
        self.image = load_image('bg-grassland.png')

    def draw(self):
        self.image.draw(self.x, self.y)

    pass


class Block:
    def __init__(self):
        self.image = load_image('block30.png')
        self.x, self.y = 200, 150
        self.frame = 0
        self.broke = 0
        self.case = 1

    def draw(self):
        if self.broke == 0:
            if self.case == 0: self.image.clip_draw(30*self.frame, 60, 30, 30, self.x, self.y)
            elif self.case == 1: self.image.clip_draw(30*self.frame, 30, 30, 30, self.x, self.y)
        else:
            self.image.clip_draw(0, 0, 30, 30, self.x, self.y)


    def update(self):
        self.frame = (self.frame+1) % 4

    pass


class Platform:
    def __init__(self):
        self.x, self.y = 50, 50
        self.image = load_image('tiles.png')
        self.case = 0

    def draw(self):
        if self.case == 0:
            self.image.clip_draw(30, 30, 30, 30, self.x, self.y)

    pass


class Item:
    def __init__(self,case):
        self.x, self.y = 100, 160
        self.image = load_image('Item.png')
        self.case = case
        self.direction = -1
        if self.case == 0: self.direction = randint(0, 2)

    def draw(self):
        if self.case == 0:
            self.image.clip_draw(0,30,30,30,self.x,self.y)
        elif self.case == 1:
            self.image.clip_draw(0,0,30,30,self.x,self.y)

    def move(self):
        if self.direction == 0:
            self.x -= 2
        elif self.direction == 1: self.x += 2


def handle_events():
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                player.running = 1
                player.dir -= 1
            elif event.key == SDLK_RIGHT:
                player.running = 1
                player.dir += 1
            elif event.key == SDLK_SPACE:
                if player.jumping == 0 and player.onAir == 0 : player.jumping = 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                player.dir += 1
                player.idle_dir = -1
            elif event.key == SDLK_RIGHT:
                player.dir -= 1
                player.idle_dir = 1

    pass


def check_Collision():
    global player
    global block
    global item
    global grassTile1

    player.onAir = 1 #항상 공중으로 초기화
    # 옆에서 진입 시 충돌
    if block.x + 15 > player.x + player.speed > block.x - 15 and player.y+30 > block.y+15 and player.y-30 < block.y - 15:
        if player.speed > 0:
            player.x = block.x - 30
        elif player.speed < 0:
            player.x = block.x + 30
        player.speed = 0

    # 착지 블록 충돌
    if block.y + 12 > player.y - player.h/2 > block.y and player.x + 15 > block.x - 15 and player.x - 15 < block.x + 15:
        player.jumping = 0
        player.jumpCnt = 0
        player.onAir = 0
        player.y = block.y + 15 + player.h/2

    # 점프로 블록 충돌
    if player.jumping > 0 and block.y + 15 > player.y + player.h/2 > block.y - 15 and player.x + 15 > block.x - 15 and player.x - 15 < block.x + 15:
        if player.power == 0:
            block.broke = 1
            player.jumping = 0
            player.jumpCnt = 0
        elif player.power == 2:
            block.broke = 2
            player.jumping = 0
            player.jumpCnt = 0

    # 아이템 충돌
    if player.x - 15 < item.x+15 and player.x + 15 > item.x - 15 and player.y + player.h/2 > item.y > player.y - player.h/2:
        item.x, item.y = -10, -10
        if item.case == 0:
            if player.power == 0: player.y += 30
            player.power = 1
        elif item.case == 1:
            if player.power == 0: player.y += 30
            player.power = 2

    # 플랫폼 충돌
    for i in range(0,10+1):
        if grassTile1[i].y + 15 > player.y - player.h/2 > grassTile1[i].y and player.x + 15 > grassTile1[i].x - 15 and player.x - 15 < grassTile1[i].x + 15:
            player.jumping = 0
            player.jumpCnt = 0
            player.onAir = 0
            player.y = grassTile1[i].y + 15 + player.h/2



# 초기화


open_canvas()

running = True
background = Background()
block = Block()
player = Player()
item = Item(1); item.x, item.y = 300,80
item0 = Item(0)
grassTile1 = [Platform() for i in range(11)]
for i in range(0,10+1):
    grassTile1[i].case = 0
    grassTile1[i].x, grassTile1[i].y = 30*i, 50


while running:
    #게임 루프

    handle_events()
    player.move()
    item.move()
    item0.move()
    check_Collision()
    block.update()

    #그려.

    clear_canvas()
    background.draw()
    item.draw()
    player.draw()
    block.draw()
    for i in range(0,10+1):
        grassTile1[i].draw()

    update_canvas()

    delay(0.05)
    pass


#소멸자
