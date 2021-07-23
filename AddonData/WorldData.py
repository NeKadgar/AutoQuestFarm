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

    @classmethod
    def update(cls, *args, **kwargs):
        image = ImageGrab.grab(Pixels.pixels_cord)
        cls.x = (image.getpixel(Pixels.x)[0] + image.getpixel(Pixels.x)[1] / 255) / 255 * 100
        cls.y = (image.getpixel(Pixels.y)[0] + image.getpixel(Pixels.y)[1] / 255) / 255 * 100
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
        return 0

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
