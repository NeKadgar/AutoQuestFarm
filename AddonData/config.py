import pyautogui
import keyboard


class Pixels(object):
    pixels_cord = [0, 0, 290, 10]
    x = (10, 5)
    facing = x
    y = (30, 5)
    zone_name = (50, 5)
    max_health = (70, 5)
    current_health = (90, 5)
    max_mana = (110, 5)
    current_mana = (130, 5)
    level = (150, 5)
    range_to_target = (170, 5)
    target_name1 = (190, 5)
    target_name2 = (210, 5)
    target_health = (230, 5)
    target_max_health = (250, 5)
    target_lvl = (270, 5)
    target_attack_range = (270, 5)


    @classmethod
    def cursor_position(cls):
        while True:
            if keyboard.is_pressed('alt'):
                print(pyautogui.position())
                return pyautogui.position()
