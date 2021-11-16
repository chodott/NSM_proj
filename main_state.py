from player import *
from object import *
from enemy import *
from pico2d import *
from random import *
from UI import *
import game_framework
import load_state
import over_state


name = "MainState"


def enter():
    global background, player
    global itemBlock, normalBlock, grassTile1
    global coins, items
    global goombas, troopas, boos
    global ui
    #UI
    ui = UI(name)
    #배경
    background = Background()
    game_world.add_object(background, 0)
    #마리오
    player = Player()
    game_world.add_object(player, 1)
    #아이템
    items = [Item() for i in range(2)]
    itemBlock = [Block() for i in range(2)]
    normalBlock = [Block() for i in range(3)]
    grassTile1 = [Platform() for i in range(21)]
    coins = [Coin() for i in range(4)]
    goombas = [Goomba() for i in range(2)]
    troopas = [Troopa() for i in range(2)]
    boos = [Boo() for i in range(2)]

    initialize()

    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for i in range(2):
        items[i].draw()
    for i in range(0, 20 + 1):
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
    for boo in boos:
        boo.draw()
    ui.draw()
    update_canvas()

    pass


def exit():
    global background, player
    global itemBlock, normalBlock, grassTile1
    global coins, items
    global goombas, troopas, boos
    global ui
    del(background); del(player)
    del(itemBlock); del(normalBlock); del(grassTile1)
    del(coins); del(items)
    del(goombas); del(troopas); del(boos)
    del(ui)
    game_world.clear()
    pass


def update():
    global Life
    global player
    #global ui
    for game_object in game_world.all_objects():
        game_object.update()
    check_Collision()
    for item in items:
        item.update()
    for coin in coins:
        coin.update()
    for ib in itemBlock:
        ib.update()
    for i in range(3):
        normalBlock[i].update()
    for goomba in goombas:
        goomba.update()
    for troopa in troopas:
        troopa.update()
    for boo in boos:
        boo.update(player.x,player.y,player.dir,player.idle_dir)
    ui.update()
    #if player.power == -1 or ui.alarm == 0:
    if player.power == -1:
        #데스 애니메이션 출력
        UI.Life -= 1
        if UI.Life == -1:
            game_framework.change_state(over_state)
        else: game_framework.change_state(load_state)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            quit()
        else: player.handle_event(event)
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_UP and player.onAir == 0:
        #     player.jumping = 1
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
        #     player.running = 1
        #     player.dir -= 1
        #     player.idle_dir = -1
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
        #     player.running = 1
        #     player.dir += 1
        #     player.idle_dir = 1
        # elif event.type == SDL_KEYUP and event.key == SDLK_LEFT:
        #     player.dir += 1
        # elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
        #     player.dir -= 1
        # elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and player.power == 2:
        #     player.attack = 1



