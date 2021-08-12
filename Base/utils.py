import win32api, win32con, win32gui, win32ui
import pydirectinput
import time
from Base.WowWindow import WowWindow


class Commands:
    MARKER = "/targetmarker 6"
    ROTATE = "/run FlipCameraYaw(90)"
    REPOP = "/run RepopMe()"
    RETRIVE = "/run RetrieveCorpse()"


def pretty_print(d, indent=0):
   for key, value in d.items():
      print("{}: {}".format(key, value))


def scalar_mult(a, b, x, y):
    return a * x + b * y


def vector_mult(a, b, x, y):
    return a * y - b * x


def save_cursor_icon(filename):
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


def convert_wowhead_cords(cords):
    cords = cords.split(" ")
    list = []
    for i in range(0, len(cords)//2):
        list.append([float(cords[0]), float(cords[1])])
        cords.pop(0)
        cords.pop(0)
        print(list)


def mouse_drag(x, y, duration):
    t = time.time()
    x_center, y_center = WowWindow.get_center_point()

    pydirectinput.moveTo(x_center, y_center)
    pydirectinput.mouseDown(button="right")
    while time.time() - t < duration:
        pydirectinput.move(50, 0)
        time.sleep(1)
    pydirectinput.mouseUp(button="right")

