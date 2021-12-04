from object import *
from enemy import *
from UI import *
import game_framework
import server

name = "MainState"

def enter():
    #UI
    server.ui = UI(name)
    game_world.add_object(server.ui, 1)
    #배경
    server.background = Background()
    game_world.add_object(server.background, 0)
    #마리오
    server.player = Player()
    game_world.add_object(server.player, 1)

    if game_framework.cur_level != 4:
        #아이템
        server.items = [Item() for i in range(5)]
        game_world.add_objects(server.items,1)
        #블럭
        server.ibs = [Block() for i in range(10)]
        server.nbs = [Block() for i in range(30)]
        server.ebs = [Block() for i in range(50)]
        game_world.add_objects(server.ibs, 1)
        game_world.add_objects(server.nbs, 1)
        game_world.add_objects(server.ebs, 1)
        #플랫폼
        server.grassTile1 = [Platform() for i in range(200)]
        game_world.add_objects(server.grassTile1,1)
        #토관
        server.pipes = [Pipe() for i in range(3)]
        game_world.add_objects(server.pipes,1)
        #코인
        server.coins = [Coin() for i in range(8)]
        game_world.add_objects(server.coins, 1)
        #적
        server.goombas = [Goomba() for i in range(4)]
        server.troopas = [Troopa() for i in range(2)]
        game_world.add_objects(server.goombas, 1)
        game_world.add_objects(server.troopas, 1)

        #깃발
        server.flag = Flag()
        game_world.add_object(server.flag,1)

        #비행정
        if game_framework.cur_level == 4 or game_framework.cur_level == 2:
            server.aircraft = Aircraft()
            game_world.add_object(server.aircraft, 1)
    #보스 방
    else:
        server.koopa = Koopa()
        server.arena = Arena()
        game_world.add_object(server.koopa,1)
        game_world.add_object(server.arena, 1)

    initialize()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

    pass


def exit():
    game_world.clear()
    pass


def fail():
    pass


def update():

    if server.player.trans == 1: #변신 중 건들기 없기
        server.player.upgrade()
        return

    for game_object in game_world.all_objects():
        game_object.update()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            quit()
        else:
            server.player.handle_event(event)


def initialize():

    #1단계 초기화
    if game_framework.cur_level == 1:
        server.goombas[0].x, server.goombas[0].y = 510, 115
        server.goombas[1].x, server.goombas[1].y = 1000,115
        server.goombas[2].x, server.goombas[2].y = 1250,115
        server.goombas[3].x, server.goombas[3].y = 1280,115

        #아이템 블록 선언
        for ib in server.ibs: ib.case = 1
        server.ibs[0].x, server.ibs[0].y = 300, 150; server.ibs[1].x, server.ibs[1].y = 510, 270; server.ibs[2].x, server.ibs[2].y = 480, 150; server.ibs[3].x, server.ibs[3].y = 540, 150

        #노말 블록 선언
        server.nbs[0].x, server.nbs[0].y = 450, 150; server.nbs[1].x, server.nbs[1].y = 510,150; server.nbs[2].x, server.nbs[2].y = 570,150

        #엔딩 블록
        for eb in server.ebs:
            eb.case = 2
        cnt = 0
        for i in range(1,8):
            for j in range(9-i):
                server.ebs[cnt].x, server.ebs[cnt].y = 2310 - 30 * j, 45 + i * 30
                cnt += 1

        #플랫폼
        for i in range(0, 55):
            server.grassTile1[i].case = 0
            server.grassTile1[i].x, server.grassTile1[i].y = 15 +30 * i, 45
        for i in range(65, 100):
            server.grassTile1[i].case = 0
            server.grassTile1[i].x, server.grassTile1[i].y = 15 +30 * i, 45
        for i in range(100,155):
            server.grassTile1[i].case = 1
            server.grassTile1[i].x, server.grassTile1[i].y = 15 + 30 * (i-100), 15
        for i in range(165,200):
            server.grassTile1[i].case = 1
            server.grassTile1[i].x, server.grassTile1[i].y = 15 + 30 * (i-100), 15

        #토관
        server.pipes[0].x, server.pipes[0].y = 900, 90; server.pipes[0].active = 1
        server.pipes[1].x, server.pipes[1].y = 1200, 105; server.pipes[1].h = 90
        server.pipes[2].x, server.pipes[2].y = 1500, 120; server.pipes[2].h = 120; server.pipes[2].active = 1

        #코인
        for i in range(0, 4):
            server.coins[i].x, server.coins[i].y = i * 30 + 340, 80

    #2단계 초기화
    elif game_framework.cur_level == 2:

        #적
        server.goombas[0].x, server.oombas[0].y = 270, 120
        server.goombas[1].x, server.goombas[1].y = 300, 120

        # 플랫폼
        for i in range(0, 30):
            server.grassTile1[i].case = 0
            server.grassTile1[i].x, server.grassTile1[i].y = 15 + 30 * i, 45
        for i in range(65, 100):
            server.grassTile1[i].case = 0
            server.grassTile1[i].x, server.grassTile1[i].y = 15 + 30 * i, 45
        for i in range(100, 130):
            server.grassTile1[i].case = 1
            server.grassTile1[i].x, server.grassTile1[i].y = 15 + 30 * (i - 100), 15
        for i in range(165, 200):
            server.grassTile1[i].case = 1
            server.grassTile1[i].x, server.grassTile1[i].y = 15 + 30 * (i - 100), 15

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


