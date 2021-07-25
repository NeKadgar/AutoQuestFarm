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
        # WowWindow.set_focus()
        pyautogui.press("tab")
        WorldData.update()
        if WorldData.target_health >= 1:
            pyautogui.press("enter")
            pyautogui.typewrite("/targetmarker 6", interval=0.01)
            pyautogui.press("enter")
            x, y, x1, y1 = WowWindow.get_app_position()
            image = ImageGrab.grab((x, y + 100, x1, y1))
            image = np.array(image)

            low_blue = (0, 100, 255)

            high_blue = (0, 255, 255)

            only_cat = cv2.inRange(image, low_blue, high_blue)
            print(only_cat)
            contours, _ = cv2.findContours(only_cat, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            counturs = sorted(contours, key=cv2.contourArea, reverse=True)
            for contour in counturs:
                cv2.drawContours(image, counturs[0], -1, (255, 0, 255), 3)
                cv2.imshow("Counturs", image)  # рисует рокно с конурами
                # cv2.imshow("Mask", mask)
            # cv2.imshow("ret",ret)
            # cv2.imshow("blur",blurred_frame)
            # key = cv2.waitKey(1)
            # cv2.imshow("", only_cat)
            # cv2.waitKey(0)

    @classmethod
    def set_target(cls):
        WowWindow.set_focus()
        pyautogui.press("tab")
        WorldData.update()
        if WorldData.target_health > 10:
            return True

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
        enemy_box = cls.find_movement()
        if enemy_box is not None:
            x, y, w, h = enemy_box
            pydirectinput.leftClick(x + w // 2, y + w // 2)
            rotation.attack()
