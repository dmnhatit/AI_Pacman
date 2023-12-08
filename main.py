#%%
import pygame as py
import sys
import load
from pacman import GamePacman
from contants import EGame, EColor, EAlgorithm, EStatus, EMap, EMoniter
import ui

class Game():
    def __init__(self):        
        py.init()
        self.width = EGame.WIDTH.value
        self.height = EGame.HEIGHT.value
        self.frame = EGame.FRAME.value
        self.screen = py.display.set_mode((self.width + self.frame*2, self.height + self.frame*2))
        self.game = None
        self.map = EMap.MAP_1

        py.display.set_caption("Game Pacman")
        py.display.set_icon(load.load_img("images\icon.png"))
        self.background_img = py.transform.scale(load.load_img('images\cover.png'), (EGame.COVER_WIDTH.value, EGame.COVER_HEIGHT.value))
        self.clock = py.time.Clock()
        self.font = py.font.Font(None, EGame.FONT_SIZE.value)

        self.chart_result = ui.Chart("Chart Result", self.frame, self.frame, 600, self.font, 50)

        self.button_width = EGame.BUTTON_WIDTH.value
        self.button_height = EGame.BUTTON_HEIGHT.value

        self.button_quit = ui.Button("Quit", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_statistics = ui.Button("Statistics", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_play = ui.Button("Play", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        
        self.button_start = ui.Button("Start", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_reset = ui.Button("Reset", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_return = ui.Button("Return", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        
        self.text_score = ui.Text("", EColor.TEXT_TITLE.value, self.button_width, self.button_height, self.font, EColor.MONITOR.value)
        self.text_message = ui.Text(EStatus.PENDING.value, EColor.TEXT_TITLE.value, self.button_width, self.button_height, self.font, EColor.MONITOR.value)
        self.text_algorithm = ui.Text(EAlgorithm.INIT.value, EColor.TEXT_TITLE.value, self.button_width, self.button_height, self.font, EColor.MONITOR.value)
        self.text_iterations = ui.Text("", EColor.TEXT_TITLE.value, self.button_width, self.button_height, self.font, EColor.MONITOR.value)
        self.text_statistics = ui.Text("", EColor.TEXT_TITLE.value, self.button_width, self.button_height, self.font, EColor.MONITOR.value)

        self.algorithm_menu = False
        self.button_algorithm_menu = ui.Button("Choose Algorithm", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_BFS_athgorithm = ui.Button(EAlgorithm.BFS.value, EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_UCS_athgorithm = ui.Button(EAlgorithm.UCS.value, EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_DFS_athgorithm = ui.Button(EAlgorithm.DFS.value, EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_IDS_athgorithm = ui.Button(EAlgorithm.IDS.value, EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_athgorithm_close = ui.Button("Close Menu", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)

        self.astart_menu = False      
        self.button_astart_menu = ui.Button("Choose A Star", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)

        self.button_euclidean_athgorithm = ui.Button(EAlgorithm.AS_E.value, EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_euclidean_nq_athgorithm = ui.Button(EAlgorithm.AS_ENQ.value, EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_manhattan_athgorithm = ui.Button(EAlgorithm.AS_M.value, EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_angle_euclide_athgorithm = ui.Button(EAlgorithm.AS_AE.value, EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_astar_close = ui.Button("Close Menu", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)

        self.map_menu = False
        self.button_map_menu = ui.Button("Choose Map", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_map_1 = ui.Button("Map 1", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        self.button_map_2 = ui.Button("Map 2", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value) 
        self.button_close_map = ui.Button("Close Menu", EColor.BUTTON_TITLE.value, self.button_width, self.button_height, self.font, EColor.BUTTON.value, EColor.INIT.value)
        
        self.run()

    def run(self):
        running = True
        moniter = EMoniter.MAIN
        while running:
            mouse = py.mouse.get_pos()
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                
                if event.type == py.MOUSEBUTTONDOWN:
                    # Quit
                    if self.button_quit.x < mouse[0] < self.button_quit.x + self.button_quit.width and self.button_quit.y < mouse[1] < self.button_quit.y + self.button_quit.height:
                        running = False

                    if moniter == EMoniter.MAIN:
                        # Play Game
                        if self.button_play.x < mouse[0] < self.button_play.x + self.button_play.width and self.button_play.y < mouse[1] < self.button_play.y + self.button_play.height:
                            moniter = EMoniter.GAME
                        
                        if self.button_statistics.x < mouse[0] < self.button_statistics.x + self.button_statistics.width and self.button_statistics.y < mouse[1] < self.button_statistics.y + self.button_statistics.height:
                            moniter = EMoniter.CHART

                    elif moniter == EMoniter.GAME:
                        # Open Algorithm Menu
                        if self.algorithm_menu and self.game.status == EStatus.PENDING.value:
                            if self.button_athgorithm_close.x < mouse[0] < self.button_athgorithm_close.x + self.button_athgorithm_close.width and self.button_athgorithm_close.y < mouse[1] < self.button_athgorithm_close.y + self.button_athgorithm_close.height:
                                self.algorithm_menu = False
                                self.astart_menu = False
                                self.map_menu = False
                        
                            elif self.button_BFS_athgorithm.x < mouse[0] < self.button_BFS_athgorithm.x + self.button_BFS_athgorithm.width and self.button_BFS_athgorithm.y < mouse[1] < self.button_BFS_athgorithm.y + self.button_BFS_athgorithm.height:
                                self.game.get_result(EAlgorithm.BFS) 

                            elif self.button_UCS_athgorithm.x < mouse[0] < self.button_UCS_athgorithm.x + self.button_UCS_athgorithm.width and self.button_UCS_athgorithm.y < mouse[1] < self.button_UCS_athgorithm.y + self.button_UCS_athgorithm.height:
                                self.game.get_result(EAlgorithm.UCS)
                                    
                            elif self.button_DFS_athgorithm.x < mouse[0] < self.button_DFS_athgorithm.x + self.button_DFS_athgorithm.width and self.button_DFS_athgorithm.y < mouse[1] < self.button_DFS_athgorithm.y + self.button_DFS_athgorithm.height:
                                self.game.get_result(EAlgorithm.DFS)
                                    
                            elif self.button_IDS_athgorithm.x < mouse[0] < self.button_IDS_athgorithm.x + self.button_IDS_athgorithm.width and self.button_IDS_athgorithm.y < mouse[1] < self.button_IDS_athgorithm.y + self.button_IDS_athgorithm.height:
                                self.game.get_result(EAlgorithm.IDS)
                        else:
                            if self.button_algorithm_menu.x < mouse[0] < self.button_algorithm_menu.x + self.button_algorithm_menu.width and self.button_algorithm_menu.y < mouse[1] < self.button_algorithm_menu.y + self.button_algorithm_menu.height:
                                self.algorithm_menu = True
                                self.astart_menu = False
        
                        # Open A Start Menu
                        if self.astart_menu and self.game.status == EStatus.PENDING.value:
                            if self.button_astar_close.x < mouse[0] < self.button_astar_close.x + self.button_astar_close.width and self.button_astar_close.y < mouse[1] < self.button_astar_close.y + self.button_astar_close.height:
                                self.astart_menu = False
                                self.map_menu = False
                                self.algorithm_menu = False
                            if self.button_euclidean_athgorithm.x < mouse[0] < self.button_euclidean_athgorithm.x + self.button_euclidean_athgorithm.width and self.button_euclidean_athgorithm.y < mouse[1] < self.button_euclidean_athgorithm.y + self.button_euclidean_athgorithm.height:
                                self.game.get_result(EAlgorithm.AS_E)
                            if self.button_euclidean_nq_athgorithm.x < mouse[0] < self.button_euclidean_nq_athgorithm.x + self.button_euclidean_nq_athgorithm.width and self.button_euclidean_nq_athgorithm.y < mouse[1] < self.button_euclidean_nq_athgorithm.y + self.button_euclidean_nq_athgorithm.height:
                                self.game.get_result(EAlgorithm.AS_ENQ)
                            if self.button_manhattan_athgorithm.x < mouse[0] < self.button_manhattan_athgorithm.x + self.button_manhattan_athgorithm.width and self.button_manhattan_athgorithm.y < mouse[1] < self.button_manhattan_athgorithm.y + self.button_manhattan_athgorithm.height:
                                self.game.get_result(EAlgorithm.AS_M)
                            if self.button_angle_euclide_athgorithm.x < mouse[0] < self.button_angle_euclide_athgorithm.x + self.button_angle_euclide_athgorithm.width and self.button_angle_euclide_athgorithm.y < mouse[1] < self.button_angle_euclide_athgorithm.y + self.button_angle_euclide_athgorithm.height:
                                self.game.get_result(EAlgorithm.AS_AE)
                        else:
                            if self.button_astart_menu.x < mouse[0] < self.button_astart_menu.x + self.button_astart_menu.width and self.button_astart_menu.y < mouse[1] < self.button_astart_menu.y + self.button_astart_menu.height:
                                self.astart_menu = True
                                self.algorithm_menu = False  

                        # Open Map Menu
                        if self.map_menu and self.game.status == EStatus.PENDING.value:
                            if self.button_close_map.x < mouse[0] < self.button_close_map.x + self.button_close_map.width and self.button_close_map.y < mouse[1] < self.button_close_map.y + self.button_close_map.height:
                                self.map_menu = False
                                self.astart_menu = False
                                self.algorithm_menu = False
                            
                            elif self.button_map_1.x < mouse[0] < self.button_map_1.x + self.button_map_1.width and self.button_map_1.y < mouse[1] < self.button_map_1.y + self.button_map_1.height:
                                if self.map != EMap.MAP_1:
                                    self.chart_result.clear_data()
                                    self.map = EMap.MAP_1 
                                    self.game = GamePacman(self.map.value)
                                
                            elif self.button_map_2.x < mouse[0] < self.button_map_2.x + self.button_map_2.width and self.button_map_2.y < mouse[1] < self.button_map_2.y + self.button_map_2.height:
                                if self.map != EMap.MAP_2:
                                    self.chart_result.clear_data()
                                    self.map = EMap.MAP_2 
                                    self.game = GamePacman(self.map.value)
                        else:
                            if self.button_map_menu.x < mouse[0] < self.button_map_menu.x + self.button_map_menu.width and self.button_map_menu.y < mouse[1] < self.button_map_menu.y + self.button_map_menu.height:
                                self.map_menu = True

                        if self.game.status != EStatus.PENDING.value:
                            # Reset
                            if self.button_reset.x < mouse[0] < self.button_reset.x + self.button_reset.width and self.button_reset.y < mouse[1] < self.button_reset.y + self.button_reset.height:
                                self.game = None 
                            
                            # Start
                            if self.button_start.x < mouse[0] < self.button_start.x + self.button_start.width and self.button_start.y < mouse[1] < self.button_start.y + self.button_start.height:
                                self.game.set_win(False)
                                self.game.set_start(True)
                                self.game.play_music() 

                        # Return
                        if self.button_return.x < mouse[0] < self.button_return.x + self.button_return.width and self.button_return.y < mouse[1] < self.button_return.y + self.button_return.height:
                            moniter = EMoniter.MAIN
                            self.game.stop_music()
                            self.game = None

                    elif moniter == EMoniter.CHART:
                        if self.button_return.x < mouse[0] < self.button_return.x + self.button_return.width and self.button_return.y < mouse[1] < self.button_return.y + self.button_return.height:
                            moniter = EMoniter.MAIN
                        
                        if self.button_reset.x < mouse[0] < self.button_reset.x + self.button_reset.width and self.button_reset.y < mouse[1] < self.button_reset.y + self.button_reset.height:
                            self.chart_result.clear_data()
          
            if self.game is not None:
                if moniter == EMoniter.GAME:
                    self.game.events()

                if self.game.get_status() == EStatus.WIN.value:
                    self.chart_result.add_data(self.game.get_algorithm().name, self.game.get_score())
            
            self.draw(moniter)
            py.display.flip()
            self.clock.tick(10)

        py.quit()
        sys.exit()
    
    def draw(self, moniter: EMoniter):
        if moniter == EMoniter.MAIN:
            self.draw_main()
        elif moniter == EMoniter.GAME:
            self.draw_game()
        elif moniter == EMoniter.CHART:
            self.draw_chart()
        
    def draw_main(self):
        self.screen.fill(EColor.BACKGROUND_TYPE1.value)
        py.draw.rect(self.screen, EColor.BACKGROUND_TYPE3.value, [15-4, 150-4, EGame.COVER_WIDTH.value + 30 + 4, EGame.COVER_HEIGHT.value + 60 + 4])
        py.draw.rect(self.screen, EColor.BACKGROUND_TYPE4.value, [15, 150, EGame.COVER_WIDTH.value + 30 + 4, EGame.COVER_HEIGHT.value + 60 + 4])
        py.draw.rect(self.screen, EColor.BACKGROUND_TYPE2.value, [15, 150, EGame.COVER_WIDTH.value + 30, EGame.COVER_HEIGHT.value + 60])
        
        self.screen.blit(self.background_img, (30, 180))

        self.button_quit.draw(self.screen, 315, 520)
        self.button_quit.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_2.value)
        self.button_statistics.draw(self.screen, 315, 470)
        self.button_statistics.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_play.draw(self.screen, 315, 420)
        self.button_play.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)

    def draw_game(self):
        self.game = GamePacman(self.map.value) if self.game is None else self.game
        self.screen.fill(EColor.BACKGROUND_TYPE1.value)

        if self.game.status == EStatus.PENDING.value:
            if self.astart_menu:
                self.draw_astar_menu()
            elif self.algorithm_menu:
                self.draw_algorithm_menu()
            elif self.map_menu:
                self.draw_map_menu()
            else:
                self.button_map_menu.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*4 - self.frame*2)        
                self.button_map_menu.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
                self.button_algorithm_menu.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*3 - self.frame)        
                self.button_algorithm_menu.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        else:
            self.button_start.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*4 - self.frame*2)        
            self.button_start.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
            self.button_reset.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*3 - self.frame)        
            self.button_reset.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        
        self.button_return.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*2)        
        self.button_return.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_2.value)
        self.button_quit.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height + self.frame)
        self.button_quit.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_2.value)

        self.text_message.draw(self.screen, self.width - self.button_width + self.frame, 10)   
        self.text_message.set_text(f"[{self.game.get_status()}]", EColor.TEXT_TITLE.value, self.font)
        
        self.text_algorithm.draw(self.screen, self.width - self.button_width + self.frame, 50)   
        self.text_algorithm.set_text(f"[{self.game.get_algorithm().value}]", EColor.TEXT_TITLE.value, self.font)

        self.text_score.draw(self.screen, self.width - self.button_width + self.frame, 90)   
        self.text_score.set_text(f"[Score: {self.game.get_score()}]", EColor.TEXT_TITLE.value, self.font)

        if self.game.get_iterations() is not None:
            self.text_iterations.draw(self.screen, self.width - self.button_width + self.frame, 130)   
            self.text_iterations.set_text(f"[Closed Node: {self.game.get_iterations()}]", EColor.TEXT_TITLE.value, self.font)

        self.game.draw()
        self.screen.blit(self.game.get_screen(),(self.frame,self.frame))
    
    def draw_algorithm_menu(self):
        self.button_athgorithm_close.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*3 - self.frame)
        self.button_athgorithm_close.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_2.value)
        self.button_BFS_athgorithm.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*4 - self.frame*2)
        self.button_BFS_athgorithm.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_UCS_athgorithm.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*5 - self.frame*3)
        self.button_UCS_athgorithm.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_DFS_athgorithm.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*6 - self.frame*4)
        self.button_DFS_athgorithm.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_IDS_athgorithm.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*7 - self.frame*5)
        self.button_IDS_athgorithm.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_astart_menu.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*8 - self.frame*6)
        self.button_astart_menu.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)

    def draw_astar_menu(self):
        self.button_astar_close.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*3 - self.frame)
        self.button_astar_close.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_2.value)
        self.button_euclidean_athgorithm.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*4 - self.frame*2)
        self.button_euclidean_athgorithm.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_euclidean_nq_athgorithm.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*5 - self.frame*3)
        self.button_euclidean_nq_athgorithm.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_manhattan_athgorithm.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*6 - self.frame*4)
        self.button_manhattan_athgorithm.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_angle_euclide_athgorithm.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*7 - self.frame*5)
        self.button_angle_euclide_athgorithm.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
    
    def draw_map_menu(self):
        self.button_close_map.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*3 - self.frame)
        self.button_close_map.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_2.value)
        self.button_map_1.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*4 - self.frame*2)
        self.button_map_1.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_map_2.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*5 - self.frame*3)
        self.button_map_2.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)

    def draw_chart(self):
        self.screen.fill(EColor.BACKGROUND_TYPE1.value)

        self.text_statistics.draw(self.screen, self.width - self.button_width + self.frame, 10)   
        self.text_statistics.set_text(f"[{self.map.name}]", EColor.TEXT_TITLE.value, self.font)

        self.button_reset.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*3 - self.frame)        
        self.button_reset.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_1.value)
        self.button_return.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height*2)        
        self.button_return.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_2.value)
        self.button_quit.draw(self.screen, self.width - self.button_width + self.frame, self.height - self.button_height + self.frame)
        self.button_quit.button_hover_change_color(EColor.BUTTON_HOVER_TYPE_2.value)

        self.chart_result.draw()
        self.screen.blit(self.chart_result.surface, (self.frame, self.frame))

if __name__ == "__main__":
    game = Game()
    # %%
