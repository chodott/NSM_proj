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

    server.fbs = [FireBall() for i in range(10)]
    game_world.add_objects(server.fbs,1)

    if game_framework.cur_level != 4:
        #아이템
        server.items = [Item() for i in range(10)]
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
        if game_framework.cur_level == 3 or game_framework.cur_level == 2:
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
        server.goombas[0].x, server.goombas[0].y = 270, 120
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
        for ib in server.ibs: ib.case = 1
        server.ibs[0].x, server.ibs[0].y = 300, 150
        server.ibs[1].x, server.ibs[1].y = 330, 150
        server.ibs[2].x, server.ibs[2].y = 360, 150
        server.ibs[3].x, server.ibs[3].y = 390, 150
        server.ibs[4].x, server.ibs[4].y = 420, 150

        #노말 블록
        server.nbs[0].x, server.nbs[0].y = 30 * 33, 200; server.nbs[1].x, server.nbs[1].y = 30 * 33, 230; server.nbs[2].x, server.nbs[2].y = 30*33, 260
        server.nbs[3].x, server.nbs[3].y = 30*34, 200; server.nbs[4].x, server.nbs[4].y = 30*35, 200; server.nbs[5].x, server.nbs[5].y = 30*36, 200
        server.nbs[6].x, server.nbs[6].y = 30*36, 230; server.nbs[7].x, server.nbs[7].y = 30*36, 260; server.nbs[8].x, server.nbs[8].y = 30*37, 260;
        server.nbs[9].x, server.nbs[9].y = 30*38, 260; server.nbs[10].x, server.nbs[10].y = 30*38, 230; server.nbs[11].x, server.nbs[11].y = 30*38, 200;
        server.nbs[12].x, server.nbs[12].y = 30*39, 200; server.nbs[13].x, server.nbs[13].y = 30*40, 200; server.nbs[14].x, server.nbs[14].y = 30*41, 200;
        server.nbs[15].x, server.nbs[15].y = 30*41, 230; server.nbs[16].x, server.nbs[16].y = 30*41, 260;

        #코인
        server.coins[0].x, server.coins[0].y = 30*34,230; server.coins[1].x, server.coins[1].y = 30*34,260; server.coins[2].x, server.coins[2].y = 30*35,260;
        server.coins[3].x, server.coins[3].y = 30 * 35, 230; server.coins[4].x, server.coins[4].y = 30*39, 230; server.coins[5].x, server.coins[5].y = 30*39, 260
        server.coins[6].x, server.coins[6].y = 30 * 40, 230; server.coins[7].x, server.coins[7].y = 30*40, 260

        #비행정
        server.aircraft.active = 2; server.aircraft.x, server.aircraft.y = 30 * 58, 200

        # 엔딩 블록
        for eb in server.ebs:
            eb.case = 2
        cnt = 0
        for i in range(1, 8):
            for j in range(9 - i):
                server.ebs[cnt].x, server.ebs[cnt].y = 2310 - 30 * j, 45 + i * 30
                cnt += 1
        for i in range(4,7):
            for j in range(i):
                server.ebs[cnt].x, server.ebs[cnt].y = 300 + 90*i, 45 + j * 30
                cnt += 1
        pass

    #3단계 초기화
    elif game_framework.cur_level == 3:

        #적
        server.troopas[0].x, server.troopas[0].y, server.troopas[0].condition = 30 * 30, 100, 2
        server.troopas[1].x, server.troopas[1].y, server.troopas[1].condition = 30 * 35, 150, 2

        #플랫폼
        for i in range(0, 30):
            server.grassTile1[i].case = 0
            server.grassTile1[i].x, server.grassTile1[i].y = 2115 + 30 * i, 45
        for i in range(100, 130):
            server.grassTile1[i].case = 1
            server.grassTile1[i].x, server.grassTile1[i].y = 2115 + 30 * (i - 100), 15

        #아이템 블록
        for ib in server.ibs: ib.case = 1
        server.ibs[0].x, server.ibs[0].y = 30 * 5, 200

        #노멀 블록
        server.nbs[0].x, server.nbs[0].y = 30 * 10, 165; server.nbs[1].x, server.nbs[1].y = 30 * 10, 195
        server.nbs[2].x, server.nbs[2].y = 30 * 13, 255; server.nbs[3].x, server.nbs[3].y = 30 * 13, 285;
        server.nbs[4].x, server.nbs[4].y = 30 * 16, 345; server.nbs[5].x, server.nbs[5].y = 30 * 16, 375;
        server.nbs[6].x, server.nbs[6].y = 30 * 19, 405; server.nbs[7].x, server.nbs[7].y = 30 * 19, 435;
        server.nbs[8].x, server.nbs[8].y = 30 * 22, 435; server.nbs[9].x, server.nbs[9].y = 30 * 22, 465;
        cnt = 10
        for i in range(12):
            server.nbs[cnt].x, server.nbs[cnt].y = 30 * 25, 150 + i * 30
            cnt += 1


        #비행정
        server.aircraft.x, server.aircraft.y, server.aircraft.w = 190, 100, 390

        # 엔딩 블록
        for eb in server.ebs:
            eb.case = 2
        cnt = 0
        for i in range(1, 8):
            for j in range(9 - i):
                server.ebs[cnt].x, server.ebs[cnt].y = 2325 - 30 * j, 45 + i * 30
                cnt += 1


