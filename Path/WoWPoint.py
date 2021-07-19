import math


class WoWPoint:
    def __init__(self, id, x=999, y=999):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return "{}.{}".format(self.x, self.y)

    def __eq__(self, other):
        # сравнение двух прямоугольников
        if isinstance(other, WoWPoint):
            return (self.x == other.x and self.y == other.y)

        return NotImplemented
