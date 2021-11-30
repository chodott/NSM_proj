from player import *
from object import *
from enemy import *
from pico2d import *
from UI import *
import game_framework
import load_state
import over_state
import select_state

GRAVITY_SPEED_KMPH = 30.0
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)
gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
name = "MainState"

player = None
flag = None
items = []
ibs = []
nbs = []
grassTile1 =[]
pipes = []
coins = []
goombas = []
troopas = []
boos = []


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def enter():
    global background, player
    global ibs, nbs, grassTile1
    global coins, items, flag, pipes
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
    items = [Item() for i in range(5)]
    game_world.add_objects(items,1)
    #블럭
    ibs = [Block() for i in range(10)]
    nbs = [Block() for i in range(3)]
    game_world.add_objects(ibs, 1)
    game_world.add_objects(nbs, 1)
    #플랫폼
    grassTile1 = [Platform() for i in range(200)]
    game_world.add_objects(grassTile1,1)
    #토관
    pipes = [Pipe() for i in range(5)]
    game_world.add_objects(pipes,1)
    #코인
    coins = [Coin() for i in range(4)]
    game_world.add_objects(coins, 1)
    #적
    goombas = [Goomba() for i in range(4)]
    troopas = [Troopa() for i in range(2)]
    boos = [Boo() for i in range(2)]
    game_world.add_objects(goombas, 1)
    game_world.add_objects(troopas, 1)
    #game_world.add_objects(boos, 1)

    #깃발
    flag = Flag()
    game_world.add_object(flag,1)

    initialize()

    pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for boo in boos:
        boo.draw()
    ui.draw()
    update_canvas()

    pass


def exit():
    global boos
    global ui
    del(boos)
    del(ui)
    game_world.clear()
    pass

def fail():
    pass


