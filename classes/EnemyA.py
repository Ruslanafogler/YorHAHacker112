from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable

##OBSOLETE FILE< SEE ENEMY INSTEAD

class EnemyA(Moveable):
     def __init__(self, gridX, gridY, boxSize):
        super().__init__(gridX, gridY, boxSize)
        self.x = self.gridX*self.boxSize + self.boxSize//2
        self.y = self.gridY*self.boxSize + self.boxSize//2

        self.centerLength = 18
        self.angle = math.pi/2
        self.theta = math.pi/3
     
     def __str__(self):
        return f'enemyA row coords, coords {self.gridX}, {self.gridY}, {self.x}, {self.y}'


     def redrawAll(self, canvas):
         x0, y0 = self.x-self.centerLength, self.y-self.centerLength
         x1, y1 = self.x, self.y-2*self.centerLength
         x2, y2 = self.x+self.centerLength, self.y-self.centerLength
         x3, y3 = self.x+self.centerLength, self.y + self.centerLength
         x4, y4 = self.x-self.centerLength, self.y+self.centerLength
         
         x0,y0 = Moveable.do2dRotation(self.x, self.y, x0, y0, self.angle-self.theta)
         x1,y1 = Moveable.do2dRotation(self.x, self.y, x1, y1, self.angle-self.theta)
         x2,y2 = Moveable.do2dRotation(self.x, self.y, x2, y2, self.angle-self.theta)
         x3,y3 = Moveable.do2dRotation(self.x, self.y, x3, y3, self.angle-self.theta)
         x4,y4 = Moveable.do2dRotation(self.x, self.y, x4, y4, self.angle-self.theta)

         canvas.create_polygon(
                            x0, y0,
                            x1, y1,
                            x2, y2,
                            x3, y3,
                            x4, y4,
                            fill='#3a3b3c'
                            )
