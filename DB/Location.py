from PIL import Image
import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from Path.WoWPoint import WoWPoint
from Path.PlayerDirection import move_by_points
from Base.WowWindow import WowWindow
from DB.PointsDB import get_location_points
from shapely.geometry.polygon import Polygon
import numpy as np
from DB.Units import Units


class Location(object):
    locations = {
        697687: "Elvynn_Forest"
    }

    @classmethod
    def get_location(cls, numbers):
        return cls.locations[numbers]

    @classmethod
    def show_map(cls, numbers):
        map_name = "{}.jpg".format(cls.get_location(numbers))
        path_to_img = os.path.abspath("DB/maps/{}".format(map_name))
        img = cv2.imread(path_to_img)
        height, width, _c = img.shape
        scale_height = height / 100
        scale_width = width / 100
        cv2.circle(img, (int(scale_width * 52.35), int(scale_height * 45.72)), 1, (0, 255, 0), -1)
        img = cv2.resize(img, (3840, 2160))
        imgplot = plt.imshow(img)

        def onclick(event):
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            if event.button == 2:
                cv2.circle(img, (int(event.xdata), int(event.ydata)), 1, (0, 255, 0), -1)
                imgplot.set_data(img)
                plt.pause(1)

        cid = imgplot.figure.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

    @classmethod
    def show_points_on_map(cls, numbers):
        map_name = "{}.jpg".format(cls.get_location(numbers))
        path_to_img = os.path.abspath("DB/maps/{}".format(map_name))
        img = cv2.imread(path_to_img)
        height, width, _c = img.shape
        scale_height = height / 100
        scale_width = width / 100
        points = get_location_points(numbers)
        for point in points:
            cv2.circle(img, (int(scale_width * point.x), int(scale_height * point.y)), 1, (0, 255, 0), -1)
        img = cv2.resize(img, (3840, 2160))
        imgplot = plt.imshow(img)
        plt.show()

    @classmethod
    def set_polygon(cls, numbers):
        name = input("Название: ")
        map_name = "{}.jpg".format(cls.get_location(numbers))
        path_to_img = os.path.abspath("DB/maps/{}".format(map_name))
        img = cv2.imread(path_to_img)
        height, width, _c = img.shape
        print(height, width, _c)
        scale_height = height / 100
        scale_width = width / 100
        points = get_location_points(numbers)
        for point in points:
            cv2.circle(img, (int(scale_width * point.x), int(scale_height * point.y)), 1, (0, 255, 0), -1)
        imgplot = plt.imshow(img)
        polygon_points = []

        def onclick(event):
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            if event.button == 2:
                cv2.circle(img, (int(event.xdata), int(event.ydata)), 3, (255, 0, 0), -1)
                polygon_points.append(WoWPoint(000, float(event.xdata/scale_width), float(event.ydata/scale_height)))
                imgplot.set_data(img)
                plt.pause(1)
            if event.button == 3:
                pts = np.array([[p.x*scale_width, p.y*scale_height] for p in polygon_points], np.int32)

                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, (255, 0, 0, 10), 3)
                polygon = Polygon([[p.x, p.y] for p in polygon_points])
                print(polygon.wkt)
                imgplot.set_data(img)
                plt.pause(1)
                save = input("Сохранить {} y/n?".format(name))
                if save == "y":
                    Units.update(name, [[p.x, p.y] for p in polygon_points])
                    print("Saved please close window.")
                    plt.clf()
        cid = imgplot.figure.canvas.mpl_connect('button_press_event', onclick)

        plt.show()

    @classmethod
    def show_path_on_map(cls, numbers, points):
        map_name = "{}.jpg".format(cls.get_location(numbers))
        path_to_img = os.path.abspath("DB/maps/{}".format(map_name))
        img = cv2.imread(path_to_img)
        height, width, _c = img.shape
        scale_height = height / 100
        scale_width = width / 100
        for point in points:
            cv2.circle(img, (int(scale_width * point[0]), int(scale_height * point[1])), 1, (255, 0, 0), -1)
        point = points[-1]
        img = cv2.resize(img, (3840, 2160))
        imgplot = plt.imshow(img)
        plt.show()


    @classmethod
    def set_path_on_map(cls, numbers):
        map_name = "{}.jpg".format(cls.get_location(numbers))
        path_to_img = os.path.abspath("DB/maps/{}".format(map_name))
        img = cv2.imread(path_to_img)

        img = cv2.resize(img, (3840, 2160))
        height, width, _c = img.shape
        scale_height = height / 100
        scale_width = width / 100
        cv2.circle(img, (int(scale_width * 52.35), int(scale_height * 45.72)), 1, (0, 255, 0), -1)

        imgplot = plt.imshow(img)
        _path = []

        def onclick(event):
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            if event.button == 2:
                cv2.circle(img, (int(event.xdata), int(event.ydata)), 1, (0, 255, 0), -1)
                _path.append(WoWPoint(int(event.xdata/scale_width), int(event.ydata/scale_height)))
                print(_path)
                imgplot.set_data(img)
                plt.pause(1)

            if event.button == 3:
                plt.clf()
                WowWindow.set_focus()
                move_by_points(_path)

        cid = imgplot.figure.canvas.mpl_connect('button_press_event', onclick)
        plt.show()

