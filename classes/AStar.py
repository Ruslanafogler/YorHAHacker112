#ref Nick Swift's medium blog on easy A* pathfinding
#https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#also ref Coder One on medium
#https://medium.com/coder-one/an-introduction-to-a-pathfinding-4c557b39cbbd 


#ref this github repo on data science medium article
#https://github.com/BaijayantaRoy/Medium-Article/blob/master/A_Star.ipynb 


#ok ngl I used these ones the most by far, way more than ^^
#heavily referred to their A-star structure and methods
#https://github.com/BaijayantaRoy/Medium-Article/blob/master/A_Star.ipynb 
#Sebasitian Joy's channel
#https://www.youtube.com/watch?v=-L-WgKMFuhE&t=391s


#enemy coord to player

import heapq
import math


#this method was adopted from daFluffyPotato's vid on map generation in video games
#https://www.youtube.com/watch?v=gE2gTCwLdFM 
def createTestMap():
    
    f = open('map.txt')
    unparsedMap = f.read().split('\n')
    map = [([]*len(unparsedMap[0])) for row in range(len(unparsedMap))]
    enemyList = []

    for row in range(len(unparsedMap)):
        for col in range(len(unparsedMap[row])):
            elem = unparsedMap[row][col]
            if(elem == 'P'):
                playerPosition = (row, col)
            elif(elem == 'A'):
                    enemyList.append((row, col))
            elif(elem == 'B'):
                enemyList.append((row, col))
            
            
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


class Node:
    def __init__(self, parent=None, position=None, movement=None):
        self.parent = parent
        self.position = position
        self.movement = movement

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        return f'Node with position: {self.position}, movement:{self.movement}'

    # def __lt__(self, other):
    #     return self.f < other.f

    # def __gt__(self, other):
    #     return self.f > other.f

    

#obtaining the final path by going back through the path of nodes
def getPath(node):
    path = []
    currentNode = node
    while currentNode is not None:
        path.append(currentNode.position)
        currentNode = currentNode.parent
    return path[::-1]

#getting the movements(each as tuples) that the enemy makes to get to their final destination
#by going back up through the path of nodes
def getMovements(node):
    movements = []
    currentNode = node
    while currentNode is not None:
        movements.append(currentNode.movement)
        currentNode = currentNode.parent
    movements = movements[::-1]
    #don't include first, because first node's parent is None
    return movements[1::]

#heursitic -- euclidean in this case
def getDistance(a,b):
    (x1, y1) = a
    (x2, y2) = b

    return (x1-x2)**2 + (y1-y2)**2


def aStar(map, start, end, allowDiagMoves = False):

    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0
    
    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0

    unVisitedList = []
    visitedList = []

    #add startNode to the unVisitedList
    unVisitedList.append(startNode)
    

    #stop condition so it won't be doing this forever
    iterations = 0
    maxIterations = 1500

    if(allowDiagMoves):
        movements = [(1,0), (0, 1), (-1, 0), (0, -1), (1, 1),
            (-1, -1), (-1, 1), (1, -1)]
    else:
        movements = [(1,0), (0, 1), (-1, 0), (0, -1)]


    while(len(unVisitedList) > 0):
        iterations+=1

        if(iterations > maxIterations):
            #print('exceeded iteration max, returning whatever we got')
            #return getPath(currentNode)
            return getMovements(currentNode)

        
        #get the node with the least f and set that as our current node

        currentNode = unVisitedList[0]
        currentIndex = 0

        #enumerate documentatino on real python
        #https://realpython.com/python-enumerate/
        for index, node in enumerate(unVisitedList):
            if(node.f < currentNode.f):
                currentNode = node
                currentIndex = index

        #remove our currentNode and put in on the visited list
        unVisitedList.pop(currentIndex)
        visitedList.append(currentNode)


        #we found the player. Return the path

        #usually checks if currentNode == endNode
        #HOWEVER I want the enemy to stop a distance away from the player
        if(currentNode.f != 0 and currentNode.f < 30):
            # print("DISTANCES", currentNode.f)
            # path = getPath(currentNode)
            # return path
            return getMovements(currentNode)

        

        neighbors = []

        for possibleMove in movements:
            dx = possibleMove[0]
            dy = possibleMove[1]
            rowInc = currentNode.position[0] + dx
            colInc = currentNode.position[1] + dy
            # print(rowInc, colInc)
        
            #make sure its not a wall or off the map
            if(isLegalMove(map, rowInc, colInc) == False):
                continue
            
            #create new node and add it the list of neighbors for cur node
            #Node creation -> (current, parent, position)
            newNode = Node(currentNode, (rowInc, colInc), (dx, dy))

            neighbors.append(newNode)

        #loop through neighbors and find the best!
        for neighbor in neighbors:
            #horrible one line way of checking if 
            #we see neighbor in the visited list, bc
            #we do not want to go back the way we came
            #(basically generates a list of every neighbor that's in visited,
            # and sees if that list is bigger than 0 or not)

            if(len([visitedNeighbor for visitedNeighbor in visitedList if visitedNeighbor == neighbor]) > 0):
                continue

            #get the g, h, f values

            neighbor.g = currentNode.g + 1
            
            #uses euclidean distance as heuristic here(func up above)
            neighbor.h = getDistance(neighbor.position, end)

            neighbor.f = neighbor.g + neighbor.h

            # print('neighbor', neighbor.position, neighbor.f)

            #check if you've already gone to the tile before
            #and if you're taking an extra step than before(g cost)
            if(len([node for node in unVisitedList if node == neighbor 
            and neighbor.g > node.g ]) > 0):
                continue
            
            #ok, we can add the neighbor to our unVisitedList
            unVisitedList.append(neighbor)

            #back to the top of the while!
        
    #guess we couldn't find a path at all, huh..
    return None
        
def isLegalMove(map, rowInc, colInc):
    # Make sure within range of the map
    if rowInc > (len(map) - 1) or rowInc < 0 or colInc > (len(map[len(map)-1]) -1) or colInc < 0:
        return False

    # Make sure there's an actual path there
    mapVal = map[rowInc][colInc]
    if mapVal == 0 or mapVal == 'P':
        return True
    else:
        return False
        
#print map method referenced from ryancollingwood's astar github
#https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc
def printMap(map, path):
    for step in path:
        map[step[0]][step[1]] = 2
    
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
            elif col == 2:
                line.append(".")
        print("".join(line))

def testAStar(print_maze = True):
    
    map, player, enemyList = createTestMap()

    enemy = enemyList[0]

    print('a star time')
    print(enemy, player)

    #path
    movements = aStar(map, enemy, player)

    # if print_maze:
    #     printMap(map, path)


    print(movements, 'for', enemy, 'to', player)
    print('\n\n\n')
    print(movements)



# testAStar()
        







    

