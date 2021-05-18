import sys
import pygame 
from .car import decode
from .config_variables import *

class Node:
    def __init__(self,id,x,y,type,color, label = "",index = 0):
        self.id = id
        self.x = x
        self.y = y
        self.type = type
        self.color = color
        self.label = label
        self.index = index
    
    def drawNode(self,world):
        colorScheme = self.getNodeColors(world)

        pygame.draw.circle(world.window, colorScheme[0], (self.x,self.y), NODE_RADIUS)
        pygame.draw.circle(world.window, colorScheme[1], (self.x,self.y), NODE_RADIUS-2)

        #draw labels
        if self.type != MIDDLE:
            text = NODE_FONT.render(self.label, 1, BLACK)
            world.window.blit(text, (self.x + (self.type-1) * ((text.get_width() if not self.type else 0) + NODE_RADIUS + 5), self.y - text.get_height()/2))
        
    def getNodeColors(self, world):
    
        if self.type == INPUT:
            ratio = world.bestInputs[self.index]
        elif self.type == OUTPUT:
            ratio = 1 if decode(world.bestCommands, self.index) else 0
        else:
            ratio = 0

        color = [[0,0,0], [0,0,0]]
        for i in range(3):
            color[0][i] = int(ratio * (self.color[1][i]-self.color[3][i]) + self.color[3][i])
            color[1][i] = int(ratio * (self.color[0][i]-self.color[2][i]) + self.color[2][i])
        return color
    
class Connection:
    def __init__(self, input, output, width):
        self.input = input
        self.output = output
        self.width = width

    def draw_Connection(self, world):
        color = GREEN if self.width >= 0 else RED
        width = int(abs(self.width * CONNECTION_WIDTH))
        pygame.draw.line(world.window, color, (self.input.x + NODE_RADIUS, self.input.y), (self.output.x - NODE_RADIUS, self.output.y), width)