from enum import Enum

class EGame(Enum):
    WIDTH = 770
    HEIGHT = 600
    FRAME = 10
    BUTTON_WIDTH = 160
    BUTTON_HEIGHT = 40
    FONT_SIZE = 25
    COVER_WIDTH = 610
    COVER_HEIGHT = 750

class EPacman(Enum):
    SIZE = 600
    WALL = 0
    TARGET = 2
    PACMAN = 3
    DEATH_PIT = 5
    
class EColor(Enum):
    INIT = (0, 0, 0)
    BACKGROUND = (33, 36, 77)
    BUTTON = (74, 38, 171)
    BUTTON_TITLE = (255, 0, 0)
    BUTTON_HOVER = (227, 80, 171)
    TEXT_TITLE = (255, 255, 255)
    PATH = (255, 255, 255)
    WALL = (70, 70, 255)
    DEATH_PIT = (61, 61, 61)
    BACKGROUND_PACMAN = (0, 0, 0)
    MONITOR = (0, 0, 0)

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
    DEATH_PIT = -200

class EAlgorithm(Enum):
    INIT = "None"
    BFS = "BFS"
    UCS = "UCS" 
    DFS = "DFS"
    IDS = "IDS"
    ASTAR = "A Start"

class EStatus(Enum):
    PENDING = "Pending"
    READY = "Ready"
    SEARCHING = "Searching"
    WIN = "You Win"
    LOSE = "You Lose"

class EMap(Enum):
    INIT = "input\map1.txt"
    MAP_1 = "input\map1.txt"
    MAP_2 = "input\map2.txt"