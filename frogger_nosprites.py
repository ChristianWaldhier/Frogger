#! /usr/bin/env python
# https://www.pygame.org/project-Rect+Collision+Response-1061-.html

import os
import random
import pygame
import sys

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Class for the orange dude
class Frog(object):
    def __init__(self):
        self.rect = pygame.Rect(160, 240, 16, 16)
        self.color = WHITE
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.color = RED
                

# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.vx = random.randrange(1, 3)
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
               
    def move(self):
        self.rect = pygame.Rect(self.x + self.vx, self.y, 16, 16)
        self.x += self.vx

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((320, 240))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
frog = Frog() # Create the player

# Holds the level layout in a list of strings.
level = [
"WWWWWWWEWWWWWWWWWWWW",
"                    ",
"W                   ",
"                    ",
"W                   ",
"                    ",
"W                   ",
"                    ",
"W                   ",
"                    ",
"W                   ",
"                    ",
"W                   ",
"                    ",
"W                   ",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        x += 16
    y += 16
    x = 0


while True:
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        frog.move(0, -2)

    
    # Just added this to make it slightly fun ;)
    if frog.rect.colliderect(end_rect):
        raise SystemExit

    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        wall.move()
        wall.draw()
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    frog.draw()
    pygame.display.flip()