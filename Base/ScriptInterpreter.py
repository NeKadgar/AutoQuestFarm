import os
import json
import time

import pyautogui

from AddonData.WorldData import WorldData
from AddonData.config import Pixels
from PIL import ImageGrab
from Path.StuckDetector import stuck_detector
from DB.PointsDB import get_location_points
from Path.Graph import find_path
from Path.WoWPoint import WoWPoint
from Path.PlayerDirection import move_by_points
from Cursor.Cursor import Cursor
import json
from Path.PlayerDirection import distance_to, calculate_heading, turn
from Base.SharkEye import SharkEye, rotation
from DB.Units import Units
from Base.TelegramCore import TelegramCore
from threading import Thread


class ActionScript:
    pass


class ScriptInterpreter(object):
    script = None
    units = None
    counter = 0
    bin_dict = None

    @classmethod
    def get_current_action(cls):
        with open('bin') as file:
            cls.bin_dict = json.load(file)
            cls.counter = cls.bin_dict["counter"]

    @classmethod
    def increase_counter(cls):
        with open('bin', 'w') as f:
            cls.counter += 1
            cls.bin_dict["counter"] = cls.counter
            json.dump(cls.bin_dict, f)

    @classmethod
    def load_script(cls, race):
        path_to_script = os.path.abspath("DB/scripts/script.json")
        path_to_units = os.path.abspath("DB/json/units.json")

        with open(path_to_script) as file:
            cls.script = json.load(file)[race]
        with open(path_to_units) as file:
            cls.units = json.load(file)
        cls.get_current_action()

    @classmethod
    def start(cls, session_name):
        cls.session_name = session_name
        th = Thread(target=stuck_detector)
        th.start()
        for action in cls.script[cls.counter:]:
            if action["Action"][0] == "Quest":
                WorldData.update()
                way = find_path(action["location"], WoWPoint(000, WorldData.x, WorldData.y),
                                WoWPoint(000, *action["NPC"]))
                move_by_points(way)
                WorldData.is_busy = True
                Cursor.find_quest()
                WorldData.is_busy = False

            if action["Action"][0] == "Sell":
                WorldData.update(image=ImageGrab.grab(Pixels.pixels_cord))
                way = find_path(action["location"], WoWPoint(000, WorldData.x, WorldData.y),
                                WoWPoint(000, *action["NPC"]))
                move_by_points(way)
                WorldData.is_busy = True
                Cursor.find_seller()
                WorldData.is_busy = False

            if action["Action"][0] == "Kill":
                WorldData.update()
                for unit in action["NPC"]:
                    WorldData.current_target = unit[0]
                    points = Units.get_enemy_points(unit[0], action["location"])
                    _points = points.copy()
                    for i in range(0, unit[1]):
                        WorldData.update()
                        WorldData.is_busy = True
                        rotation.prepare()
                        WorldData.is_busy = False
                        enemy = min(points, key=lambda p: distance_to(WoWPoint(000, p.x, p.y),
                                                                      WoWPoint(000, WorldData.x, WorldData.y)))
                        points = [item for item in points if item != enemy]
                        way = find_path(action["location"], WoWPoint(000, WorldData.x, WorldData.y),
                                        WoWPoint(000, enemy.x, enemy.y))
                        move_by_points(way)
                        WorldData.is_busy = True
                        if not points:
                            points = _points.copy()
                        print("Killing {} at {}".format(unit[0], enemy))
                        if SharkEye.set_target():
                            SharkEye.attack()
                            if action["Action"][1] == "Loot":
                                SharkEye.loot_time = time.time()
                                SharkEye.find_lootable()
                        else:
                            pyautogui.keyDown("d")
                            time.sleep(1.2)
                            pyautogui.keyUp("d")
                            if SharkEye.set_target():
                                SharkEye.attack()
                                if action["Action"][1] == "Loot":
                                    SharkEye.loot_time = time.time()
                                    SharkEye.find_lootable()
                            else:
                                i -= 1
                        WorldData.is_busy = False

            if action["Action"][0] == "SendM":
                TelegramCore.send_message(cls.session_name, action["Action"][1])
            cls.increase_counter()
