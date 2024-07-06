import sys
import copy
import time

## Printing the board in a nice format
## This function used for debugging
## Parameter: board(2d array)
def print_board(board):
    for i in board:
        print(i)
        print()
    print('-------------')

## Writing results into a file
## Parameters: algorithm used for finding solutions and file name and N
def write_results_to_file(algo, file_name, n):
    f = open(file_name, "w")
    # Printing Algorithm
    if algo == 'FOR':
        f.write("FORWARD CHECKING")
    elif algo == 'MAC':
        f.write("MAC")
    
    f.write("\n\n")

    # Printing Number of Solutions
    f.write("Solutions ")
    global Number_of_solutions
    f.write(str(Number_of_solutions))
    f.write("\n\n")

    # Printing Number of Backtracks
    f.write("Backtracks ")
    global Number_of_backtracks
    f.write(str(Number_of_backtracks-1))
    f.write("\n")

    # Printing the first 2*N Solution Boards
    global solutions
    if len(solutions) < 2*n:
        number_of_printed_solutions = len(solutions)
    else:
        number_of_printed_solutions = 2*n
    for i in range(number_of_printed_solutions):
        f.write("\n")
        f.write("#")
        f.write(str(i))
        f.write("\n")
        for j in solutions[i]:
            for k in range(len(j)):
                if j[k]==-1:
                    f.write('0')
                else:
                    f.write(str(j[k]))
                if k != len(j)-1:
                    f.write(", ") 
            f.write("\n")
            
    f.close()

## Checking if a queen can locate in a specific cell
## This function used for Forward Checking algorithm
## Parameters: board and proposed location for next queen
## Returns True or False 
def possible(board, x, y):
    # Check this row on left side
    for i in range(x):
        if board[i][y] == 1:
            return False
        
    # Check upper diagonal on left side
    for i, j in zip(range(x, -1, -1), range(y, -1, -1)):
        if board[i][j] == 1:
            return False
 
    # Check lower diagonal on right side
    for i, j in zip(range(x, -1, -1), range(y, len(board), 1)):
        if board[i][j] == 1:
            return False

    return True

## Update the Constraint for the new queen
## Parameters: Board(2d array), location of the new queen
## Return: New board with updated constraints
def update_constraint(board, x, y):
    # Propogate constraint of this row on right side
    for i in range(x+1, len(board)):
        board[i][y] = -1
    
    # Constraint of upper diagonal on right side
    for i, j in zip(range(x+1, len(board)), range(y-1, -1, -1)):
        board[i][j] = -1
 
    # Constraint of lower diagonal on right side
    for i, j in zip(range(x+1, len(board)), range(y+1, len(board), 1)):
        board[i][j] = -1

    return board
    
## Checking the consistancy of board if a new queen locates
## Parameters: Board(2d array), proposed location of the new queen
## Return: True or False
def consistant(current_board, x, y):
    # First update the constraints of the new queen
    board = update_constraint(copy.deepcopy(current_board), x, y)

    # Check whether there is a column that all the rows are constrained
    for i in range(x+1, len(board)):
        check = False
        for j in range(len(board[i])):
            if board[i][j] == 0:
                check = True
        if check is False:
            return check
    
    return True

## Main function for implementing Maintaining Arc Consistancy
## It is a recursive function
## Parameters: Number of columns, board(2d array), 
##             Number of queens that are already located(starts from 0)                
def mac(n, board, step):
    # Check whether all the queens are located
    if step == n:
        global Number_of_solutions
        Number_of_solutions += 1
        global solutions
        solutions.append(board)
        return

    # iterating columns
    for i in range(0, n):
        # Check if this location is constrained or available
        if board[step][i] == 0:
            # Check if choosing this location for the next queen 
            # maintains consistancy in the board. This is the difference with FOR.
            if consistant(board, step, i):
                # Creating new board with updated constraint, 
                # add a new queen, and run the MAC again
                new_board = update_constraint(copy.deepcopy(board), step, i)
                new_board[step][i] = 1
                mac(n, new_board, step+1)
                global Number_of_backtracks
                Number_of_backtracks += 1

## Main function for implementing Forward Checking
## It is a recursive function
## Parameters: Number of columns, board(2d array), 
##             Number of queens that are already located(starts from 0)                
def forward_checking(n, board, step):
    # Check whether all the queens are located
    if step == n:
        global Number_of_solutions
        Number_of_solutions += 1
        global solutions
        solutions.append(board)
        return

    # iterating columns
    for i in range(0, n):
        # This if statement prunes several inefficient backtracks 
        if possible(board, step, i):
            # Creating new board, add a new queen, and run the FOR again
            new_board = copy.deepcopy(board)
            new_board[step][i] = 1
            forward_checking(n, new_board, step+1)
            global Number_of_backtracks
            Number_of_backtracks += 1


## Following 3 Variables are Global, since they update
## in recursion functions
Number_of_solutions = 0
Number_of_backtracks = 0
solutions = []

# Obtaining N, Algorithm, and File name from command line
algo = sys.argv[1]
n = int(sys.argv[2])
file_name = sys.argv[3]

# Creating the board
initial_board = [[0 for i in range(n)] for j in range(n)]

# Keeping start time for calculating total running time
start_time = time.time()

# Choosing suitable algorithm and run it!
if algo == 'FOR':
    forward_checking(n, initial_board, 0)
elif algo == 'MAC':
    mac(n, initial_board, 0)

# End time for calculating total running time
end_time = time.time()

# Writing Final results to file
write_results_to_file(algo, file_name, n)

# Print total running time in command line
print(end_time-start_time)