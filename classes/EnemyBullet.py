
from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable
from .Bullet import Bullet


#OBSOLETE, see bullet class for this
class EnemyBullet(Bullet):
    def __init__(self, gridX, gridY, playerX, playerY, boxSize, angle, color):
        super().__init__(gridX, gridY, playerX, playerY, boxSize, angle)
        self.bulletSpeed = 40
        self.bulletLength = 45
        self.bulletWidth = 6
        self.color = color


    colors = {
        'purple': "#3e236e",
        'orange': "#ffa90a"
    }


    def redrawAll(self, canvas):
        radius = 30
        canvas.create_oval(self.x-radius, self.y-radius, self.x+radius, self.y+radius, fill=EnemyBullet.colors[self.color], width=0)
        
        


