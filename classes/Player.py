
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

        self.angle = math.pi/2
        self.theta = math.pi/2
        self.health = health
        self.maxHealth = maxHealth
        self.color = 'white'
        
        self.hit = False
        self.hitTimer = 0

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


        self.caps = {
            'BULLET_COOLDOWN': 0,
            "BULLET_POWER_UP": 25,
            'DASH_DISTANCE': 5,
            'DASH_COOLDOWN': 0,
            'HP_RECOVER': self.maxHealth,
            'HP_INCREASE': 150
        }

        self.powerUps = dict()
        Player.applyPowerUps(self, powerUps)

        
        #parameters for drawing stuff
        self.width = 18
        self.expWidth = 50
        self.centerDownLength = 20
        self.centerUpLength = 40
        self.scannerCircleR = 5

        self.squareWidth = 7
        self.squareHeight = 10
        self.squareDistanceFar = 20
        self.squareShadowDropDown = 4

        self.shadowMargin = 2
        self.shadowDropDown = 6


        self.dashingTriangleHeight = 60
        self.dashingTriangleWidth = 50
    


    def storePlayerPowerUps(self, powerUps):
        for powerUp in powerUps:
            type = powerUp[0]
            parameter = powerUp[1]
            self.powerUps[type] = self.powerUps.get(type, 0) + parameter

    

    def applyPowerUps(self, powerUps):
        
        for powerUp in powerUps:
            
            typeOfPowerUp = powerUp[0]
            parameter = powerUp[2]
            cap = self.caps[typeOfPowerUp]

            
            if(typeOfPowerUp == 'BULLET_COOLDOWN'):
                self.shootingCoolDown = max(self.shootingCoolDown + parameter, cap)
            elif(typeOfPowerUp == 'BULLET_POWER_UP'):
                self.bulletDamage = min(self.bulletDamage + parameter, cap)
            elif(typeOfPowerUp == 'DASH_DISTANCE'):
                self.dashRange = min(self.dashRange + parameter, cap)
                if(self.dashRange == 4):
                    self.dashingColor = COLORS['green']
                elif(self.dashRange == 5):
                    self.dashingColor = COLORS['brightpurple']
            elif(typeOfPowerUp == 'DASH_COOLDOWN'):
                self.dashingCoolDown = max(self.dashingCoolDown + parameter, cap)
            elif(typeOfPowerUp == 'HP_RECOVER'):
                self.health = min(self.health + parameter, cap)
                self.powerUps['HP_RECOVER'] = 0
            elif(typeOfPowerUp == 'HP_INCREASE'):
                self.maxHealth = min(self.maxHealth + parameter, cap)
            
           


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

    
    def setPlayerColor(self):
        self.color = 'white'


    def onHit(self):
        if(self.hit):
           self.color = COLORS['mediumgray']
        else:
            Player.setPlayerColor(self)    
    
    def incTimers(self):
        self.dashingTimer+=1
        self.shootingTimer+=1








    def redrawAll(self, canvas, mouseX, mouseY):
        Moveable.getAngle(self, mouseX, mouseY)
        # canvas.create_line(self.x,self.y,mouseX,mouseY)
        if(self.isDashing):
            Player.drawDashingAnimation(self, canvas)
        Player.drawPlayer(self, canvas)


    #player appearance inspird by Nier's scanner object look
    def drawPlayer(self, canvas):

        x0 = self.x - self.width
        y0 = self.y
        x1 = self.x
        y1 = self.y - self.centerUpLength
        x2 = self.x + self.width
        y2 = self.y
        x3 = self.x
        y3 = self.y + self.centerDownLength

        box1x0 = self.x - self.squareDistanceFar
        box1y0 = self.y + self.squareHeight
        box1x1 = box1x0 + self.squareWidth
        box1y1 = box1y0 + self.squareWidth

        box2x0 = self.x + self.squareDistanceFar
        box2y0 = self.y + self.squareHeight
        box2x1 = box2x0 + self.squareWidth
        box2y1 = box2y0 + self.squareWidth  


        shadow1x0 = self.x - self.width
        shadow1y0 = self.y + self.shadowMargin
        shadow1x1 = self.x
        shadow1y1 = self.y + self.centerDownLength + self.shadowMargin
        shadow1x2 = shadow1x1
        shadow1y2 = shadow1y1 + self.shadowDropDown
        shadow1x3 = shadow1x0
        shadow1y3 = shadow1y0 + self.shadowDropDown

        shadow2x0 = self.x + self.width
        shadow2y0 = self.y + self.shadowMargin
        shadow2x1 = self.x
        shadow2y1 = self.y + self.centerDownLength + self.shadowMargin
        shadow2x2 =shadow2x1
        shadow2y2 =shadow2y1 + self.shadowDropDown
        shadow2x3 =shadow2x0
        shadow2y3 =shadow2y0 + self.shadowDropDown
        


        x0,y0 = Moveable.do2dRotation(self.x, self.y, x0, y0, self.angle-self.theta)
        x1,y1 = Moveable.do2dRotation(self.x, self.y, x1, y1, self.angle-self.theta)
        x2,y2 = Moveable.do2dRotation(self.x, self.y, x2, y2, self.angle-self.theta)
        x3,y3 = Moveable.do2dRotation(self.x, self.y, x3, y3, self.angle-self.theta)

        box1x0,box1y0 = Moveable.do2dRotation(self.x, self.y, box1x0, box1y0, self.angle-self.theta)
        box1x1,box1y1 = Moveable.do2dRotation(self.x, self.y, box1x1, box1y1, self.angle-self.theta)
        box2x0,box2y0 = Moveable.do2dRotation(self.x, self.y, box2x0, box2y0, self.angle-self.theta)
        box2x1,box2y1 = Moveable.do2dRotation(self.x, self.y, box2x1, box2y1, self.angle-self.theta)

        shadow1x0,shadow1y0 = Moveable.do2dRotation(self.x, self.y, shadow1x0, shadow1y0, self.angle-self.theta)
        shadow1x1,shadow1y1 = Moveable.do2dRotation(self.x, self.y, shadow1x1, shadow1y1, self.angle-self.theta)
        shadow1x2,shadow1y2 = Moveable.do2dRotation(self.x, self.y, shadow1x2, shadow1y2, self.angle-self.theta)
        shadow1x3,shadow1y3 = Moveable.do2dRotation(self.x, self.y, shadow1x3, shadow1y3, self.angle-self.theta)
        
        shadow2x0,shadow2y0 = Moveable.do2dRotation(self.x, self.y, shadow2x0, shadow2y0, self.angle-self.theta)
        shadow2x1,shadow2y1 = Moveable.do2dRotation(self.x, self.y, shadow2x1, shadow2y1, self.angle-self.theta)
        shadow2x2,shadow2y2 = Moveable.do2dRotation(self.x, self.y, shadow2x2, shadow2y2, self.angle-self.theta)
        shadow2x3,shadow2y3 = Moveable.do2dRotation(self.x, self.y, shadow2x3, shadow2y3, self.angle-self.theta)
        
        canvas.create_polygon(x0, y0,
                                x1, y1,
                                x2, y2,
                                x3, y3, 
                                fill=self.color)

        canvas.create_polygon(shadow1x0, shadow1y0,
                              shadow1x1, shadow1y1,
                              shadow1x2, shadow1y2,
                              shadow1x3, shadow1y3,
                         fill=COLORS['lightgray'])
        canvas.create_polygon(shadow2x0, shadow2y0,
                              shadow2x1, shadow2y1,
                              shadow2x2, shadow2y2,
                              shadow2x3, shadow2y3,
                                fill=COLORS['lightgray'])   

        canvas.create_rectangle(box1x0, box1y0,
                                box1x1, box1y1,
                                fill=self.color, width=0)
        canvas.create_rectangle(box2x0, box2y0,
                                box2x1, box2y1,
                                fill=self.color, width=0)                                        
        
        canvas.create_oval(self.x-self.scannerCircleR, self.y-self.scannerCircleR,
                           self.x+self.scannerCircleR, self.y+self.scannerCircleR, fill=COLORS['darkgray'])        



    #dashing mechanic inspired by Hades spacebar dashing move
    def drawDashingAnimation(self, canvas):
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
