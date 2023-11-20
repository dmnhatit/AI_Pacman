#%%
import pygame as py
import sys
import load
from pacman import GamePacMan
from contants import EColor
import ui

class Game():
    def __init__(self):        
        py.init()
        self.width = 750
        self.height = 600
        self.frame = 10
        self.screen = py.display.set_mode((self.width + self.frame*2, self.height + self.frame*2))
        self.game = None

        py.display.set_caption("Game Pacman")
        self.background_img = py.transform.scale(load.load_img('images\cover.jpg'), (610, 750))
        self.clock = py.time.Clock()
        self.font = py.font.Font(None, 25)

        self.button_width = 140
        self.button_height = 40
        self.button_quit = ui.Button("Quit", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_play = ui.Button("Play", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_start = ui.Button("Start", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_reset = ui.Button("Reset", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_return = ui.Button("Return", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_athgorithm_A_Start = ui.Button("A Start", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_athgorithm_BFS = ui.Button("BFS", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_athgorithm_UCS = ui.Button("UCS", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_athgorithm_DFS = ui.Button("DFS", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.button_athgorithm_IDS = ui.Button("IDS", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value)
        self.text_score = ui.Text("", EColor.TEXT_TITLE.value, self.button_width, self.button_height, self.font, EColor.BLACK.value)
        self.text_message = ui.Text("Peding", EColor.TEXT_TITLE.value, self.button_width, self.button_height, self.font, EColor.BLACK.value)
        self.text_algorithm = ui.Text("None", EColor.TEXT_TITLE.value, self.button_width, self.button_height, self.font, EColor.BLACK.value)

        self.run()

    def run(self):
        running = True
        playgame = False
        while running:
            mouse = py.mouse.get_pos()
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                
                if event.type == py.MOUSEBUTTONDOWN:
                    if self.button_quit.x < mouse[0] < self.button_quit.x + self.button_quit.width and self.button_quit.y < mouse[1] < self.button_quit.y + self.button_quit.height:
                        running = False

                if event.type == py.MOUSEBUTTONDOWN and playgame == False:
                    if self.button_play.x < mouse[0] < self.button_play.x + self.button_play.width and self.button_play.y < mouse[1] < self.button_play.y + self.button_play.height:
                        playgame = True
                        self.game = GamePacMan("input\maze.txt")
                
                if event.type == py.MOUSEBUTTONDOWN and playgame == True:
                    if self.button_return.x < mouse[0] < self.button_return.x + self.button_return.width and self.button_return.y < mouse[1] < self.button_return.y + self.button_return.height:
                        playgame = False
                        self.game.stop_music()
                                
                if event.type == py.MOUSEBUTTONDOWN and playgame == True:
                    if self.button_start.x < mouse[0] < self.button_start.x + self.button_start.width and self.button_start.y < mouse[1] < self.button_start.y + self.button_start.height:
                        self.game.win = False
                        self.game.start = True
                        self.game.play_music()
                                
                if event.type == py.MOUSEBUTTONDOWN and playgame == True:
                    if self.button_reset.x < mouse[0] < self.button_reset.x + self.button_reset.width and self.button_reset.y < mouse[1] < self.button_reset.y + self.button_reset.height:
                        self.game = None

                if event.type == py.MOUSEBUTTONDOWN and playgame == True:
                    if self.button_athgorithm_BFS.x < mouse[0] < self.button_athgorithm_BFS.x + self.button_athgorithm_BFS.width and self.button_athgorithm_BFS.y < mouse[1] < self.button_athgorithm_BFS.y + self.button_athgorithm_BFS.height:
                        self.game.get_result("bfs") 

                if event.type == py.MOUSEBUTTONDOWN and playgame == True:
                    if self.button_athgorithm_UCS.x < mouse[0] < self.button_athgorithm_UCS.x + self.button_athgorithm_UCS.width and self.button_athgorithm_UCS.y < mouse[1] < self.button_athgorithm_UCS.y + self.button_athgorithm_UCS.height:
                        self.game.get_result("ucs")
                        
                if event.type == py.MOUSEBUTTONDOWN and playgame == True:
                    if self.button_athgorithm_DFS.x < mouse[0] < self.button_athgorithm_DFS.x + self.button_athgorithm_DFS.width and self.button_athgorithm_DFS.y < mouse[1] < self.button_athgorithm_DFS.y + self.button_athgorithm_DFS.height:
                        self.game.get_result("dfs")
                        
                if event.type == py.MOUSEBUTTONDOWN and playgame == True:
                    if self.button_athgorithm_IDS.x < mouse[0] < self.button_athgorithm_IDS.x + self.button_athgorithm_IDS.width and self.button_athgorithm_IDS.y < mouse[1] < self.button_athgorithm_IDS.y + self.button_athgorithm_IDS.height:
                        self.game.get_result("ids")

            if playgame == True and self.game is not None:
                self.game.events()
            
            self.draw(playgame)
            py.display.flip()
            self.clock.tick(12)

        py.quit()
        sys.exit()
    
    def draw(self, playgame):
        if playgame:
            self.draw_game()
        else:
            self.draw_main()
            

    def draw_main(self):
        self.screen.fill(EColor.BACKGROUND.value)
        self.screen.blit(self.background_img, (0, -100))

        self.button_quit.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height + self.frame)
        self.button_quit.button_hover_change_color(EColor.BUTTON_HOVER.value)
        self.button_play.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*2)
        self.button_play.button_hover_change_color(EColor.BUTTON_HOVER.value)

    def draw_game(self):
        self.game = GamePacMan("input\maze.txt") if self.game is None else self.game
        self.screen.fill(EColor.BACKGROUND.value)

        if self.game.status == "Pending":
            self.button_athgorithm_BFS.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*5 - self.frame*3)
            self.button_athgorithm_BFS.button_hover_change_color(EColor.BUTTON_HOVER.value)
            self.button_athgorithm_UCS.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*6 - self.frame*4)
            self.button_athgorithm_UCS.button_hover_change_color(EColor.BUTTON_HOVER.value)
            self.button_athgorithm_DFS.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*7 - self.frame*5)
            self.button_athgorithm_DFS.button_hover_change_color(EColor.BUTTON_HOVER.value)
            self.button_athgorithm_IDS.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*8 - self.frame*6)
            self.button_athgorithm_IDS.button_hover_change_color(EColor.BUTTON_HOVER.value)
            self.button_athgorithm_A_Start.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*9 - self.frame*7)
            self.button_athgorithm_A_Start.button_hover_change_color(EColor.BUTTON_HOVER.value)
        
        self.button_start.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*4 - self.frame*2)        
        self.button_start.button_hover_change_color(EColor.BUTTON_HOVER.value)
        self.button_reset.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*3 - self.frame)        
        self.button_reset.button_hover_change_color(EColor.BUTTON_HOVER.value)
        self.button_return.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*2)        
        self.button_return.button_hover_change_color(EColor.BUTTON_HOVER.value)
        self.button_quit.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height + self.frame)
        self.button_quit.button_hover_change_color(EColor.BUTTON_HOVER.value)

        self.text_message.draw(self.screen, self.width - self.button_width + self.frame, 90)   
        self.text_message.set_text(f"[{self.game.status}]", EColor.TEXT_TITLE.value, self.font)
        
        self.text_score.draw(self.screen, self.width - self.button_width + self.frame, 50)   
        self.text_score.set_text(f"[Score: {self.game.score}]", EColor.TEXT_TITLE.value, self.font)

        self.text_algorithm.draw(self.screen, self.width - self.button_width + self.frame, 10)   
        self.text_algorithm.set_text(f"[{self.game.algorithm}]", EColor.TEXT_TITLE.value, self.font)

        self.game.draw()
        self.screen.blit(self.game.screen,(self.frame,self.frame))

if __name__ == "__main__":
    game = Game()
# %%
