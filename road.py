# Random self generated Road Map
import sys
import pygame as pygame
import numpy as numpy
from scipy import interpolate
from math import *
from random import random, seed
from .config_variables import *
from .vector2d import vector2d


class Road:
    def __init__(self, world):
        self.numcontrolpt = (int)((world.win_height+SAFE_SPACE)/SPACING)+2

        self.lastcontrolpt = 0
        self.controlpt = []
        self.centerpt = []
        self.Leftpt = []
        self.Rightpt = []

        for i in range(self.numcontrolpt):
             self.controlpt.append(vector2d())

        for i in range(NUMBER_Pt*self.numcontrolpt):                    # Fill the Left point and right point 
            self.Leftpt.append(vector2d(1000,1000))
            self.Rightpt.append(vector2d(1000,1000))
            self.centerpt.append(vector2d(1000,1000))

        self.controlpt[0].co(0, SPACING)                                  # initialise the first two control_points to be straight
        self.controlpt[1].co(0, 0)
        for i in range(NUMBER_Pt):
            x = self.controlpt[0].x
            y = self.controlpt[0].y - SPACING/NUMBER_Pt*i
            self.centerpt[i].co(x, y)
            self.Leftpt[i].co(x - ROAD_WIDTH/2, y)
            self.Rightpt[i].co(x + ROAD_WIDTH/2, y)
        self.next_point = NUMBER_Pt

        for i in range(self.numcontrolpt-2):
            self.createSegment(i+1)

        self.lastcontrolpt = self.numcontrolpt-1
        self.bottomPTIndex = 0

    def calcBorders(self, i):
        previous_index = getPoint(i-1, self.numcontrolpt*NUMBER_Pt)
        center = self.centerpt[i]
        prev = self.centerpt[previous_index]
        angle = atan2(center.x-prev.x, prev.y-center.y)

        x = ROAD_WIDTH/2 * cos(angle)
        y = ROAD_WIDTH/2 * sin(angle)
        self.Leftpt[i].x = center.x - x
        self.Leftpt[i].y = center.y - y if not center.y - y >= self.Leftpt[previous_index].y else self.Leftpt[previous_index].y
        self.Rightpt[i].x = center.x + x
        self.Rightpt[i].y = center.y + y if not center.y + y >= self.Rightpt[previous_index].y else self.Rightpt[previous_index].y

    def createSegment(self, index):
        p1 = self.controlpt[getPoint(index, self.numcontrolpt)]
        p2 = self.controlpt[getPoint(index+1, self.numcontrolpt)]

        #define p2
        seed()
        p2.co(p1.x + (random()-0.5)*MAX_DEVIATION, p1.y-SPACING)
        p2.angle = MAX_ANGLE*(random()-0.5)

        y_temporary = []
        for i in range(NUMBER_Pt):
            y_temporary.append(p2.y+SPACING/NUMBER_Pt*i)

        # Get Center Line of the Road
        ny = numpy.array([p2.y, p1.y])                                         # Inverted because scipy increasing the X (in this case the Y)
        nx = numpy.array([p2.x, p1.x])
        cs = interpolate.CubicSpline(ny, nx, axis=0, bc_type=((1,p2.angle),(1,p1.angle)))
        res = cs(y_temporary)

        #create the actual borders
        for i in range(NUMBER_Pt):
            self.centerpt[self.next_point].x = res[NUMBER_Pt-i-1]
            self.centerpt[self.next_point].y = y_temporary[NUMBER_Pt-i-1]
            self.calcBorders(self.next_point)

            self.next_point = getPoint(self.next_point+1, NUMBER_Pt*self.numcontrolpt)

        self.lastcontrolpt = getPoint(self.lastcontrolpt + 1, self.numcontrolpt)
        self.bottomPTIndex = self.next_point

    def update(self, world):
        if world.getScreenCoords(0, self.controlpt[set].y)[1] > -SAFE_SPACE:
            self.createSegment(set)


    def draw(self, world):
        #draw control_points
        if(ROAD_DBG):
            for i in range(len(self.Leftpt)):
                pygame.draw.circle(world.win, BLUE, world.getScreenCoords(self.Leftpt[i].x, self.Leftpt[i].y), 2)
                pygame.draw.circle(world.win, BLUE, world.getScreenCoords(self.Rightpt[i].x, self.Rightpt[i].y), 2)
            #draw borders
            for i in range(len(self.Leftpt)):
                next_index = getPoint(i+1, NUMBER_Pt*self.numcontrolpt)

                p = self.Leftpt[i]
                f = self.Leftpt[next_index]
                if p.y >= f.y:
                    pygame.draw.line(world.win, BLACK, world.getScreenCoords(p.x, p.y), world.getScreenCoords(f.x, f.y), 4)

                p = self.Rightpt[i]
                f = self.Rightpt[next_index]
                if p.y >= f.y:
                    pygame.draw.line(world.win, BLACK, world.getScreenCoords(p.x, p.y),world.getScreenCoords(f.x, f.y), 4)


def getPoint(i, cap):
    return (i+cap)%cap
