import socket
import pyautogui
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from pynput.mouse import Button
import json
from screeninfo import get_monitors

screensize = pyautogui.size()
mouseController = MouseController()
keyboardController = KeyboardController()

name = "JT-Laptop"

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
    if data["target"] != name:
        continue
    if data["message"] == "info":
        for m in get_monitors():
            if m.is_primary:
                s.sendto(json.dumps({
                    "x": m.x,
                    "y": m.y,
                    "width": m.width,
                    "height": m.height,
                    "width_mm": m.width_mm,
                    "height_mm": m.height_mm
                }).encode("utf-8"), client)
                break
    elif data["message"] == "mouse":
        x = data["coords"]["x"]
        y = data["coords"]["y"]
        mouseController.position = (x, y)
    elif data["message"] == "press":
        keycode = data["keycode"]
        for k in Key:
            if str(k) == keycode:
                keyboardController.press(k)
                break
        else:
            keyboardController.press(keycode.strip("\'"))
    elif data["message"] == "unpress":
        keycode = data["keycode"]
        for k in Key:
            if str(k) == keycode:
                keyboardController.release(k)
                break
        else:
            keyboardController.release(keycode.strip("\'"))
        # keyboardController.tap(KeyCode.from_vk(keycode))
    elif data["message"] == "button":
        button = data["button"]
        for b in Button:
            if str(b) == button:
                mouseController.press(b)
    elif data["message"] == "unbutton":
        button = data["button"]
        for b in Button:
            if str(b) == button:
                mouseController.release(b)
    elif data["message"] == "quit":
        break
