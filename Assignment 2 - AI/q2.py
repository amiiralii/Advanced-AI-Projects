# This library is only used for reading the arguments of the command
import sys
# Used for deepcopy the list of keys, so that we can update them for each path individualy
import copy

# Returns a 2d array representing the board
# Paramethers are fileName which is the name of file which contains the board's data, 
# and algorithm that determines the directory of input file
def readBoardFromFile(fileName, algorithm):
    # Start using the input file
    inputFile = open("Q2/Mazes/" + algorithm + "/" + fileName, "r")

    # Creating a 2d list that keeps the board information
    board = []

    line = inputFile.readline()
    while (line):
        # Reading new line and split it to 2 items
        inputRow = line.strip().split(",")
        board.append(inputRow)
        line = inputFile.readline()
    return board

# Returns the location of Harry
# The only paramethher is the game board
def findHarry(board):
    # looking for harry
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j] == 'H'):
                return i,j

# Returns a list that contains the location of keys
# The only paramethher is the game board
def findKeys(board):
    keys = []
    # looking for keys
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j] == 'K'):
                keys.append([i, j, 0])
    return keys

## Check whether a path that is chosen by the algorithm is already explored or not.
## Returns True or False            
## Parameters are start and end point of a suggested path and a list of already visited nodes        
def is_visited(start, end, visited):
    # Identify whether the path is vertical or horizontal
    if start[1] == end[1]:
        # Vertical Path
        # Identify whether the path is upward or downward
        if start[0] < end[0]:
            # Downward path
            for i in range(start[0]+1, end[0]+1):
                if ([i, start[1]] in visited):
                    return False
        else:
            # Upward path
            for i in range(end[0], start[0]):
                if ([i, start[1]] in visited):
                    return False
    else:
        # Horizontal Path
        # Identify whether the path is ltr or rtl
        if start[1] < end[1]:
            # Left to Right path
            for i in range(start[1]+1, end[1]+1):
                if ([start[0], i] in visited):
                    return False
        else:
            # Right to left path
            for i in range(start[1]-1, end[1]-1, -1):
                if ([start[0], i] in visited):
                    return False
    return True

# Writing the final path from
# the start node to the final node
# parameters are path, which is a list of nodes and algorithm, which is dfs or bfs and is used for the file path
def printPath(path, algorithm):
    # Writing into output file
    outputFile = open("Q2/Solutions/"+ algorithm + "/" + sys.argv[1][:-4] + "_solution.txt", "w")
    for i in path:
        outputFile.write(str(tuple(i)))
        if i != path[-1]:
            outputFile.write(',')
    outputFile.close()

# Generating the suitable output for A* algorithm.
# parameters are path, which is a list of nodes and keys, which is the order of keys the agent have been founded
def printOutputAStar(path, keys):
    # Opening/Creating output file
    outputFile = open("Q2/Solutions/ASTAR/" + sys.argv[1][:-4] + "_solution.txt", "w")
    # Sorte the keys based on their visit order
    sortedKeys = sorted(keys, key=lambda k: k[2])
    for i in range(len(sortedKeys)):
        outputFile.write(str(tuple([sortedKeys[i][0], sortedKeys[i][1]])))
        if i != len(sortedKeys)-1:
            outputFile.write(',')
    outputFile.write('\n')
    # Printing the final path length
    outputFile.write(str(len(path)-1))
    outputFile.write('\n')
    # Printing the final path
    for i in path:
        outputFile.write(str(tuple(i)))
        if i != path[-1]:
            outputFile.write(',')
    outputFile.close()

# Writing the result to the output where the agent
# could'nt find a possible path
# Get algorithm as paramether to determine the path for saving the file
def printImpossible(algorithm):
    outputFile = open("Q2/Solutions/" + algorithm + "/" + sys.argv[1][:-4] + "_solution.txt", "w")
    outputFile.write('Not possible')
    outputFile.close()

# Writing the result to the output where the agent
# could'nt find a possible path with A* algorithm
# Get keys as paramether to write the accessible keys on the output file
def printImpossibleAStar(keys):
    # Opening/Creating output file
    outputFile = open("Q2/Solutions/ASTAR/" + sys.argv[1][:-4] + "_solution.txt", "w")
    # Sorte the keys based on their visit order
    sortedKeys = sorted(keys, key=lambda k: k[2])
    for i in range(len(sortedKeys)):
        # Write down the ones that are visited
        if (sortedKeys[i][2] != 0):
            outputFile.write(str(tuple([sortedKeys[i][0], sortedKeys[i][1]])))
            if i != len(sortedKeys)-1:
                outputFile.write(',')
    outputFile.write('\n')
    outputFile.write('-1\n')
    outputFile.write('Not possible')
    outputFile.close()