def update():
    global Life
    global boos
    global ui
    global gravity
    if player.trans == 1: #변신 중 건들기 없기
        player.upgrade()
        return

    for game_object in game_world.all_objects():
        game_object.update(-player.gap)
    for boo in boos:
        boo.update(player.x, player.y, player.dir, player.idle_dir, -player.gap)
    ui.update()
    player.move = 1
    #중력 초기화
    player.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
    for item in items:
        item.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
    for goomba in goombas:
        goomba.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
    for troopa in troopas:
        troopa.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time

    #깃발 충돌
    if collide(flag,player):
        player.cur_state = EndState
        player.x = flag.x
        flag.condi = 1

    #토관 충돌
    for pipe in pipes:
        for goomba in goombas:
            if collide(goomba, pipe) and goomba.condition != -1:
                if goomba.y - 15 >= pipe.y + 10:
                    goomba.stop()
                elif pipe.x <= goomba.x-15<pipe.x+30:
                    goomba.dir = 1
                    goomba.x = pipe.x + 45
                elif pipe.x - 40 <= goomba.x + 15 < pipe.x:
                    goomba.dir = -1
                    goomba.x = pipe.x - 45

        for troopa in troopas:
            if collide(troopa, pipe):
                troopa.stop()
        if collide(pipe, player):
            if player.y - player.h / 2 >= pipe.y + 10:
                player.stop()
                break
            elif pipe.x <= player.x - 15 <pipe.x + 30:
                player.x = pipe.x + 45
                player.move = 0
                break
            elif pipe.x - 30 <= player.x + 15 <pipe.x:
                player.x = pipe.x - 45
                player.move = 0
                break


    #플랫폼 충돌 체크
    for grass in grassTile1:
        if collide(grass,player):
            player.stop()
        for goomba in goombas:
            if collide(grass, goomba) and goomba.condition != -1:
                goomba.stop()
        for troopa in troopas:
            if collide(grass, troopa):
                troopa.stop()
        for item in items:
            if collide(grass, item):
                item.stop()

    #블록 충돌 체크
    for ib in ibs:
        for item in items:
            if collide(item, ib) and item.active == 1:
                item.stop()
        for goomba in goombas:
            if collide(goomba, ib) and goomba.condition != -1:
                goomba.stop()
        for troopa in troopas:
            if collide(troopa, ib):
                troopa.stop()
        if collide(ib, player):
            if player.y - player.h / 2 >= ib.y + 10:
                player.stop()
                break
            elif ib.x <= player.x - 15 <ib.x + 15:
                player.x = ib.x + 30
                player.move = 0
                break
            elif ib.x - 15 <= player.x + 15 <ib.x:
                player.x = ib.x - 30
                player.move = 0
                break
            elif player.y + player.h/2 <= ib.y - 10 and player.jumping == 1:
                if ib.broke != 1:
                    items[ibs.index(ib)].x = ib.x
                    items[ibs.index(ib)].y = ib.y + 2
                    items[ibs.index(ib)].hit()
                    ib.broke = 1;
                player.jumping = 0
                break

    for nb in nbs:
        for item in items:
            if collide(item, nb):
                item.stop()
        for goomba in goombas:
            if collide(goomba, nb) and goomba.condition != -1:
                goomba.stop()
        for troopa in troopas:
            if collide(troopa, nb):
                troopa.stop()
        if collide(nb, player):
            if player.y - player.h / 2 >= nb.y + 10:
                player.stop()
                break
            elif nb.x <= player.x - 15 <nb.x + 15:
                player.x = nb.x + 30
                player.move = 0
                break
            elif nb.x - 15 <= player.x + 15 <nb.x:
                player.x = nb.x - 30
                player.move = 0
                break
            elif player.y + player.h/2 <= nb.y - 10 and player.jumping == 1:
                if player.power >= 1:
                    nb.broke = 1
                    nbs.remove(nb)
                    game_world.remove_object(nb)
                nb.broke = 1; player.jumping = 0
                break

    #플레이어 적 충돌
    for troopa in troopas:
        if collide(player, troopa):
            if player.y - player.h / 2 >= troopa.y + 10:
                player.attack()
                troopa.hit(player.x)
                break
            else:
                if troopa.speed == 0: troopa.hit(player.x); break
                else: player.hit(); break
        if troopa.condition == 0 and troopa.speed != 0:
            for goomba in goombas:
                if collide(troopa,goomba):
                    goomba.hit(1)
        #파이어볼 충돌
        # if collide(fireball, troopa):
        #     troopa.death()
        #     print('충돋하네')


    for goomba in goombas:
        if collide(player, goomba):
            if player.y - player.h/2 >= goomba.y + 10:
                player.attack()
                goomba.hit(0)
                break
            elif goomba.condition == 0:
                player.hit()
                break

    #죽음
    if ui.alarm <= 0: player.power = -1
    if player.y <= 10 and player.power != 4:
        player.power = -1
    if player.power == -1:
        UI.Life -= 1
        player.power = 4
        player.gap = 0
        player.speed = 0
        player.frame = 0
        player.hitTimer = time.time()
        if UI.Life == -1:
            player.cur_state = DeathState

        else:
            player.cur_state = DeathState

    if player.power == 4:
        if UI.Life == -1 and player.y <= -10:
            game_framework.change_state(over_state)
            game_world.remove_object(player)
        if UI.Life >= 0 and player.y <= -10:
            game_framework.change_state(load_state)
            game_world.remove_object(player)

    # for boo in boos:
    #     if collide(player, boo):
    #         player.hit()
    #         if player.power == -1:
    #             game_world.remove_object(player)

    #코인 충돌
    for coin in coins:
        if collide(player,coin):
            coins.remove(coin)
            game_world.remove_object(coin)
            ui.coin += 1

    #아이템 충돌
    for item in items:
        if collide(player,item):
            player.transTimer = time.time()
            player.upgrade(item.case)
            items.remove(item)
            game_world.remove_object(item)


    #종료 조건
    if player.x >= 700:
        game_framework.clear_level += 1
        game_framework.change_state(select_state)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            quit()
        else: player.handle_event(event)


def initialize():
    if game_framework.cur_level == 1:
        goombas[0].x, goombas[0].y = 510, 90
        goombas[1].x, goombas[1].y = 1000,90
        goombas[2].x, goombas[2].y = 1650,90
        goombas[3].x, goombas[3].y = 1680,90
        troopas[0].x, troopas[0].y = 400, 400
        boos[0].x, boos[0].y = 400, 400
        #아이템 블록 선언
        for ib in ibs:
            ib.case = 1
        ibs[0].x, ibs[0].y = 300, 150; ibs[1].x, ibs[1].y = 510, 270; ibs[2].x, ibs[2].y = 480, 150; ibs[3].x, ibs[3].y = 540, 150

        #노말 블록 선언
        for i in range(3):
            nbs[i].x, nbs[i].y = 350 + i * 30, 150
        nbs[0].x, nbs[0].y = 450, 150; nbs[1].x, nbs[1].y = 510,150; nbs[2].x, nbs[2].y = 570,150

        #플랫폼
        for i in range(0, 100):
            grassTile1[i].case = 0
            grassTile1[i].x, grassTile1[i].y = 15 +30 * i, 40
        for i in range(100,200):
            grassTile1[i].case = 1
            grassTile1[i].x, grassTile1[i].y = 15 + 30 * (i-100), 15

        #토관
        pipes[0].x, pipes[0].y = 900, 90
        pipes[1].x, pipes[1].y = 1200, 90
        pipes[2].x, pipes[2].y = 1500, 90
        #코인
        for i in range(0, 4):
            coins[i].x, coins[i].y = i * 30 + 340, 80

