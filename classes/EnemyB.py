from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable



class EnemyB(Moveable):
    def __init__(self, gridX, gridY, boxSize):
        super().__init__(gridX, gridY, boxSize)
        self.x = self.gridX*self.boxSize + self.boxSize//2
        self.y = self.gridY*self.boxSize + self.boxSize//2
        self.enemyR = 25

    def __str__(self):
        return f'enemyA row coords, coords {self.gridX}, {self.gridY}, {self.x}, {self.y}'

        

    def redrawAll(self, canvas):
        canvas.create_oval(self.x - self.enemyR, self.y-self.enemyR,
                    self.x + self.enemyR, self.y + self.enemyR, fill='#242526')