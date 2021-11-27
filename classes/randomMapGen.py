
import math
import random
import numpy as np


#referenced this free code camp website
#uses random walk to make random tunnels
# https://www.freecodecamp.org/news/how-to-make-your-own-procedural-dungeon-map-generator-using-the-random-walk-algorithm-e0085c8aa9a/ 

##*****************
#UNUSED. DON"T LOOKT AT THIS ONE. SEE RANDOMAPGEN2
##*****************
def printMap(map):
    
    for row in map:
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
            elif col == 4:
                line.append("|")
        print("".join(line))        




def create2dList(defaultNum, rowDim, colDim):
    result = []
    for r in range(rowDim):
        newRow = []
        for c in range(colDim):
            newRow.append(defaultNum)
        result.append(newRow)

    return result


def randomMapGen(allowDiagMoves = False):
    minRowColCount = 30
    minSurroundingMapCount = 3
    maxSurroudningMapCount = 9

    #random from 25 to 80
    rowDim, colDim = 25, 50

    maxTunnels = 50
    maxLength = 30

    genRectRoomChance = 7 #checked with a random from 0 to 10

    iterations = 0
    maxIterations = 2000

    map = create2dList(1, rowDim, colDim)

    #range of row/col selection is 3 to the end
    currentRow = random.randint(8, rowDim-8)
    currentCol = random.randint(15, colDim-15)

    if(allowDiagMoves):
        movements = [(1,0), (0, 1), (-1, 0), (0, -1), (1, 1),
            (-1, -1), (-1, 1), (1, -1)]
    else:
        movements = [(1,0), (0, 1), (-1, 0), (0, -1)]

    randomDirection = movements[random.randint(0, len(movements)-1)]
    lastDirection = (0,0)


    while(maxTunnels > 0 and rowDim > 0 and colDim > 0 and maxLength > 0):
        if(iterations > maxIterations):
            print('could not tunnel, returning map')
            return map

        #ensure that its going an actual direction somewhere
        #instead of going back in on its self or something
        while(randomDirection[0] == lastDirection[0] and
            randomDirection[1] == -lastDirection[1] or
            randomDirection[0] == lastDirection[0] and
            randomDirection[1] == lastDirection[1]):
            randomDirection = movements[random.randint(0, len(movements)-1)]

        randLength = random.randint(0, maxLength)
        tunnelLength = 0

        while(tunnelLength < randLength):
            
            #make sure we're not going off bounds based on
            #our cur location and whichever random direction
            #we are going
            if((currentRow == 0 and randomDirection[0] == -1) or
                (currentCol == 0 and randomDirection[1] == -1)  or
                (currentRow == rowDim -1 and randomDirection[0] == 1) or
                (currentCol == colDim -1 and randomDirection[1] == 1)):
                break
            else:
                map[currentRow][currentCol] = 0
                currentRow+=randomDirection[0]
                currentCol+=randomDirection[1]
                tunnelLength+=1
        if(tunnelLength >= 1):
            lastDirection = randomDirection
            maxTunnels-=1
        iterations+=1
    

    return map


        
def randomRectGen(map, row, col):
    minRow = -1
    minCol = -1
    maxRow = len(map) - 3
    maxCol = len(map[0]) - 3
    iterations = 0
    maxIterations = 50
    while(not isLegal(map, minRow, minCol, maxRow, maxCol)):
        minRow = row - random.randint(0, 10)
        minCol = col - random.randint(0, 10)
        if(iterations > maxIterations):
            print('gen rect would not work, returning')
            return
        iterations+=1

    randRowLen = random.randint(minRow, maxRow)
    randColLen = random.randint(minCol, maxCol)

    for r in range(minRow, randRowLen):
        for c in range(minRow, randColLen):
                map[r][c] = 0
    return map    



def isLegal(map, minRow, minCol, maxRow, maxCol):
    #off bounds
    if(minRow == None or minCol == None or
        minRow < 0 or minRow >= len(map) or 
        minCol < 0 or minCol >= len(map[0])):
        return False
   
    if(minRow >= maxRow-2 or minCol >= maxCol-2):
        return False

    return True



def placePlayer(map):
    for r in range(5, len(map)):
        for c in range(5,len(map[0])):
            if(map[r][c] == 0):
                map[r][c] = 'P'
                return

def getEnemy():
    chance = random.randint(0, 10)
    if(chance > 6):
        return 'B'
    else: return 'A'


def spawnEnemies(map, numberOfEnemies):
    enemySpawnRate = 15
    enemySpawnCoolDown = 0
    iterations = 0
    maxIterations = 800
    while(numberOfEnemies > 0):
        iterations+=1
        if(iterations > maxIterations):
            print('could not spawn all enemies, quitting')
            return
        for r in range(len(map)-3, 0, -1):
            for c in range(len(map[0])-3, 0, -1):
                if(map[r][c] == 0 and enemySpawnCoolDown > enemySpawnRate):
                    map[r][c] = getEnemy()
                    numberOfEnemies-=1
                    if(numberOfEnemies < 1):
                        return
                    enemySpawnCoolDown = 0
                enemySpawnCoolDown+=1

                    


def createRandomMap():
    map = randomMapGen()
    placePlayer(map)
    spawnEnemies(map, 3)

    return map



def testMapGen():
    print('testing')

    printMap(createRandomMap())
    print('end')



# testMapGen()







