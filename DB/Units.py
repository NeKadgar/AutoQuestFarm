import json
import os
from shapely.geometry.polygon import Polygon
from shapely.geometry.point import Point

from DB.PointsDB import get_location_points


class Units:
    path_to_units = os.path.abspath("DB/json/units.json")
    loaded = False
    units = {}

    @classmethod
    def load(cls):
        with open(cls.path_to_units, "r") as file:
            cls.units = json.load(file)
        cls.loaded = True

    @classmethod
    def update(cls, key, value):
        if not cls.loaded:
            cls.load()
        cls.units[key.upper()] = value
        with open(cls.path_to_units, "w") as jsonFile:
            json.dump(cls.units, jsonFile)

    @classmethod
    def get_polygon(cls, key):
        if not cls.loaded:
            cls.load()
        return Polygon([[p[0], p[1]] for p in cls.units[key.upper()]])

    @classmethod
    def get_enemy_points(cls, key, location):
        polygon = cls.get_polygon(key)
        points = get_location_points(location)
        points = [Point(p.x, p.y) for p in points]
        return [p for p in points if polygon.contains(p)]
