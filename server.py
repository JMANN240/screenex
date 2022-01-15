import socket
import pyautogui
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import json

screensize = pyautogui.size()
mouseController = MouseController()
keyboardController = KeyboardController()

server = ('10.42.0.1', 4000)
client = ('10.42.0.226', 4001)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(server)
data = ""
while True:
    data, addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    data = json.loads(data)
    print(json.dumps(data, indent=4))
    if data["message"] == "mouse":
        x = data["coords"]["x"]
        y = data["coords"]["y"]
        mouseController.position = (x, screensize[1]+y)
    elif data["message"] == "press":
        keycode = data["keycode"]
    elif data["message"] == "unpress":
        keycode = data["keycode"]
        # keyboardController.tap(KeyCode.from_vk(keycode))
    elif data["message"] == "quit":
        break