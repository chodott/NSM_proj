from player import *
from object import *

from pico2d import *
from random import *

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
                if player.jumping == 0 and player.onAir == 0:
                    player.jumping = 1; player.onAir == 1;
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
    global itemBlock
    global grassTile1
    global coins
    global item
    global itemBlock
    airCheck = 1

    # 아이템 블록과 충돌
    for block in itemBlock:
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
            player.y = block.y + 15 + player.h/2
            airCheck = 0

        # 점프로 블록 충돌
        if player.jumping > 0 and block.y + 15 > player.y + player.h/2 > block.y - 15 and player.x + 15 > block.x - 15 and player.x - 15 < block.x + 15:
            if player.power == 0:
                block.broke = 1
                player.jumping = 0
                player.jumpCnt = 0
                item.x = block.x
                item.y = block.y+30
                if item.case == 0: item.direction = randint(0,1)
                item.active = 1
            elif player.power == 1:
                block.broke = 2
                player.jumping = 0
                player.jumpCnt = 0

    # 노말 블록 충돌
    for block in normalBlock:
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
            player.y = block.y + 15 + player.h/2
            airCheck = 0

        # 점프로 블록 충돌
        if player.jumping > 0 and block.y + 15 > player.y + player.h/2 > block.y - 15 and player.x + 15 > block.x - 15 and player.x - 15 < block.x + 15:
            if player.power == 0:
                block.broke = 1
                player.jumping = 0
                player.jumpCnt = 0
            elif player.power == 1:
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
    for tile in grassTile1:
        if tile.y + 15 > player.y - player.h/2 > tile.y and player.x + 15 > tile.x - 15 and player.x - 15 < tile.x + 15:
            player.jumping = 0
            player.jumpCnt = 0
            player.y = tile.y + 15 + player.h/2
            airCheck = 0

    #코인 충돌
    for coin in coins:
         if player.x - 15 < coin.x+15 and player.x + 15 > coin.x - 15 and player.y + player.h/2 > coin.y > player.y - player.h/2:
             coin.x, coin.y = -10, -10



    # 공중 판정
    if airCheck: player.onAir = 1
    else: player.onAir = 0

# 초기화

havecoin = 0 #먹은 코인

open_canvas()

running = True
background = Background()
player = Player()
item = Item()
itemBlock = [Block() for i in range(2)]
normalBlock = [Block() for i in range(3)]
grassTile1 = [Platform() for i in range(21)]
coins = [Coin() for i in range(4)]
for ib in itemBlock:
    ib.x, ib.y = 100,180
    ib.case = 1
itemBlock[0].x, itemBlock[0].y = 200, 150
itemBlock[1].x, itemBlock[1].y = 380, 250

for i in range(0,20+1):
    grassTile1[i].case = 0
    grassTile1[i].x, grassTile1[i].y = 30*i, 50

for i in range(0,4):
    coins[i].x, coins[i].y = i * 30 + 340, 80


while running:
    #게임 루프

    handle_events()
    player.move()
    for ib in itemBlock:
        ib.update()
    for i in range(3):
        normalBlock[i].x, normalBlock[i].y = 350 + i*30, 150
        normalBlock[i].update()
    check_Collision()
    item.update()
    for coin in coins:
        coin.update()

    #그려.

    clear_canvas()
    background.draw()
    item.draw()
    player.draw()
    for i in range(0,20+1):
        grassTile1[i].draw()
    for ib in itemBlock:
        ib.draw()
    for nb in normalBlock:
        nb.draw()
    for coin in coins:
        coin.draw()

    update_canvas()

    delay(0.05)
    pass


#소멸자
