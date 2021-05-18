import sys
import pygame 

class World:
    
    #Declare initial position
    initPos = (0,0)
    bestCarPosition = (0,0)
    
    #initialise world map and car model position
    def __init__(self,startPos, world_width,world_height):
        self.initPos = startPos
        self.bestCarPosition = (0,0)
        self.window = pygame.display.set_mode(world_width,world_height)
        self.window_width = world_width
        self.window_height = world_height
        self.score = 0
        self.bestGenome = None
        
    def BestCarPosUpdate(self,position):
        self.bestCarPosition = position
    
    def getScreenCoords(self,x,y):
        return (int(x + self.initPos[0] - self.bestCarPosition[0]),
                (y + self.initPos[1] - self.bestCarPosition[1]))
        
    def getBestCarPos(self):
        return self.bestCarPosition
    
    def updateScoreResult(self,NewScore):
        self.score = NewScore
    
    def getScoreResult(self):
        return self.score
    