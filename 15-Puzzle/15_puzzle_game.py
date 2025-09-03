## This code is written by Husnain Maroof, Machine Learning Engineer, on 3 Sep, 2025.
## I intentionally avoided global variables (due to keeping their track) here.
import random
import os
import time
import datetime
import platform

def setUpGrid(n):
    'Sets up a solvable grid for any nxn sliding puzzle'
    tiles = list(range(1, n*n)) + ['-']   
    while True:
        random.shuffle(tiles)
        nums = [i for i in tiles if i != '-']
        
        # Count inversions
        inversions = 0
        for j in range(len(nums)):
            for k in range(j + 1, len(nums)):
                if nums[j] > nums[k]:
                    inversions += 1
        
        # Find blank row from bottom (1-based)
        blank_tile = tiles.index('-')
        row_from_top = blank_tile // n
        blank_row_from_bottom = n - row_from_top  # 1 based index
        
        if n % 2 == 1:
            # Odd n: solvable iff inversions are even
            if inversions % 2 == 0:
                break
        else:
            # Even n: sum of blank rom from bottom and inversions should be odd (if we follow rule for n-->even)
            if (blank_row_from_bottom + inversions) % 2 == 1:
                break
    # Convert to 2D
    grid = [tiles[i:i+n] for i in range(0, n*n, n)]
    return grid

def dispGrid(grid):
    'Displays the grid as a real 15-puzzle with nicely formatted tiles'
    n = len(grid)
    tile_width = 4  # width for each tile including spaces
    horizontal = '+' + ('-' * tile_width + '+') * n

    for row in grid:
        print(horizontal)
        for value in row:
            if value == '-':
                print(f'|{"":^{tile_width}}', end='')  # blank tile
            else:
                print(f'| {str(value):>{tile_width-1}}', end='')  # right-aligned number
        print('|')
    print(horizontal)

def showCommands():
    'Shows commands to user'  
    print('Commands are as follows :') 
    print("'W' or 'w' : Move Up")
    print("'S' or 's' : Move Down")
    print("'A' or 'a' : Move Left")
    print("'D' or 'd' : Move Right")
    
def clearScreen():
    'Clears the console screen based on the operating system'
    current_os = platform.system()  # Returns 'Windows', 'Linux', 'Darwin' (macOS)
    if current_os == "Windows":
        os.system('cls')
    else:  # Linux or macOS
        os.system('clear') 
           
def updateDisplay(grid):
    'Clears the screen, shows commands and current grid'
    time.sleep(0.2)
    clearScreen()
    showCommands()
    dispGrid(grid)
    
def findBlank(grid):
    'Finds - in grid and then returns row and column number in which it is'
    for row, row_data in enumerate(grid): ## enumerate gives index, data (in iterable)
        if '-' in row_data: 
            col = row_data.index('-')           
            return row, col 
            
def moveLeft(grid):
    'Moves - to left if it is not in 1st column'
    row, col = findBlank(grid)
    if col == 0: ## If '-' is in 1st column
        return False
    else:
        grid[row][col-1], grid[row][col] = grid[row][col], grid[row][col-1]  ## Exchanges - with adjacent element
        return True       

def moveRight(grid):
    'Moves - to right if it is not in last column'
    row, col = findBlank(grid)
    if col == len(grid)-1 : ## If '-' is in last column
        return False
    else:
        grid[row][col+1], grid[row][col] = grid[row][col], grid[row][col+1]  
        return True
    
def moveUp(grid):
    'Moves - up if it is not in 1st row'
    row, col = findBlank(grid)
    if row == 0 : ## If '-' is in 1st row
        return False
    else:
        grid[row][col], grid[row-1][col] = grid[row-1][col], grid[row][col]  
        return True
    
def moveDown(grid):
    'Moves - down if it is not in last row'
    row, col = findBlank(grid)
    if row == len(grid)-1 : ## If '-' is in last row
        return False
    else:
        grid[row][col], grid[row+1][col] = grid[row+1][col], grid[row][col]  
        return True
    
def checkWin(grid):
    # Flatten the 2D grid into a 1D list
    flat = [cell for row in grid for cell in row]

    # Check two conditions:
    # 1. All numbers before the last cell should be in ascending order from 1 to n^2 - 1
    # 2. The last cell should be the empty space ('-')
    if flat[:-1] == list(range(1, len(flat))) and flat[-1] == '-':
        return True
    
    # If either condition fails, puzzle is not solved
    return False        
          
## Main Program
if __name__=='__main__':   
    n = 4 ## Size of grid; 4x4
    grid = setUpGrid(n)
    updateDisplay(grid) 
    total_moves = 0   
       
    while True:
        print('Enter Your Move...')
        user_move = input('> ').strip().lower()
        if user_move not in ['w', 's', 'a', 'd']:
            print('Enter a Valid Command!')
            print('No Diagonal Movement is allowed!')
            continue
        
        if user_move == 'a':
            if not moveLeft(grid):
                print('Invalid Move')
                continue
        
        elif user_move == 'd':
            if not moveRight(grid):
                print('Invalid Move')
                continue
            
        elif user_move == 'w': 
            if not moveUp(grid):
                print('Invalid Move')
                continue
            
        elif user_move == 's':
            if not moveDown(grid):
                print('Invalid Move')
                continue
        total_moves += 1    
        if checkWin(grid): ## Checking Winning Possibility
            dispGrid(grid)
            print('You won!. Numbers are successfully arranged.')
            print(f'Total moves taken are: {total_moves}')
            now = datetime.datetime.now()
            print("Game finished on:", now.strftime("%Y-%m-%d %H:%M:%S"))
            break            
        updateDisplay(grid)    


        

