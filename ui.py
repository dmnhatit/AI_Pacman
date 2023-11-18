import pygame as py

class Text():
    def __init__(self, title, color, width, height, font: py.font.FontType, background_color = None):
        self.button_title = font.render(title, True, color)
        self.button_title_rect = self.button_title.get_rect()
        self.width = width
        self.height = height
        self.background_color = background_color
        self.surface = None
        self.x = 0
        self.y = 0
    
    def draw(self, surface, x = 0, y = 0):
        self.x = x
        self.y = y
        self.surface = surface

        if self.background_color is not None:
            py.draw.rect(self.surface, self.background_color, [self.x, self.y, self.width, self.height])
        self.button_title_rect = self.button_title.get_rect()
        self.button_title_rect.center = (self.width//2 + self.x, self.height//2 + self.y)
        self.surface.blit(self.button_title, self.button_title_rect)
    
    def set_text(self, text, color, font):
        self.button_title = font.render(text, True, color)


class Button(Text):
    def __init__(self, title, color, width, height, font: py.font.FontType, background_color=None):
        super().__init__(title, color, width, height, font, background_color)
    
    def button_hover_change_color(self, color_new):
        index_mouse =  py.mouse.get_pos()
        if self.x < index_mouse[0] < self.x + self.width and self.y < index_mouse[1] < self.y + self.height:
            py.draw.rect(self.surface, color_new , [self.x, self.y, self.width, self.height])
        else:
            py.draw.rect(self.surface, self.background_color, [self.x, self.y, self.width, self.height])
        
        self.surface.blit(self.button_title, self.button_title_rect)

