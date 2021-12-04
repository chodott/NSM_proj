from player import *
from object import *
from enemy import *
from pico2d import *
from UI import *
import game_framework
import load_state
import over_state
import select_state

GRAVITY_SPEED_KMPH = 35.0
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)
gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
name = "MainState"

player = None
flag = None
koopa = None
arena = None
items = []
ibs = []
nbs = []
ebs = []
grassTile1 =[]
pipes = []
coins = []
goombas = []
troopas = []
boos = []
aircraft = None


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
    global ibs, nbs, ebs, grassTile1, arena
    global coins, items, flag, pipes, aircraft
    global goombas, troopas, boos, koopa
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
    nbs = [Block() for i in range(30)]
    ebs = [Block() for i in range(50)]
    game_world.add_objects(ibs, 1)
    game_world.add_objects(nbs, 1)
    game_world.add_objects(ebs, 1)
    #플랫폼
    grassTile1 = [Platform() for i in range(200)]
    game_world.add_objects(grassTile1,1)
    #토관
    pipes = [Pipe() for i in range(3)]
    game_world.add_objects(pipes,1)
    #코인
    coins = [Coin() for i in range(8)]
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

    #비행정
    if game_framework.cur_level == 3 or game_framework.cur_level==2:
        aircraft = Aircraft()
        game_world.add_object(aircraft, 1)

    #보스 방
    if game_framework.cur_level == 4:
        print("쿠파 등장")
        koopa = Koopa()
        arena = Arena()
        game_world.add_object(koopa,1)
        game_world.add_object(arena, 1)

    initialize()



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
    if game_framework.cur_level == 4:
        koopa.gravity = GRAVITY_SPEED_PPS * game_framework.frame_time
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
    for i in range(len(pipes)):
        for goomba in goombas:
            if collide(goomba, pipes[i]) and goomba.condition != -1:
                if goomba.y - 15 >= pipes[i].y + 10:
                    goomba.stop()
                elif pipes[i].x <= goomba.x-15<pipes[i].x+30:
                    goomba.dir = 1
                    goomba.x = pipes[i].x + 45
                elif pipes[i].x - 40 <= goomba.x + 15 < pipes[i].x:
                    goomba.dir = -1
                    goomba.x = pipes[i].x - 45

        for troopa in troopas:
            if collide(troopa, pipes[i]):
                troopa.stop()

        if collide(pipes[i], player):
            if player.y - player.h / 2 >= pipes[i].y + pipes[i].h/2 - 5:
                player.stop()
                if player.cur_state == SitState and pipes[i].active != 0:
                    player.x = pipes[i].x
                    player.y -= GRAVITY_SPEED_PPS * game_framework.frame_time
                    player.goalpipe = pipes[i+1].x
                    player.power = 3

                break
            elif pipes[i].x <= player.x - 15 < pipes[i].x + 30:
                player.meetwall()
                break
            elif pipes[i].x - 30 <= player.x + 15 < pipes[i].x:
                player.meetwall()
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

    #3단계
    if game_framework.cur_level == 3 or game_framework.cur_level == 2:
        if collide(aircraft, player):
            player.stop()
            if game_framework.cur_level == 3:
                aircraft.active = 1
            elif game_framework.cur_level == 2:
                player.y += aircraft.speed * 2
        for item in items:
            if collide(aircraft, item):
                item.stop()
        for goomba in goombas:
            if collide(aircraft, goomba):
                goomba.stop()
        for troopa in troopas:
            if collide(aircraft, troopa):
                troopa.stop()

    #4단계
    elif game_framework.cur_level == 4:
        if collide(arena,player):
            player.stop()
        if collide(arena,koopa):
            koopa.stop()
            # 플레이어 적 충돌
        if collide(player, koopa):
            if player.y - player.h / 2 >= koopa.y + 20 and koopa.condition == 0:
                player.attack()
                koopa.hit()
            else:
                player.hit()

    #블록 충돌 체크
    for ib in ibs:
        for item in items:
            if collide(item, ib) and item.active == 1:
                item.stop()
        for goomba in goombas:
            if collide(goomba, ib) and goomba.condition != -1:
                goomba. stop()
        for troopa in troopas:
            if collide(troopa, ib):
                troopa.stop()
        if collide(ib, player):
            if player.y - player.h / 2 >= ib.y + 10:
                player.stop()
                break
            elif player.y + player.h/2 <= ib.y - 10 and player.jumping == 1:
                if ib.broke != 1:
                    items[ibs.index(ib)].x = ib.x
                    items[ibs.index(ib)].y = ib.y + 2
                    items[ibs.index(ib)].hit()
                    ib.broke = 1;
                player.jumping = 0
                player.y -= JUMP_SPEED_PPS * game_framework.frame_time
                break
            elif ib.x + 10 <= player.x - 15 <ib.x + 15:
                player.meetwall()
                break
            elif ib.x - 15 <= player.x + 15 <ib.x - 10:
                player.meetwall()
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
            elif player.y + player.h/2 <= nb.y - 10 and player.jumping == 1:
                if player.power >= 1:
                    nb.broke = 1
                    nbs.remove(nb)
                    game_world.remove_object(nb)
                player.jumping = 0
                break
            elif nb.x + 10 <= player.x - 15 < nb.x + 15:
                player.meetwall()
            elif nb.x - 15 <= player.x + 15 < nb.x - 10:
                player.meetwall()

    for eb in ebs:
        if collide(eb, player):
            if player.y - player.h / 2 >= eb.y + 12:
                player.stop()
            elif eb.x + 14 <= player.x - 15 <eb.x + 15:
                player.meetwall()

            elif eb.x - 15 <= player.x + 15 <eb.x - 14:
                player.meetwall()



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
        #for fb in fireball:
        #    if collide(fb, troopa):
        #        troopa.death()
        #        print('충돋하네')


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
    if player.x >= 700 and game_framework.cur_level != 4:
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

    #1단계 초기화
    if game_framework.cur_level == 1:
        goombas[0].x, goombas[0].y = 510, 120
        goombas[1].x, goombas[1].y = 1000,120
        goombas[2].x, goombas[2].y = 1250,120
        goombas[3].x, goombas[3].y = 1280,120

        #아이템 블록 선언
        for ib in ibs: ib.case = 1
        ibs[0].x, ibs[0].y = 300, 150; ibs[1].x, ibs[1].y = 510, 270; ibs[2].x, ibs[2].y = 480, 150; ibs[3].x, ibs[3].y = 540, 150

        #노말 블록 선언
        nbs[0].x, nbs[0].y = 450, 150; nbs[1].x, nbs[1].y = 510,150; nbs[2].x, nbs[2].y = 570,150

        #엔딩 블록
        for eb in ebs:
            eb.case = 2
        cnt = 0
        for i in range(1,8):
            for j in range(9-i):
                ebs[cnt].x, ebs[cnt].y = 2310 - 30 * j, 45 + i * 30
                cnt += 1

        #플랫폼
        for i in range(0, 55):
            grassTile1[i].case = 0
            grassTile1[i].x, grassTile1[i].y = 15 +30 * i, 45
        for i in range(65, 100):
            grassTile1[i].case = 0
            grassTile1[i].x, grassTile1[i].y = 15 +30 * i, 45
        for i in range(100,155):
            grassTile1[i].case = 1
            grassTile1[i].x, grassTile1[i].y = 15 + 30 * (i-100), 15
        for i in range(165,200):
            grassTile1[i].case = 1
            grassTile1[i].x, grassTile1[i].y = 15 + 30 * (i-100), 15

        #토관
        pipes[0].x, pipes[0].y = 900, 90; pipes[0].active = 1
        pipes[1].x, pipes[1].y = 1200, 105; pipes[1].h = 90
        pipes[2].x, pipes[2].y = 1500, 120; pipes[2].h = 120; pipes[2].active = 1

        #코인
        for i in range(0, 4):
            coins[i].x, coins[i].y = i * 30 + 340, 80

    #2단계 초기화
    elif game_framework.cur_level == 2:

        #적
        goombas[0].x, goombas[0].y = 270, 120
        goombas[1].x, goombas[1].y = 300, 120

        # 플랫폼
        for i in range(0, 30):
            grassTile1[i].case = 0
            grassTile1[i].x, grassTile1[i].y = 15 + 30 * i, 45
        for i in range(65, 100):
            grassTile1[i].case = 0
            grassTile1[i].x, grassTile1[i].y = 15 + 30 * i, 45
        for i in range(100, 130):
            grassTile1[i].case = 1
            grassTile1[i].x, grassTile1[i].y = 15 + 30 * (i - 100), 15
        for i in range(165, 200):
            grassTile1[i].case = 1
            grassTile1[i].x, grassTile1[i].y = 15 + 30 * (i - 100), 15

        # 아이템 블록 선언
        for ib in ibs: ib.case = 1
        ibs[0].x, ibs[0].y = 300, 150
        ibs[1].x, ibs[1].y = 330, 150
        ibs[2].x, ibs[2].y = 360, 150
        ibs[3].x, ibs[3].y = 390, 150
        ibs[4].x, ibs[4].y = 420, 150

        #노말 블록
        nbs[0].x, nbs[0].y = 30 * 33, 200; nbs[1].x, nbs[1].y = 30 * 33, 230; nbs[2].x, nbs[2].y = 30*33, 260
        nbs[3].x, nbs[3].y = 30*34, 200; nbs[4].x, nbs[4].y = 30*35, 200; nbs[5].x, nbs[5].y = 30*36, 200
        nbs[6].x, nbs[6].y = 30*36, 230; nbs[7].x, nbs[7].y = 30*36, 260; nbs[8].x, nbs[8].y = 30*37, 260;
        nbs[9].x, nbs[9].y = 30*38, 260; nbs[10].x, nbs[10].y = 30*38, 230; nbs[11].x, nbs[11].y = 30*38, 200;
        nbs[12].x, nbs[12].y = 30*39, 200; nbs[13].x, nbs[13].y = 30*40, 200; nbs[14].x, nbs[14].y = 30*41, 200;
        nbs[15].x, nbs[15].y = 30*41, 230; nbs[16].x, nbs[16].y = 30*41, 260;

        #코인
        coins[0].x, coins[0].y = 30*34,230; coins[1].x, coins[1].y = 30*34,260; coins[2].x, coins[2].y = 30*35,260;
        coins[3].x, coins[3].y = 30 * 35, 230; coins[4].x, coins[4].y = 30*39, 230; coins[5].x, coins[5].y = 30*39, 260
        coins[6].x, coins[6].y = 30 * 40, 230; coins[7].x, coins[7].y = 30*40, 260

        #비행정
        aircraft.active = 2; aircraft.x, aircraft.y = 30 * 58, 200

        # 엔딩 블록
        for eb in ebs:
            eb.case = 2
        cnt = 0
        for i in range(1, 8):
            for j in range(9 - i):
                ebs[cnt].x, ebs[cnt].y = 2310 - 30 * j, 45 + i * 30
                cnt += 1
        for i in range(4,7):
            for j in range(i):
                ebs[cnt].x, ebs[cnt].y = 300 + 90*i, 45 + j * 30
                cnt += 1
        pass

    #3단계 초기화
    elif game_framework.cur_level == 3:

        #적
        troopas[0].x, troopas[0].y, troopas[0].condition = 30 * 30, 100, 2
        troopas[1].x, troopas[1].y, troopas[1].condition = 30 * 35, 150, 2

        #플랫폼
        for i in range(0, 30):
            grassTile1[i].case = 0
            grassTile1[i].x, grassTile1[i].y = 2115 + 30 * i, 45
        for i in range(100, 130):
            grassTile1[i].case = 1
            grassTile1[i].x, grassTile1[i].y = 2115 + 30 * (i - 100), 15

        #아이템 블록
        for ib in ibs: ib.case = 1
        ibs[0].x, ibs[0].y = 30 * 5, 200

        #노멀 블록
        nbs[0].x, nbs[0].y = 30 * 10, 165; nbs[1].x, nbs[1].y = 30 * 10, 195
        nbs[2].x, nbs[2].y = 30 * 13, 255; nbs[3].x, nbs[3].y = 30 * 13, 285;
        nbs[4].x, nbs[4].y = 30 * 16, 345; nbs[5].x, nbs[5].y = 30 * 16, 375;
        nbs[6].x, nbs[6].y = 30 * 19, 405; nbs[7].x, nbs[7].y = 30 * 19, 435;
        nbs[8].x, nbs[8].y = 30 * 22, 435; nbs[9].x, nbs[9].y = 30 * 22, 465;
        cnt = 10
        for i in range(12):
            nbs[cnt].x, nbs[cnt].y = 30 * 25, 150 + i * 30
            cnt += 1


        #비행정
        aircraft.x, aircraft.y, aircraft.w = 190, 100, 390

        # 엔딩 블록
        for eb in ebs:
            eb.case = 2
        cnt = 0
        for i in range(1, 8):
            for j in range(9 - i):
                ebs[cnt].x, ebs[cnt].y = 2325 - 30 * j, 45 + i * 30
                cnt += 1


