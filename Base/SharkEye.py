import pyautogui
import pydirectinput
from AddonData.WorldData import WorldData
from Base.WowWindow import WowWindow
from PIL import ImageGrab, ImageChops
import time
import cv2
import copy
import numpy as np
from Base.display import Display
from Cursor.Cursor import Cursor
from Base.FightRotation import MageRotation
from Base.utils import Commands
# display = Display(3840, 2160)
# display = None
rotation = MageRotation


class SharkEye(object):
    marker = cv2.imread('./marker.png', 1)

    @staticmethod
    def _get_enemy_cords(image, w_min=40, h_min=40):
        # display = Display(3840, 2160)

        image = np.array(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        edged = cv2.Canny(gray, 10, 150)
        cv2.imwrite('./frame2.jpg', edged)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        # cv2.imwrite('./frame2.jpg', closed)

        cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if w > w_min and h > h_min:
                boxes.append((x, y, w, h))
        x, y = WowWindow.get_center_point()
        y -= 50
        boxes.sort(key=lambda p: (p[0] - x) ** 2 + (p[0] - y) ** 2)
        # for box in boxes:
        #     x, y, w, h = box
        #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        #
        # cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
        # im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite('./frame.jpg', image)
        return boxes

    @classmethod
    def find_movement(cls):
        WowWindow.set_focus()
        image = ImageGrab.grab(WowWindow.get_app_position())
        time.sleep(1)
        image2 = ImageGrab.grab(WowWindow.get_app_position())
        diff = ImageChops.difference(image, image2)
        if diff.getbbox():
            boxes = cls._get_enemy_cords(diff)
            enemy_box = Cursor.find_enemy(boxes)
            return enemy_box

    @classmethod
    def find_target(cls):
        # x, y, x1, y1 = WowWindow.get_app_position()
        # image = ImageGrab.grab((x, y + 100, x1, y1))
        # image = np.array(image)
        #
        # low_blue = (0, 100, 255)
        #
        # high_blue = (0, 255, 255)
        #
        # only_cat = cv2.inRange(image, low_blue, high_blue)
        # contours, _ = cv2.findContours(only_cat, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # contours = sorted(contours, key=cv2.contourArea, reverse=True)
        # x_center, y_center = WowWindow.get_center_point()
        # if contours:
        #     x = contours[0][0][0][0]
        #     pydirectinput.moveTo(x_center, y_center)
        #     pydirectinput.mouseDown(button="right")
        #     pydirectinput.move((x - x_center) // 6)
        #     pydirectinput.mouseUp(button="right")
        #     print("find")
        #     return True
        # else:
        #     x = x_center
        #     return False
        pyautogui.keyDown("a")
        while True:
            pyautogui.press("2")
            WorldData.update()
            if WorldData.action_used:
                pyautogui.keyUp("a")
                return True
            if not WorldData.target_health:
                return True

    @classmethod
    def set_target(cls):
        WowWindow.set_focus()
        pyautogui.press("tab")
        WorldData.update()
        if WorldData.target_health > 10 and WorldData.range_to_target < 45:
            pyautogui.press("enter")
            pyautogui.typewrite(Commands.MARKER, interval=0.01)
            pyautogui.press("enter")

            while not cls.find_target():
                pass
            return True
        return False

    @classmethod
    def find_lootable(cls):
        x, y, x1, y1 = WowWindow.get_app_position()
        image1 = ImageGrab.grab((x, y, x1, y1))
        time.sleep(0.7)
        image2 = ImageGrab.grab((x, y, x1, y1))
        diff = ImageChops.difference(image1, image2)
        if diff.getbbox():
            boxes = cls._get_enemy_cords(diff, 0, 0)
            lootable = Cursor.find_lootable(boxes)
            if lootable == "again":
                cls.find_lootable()
        pass

    @classmethod
    def attack(cls):
        # WorldData.in_combat_bot = True
        rotation.attack()

    @classmethod
    def check_combat(cls):
        if WorldData.in_combat:
            if WorldData.target_health < 10:
                SharkEye.set_target()
            else:
                while cls.find_target():
                    pyautogui.keyDown("a")
                    time.sleep(0.5)
                    pyautogui.keyUp("a")
            SharkEye.attack()