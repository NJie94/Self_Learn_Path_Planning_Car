import sys
import os
import pygame as pygame
import numpy as numpy
from .config_variables import *
from math import *
from random import random
from .road import *
from .vector2d import vector2d

#******************************************* Function ************************************
def getSensor(self, world):       #returns the equations of the straight lines(in variable y) of the machine in order [vertical, increasing diagonal, horizontal, decreasing diagonal]
        eq = []
        for i in range(4):
            omega = radians(self.rot + 45*i)
            dx = SENSOR_DISTANCE * sin(omega)
            dy = - SENSOR_DISTANCE * cos(omega)

            if CAR_DBG:             #Draw Sensor Line
                pygame.draw.lines(world.win, GREEN, False, [world.getScreenCoords(self.x+dx, self.y+dy), world.getScreenCoords(self.x-dx, self.y-dy)], 2)

            coef = getSEGEquation(self, vector2d(x = self.x+dx, y = self.y+dy))
            eq.append(coef)
        return eq
    
def getSEGEquation(g, h):          #equations in variable y between two points (taking into ACCELETATIONount the coordinate system with y inverted) in the general form ax + by + c = 0

    a = g.y - h.y
    b = h.x -g.x
    c = g.x*h.y - h.x*g.y

    return (a,b,c)

def getDistance(world, car, sensors, sensorsEquations, g, h):     #given the segment (m, q) I calculate the distance and put it in the corresponding sensor
    (a2,b2,c2) = getSEGEquation(g, h)

    for i,(a1,b1,c1) in enumerate(sensorsEquations):
        #get intersection between sensor and segment
        if a1!=a2 or b1!=b2:
            d = b1*a2 - a1*b2
            if d == 0:
                continue
            y = (a1*c2 - c1*a2)/d
            x = (c1*b2 - b1*c2)/d
            if (y-g.y)*(y-h.y) > 0 or (x-g.x)*(x-h.x) > 0:        #if the intersection is not between a and b, go to the next iteration
                continue
        else:       #coincident lines
            (x, y) = (abs(g.x-h.x), abs(g.y-h.y))

        #aquire distance
        dist = ((car.x - x)**2 + (car.y - y)**2)**0.5

        #insert into the sensor in the right direction
        omega = car.rot +45*i                               #angle of the sensor line (and its opposite)
        alpha = 90- degrees(atan2(car.y - y, x-car.x))     #angle to vertical (as car.rot)
        if cos(alpha)*cos(omega)*100 + sin(alpha)*sin(omega)*100 > 0:
            index = i
        else:
            index = i + 4

        if dist < sensors[index]:
            sensors[index] = dist

def decode(commands, type):
    if commands[type] > ACTIVATION_TRESHOLD:
        if type == ACCELETATION and commands[type] > commands[BRAKE]:
            return True
        elif type == BRAKE and commands[type] > commands[ACCELETATION]:
            return True
        elif type == TURNLEFT and commands[type] > commands[TURNRIGHT]:
            return True
        elif type == TURNRIGHT and commands[type] > commands[TURNLEFT]:
            return True
    return False

#******************************************** Class *************************************
class car:
    x, y = 0
    
    def __init__(self,x,y,turn):
        self.x = x
        self.y = y
        self.rotation = turn
        self.rotation = 0
        self.VELOCITY = MAX_VELOCITY/2
        self.ACCELETATION = 0
        self.initImgs()
        self.commands = [0,0,0,0]
        
    def initImgs(self):
        img_names = ["yellow_car.png", "red_car.png", "blu_car.png", "green_car.png"]
        name = img_names[floor(random()*len(img_names))%len(img_names)]                 #Randomly Take one of this image

        self.img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imgs", name)).convert_alpha(), (120,69)), -90)
        self.brake_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("imgs", "brakes.png")).convert_alpha(), (120,69)), -90)
        
    #Detect collision of the car with the road model
    def detectCollision(self, road):
        #get mask
        mask = pygame.mask.from_surface(self.img)
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
    

    def getInputs(self, map, road):         #Draw the sensor when dbg is True
        sensors = []
        for w in range(8):
            sensors.append(SENSOR_DISTANCE)
        sensorsEquations = getSensor(self, map)

        for v in [road.pointsLeft, road.pointsRight]:
            i = road.bottomPointIndex
            while v[i].y > self.y - SENSOR_DISTANCE:
                next_index = getPoint(i+1, NUMBER_Pt*road.num_ctrl_points)

                getDistance(map, self, sensors, sensorsEquations, v[i], v[next_index])
                i = next_index

        if CAR_DBG:
            for w,z in enumerate(sensors):
                omega = radians(self.rotation + 45*w)
                dx = z * sin(omega)
                dy = - z * cos(omega)
                #draw sensor intersections
                if z < SENSOR_DISTANCE:
                    pygame.draw.circle(map.win, RED, map.getScreenCoords(self.x+dx, self.y+dy), 6)

        #convert to value between 0 (distance = max) and 1 (distance = 0)
        for z in range(len(sensors)):
            sensors[z] = 1 - sensors[z]/SENSOR_DISTANCE

        return sensors
    
    def move(self, road, t):
        self.ACCELETATION = FRICTION
        if decode(self.commands, ACCELETATION):
            self.ACCELETATION = ACCELETATION_STRENGTH
        if decode(self.commands, BRAKE):
            self.ACCELETATION = -BRAKE_STREGTH
        if decode(self.commands, ):
            self.rotation -= TURN_VELOCITY
        if decode(self.commands, TURNRIGHT):
            self.rotation += TURN_VELOCITY

        timeBuffer = 500
        if MAX_VELOCITY_REDUCTION == 1 or t >= timeBuffer:
            max_VELOCITY_local = MAX_VELOCITY
        else:
            ratio = MAX_VELOCITY_REDUCTION + (1 - MAX_VELOCITY_REDUCTION)*(t/timeBuffer)
            max_VELOCITY_local = MAX_VELOCITY *ratio

        self.VELOCITY += self.ACCELETATION
        if self.VELOCITY > max_VELOCITY_local:
            self.VELOCITY = max_VELOCITY_local
        if self.VELOCITY < 0:
            self.VELOCITY = 0
        self.x=self.x+self.VELOCITY*sin(radians(self.rotation))
        self.y=self.y-self.VELOCITY*cos(radians(self.rotation)) #origin at top left hence use subtraction

        

        return (self.x, self.y)
    
    def draw(self, world):
        screen_position = world.getScreenCoords(self.x, self.y)
        rotated_img = pygame.transform.rotate(self.img, -self.rotation)
        new_rect = rotated_img.get_rect(center = screen_position)
        world.win.blit(rotated_img, new_rect.topleft)

        if decode(self.commands, BRAKE):
            rotated_img = pygame.transform.rotate(self.brake_img, -self.rotation)
            new_rect = rotated_img.get_rect(center = screen_position)
            world.win.blit(rotated_img, new_rect.topleft)