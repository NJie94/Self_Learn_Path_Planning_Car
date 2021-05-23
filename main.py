import sys
from neat import config
import pygame
import neat
import numpy as np
import time
import os
import random
from .car import Car
from .road import Road
from .world import World, world
from .DrawNeuralNetwork import NeuralNetwork
from .config_variables import *
pygame.font.init()


background = pygame.surface(WINDOW_WIDTH, WINDOW_HEIGHT)
background.fill(BLUE)

def draw_Window(cars,road, world,GENENRATION):
    road.draw(world)
    for car in cars:
        car.draw(world)
    
    Scoretext = STAT_FONT.render("Best Score: " + str(int( world.getscore())), 1, BLACK )
    world.window.blit(Scoretext, (world.win_width-Scoretext.get_width() - 10, 10))
    Generationtext = STAT_FONT.render("Generation: " + str(GENENRATION), 1, BLACK)
    world.win.blit(Generationtext,(world.win_width-Generationtext.get_width()-10,50))
    
    world.BestNeuralNetwork.draw(world)
    
    pygame.display.update()
    world.window.blit(background,(0,0))

def main(genomes = [], configuration = []):
    global GENENRATION
    GENENRATION += 1
    
    NeuralNetworks = []
    cars = []
    dummy = []
    nets = []
    time = 0
    
    world = World(STARTING_POS, WINDOW_WIDTH,WINDOW_HEIGHT)
    world.window.blit(background,(0,0))
    
    for _,gene in genomes:
        net = neat.nn.FeedForwardNetwork.create(gene,config)
        nets.append(net)
        cars.append(Car,(0,0,0))
        gene.fitness = 0
        dummy.append(gene)
        NeuralNetworks.append(NeuralNetwork(config,gene,(100,220)))
        
    road = Road(world)
    clock = pygame.time.Clock()  
    
    run = True
    while run:
        time += 1
        clock.tick(FPS)
        world.updateScoreResult(0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        (xa,ya) = (0,0)
        i = 0
        while(i < len(cars)):
            car = cars[i]
            
            input = car.getInputs(world, road)
            input.append(car.vel/MAX_VELOCITY)
            car.commands = nets[i].activate(tuple(input))
            
            y_previous = car.y
            (x,y) = car.move(road,time)
            
            if time>10 and (car.detectCollision or y>world.getBestCarPos()[1] + BAD_GENONE_TRESHOLD or y>y_previous or car.velocity < 0.1):
                dummy[i].fitness -= 11
                cars.pop(i)
                nets.pop(i)
                dummy.pop(i)
                NeuralNetworks(i)
            else:
                dummy[i].fitness += -(y - y_previous)/100 + car.vel*SCORE_VELOCITY_MULTIPLYER
                if(dummy[i].fitness > world.getScoreResult()):
                    world.updateScoreResult(dummy[i].fitness)
                    world.BestNeuralNetwork = NeuralNetworks[i]
                    world.bestInputs = input
                    world.bestCarCommands = car.commands
                i += 1
            
            if y < ya:
                (xa,ya) = (x,y)
            
            
        if len (cars) == 0:
            run = False
            break
        
        world.BestCarPosUpdate(xa,ya)
        road.update(world)
        draw_Window(cars,road,world,GENENRATION)
        
        
#Neat
#NEAT function
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    d = neat.Population(config)

    d.add_reporter(neat.StdOutReporter(True))
    stats =neat.StatisticsReporter()
    d.add_reporter(stats)

    winner = d.run(main, 10000)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_file.txt")
    run(config_path)
        
          
    
