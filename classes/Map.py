
from cmu_112_graphics import *
import math
import numpy as np

from .Player import Player
from .Enemy import Enemy
from .convertToGrid import convertToGrid
from .AStar import isLegalMove
from .RandomMapGen2 import getRandomMap, printMap
from .config import COLORS, LEVEL_BY_CHAMBER_COUNT



def determineEnemyNum(difficulty):
    #equation found with onlien curve fitting https://mycurvefit.com/
    #with pts (0, 2), (5, 4), (10, 4), (15, 6), (18, 9), (21, 10)      
    #y = 2.359863 + 0.07231715*x + 0.01421609*x^2
    x0 = 2.359863
    x1 = 0.07231715
    x2 = 0.01421609
    return x0 + x1*difficulty + x2*(difficulty**2)



def createMap(boxSize, difficulty):
    unparsedMap, state = getRandomMap(determineEnemyNum(difficulty))
    map = [([]*len(unparsedMap[0])) for row in range(len(unparsedMap))]

    enemyList = []
    

    for row in range(len(unparsedMap)):
        for col in range(len(unparsedMap[0])):
            elem = unparsedMap[row][col]
            if(elem == 'P'):
                playerPosition = (col, row)
            elif(elem == 'A' or elem == 'B'):
                    enemyList.append(Enemy(elem, col, row, boxSize, difficulty))
            
           
            if(isinstance(elem, str)):
                map[row].append((elem))
            else: 
                map[row].append(int(elem))

    #print("FROM FORMULA")    
    #printMap(map)


    return map, state, playerPosition, enemyList




def createMapFromFile(boxSize, difficulty):
    
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
                    enemyList.append(Enemy(elem, col, row, boxSize, difficulty))
            
           
            if(elem.isalpha()):
                map[row].append((elem))
            else: 
                map[row].append(int(elem))
            
    # map = [[int(col) 
    #             for col in row] 
    # #             for row in unparsedMap]
    f.close()
    print("FROM FILE")
    printMap(map)
    return map, playerPosition, enemyList


#dumb af stupid lazy stressed solution right here lol
#should just use numpy throughout the whole thing but ¯\_(ツ)_/¯
#ref website is numpy doc on shape and this:
#https://numpy.org/doc/stable/reference/generated/numpy.shape.html
#https://thispointer.com/how-to-get-numpy-array-dimensions-using-numpy-ndarray-shape-numpy-ndarray-size-in-python/
def getRowAndColLength(map):
    newList = np.array(map, dtype=object) 
    return newList.shape


 
