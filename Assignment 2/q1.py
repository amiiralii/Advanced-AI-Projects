import sys
# This library is only used for reading the arguments of the command

# Reading the file name which is given in the command line argument
fileName = sys.argv[1]

# Start using the input file
inputFile = open("Q1 Test Cases/" + fileName, "r")

# Save the heuristic of each node
heuristics = {}
# Save the routes and their distances
# each key of this dictionary is a 2 param list that indicates src and dst
map = {}

# Reading the input file line by line
# ignoring the first line of input file
line = inputFile.readline()
while (line):
    line = inputFile.readline()
    if (line == '\n'):
        break

    # Reading new line, removing whitespace, and split it to 2 items
    inputString = line.strip().split(",")
    # Setting up the dictionary that shows H function per each node
    heuristics[inputString[0]] = int( inputString[1] )


# ignoring the decleration line of input file
line = inputFile.readline()
while (line):
    line = inputFile.readline()
    if (line == ''):
        break
    # Reading new line, removing whitespace, and split it to 2 items
    inputString = line.strip().split(",")
    # Setting up the dictionary that saves the routes and distances
    map [ inputString[0], inputString[1].strip() ] = int(inputString[2])

# Creating a fringe to follow the path
# [Node, heuristic, cost]
route = []
route.append(['S', heuristics['S'], 0])

reachDest = False
while (reachDest is False):
    # Set next node to the first member of list
    nextNode = 0
    # Finding a node from route to follow next
    for i in range(len(route)):
        if (route[i][1] + route[i][2] < route[nextNode][1] + route[nextNode][2]):
            nextNode = i
    
    # Checking if we reach to the goal or not
    if (route[nextNode][0][-1].isnumeric()):
        reachDest = True
        break

    # Finding the possible path from selected node
    possiblePath = []
    for key,value in map.items():
        if (key[0] == route[nextNode][0][-1]):
            possiblePath.append([key,value])
    
    # Adding the next possible steps to route list
    currentState = route[nextNode][0]
    currentCost = route[nextNode][2]
    route.pop(nextNode)
    for i in range(len(possiblePath)):
        route.append( [currentState + possiblePath[i][0][1],
                        heuristics[possiblePath[i][0][1]], 
                        currentCost + possiblePath[i][1]] )

# Writing into output file
outputFile = open("Q1/Solutions/" + fileName[:-4] + "_solution.txt", "w")
outputFile.write(str([route[nextNode][0], route[nextNode][2]]))
outputFile.close()