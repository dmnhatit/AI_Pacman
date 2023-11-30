import pygame as py

class Text():
    def __init__(self, init_text, color, width, height, font: py.font.FontType, background_color = None, border_color = None):
        self.init_text = font.render(init_text, True, color)
        self.init_text_rect = self.init_text.get_rect()
        self.width = width
        self.height = height
        self.background_color = background_color
        self.border_color = border_color
        self.surface = None
        self.x = 0
        self.y = 0
    
    def draw(self, surface, x = 0, y = 0):
        self.x = x
        self.y = y
        self.surface = surface

        if self.border_color is not None:
            py.draw.rect(self.surface, self.border_color, [self.x - 2, self.y - 2, self.width + 4, self.height + 4])
        if self.background_color is not None:
            py.draw.rect(self.surface, self.background_color, [self.x, self.y, self.width, self.height])
        self.init_text_rect = self.init_text.get_rect()
        self.init_text_rect.center = (self.width//2 + self.x, self.height//2 + self.y)
        self.surface.blit(self.init_text, self.init_text_rect)
    
    def set_text(self, text, color, font):
        self.init_text = font.render(text, True, color)


class Button(Text):
    def __init__(self, init_text, color, width, height, font: py.font.FontType, background_color=None, border_color = None):
        super().__init__(init_text, color, width, height, font, background_color, border_color)
    
    def button_hover_change_color(self, change_color):
        index_mouse =  py.mouse.get_pos()
        if self.x < index_mouse[0] < self.x + self.width and self.y < index_mouse[1] < self.y + self.height:
            py.draw.rect(self.surface, change_color , [self.x, self.y, self.width, self.height])
        else:
            py.draw.rect(self.surface, self.background_color, [self.x, self.y, self.width, self.height])
        
        self.surface.blit(self.init_text, self.init_text_rect)