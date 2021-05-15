import sys
import os
import pygame as py
import numpy as np
from .config_variables import *
from math import *
from random import random
from .road import *
from .vect2d import vect2d

#******************************************* Function ************************************
def getSensorEquations(self, world):       #returns the equations of the straight lines(in variable y) of the machine in order [vertical, increasing diagonal, horizontal, decreasing diagonal]
        eq = []
        for i in range(4):
            omega = radians(self.rot + 45*i)
            dx = SENSOR_DISTANCE * sin(omega)
            dy = - SENSOR_DISTANCE * cos(omega)

            if CAR_DBG:             #Draw Sensor Line
                py.draw.lines(world.win, GREEN, False, [world.getScreenCoords(self.x+dx, self.y+dy), world.getScreenCoords(self.x-dx, self.y-dy)], 2)

            coef = getSegmentEquation(self, vect2d(x = self.x+dx, y = self.y+dy))
            eq.append(coef)
        return eq
    
def getSegmentEquation(p, q):          #equations in variable y between two points (taking into account the coordinate system with y inverted) in the general form ax + by + c = 0

    a = p.y - q.y
    b = q.x -p.x
    c = p.x*q.y - q.x*p.y

    return (a,b,c)

def getDistance(world, car, sensors, sensorsEquations, p, q):     #given the segment (m, q) I calculate the distance and put it in the corresponding sensor
    (a2,b2,c2) = getSegmentEquation(p, q)

    for i,(a1,b1,c1) in enumerate(sensorsEquations):
        #get intersection between sensor and segment
        if a1!=a2 or b1!=b2:
            d = b1*a2 - a1*b2
            if d == 0:
                continue
            y = (a1*c2 - c1*a2)/d
            x = (c1*b2 - b1*c2)/d
            if (y-p.y)*(y-q.y) > 0 or (x-p.x)*(x-q.x) > 0:        #if the intersection is not between a and b, go to the next iteration
                continue
        else:       #rette coincidenti
            (x, y) = (abs(p.x-q.x), abs(p.y-q.y))

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

def decodeCommand(commands, type):
    if commands[type] > ACTIVATION_TRESHOLD:
        if type == ACC and commands[type] > commands[BRAKE]:
            return True
        elif type == BRAKE and commands[type] > commands[ACC]:
            return True
        elif type == TURN_LEFT and commands[type] > commands[TURN_RIGHT]:
            return True
        elif type == TURN_RIGHT and commands[type] > commands[TURN_LEFT]:
            return True
    return False

#******************************************** Class *************************************
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
    

    def getInputs(self, world, road):         #Draw the sensor when dbg is True
        sensors = []
        for k in range(8):
            sensors.append(SENSOR_DISTANCE)
        sensorsEquations = getSensorEquations(self, world)

        for v in [road.pointsLeft, road.pointsRight]:
            i = road.bottomPointIndex
            while v[i].y > self.y - SENSOR_DISTANCE:
                next_index = getPoint(i+1, NUM_POINTS*road.num_ctrl_points)

                getDistance(world, self, sensors, sensorsEquations, v[i], v[next_index])
                i = next_index

        if CAR_DBG:
            for k,s in enumerate(sensors):
                omega = radians(self.rot + 45*k)
                dx = s * sin(omega)
                dy = - s * cos(omega)
                #disegna intersezioni dei sensori
                if s < SENSOR_DISTANCE:
                    py.draw.circle(world.win, RED, world.getScreenCoords(self.x+dx, self.y+dy), 6)

        #convert to value between 0 (distance = max) and 1 (distance = 0)
        for s in range(len(sensors)):
            sensors[s] = 1 - sensors[s]/SENSOR_DISTANCE

        return sensors
    