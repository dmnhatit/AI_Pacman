import pygame as py
import load
from contants import EAngle, EColor, EPosition

class GameObject():
    def __init__(self, x, y, size: int, color = EColor.BLACK.value):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.surface = py.surface.Surface((self.size, self.size))
        self.surface_rect = self.surface.get_rect(center=(self.x*self.size + self.size//2, self.y*self.size + self.size//2))
        self.image = None

    def draw(self):
        self.surface.fill(EColor.BACKGROUND_OBJECT)

    def tick(self):
        pass

    def set_position(self, x, y):
        self.x = x
        self.y = y

class Pacman(GameObject):
    def __init__(self, x, y, size):
        super().__init__(x, y, size)
        self.open = py.transform.scale(load.load_img("images\pacman_open.png"), (size-3, size-3))
        self.close = py.transform.scale(load.load_img("images\pacman_close.png"), (size-3, size-3))
        self.image = self.open
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (self.size//2, self.size//2)
        self.angel = EAngle.RIGHT.value
        self.angel_future = EAngle.RIGHT.value
        self.position = EPosition.RIGHT.value
        self.position_future = EPosition.RIGHT.value
        self.speed = self.size

        self.open_mouth_event = py.USEREVENT + 1
        self.mounth_open = True

    def draw(self):
        self.surface.fill(EColor.BLACK.value)
        self.surface.blit(self.image, self.image_rect)

    def mounth_event(self):
        py.time.set_timer(self.open_mouth_event, 1)
        self.image = self.open if self.mounth_open else self.close
        self.mounth_open = not self.mounth_open
        self.image = py.transform.rotate(self.image, self.angel)
        self.draw()
    
    def move(self):
        x = self.x + self.position[0]
        y = self.y + self.position[1]

        self.x = x if x*self.size>0 and x*self.size<600 else x == 0 if x*self.size>600 else x==600//self.size
        self.y = y if y*self.size>0 and y*self.size<600 else y == 0 if y*self.size>600 else y==600//self.size

    def change_direction(self):
        self.position = self.position_future
        self.angel = self.angel_future
    
    def move_to_location(self):
        self.change_direction()
        self.move()
    
    def move_controller(self, keys):
        if keys[py.K_RIGHT]:
            print("K_RIGHT")
            self.position_future = EPosition.RIGHT.value
            self.angel_future = EAngle.RIGHT.value
        elif keys[py.K_LEFT]:
            print("K_LEFT")
            self.position_future = EPosition.LEFT.value
            self.angel_future = EAngle.LEFT.value
        elif keys[py.K_UP]:
            print("K_UP")
            self.position_future = EPosition.UP.value
            self.angel_future = EAngle.UP.value
        elif keys[py.K_DOWN]:
            print("K_DOWN")
            self.position_future = EPosition.DOWN.value
            self.angel_future = EAngle.DOWN.value
    
    def move_command(self, command):
        if command == "RIGHT":
            self.position_future = EPosition.RIGHT.value
            self.angel_future = EAngle.RIGHT.value
        elif command == "LEFT":
            self.position_future = EPosition.LEFT.value
            self.angel_future = EAngle.LEFT.value
        elif command == "UP":
            self.position_future = EPosition.UP.value
            self.angel_future = EAngle.UP.value
        elif command == "DOWN":
            self.position_future = EPosition.DOWN.value
            self.angel_future = EAngle.DOWN.value

class Target(GameObject):
    def __init__(self, x, y, size, color):
        super().__init__(x, y, size, color)
    
    def draw(self):
        py.draw.circle(self.surface, self.color, (self.size //2, self.size //2), self.size//5)

class Wall(GameObject):
    def __init__(self, x, y, size: int, color=EColor.WALL.value):
        super().__init__(x, y, size, color)

    def draw(self):
       py.draw.circle(self.surface, self.color, (self.size//2, self.size//2), 15.5)