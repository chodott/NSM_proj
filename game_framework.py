from pico2d import *
import time
frame_time = 0.0
running = None
stack = None
clear_level = 4
cur_level = 0
Life = 3
PIXEL_PER_METER = (10.0 / 0.3)
GRAVITY_SPEED_KMPH = 35.0
GRAVITY_SPEED_MPM = (GRAVITY_SPEED_KMPH * 1000.0 / 60.0)
GRAVITY_SPEED_MPS = (GRAVITY_SPEED_MPM / 60.0)
GRAVITY_SPEED_PPS = (GRAVITY_SPEED_MPS * PIXEL_PER_METER)


class GameState:
    def __init(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw


def change_state(state):
    global stack
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    stack.append(state)
    state.enter()
    pass


def quit():
    global running
    running = False


def run(start_state):
    global running, stack
    running = True
    stack = [start_state]
    start_state.enter()
    global frame_time
    current_time = time.time()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
        frame_time = time.time() - current_time
        frame_rate = 1.0/ frame_time
        current_time += frame_time

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()