## The Whole Depth First Search process is performing here.
## This is a recursive function that returns True if there is a path and returns false if it is not possible.
## Parameters are the location of the starting point at each iteration, board, and a list that indicates the nodes that are already visited.
def dfs(startRow, startColumn, board, visited):
    ## Return False if we have previously visited this node.
    for i in visited:
        if i == [startRow, startColumn]:
            return False

    ## Adding the current node to the list of visited nodes.
    visited.append([startRow, startColumn])
    
    ## Check whether we reach the goal or not
    if (board[startRow][startColumn] == 'T'):
        printPath(visited, 'dfs')
        return True
    
    ## These two variables identify the next node to visit
    newRow = startRow
    newColumn = startColumn

    # Navigating to left
    ## Finding the node to be visited next if we turn left
    while board[startRow][newColumn] != '#':
        newColumn -= 1
    newColumn += 1
    # Turn left if there is no wall and the path does not contain a node that is already visited
    if (newColumn != startColumn and is_visited([startRow, startColumn],[startRow, newColumn],visited)):
        if dfs(startRow, newColumn, board, visited):
            return True
    
    # Navigating to right
    newColumn = startColumn
    ## Finding the node to be visited next if we turn right
    while board[startRow][newColumn] != '#':
        newColumn += 1
    newColumn -= 1
    # Turn right if there is no wall and the path does not contain a node that is already visited
    if (newColumn != startColumn and is_visited([startRow, startColumn],[startRow, newColumn],visited)):
        if dfs(startRow, newColumn, board, visited):
            return True

    # Navigating to Up
    newColumn = startColumn
    ## Finding the node to be visited next if we go Up
    while board[newRow][startColumn] != '#':
        newRow -= 1
    newRow += 1
    # Go up if there is no wall and the path does not contain a node that is already visited
    if (newRow != startRow and is_visited([startRow, startColumn],[newRow, startColumn],visited)):
        if dfs(newRow, startColumn, board, visited):
            return True

    # Navigating to Down
    newRow = startRow
    ## Finding the node to be visited next if we go Down
    while board[newRow][startColumn] != '#':
        newRow += 1
    newRow -= 1
    # Go down if there is no wall and the path does not contain a node that is already visited
    if (newRow != startRow and is_visited([startRow, startColumn],[newRow, startColumn],visited)):
        if dfs(newRow, startColumn, board, visited):
            return True

    return False

## The Whole Breadth First Search process is performing here.
## This is not a recursive function.
## Parameters are the location of the starting point and the board
def bfs(startRow, startColumn, board):
    ## Setting up the variables need to start BFS
    # Nodes that are visited
    visited = []
    # A Queue that identifies the next node to explore
    fringe = [ [startRow, startColumn] ]
    # A Queue that works similarly with the previous one, but keep paths instead of nodes
    path = [ [[startRow, startColumn]] ]
    # The main loop. Repeats until the fringe is empty
    while len(fringe) > 0:
        # Taking out the node we are going to explore
        currentNode = fringe.pop(0)
        currentPath = path.pop(0)
        
        # Check whether we achieve our goal
        if (board[currentNode[0]][currentNode[1]] == 'T'):
            printPath(currentPath, 'bfs')
            return True
        
        # Adding the current node to visited list
        visited.append(currentNode)

        ## These three variables identify the next node to visit and the path each make
        newRow = currentNode[0]
        newColumn = currentNode[1]
        newPath = currentPath.copy()

        # Navigating to left
        ## Finding the node to be visited next if we turn left
        while board[currentNode[0]][newColumn] != '#':
            newColumn -= 1
        newColumn += 1
        # Turn left if there is no wall and the path does not contain a node that is already visited
        if (newColumn != currentNode[1] and is_visited([currentNode[0], currentNode[1]],[currentNode[0], newColumn], visited)):
            fringe.append([currentNode[0], newColumn])
            newPath.extend([[currentNode[0], newColumn]])
            path.append(newPath)
            newPath = currentPath.copy()
        
        # Navigating to right
        newColumn = currentNode[1]
        ## Finding the node to be visited next if we turn right
        while board[currentNode[0]][newColumn] != '#':
            newColumn += 1
        newColumn -= 1
        # Turn right if there is no wall and the path does not contain a node that is already visited
        if (newColumn != currentNode[1] and is_visited([currentNode[0], currentNode[1]],[currentNode[0], newColumn], visited)):
            fringe.append([currentNode[0], newColumn])
            newPath.extend([[currentNode[0], newColumn]])
            path.append(newPath)
            newPath = currentPath.copy()

        # Navigating to Up
        newColumn = currentNode[1]
        ## Finding the node to be visited next if we go Up
        while board[newRow][currentNode[1]] != '#':
            newRow -= 1
        newRow += 1
        # Go up if there is no wall and the path does not contain a node that is already visited
        if (newRow != currentNode[0] and is_visited([currentNode[0], currentNode[1]],[newRow, currentNode[1]],visited)):
            fringe.append([newRow, currentNode[1]])
            newPath.extend([[newRow, currentNode[1]]])
            path.append(newPath)
            newPath = currentPath.copy()

        # Navigating to Down
        newRow = currentNode[0]
        ## Finding the node to be visited next if we go Down
        while board[newRow][currentNode[1]] != '#':
            newRow += 1
        newRow -= 1
        # Go down if there is no wall and the path does not contain a node that is already visited
        if (newRow != currentNode[0] and is_visited([currentNode[0], currentNode[1]],[newRow, currentNode[1]],visited)):
            fringe.append([newRow, currentNode[1]])
            newPath.extend([[newRow, currentNode[1]]])
            path.append(newPath)
            newPath = currentPath.copy()
       
    return False

