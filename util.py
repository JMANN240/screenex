import screeninfo
from math import inf

def dist(x1, y1, x2, y2):
    return (((x1-x2)**2)+((y1-y2)**2))**0.5

def monitor_from_dict(dict):
    return screeninfo.Monitor(name=dict["name"], x=dict["x"], y=dict["y"], width=dict["width"], height=dict["height"])

def on_monitor(x, y, monitor):
    within_x = x >= monitor.x and x < monitor.x + monitor.width
    within_y = y >= monitor.y and y < monitor.y + monitor.height
    return within_x and within_y

def on_monitors(x, y, monitors):
    return any([on_monitor(x, y, m) for m in monitors])

def monitor(x, y, monitors):
    for m in monitors:
        if on_monitor(x, y, m):
            return m
    return None

def to_monitor(x, y, monitor):
    if x < monitor.x:
        x = monitor.x
    elif x >= monitor.x + monitor.width:
        x = monitor.x + monitor.width - 1

    if y < monitor.y:
        y = monitor.y
    elif y >= monitor.y + monitor.height:
        y = monitor.y + monitor.height - 1

    return x, y

def closest_monitor(x, y, monitors):
    min_dist = inf
    ret = None

    for m in monitors:
        c_x, c_y = to_monitor(x, y, m)
        if dist(c_x, c_y, x, y) < min_dist:
            min_dist = dist(c_x, c_y, x, y)
            ret = m
    
    return ret

def to_monitors(x, y, monitors):
    if on_monitors(x, y, monitors):
        return x, y
    
    closest = closest_monitor(x, y, monitors)
    return to_monitor(x, y, closest)

if __name__ == "__main__":
    monitors = screeninfo.get_monitors()
    point = (100, 100)
    print(f"Point {'is' if on_monitors(point[0], point[1], monitors) else 'isnt'} on the monitors")
    print(f"Point to monitor {monitors[0]} is {to_monitor(point[0], point[1], monitors[0])}")
    point = (800, -100)
    print(f"Closest monitor to point {point} is {closest_monitor(point[0], point[1], monitors)}")
    print(f"Point {point} would be moved to {to_monitors(point[0], point[1], monitors)}")
    point = (1700, -100)
    print(f"Closest monitor to point {point} is {closest_monitor(point[0], point[1], monitors)}")
    print(f"Point {point} would be moved to {to_monitors(point[0], point[1], monitors)}")
    point = (10, -100)
    print(f"Closest monitor to point {point} is {closest_monitor(point[0], point[1], monitors)}")
    print(f"Point {point} would be moved to {to_monitors(point[0], point[1], monitors)}")