from pico2d import *
import time
frame_time = 0.0

class GameState:
    def __init(self, state):
        self.enter = state.enter
        self.exit = state.exit
        self.handle_events = state.handle_events
        self.update = state.update
        self.draw = state.draw

running = None
stack = None
Life = 3

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
        #delay(0.05)

    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()



