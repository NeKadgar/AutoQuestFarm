import math
from PIL import ImageGrab, Image
from AddonData.WorldData import PI, PI2, WorldData
import pyautogui
from Base.WowWindow import WowWindow
from AddonData.config import Pixels
from Base.utils import scalar_mult, vector_mult
import time
import autoit
from .WoWPoint import WoWPoint
import keyboard
from DB.PointsDB import add_point, get_location_points, get_near_points


def calculate_heading(p_from, p_to):  # for WoWPoint's
    target = math.atan2(p_to.x - p_from.x, p_to.y - p_from.y)
    return math.pi + target


def distance_to(p_from, p_to):
    x = p_from.x - p_to.x
    y = p_from.y - p_to.y
    x = x * 100
    y = y * 100
    distance = math.sqrt((x * x) + (y * y))
    return distance


def get_direction_key_to_press(desired_direction):
    result = "A" if (PI2 + desired_direction - WorldData.facing) % PI2 < PI else "D"
    return result


def get_direction(p_from, p_to, angle):
    dx = p_from.x - p_to.x
    dy = p_from.y - p_to.y
    result = [scalar_mult(-math.sin(angle), -math.cos(angle), dx, dy),
              vector_mult(-math.sin(angle), -math.cos(angle), dx, dy)]
    return result


def turn(desired_direction):
    WorldData.update(image=ImageGrab.grab(Pixels.pixels_cord))
    key = get_direction_key_to_press(desired_direction)
    while True:
        pyautogui.keyDown(key)
        time.sleep(0.1)
        pyautogui.keyUp(key)
        WorldData.update(image=ImageGrab.grab(Pixels.pixels_cord))
        if desired_direction - 0.7 < WorldData.facing < desired_direction + 0.7:
            break


def move_to_point(p_to):
    WorldData.update(image=ImageGrab.grab(Pixels.pixels_cord))
    while True:
        t = time.time()
        WorldData.update(image=ImageGrab.grab(Pixels.pixels_cord))
        x, y, facing = WorldData.x, WorldData.y, WorldData.facing

        dir = get_direction(WoWPoint(000, x, y), p_to, facing)
        if abs(dir[0]) < 0.1 and abs(dir[1]) < 0.1:
            break
        if abs(dir[0]) >= abs(dir[1]):
            autoit.send("{a up}{d up}")
            if dir[0] <= 0:
                autoit.send("{w down}{s up}")
            else:
                autoit.send("{s down}{w up}")
        else:
            autoit.send("{s up}")
            if dir[1] < 0:
                autoit.send("{d down}{a up}")
            else:
                autoit.send("{a down}{d up}")
        # print("runtime:", time.time() - t)
    autoit.send("{s up}{a up}{d up}{w up}")


def move_by_points(points):
    WowWindow.set_focus()
    for p_to in points:
        # print(p_to)
        move_to_point(p_to)


def record_points():
    WowWindow.set_focus()
    while True:
        if keyboard.is_pressed('alt'):
            break
        WorldData.update(image=ImageGrab.grab(Pixels.pixels_cord))
        x, y, location = WorldData.x, WorldData.y, WorldData.zone
        add_point(location, x, y)
        time.sleep(1)