class Map:
    def __init__(self, width, height, gridSize, boxSize, 
                 playerHealth, playerMaxHealth, playerPowerUps, 
                 difficulty):

        self.margin = 100
        self.width = width
        self.height = height
        #createMapFromFile was used to create map previously
        # self.map, self.playerPosition, self.enemyList = createMap(boxSize)
        self.map, self.state, self.playerPosition, self.enemyList = createMap(boxSize, difficulty)

        #print(getRowAndColLength(self.map))
        self.rowLength, self.colLength = getRowAndColLength(self.map)

        # print('player position', self.playerPosition)
        for enemy in self.enemyList:
            enemy.initMovements(self.map, self.playerPosition)

        
        self.gridSize = gridSize
        self.boxSize = boxSize
        self.offsetX = 0
        self.offsetY = 0
        Map.decideOffset(self)

        self.player = Player(self.playerPosition[0], self.playerPosition[1], 
                            self.offsetX, self.offsetY, boxSize, playerHealth, playerMaxHealth, playerPowerUps)

        self.maxRowIndex = self.height//boxSize+self.offsetY
        self.maxColIndex = self.width//boxSize+self.offsetX
        self.boxesDim = self.width//boxSize

        def determineDiff(difficulty):
            if(difficulty > LEVEL_BY_CHAMBER_COUNT[3]):
                return 3
            elif(difficulty > LEVEL_BY_CHAMBER_COUNT[2]):
                return 2
            elif(difficulty >= LEVEL_BY_CHAMBER_COUNT[1]):
                return 1


        self.colors = COLORS[f'LEVEL{determineDiff(difficulty)}']

        #print('maprange columns', self.offsetX, self.maxColIndex)
        #print('maprange rows', self.offsetY, self.maxRowIndex)

        

    def decideOffset(self):

        if(self.state == 'topLeft'):
            self.offsetX = 0
            self.offsetY = 0
        elif(self.state == 'topRight'):
            self.offsetX = self.colLength - 20
            self.offsetY = 0
        elif(self.state == 'bottomRight'):
            self.offsetX = self.colLength - 20
            self.offsetY = self.rowLength - 20
        else:
            self.offsetX = 0
            self.offsetY = self.rowLength - 20



    def enemyAutoTravel(self, enemy):
        enemy.movementIndex+=1
        Map.moveEnemy(self, enemy, enemy.getMovement())



    def moveEnemy(self, enemy, movement):
        #printMap(self)
        rowInc = movement[0]
        colInc = movement[1]
        newGridX = enemy.gridX + colInc
        newGridY = enemy.gridY + rowInc
        

        if(isLegalMove(self.map, newGridY, newGridX)):
            self.map[enemy.gridY][enemy.gridX] = 0
            self.map[newGridY][newGridX] = enemy.type
            enemy.move(colInc, rowInc)

        # else:
            #print('illegal move enemy')

        

    def gonnaHitWallPlayer(self, moveX, moveY):
        newPlayerCol = self.player.gridX+moveX
        newPlayerRow = self.player.gridY+moveY
        nextSpotValue = self.map[newPlayerRow][newPlayerCol]
        #print('player location', self.player.gridX, self.player.gridY)

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
                # self.player.gridX+=moveX
                # self.player.gridY+=moveY
                newGridX = self.player.gridX + moveX
                newGridY = self.player.gridY + moveY
                self.map[self.player.gridY][self.player.gridX] = 0
                self.map[newGridY][newGridX] = 'P' 
                self.player.gridX, self.player.gridY = newGridX, newGridY            
            else:
                self.player.move(moveX, moveY)
                for enemy in self.enemyList:
                    playerPosition = (self.player.gridY, self.player.gridX)
                    enemy.initMovements(self.map, playerPosition)
        else:
            return False
                    

    
    def changeViewOffset(self, dx, dy):
        # print("BTW, max row and col lengths", self.rowLength, self.colLength)
        #print(dx, dy)
        if(self.offsetX + dx >= 0 and 
           self.offsetY + dy >= 0 and
           self.maxRowIndex + dy <= self.rowLength and
           self.maxColIndex + dx <= self.colLength ):
           
           self.offsetX+=dx
           self.offsetY+=dy
           self.maxRowIndex+=dy
           self.maxColIndex+=dx

        #    print("VIEW CHANED")
        #    print('X: drawing cols from', self.offsetX, self.maxColIndex)
        #    print('Y: drawing rows frwom', self.offsetY, self.maxRowIndex)

           return True
        else:
            # print('X: drawing cols from', self.offsetX, self.maxColIndex)
            # print('Y: drawing rdows from', self.offsetY, self.maxRowIndex)
            return False
       


        # self.map = Map.setMap(self)


    def findEnemy(self, r, c):
        for enemy in self.enemyList:
            if(enemy.gridX == c and enemy.gridY == r):
                return enemy


    

