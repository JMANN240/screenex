# Screenex

Put your old laptop to use! Screenex allows you to seamlessly control other computers as if they were connected to your own! Your mouse is no longer bound by your monitors, but can roam freely on an infinite 2D plane. "Place" screens on that plane to control them remotely

Configure the computers' IP addresses in `config.py` and configure the screen you want to control in `screens.json`. The dependencies are in `requirements.txt`. Run `server.py` on your computer you want to control and run `client.py` on your primary computer.

## Configuration

Think of your screens being part of some 'virtual 2D space'. The top left corner of your primary monitor is (0, 0). In `screens.json` you can configure the screens that you want to control. For example, if my primary monitor is 1600x900 and one I want to control is directly to the right of it, I would set the x to 1600 and the y to 0.

## Todo:

 - Multiple screens
 - Easier config