import random
import pygame
import sys

pygame.font.init()
pygame.init()
pygame.display.set_caption("Reach the other side!")


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
STAT_FONT = pygame.font.SysFont("comicsans", 50)
LIFESPAN = 600

population_count = 100
count = 0
generation = 0
mutation_rate = 10
fitness_pop = 0

START_SPEED = 30
speed = START_SPEED

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

cars = []
walls = []
frogs = []


class Frog():
    global generation
    def __init__(self, x, y, size):
        frogs.append(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.color = pygame.Color("Turquoise")
        self.vy = 0
        self.fitness = 0
        self.alive = True
        self.generation = generation
        self.dna = DNA()
        
    def calculate_fitness(self):
        self.fitness = int(((1 - self.y / SCREEN_HEIGHT) * 100) ** 2)
        
    def draw(self):
        if self.generation == generation:
            pygame.draw.rect(screen, self.color, self.rect)
            self.calculate_fitness()
        
    def remove(self):
        frogs.remove(self)

    def move(self):
        
        self.y += self.dna.genes[count][0]
        self.rect.y += self.dna.genes[count][0]
        self.x += self.dna.genes[count][1]
        self.rect.x += self.dna.genes[count][1]

        for car in cars:
            if self.rect.colliderect(car.rect):
                self.color = pygame.Color("Salmon")
                self.vy = 0
                self.alive = False
                
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.color = pygame.Color("Salmon")
                self.vy = 0
                self.alive = False
                
        if self.rect.colliderect(end_rect):
            self.color = pygame.Color("turquoise1")
            self.vy = 0
            self.alive = False
            self.fitness = 1

    def __del__(self):
        pass
     
         
class DNA():
    def __init__(self):
        self.genes = []
        for i in range(LIFESPAN):
            self.genes.append([random.randint(-10, 10), random.randint(-10, 10)])
        if generation > 0:
            self.genes = crossover()
            self.genes = mutate(self.genes)
            

class Car():
    def __init__(self, x, y, w, h, vx):
        cars.append(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(x - w, y, w, h)
        self.vx = vx
        self.color = pygame.Color("grey96")
        self.alive = True
               
    def move(self):
        
        if self.vx > 0:
            if self.x < SCREEN_WIDTH:
                self.rect = pygame.Rect(self.x + self.vx, self.y, self.w, self.h)
                self.x += self.vx
            else:
                self.x = -50
                
        if self.vx < 0:
            if self.x > 0:
                self.rect = pygame.Rect(self.x + self.vx, self.y, self.w, self.h)
                self.x += self.vx
            else:
                self.x = SCREEN_WIDTH + 50
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

        
class Wall():
    def __init__(self, x, y, width, height):
        walls.append(self)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.color = pygame.Color("grey96")
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


def calc_selection_prob():
    total_fitness = 0
    for frog in frogs:
        total_fitness += frog.fitness
    
    for frog in frogs:
        frog.fitness = int(frog.fitness / total_fitness * 100)


def select_frog():
    selection_accepted = False
    while selection_accepted is False:
        selected_frog = random.randint(0, len(frogs) - 1)
        random_number = random.randint(0, fitness_pop)
        if frogs[selected_frog].fitness >= random_number:
            selection_accepted = True
            return frogs[selected_frog].dna.genes
                       
        
def crossover():
    mid = random.randrange(0, LIFESPAN)

    genes_mama = select_frog()
    genes_papa = select_frog()
    genes_child = []
    genes_child = [0, 0] * LIFESPAN
      
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
        a[index] = [random.randint(-10, 10), random.randint(-10, 10)]
    return a


def create_frogs():
    for _ in range(population_count):
        Frog(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 25, 16)


def create_cars():
    cars.clear()
    Car(SCREEN_WIDTH, 80, 80, 50, -4)
    Car(-500, 160, 80, 50, 7)
    Car(SCREEN_WIDTH + 200, 240, 80, 50, -3)
    Car(SCREEN_WIDTH + 500, 240, 80, 50, -3)
    Car(0, 320, 80, 50, 4)
    Car(SCREEN_WIDTH + 100, 400, 80, 50, -5)
    Car(SCREEN_WIDTH + 500, 400, 80, 50, -5)
    Car(-300, 480, 80, 50, 5)


def draw_screen():
    screen.fill((51, 51, 51))

    pygame.draw.rect(screen, pygame.Color("SteelBlue"), end_rect)
    pygame.draw.rect(screen, pygame.Color("SteelBlue"), start_rect)
    for wall in walls:
        wall.draw()
    for frog in frogs:
        if frog.alive:
            frog.move()
        frog.draw()
    for car in cars:
        car.move()
        car.draw()

    draw_stats()

     
def draw_stats():
    score_label = STAT_FONT.render("Generation: " + str(generation), 1, (255, 255, 255))
    screen.blit(score_label, (SCREEN_WIDTH - score_label.get_width() - 15, 15))


def calc_fitness_pop():
    global fitness_pop
    for frog in frogs:
        fitness_pop += frog.fitness

def main():
    global speed, count, generation, frogs, end_rect, start_rect
    Wall(0, 0, SCREEN_WIDTH, 10)
    Wall(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 20)
    end_rect = pygame.Rect(0, 10, SCREEN_WIDTH, 40)
    start_rect = pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 40)

    create_frogs()
    create_cars()
    
    while True:
        
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    speed = START_SPEED * 1
                if event.key == pygame.K_2:
                    speed = START_SPEED * 2
                if event.key == pygame.K_3:
                    speed = START_SPEED * 3
                if event.key == pygame.K_4:
                    speed = START_SPEED * 4
                if event.key == pygame.K_5:
                    speed = START_SPEED * 5
                if event.key == pygame.K_6:
                    speed = START_SPEED * 6
                if event.key == pygame.K_7:
                    speed = START_SPEED * 7
                if event.key == pygame.K_8:
                    speed = START_SPEED * 8
                if event.key == pygame.K_9:
                    speed = START_SPEED * 9
         
        draw_screen()
        pygame.display.flip()
        
        count += 1
        
        if count == LIFESPAN - 1:
            generation += 1
            for i in range(len(frogs) - 1):
                frogs[i].alive = False
            calc_fitness_pop()
    
            create_frogs()
            create_cars()
            for i in range(99):
                if frogs[i].alive is False:
    
                    del frogs[i]
            count = 0


import cProfile as profile
profile.run('main()')