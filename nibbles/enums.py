from enum import Enum


class UnitType(Enum):
    SNAKE = 1
    FRUIT = 2


class Color(Enum):
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 255, 255)
    PURPLE = (255, 0, 255)
