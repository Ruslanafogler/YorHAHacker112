


#referenced 112 TA Kian's idea on random rect + tunnel map gen + cellular auto obstacles
#(scrapped by previous random walk tunnel generation in tp2 because I didn't like it)

#Used these two articles for figuring out random rect & tunnel generation in a grid map
#  https://python.plainenglish.io/create-a-random-dungeon-with-python-f17118c1eebd
#glanced at this one a little:
#http://roguebasin.com/?title=A_Simple_Dungeon_Generator_for_Python_2_or_3


#cellular automata tutorial that I heavily relied on to randomly spawn obstacles in the map: 
# https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664

import random
import copy



#print map method referenced from ryancollingwood's astar github
#https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
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



def create2dList(defaultNum, rowDim, colDim, cellularAuto=False):
    map =[]
    initChance = 2
    margin = 2
    for r in range(rowDim):
        newRow = []
        for c in range(colDim):
            if(cellularAuto == True and 
            r >= margin 
            and r <= rowDim-margin 
            and c >= margin 
            and c <= colDim-margin):
                #either 1 or 0
                num = random.randint(0, 10)
                if(num <= initChance):
                    newRow.append(1)
                else:
                    newRow.append(0)
            else:
                newRow.append(defaultNum)
        map.append(newRow)
    return map



def initMap():
    map = []
    rowDim = 30
    colDim = 45
    map = create2dList(4, rowDim, colDim)
    return map, rowDim, colDim

