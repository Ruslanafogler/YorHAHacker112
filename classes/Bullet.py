
from cmu_112_graphics import *
import math
import numpy as np


#referenced Rabbid76's stackoverflow answer here
#https://stackoverflow.com/questions/59977052/shooting-a-bullet-in-pygame-in-the-direction-of-mouse

class Bullet:
    def __init__(self, initGridX, initGridY, playerX, playerY, boxSize, angle):
        
        
        self.gridX = initGridX
        self.gridY = initGridY
        self.incDx = 0
        self.incDy = 0



        self.x = playerX
        self.y = playerY


        
        
        self.speed = 45
        self.angle = angle
        self.theta = math.pi/2
        self.boxSize = boxSize



    def linearTravel(self, map):
        nextGridX, nextGridY, dx, dy = Bullet.nextGridIndexParams(self)
        print(nextGridY, nextGridX)

        nextSpotVal = map[nextGridY][nextGridX]
        if(nextSpotVal == 1 or nextSpotVal == 4):
           print('ah, wall at', nextGridY, nextGridX)
           return False
        else:
            self.gridX = nextGridX
            self.gridY = nextGridY
            self.incDx+=dx
            self.incDy+=dy
            self.x+=dx
            self.y+=dy
            return True
        
        
        
    
    def nextGridIndexParams(self):
        dx, dy = Bullet.calcLinearDx(self), Bullet.calcLinearDy(self)
        nextGridX = int(self.gridX + self.incDx//self.boxSize)
        nextGridY = int(self.gridY + self.incDy//self.boxSize)

        return nextGridX, nextGridY, dx, dy

    # def linearTravel(self, map):
    #     nextGridX, nextGridY, dx, dy = Bullet.nextGridIndexParams(self)
    #     print(nextGridY, nextGridX)

    #     nextSpotVal = map[nextGridY][nextGridX]
    #     if(nextSpotVal == 1 or nextSpotVal == 4):
    #        return False
    #     else:
    #         self.gridX = nextGridX
    #         self.gridY = nextGridY
    #         self.x+=dx
    #         self.y+=dy
    #         return True
        
        
        
    
    # def nextGridIndexParams(self):
    #     dx, dy = Bullet.calcLinearDx(self), Bullet.calcLinearDy(self)
    #     print(dx, dy)
    #     return (round((self.gridX*self.boxSize + dx)//self.boxSize), 
    #             round((self.gridY*self.boxSize + dy)//self.boxSize), 
    #             dx, dy)

    def calcLinearDx(self):
        return self.speed*math.cos(self.angle+math.pi)

    def calcLinearDy(self):
        return self.speed*math.sin(self.angle+math.pi)
    
    