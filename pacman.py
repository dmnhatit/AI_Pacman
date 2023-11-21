import pygame as py
import load
from contants import EColor, EScore 
from pacman_agent import Pacman, Target, Wall
from algorithm import *

class GamePacMan():
    def __init__(self, file_path):
        self.game_board = self.get_maze(file_path)
        self.size = 600
        self.square = self.size/len(self.game_board[0])
        self.screen = py.Surface((self.size, self.size))
        self.start = False
        self.win = False
        self.hero:Pacman = None
        self.target: Pacman = None
        self.walls = []
        self.score = 0
        self.status = "Pending"
        self.algorithm = "None"
        
        self.commands = []

        self.set_value()
        self.stop_music()
  
    def display_score(self):
        pass

    def win_game(self):
        self.win = True
        self.start = False
        self.status = "You Win"
        self.stop_music()
        self.commands = None

    def add_score(self, score: EScore):
        self.score += score.value

    def check_hero_eat_target(self, direction):
        hero_rect = py.Rect(self.hero.x*self.hero.size + direction[0]*self.hero.speed, self.hero.y*self.hero.size + direction[1]*self.hero.speed, self.hero.size, self.hero.size)
        if self.target is not None:
            target_rect = py.Rect(self.target.x*self.target.size, self.target.y*self.target.size, self.target.size, self.target.size)
            if hero_rect.colliderect(target_rect):
                self.target == None
                self.score += EScore.TARGET.value
                print("Founded target")
                return True
        return False

    def colliderect_wall(self, direction):
        hero_rect = py.Rect(self.hero.x*self.hero.size + direction[0]*self.hero.speed, self.hero.y*self.hero.size + direction[1]*self.hero.speed, self.hero.size, self.hero.size)
        for item in self.walls:
            wall_rect = py.Rect(item.x*item.size, item.y*item.size, item.size, item.size)
            if hero_rect.colliderect(wall_rect):
                return True, item        
        return False, None
    
    def check_move_hero(self):
        if self.check_hero_eat_target(self.hero.position_future):
            self.hero.move_to_location()
            self.win_game()
        else:
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
    
    def controller_move(self):
        keys = py.key.get_pressed()
        self.hero.move_controller(keys)
        self.check_move_hero()
        

    def auto_move(self):
        if len(self.commands) > 0 and self.commands is not None:
            command = self.commands.pop(0)
            self.add_score(EScore.STEP)
            self.hero.move_command(command)
            self.check_move_hero()
        else:
            self.commands.clear()
    
    def events(self):
        if self.hero is not None:
            self.hero.mounth_event()
            if self.start: 
                self.status = "Searching"
                self.auto_move()
            
    def draw(self):
        self.screen.fill(EColor.BLACK.value)

        if len(self.walls) > 0:
            for item in self.walls:
                item.draw()
                self.screen.blit(item.surface, item.surface_rect)

        if self.target is not None:
            self.target.draw()
            self.screen.blit(self.target.surface, self.target.surface_rect)
        
        if self.hero is not None:
            self.screen.blit(self.hero.surface, (self.hero.x*self.hero.size, self.hero.y*self.hero.size))

    def set_value(self): 
        for row in range(len(self.game_board)):
            for col in range(len(self.game_board[0])):
                if self.game_board[row][col] == 0:
                    wall = Wall(col, row, self.square, EColor.WALL.value)
                    self.walls.append(wall)
                elif self.game_board[row][col] == 2:
                    self.target = Target(col, row, self.square, EColor.TARGET.value)
        
        self.hero = Pacman(1, 1, self.square)

    def get_maze(self, file_path):
        return load.load_maze(file_path)
    
    def get_result(self, algorithm):
        problem = Problem(self.game_board, (self.hero.y, self.hero.x), (self.target.y, self.target.x))
        if algorithm == "bfs":
            self.algorithm = "BFS"
            self.commands = bfs(problem).get_directions()
        elif algorithm == "ucs":
            self.algorithm = "UCS"
            self.commands = ucs(problem).get_directions()
        elif algorithm == "dfs":
            self.algorithm = "DFS"
            self.commands = dfs(problem).get_directions()
        elif algorithm == "ids":
            self.algorithm = "IDS"
            self.commands = ids(problem).get_directions()
    
    def play_music(self):
        load.load_mp3("mp3\playing_pacman.mp3")
        py.mixer.music.play()

    def stop_music(self):
        py.mixer.music.stop()  