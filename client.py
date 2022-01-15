import socketio
import pyautogui
from pynput.mouse import Controller as MouseController

screensize = pyautogui.size()
mouseController = MouseController()

sio = socketio.Client()

@sio.on('mouse')
def handle_mouse(x, y):
    print("mouse event")
    print(x, y)
    # mouseController.position = (x, screensize+y)

sio.connect('http://10.244.34.14:8070')