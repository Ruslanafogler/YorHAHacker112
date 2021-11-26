
#referenced Kian's idea on random rect + tunnel map gen
#and also these two articles for dungeon rectangle and tunnels
# (I did one on random walk tunnels but I didn't like it so  I scrapped it lol) 
# https://gamedevelopment.tutsplus.com/tutorials/create-a-procedurally-generated-dungeon-cave-system--gamedev-10099
#and this one https://python.plainenglish.io/create-a-random-dungeon-with-python-f17118c1eebd

#glanced at this one a little:
#http://roguebasin.com/?title=A_Simple_Dungeon_Generator_for_Python_2_or_3


#cellular automata tutorial:

import random




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
    map =[]
    for r in range(rowDim):
        newRow = []
        for c in range(colDim):
            newRow.append(defaultNum)
        map.append(newRow)
    return map



def initMap():
    map = []
    rowDim = 80
    colDim = 50
    map = create2dList(4, rowDim, colDim)
    return map, rowDim, colDim

#possible to land in any of the four corners
#of the map
class Room:
    def __init__(self, row, col, width, height):
        self.minRow = row
        self.minCol = col
        self.maxRow = row + height
        self.maxCol = col + width

        self.center = ((self.minRow+self.maxRow)//2, (self.minCol+self.maxCol)//2)

    def __str__(self):
        return f'room at rows {self.minRow} to {self.maxRow}, cols {self.minCol} to {self.maxCol}'

class RandomMapGenerator:

    def __init__(self, mapMargin = 3):
        self.map, self.rowDim, self.colDim = initMap()
        self.mapMargin = 3
        self.state = RandomMapGenerator.createStartingRoom(self)
        self.deathLimit = 3
        self.birthLimit = 3



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
        print(rand)
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
        print(self.state)
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


    def initRooms(self):
        self.rooms=[]
        mapMargin = 3
        totalRooms = random.randrange(3, 6)
        
        minSize = 5
        maxSize = 20
        
        iterations = 0
        maxIterations = 600 


        self.rooms.append(RandomMapGenerator.createStartingRoom(self))

        while(len(self.rooms) < totalRooms):
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
        
        newMap = RandomMapGenerator.createRooms(self)
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


    def createRooms(self):

        # for i in range(steps):
        #     RandomMapGenerator.doSimulationStep(self)

        for room in self.rooms:
            # initMap()


            for r in range(room.minRow, room.maxRow):
                for c in range(room.minCol, room.maxCol):
                    self.map[r][c] = 0

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
        oldMap = roomMatrix
        for r in range(self.rowDim):
            for c in range(self.colDim):
                n = RandomMapGenerator.livingNeighbors(self, r, c)
                

                if(oldMap[r][c] != 1):
                    #it's alive(equal to 1 or 4, which is obstacle)
                    #if it's got 3 neighbors, kill it
                    if(n < self.deathLimit):
                        roomMatrix[r][c] = 1
                    else:
                        roomMatrix[r][c] = 0
                else:
                    #it's dead(equal to 0 and walkable space)
                    #if its got 1 or 2 neighbors, regen it  
                    if(n > self.birthLimit):
                        roomMatrix[r][c] = 0
                    else:
                        roomMatrix[r][c] = 1
                        


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
            #if the value exists and is 0, its alive
            elif(self.map[drow][dcol] == 4):
                count+=1
        return count



    def generateRandomMap(self, steps):
        RandomMapGenerator.initRooms(self)
        RandomMapGenerator.createRooms(self)





        



        



def testMapGen():
    dungeon = RandomMapGenerator()
    dungeon.generateRandomMap(2)
    printMap(dungeon.map)
    
testMapGen()

