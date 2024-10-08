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

barrel_spawn_time = 360
barrel_count = barrel_spawn_time / 2
barrel_time = 360

fireball_trigger = False

counter = 0


# levels
active_level = 0
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
light_blue = pygame.Color('light blue')


# images
barrel_image = pygame.image.load('assets/barrel.png')
barrel_image = pygame.transform.scale(barrel_image, (section_width * 1.5, section_height * 2))
fire_image = pygame.image.load('assets/fire.png')
fire_image = pygame.transform.scale(fire_image, (section_width * 2, section_height))

# font
font = pygame.font.Font('freesansbold.ttf', 25)

# classes
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
        top_surface = pygame.rect.Rect((self.x_pos, self.y_pos), (self.length * section_width, 2))
        # pygame.draw.rect(window, blue, top_surface) 
        
        return top_surface

class Ladder:

    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()

    def draw(self):
        line_width = 3
        ladder_color = light_blue
        ladder_height = 0.6
        
        for i in range(self.length):
            top_coord = self.y_pos + ladder_height * section_height * i
            bottom_coord = top_coord + ladder_height * section_height
            mid_coord = (ladder_height / 2) * section_height + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + section_width
            
            pygame.draw.line(window, ladder_color, (left_coord, top_coord), (left_coord, bottom_coord), line_width)
            pygame.draw.line(window, ladder_color, (right_coord, top_coord), (right_coord, bottom_coord), line_width)
            pygame.draw.line(window, ladder_color, (left_coord, mid_coord), (right_coord, mid_coord), line_width)
        
        body = pygame.rect.Rect((self.x_pos, self.y_pos - section_height), (section_width, (ladder_height * self.length + section_height)))
        return body
            

barrels = pygame.sprite.Group()
oil_drum = pygame.rect.Rect((0, 0), (0, 0))

class Barrel(pygame.sprite.Sprite):
    
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_frect(center=(x_pos, y_pos))
        self.x_change = 1
        self.y_change = 0
        self.pos = 0
        self.count = 0
        self.oil_collision = False
        self.falling = False
        self.check_lad = False
        self.bottom = self.rect.bottom

    
    def draw(self):
        window.blit(pygame.transform.rotate(barrel_image, 90 * self.pos), self.rect.topleft)

    def check_fall(self):
        already_collided = False
        below = pygame.rect.Rect((self.rect[0], self.rect[1] + section_height), (self.rect[2], section_height))
        for lad in ladders:
            if below.colliderect(lad) and not self.falling and not self.check_lad:
                self.check_lad = True
                already_collided = True
                
                if random.randint(0, 50) == 50:
                    self.falling = True
                    self.y_change = 4
        
        if not already_collided:
            self.check_lad = False

        # print('falling', self.falling)

    def update(self, fireball_trigger):
        if self.y_change < 8 and not self.falling:
            self.y_change += 2
        
        self.bottom = pygame.rect.Rect((self.rect[0], self.rect.bottom - 3), (self.rect[2], 3))

        for i in range(len(platforms)):
            # print(platforms[i])
            if self.bottom.colliderect(platforms[i]):
            # if self.bottom.bottom >= platforms[i].top:
                self.y_change = 0
                self.falling = False
                print("Barrel bottom:", self.bottom)
                print("Platform:", platforms[i])

        
        if self.rect.colliderect(oil_drum):
            if not self.oil_collision:
                self.oil_collision = True
                
                # fireball spawn 1/5 random chance
                if random.randint(0, 4) == 4:
                    fireball_trigger = True

        if not self.falling:
            if row5_top >= self.rect.bottom or row3_top >= self.rect.bottom >= row4_top or row1_top > self.rect.bottom >= row2_top:
                self.x_change = 3
                # print(self.x_change)
            else:
                self.x_change = -3
        else:
            self.x_change = 0
        # print(self.x_change)
        self.rect.move_ip(self.x_change, self.y_change)
        # print(self.x_change)

        # remove barrel that moves off screen
        if self.rect.top > screen_height:
            self.kill()

        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            
            if self.x_change > 0:
                if self.pos < 3:
                    self.pos += 1
                else:
                    self.pos = 0
            else:
                if self.pos > 0:
                    self.pos -= 1
                else:
                    self.pos = 3

        # self.bottom = pygame.rect.Rect((self.rect[0], self.rect.bottom), (self.rect[2], 3))
        # print(self.x_change)
        return fireball_trigger


# functions
def draw_screen():
    platforms = []
    ladders_objs = []
    bridge_objs = []
    # climbable ladders
    climbers = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']
    
    
    # ladders
    for ladder in ladders:
        ladders_objs.append(Ladder(*ladder))
        
        # climbable ladders
        if ladder[2] >= 3:
            climbers.append(ladders_objs[-1].body)

    # platforms
    for bridge in bridges:
        bridge_objs.append(Platform(*bridge))
        platforms.append(bridge_objs[-1].top)

    # platforms = [platform for platform in platforms if isinstance(platform, Platform)]
    # platforms = [platform.top for platform in bridge_objs]
    
    
    
    return platforms, climbers

def draw_oil():
    x_coord, y_coord = 4 * section_width, window_height - 4.5 * section_height
    oil = pygame.draw.rect(window, blue, (x_coord, y_coord, 2 * section_width, 2.5 * section_height))
    pygame.draw.rect(window, blue, (x_coord - 0.1 * section_width, y_coord, 2.2 * section_width, 0.2 * section_height))
    pygame.draw.rect(window, blue, (x_coord - 0.1 * section_width, y_coord + 2.3 * section_height, 2.2 * section_width, 0.2 * section_height))
    pygame.draw.rect(window, blue, (x_coord - 0.1 * section_width, y_coord + 0.2 * section_height, 0.2 * section_width, 2.1 * section_height))
    pygame.draw.rect(window, blue, (x_coord, y_coord + 0.5 * section_height, 2 * section_width, 0.2 * section_height))
    pygame.draw.rect(window, blue, (x_coord, y_coord + 1.7 * section_height, 2 * section_width, 0.2 * section_height))

    window.blit(font.render('OIL', True, white), (x_coord, y_coord + 0.5 * section_height))

    for i in range(4):
        pygame.draw.circle(window, red, (x_coord + 0.5 * section_width + i * 0.4 * section_width, y_coord + 2.1 * section_height), 3)

    # flames
    if counter < 15 or 30 < counter < 45:
        window.blit(fire_image, (x_coord, y_coord - section_height))
    else:
        window.blit(pygame.transform.flip(fire_image, True, False), (x_coord, y_coord - section_height))

    return oil


def draw_extras():
    # draw oil drum
    oil = draw_oil()

    # draw barrels
    # draw_barrels()


# main loop
running = True
while running:
    clock.tick(60)

    if counter < 60:
        counter += 1
    else:
        counter = 0


    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    



    # draw
    window.fill(black)
    
    platforms, ladders = draw_screen()
    
    oildrum = draw_extras()
    
    if barrel_count < barrel_spawn_time:
        barrel_count += 1
    else:
        barrel_count = random.randint(0, 120)
        barrel_time = barrel_count - barrel_spawn_time
        barrel = Barrel(190, 190)
        barrels.add(barrel)

    for barrel in barrels:
        barrel.draw()
        barrel.check_fall()
        fireball_trigger = barrels.update(fireball_trigger)
    
    pygame.display.flip()

pygame.quit()