###############################
#DRAWING FUNCTIONS

    def redrawAll(self, canvas, mouseX, mouseY):  
        Map.drawMap(self, canvas) 
        self.player.redrawAll(canvas, mouseX, mouseY)
    
    
    
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
                            Map.drawEnemyHealth(self, enemy, canvas)
                drawCol+=1
            drawRow+=1

                

    def drawEnemy(self, canvas, enemy, r, c):
        rowCoord = r*self.boxSize+self.boxSize//2
        colCoord = c*self.boxSize+self.boxSize//2

        enemy.x = rowCoord
        enemy.y = colCoord

        enemy.redrawAll(canvas, self.player.x, self.player.y)
        
        

    def drawBox(self, canvas, type, c, r):
        rowCoord = r*self.boxSize
        colCoord = c*self.boxSize
        if(type == 'obstacle'):
            width = 0
        else:
            width = 0
        
        canvas.create_rectangle(
        colCoord, rowCoord,
        colCoord + self.boxSize, rowCoord + self.boxSize,
        fill=self.colors[type],
        width = width
        )
        if(type == 'obstacle'):
            Map.drawObstacleShadow(self, canvas, colCoord, rowCoord, self.boxSize, width)

    
    def drawObstacleShadow(self, canvas, colCoord, rowCoord, boxSize, width):
            sideMargin = boxSize*0.08
            bottomMargin = boxSize*0.92
            canvas.create_rectangle(
            colCoord, rowCoord,
            colCoord + sideMargin, rowCoord + boxSize,
            fill=self.colors['shadow'],
            width = width
            )
            canvas.create_rectangle(
            colCoord, rowCoord+bottomMargin,
            colCoord + boxSize, rowCoord + boxSize,
            fill=self.colors['shadow'],
            width = width
            )





    #health container logic inspired from tech from tim's pygame tutorial
    #https://www.youtube.com/watch?v=jO6qQDNa2UY
    def drawPlayerHealth(self, canvas):
        healthDisplayLength = self.boxSize*10
        healthDisplayWidth = self.boxSize

        healthRectLen = self.boxSize*7
        healthRectWidth = 5

        textMargin = 20

        healthBarX0 = self.boxSize//2 + textMargin
        healthBarY0 = self.boxSize//2 - healthRectWidth

        healthBarX1 = self.boxSize//2+15 + healthRectLen
        healthBarY1 = self.boxSize//2 + healthRectWidth

        #white display box
        canvas.create_rectangle(0,0, healthDisplayLength, healthDisplayWidth, fill = '#ffffff', width=0)
        #hp text
        canvas.create_text(textMargin+self.boxSize//2, self.boxSize//2, text="HP:", font='Helvetica 14 bold')
        #max health container
        canvas.create_rectangle(textMargin+healthBarX0, healthBarY0, 
                                healthBarX1, healthBarY1, 
                                fill=self.colors['obstacle'], width=0)
        #actual health container
        if(self.player.health >= 0):
            #0.18 bc anything lower and the health bar starts going backwards when its too low
            fractionOfHealth = max(0.18, abs(self.player.health/self.player.maxHealth))
            if(fractionOfHealth > 0.3):
                textColor = 'black'
                color = COLORS['green']
            else: 
                textColor=COLORS['red']
                color = COLORS['red']
            canvas.create_text(healthBarX1+1.5*textMargin, self.boxSize//2, 
                                text=f"{self.player.health}/{self.player.maxHealth}",
                                fill=textColor,  font='Helvetica 14 bold')
            canvas.create_rectangle(textMargin+healthBarX0, healthBarY0, float(healthBarX1*fractionOfHealth), healthBarY1, fill=color, width=0)



    
    def drawEnemyHealth(self, enemy, canvas):
        healthRectLen = self.boxSize*1
        healthRectWidth = 50

        healthBarX0 = enemy.x+25
        healthBarY0 = enemy.y-25

        healthBarX1 = healthBarX0 + healthRectLen
        healthBarY1 = healthBarY0 + healthRectWidth
        
        
        #max health container
        canvas.create_rectangle(healthBarX0, healthBarY0, 
                                healthBarX1, healthBarY1, 
                                fill='#ffffff', width=0)

        #actual health container
        if(enemy.health >= 0):
            #0.18 bc anything lower and the health bar starts going backwards when its too low
            fractionOfHealth = max(0.2, abs(enemy.health/enemy.maxHealth))
            if(fractionOfHealth > 0.3):
                color = COLORS['green']
            else: 
                color = COLORS['red']
            canvas.create_rectangle(healthBarX0, healthBarY0, 
                                healthBarX0+fractionOfHealth*healthRectLen, healthBarY1, 
                                fill=color, width=0)
     




    
    
