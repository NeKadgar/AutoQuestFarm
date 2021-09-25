import win32api, win32con, win32gui, win32ui
from PIL import Image, ImageChops
import os
import pyautogui
import pydirectinput
from Base.WowWindow import WowWindow
from AddonData.WorldData import WorldData, PI2
import time


class Cursor(object):
    QUEST1 = None
    QUEST0 = None
    QUEST_COMPLETED0 = None
    QUEST_COMPLETED1 = None
    ATTACK0 = None
    ATTACK1 = None
    SELLER0 = None
    SELLER1 = None
    AUTOLOOT0 = None
    AUTOLOOT1 = None
    REPAIR0 = None
    REPAIR1 = None

    cursors = [{"var": QUEST1, "icon_name": "Quest1"},
               {"var": QUEST0, "icon_name": "Quest0"},
               {"var": QUEST_COMPLETED0, "icon_name": "Quest_Сompleted0"},
               {"var": QUEST_COMPLETED1, "icon_name": "Quest_Сompleted1"},
               {"var": ATTACK0, "icon_name": "Attack0"},
               {"var": ATTACK1, "icon_name": "Attack1"},
               {"var": SELLER0, "icon_name": "Seller0"},
               {"var": SELLER1, "icon_name": "Seller1"},
               {"var": AUTOLOOT0, "icon_name": "AutoLoot0"},
               {"var": AUTOLOOT1, "icon_name": "AutoLoot1"},
               {"var": REPAIR0, "icon_name": "Repair0"},
               {"var": REPAIR1, "icon_name": "Repair1"}]
    loaded = False

    @classmethod
    def get_path_to_image(cls, image_name):
        path_to_img = os.path.abspath("Cursor/Icons/{}.bmp".format(image_name))
        return path_to_img

    @classmethod
    def get_cursor_icon(cls, icon_name):
        return Image.open(cls.get_path_to_image(icon_name))

    @classmethod
    def load_cursors(cls):
        for cursor in cls.cursors:
            cursor["var"] = cls.get_cursor_icon(cursor["icon_name"])

    @classmethod
    def get_cursor_type(cls):
        try:
            info = win32gui.GetCursorInfo()
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, 32, 32)
            hdc = hdc.CreateCompatibleDC()
            hdc.SelectObject(hbmp)
            hdc.DrawIcon((0, 0), info[1])
            hbmp.SaveBitmapFile(hdc, "bin.bmp")
            current_cursor = Image.open("bin.bmp")
            if not cls.loaded:
                cls.load_cursors()
                cls.loaded = True
            for cursor in cls.cursors:
                result = ImageChops.difference(current_cursor, cursor["var"]).getbbox()
                if result is None:
                    return cursor["icon_name"]
            return None
        except:
            print("Error")
            return None

    @classmethod
    def find_enemy(cls, boxes):
        enemy_boxes = []
        for box in boxes:
            x, y, w, h = box
            pydirectinput.moveTo(int(x + w // 2), int(y + h // 2))
            cursor_type = cls.get_cursor_type()
            if cursor_type == "Attack1":
                return box
            elif cursor_type == "Attack0":
                enemy_boxes.append(box)
        if enemy_boxes:
            return enemy_boxes[0]
        return None

    @classmethod
    def find_lootable(cls, boxes):
        for box in boxes:
            x, y, w, h = box
            pydirectinput.moveTo(int(x + w // 2), int(y + h // 2))
            cursor_type = cls.get_cursor_type()
            if cursor_type == "AutoLoot0":
                x_center, y_center = WowWindow.get_center_point()
                pydirectinput.moveTo(x_center, y_center)
                pydirectinput.mouseDown(button="right")
                pydirectinput.move((x - x_center) // 6)
                pydirectinput.mouseUp(button="right")
                pyautogui.keyDown("w")
                time.sleep(0.5)
                pyautogui.keyUp("w")
                return "again"
            elif cursor_type == "AutoLoot1":
                pydirectinput.rightClick(int(x + w // 2), int(y + h // 2))
                return True
        return False

    @classmethod
    def find_seller(cls):
        x, y = WowWindow.get_center_point()
        pydirectinput.moveTo(x, y)
        for i in range(0, 50):
            for k in range(1, 11):
                pydirectinput.moveTo(x, y // 5 * k)
                if cls.get_cursor_type() == "Repair1" or cls.get_cursor_type() == "Seller1":
                    pydirectinput.click(button='right')
                    return True
                elif cls.get_cursor_type() == "Repair0" or cls.get_cursor_type() == "Seller0":
                    pyautogui.keyDown("w")
                    for j in range(0, 12):
                        time.sleep(0.01)
                        if cls.get_cursor_type() == "Quest1":
                            pydirectinput.click(button='right')
                            pyautogui.keyUp("w")
                            return True
                    pyautogui.keyUp("w")
            pydirectinput.moveTo(x, y)
            pydirectinput.mouseDown(button="right")
            pydirectinput.move(50, 0)
            pydirectinput.mouseUp(button="right")

    @classmethod
    def find_quest(cls):
        x, y = WowWindow.get_center_point()
        pydirectinput.moveTo(x, y)
        for i in range(0, 50):
            for k in range(1, 11):
                pydirectinput.moveTo(x, y // 5 * k)
                if cls.get_cursor_type() == "Quest1" or cls.get_cursor_type() == "Quest_Сompleted1":
                    pydirectinput.click(button='right')
                    break
                elif cls.get_cursor_type() == "Quest0" or cls.get_cursor_type() == "Quest_Сompleted0":
                    pyautogui.keyDown("w")
                    for j in range(0, 12):
                        time.sleep(0.01)
                        if cls.get_cursor_type() == "Quest1":
                            pydirectinput.click(button='right')
                            pyautogui.keyUp("w")
                            break
                    pyautogui.keyUp("w")
            if WorldData.quest_completed():
                print("quest completed")
                return True
            pydirectinput.moveTo(x, y)
            pydirectinput.mouseDown(button="right")
            pydirectinput.move(50, 0)
            pydirectinput.mouseUp(button="right")

    @classmethod
    def save_cursor_icon(cls, filename):
        info = win32gui.GetCursorInfo()
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)

        hdc.DrawIcon((0, 0), info[1])
        hbmp.SaveBitmapFile(hdc, filename)

        win32gui.DestroyIcon(info[1])
        win32gui.DeleteObject(hbmp.GetHandle())
        hdc.DeleteDC()
