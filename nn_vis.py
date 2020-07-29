import numpy as np
import scipy.special
import random
from defs import *
import pygame

pygame.font.init()
pygame.init()
pygame.display.set_caption("Reach the other side!")


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
STAT_FONT = pygame.font.SysFont("comicsans", 50)
LIFESPAN = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()




neurons = []
weights = []


class Neuron():
    def __init__(self, x, y):
        #neurons.append(self)
        self.x = int(x)
        self.y = int(y)
        self.diameter = 50
        self.radius = 25
        self.rect = pygame.Rect(self.x, self.y, self.diameter, self.diameter)
        self.color = pygame.Color("Turquoise")
        
    def draw(self):
        #pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        
        
class Layer():
    def __init__(self, neuron_count, layer_id):
        self.neurons = self.create_neurons(neuron_count, layer_id)
        
    def create_neurons(self, neuron_count, layer_id):
        neurons = []

        for i in range(neuron_count):
            neuron = Neuron(SCREEN_WIDTH / 4 * layer_id, ((SCREEN_HEIGHT/ (neuron_count+1)*(i+1))))
            neurons.append(neuron)
            
        return neurons
        
        
class Weight():
    def __init__(self, from_neuron, to_neuron):
        weights.append(self)
        # self.from_point = from_neuron.x + from_neuron.diameter / 2, from_neuron.y + from_neuron.diameter / 2
        # self.to_point = to_neuron.x + to_neuron.diameter / 2, to_neuron.y + to_neuron.diameter / 2
        self.from_point = from_neuron.x, from_neuron.y
        self.to_point = to_neuron.x, to_neuron.y
        self.width = 2
        self.color = pygame.Color("Turquoise")
        
    def draw(self):
        pygame.draw.line(screen, self.color, self.from_point, self.to_point, self.width)
    

def draw_screen():
    for neuron in neurons:
        neuron.draw()

    input_layer = Layer(3, 1)
    hidden_layer = Layer(4, 2)
    output_layer = Layer(2, 3)
    
    for input_neuron in input_layer.neurons:
        input_neuron.draw()
        for hidden_neuron in hidden_layer.neurons:
            Weight(input_neuron, hidden_neuron)
            
    for hidden_neuron in hidden_layer.neurons:
        hidden_neuron.draw()
        for output_neuron in output_layer.neurons:
            Weight(hidden_neuron, output_neuron)
    for output_neuron in output_layer.neurons:
        output_neuron.draw()
        

    for weight in weights:
        weight.draw()
    
    
    ar1 = np.random.uniform(0, 1, size=(3, 1))
    ar1 = np.random.uniform(0, 1, size=(3, 1))


def main():
   
    while True:
        
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

         
        draw_screen()
        pygame.display.flip()


if __name__ == "__main__":
    main()
