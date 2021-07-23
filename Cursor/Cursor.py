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
    cursors = [{"var": QUEST1, "icon_name": "Quest1"},
               {"var": QUEST0, "icon_name": "Quest0"},
               {"var": QUEST_COMPLETED0, "icon_name": "Quest_Сompleted0"},
               {"var": QUEST_COMPLETED1, "icon_name": "Quest_Сompleted1"}]
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
                        time.sleep(0.05)
                        if cls.get_cursor_type() == "Quest1":
                            pydirectinput.click(button='right')
                            pyautogui.keyUp("w")
                            break
                    pyautogui.keyUp("w")
            if WorldData.quest_completed():
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