def check_Collision():
    global player
    global itemBlock
    global grassTile1
    global coins
    global items
    global itemBlock
    global goombas
    global troopas
    global boos
    global ui
    airCheck = 1
    # 아이템 블록과 충돌
    for ib in itemBlock:
        # 착지 블록 충돌
        if ib.y + 12 > player.y - player.h / 2 > ib.y and player.x + 15 > ib.x - 15 and player.x - 15 < ib.x + 15:
            player.jumping = 0
            player.jumpCnt = 0
            player.onAir = 0
            player.y = ib.y + 15 + player.h / 2
            airCheck = 0
            break

        # 옆에서 진입 시 충돌
        elif ib.x + 15 > player.x + player.speed > ib.x - 15 and player.y+30 > ib.y+15 and player.y-30 < ib.y - 15:
            if player.speed > 0:
                player.x = ib.x - 30
            elif player.speed < 0:
                player.x = ib.x + 30
            player.speed = 0
            break


        # 점프로 블록 충돌
        elif player.jumping > 0 and ib.y + 15 > player.y + player.h/2 > ib.y - 15 and player.x + 15 > ib.x - 15 and player.x - 15 < ib.x + 15:
            ib.broke = 1
            player.jumping = 0
            player.jumpCnt = 0
            item.x = ib.x
            item.y = ib.y+30
            if item.case == 0: item.direction = 1
            item.active = 1
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

        #파이어볼, 플랫폼
        if tile.y + 15 > player.fb.y - 10 > tile.y and player.fb.x + 10 > tile.x - 15 and player.fb.x - 10 < tile.x + 15:
            player.fb.bounce = 1

    if airCheck == 1: player.onAir = 1

    # 아이템 충돌
    for item in items:
        if player.x - 15 < item.x+15 and player.x + 15 > item.x - 15 and player.y + player.h/2 > item.y > player.y - player.h/2:
            item.x, item.y = -10, -10
            if item.case == 0:
                if player.power == 0: player.y += 30
                player.power = 1
            elif item.case == 1:
                if player.power == 0: player.y += 30
                player.power = 2

    #코인 충돌
    for coin in coins:
         if player.x - 15 < coin.x+15 and player.x + 15 > coin.x - 15 and player.y + player.h/2 > coin.y > player.y - player.h/2:
            coin.x, coin.y = -10, -10
            ui.coin += 1

    #적, 아이템, 아이템 블록 충돌
    for ib in itemBlock:
        # 착지 블록 충돌
        for item in items:
            if ib.y + 12 > item.y - 15 > ib.y and item.x + 15 > ib.x - 15 and item.x - 15 < ib.x + 15:
                item.y = ib.y + 30
                break

        # 옆에서 진입 시 충돌
            elif ib.x + 15 > item.x + 2 > ib.x - 15 and item.y + 30 > ib.y + 15 and item.y - 30 < ib.y - 15:
                #미작성
                break

    #적, 아이템, 노말 블록 충돌
    for block in normalBlock:
        for j in range(2):
            # 옆에서 진입 시 충돌
            if block.x + 15 > items[j].x + 2 > block.x - 15 and items[j].y + 30 > block.y + 15 and items[j].y - 30 < block.y - 15:
                #미작성
                break

            # 착지 블록 충돌
            if block.y + 12 > items[j].y - 15 > block.y and items[j].x + 15 > block.x - 15 and items[j].x - 15 < block.x + 15:
                items[j].y = block.y + 30

    #적, 아이템, 발판 충돌
    for tile in grassTile1:
        for i in range(2):
            if tile.y + 15 > items[i].y - 15 > tile.y and items[i].x + 15 > tile.x - 15 and items[i].x - 15 < tile.x + 15:
                items[i].y = tile.y + 30
                break
        for goomba in goombas:
            if tile.y + 15 > goomba.y - goomba.h/2 > tile.y and goomba.x + goomba.w/2 > tile.x - 15 and goomba.x - goomba.w/2 < tile.x + 15 and goomba.condition != -1:
                goomba.y = tile.y + 15 + goomba.h/2
                break
        for troopa in troopas:
            if tile.y + 15 > troopa.y - troopa.h/2 > tile.y and troopa.x + troopa.w/2 > tile.x - 15 and troopa.x - troopa.w/2 < tile.x + 15:
                troopa.y = tile.y + 15 + troopa.h/2
                break

    # #플레이어, 적 충돌
    # for goomba in goombas:
    #
    #     #점프 충돌
    #     if goomba.y + goomba.h/2 > player.y - player.h/2 - 10 > goomba.y \
    #             and (goomba.x - goomba.w/2 < player.x - player.w/2 < goomba.x + goomba.w/2 or goomba.x - goomba.w/2 < player.x + player.w/2 < goomba.x + goomba.h/2)\
    #             and goomba.condition == 0:
    #         goomba.death(0)
    #
    #
    #     #정면 충돌
    #     elif (goomba.x - goomba.w/2 < player.x + player.w/2 < goomba.x + goomba.w/2 or goomba.x - goomba.w/2 < player.x - player.w/2 < goomba.x + goomba.w/2)\
    #             and player.y + player.h/2 > goomba.y + goomba.h/2 > player.y - player.h/2 and goomba.condition == 0:
    #         if player.hitTimer == 0:
    #             player.power -= 1
    #             player.hitTimer = 400
    #
    #     #파이어볼 충돌
    #     elif (goomba.y - goomba.h/2 < player.fb.y - 10 < goomba.y + goomba.h/2 or goomba.y - goomba.h/2 < player.fb.y + 10 < goomba.y + goomba.h/2)\
    #             and (goomba.x - goomba.w/2 < player.fb.x + 10 < goomba.x+goomba.w/2 or goomba.x - goomba.w/2 < player.fb.x - 10 < goomba.x + goomba.w/2):
    #         goomba.death(1)
    #
    # for troopa in troopas:
    #
    #     # 점프 충돌
    #     if troopa.y + troopa.h / 2 > player.y - player.h / 2 - 10 > troopa.y \
    #             and (troopa.x - troopa.w / 2 < player.x - player.w / 2 < troopa.x + troopa.w / 2 or troopa.x - troopa.w / 2 < player.x + player.w / 2 < troopa.x + troopa.h / 2):
    #         if troopa.condition > 0: troopa.condition -= 1
    #         if troopa.condition == 0:
    #             if troopa.speed == 0:
    #                 if troopa.x < player.x: troopa.speed = -5
    #                 else: troopa.speed = 5
    #             else: troopa.speed = 0
    #
    #     # 정면 충돌
    #     if (troopa.x - troopa.w / 2 < player.x + player.w / 2 < troopa.x + troopa.w / 2 or troopa.x - troopa.w / 2 < player.x - player.w / 2 < troopa.x + troopa.w / 2) \
    #             and player.y + player.h / 2 > troopa.y + troopa.h / 2 > player.y - player.h / 2:
    #         if troopa.speed == 0:
    #             if troopa.x < player.x:
    #                 troopa.speed = -5
    #             else:
    #                 troopa.speed = 5
    #         else:
    #             if player.hitTimer == 0:
    #                 player.power -= 1
    #                 player.hitTimer = 400
    #
    #     #파이어볼 충돌
    #     elif (troopa.y - troopa.h/2 < player.fb.y - 10 < troopa.y + troopa.h/2 or troopa.y - troopa.h/2 < player.fb.y + 10 < troopa.y + troopa.h/2)\
    #             and (troopa.x - troopa.w/2 < player.fb.x + 10 < troopa.x+troopa.w/2 or troopa.x - troopa.w/2 < player.fb.x - 10 < troopa.x + troopa.w/2):
    #         troopa.condition = -1
    #
    #
    # for boo in boos:
    #
    #     # 점프 충돌
    #     if boo.y + boo.h / 2 > player.y - player.h / 2 - 10 > boo.y \
    #             and (boo.x - boo.w / 2 < player.x - player.w / 2 < boo.x + boo.w / 2 or boo.x - boo.w / 2 < player.x + player.w / 2 < boo.x + boo.h / 2) \
    #             and boo.condition > 0:
    #         boo.condition -= 1
    #         if boo.condition == 0: boo.speed = 0
    #
    #     # 정면 충돌
    #     if (boo.x - boo.w / 2 < player.x + player.w / 2 < boo.x + boo.w / 2 or boo.x - boo.w / 2 < player.x - player.w / 2 < boo.x + boo.w / 2) \
    #             and player.y + player.h / 2 > boo.y + boo.h / 2 > player.y - player.h / 2:
    #         if player.hitTimer == 0:
    #             player.power -= 1
    #             player.hitTimer = 400



def initialize():
    goombas[0].x, goombas[0].y = 400, 500
    troopas[0].x, troopas[0].y = 400, 400
    boos[0].x, boos[0].y = 400, 400
    for ib in itemBlock:
        ib.x, ib.y = 100, 180
        ib.case = 1
    itemBlock[0].x, itemBlock[0].y = 200, 150;
    items[0].case = 0
    itemBlock[1].x, itemBlock[1].y = 380, 250;
    items[1].case = 1
    for i in range(3):
        normalBlock[i].x, normalBlock[i].y = 350 + i * 30, 150

    for i in range(0, 20 + 1):
        grassTile1[i].case = 0
        grassTile1[i].x, grassTile1[i].y = 30 * i, 50

    for i in range(0, 4):
        coins[i].x, coins[i].y = i * 30 + 340, 80


# 초기화

#open_canvas()


# while running:
#
#     game_loop()
#
#     game_draw()
#
#
#     delay(0.05)
#     pass


#소멸자
