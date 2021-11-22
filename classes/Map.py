
from cmu_112_graphics import *
import math
import numpy as np

from .Player import Player
from .EnemyA import EnemyA
from .EnemyB import EnemyB



def createMap(boxSize):
    
    f = open('classes/map.txt')
    unparsedMap = f.read().split('\n')
    map = [([]*len(unparsedMap[0])) for row in range(len(unparsedMap))]
    enemyList = []

    for row in range(len(unparsedMap)):
        for col in range(len(unparsedMap[row])):
            elem = unparsedMap[row][col]
            if(elem == 'P'):
                playerPosition = (col, row)
            elif(elem == 'A'):
                    enemyList.append(EnemyA(col, row, boxSize))
            elif(elem == 'B'):
                enemyList.append(EnemyB(col, row, boxSize))
            
            
            if(elem.isalpha()):
                map[row].append((elem))
            else: 
                map[row].append(int(elem))
            
    # map = [[int(col) 
    #             for col in row] 
    #             for row in unparsedMap]
    f.close()
    # print(map)
    return map, playerPosition, enemyList


#dumb af stupid lazy stressed solution right here lol
#should just use numpy throughout the whole thing but ¯\_(ツ)_/¯
#ref website is numpy doc on shape and this:
#https://numpy.org/doc/stable/reference/generated/numpy.shape.html
#https://thispointer.com/how-to-get-numpy-array-dimensions-using-numpy-ndarray-shape-numpy-ndarray-size-in-python/
def getRowAndColLength(daList):
    newList = np.array(daList, dtype=object) 
    return newList.shape






class Map:
    def __init__(self, width, height, gridSize, boxSize):
        self.margin = 100
        self.width = width
        self.height = height
        self.map, self.playerPosition, self.enemyList = createMap(boxSize)
        self.rowLength, self.colLength = getRowAndColLength(self.map)

        print('player position', self.playerPosition)
        print(self.enemyList)

        self.player = Player(self.playerPosition[0], self.playerPosition[1], boxSize)


        
        self.gridSize = gridSize
        self.boxSize = boxSize
        self.offsetX = 0
        self.offsetY = 0


        self.maxRowIndex = self.width//boxSize+self.offsetY
        self.maxColIndex = self.height//boxSize+self.offsetX
        self.boxesDim = self.width//boxSize

        


    def changeViewOffset(self, dx, dy):
        # print("BTW, max row and col lengths", self.rowLength, self.colLength)

        if(self.offsetX + dx >= 0 and 
           self.offsetY + dy >= 0 and
           self.maxRowIndex + dy < self.rowLength and
           self.maxColIndex + dx < self.colLength ):
           
           self.offsetX+=dx
           self.offsetY+=dy
           self.maxRowIndex+=dy
           self.maxColIndex+=dx

           
        #    print('X: drawing cols from', self.offsetX, self.maxColIndex)
        #    print('Y: drawing rows from', self.offsetY, self.maxRowIndex)

           return True
        else:
            # print('X: drawing cols from', self.offsetX, self.maxColIndex)
            # print('Y: drawing rows from', self.offsetY, self.maxRowIndex)
            return False
       


        # self.map = Map.setMap(self)




    def findEnemy(self, r, c):
        for enemy in self.enemyList:
            if(enemy.gridX == c and enemy.gridY == r):
                return enemy


    def drawMap(self, canvas):
        drawRow = 0
        for r in range(self.offsetY, self.maxRowIndex):
            drawCol = 0
            for c in range(self.offsetX, self.maxColIndex):
                val = self.map[r][c]                  
                if(val == 4):
                    Map.drawBox(self, canvas, 'offMap', drawCol, drawRow)
                elif(val == 1):
                    Map.drawBox(self, canvas, 'obstacle', drawCol, drawRow)
                else:
                    Map.drawBox(self, canvas, 'onMap', drawCol, drawRow)
                    if(val == 'A' or val == 'B'):
                        enemy = Map.findEnemy(self, r, c)
                        if(enemy):
                            Map.drawEnemy(self, canvas, enemy, drawCol, drawRow)


                    

                drawCol+=1
            drawRow+=1

    def drawEnemies(self, canvas):
        for enemy in self.enemyList:
            enemy.redrawAll(canvas)



    

    def redrawAll(self, canvas, mouseX, mouseY):  
        Map.drawMap(self, canvas) 
        self.player.redrawAll(canvas, mouseX, mouseY)
                


    colors = {
        'offMap': '#817b69',
        'onMap': '#beb99c',
        'obstacle': '#dad3c5'
    }

    def drawEnemy(self, canvas, enemy, r, c):
        rowCoord = r*self.boxSize+self.boxSize//2
        colCoord = c*self.boxSize+self.boxSize//2

        enemy.x = rowCoord
        enemy.y = colCoord

        enemy.redrawAll(canvas)
        
        

    def drawBox(self, canvas, type, c, r):
        rowCoord = r*self.boxSize
        colCoord = c*self.boxSize
        if(type == 'obstacle'):
            width = 2
        else:
            width = 0
        
        canvas.create_rectangle(
        colCoord, rowCoord,
        colCoord + self.boxSize, rowCoord + self.boxSize,
        fill=Map.colors[type],
        width = width
        )




    
    
