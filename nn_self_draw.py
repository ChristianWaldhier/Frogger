import numpy as np
import scipy.special
import random
from defs import *
import pygame
from pygame import gfxdraw
import sys

pygame.font.init()
pygame.init()
pygame.display.set_caption("Reach the other side!")


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
STAT_FONT = pygame.font.SysFont("comicsans", 50)
LIFESPAN = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA, 32)
clock = pygame.time.Clock()

weights = []


class Nnet:

    def __init__(self, num_input, num_hidden, num_output):
        self.num_input = num_input
        self.inputs = [0] * num_input
        self.num_hidden = num_hidden
        self.hidden_inputs = [0] * num_hidden
        self.num_output = num_output
        self.final_outputs = [0] * num_output
        self.weight_input_hidden = np.random.uniform(-0.5, 0.5, size=(self.num_hidden, self.num_input))
        self.weight_hidden_output = np.random.uniform(-0.5, 0.5, size=(self.num_output, self.num_hidden))
        self.activation_function = lambda x: scipy.special.expit(x)

    def get_outputs(self, inputs_list):
        self.inputs = np.array(inputs_list, ndmin=2).T
        self.hidden_inputs = np.dot(self.weight_input_hidden, self.inputs)
        hidden_outputs = self.activation_function(self.hidden_inputs)
        final_inputs = np.dot(self.weight_hidden_output, hidden_outputs)
        self.final_outputs = self.activation_function(final_inputs)
        return self.final_outputs 

    def get_max_value(self, inputs_list):
        outputs = self.get_outputs(inputs_list)
        return np.max(outputs)

    def modify_weights(self):
        Nnet.modify_array(self.weight_input_hidden)
        Nnet.modify_array(self.weight_hidden_output)

    def create_mixed_weights(self, net1, net2):
        self.weight_input_hidden = Nnet.get_mix_from_arrays(net1.weight_input_hidden,  net2.weight_input_hidden)
        self.weight_hidden_output = Nnet.get_mix_from_arrays(net1.weight_hidden_output,  net2.weight_hidden_output)       

    def modify_array(a):
        for x in np.nditer(a, op_flags=['readwrite']):
            if random.random() < MUTATION_WEIGHT_MODIFY_CHANCE:
                x[...] = np.random.random_sample() - 0.5

    def get_mix_from_arrays(ar1, ar2):

        total_entries = ar1.size
        num_rows = ar1.shape[0]
        num_cols = ar1.shape[1]

        num_to_take = total_entries - int(total_entries * MUTATION_ARRAY_MIX_PERC)
        idx = np.random.choice(np.arange(total_entries),  num_to_take, replace=False)

        res = np.random.rand(num_rows, num_cols)

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                index = row * num_cols + col
                if index in idx:
                    res[row][col] = ar1[row][col]
                else:
                    res[row][col] = ar2[row][col]

        return res

    def draw(self):
        
                
        input_layer = Layer(self.inputs, 1)
        hidden_layer = Layer(self.hidden_inputs, 2)
        output_layer = Layer(self.final_outputs, 3)
        
        for input_neuron in input_layer.neurons:
            for hidden_neuron in hidden_layer.neurons:
                Weight(input_neuron, hidden_neuron)
                
        for hidden_neuron in hidden_layer.neurons:
            for output_neuron in output_layer.neurons:
                Weight(hidden_neuron, output_neuron)
    
        for weight in weights:
            weight.draw()
            
        for input_neuron in input_layer.neurons:
            input_neuron.draw()
        for hidden_neuron in hidden_layer.neurons:
            hidden_neuron.draw()
        for output_neuron in output_layer.neurons:
            # print(output_neuron.color_test)
            output_neuron.draw()


def tests():
    
    nnet = Nnet(2, 5, 1)
    
    ar1 = np.random.uniform(-0.5, 0.5, size=(3, 4))
    ar2 = np.random.uniform(-0.5, 0.5, size=(3, 4))
    print('ar1.size', ar1.size, sep='\n')
    print('ar1', ar1, sep='\n')

    Nnet.modify_array(ar1)
    print('ar1', ar1, sep='\n')

    print('')

    print('ar1', ar1, sep='\n')
    print('ar2', ar2, sep='\n')

    mixed = Nnet.get_mix_from_arrays(ar1, ar2)
    print('mixed', mixed, sep='\n')
   

class Neuron():
    def __init__(self, x, y, value):
        #neurons.append(self)
        self.x = int(x)
        self.y = int(y)
        self.value = value
        self.diameter = 50
        self.radius = 25
        self.rect = pygame.Rect(self.x, self.y, self.diameter, self.diameter)
        self.color_test = abs(int(value * 255))
        self.color = (self.color_test, self.color_test, self.color_test)
        #self.color = pygame.Color("Turquoise")
        
    def draw(self):
        #pygame.draw.rect(screen, self.color, self.rect)
        #pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, self.radius, self.color)
        pygame.gfxdraw.aacircle(screen, self.x, self.y, self.radius, pygame.Color("Turquoise"))
        pygame.gfxdraw.aacircle(screen, self.x, self.y, self.radius + 1, pygame.Color("Turquoise"))
        pygame.gfxdraw.aacircle(screen, self.x, self.y, self.radius + 2, pygame.Color("Turquoise"))
        
        
class Layer():
    def __init__(self, layer_values, layer_id):
        
        self.neuron_count = len(layer_values)
        self.neurons = self.create_neurons(self.neuron_count, layer_id, layer_values)
        
    def create_neurons(self, neuron_count, layer_id, layer_values):
        neurons = []

        for i in range(neuron_count):
            neuron = Neuron(SCREEN_WIDTH / 4 * layer_id, ((SCREEN_HEIGHT/ (neuron_count+1)*(i+1))),layer_values[i - 1])
            neurons.append(neuron)
            
        return neurons
        
        
class Weight():
    def __init__(self, from_neuron, to_neuron):
        weights.append(self)
        self.from_point = from_neuron.x, from_neuron.y
        self.to_point = to_neuron.x, to_neuron.y
        self.width = 3
        self.color = pygame.Color("Turquoise")
        
    def draw(self):
        pygame.draw.line(screen, self.color, self.from_point, self.to_point, self.width)
        # pygame.draw.aaline(screen, self.color, self.from_point, self.to_point, self.width)
        
        

def main():
    
    test_net = Nnet(3, 5, 2)
    
    while True:
        
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        test_net.get_outputs(np.random.uniform(0, 1, size=(test_net.num_input)))

        test_net.draw()
        pygame.display.flip()


if __name__ == "__main__":
    tests()
    main()
