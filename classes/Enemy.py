from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable
from .AStar import aStar
from .config import COLORS


#INCLUDES BOTH TYPE A AND B

class Enemy(Moveable):
     def __init__(self, type, gridX, gridY, boxSize, difficulty):
        super().__init__(gridX, gridY, boxSize)
        self.type = type
        self.x = self.gridX*self.boxSize + self.boxSize//2
        self.y = self.gridY*self.boxSize + self.boxSize//2
        
        self.movementTimer = 0
        self.aimingTimer = 0
        self.shootingTimer = 0
        
        self.hitTimer = 0
        self.hit = False
       
        Enemy.scaleDifficulty(self, difficulty)
        Enemy.setEnemyColor(self)

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

     def scaleDifficulty(self, difficulty):
      #difficulty ranges from 1 to 21

      self.fireCoolDown = Enemy.scaleFireCoolDownDiff(difficulty)
      self.movementCoolDown = Enemy.scaleMovementCoolDownDiff(difficulty)
      
      #max health is 25
      self.health = Enemy.scaleHealthDiff(difficulty)
      self.maxHealth = self.health

     
     def scaleFireCoolDownDiff(d):
        #equation found with onlien curve fitting https://mycurvefit.com/
        #with pts (0, 60), (21, 20)
        #y = -1.428571*x+60

        x1 = -1.428571
        x0 = 60
        return x0 + x1*d      
     
     def scaleMovementCoolDownDiff(d):
        #equation found with onlien curve fitting https://mycurvefit.com/
        #with pts (0, 10), (12, 8), (21, 5), (21, 25)
        #y = -0.2342342*x + 10.24324

        x1 = -0.2342342
        x0 = 10.24324
        
        return x0 + x1*d

     def scaleHealthDiff(d):
        #equation found with onlien curve fitting https://mycurvefit.com/
        #with pts (0, 10), (5, 15), (15, 21), (21, 25)
        #y = 10 + 1.360119*x - 0.08492063*x^2 + 0.002579365*x^3
        x3 = 0.002579365
        x2 = -0.08492063
        x1 = 1.360119
        x0 = 10
        return x0 + x1*d + x2*(d**2) + x3*(d**3)
        

     def setEnemyColor(self):
         if(self.type == 'A'):
            self.color = COLORS['enemyA']
         elif(self.type=='B'):
            self.color = COLORS['enemyB']

     def onHit(self):
        if(self.hit):
           self.color = COLORS['lightgray']
        else:
            Enemy.setEnemyColor(self)


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

     def getAngle(self, playerX, playerY):
         if(self.type == 'A'):
            Moveable.getAngle(self, playerX, playerY)
         else:
            Moveable.getAngle(self, playerX, playerY, math.pi/6)




     def redrawAll(self, canvas, playerX, playerY):
         Enemy.getAngle(self, playerX, playerY)
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
                            fill=self.color
                            )


    #the circle one
     def drawEnemyB(self, canvas):

        canvas.create_oval(self.x - self.enemyR, self.y-self.enemyR,
                    self.x + self.enemyR, self.y + self.enemyR, fill=self.color)

            


