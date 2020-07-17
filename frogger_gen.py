import random
import pygame
import sys
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

LIFESPAN = 300


population_count = 10
count = 0
generation = 0

mutation_rate = 3

# TO-DO: create surface to be able to set alpha, see smart boxes


class Frog(object):
    
    def __init__(self, x, y, size):
        frogs.append(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.color = pygame.Color("darkgreen")
        self.vy = 0
        self.fitness = 0
        self.alive = True
        self.dna = DNA()
        
    def calculate_fitness(self):
        self.fitness = ((1 - self.y / SCREEN_HEIGHT) * 100) ** 2
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        self.calculate_fitness()
        
    def remove(self):
        frogs.remove(self)



    def move(self):
        
        self.y += self.dna.genes[count]
        self.rect.y += self.dna.genes[count]


        for car in cars:
            if self.rect.colliderect(car.rect):
                self.color = pygame.Color("red")
                self.vy = 0
                self.alive = False
                
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.color = pygame.Color("red")
                self.vy = 0
                self.alive = False
                
        if self.rect.colliderect(end_rect):
            self.color = pygame.Color("red")
            self.vy = 0
            self.alive = False
            self.fitness = 1
                
class DNA():
    def __init__(self):
        self.genes = []
        for i in range(LIFESPAN):
            self.genes.append(random.randint(-6, 6))
        if generation > 0:
            self.genes = crossover()
            self.genes = mutate(self.genes)
            

        
class Car():
    def __init__(self, x, y, w, h):
        cars.append(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x - w, y, w, h)
        self.vx = 2
        self.color = pygame.Color("blue")
        self.alive = True
               
    def move(self):
        if self.x < SCREEN_WIDTH:
            self.rect = pygame.Rect(self.x + self.vx, self.y, self.w, self.h)
            self.x += self.vx
        else:
            self.x = -50

        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        
class Wall():
    def __init__(self, x, y, width, height):
        walls.append(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color("white")
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def calc_selection_prob():
    total_fitness = 0
    for frog in frogs:
        total_fitness += frog.fitness
    
    for frog in frogs:
        frog.fitness = int(frog.fitness / total_fitness * 100)

        

def select_frog():
    # selected_frog = random.randint(0, len(frogs) - 1)
    # if frogs[selected_frog].fitness > random.randint(0, 100):
    #     return frogs[selected_frog].dna.genes
    # else:
    #     select_frog()
        
    selection_accepted = False
    
    for _ in range(10000000):
        selected_frog = random.randint(0, len(frogs) - 1)
        random_number = random.randint(0, 100)
        print("fitness: " + str(frogs[selected_frog].fitness))
        print("rand: " +  str(random_number))
        if frogs[selected_frog].fitness >= random_number:
            return frogs[selected_frog].dna.genes
            break
            
            
def select_frog2():
    prob = random.uniform(0, 1)

    for i in range(len(frogs)-1):
        prob -= frogs[i].fitness
        if prob < 0:
            return i

        
def crossover():
    mid = random.randrange(0, LIFESPAN)

    genes_mama = select_frog()
    genes_papa = select_frog()
    genes_child = []
    genes_child = [0] * LIFESPAN
        
    for i in range(LIFESPAN):
        if i > mid:
            genes_child[i] = genes_mama[i]
        else:
            genes_child[i] = genes_papa[i]

    return genes_child

def mutate(a):
    prob = random.randrange(0, 100)
    index = random.randrange(0, LIFESPAN)
    if prob < mutation_rate:
        if random.randint(0, 1):
            a[index] = 10
        else:
            a[index] = -10

    return a







def create_frogs():
    for _ in range(population_count):
        Frog(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, 16)


def draw_screen():

    screen.fill((0, 0, 0))
    
    for frog in frogs:
        if frog.alive:
            frog.move()
        frog.draw()
    
    for car in cars:
        car.move()
        car.draw()
    pygame.draw.rect(screen, pygame.Color("lightblue"), end_rect)
    
    for wall in walls:
        wall.draw()



pygame.init()

pygame.display.set_caption("Get to the green square!")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
cars = []
walls = []

frogs = []

Wall(0, 0, SCREEN_WIDTH, 10)
Wall(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10)

end_rect = pygame.Rect(10, 10, SCREEN_WIDTH, 32)

# create cars
Car(0, 100, 80, 50)
Car(-300, 200, 80, 50)
Car(-200, 300, 80, 50)
Car(0, 400, 80, 50)
# Car(-100, 500, 80, 50)
    
create_frogs()

while True:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
     
    draw_screen()
    pygame.display.flip()
    
    count += 1
    
    if count == LIFESPAN - 1:
        calc_selection_prob()
        generation += 1
        for i in range(len(frogs) - 1):
            frogs[i].alive = False

        create_frogs()
        for frog in frogs:
            if frog.alive == False:
                frog.remove()
        
        
        count = 0
