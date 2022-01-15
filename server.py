import socket
import pyautogui
from pynput.mouse import Controller as MouseController

screensize = pyautogui.size()
mouseController = MouseController()

server = ('10.42.0.1', 4000)
client = ('10.42.0.226', 4001)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(server)
data = ""
while True:
    data, addr = s.recvfrom(1024)
    data = data.decode('utf-8')
    if data == "quit":
        break
    coords = (int(coord) for coord in data.split(" "))
    x = coords[0]
    y = coords[1]
    mouseController.position = (x, screensize+y)