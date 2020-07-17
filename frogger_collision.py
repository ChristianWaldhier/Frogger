import random
import pygame
import sys

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Frog(object):
    def __init__(self, x, y, size):
        frogs.append(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.color = pygame.Color("darkgreen")
        self.vy = 0
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, vy):
        self.vy = vy
        self.rect.y += self.vy

        for car in cars:
            if self.rect.colliderect(car.rect):
                self.color = pygame.Color("red")
         

class Car():
    def __init__(self, x, y):
        cars.append(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)
        self.vx = random.randrange(1, 3)
        self.color = pygame.Color("blue")
        self.alive = True
               
    def move(self):
        self.rect = pygame.Rect(self.x + self.vx, self.y, 32, 32)
        self.x += self.vx
        # if self.rect.colliderect(frog.rect):
        #     self.vx = 0
        #     self.color = pygame.Color("red")
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


pygame.init()

pygame.display.set_caption("Get to the green square!")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
cars = []

frogs = []


end_rect = pygame.Rect(SCREEN_WIDTH / 2, 0, 32, 32)

while len(cars) < 10:
    Car(0, random.randrange(0, SCREEN_HEIGHT))
    
while len(frogs) < 20:
    Frog(random.randrange(0, SCREEN_WIDTH), SCREEN_HEIGHT - 16 , 16)


def draw_screen(screen, frogs, cars):

    screen.fill((0, 0, 0))
    
    for frog in frogs:
        frog.move(random.randrange(-3, -1))
        frog.draw()
        if frog.rect.colliderect(end_rect):
            print("You Win!")
    
    for car in cars:
        car.move()
        car.draw()
    pygame.draw.rect(screen, pygame.Color("green"), end_rect)

    
while True:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # key = pygame.key.get_pressed()
    # if key[pygame.K_UP]:
    #     frog.move(-2)
    
    draw_screen(screen, frogs, cars)
    pygame.display.flip()




