
from cmu_112_graphics import *
import math
import numpy as np

from .MapGrid import convertMapToGrid
from .Player import Player
from .EnemyA import EnemyA
from .EnemyB import EnemyB



def createMap():
    
    f = open('classes/map.txt')
    unparsedMap = f.read().split('\n')
    map = [([]*len(unparsedMap[0])) for row in range(len(unparsedMap))]
    
    for row in range(len(unparsedMap)):
        for col in range(len(unparsedMap[row])):
            if(unparsedMap[row][col] == 'P'):
                playerPosition = (row, col)
                map[row].append('P')
            else:
                map[row].append(int(unparsedMap[row][col]))
            
    # map = [[int(col) 
    #             for col in row] 
    #             for row in unparsedMap]
    f.close()
    # print(map)
    return map, playerPosition


class Map:
    def __init__(self, width, height, gridSize, boxSize):
        self.margin = 100
        self.width = width
        self.height = height
        self.map, self.playerPosition = createMap()

        print('player position', self.playerPosition)

        self.player = Player(self.playerPosition[0], self.playerPosition[1], boxSize)

        
        self.gridSize = gridSize
        self.boxSize = boxSize
        self.offsetX = 0
        self.offsetY = 0


        self.maxRowIndex = self.width//boxSize+self.offsetY
        self.maxColIndex = self.height//boxSize+self.offsetX
        self.boxesDim = self.width//boxSize

        
        #print(self.map)
        

       


    # def setMap(self):
    #     self.map = createMap(self.offsetX, self.offsetY, 
    #                         self.maxRowIndex, self.maxColIndex)
    #     print('NEW MAP', self.map)

    # def getColNum(matrix):
    #     for r in len(matrix):
    #         for c in len(matrix[])


    def changeViewOffset(self, dx, dy, playerRow, playerCol):
        
        if(self.offsetX + dx >= 0 and 
           self.offsetY + dy >= 0 and
           self.maxRowIndex + dx < len(self.map[playerCol]) and
           self.maxColIndex + dy < 100 ):
           
           self.offsetX+=dx
           self.offsetY+=dy
           self.maxRowIndex+=dy
           self.maxColIndex+=dx
           print('drawing rows from', self.offsetX, self.maxRowIndex)
           print('drawing cols from', self.offsetY, self.maxColIndex)

           return True
        else:
            print('drawing rows from', self.offsetX, self.maxRowIndex)
            print('drawing cols from', self.offsetY, self.maxColIndex)
            return False
       


        # self.map = Map.setMap(self)

    

    def redrawAll(self, canvas, mouseX, mouseY):        
        drawBoxRow = 0
        
        for r in range(self.offsetY, self.maxRowIndex):
            drawColRow = 0
            for c in range(self.offsetX, self.maxColIndex):                  
                if(self.map[r][c] == 4):
                    Map.drawBox(self, canvas, 'offMap', drawBoxRow, drawColRow)
                elif(self.map[r][c] == 0 or self.map[r][c] == 'P'):
                    Map.drawBox(self, canvas, 'onMap', drawBoxRow, drawColRow)
                elif(self.map[r][c] == 1):
                    Map.drawBox(self, canvas, 'obstacle', drawBoxRow, drawColRow)
                drawColRow+=1

            drawBoxRow+=1
        self.player.redrawAll(canvas, mouseX, mouseY)
                


    colors = {
        'offMap': '#817b69',
        'onMap': '#beb99c',
        'obstacle': '#dad3c5'
    }

    def drawBox(self, canvas, type, r, c):
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


    
    
