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
        point_a, point_b = cls.get_app_position()
        return (point_a[0] + point_b[0]) // 2, (point_a[1] + point_b[1]) // 2