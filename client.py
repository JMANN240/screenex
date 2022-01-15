import socket
from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListener

mouseController = MouseController()

init_pos = tuple(mouseController.position)
pos = list(mouseController.position)

def move_callback(x, y):
    global pos, init_pos, suppressedMouseListener, mouseListener
    pos = [x, y]
    print(f"not:{pos}")
    if mouseListener.running and pos[1] < 0:
        print("switching to suppressing")
        mouseListener.stop()
        init_pos = (mouseController.position[0], 0)
        suppressedMouseListener = MouseListener(on_move=suppressed_move_callback, suppress=True)
        suppressedMouseListener.start()
        suppressedMouseListener.wait()

def suppressed_move_callback(x, y):
    global pos, init_pos, suppressedMouseListener, mouseListener
    pos[0] += x - init_pos[0]
    pos[1] += y - init_pos[1]
    print(f"sup:{pos}")
    if suppressedMouseListener.running and pos[1] >= 0:
        print("switching to free")
        suppressedMouseListener.stop()
        mouseController.position = tuple(pos)
        mouseListener = MouseListener(on_move=move_callback)
        mouseListener.start()
        mouseListener.wait()

mouseListener = MouseListener(on_move=move_callback)
suppressedMouseListener = MouseListener(on_move=suppressed_move_callback, suppress=True)

mouseListener.start()
mouseListener.wait()

server = ('10.42.0.1', 4000)
client = ('10.42.0.226', 4001)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(client)

last_pos = list(pos)

while pos != [100, 100]:
    if pos != last_pos:
        s.sendto(f"{pos[0]} {pos[1]}".encode('utf-8'), server)
        last_pos = list(pos)

s.sendto("quit".encode('utf-8'), server)
s.close()
