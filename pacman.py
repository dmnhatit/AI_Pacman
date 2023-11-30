import pygame as py
import load
from contants import EPacman, EColor, EScore , EAlgorithm, EStatus
from pacman_agent import Pacman, Target, Wall, Path, DeathPit
from algorithm import *

class GamePacman():
    def __init__(self, file_path):
        self.game_board = self.get_maze(file_path)
        self.size = EPacman.SIZE.value
        self.square = self.size/len(self.game_board[0])
        self.screen = py.Surface((self.size, self.size))
        self.start = False
        self.win = False
        self.hero:Pacman = None
        self.target: Target = None
        self.walls = []
        self.death_pits = []
        self.score = 0
        self.status = EStatus.PENDING.value
        self.algorithm = EAlgorithm.INIT.value
        
        self.commands = []
        self.path_result = []

        self.set_value()
        self.stop_music()
        
    def get_status(self):
        return self.status

    def get_algorithm(self):
        return self.algorithm

    def get_score(self):
        return self.score
    
    def get_screen(self):
        return self.screen
    
    def set_win(self, is_win):
        self.win = is_win
    
    def set_start(self, is_start):
        self.start = is_start
  
    def display_score(self):
        pass

    def win_game(self):
        self.win = True
        self.start = False
        self.status = EStatus.WIN.value
        self.stop_music()

    def lose_game(self):
        self.win = False
        self.start = False
        self.status = EStatus.LOSE.value
        self.stop_music()
        self.commands = []

    def add_score(self, score: EScore):
        self.score += score.value

    def colliderect_target(self, direction):
        hero_rect = py.Rect(self.hero.get_x()*self.hero.get_size() + direction[0]*self.hero.get_speed(), self.hero.get_y()*self.hero.get_size() + direction[1]*self.hero.get_speed(), self.hero.get_size(), self.hero.get_size())
        if self.target is not None:
            target_rect = py.Rect(self.target.get_x()*self.target.get_size(), self.target.get_y()*self.target.get_size(), self.target.get_size(), self.target.get_size())
            if hero_rect.colliderect(target_rect):
                self.target == None
                self.add_score(EScore.TARGET)
                return True
        return False

    def colliderect_death_pit(self, direction):
        hero_rect = py.Rect(self.hero.get_x()*self.hero.get_size() + direction[0]*self.hero.get_speed(), self.hero.get_y()*self.hero.get_size() + direction[1]*self.hero.get_speed(), self.hero.get_size(), self.hero.get_size())
        for item in self.death_pits:
            death_pit = py.Rect(item.get_x()*item.get_size(), item.get_y()*item.get_size(), item.get_size(), item.get_size())
            if hero_rect.colliderect(death_pit):
                self.add_score(EScore.DEATH_PIT)
                return True       
        return False

    def colliderect_wall(self, direction):
        hero_rect = py.Rect(self.hero.get_x()*self.hero.get_size() + direction[0]*self.hero.get_speed(), self.hero.get_y()*self.hero.get_size() + direction[1]*self.hero.get_speed(), self.hero.get_size(), self.hero.get_size())
        for item in self.walls:
            wall_rect = py.Rect(item.get_x()*item.get_size(), item.get_y()*item.get_size(), item.get_size(), item.get_size())
            if hero_rect.colliderect(wall_rect):
                return True       
        return False
    
    def check_move_hero(self):
        self.path_result.append((self.hero.x, self.hero.y))
        if self.colliderect_target(self.hero.position_future):
            self.hero.move_to_location()
            self.win_game()
        elif self.algorithm ==  EAlgorithm.UCS.value and self.colliderect_death_pit(self.hero.position_future):
            self.hero.move_to_location()
        else:
            if not self.colliderect_wall(self.hero.position_future):
                self.hero.move_to_location()
            else:
                if not self.colliderect_wall(self.hero.position):
                    self.hero.angel_future = self.hero.angel
                    self.hero.position_future = self.hero.position
                    self.hero.move_to_location()
    
    def controller_move(self):
        keys = py.key.get_pressed()
        self.hero.move_controller(keys)
        self.check_move_hero()

    def auto_move(self):
        if len(self.commands) > 0:
            command = self.commands.pop(0)
            self.add_score(EScore.STEP)
            self.hero.move_command(command)
            self.check_move_hero()
        else:
            self.commands.clear()
            if self.win == False:
                self.lose_game()
    
    def events(self):
        if self.hero is not None:
            if self.start: 
                self.status = "Searching"
                self.auto_move()
            
    def draw(self):
        self.screen.fill(EColor.BACKGROUND_PACMAN.value)

        if len(self.walls) > 0:
            for item in self.walls:
                item.draw()
                self.screen.blit(item.get_surface(), item.get_surface_rect())

        if self.target is not None:
            self.target.animation_event()
            self.screen.blit(self.target.get_surface(), self.target.get_surface_rect())
        
        if self.hero is not None:
            self.hero.mounth_event()
            self.screen.blit(self.hero.get_surface(), (self.hero.get_x()*self.hero.get_size(), self.hero.get_y()*self.hero.get_size()))
        
        if self.algorithm == EAlgorithm.UCS.value:
            if len(self.death_pits) > 0:
                for item in self.death_pits:
                    item.draw()
                    self.screen.blit(item.get_surface(), item.get_surface_rect())

        if len(self.path_result) > 0:
            for index in self.path_result:
                path = Path(index[0], index[1], self.square,  EColor.PATH.value)
                path.draw()
                self.screen.blit(path.get_surface(), path.get_surface_rect())
        
    def set_value(self): 
        for row in range(len(self.game_board)):
            for col in range(len(self.game_board[0])):
                if self.game_board[row][col] == EPacman.WALL.value:
                    wall = Wall(col, row, self.square, EColor.WALL.value)
                    self.walls.append(wall)

                elif self.game_board[row][col] == EPacman.TARGET.value:
                    self.target = Target(col, row, self.square, EColor.PATH.value)

                elif self.game_board[row][col] == EPacman.PACMAN.value:
                    self.hero = Pacman(col, row, self.square)

                elif self.game_board[row][col] == EPacman.DEATH_PIT.value:
                    death_pit = DeathPit(col, row, self.square)
                    self.death_pits.append(death_pit)

    def get_maze(self, file_path):
        return load.load_maze(file_path)
    
    def get_result(self, algorithm):
        result = Node()
        problem = Problem(self.game_board, (self.hero.y, self.hero.x), (self.target.y, self.target.x))
        if algorithm == EAlgorithm.BFS:
            result = bfs(problem)
        elif algorithm == EAlgorithm.UCS:
            result = ucs(problem)
        elif algorithm == EAlgorithm.DFS:
            result = dfs(problem)
        elif algorithm == EAlgorithm.IDS:
            result = ids(problem)
        elif algorithm == EAlgorithm.ASTAR:
            result = astar(problem)

        self.commands = result.get_directions() if result is not None else []
        if self.commands is not None:
            self.status = EStatus.READY.value
            self.algorithm = algorithm.value

    
    def play_music(self):
        load.load_mp3("mp3\playing_pacman.mp3")
        py.mixer.music.play()

    def stop_music(self):
        py.mixer.music.stop()  