#possible to land in any of the four corners
#of the map
class Room:
    def __init__(self, row, col, width, height):
        self.minRow = row
        self.minCol = col
        self.height = height
        self.width = width
        self.maxRow = row + height
        self.maxCol = col + width

        self.center = ((self.minRow+self.maxRow)//2, (self.minCol+self.maxCol)//2)

    def __str__(self):
        return f'room at rows {self.minRow} to {self.maxRow}, cols {self.minCol} to {self.maxCol}'

class RandomMapGenerator:

    def __init__(self, neededEnemyNum, mapMargin = 5):

        self.map, self.rowDim, self.colDim = initMap()
        self.mapMargin = mapMargin
        self.state = RandomMapGenerator.createStartingRoom(self)

        self.rooms = []
        self.totalRooms = random.randrange(3, 6)

        self.birthLimit = 4
        self.deathLimit = 6

        self.enemyNum = 0
        self.neededEnemyNum = neededEnemyNum




    def createStartingRoom(self):
        chance = {
            'topLeft': 2,
            'topRight': 4,
            'bottomRight': 6,
            'bottomLeft': 8
        }
        minSize = 5
        maxSize = 20

        self.startingRectWidth = random.randint(minSize, maxSize)
        self.startingRectHeight = random.randint(minSize, maxSize)

        rand = random.randint(0, 8)

        if(rand <= chance['topLeft']):
            self.state = 'topLeft'
        elif(rand <= chance['topRight']):
            self.state = 'topRight'
        elif(rand <= chance['bottomRight']):
            self.state = 'bottomRight'
        elif(rand <= chance['bottomLeft']):
            self.state = 'bottomLeft'
        
        return RandomMapGenerator.initStartingRoom(self)


    def initStartingRoom(self):
        rectMargin = self.mapMargin

        if(self.state == 'topLeft'):
            minRow = rectMargin
            minCol = rectMargin
            return Room(minRow, minCol, self.startingRectWidth, self.startingRectHeight)
        elif(self.state == 'topRight'):
            minRow = rectMargin
            minCol = self.colDim - rectMargin - self.startingRectWidth    
            return Room(minRow, minCol, self.startingRectWidth, self.startingRectHeight)   
        elif(self.state == 'bottomRight'):
            minRow = self.rowDim - rectMargin - self.startingRectHeight
            minCol = self.colDim - rectMargin - self.startingRectWidth
            return Room(minRow, minCol, self.startingRectWidth, self.startingRectHeight)
        else:
            minRow = self.rowDim - rectMargin - self.startingRectHeight 
            minCol = rectMargin
            return Room(minRow, minCol, self.startingRectWidth, self.startingRectHeight)

    def placePlayer(self):
        margin = self.mapMargin + 2
        if(self.state == 'topLeft'):
            self.map[margin][margin] = 'P'
        elif(self.state == 'topRight'):
            self.map[margin][self.colDim - margin] = 'P'
        elif(self.state == 'bottomRight'):
            self.map[self.rowDim - margin][self.colDim - margin] = 'P'
        else:
            self.map[self.rowDim - margin][margin] = 'P'


    def initRooms(self):
        mapMargin = 3
        
        minSize = 5
        maxSize = 20
        
        iterations = 0
        maxIterations = 600 


        self.rooms.append(RandomMapGenerator.createStartingRoom(self))

        while(len(self.rooms) < self.totalRooms):
            if(iterations > maxIterations):
                print('exceeded room count, gonna make rooms with what we got')
                break
            row = None
            col = None
            width = None
            height = None
            while(not RandomMapGenerator.isLegalRoom(self, row, col, width, height)):                
                row = random.randint(mapMargin, self.rowDim-mapMargin)
                col = random.randint(mapMargin, self.colDim-mapMargin)
                width = random.randint(minSize, maxSize)
                height = random.randint(minSize, maxSize)
            
        

            newRoom = Room(row, col, width, height)

            for otherRoom in self.rooms:
                if(RandomMapGenerator.isOverlapping(newRoom, otherRoom)):
                    pass

            #this means that we have created a successful room, time to tunnel

            if(len(self.rooms) != 0):
                prevCenter = self.rooms[len(self.rooms)-1].center
                newCenter = newRoom.center
                rand = random.randint(1, 2)
                if(rand == 1):
                    RandomMapGenerator.hTunnel(self, prevCenter[0], newCenter[0], prevCenter[1])
                    RandomMapGenerator.vTunnel(self, prevCenter[1], newCenter[1], newCenter[0])
                else:
                    RandomMapGenerator.hTunnel(self, prevCenter[0], newCenter[0], newCenter[1])
                    RandomMapGenerator.vTunnel(self, prevCenter[1], newCenter[1], prevCenter[0])
                    
            self.rooms.append(newRoom)
        
        newMap = RandomMapGenerator.createRooms(self, 2)

        
        RandomMapGenerator.placeEnemy(self, self.map, self.rowDim, self.colDim, 
                                    self.neededEnemyNum - self.enemyNum)



        return newMap


    #rowDim is 80, colDim is 50

    def isLegalRoom(self, row, col, width, height):
        if(row==None or col==None or width==None or height==None):
            return False
        if(row + height > self.rowDim - self.mapMargin or
            col + width > self.colDim - self.mapMargin):
            return False
        return True


    def isOverlapping(roomA, roomB):

        return (roomA.minRow <= roomB.maxRow and 
                roomB.maxRow >= roomA.minRow and
                roomA.minCol <= roomA.maxCol and
                roomB.maxCol >= roomA.minCol
                )


    def createRooms(self, steps):
        for room in self.rooms:
            roomMap = create2dList(0, room.height, room.width, True)

            for i in range(steps):
                roomMap = RandomMapGenerator.doSimulationStep(self, roomMap)

            roomMapR = -1
            roomMapC = -1
            for mapR in range(room.minRow, room.maxRow):
                roomMapR+=1
                for mapC in range(room.minCol, room.maxCol):
                    roomMapC+=1
                    self.map[mapR][mapC] = roomMap[roomMapR][roomMapC]
                roomMapC = -1

    def hTunnel(self, row1, row2, col):
        minRow = min(row1, row2)
        maxRow = max(row1, row2)

        for row in range(minRow, maxRow):
            self.map[row][col] = 0

    def vTunnel(self, col1, col2, row):
        minCol = min(col1, col2)
        maxCol = max(col1, col2)

        for col in range(minCol, maxCol):
            self.map[row][col] = 0


    def isOnMap(self, newRow, newCol):
        return (newRow < self.rowDim and newRow >= 0 and
                newCol < self.colDim and newCol >= 0)

    def doSimulationStep(self, roomMatrix):
        oldMap = copy.deepcopy(roomMatrix)
        rowDim = len(oldMap)
        colDim = len(oldMap[0])
        spawnedEnemy = False
        enemiesPerRoom = max(1, int(self.neededEnemyNum//self.totalRooms))

        
        def spawnEnemy(rand, spawnedEnemy):
            if rand <= enemyChance and spawnedEnemy == False:
                RandomMapGenerator.placeEnemy(self, roomMatrix, rowDim, colDim, 
                                            enemiesPerRoom)
                return True
        
        for r in range(3, rowDim-3):
            for c in range(3, colDim-3):
                n = RandomMapGenerator.livingNeighbors(self, r, c)
                enemyChance = 3
                rand = random.randint(0, 10)


                

                if(oldMap[r][c] == 1):
                    #this means its alive
                    if(n < self.deathLimit):
                        roomMatrix[r][c] = 1
                    else:
                        roomMatrix[r][c] = 0
                        spawnedEnemy = spawnEnemy(rand, spawnedEnemy)
                else:
                    #this means is dead
                    if(n > self.birthLimit):
                        roomMatrix[r][c] = 0
                        spawnedEnemy = spawnEnemy(rand, spawnedEnemy)
                    else:
                        roomMatrix[r][c] = 1
                
        return roomMatrix
                        


    def livingNeighbors(self, row, col):
        count = 0
        possibleMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), 
                (0, 1), (1, -1), (1,0), (1,1)]
        for move in possibleMoves:
            drow = row + move[0]
            dcol = col + move[1]

            #if its not on the map, its alive Ig(tho this condition shouldn't be checked?)
            if(not RandomMapGenerator.isOnMap(self, drow, dcol)):
                count+=1
            #if the value exists and is not 0, its alive
            elif(self.map[drow][dcol] != 0):
                count+=1
        return count

    def getEnemy():
        rand = random.randint(0, 1)
        if(rand == 1):
            return 'A'
        else:
            return 'B'

    def placeEnemy(self, map, rowDim, colDim, enemiesToAdd):
        limit = 5
        addedEnemies = 0
        for r in range(rowDim):
            for c in range(colDim):
                if(map[r][c] == 0):
                    n = RandomMapGenerator.livingNeighbors(self, r, c)
                    if(n > limit and addedEnemies < enemiesToAdd and self.enemyNum < self.neededEnemyNum):
                        map[r][c] = RandomMapGenerator.getEnemy()
                        self.enemyNum+=1
                        addedEnemies+=1

        



    def generateRandomMap(self):
        RandomMapGenerator.initRooms(self)
        



def getRandomMap(neededEnemyNum):
    dungeon = RandomMapGenerator(neededEnemyNum)
    dungeon.generateRandomMap()
    dungeon.placePlayer()
    print(dungeon.state)
    return dungeon.map, dungeon.state



# def testMapGen():
#     map = getRandomMap(4)
#     printMap(map[0])
    
# testMapGen()

