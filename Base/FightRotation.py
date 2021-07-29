from AddonData.WorldData import WorldData
import pyautogui
import time


class Target:
    def __init__(self, health=None):
        self.health = health


class Spell:
    def __init__(self, effect_duration=None, casted=False, button=None, time_of_cast=0, cast_range=0,
                 mana_cost=None, cast_time=None):
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

            if health < 0.6:
                cls.heal_spell.cast()

            if mana < 0.6:
                cls.mana_spell.cast()

            if mana > 0.8 and health > 0.8:
                if cls.frost_armor.is_available():
                    cls.frost_armor.cast()
                return True
            time.sleep(0.5)

        return True

    @classmethod
    def attack(cls):
        i = 0
        while WorldData.target_health >= 1 or i > 20:
            WorldData.update()
            if cls.fire_ball.is_in_range():
                pyautogui.press("1")
                if not cls.fire_ball.is_available():
                    time.sleep(2)
                cls.fire_ball.cast()
                time.sleep(float(cls.fire_ball.cast_time))
                continue
            pyautogui.keyDown("w")
            time.sleep(0.1)
            i += 1
            pyautogui.keyUp("w")
        WorldData.in_combat_bot = False
