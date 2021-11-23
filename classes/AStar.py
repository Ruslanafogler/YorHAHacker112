#ref Nick Swift's medium blog on easy A* pathfinding
#https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#also ref Coder One on medium
#https://medium.com/coder-one/an-introduction-to-a-pathfinding-4c557b39cbbd 


#ref this github repo on data science medium article
#https://github.com/BaijayantaRoy/Medium-Article/blob/master/A_Star.ipynb 

#ryancollingwood bc he used queues
#https://gist.github.com/ryancollingwood/32446307e976a11a1185a5394d6657bc

#enemy coord to player

import heapq
import math



def createMap():
    
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
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self, other):
        return self.position == other.position

    # def __lt__(self, other):
    #     return self.f < other.f

    # def __gt__(self, other):
    #     return self.f > other.f

    

#backtracking for final path
def getPath(node):
    path = []
    currentNode = node
    while currentNode is not None:
        path.append(currentNode.position)
        currentNode = currentNode.parent
    return path[::-1]

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
    maxIterations = 3000

    if(allowDiagMoves):
        movements = [(1,0), (0, 1), (-1, 0), (0, -1), (1, 1),
            (-1, -1), (-1, 1), (1, -1)]
    else:
        movements = [(1,0), (0, 1), (-1, 0), (0, -1)]


    while(len(unVisitedList) > 0):
        iterations+=1

        if(iterations > maxIterations):
            print('exceeded iteration max, returning whatever we got')
            return getPath(currentNode)

        
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
        if(currentNode == endNode):
            path = getPath(currentNode)
            return path
        

        neighbors = []

        for possibleMove in movements:
            dx = possibleMove[0]
            dy = possibleMove[1]
            nodePositionX = currentNode.position[0] + dx
            nodePositionY = currentNode.position[1] + dy
            # print(nodePositionX, nodePositionY)
        
            #make sure its not a wall or off the map
            if(isLegalMove(map, nodePositionX, nodePositionY) == False):
                continue
            
            #create new node and add it the list of neighbors for cur node
            #Node creation -> (current, parent, position)
            newNode = Node(currentNode, (nodePositionX, nodePositionY))

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

            print('neighbor', neighbor.position, neighbor.f)

            #check if the neighbor is already in the unVisitedList and
            #the g cost is lower
            if(len([i for i in unVisitedList if i == neighbor 
            and neighbor.g > i.g ]) > 0):
                continue
            
            #ok, we can add the neighbor to our unVisitedList
            unVisitedList.append(neighbor)

            #back to the top of the while!
        
    #guess we couldn't find a path at all, huh..
    return None
        
def isLegalMove(map, nodePositionX, nodePositionY):
    # Make sure within range of the map
    if nodePositionX > (len(map) - 1) or nodePositionX < 0 or nodePositionY > (len(map[len(map)-1]) -1) or nodePositionY < 0:
        return False

    # Make sure there's an actual path there
    mapVal = map[nodePositionX][nodePositionY]
    if mapVal == 0 or mapVal == 'P':
        return True
    else:
        return False
        


def example(print_maze = True):

    
    map, player, enemyList = createMap()

    enemy = enemyList[2]

    print('a star time')
    print(enemy, player)

    path = aStar(map, enemy, player)

    if print_maze:
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

    print(path, 'for', enemy, 'to', player)



example()
        







    

