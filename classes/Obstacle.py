from cmu_112_graphics import *
import math
import numpy as np

class Obstacle:
    def __init__(self, x, y, boxSize, color):
        self.color = color
        self.rowX = x
        self.rowY = y
        self.x = x*boxSize
        self.y = y*boxSize
        self.boxSize = boxSize

    def redrawAll(self, canvas):
        canvas.create_rectangle(
            self.x, self.y,
            self.x+self.boxSize, self.y+ self.boxSize,
            fill=self.color,
            width = 2
        )


    
