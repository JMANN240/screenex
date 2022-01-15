import socket
from pynput.mouse import Controller as MouseController
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import KeyCode, Key
import json
from time import sleep
from util import to_monitors, on_monitors, monitor_from_dict, monitor
from config import *

from screeninfo import get_monitors
monitors = get_monitors()

with open("screens.json") as json_file:
    screens = [monitor_from_dict(m) for m in json.load(json_file)]

mouseController = MouseController()

init_pos = tuple(mouseController.position)
pos = list(mouseController.position)

def move_callback(x, y):
    global pos, init_pos, suppressedMouseListener, mouseListener, suppressedKeyboardListener, controlling_self
    if controlling_self:
        pos = [x, y]
        if not on_monitors(pos[0], pos[1], monitors):
            controlling_self = not controlling_self
            mouseListener.stop()
            init_pos = to_monitors(pos[0], pos[1], monitors)
            mouseController.position = init_pos
            mouseController.position = init_pos
            suppressedMouseListener = MouseListener(on_move=suppressed_move_callback, on_click=suppressed_click_callback, suppress=True)
            suppressedKeyboardListener = KeyboardListener(on_press=suppressed_keypress_callback, on_release=suppressed_keyunpress_callback, suppress=True)
            suppressedMouseListener.start()
            suppressedKeyboardListener.start()

def suppressed_move_callback(x, y):
    global pos, init_pos, suppressedMouseListener, mouseListener, suppressedKeyboardListener, controlling_self
    if not controlling_self:
        pos[0] += x - init_pos[0]
        pos[1] += y - init_pos[1]
        if on_monitors(pos[0], pos[1], monitors):
            controlling_self = not controlling_self
            suppressedMouseListener.stop()
            suppressedKeyboardListener.stop()
            init_pos = to_monitors(pos[0], pos[1], monitors)
            mouseController.position = init_pos
            mouseController.position = init_pos
            mouseListener = MouseListener(on_move=move_callback)
            mouseListener.start()

def suppressed_click_callback(x, y, button, pressed):
    if pressed:
        pressed_buttons.append(str(button))
    else:
        released_buttons.append(str(button))

def suppressed_keypress_callback(key):
    if suppressedKeyboardListener.canonical(key) == Key.ctrl:
        key = suppressedKeyboardListener.canonical(key)
    pressed_keys.append(str(key))

def suppressed_keyunpress_callback(key):
    if suppressedKeyboardListener.canonical(key) == Key.ctrl:
        key = suppressedKeyboardListener.canonical(key)
    released_keys.append(str(key))


mouseListener = MouseListener(on_move=move_callback)
suppressedMouseListener = MouseListener(on_move=suppressed_move_callback, suppress=True)
suppressedKeyboardListener = KeyboardListener(on_press=suppressed_keypress_callback, on_release=suppressed_keyunpress_callback, suppress=True)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(client)

last_pos = list(pos)

controlling_self = True
pressed_keys = []
released_keys = []
pressed_buttons = []
released_buttons = []

mouseListener.start()

while True:
    if pos != last_pos:
        target = monitor(pos[0], pos[1], screens)
        if target is not None and not controlling_self:
            s.sendto(json.dumps({
                "target": target.name,
                "message": "mouse",
                "coords": {
                    "x": pos[0] - target.x,
                    "y": pos[1] - target.y
                }
            }).encode('utf-8'), server)
        last_pos = list(pos)
    
    for key in pressed_keys:
        s.sendto(json.dumps({
            "target": target.name,
            "message": "press",
            "keycode": key
        }).encode('utf-8'), server)
    pressed_keys = []

    for key in released_keys:
        s.sendto(json.dumps({
            "target": target.name,
            "message": "unpress",
            "keycode": key
        }).encode('utf-8'), server)
    released_keys = []

    for button in pressed_buttons:
        s.sendto(json.dumps({
            "target": target.name,
            "message": "button",
            "button": button
        }).encode('utf-8'), server)
    pressed_buttons = []

    for button in released_buttons:
        s.sendto(json.dumps({
            "target": target.name,
            "message": "unbutton",
            "button": button
        }).encode('utf-8'), server)
    released_buttons = []

    sleep(1/60)
