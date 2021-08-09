import time

import cv2
import numpy as np
import pyautogui
import pydirectinput
from Base.utils import Commands
from Base import WowWindow
from .config import Pixels
from Path.WoWPoint import WoWPoint
from PIL import ImageGrab
import autoit

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
    action_used = None
    quest_counter = None
    in_combat = 0
    in_combat_bot = False  # if in combat by script
    in_dead_body = False
    _set_target = None
    _attack = None
    _find_target = None
    _move_to_point = None

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
        cls.action_used = image.getpixel(Pixels.action_used)[1]
        if not cls.in_combat_bot:
            if cls.in_combat:
                autoit.send("{s up}{a up}{d up}{w up}")
                print("start fight")
                cls.in_combat_bot = True
                print("attack mode")
                cls._attack()
        if not cls.in_dead_body:
            if cls.current_health < 2:
                cls.in_dead_body = True
                print("dead")
                x, y = cls.x, cls.y
                print(x, y)
                pyautogui.typewrite(Commands.REPOP, interval=0.01)
                pyautogui.press("enter")
                time.sleep(10)
                cls._move_to_point(WoWPoint(000, x, y))
                pyautogui.typewrite(Commands.RETRIVE, interval=0.01)
                pyautogui.press("enter")
                time.sleep(1)
        return 0

    @classmethod
    def set_funcs(cls, set_target, attack, find_target, move_to_point):
        cls._set_target = set_target
        cls._attack = attack
        cls._find_target = find_target
        cls._move_to_point = move_to_point

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
