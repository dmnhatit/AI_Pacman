from enum import Enum

class EColor(Enum):
    BLACK = (0, 0, 0)
    BACKGROUND = (33, 36, 77)
    BUTTON = (74, 38, 171)
    BUTTON_TITLE = (255, 0, 0)
    BUTTON_HOVER = (227, 80, 171)
    TEXT_TITLE = (255, 255, 255)
    PATH = (255, 255, 255)
    WALL = (0, 0, 255)
    BACKGROUND_OBJECT = (0, 0, 0, 0)

class EAngle(Enum):
    NONE = 360
    LEFT = 180
    RIGHT = 0
    UP = 90
    DOWN = -90

class EPosition(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class EScore(Enum):
    TARGET = 500
    STEP = -5