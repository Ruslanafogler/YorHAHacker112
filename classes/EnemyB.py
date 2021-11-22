from cmu_112_graphics import *
import math
import numpy as np
from .Moveable import Moveable



class EnemyB(Moveable):
    def __init__(self, x, y, boxSize):
        super().__init__(x, y, boxSize)
        self.enemyR = 25
        

    def redrawAll(self, canvas):
        canvas.create_oval(self.x - self.enemyR, self.y-self.enemyR,
                    self.x + self.enemyR, self.y + self.enemyR, fill='#242526')