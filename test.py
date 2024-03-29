from AddonData.config import Pixels
from AddonData.WorldData import WorldData
from PIL import ImageGrab
from Base.utils import convert_wowhead_cords
from Base.ScriptInterpreter import ScriptInterpreter
from DB.Location import Location
from Cursor.Cursor import Cursor
import time
from Path.WoWPoint import WoWPoint
from DB.PointsDB import get_near_points, get_location_points
from Path.Graph import find_path, Graph
from Base.SharkEye import SharkEye
from Base.FightRotation import MageRotation
from Path.StuckDetector import stuck_detector


# WowWindow.set_focus()
Pixels.cursor_position()
# move_by_points(points)
# c = "46.4 32.4 46.4 32.6 47.2 34.0 47.2 35.0 47.4 32.4 47.4 32.6 47.4 36.0 47.4 37.0 47.6 31.8 47.6 32.8 47.6 36.0 47.6 36.8 47.8 31.2 48.0 35.4 48.4 33.6 48.6 33.8 48.8 33.0 48.8 36.0 49.2 35.2 50.0 33.2 50.0 34.4 50.0 35.0 50.8 38.0 51.0 35.4 51.0 35.6 51.0 38.6 51.4 36.6 51.6 36.4 51.6 36.6 51.6 37.6"
# convert_wowhead_cords(c)
# Cursor.find_quest()
# WorldData.update(ImageGrab.grab(Pixels.pixels_cord))
# Location.show_points_on_map(697687)
WorldData.update(ImageGrab.grab(Pixels.pixels_cord))
# MageRotation.prepare()
# SharkEye.set_target()
# MageRotation.attack()
# SharkEye.find_lootable()

# stuck_detector()
# Cursor.save_cursor_icon("Cursor/Icons/AutoLoot1.bmp")
ScriptInterpreter.load_script("Human")
ScriptInterpreter.start()
# points = get_location_points(697687)
# p_to = WoWPoint(000, 48.93, 40.16)
# p_from = WoWPoint(000, 48.16, 42.93)
# way = find_path(697687, WoWPoint(000, 48.16, 42.93), WoWPoint(000, 48.93, 40.16))
# print(way)
# for i in way:
#     print(i)
# goal = min(points, key=lambda x: distance_to(x, p_to))
# print(goal)
WorldData.show()
