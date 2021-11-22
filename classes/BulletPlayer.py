
from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable
from .Bullet import Bullet


class PlayerBullet(Bullet):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.bulletSpeed = 40
        self.bulletLength = 45
        self.bulletWidth = 6


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
        
        


