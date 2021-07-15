import win32api, win32con, win32gui, win32ui


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
