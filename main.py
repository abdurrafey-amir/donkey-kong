import random
import pygame
import os


# general setup
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width // 2, screen_height - 200 
window = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# variables
section_width = window_width // 32
section_height = window_height // 32
slope = section_height // 8

start_y = window_height - (section_height * 2)
row2_y = start_y - (section_height * 4)
row3_y = row2_y - 7 * slope - 3 * section_height
row4_y = row3_y - (section_height * 4)
row5_y = row4_y - 7 * slope - 3 * section_height
row6_y = row5_y - (section_height * 4)

row1_top = start_y - (slope * 5)
row2_top = row2_y - (slope * 8)
row3_top = row3_y - (slope * 8)
row4_top = row4_y - (slope * 8)
row5_top = row5_y - (slope * 8)
row6_top = row6_y - (slope * 4)

# levels
levels = [
    {'bridges': [
        (1, start_y, 15), (16, start_y - slope, 3),
        (19, start_y - 2 * slope, 3), (22, start_y - 3 * slope, 3),
        (25, start_y - 4 * slope, 3), (28, start_y - 5 * slope, 3),
        (25, row2_y, 3), (22, row2_y - slope, 3),
        (19, row2_y - 2 * slope, 3), (16, row2_y - 3 * slope, 3),
        (13, row2_y - 4 * slope, 3), (10, row2_y - 5 * slope, 3),
        (7, row2_y - 6 * slope, 3), (4, row2_y - 7 * slope, 3),
        (2, row2_y - 8 * slope, 2), (4, row3_y, 3),
        (7, row3_y - slope, 3), (10, row3_y - 2 * slope, 3),
        (13, row3_y - 3 * slope, 3), (16, row3_y - 4 * slope, 3),
        (19, row3_y - 5 * slope, 3), (22, row3_y - 6 * slope, 3),
        (25, row3_y - 7 * slope, 3), (28, row3_y - 8 * slope, 2),
        (25, row4_y, 3), (22, row4_y - slope, 3),
        (19, row4_y - 2 * slope, 3), (16, row4_y - 3 * slope, 3),
        (13, row4_y - 4 * slope, 3), (10, row4_y - 5 * slope, 3),
        (7, row4_y - 6 * slope, 3), (4, row4_y - 7 * slope, 3),
        (2, row4_y - 8 * slope, 2), (4, row5_y, 3),
        (7, row5_y - slope, 3), (10, row5_y - 2 * slope, 3),
        (13, row5_y - 3 * slope, 3), (16, row5_y - 4 * slope, 3),
        (19, row5_y - 5 * slope, 3), (22, row5_y - 6 * slope, 3),
        (25, row5_y - 7 * slope, 3), (28, row5_y - 8 * slope, 2),
        (25, row6_y, 3), (22, row6_y - slope, 3),
        (19, row6_y - 2 * slope, 3), (16, row6_y - 3 * slope, 3),
        (2, row6_y - 4 * slope, 14), (13, row6_y - 4 * section_height, 6),
        (10, row6_y - 3 * section_height, 3)
        ],
    'ladders': [
        (12, row2_y + 6 * slope, 2), (12, row2_y + 26 * slope, 2),
        (25, row2_y + 11 * slope, 4), (6, row3_y + 11 * slope, 3),
        (14, row3_y + 8 * slope, 4), (10, row4_y + 6 * slope, 1),
        (10, row4_y + 24 * slope, 2), (16, row4_y + 6 * slope, 5),
        (25, row4_y + 9 * slope, 4), (6, row5_y + 11 * slope, 3),
        (11, row5_y + 8 * slope, 4), (23, row5_y + 4 * slope, 1),
        (23, row5_y + 24 * slope, 2), (25, row6_y + 9 * slope, 4),
        (13, row6_y + 5 * slope, 2), (13, row6_y + 25 * slope, 2),
        (18, row6_y - 27 * slope, 4), (12, row6_y - 17 * slope, 2),
        (10, row6_y - 17 * slope, 2), (12, -5, 13), (10, -5, 13)
        ],
}]

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

# class
class Platform:
    
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw()

    def draw(self):
        line_width = 7
        platform_color = red
        
        for i in range(self.length):
            bottom_coord = self.y_pos + section_height
            top_coord = self.y_pos
            x_coord = self.x_pos + (i * section_width)
            mid_coord = x_coord + (section_width // 2)
            right_coord = x_coord + section_width

            # drawing lines
            pygame.draw.line(window, platform_color, (x_coord, top_coord), (right_coord, top_coord), line_width)
            pygame.draw.line(window, platform_color, (x_coord, bottom_coord), (right_coord, bottom_coord), line_width)
            pygame.draw.line(window, platform_color, (mid_coord, top_coord), (right_coord, bottom_coord), line_width)
            pygame.draw.line(window, platform_color, (x_coord, bottom_coord), (mid_coord, top_coord), line_width)

        # for collisions
        top_surface = pygame.rect.FRect((self.x_pos, self.y_pos), (self.length * section_width, 2))
        pygame.draw.rect(window, blue, top_surface) 


            
            

# functions
def draw_screen():
    platforms = [(7, 300, 15)]
    ladders = []
    platform_objs = []

    for platform in platforms:
        platform_objs.append(Platform(*platform))


# main loop
running = True
while running:
    clock.tick(60)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw
    window.fill(black)
    draw_screen()

    pygame.display.flip()

pygame.quit()