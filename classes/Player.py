
from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable

class Player(Moveable):
    def __init__(self, gridX, gridY, boxSize):
        super().__init__(gridX, gridY, boxSize)
        
        self.x = gridX*boxSize + boxSize//2
        self.y = gridY*boxSize+boxSize//2    
        self.angle = math.pi/2
        self.theta = math.pi/2
        self.health = 50
        self.maxHealth = 50

        
        self.width = 20
        self.expWidth = 50
        self.centerDownLength = 20
        self.centerUpLength = 40


    def redrawAll(self, canvas, mouseX, mouseY):
        Moveable.getAngle(self, mouseX, mouseY)
        # canvas.create_line(self.x,self.y,mouseX,mouseY)

        x0 = self.x - self.width
        y0 = self.y
        x1 = self.x
        y1 = self.y - self.centerUpLength
        x2 = self.x + self.width
        y2 = self.y
        x3 = self.x
        y3 = self.y + self.centerDownLength

        x0,y0 = Moveable.do2dRotation(self.x, self.y, x0, y0, self.angle-self.theta)
        x1,y1 = Moveable.do2dRotation(self.x, self.y, x1, y1, self.angle-self.theta)
        x2,y2 = Moveable.do2dRotation(self.x, self.y, x2, y2, self.angle-self.theta)
        x3,y3 = Moveable.do2dRotation(self.x, self.y, x3, y3, self.angle-self.theta)
        canvas.create_polygon(x0, y0,
                                x1, y1,
                                x2, y2,
                                x3, y3, 
                                fill='white')