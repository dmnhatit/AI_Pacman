import pygame as py
import load
from contants import EColor, EScore 
from pacman_agent import Pacman, Target, Wall

class GamePacMan():
    def __init__(self, file_path):
        self.game_board = self.get_maze(file_path)
        self.size = 600
        self.square = self.size/len(self.game_board[0])
        self.screen = py.Surface((self.size, self.size))
        self.start = False
        self.win = False
        self.hero:Pacman = None
        self.targets = []
        self.walls = []
        self.score = 0
        self.message = "Pending"

        self.fetch = True #Fetch command
        self.fetch_F = 1 #F of fetch

        self.set_value()
        self.stop_music()
  
    def display_score(self):
        pass

    def win_game(self):
        self.win = True
        self.start = False
        self.message = "You Win"
        self.stop_music()

    def add_score(self, score: EScore):
        self.score += score.value

    def check_hero_eat_target(self, direction):
        hero_rect = py.Rect(self.hero.x - direction[0]*self.hero.speed, self.hero.y -direction[1]*self.hero.speed, self.hero.size, self.hero.size)
        if len(self.targets) > 0:
            for item in self.targets:
                target_rect = py.Rect(item.x, item.y, item.size, item.size)
                if hero_rect.colliderect(target_rect):
                    self.targets.remove(item)
                    self.score += EScore.TARGET.value
                    print("Founded target")
                    return True
        else:
            self.win_game()
        return False

    def colliderect_wall(self, direction):
        hero_rect = py.Rect(self.hero.x + direction[0]*self.hero.speed, self.hero.y + direction[1]*self.hero.speed, self.hero.size, self.hero.size)
        for item in self.walls:
            wall_rect = py.Rect(item.x, item.y, item.size, item.size)
            if hero_rect.colliderect(wall_rect):
                return True, item        
        return False, None
    
    def controller_move(self):
        keys = py.key.get_pressed()
        self.hero.move_controller(keys)
        if self.check_hero_eat_target(self.hero.position_future):
            self.hero.move_to_location()
        collision_feature, wall = self.colliderect_wall(self.hero.position_future)
        if not collision_feature:
            self.hero.move_to_location()
        else:
            collision, wall = self.colliderect_wall(self.hero.position)
            if not collision:
                self.hero.angel_future = self.hero.angel
                self.hero.position_future = self.hero.position
                self.hero.move_to_location()
            else:
                print(f"Collision with wall at position ({wall.x}, {wall.y})")

    def auto_move(self):
        if self.fetch_F == 0:
            self.fetch = True

        if len(self.hero.locations) > 0 and self.fetch:
            command = self.hero.next_location()
            self.hero.move_command(command)
            self.hero.change_direction()
            self.fetch_F = self.hero.size//self.hero.speed
            self.fetch = False

        elif self.fetch == False:
            self.fetch_F-=1
            self.hero.move()
    
    def events(self):
        if self.hero is not None:
            self.fetch_F = 0
            self.hero.mounth_event()
            if self.start: 
                self.message = "Searching"
                self.controller_move()
                

    def draw(self):
        self.screen.fill(EColor.BLACK.value)

        if len(self.walls) > 0:
            for item in self.walls:
                item.draw()
                self.screen.blit(item.surface, item.surface_rect)

        if len(self.targets) > 0:
            for item in self.targets:
                item.draw()
                self.screen.blit(item.surface, item.surface_rect)
        
        if self.hero is not None:
            self.screen.blit(self.hero.surface, (self.hero.x, self.hero.y))

    def set_value(self): 
        for row in range(len(self.game_board)):
            for col in range(len(self.game_board[0])):
                if self.game_board[row][col] == 0:
                    wall = Wall(col*self.square, row*self.square, self.square, EColor.WALL.value)
                    self.walls.append(wall)
                elif self.game_board[row][col] == 2:
                    target = Target(col*self.square, row*self.square, self.square, EColor.TARGET.value)
                    self.targets.append(target)
        
        self.hero = Pacman(1*self.square, 1*self.square, self.square)

    def get_maze(self, file_path):
        return load.load_maze(file_path)
    
    def play_music(self):
        load.load_mp3("mp3\playing_pacman.mp3")
        py.mixer.music.play()

    def stop_music(self):
        py.mixer.music.stop()  