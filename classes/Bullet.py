
from cmu_112_graphics import *
import math
import numpy as np


#referenced Rabbid76's stackoverflow answer here
#https://stackoverflow.com/questions/59977052/shooting-a-bullet-in-pygame-in-the-direction-of-mouse

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y 
        self.speed = 45
        self.angle = angle
        self.theta = math.pi/2

    def linearTravel(self):
        self.x+=self.speed*math.cos(self.angle+math.pi)
        self.y+=self.speed*math.sin(self.angle+math.pi)
    
    