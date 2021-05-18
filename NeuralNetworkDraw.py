import sys
import pygame
from .config_variables import *
from .car import decode
from .vector2d import vector2d
from .drawnode import *

pygame.font.init()


class NeuralNetwork:
    
    def __init__(self, config, genome, position):
        self.input_nodes = []
        self.output_nodes = []
        self.nodes = []
        self.genome = genome
        self.pos = (int(position[0]+NODE_RADIUS), int(position[1]))
        input_names_list = ["T", "T_Right", "Right", "B_Right", "B", "B_Left", "Left", "T_Left", "Velocity"]
        output_names_list = ["Forward", "Brake", "Left", "Right"]
        midNodes = [n for n in genome.nodes.keys()]
        Id_List = []
        
        #nodes
        a = (NUMBER_OF_INPUT_NEURONS-1)*(NODE_RADIUS*2 + NODE_SPACING)
        for i, input in enumerate(config.genome_config.input_keys):
            j = Node(input, position[0], position[1]+int(-a/2 + i*(NODE_RADIUS*2 + NODE_SPACING)), INPUT, [GREEN_PALE, GREEN, DARK_GREEN_PALE, DARK_GREEN], input_names_list[i], i)
            self.nodes.append(j)
            Id_List.append(input)

        a = (NUMBER_OF_OUTPUT_NEURONS-1)*(NODE_RADIUS*2 + NODE_SPACING)
        for i,out in enumerate(config.genome_config.output_keys):
            j = Node(out+NUMBER_OF_INPUT_NEURONS, position[0] + 2*(LAYER_SPACING+2*NODE_RADIUS), position[1]+int(-a/2 + i*(NODE_RADIUS*2 + NODE_SPACING)), OUTPUT, [RED_PALE, RED, DARK_RED_PALE, DARK_RED], output_names_list[i], i)
            self.nodes.append(j)
            midNodes.remove(out)
            Id_List.append(out)

        a = (len(midNodes)-1)*(NODE_RADIUS*2 + NODE_SPACING)
        for i, m in enumerate(midNodes):
            j = Node(m, self.pos[0] + (LAYER_SPACING+2*NODE_RADIUS), self.pos[1]+int(-a/2 + i*(NODE_RADIUS*2 + NODE_SPACING)), MIDDLE, [BLUE_PALE, DARK_BLUE, BLUE_PALE, DARK_BLUE])
            self.nodes.append(j)
            Id_List.append(m)

        #connections
        self.connections = []
        for k in genome.connections.values():
            if k.enabled:
                input, output = k.key
                self.connections.append(Connection(self.nodes[Id_List.index(input)],self.nodes[Id_List.index(output)], k.weight))

    def drawNeural(self, world):
        for k in self.connections:
            k.draw_Connection(world)
        for node in self.nodes:
            node.drawnode(world)














