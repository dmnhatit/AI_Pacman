import pygame as py
from contants import EColor, EChart

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

class Chart():
    def __init__(self, caption, x, y, size, font: py.font.FontType, frame, axis_color = EColor.CHART_AXIS.value, columns_color = EColor.CHART_COLUMNS.value):
        self.x = x
        self.y = y
        self.datas = []
        self.columns = []
        self.size = size
        self.font = font
        self.caption = Text(caption, EColor.CHART_CAPTION.value, self.size, 40, self.font)
        self.frame = frame
        self.axis_color = axis_color
        self.columns_color = columns_color
        self.surface =  py.surface.Surface((size, size))
        self.surface_rect = self.surface.get_rect()
        self.surface_rect.center = (size//2, size//2)
    
    def add_data(self, column_name, data):
        if column_name in self.columns:
            index = self.columns.index(column_name)
            self.datas[index] = data
        else:
            self.datas.append(data)
            self.columns.append(column_name)
    
    def clear_data(self):
        self.datas = []
        self.columns = []
    
    def draw(self):
        self.surface.fill(EColor.INIT.value)

        column_size = EChart.COLUMN_SIZE.value
        margin = EChart.COLUMN_MARGIN.value
        column_index = self.frame + margin

        is_negative = - min(self.datas) + 10 if len(self.datas) > 0 and min(self.datas)<0 else 0
        value_unit = float((self.size - 10 - self.frame*2)/(max(self.datas)+is_negative)) if len(self.datas) > 0 else 1
        
        py.draw.line(self.surface, self.axis_color, (self.frame, self.size - self.frame), (self.size - self.frame, self.size - self.frame), 2)
        py.draw.line(self.surface, self.axis_color, (self.frame, self.frame), (self.frame, self.size - self.frame), 2)

        for index in range(len(self.datas)):
            value = self.datas[index]
            py.draw.rect(self.surface, self.columns_color, (column_index, self.size - self.frame - value*value_unit - is_negative*value_unit, column_size, value*value_unit + is_negative*value_unit))
            column_name = self.columns[index]
            label = self.font.render(column_name, True, self.axis_color)
            self.surface.blit(label, (column_index + column_size//2 - label.get_width()//2, self.size - self.frame + 10))
            label_value = self.font.render(str(value), True, self.axis_color)
            self.surface.blit(label_value, (column_index + column_size//2 - label_value.get_width()//2, self.size - self.frame - value*value_unit - 20 - is_negative*value_unit))
            column_index += (column_size + margin)