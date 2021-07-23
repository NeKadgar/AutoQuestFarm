from Base.WowWindow import WowWindow
from PIL import ImageGrab, ImageChops
import time
import cv2
import copy
import numpy as np
from Base.display import Display

# display = Display(3840, 2160)
# display = None


class SharkEye(object):
    @staticmethod
    def _get_enemy_cords(image):
        display = Display(3840, 2160)

        image = np.array(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        edged = cv2.Canny(gray, 10, 100)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        cv2.imwrite('./frame2.jpg', closed)

        cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            boxes.append(cv2.boundingRect(c))
        for box in boxes:
            x, y, w, h = box
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # cv2.drawContours(image, contours, -1, (0, 0, 255), 3)
        im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('./frame.jpg', image)
        return boxes

    @classmethod
    def find_movement(cls):
        WowWindow.set_focus()
        image = ImageGrab.grab(WowWindow.get_app_position())
        time.sleep(1)
        image2 = ImageGrab.grab(WowWindow.get_app_position())
        diff = ImageChops.difference(image, image2)
        if diff.getbbox():
            print(cls._get_enemy_cords(diff))
            diff.show()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                pass
