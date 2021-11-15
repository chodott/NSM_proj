from pico2d import *
import game_framework
import start_state
from UI import *

name = "OverState"


def enter():
    global image
    image = load_image('gameover.png')
    pass


def exit():
    global image
    del(image)
    pass


def update():
    pass


def draw():
    global image
    clear_canvas()
    image.draw(400,300)
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            UI.Life = 3
            game_framework.change_state(start_state)

    pass
