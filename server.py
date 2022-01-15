from pynput.keyboard import Listener as KeyListener
from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListener
from time import sleep, time
import socketio

sio = socketio.Server()

mouseController = MouseController()

init_pos = tuple(mouseController.position)
pos = list(mouseController.position)

def move_callback(x, y):
    global pos
    pos = [x, y]
    print(f"not:{pos}")

def suppressed_move_callback(x, y):
    global pos, init_pos
    pos[0] += x - init_pos[0]
    pos[1] += y - init_pos[1]
    print(f"sup:{pos}")
    sio.emit('mouse', {'x': x, 'y': y})

mouseListener = MouseListener(on_move=move_callback)
suppressedMouseListener = MouseListener(on_move=suppressed_move_callback, suppress=True)

mouseListener.start()
mouseListener.wait()

t = time()

while time() - t < 60:
    if (mouseListener.running and pos[1] < 0):
        print("switching to suppressing")
        mouseListener.stop()
        init_pos = tuple(mouseController.position)
        suppressedMouseListener = MouseListener(on_move=suppressed_move_callback, suppress=True)
        suppressedMouseListener.start()
        suppressedMouseListener.wait()
    
    
    if (suppressedMouseListener.running and pos[1] >= 0):
        print("switching to free")
        suppressedMouseListener.stop()
        mouseController.position = tuple(pos)
        mouseListener = MouseListener(on_move=move_callback)
        mouseListener.start()
        mouseListener.wait()

mouseListener.stop()
suppressedMouseListener.stop()