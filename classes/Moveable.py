#cmu 112 graphics from 
from cmu_112_graphics import *
import math
import numpy as np


#parent class of the player and enemy classes
class Moveable():
    def __init__(self, gridX, gridY, boxSize, health=50):
        self.gridX = gridX
        self.gridY = gridY
    

        self.boxSize = boxSize 
        self.health = health
        self.collisionDamage = 1
        self.collided = False


    def move(self, x, y):
        self.gridX+=x
        self.gridY+=y
        self.x+=x*self.boxSize
        self.y+=y*self.boxSize
    
    #dumb methods

    #this self angle finding function is inspired from Jeff Chen's Nier 112 updateAngle
    #https://github.com/jrchen312/Nier112/blob/main/hacking2.py

    #learned about static methods from Kosbie's OH and 112 website:
    #https://www.cs.cmu.edu/~112/notes/notes-oop-part3.html 
    @staticmethod
    def getAngle(self, targetX, targetY, offset=0):
        ydifference = targetY-self.y
        xdifference = targetX-self.x

        try:
            newAngle = math.atan(ydifference/xdifference)
        except:
            #this means that x difference is 0, just subsitute a small num to
            # avoid crashing 
            newAngle = math.atan(ydifference/0.01)
        
        if xdifference < 0:
            newAngle = newAngle+math.pi
        
        self.angle = newAngle + math.pi
        return newAngle+offset

    @staticmethod
    def do2dRotation(ox, oy, x,y, angle):
        rotationMatrix = [[math.cos(angle), -math.sin(angle)],
                            [math.sin(angle), math.cos(angle)]]
        newX = ox + rotationMatrix[0][0]*(x - ox) + rotationMatrix[0][1]*(y - oy)
        newY = oy +  rotationMatrix[1][0]*(x - ox) +  rotationMatrix[1][1]*(y - oy)
        return newX,newY  

    def dealCollisionDmg(self, other):
        if(self.gridX == other.gridX and self.gridY == other.gridY and not self.collided
        and not other.collided):
            other.health-=self.collisionDamage
            self.collided = True
            other.collided = True
        else:
            self.collided = False
            other.collided = False



