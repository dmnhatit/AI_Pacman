#%%
import pygame
import sys
from ui import Chart

pygame.init()

# Cài đặt cửa sổ
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Đồ Thị Cột với Nhãn Trục X")

# Dữ liệu đồ thị (ví dụ)
data_values = [50, 120, 200, 80, 160]

# Nhãn trục x
variable_names = ['A', 'B', 'C', 'D', 'E']

# Kích thước cột
bar_width = 50
bar_gap = 20

# Màu sắc
bar_color = (0, 0, 255)
axis_color = (0, 0, 0)

font = pygame.font.Font(None, 25)

chart = Chart("", 0, 0, 600, font, 50)
chart.datas = data_values
chart.columns = variable_names

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    chart.draw()
    screen.blit(chart.surface, (0,0))

    # Xóa màn hình
    # screen.fill((255, 255, 255))

    # # Vẽ trục x và y
    # pygame.draw.line(screen, axis_color, (50, height - 50), (width - 50, height - 50), 2)  # Trục x
    # pygame.draw.line(screen, axis_color, (50, height - 50), (50, 50), 2)  # Trục y

    # # Vẽ các cột và nhãn trục x
    # x = 50
    # for i, value in enumerate(data_values):
    #     pygame.draw.rect(screen, bar_color, (x + 100 , height - value - 50, bar_width, value))
    #     font = pygame.font.Font(None, 36)
    #     label = font.render(variable_names[i], True, axis_color)
    #     screen.blit(label, (x + bar_width // 2 - label.get_width() // 2, height - 30))
    #     x += bar_width + bar_gap

    # Cập nhật màn hình
    pygame.display.flip()

# %%
