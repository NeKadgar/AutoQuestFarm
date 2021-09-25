from AddonData.WorldData import WorldData
import pyautogui
import pydirectinput
import time
from Base.utils import Commands, mouse_drag
import threading


class Target:
    def __init__(self, health=None, change_time=None):
        self.health = health
        self.change_time = change_time


class Spell:
    def __init__(self, effect_duration=None, casted=False, button=None, time_of_cast=0, cast_range=0,
                 mana_cost=None, cast_time=0.0):
        self.effect_duration = effect_duration
        self.casted = casted
        self.button = button
        self.time_of_cast = time_of_cast
        self.cast_range = cast_range
        self.mana_cost = mana_cost
        self.cast_time = cast_time

    def cast(self):
        pyautogui.press(self.button)
        self.casted = True
        self.time_of_cast = time.time()
        # pyautogui.dragRel(4000, 0, duration=self.cast_time+0.4, button="right")
        time.sleep(self.cast_time)

    def rotating_cast(self):
        t = time.time()
        while time.time() - t < self.cast_time+0.4:
            pyautogui.press(self.button)
            time.sleep(0.1)

    def rotating(self):
        pyautogui.dragRel(4000, 0, duration=self.cast_time+0.4, button="right")

    def is_available(self):
        if WorldData.current_mana >= self.mana_cost:
            if time.time() - self.time_of_cast > self.effect_duration:
                return True
        return False

    def is_in_range(self):
        if WorldData.range_to_target:
            if self.cast_range >= WorldData.range_to_target:
                return True
            return False
        return True


class MageRotation(object):
    heal_spell = Spell(effect_duration=18, button="=", cast_range=999, mana_cost=0)
    mana_spell = Spell(effect_duration=18, button="-", cast_range=999, mana_cost=0)
    frost_armor = Spell(effect_duration=1800, button="0", cast_range=999, mana_cost=60)
    fire_ball = Spell(effect_duration=0, button="2", cast_range=35, cast_time=1.6, mana_cost=30)

    @classmethod
    def prepare(cls):
        WorldData.update()
        t = time.time()

        while time.time() - t < 20:
            WorldData.update()
            health = WorldData.current_health / WorldData.max_health
            mana = WorldData.current_mana / WorldData.max_mana
            if cls.frost_armor.is_available():
                cls.frost_armor.cast()

            if health < 0.6 and cls.heal_spell.is_available():
                cls.heal_spell.cast()

            if mana < 0.6 and cls.mana_spell.is_available():
                cls.mana_spell.cast()

            if mana > 0.8 and health > 0.8:
                if cls.frost_armor.is_available():
                    print(cls.frost_armor.is_available())
                    cls.frost_armor.cast()
                return True
            time.sleep(0.5)

        return True

    @classmethod
    def set_facing(cls):
        pyautogui.press("2")
        time.sleep(0.1)
        WorldData.update()
        time.sleep(0.1)
        if WorldData.action_used:
            return True
        t = time.time()
        pyautogui.keyDown("a")
        while time.time() - t <= 10:
            pyautogui.press("2")
            WorldData.update()
            if WorldData.action_used:
                pyautogui.keyUp("a")
                return True
            if not WorldData.target_health:
                pyautogui.keyUp("a")
                return True
        pyautogui.keyUp("a")
        return True

    @classmethod
    def attack(cls):
        t = time.time()
        while WorldData.target_health >= 1 and time.time() - t < 40:
            WorldData.update()
            if cls.fire_ball.is_in_range():
                pyautogui.press("1")
                if not cls.fire_ball.is_available():
                    time.sleep(2)
                cls.set_facing()
                cls.fire_ball.cast()
        WorldData.in_combat_bot = False