## Helper function that calculates the Manhattan distance between two nodes
## Parametes are the nodes we are looking for their distance
def distance(firstNode, secondNode):
    return abs(firstNode[0] - secondNode[0]) + abs(firstNode[1] - secondNode[1])

## This function calculates the heuristic of each point.
## Suggested heuristic is based on the manhattan distance(MD) of the closest key.
## This is a recursive function. The formula for calculating the heuristic function is:
## MD(node, closest key) + MD(closest key, second closest key) + ... + MD(farest key, destination)
def findHeuristic(node, keys, dest):
    # If there is no other key, calculate distance between node and destination
    if leftKeysNumber(keys) == 0:
        return distance(node, dest)
    else:
        # Finding the closest key
        minDistance = 10000000
        minIndex = 0
        for i in range(len(keys)):
            if (keys[i][2] == 0):
                currentDistance = distance(node ,keys[i])
                if (currentDistance < minDistance):
                    minDistance = currentDistance
                    minIndex = i
        # Removing the closest key from keys list
        newKeys = copy.deepcopy(keys)
        newKeys[minIndex][2] += 1

        # Returning the calculated distance + the next distance
        return minDistance + findHeuristic(newKeys[minIndex], newKeys, dest)

## This function checks whether the node is a valid node to move into it.
## If the cordinates does not match the board or there is a # in that square then it is not valid.
## The only parameters are node cordinates and the main board
def isPossible(node, board):
    # Check if the cordinates are smaller than 0
    if (node[0] < 0 or node[1] < 0):
        return False
    # Check if the cordinates are greater than board width/height
    if (node[0] >= len(board) or node[1] >= len(board[0])):
        return False
    # Check whether there is a wall in that square
    if (board[node[0]][node[1]] == '#'):
        return False
    # Otherwise
    return True

## Returns the number of keys that are not yet visited
## By checking the 3rd parameter of each key in the list
def leftKeysNumber(keys):
    notFoundedKeys = len(keys)
    lastVisitedKeys = 0
    for i in keys:
        if (i[2] != 0):
            notFoundedKeys -= 1
            if (i[2] > lastVisitedKeys):
                lastVisitedKeys = i[2]
    return notFoundedKeys

## Returns the number of keys that are visited
## By checking the 3rd parameter of visited keys in the list
def lastVisitedKey(keys):
    lastVisitedKeys = 0
    for i in keys:
        if (i[2] != 0 and i[2] > lastVisitedKeys):
            lastVisitedKeys = i[2]
    return lastVisitedKeys

