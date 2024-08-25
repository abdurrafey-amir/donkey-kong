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

# colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# class
class Bridge:
    
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
            
            

# functions
def draw_screen():
    platforms = []
    ladders = []


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


    pygame.display.flip()

pygame.quit()