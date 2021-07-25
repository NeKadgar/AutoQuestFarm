import time

from AddonData.WorldData import WorldData
import pyautogui


def stuck_detector():
    cords = []
    i = 0
    while True:
        WorldData.update()
        if not WorldData.in_combat:
            cords.append((WorldData.x, WorldData.y))
            if i == 5:
                if cords[0] == cords[-1]:
                    pyautogui.press("space")
                i = 0
                cords = []
            i += 1
            time.sleep(1)
