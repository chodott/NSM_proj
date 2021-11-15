from pico2d import *
import game_framework
import load_state
from UI import *

name = "SelectState"

pos = [110, 205, 300, 485, 670]

class SELECT:
    def __init__(self):
        self.pos = 0
        self.x = pos[self.pos]
        self.y = 310
        self.image = load_image('stagemario.png')
        self.frame = 0

    def draw(self):
        if self.frame == 0:
            self.image.clip_draw(0,0,30,50,self.x,self.y)
        elif self.frame == 1:
            self.image.clip_draw(30, 0, 30, 50, self.x, self.y)

    def update(self):
        self.x = pos[self.pos]





def enter():
    global image
    global select
    global ui
    select = SELECT()
    ui = UI(name)
    image = load_image('select.png')
    pass


def exit():
    global image
    global select
    global ui
    del(image)
    del(select)
    del(ui)
    pass


def update():
    select.update()
    ui.update()
    pass


def draw():
    global image
    global select
    global ui
    clear_canvas()
    image.draw(400,300)
    select.draw()
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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_state(load_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if select.pos < 4: select.pos += 1
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if select.pos > 0: select.pos -= 1

    pass
