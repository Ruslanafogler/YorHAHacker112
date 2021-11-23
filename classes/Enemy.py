from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable
from .AStar import aStar


#INCLUDES BOTH TYPE A AND B

class Enemy(Moveable):
     def __init__(self, type, playerPosition, gridX, gridY, boxSize):
        super().__init__(gridX, gridY, boxSize)
        self.type = type
        self.x = self.gridX*self.boxSize + self.boxSize//2
        self.y = self.gridY*self.boxSize + self.boxSize//2
        
        self.movementTimer = 0
        self.aimingTimer = 0
        self.shootingTimer = 0
        self.aimCoolDown = 0.1
        self.fireCoolDown = 9
        self.movementCoolDown = 0.8


        self.movements = []
        self.movementIndex = -1

        self.bullets=[]

        self.centerLength = 18
        self.angle = math.pi/2
        self.theta = math.pi/3

        self.enemyR = 25
     
     def __str__(self):
        return f'enemy{self.type} row coords, coords {self.gridX}, {self.gridY}, {self.x}, {self.y}'

    #the polygon one


     def incTimers(self):
        self.movementTimer+=1
        self.aimingTimer+=1
        self.shootingTimer+=1
     
     def initMovements(self, map, playerPosition):
         startPosition = (self.gridY, self.gridX)
         self.movements = aStar(map, startPosition, playerPosition)
        #  self.movements= [(1,0), (0, 1), (1, 0), (0, 1), (-1, 0),(0,-1)]
         self.movementIndex = -1

     def getMovement(self):
         if(self.movementIndex >= len(self.movements)):
             return (0,0)
         else:
            return self.movements[self.movementIndex]
    
     def fireBullet(self, newBullet):
         self.bullets.append(newBullet)

     def removeBullet(self, bullet):
         self.bullets.remove(bullet)


     def redrawAll(self, canvas, playerX, playerY):
         Moveable.getAngle(self, playerX, playerY)

         if(self.type == 'A'):
            Enemy.drawEnemyA(self, canvas)
         elif(self.type == 'B'):
            Enemy.drawEnemyB(self, canvas)




     def drawEnemyA(self, canvas):
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


    #the circle one
     def drawEnemyB(self, canvas):

        canvas.create_oval(self.x - self.enemyR, self.y-self.enemyR,
                    self.x + self.enemyR, self.y + self.enemyR, fill='#242526')

            


