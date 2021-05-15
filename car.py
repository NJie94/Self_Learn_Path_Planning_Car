import sys
import os
import pygame as py
import numpy as np
from .config_variables import *
from math import *
from random import random
from .road import *
from .vect2d import vect2d

class car:
    x, y = 0
    
    def __init__(self,x,y,turn):
        self.x = x
        self.y = y
        self.rot = turn
        self.rot = 0
        self.vel = MAX_VEL/2
        self.acc = 0
        self.initImgs()
        self.commands = [0,0,0,0]
        
    def initImgs(self):
        img_names = ["yellow_car.png", "red_car.png", "blu_car.png", "green_car.png"]
        name = img_names[floor(random()*len(img_names))%len(img_names)]                 #Randomly Take one of this image

        self.img = py.transform.rotate(py.transform.scale(py.image.load(os.path.join("imgs", name)).convert_alpha(), (120,69)), -90)
        self.brake_img = py.transform.rotate(py.transform.scale(py.image.load(os.path.join("imgs", "brakes.png")).convert_alpha(), (120,69)), -90)
        
    #Detect collision of the car with the road model
    def detectCollision(self, road):
        #get mask
        mask = py.mask.from_surface(self.img)
        (width, height) = mask.get_size()
        for v in [road.pointsLeft, road.pointsRight]:
            for p in v:
                x = p.x - self.x + width/2
                y = p.y - self.y + height/2
                try:
                    if mask.get_at((int(x),int(y))):
                        return True
                except IndexError as error:
                    continue
        return False