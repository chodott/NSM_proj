from player import *
from object import *
from enemy import *
from pico2d import *
from random import *

def handle_events():
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and player.onAir == 0:
            player.jumping = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            player.running = 1
            player.dir -= 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            player.running = 1
            player.dir += 1
        elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
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
    global items
    global itemBlock
    airCheck = 1
    # 아이템 블록과 충돌
    for i in range(2):
        # 착지 블록 충돌
        if itemBlock[i].y + 12 > player.y - player.h / 2 > itemBlock[i].y and player.x + 15 > itemBlock[i].x - 15 and player.x - 15 < itemBlock[i].x + 15:
            player.jumping = 0
            player.jumpCnt = 0
            player.onAir = 0
            player.y = itemBlock[i].y + 15 + player.h / 2
            airCheck = 0
            break

        # 옆에서 진입 시 충돌
        elif itemBlock[i].x + 15 > player.x + player.speed > itemBlock[i].x - 15 and player.y+30 > itemBlock[i].y+15 and player.y-30 < itemBlock[i].y - 15:
            if player.speed > 0:
                player.x = itemBlock[i].x - 30
            elif player.speed < 0:
                player.x = itemBlock[i].x + 30
            player.speed = 0
            break


        # 점프로 블록 충돌
        elif player.jumping > 0 and itemBlock[i].y + 15 > player.y + player.h/2 > itemBlock[i].y - 15 and player.x + 15 > itemBlock[i].x - 15 and player.x - 15 < itemBlock[i].x + 15:
            itemBlock[i].broke = 1
            player.jumping = 0
            player.jumpCnt = 0
            items[i].x = itemBlock[i].x
            items[i].y = itemBlock[i].y+30
            if items[i].case == 0: item.direction = 1
            items[i].active = 1
            break

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
            player.onAir = 0
            airCheck = 0


        # 점프로 블록 충돌
        if player.jumping > 0 and block.y + 15 > player.y + player.h/2 > block.y - 15 and player.x + 15 > block.x - 15 and player.x - 15 < block.x + 15:
            if player.power == 0:
                block.broke = 0
                player.jumping = 0
                player.jumpCnt = 0
            elif player.power >= 1:
                block.broke = 1
                block.x, block.y = -10, -10
                player.jumping = 0
                player.jumpCnt = 0

    # 플랫폼 충돌
    for tile in grassTile1:
        if tile.y + 15 > player.y - player.h / 2 > tile.y and player.x + 15 > tile.x - 15 and player.x - 15 < tile.x + 15:
            player.jumping = 0
            player.jumpCnt = 0
            player.onAir = 0
            player.y = tile.y + 15 + player.h / 2
            airCheck = 0
            break

    if airCheck == 1: player.onAir = 1

    # 아이템 충돌
    for i in range(2):
        if player.x - 15 < items[i].x+15 and player.x + 15 > items[i].x - 15 and player.y + player.h/2 > items[i].y > player.y - player.h/2:
            items[i].x, items[i].y = -10, -10
            if items[i].case == 0:
                if player.power == 0: player.y += 30
                player.power = 1
            elif items[i].case == 1:
                if player.power == 0: player.y += 30
                player.power = 2

    #코인 충돌
    for coin in coins:
         if player.x - 15 < coin.x+15 and player.x + 15 > coin.x - 15 and player.y + player.h/2 > coin.y > player.y - player.h/2:
             coin.x, coin.y = -10, -10

    #아이템과 블록 충돌
    for i in range(2):
        # 착지 블록 충돌
        for j in range(2):
            if itemBlock[i].y + 12 > items[j].y - 15 > itemBlock[i].y and items[j].x + 15 > itemBlock[i].x - 15 and items[j].x - 15 < itemBlock[i].x + 15:
                items[j].y = itemBlock[i].y + 30
                break

        # 옆에서 진입 시 충돌
            elif itemBlock[i].x + 15 > items[j].x + 2 > itemBlock[i].x - 15 and items[j].y + 30 > itemBlock[i].y + 15 and items[j].y - 30 < itemBlock[i].y - 15:
                #미작성
                break
     # 노말 블록 충돌
    for block in normalBlock:
        for j in range(2):
            # 옆에서 진입 시 충돌
            if block.x + 15 > items[j].x + 2 > block.x - 15 and items[j].y + 30 > block.y + 15 and items[j].y - 30 < block.y - 15:
                #미작성
                break

            # 착지 블록 충돌
            if block.y + 12 > items[j].y - 15 > block.y and items[j].x + 15 > block.x - 15 and items[j].x - 15 < block.x + 15:
                items[j].y = block.y + 30

    #아이템과 발판 충돌
    for tile in grassTile1:
        for i in range(2):
            if tile.y + 15 > items[i].y - 15 > tile.y and items[i].x + 15 > tile.x - 15 and items[i].x - 15 < tile.x + 15:
                items[i].y = tile.y + 30
                break

# 초기화

havecoin = 0 #먹은 코인

open_canvas()

running = True
background = Background()
player = Player()
items = [Item() for i in range(2)]
itemBlock = [Block() for i in range(2)]
normalBlock = [Block() for i in range(3)]
grassTile1 = [Platform() for i in range(21)]
coins = [Coin() for i in range(4)]
goombas = [Goomba() for i in range(2)]
troopas = [Troopa() for i in range(2)]
goombas[0].x, goombas[0].y = 400, 500
troopas[0].x, troopas[0].y = 400,400
for ib in itemBlock:
    ib.x, ib.y = 100,180
    ib.case = 1
itemBlock[0].x, itemBlock[0].y = 200, 150; items[0].case = 0
itemBlock[1].x, itemBlock[1].y = 380, 250; items[1].case = 1
for i in range(3):
    normalBlock[i].x, normalBlock[i].y = 350 + i * 30, 150

for i in range(0,20+1):
    grassTile1[i].case = 0
    grassTile1[i].x, grassTile1[i].y = 30*i, 50

for i in range(0,4):
    coins[i].x, coins[i].y = i * 30 + 340, 80


while running:
    #게임 루프

    handle_events()
    for item in items:
        item.update()
    for coin in coins:
        coin.update()
    player.move()
    check_Collision()
    for ib in itemBlock:
        ib.update()
    for i in range(3):
        normalBlock[i].update()
    for goomba in goombas:
        goomba.update()
    for troopa in troopas:
        troopa.update()

    #그려.

    clear_canvas()
    background.draw()
    player.draw()
    for i in range(2):
        items[i].draw()
    for i in range(0,20+1):
        grassTile1[i].draw()
    for ib in itemBlock:
        ib.draw()
    for nb in normalBlock:
        nb.draw()
    for coin in coins:
        coin.draw()
    for goomba in goombas:
        goomba.draw()
    for troopa in troopas:
        troopa.draw()

    update_canvas()

    delay(0.05)
    pass


#소멸자
