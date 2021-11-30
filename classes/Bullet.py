
from cmu_112_graphics import *
import math
import random
from .config import COLORS


#referenced Rabbid76's stackoverflow answer here
#https://stackoverflow.com/questions/59977052/shooting-a-bullet-in-pygame-in-the-direction-of-mouse

#contains bullet, playerbullet, enemybullet classes

class Bullet:
    def __init__(self, playerX, playerY, boxSize, angle, speed=35):
        
        self.x = playerX
        self.y = playerY    
        
        self.speed = speed
        self.angle = angle
        self.theta = math.pi/2
        self.boxSize = boxSize
  
  
    def damage(self, other):
        other.health-=self.bulletDamage
        print(other, other.health)      


    def isLegalIndex(map, row, col):
        if(row < 0 or row >= len(map) or col < 0 or col >= len(map[0])):
            return False
        else:
            return True


    
    def linearTravel(self, map, minRowScreen, minColScreen, isPlayerBullet):
        bulletScreenRow, bulletScreenCol = Bullet.findLocationOnScreenGrid(self)
        actualGridRow, actualGridCol = bulletScreenRow+minRowScreen, bulletScreenCol+minColScreen
        if(not Bullet.isLegalIndex(map, actualGridRow, actualGridCol)):
            return   
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
            self.x+=Bullet.calcLinearDx(self, self.angle+math.pi)
            self.y+=Bullet.calcLinearDy(self, self.angle+math.pi)
            return 'success'


    
    def findLocationOnScreenGrid(self):
        row = int(self.y // self.boxSize)
        col = int(self.x // self.boxSize)
        return (row, col)

    def calcLinearDx(self, angle):
        return self.speed*math.cos(angle)

    def calcLinearDy(self, angle):
        return self.speed*math.sin(angle)





class EnemyBullet(Bullet):
    def __init__(self, playerX, playerY, boxSize, angle, type):
        super().__init__(playerX, playerY, boxSize, angle)
        self.bulletSpeed = 40
        self.bulletLength = 45
        self.bulletWidth = 6
        self.color = EnemyBullet.decideColor(type)
        self.bulletDamage = 2


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
        canvas.create_oval(self.x-radius, self.y-radius, 
                            self.x+radius, self.y+radius, 
                            fill=COLORS[self.color], width=0)





class PlayerBullet(Bullet):
    def __init__(self, playerX, playerY, boxSize, angle, bulletDamage=2):
        super().__init__(playerX, playerY, boxSize, angle)
        self.bulletSpeed = 40
        self.bulletLength = 45
        self.bulletWidth = 6
        self.bulletDamage = bulletDamage
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

        

    
    