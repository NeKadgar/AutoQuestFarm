import pywinauto
from pywinauto.application import Application

# from pywinauto import Desktop
# windows = Desktop(backend="uia").windows()
# print([w.window_text() for w in windows])


class WowWindow(object):
    TITLE = "World of Warcraft"
    # TITLE = ""
    app = Application().connect(title=TITLE, found_index=0)


    @classmethod
    def get_app_position(cls):
        func = getattr(cls.app, cls.TITLE)  # self.app.TITLE
        position = func.rectangle()
        position = [position.left, position.top, position.right, position.bottom]
        return position

    @classmethod
    def set_focus(cls):
        getattr(cls.app, cls.TITLE).SetFocus()

    @classmethod
    def get_center_point(cls):
        x1, y1, x2, y2 = cls.get_app_position()
        return (x1 + x2) // 2, (y1 + y2) // 2