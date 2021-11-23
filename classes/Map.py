
from cmu_112_graphics import *
import math
import numpy as np

from .Player import Player
from .Enemy import Enemy
from .convertToGrid import convertToGrid
from .AStar import isLegalMove
from .randomMapGen import createRandomMap


def createMap(boxSize):
    unparsedMap = createRandomMap()
    map = [([]*len(unparsedMap[0])) for row in range(len(unparsedMap))]

    enemyList = []
    

    for row in range(len(unparsedMap)):
        for col in range(len(unparsedMap[0])):
            elem = unparsedMap[row][col]
            if(elem == 'P'):
                playerPosition = (col, row)
            elif(elem == 'A' or elem == 'B'):
                    enemyList.append(Enemy(elem, playerPosition, col, row, boxSize))
            
           
            if(isinstance(elem, str)):
                map[row].append((elem))
            else: 
                map[row].append(int(elem))
    return map, playerPosition, enemyList



def createMapFromFile(boxSize):
    
    f = open('classes/map.txt')
    unparsedMap = f.read().split('\n')
    map = [([]*len(unparsedMap[0])) for row in range(len(unparsedMap))]
    enemyList = []
    # unparsedMap = createRandomMap()


    for row in range(len(unparsedMap)):
        for col in range(len(unparsedMap[row])):
            elem = unparsedMap[row][col]
           
            if(elem == 'P'):
                playerPosition = (col, row)
            elif(elem == 'A' or elem == 'B'):
                    enemyList.append(Enemy(elem, playerPosition, col, row, boxSize))
            
           
            if(elem.isalpha()):
                map[row].append((elem))
            else: 
                map[row].append(int(elem))
            
    # map = [[int(col) 
    #             for col in row] 
    # #             for row in unparsedMap]
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
        #createMapFromFile was used to create map previously
        self.map, self.playerPosition, self.enemyList = createMapFromFile(boxSize)

        print(getRowAndColLength(self.map))
        self.rowLength, self.colLength = getRowAndColLength(self.map)

        # print('player position', self.playerPosition)
        for enemy in self.enemyList:
            enemy.initMovements(self.map, self.playerPosition)


        # print("NEW MAP")
        # print(convertToGrid(self.map))

        self.player = Player(self.playerPosition[0], self.playerPosition[1], boxSize)


        
        self.gridSize = gridSize
        self.boxSize = boxSize
        self.offsetX = 0
        self.offsetY = 0


        self.maxRowIndex = self.width//boxSize+self.offsetY
        self.maxColIndex = self.height//boxSize+self.offsetX
        self.boxesDim = self.width//boxSize

        


    def enemyAutoTravel(self, enemy):
        enemy.movementIndex+=1
        Map.moveEnemy(self, enemy, enemy.getMovement())



    def moveEnemy(self, enemy, movement):
        #printMap(self)
        rowInc = movement[0]
        colInc = movement[1]
        newGridX = enemy.gridX + colInc
        newGridY = enemy.gridY + rowInc
        
        #print(enemy)
        if(isLegalMove(self.map, newGridY, newGridX)):
            self.map[enemy.gridY][enemy.gridX] = 0
            self.map[newGridY][newGridX] = enemy.type
            enemy.move(colInc, rowInc)
            #print(enemy)
            #printMap(self)
        # else:
            #print('illegal move enemy')

        

    def gonnaHitWallPlayer(self, moveX, moveY):
        newPlayerCol = self.player.gridX+moveX
        newPlayerRow = self.player.gridY+moveY
        nextSpotValue = self.map[newPlayerRow][newPlayerCol]
        print('player location', self.player.gridX, self.player.gridY)

        if(nextSpotValue == 1 or
        nextSpotValue == 4):
            return True
        else:
            return False

    def getGridLocation(app, i):
        return int(i // app.boxSize)
        

        

    def movePlayer(self, moveX, moveY):
        if(not Map.gonnaHitWallPlayer(self, moveX, moveY)):
            if(Map.changeViewOffset(self, moveX, moveY)):
                self.player.gridX+=moveX
                self.player.gridY+=moveY
            else:
                self.player.move(moveX, moveY)
                for enemy in self.enemyList:
                    playerPosition = (self.player.gridY, self.player.gridX)
                    enemy.initMovements(self.map, playerPosition)
                    

    
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


def printMap(self):
    
    for row in self.map:
        line = []
        for col in row:
            if col == 'P':
                line.append("P")
            elif col == 'B' or col == 'A':
                line.append("E")
            elif col == 1:
                line.append("\u2588")
            elif col == 0:
                line.append(" ")
            elif col == 2:
                line.append(".")
        print("".join(line))        




    
    
