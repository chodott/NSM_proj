from pico2d import *
import game_framework
import main_state
from select_state import *
from time import *
from UI import *

name = "LoadState"


def enter():
    global image
    global ui
    global loadTimer
    image = load_image('load.png')
    ui = UI(name)
    loadTimer = time.time()
    pass


def exit():
    global image
    del(image)
    pass


def update():
    global loadTimer
    global ui
    ui.update()
    if time.time() - loadTimer > 1:
        game_framework.change_state(main_state)
    pass


def draw():
    global image
    global ui
    clear_canvas()
    image.draw(400,300)
    ui.draw()
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()

    pass

