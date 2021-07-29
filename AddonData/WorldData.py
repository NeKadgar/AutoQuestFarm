import time

import cv2
import numpy as np
import pyautogui
import pydirectinput

from Base import WowWindow
from .config import Pixels
from Path.WoWPoint import WoWPoint
from PIL import ImageGrab

PI = 3.14159265
PI2 = PI * 2


class WorldData(object):
    x = None
    y = None
    facing = None
    zone = None
    max_health = None
    current_health = None
    max_mana = None
    current_mana = None
    level = None
    range_to_target = None
    target_name = None
    target_health = None
    target_max_health = None
    target_lvl = None
    target_attack_range = None
    quest_counter = None
    in_combat = 0
    in_combat_bot = False  # if in combat by script
    _set_target = None
    _attack = None
    _find_target = None

    @classmethod
    def update(cls, *args, **kwargs):
        image = ImageGrab.grab(Pixels.pixels_cord)
        cls.x = (image.getpixel(Pixels.x)[0] + image.getpixel(Pixels.x)[1] / 255) / 255 * 100
        cls.y = (image.getpixel(Pixels.y)[0] + image.getpixel(Pixels.y)[1] / 255) / 255 * 100
        cls.in_combat = image.getpixel(Pixels.in_combat)[2]
        cls.facing = image.getpixel(Pixels.facing)[2] * 2 * PI / 255
        cls.zone = "".join([str(a) for a in image.getpixel(Pixels.zone_name)])
        cls.max_health = sum(list(image.getpixel(Pixels.max_health)))
        cls.current_health = sum(list(image.getpixel(Pixels.current_health)))
        cls.max_mana = sum(list(image.getpixel(Pixels.max_mana)))
        cls.current_mana = sum(list(image.getpixel(Pixels.current_mana)))
        cls.level = sum(list(image.getpixel(Pixels.level)))
        cls.range_to_target = sum(list(image.getpixel(Pixels.range_to_target)))
        cls.target_name = sum(list(image.getpixel(Pixels.target_name1)))  # not work
        cls.target_health = sum(list(image.getpixel(Pixels.target_health)))
        cls.target_max_health = sum(list(image.getpixel(Pixels.target_max_health)))
        cls.target_lvl = image.getpixel(Pixels.target_lvl)[0]
        cls.target_attack_range = image.getpixel(Pixels.target_attack_range)[2]
        cls.quest_counter = sum(list(image.getpixel(Pixels.quest_counter)))
        if not cls.in_combat_bot:
            if cls.in_combat:
                print("start fight")
                cls.in_combat_bot = True
                # if not WorldData.target_health:
                #     print("set target")
                #     cls._set_target()

                pyautogui.press("enter")
                pyautogui.typewrite("/targetmarker 6", interval=0.01)
                pyautogui.press("enter")
                f = False
                while not f:
                    pyautogui.keyDown("a")
                    time.sleep(0.5)
                    pyautogui.keyUp("a")
                    f = cls._find_target()
                    print(f)

                print("attack mode")
                cls._attack()
        return 0

    @classmethod
    def set_funcs(cls, set_target, attack, find_target):
        cls._set_target = set_target
        cls._attack = attack
        cls._find_target = find_target

    @classmethod
    def quest_completed(cls, *args, **kwargs):
        image = ImageGrab.grab(Pixels.pixels_cord)
        count = sum(list(image.getpixel(Pixels.quest_counter)))
        if cls.quest_counter != count:
            cls.quest_counter = count
            return True
        return False

    @classmethod
    def show(cls):
        attrs = ["{}: {}".format(attr, value) for attr, value in cls.__dict__.items() if not attr.startswith('__')]
        print("\n".join(attrs))

    @classmethod
    def position(cls):
        return WoWPoint(cls.x, cls.y)
