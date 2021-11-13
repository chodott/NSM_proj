from pico2d import *
import game_framework
import main_state

name = "SelectState"


class PLAYER:
    def __init__(self):
        self.x,self.y = 120, 300
        self.image = load_image('stagemario.png')
        self.frame = 0

    def draw(self):
        if self.frame == 0:
            self.image.clip_draw(00,0,30,50,self.x,self.y)
        elif self.frame == 1:
            self.image.clip_draw(30, 0, 30, 50, self.x, self.y)




def enter():
    global image
    global player
    player = PLAYER()
    image = load_image('select.png')
    pass


def exit():
    global image
    del(image)
    pass


def update():
    pass


def draw():
    global image
    global player
    clear_canvas()
    image.draw(400,300)
    player.draw()
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
            game_framework.change_state(main_state)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RSHIFT):
            player.frame = 1


    pass

