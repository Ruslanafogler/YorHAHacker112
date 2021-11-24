
from cmu_112_graphics import *
import math
import random
import numpy as np


#referenced Rabbid76's stackoverflow answer here
#https://stackoverflow.com/questions/59977052/shooting-a-bullet-in-pygame-in-the-direction-of-mouse

class Bullet:
    def __init__(self, initGridX, initGridY, playerX, playerY, boxSize, angle):
        
        
        self.gridX = initGridX
        self.gridY = initGridY

        self.x = playerX
        self.y = playerY    
        
        self.speed = 45
        self.angle = angle
        self.theta = math.pi/2
        self.boxSize = boxSize
  
  
    def damage(self, other):
        other.health-=self.bulletDamage
        print(other, other.health)        


    def linearTravel(self, map, minRowScreen, minColScreen, isPlayerBullet):
        

        bulletScreenRow, bulletScreenCol = Bullet.findLocationOnScreenGrid(self)

        actualGridRow, actualGridCol =bulletScreenRow+minRowScreen, bulletScreenCol+minColScreen
        mapVal = map[actualGridRow][actualGridCol]


        if( mapVal == 1 or mapVal == 4):
            #hit a wall or enemy
            return False
        elif(isPlayerBullet and (mapVal == 'A' or mapVal == 'B')):
            #we hit an enemy
            #print('hit an enemy')
            return (actualGridRow, actualGridCol)
        elif(not isPlayerBullet and (mapVal == 'P')):
            #we hit an enemy
            #print('hit the player')
            return 'player'
        else:
            # print(self, 'traveling')
            self.x+=Bullet.calcLinearDx(self)
            self.y+=Bullet.calcLinearDy(self)
            return 'success'


    
    def findLocationOnScreenGrid(self):
        row = int(self.y // self.boxSize)
        col = int(self.x // self.boxSize)
        return (row, col)

    def calcLinearDx(self):
        return self.speed*math.cos(self.angle+math.pi)

    def calcLinearDy(self):
        return self.speed*math.sin(self.angle+math.pi)





class EnemyBullet(Bullet):
    def __init__(self, gridX, gridY, playerX, playerY, boxSize, angle, type):
        super().__init__(gridX, gridY, playerX, playerY, boxSize, angle)
        self.bulletSpeed = 40
        self.bulletLength = 45
        self.bulletWidth = 6
        self.color = EnemyBullet.decideColor(type)
        self.bulletDamage = 2


    colors = {
        'purple': "#3e236e",
        'orange': "#ffa90a"
    }

    def decideColor(type):
        chance = random.randint(0, 10)
        if(type == 'B'):
            purpleChance = 3
        else:
            purpleChance = 7

        if(chance > purpleChance):
            return 'purple'
        else:
            return 'orange'
        


    def __str__(self):
        return f'enemy bullet spawned at row {self.gridY}, col {self.gridX}'


    def redrawAll(self, canvas):
        radius = 20
        canvas.create_oval(self.x-radius, self.y-radius, self.x+radius, self.y+radius, fill=EnemyBullet.colors[self.color], width=0)





class PlayerBullet(Bullet):
    def __init__(self, gridX, gridY, playerX, playerY, boxSize, angle):
        super().__init__(gridX, gridY, playerX, playerY, boxSize, angle)
        self.bulletSpeed = 40
        self.bulletLength = 45
        self.bulletWidth = 6
        self.bulletDamage = 2
    def __str__(self):
        return f'player bullet spawned at row {self.gridY}, col {self.gridX}'



    def redrawAll(self, canvas):
        # x0 = self.x-self.bulletWidth/2
        # y0 = self.x-self.bulletLength/2

        # x1 = self.x+self.bulletWidth/2
        # y1 = self.x+self.bulletLength/2
        
        # x0,y0 = Moveable.do2dRotation(self.x, self.y, x0, y0, self.angle-self.theta)
        # x1,y1 = Moveable.do2dRotation(self.x, self.y, x1, y1, self.angle-self.theta)

        # # canvas.create_polygon(x0, y0,
        # #                         x1, y1,
        # #                         fill='white')
        # # canvas.create_rectangle(x0, y0,
        # #                         x1, y1,
        # #                         fill='white')
        radius = 8
        canvas.create_oval(self.x-radius, self.y-radius, self.x+radius, self.y+radius, fill='white', width=0)

        

    
    