#! /usr/bin/env python
# https://www.pygame.org/project-Rect+Collision+Response-1061-.html

import random
import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Frog(object):
    def __init__(self, size):
        self.rect = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT - size, size, size)
        self.color = pygame.Color("blue")
        self.vy = 0
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, vy):
        self.vy = vy
        self.rect.y += self.vy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.color = pygame.Color("red")
         

class Wall(object):
    def __init__(self, x, y):
        walls.append(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vx = random.randrange(1, 3)
        self.color = pygame.Color("white")
               
    def move(self):
        self.rect = pygame.Rect(self.x + self.vx, self.y, 32, 32)
        self.x += self.vx

    def draw(self):
        pygame.draw.rect(screen, self.color, wall.rect)


pygame.init()

pygame.display.set_caption("Get to the green square!")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
walls = []
frog = Frog(32)

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
            Wall(x, y)
        if col == "E":
            end_rect = pygame.Rect(SCREEN_WIDTH / 2, 0, 32, 32)
        x += 32
    y += 32
    x = 0

while True:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        frog.move(-2)

    if frog.rect.colliderect(end_rect):
        print("You Win!")

    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        wall.move()
        wall.draw()
    pygame.draw.rect(screen, pygame.Color("green"), end_rect)
    frog.draw()
    pygame.display.flip()
