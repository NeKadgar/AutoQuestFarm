import os
import json
from AddonData.WorldData import WorldData
from AddonData.config import Pixels
from PIL import ImageGrab
from Path.Graph import find_path
from Path.WoWPoint import WoWPoint
from Path.PlayerDirection import move_by_points
from Cursor.Cursor import Cursor
import json
from Path.PlayerDirection import distance_to, calculate_heading, turn
from Base.SharkEye import SharkEye, rotation


class ScriptInterpreter(object):
    script = None
    units = None

    @classmethod
    def load_script(cls, race):
        path_to_script = os.path.abspath("DB/scripts/script.json")
        path_to_units = os.path.abspath("DB/json/units.json")

        with open(path_to_script) as file:
            cls.script = json.load(file)[race]
        with open(path_to_units) as file:
            cls.units = json.load(file)

    @classmethod
    def start(cls):
        for action in cls.script:
            if action["Action"][0] == "Quest":
                WorldData.update(image=ImageGrab.grab(Pixels.pixels_cord))
                way = find_path(action["location"], WoWPoint(000, WorldData.x, WorldData.y), WoWPoint(000, *action["NPC"]))
                move_by_points(way)
                Cursor.find_quest()

            if action["Action"][0] == "Kill":
                WorldData.update()
                for unit in action["NPC"]:
                    units = cls.units[unit[0]]
                    for i in range(0, unit[1]):
                        rotation.prepare()
                        enemy = min(units, key=lambda x: distance_to(WoWPoint(000, x[0], x[1]),
                                                                     WoWPoint(000, WorldData.x, WorldData.y)))
                        units = [item for item in units if item != enemy]
                        way = find_path(action["location"], WoWPoint(000, WorldData.x, WorldData.y),
                                        WoWPoint(000, *enemy))
                        move_by_points(way)
                        turn(calculate_heading(WoWPoint(000, WorldData.x, WorldData.y), WoWPoint(000, *enemy)))
                        print("Killing {} at {}".format(unit[0], enemy))
                        SharkEye.set_target()
                        SharkEye.attack()
                        if action["Action"][1] == "Loot":
                            SharkEye.find_lootable()
