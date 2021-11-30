
from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable
from .config import COLORS

class Player(Moveable):
    def __init__(self, gridX, gridY, 
                offsetX, offsetY, boxSize, 
                health, maxHealth, powerUps=[]):
        super().__init__(gridX, gridY, boxSize)

        
        
        self.x = (gridX - offsetX)*boxSize + boxSize//2
        self.y = (gridY - offsetY)*boxSize+boxSize//2    
        #print('player class pos', gridX, gridY, self.x, self.y)
        self.angle = math.pi/2
        self.theta = math.pi/2
        self.health = health
        self.maxHealth = maxHealth
        self.color = 'white'
        

        #default dash range 3, dash cool down 25, shooting cool down 12
        
        self.dashRange = 3
        self.dashingColor = COLORS['red']
        self.isDashing = False
        self.dashingDuration = 0
        
        
        self.canDash = True
        self.dashingTimer = 0
        self.dashingCoolDown = 25

        self.canShoot = True
        self.shootingTimer = 0
        self.shootingCoolDown = 8 

        self.bulletDamage = 2


        self.bulletDamageCap = 25
        self.maxHealthCap = 150

        Player.applyPowerUps(self, powerUps)

        
        self.width = 18
        self.expWidth = 50
        self.centerDownLength = 20
        self.centerUpLength = 40
        self.scannerCircleR = 5

        self.dashingTriangleHeight = 60
        self.dashingTriangleWidth = 50
    
    def drawDashingAnimation(self, canvas, mouseX, mouseY):
        x0 = self.x - self.dashingTriangleWidth
        y0 = self.y + self.dashingTriangleHeight
        
        x1 = self.x
        y1 = self.y - self.dashingTriangleWidth
        
        x2 = self.x + self.dashingTriangleWidth
        y2 = self.y + self.dashingTriangleHeight

        x0,y0 = Moveable.do2dRotation(self.x, self.y, x0, y0, self.angle-self.theta)
        x1,y1 = Moveable.do2dRotation(self.x, self.y, x1, y1, self.angle-self.theta)
        x2,y2 = Moveable.do2dRotation(self.x, self.y, x2, y2, self.angle-self.theta)
        canvas.create_polygon(x0, y0,
                                x1, y1,
                                x2, y2,
                                fill=self.dashingColor)



    def getPowerUpAttr(self, typeOfPowerUp):
    
        if(typeOfPowerUp == 'BULLET_COOLDOWN'):
            return self.shootingCoolDown
        elif(typeOfPowerUp == 'BULLET_POWER_UP'):
            return self.bulletDamage
        elif(typeOfPowerUp == 'DASH_DISTANCE'):
            return self.dashRange 
        elif(typeOfPowerUp == 'DASH_COOLDOWN'):
            return self.dashingCoolDown
        elif(typeOfPowerUp == 'HP_RECOVER'):
            return self.health
        elif(typeOfPowerUp == 'HP_INCREASE'):
            return self.maxHealth


    def applyPowerUps(self, powerUps):
        
        for powerUp in powerUps:
            
            typeOfPowerUp = powerUp[0]
            parameter = powerUp[2]

            #argh this is so repetitive from above
            #please think of a bettesr way soon
            #without using enumerate or whatever bc I don't trust it
            
            if(typeOfPowerUp == 'BULLET_COOLDOWN'):
                self.shootingCoolDown = max(self.shootingCoolDown + parameter, 0)
            elif(typeOfPowerUp == 'BULLET_POWER_UP'):
                self.bulletDamage = min(self.bulletDamage + parameter, self.bulletDamageCap)
            elif(typeOfPowerUp == 'DASH_DISTANCE'):
                self.dashRange = min(self.dashRange + parameter, 5)
                if(self.dashRange == 4):
                    self.dashingColor = COLORS['green']
                elif(self.dashRange == 5):
                    self.dashingColor = COLORS['brightPurple']
            elif(typeOfPowerUp == 'DASH_COOLDOWN'):
                self.dashingCoolDown = max(self.dashingCoolDown + parameter, 0)
            elif(typeOfPowerUp == 'HP_RECOVER'):
                self.health = min(self.health + parameter, self.maxHealth)
            elif(typeOfPowerUp == 'HP_INCREASE'):
                self.maxHealth = min(self.maxHealth + parameter, self.maxHealthCap)
            
           

    def incTimers(self):
        self.dashingTimer+=1
        self.shootingTimer+=1







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
      
        if(self.isDashing):
            Player.drawDashingAnimation(self, canvas, mouseX, mouseY)
        
        canvas.create_polygon(x0, y0,
                                x1, y1,
                                x2, y2,
                                x3, y3, 
                                fill=self.color)
        canvas.create_oval(self.x-self.scannerCircleR, self.y-self.scannerCircleR,
                           self.x+self.scannerCircleR, self.y+self.scannerCircleR, fill=COLORS['darkgray'])