## The Whole process of A* search is implemented in this function.
## This is not a recursive function.
## Parameters are the location of the starting point and the board
def astar(startRow, startColumn, board):
    # Checking the destination location
    if (board[-1][-1] == 'D'):
        dest = [len(board)-1,len(board[0])-1]
    else:
        print('Destination is misplaced.')
        return False
    
    # Finding the locations of the Key
    # Format of each key: [ row, column, the order in which this key is visited (0 by default) ]
    keys = findKeys(board)

    # Creating a fringe to follow the path
    # [Node, heuristic, cost, keys]
    fringe = []
    fringe.append([[startRow, startColumn], findHeuristic([startRow, startColumn], keys, dest), 0, keys])
    
    # Creating a list similar to fringe which keeps the path from starting node to the mapped node on the fringe
    # Per each node in fringe there is a path in routes
    routes = []
    routes.append([[startRow, startColumn]])

    # List of nodes that are already visited
    visited = []

    # The main A* implementation takes place in the following loop
    reachDest = False
    while (reachDest is False):
        
        ## Choosing the next node to pick from fringe (Node with lowest Cost+Heuristic)
        # Set next node to the first member of list
        nextNode = 0
        # Finding a node from fringe to follow next
        for i in range(len(fringe)):
            if fringe[i][1] + fringe[i][2] < fringe[nextNode][1] + fringe[nextNode][2]:
                nextNode = i
        
        # Saving Current Node features different variables
        currentNode = fringe[nextNode][0]
        currentNodeCost = fringe[nextNode][2]
        currentKeys = copy.deepcopy(fringe[nextNode][3])

        # Picking out the selected node from fringe and put it in the list of visited nodes
        visited.append(fringe.pop(nextNode))
        # Picking out the path of selected node from the list of routes
        currentRoute = routes.pop(nextNode)

        ## Checking if we reach to the goal or not
        if (currentNode == dest and leftKeysNumber(currentKeys) == 0):
            reachDest = True
            printOutputAStar(currentRoute, currentKeys)
            return True

        # Checking if we reach to any key
        for i in range(len(currentKeys)):
            if (currentNode[0] == currentKeys[i][0]
                 and currentNode[1] == currentKeys[i][1] and leftKeysNumber(currentKeys) != 0):
                currentKeys[i][2] = lastVisitedKey(currentKeys) + 1
                break

        # Adding the next node to a list which indicates possible paths
        # In the following order: Right, Down, Left, Up
        possiblePath = []
        possiblePath.append([currentNode[0]  ,currentNode[1]+1])
        possiblePath.append([currentNode[0]+1,currentNode[1]  ])
        possiblePath.append([currentNode[0]  ,currentNode[1]-1])
        possiblePath.append([currentNode[0]-1,currentNode[1]  ])

        # Adding the next possible nodes to fringe list       
        for i in possiblePath:
            # Check whether each possible moves are valid in the board
            if isPossible(i, board) is True:
                # Calculating the Heuristic and the cost of the next possible node
                possiblePathHeuristic = findHeuristic(i, currentKeys, dest)
                possiblePathCost = currentNodeCost + 1

                # Check whether the suggested next node is already visited or
                # is already in the fringe with a lower cost+heuristic
                check = True
                for j in fringe:
                    if (j[0] == i and leftKeysNumber(currentKeys) == leftKeysNumber(j[3]) and j[1] + j[2] <= possiblePathHeuristic + possiblePathCost):
                        check = False
                for j in visited:
                    if (j[0] == i and leftKeysNumber(currentKeys) == leftKeysNumber(j[3]) and j[1] + j[2] <= possiblePathHeuristic + possiblePathCost):
                        check = False

                # If all the conditions are suitable then we add the suggested node to the fringe
                if check:
                    # Adding new node to fringe
                    fringe.append([i, possiblePathHeuristic, possiblePathCost, currentKeys])
                    # Creating the new path and add it to the routes
                    newPath = currentRoute.copy()
                    newPath.extend([i])
                    routes.append(newPath)
                    newPath = currentRoute.copy()

        # There is no possible path if fringe is empty
        if (len(fringe) == 0):
            printImpossibleAStar(currentKeys)
            return False

## Getting Inout from the input file
# Game board
board = readBoardFromFile(sys.argv[1], sys.argv[2])

# Harry's location
harryRow, harryColumn = findHarry(board)

# A boolean that identifies the possibility of finding a path
isImpossible = False
k = 0
# Performing appropriate algorithm
algorithm = sys.argv[2]
if (algorithm == 'dfs'):
    isImpossible = dfs(harryRow, harryColumn, board, [])
elif (algorithm == 'bfs'):
    isImpossible = bfs(harryRow, harryColumn, board)
elif (algorithm == 'astar'):
    isImpossible = astar(harryRow, harryColumn, board)

# Printing output if there is no path
if isImpossible is False and algorithm != 'astar':
    printImpossible(algorithm)