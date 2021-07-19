import os
import json
from AddonData.WorldData import WorldData
from AddonData.config import Pixels
from PIL import ImageGrab
from Path.Graph import find_path
from Path.WoWPoint import WoWPoint
from Path.PlayerDirection import move_by_points
from Cursor.Cursor import Cursor

class ScriptInterpreter(object):
    script = None

    @classmethod
    def load_script(cls, race):
        path_to_script = os.path.abspath("DB/scripts/script.json")
        with open(path_to_script) as file:
            cls.script = json.load(file)[race]
        print(cls.script)

    @classmethod
    def start(cls):
        for action in cls.script:
            if action["Action"][0] == "Quest":
                WorldData.update(image=ImageGrab.grab(Pixels.pixels_cord))
                way = find_path(action["location"], WoWPoint(000, WorldData.x, WorldData.y), WoWPoint(000, *action["NPC"]))
                move_by_points(way)
                Cursor.find_quest()
