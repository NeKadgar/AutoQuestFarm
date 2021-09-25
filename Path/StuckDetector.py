import time
import random

from AddonData.WorldData import WorldData
import pyautogui


def stuck_detector():
    cords = []
    buttons = ["a", "d"]
    i = 0
    while True:
        if not (WorldData.in_combat or WorldData.is_busy or WorldData.in_dead_body):
            cords.append((WorldData.x, WorldData.y))
            if i == 5:
                if cords[0] == cords[-1]:
                    print("Stuck")
                    button = random.choice(buttons)
                    pyautogui.keyDown(button)
                    pyautogui.press("space")
                    time.sleep(1.5)
                    pyautogui.keyUp(button)
                i = 0
                cords = []
            i += 1
            time.sleep(1)
