import pygame
import sys
import random



# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)




class Frog(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface([50, 50])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vy = 0

    def update(self):
        self.rect.y += self.vy
        
        
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface([50, 50])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vx = 1

    def update(self):
        self.rect.x += self.vx

    
frog = Frog(SCREEN_WIDTH/2, SCREEN_HEIGHT - 25)
car = Car(25, SCREEN_HEIGHT / 2)

player_group = pygame.sprite.Group()
player_group.add(frog)
player_group.add(car)


pygame.display.set_caption('Beach Soccer Tactics')

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                frog.vy = -1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                frog.vy = 0

    # Updating the window
    
    SCREEN.fill(WHITE)
    player_group.draw(SCREEN)
    pygame.display.flip()
    frog.update()
    car.update()
    if frog.rect.colliderect(car.rect):
        print("collision")

    clock.tick(60)
