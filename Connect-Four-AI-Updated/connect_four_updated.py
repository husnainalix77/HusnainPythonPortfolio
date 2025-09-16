# Connect Four Game (Human vs Strong AI) — Coded & Edited - Husnain Maroof ML Engineer - 16 Sep, 2025. 

import time
import os
import platform

def colorize(cell):
    'Return colored discs for players and a very faint gray hollow circle for empty'
    if cell == 'R':
        return "\033[91m●\033[0m"       # bright red filled circle
    elif cell == 'Y':
        return "\033[33m●\033[0m"       # dark yellow (duller gold) filled circle
    elif cell == '-':
        return "\033[2;90m○\033[0m"     # faint dull gray hollow circle
    return cell

def dispGrid(grid):
    'Display the game grid in a nice Unicode box format with circles'
    cols = len(grid[0])
    rows = len(grid)
    print()
    print('╔' + '═══╦' * (cols - 1) + '═══╗')
    for r_index, row in enumerate(grid):
        print('║' + '║'.join(f' {colorize(cell)} ' for cell in row) + '║')
        if r_index < rows - 1:
            print('╠' + '═══╬' * (cols - 1) + '═══╣')
        else:
            print('╚' + '═══╩' * (cols - 1) + '═══╝')
    print('  ' + '   '.join(colorize_column_number(c) for c in range(cols)))
    print()

def colorize_column_number(num):
    'Return the column number in cyan'
    return f"\033[94m{num}\033[0m"

def clearScreen():
    'Clear the terminal screen (cross-platform)'
    current_system = platform.system()
    if current_system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def updateDisplay(grid):
    'Pause briefly, clear screen, and redraw the grid'
    time.sleep(0.1)
    clearScreen()
    dispGrid(grid)

def getColumn(grid, col_num):
    'Return the values of a specific column as a list'
    return list(map(lambda row: row[col_num], grid))

def validMove(grid, c, mark):
    'Try placing a mark in column c. Returns True if successful'
    n = len(grid) - 1
    col = getColumn(grid, c)
    for r, data in enumerate(col[::-1]):  # search bottom-up
        if data == '-':
            grid[n-r][c] = mark
            return True
    return False  # column full

def getEmptyPieces(grid):
    'Returns total empty pieces available currently in grid'
    empty_pieces = sum(row.count('-') for row in grid)
    return empty_pieces

def canWin(grid, mark):
    'Check if player with mark has a winning 4-in-a-row'
    rows, cols = len(grid), len(grid[0])
    # Vertical
    for col in range(cols):
        column = getColumn(grid, col)
        for r in range(rows - 3):
            if all(column[i] == mark for i in range(r, r+4)): ## 3 Cominations
                return True
    # Horizontal
    for row in grid:
        for c in range(cols - 3):
            if all(row[i] == mark for i in range(c, c+4)): ## 4 Cominations
                return True
    # Diagonal \
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(grid[r+i][c+i] == mark for i in range(4)):
                return True
    # Diagonal /
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(grid[r-i][c+i] == mark for i in range(4)):
                return True
    return False

def hasEmptySlot(grid):
    'Return True if there is at least one empty slot in the grid'
    if any('-' in getColumn(grid, c) for c in range(len(grid[0]))):
        return True
    return False

def allVerticalStreak(grid, mark, n):
    'Checks if there are n marks in a row vertically with 1 empty above them'
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    for c in range(cols):
        column = getColumn(grid, c)
        for r in range(rows - n):
            # Found n in a row
            if column[r:r+n] == [mark] * n:
                # Check slot immediately above them (if inside grid)
                if r + n < rows and column[r+n] == '-':
                    count += 1
    return count

def allHorizontalStreak(grid, mark, n):
    'Checks if there are n marks in a row horizontally with 1 empty left or right'
    cols = len(grid[0])
    count = 0
    for row in grid:
        for r in range(cols - n + 1):
            # Found n in a row
            if row[r:r+n] == [mark] * n:
                # Check immediate right
                if (r + n < cols and row[r+n] == '-')\
                    or (r - 1 >= 0 and row[r-1] == '-'):
                    count += 1
    return count
               
## Diagonal Streak Check
def allDiagonalStreak(grid, mark, n):
    'Checks if there are n marks in a row diagonally with 1 empty before or after them'
    rows, cols = len(grid), len(grid[0])
    count = 0
    # Diagonal \
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(grid[r+i][c+i] == mark for i in range(n)):
                # Check forward (bottom-right)
                if (r+n < rows and c+n < cols and grid[r+n][c+n] == '-')\
                    or (r-1 >= 0 and c-1 >= 0 and grid[r-1][c-1] == '-'):

                    count += 1 
    # Diagonal /
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(grid[r-i][c+i] == mark for i in range(n)):
                # Check forward+ backward (top-right)
                if (r-n >= 0 and c+n < cols and grid[r-n][c+n] == '-')\
                    or (r+1 < rows and c-1 >= 0 and grid[r+1][c-1] == '-'):
                    count += 1
    return count
                    
def countStreaks(grid, mark, n):
    'Counts number of n-in-a-row streaks for given mark'
    rows_streaks = allHorizontalStreak(grid, mark, n)
    cols_streaks = allVerticalStreak(grid, mark, n)
    diags_streaks = allDiagonalStreak(grid, mark, n)
    return rows_streaks + cols_streaks + diags_streaks

def countOpenEndedStreaks(grid, mark, n):
    'Counts - around both ends of n-in-a-row streaks for given mark'
    ## We will not check for vertical (only one possible open side)
    rows, cols = len(grid), len(grid[0])
    count = 0
    # Horizontal
    for row in grid:
        for c in range(1, cols - n):
            if row[c:c+n] == [mark] * n:
                if row[c-1] == '-' and row[c+n] == '-': # Check Left & Right Open
                    count += 1
    # Diagonal \
    for r in range(1, rows - n):
        for c in range(1, cols - n):
            if all(grid[r+i][c+i] == mark for i in range(n)):
                if grid[r-1][c-1] == '-' and grid[r+n][c+n] == '-': # Check Before & After Open
                    count += 1
    # Diagonal /
    for r in range(n, rows - 1):
        for c in range(1, cols - n):
            if all(grid[r-i][c+i] == mark for i in range(n)):
                if grid[r+1][c-1] == '-' and grid[r-n][c+n] == '-': # Check Before & After Open
                    count += 1
    return count
                   
def allValidColumns(grid):
    'Gets all valid columns(Prefering center one first) where move can be made'
    total_cols = len(grid[0])
    center = total_cols // 2
    search_order = [center]
    for offset in range(1, total_cols // 2 + 1):
        if center - offset >= 0:
            search_order.append(center - offset)
        if center + offset < total_cols:
            search_order.append(center + offset)   
    cols = [col_num for col_num in search_order if '-' in getColumn(grid, col_num)]
    return cols   
                
def isTerminal(grid):
    'Checks terminal condition particularly for some evaluation'
    if canWin(grid, 'R') or canWin(grid, 'Y') or not hasEmptySlot(grid):
        return True
    return False
            
def evaluateBoard(grid):
    'Evaluates the board and returns a score'
    human_mark = 'R'
    ai_mark = 'Y' 
    score = 0
    # Check for win, block, 3-in-a-row, 2-in-a-row
    if canWin(grid, ai_mark):
        return 1000000
    if canWin(grid, human_mark):
        return -1000000
    # Check 3-in-a-row in column, row, diagonal
    for n, weight in [(3, 1000), (2, 100)]:
        # open-ended streaks stronger
        ai_open = countOpenEndedStreaks(grid, ai_mark, n)
        human_open = countOpenEndedStreaks(grid, human_mark, n)
        ai_streaks = countStreaks(grid, ai_mark, n)
        human_streaks = countStreaks(grid, human_mark, n)
        score += ai_streaks * weight
        score += ai_open * (weight // 2)   # bonus for open-ended
        score -= human_streaks * weight * 15
        score -= human_open * (weight // 2) * 15
    ## Count pieces for both players having preference for center columns    
    search_order = allValidColumns(grid)    
    ai_pieces = sum(getColumn(grid, col_num).count(ai_mark) for col_num in search_order)
    human_pieces = sum(getColumn(grid, col_num).count(human_mark) for col_num in search_order)
    score += ai_pieces*10
    score -= human_pieces*10
    return score

def getAdaptiveDepth(grid):
    'Returns adaptive depth based on empty pieces'
    empty_pieces = getEmptyPieces(grid)
    if empty_pieces >= 35:
        return 5
    elif empty_pieces >= 25:
        return 6
    elif empty_pieces >= 15:
        return 7
    else:
        return 8  

def simulateMove(c, mark, grid):
    'Simulates the specific move and updates grid'
    new_grid = [row.copy() for row in grid]
    validMove(new_grid, c, mark)
    return new_grid  

def causesDoubleThreat(grid, mark):
    'Checks if this move causes double threat'
    valid_cols = allValidColumns(grid)
    threats = 0
    if not valid_cols:
        return None
    for col in valid_cols:
        new_grid = simulateMove(col, mark, grid)
        if canWin(new_grid, mark):
            threats += 1
    if threats>=2:
        return True        
    return False    
    
def minimax(grid, depth, maximizingPlayer, AI_mark, alpha, beta):
    'Implements Minimax Algorithm for given Depth using alpha beta'
    opponent_mark = 'R' if AI_mark == 'Y' else 'Y'
    valid_cols = allValidColumns(grid)
    if depth == 0 or isTerminal(grid) or not valid_cols:
        return evaluateBoard(grid)
    if maximizingPlayer:
        maxEval = float('-inf')
        for col in valid_cols:
            new_grid = simulateMove(col, AI_mark, grid)
            eval = minimax(new_grid, depth-1, False, AI_mark, alpha, beta)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if alpha>=beta:
                break ## Beta Pruning
        return maxEval
    else:
        minEval = float('inf')
        for col in valid_cols:
            new_grid = simulateMove(col, opponent_mark, grid)
            eval = minimax(new_grid, depth-1, True, AI_mark, alpha, beta)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha Pruning
        return minEval

def getBestMove(grid, AI_mark):
    'Gives AI Best Move'
    opponent_mark = 'R' if AI_mark == 'Y' else 'Y'
    depth = getAdaptiveDepth(grid)
    if depth > 6:
        print("Computer is thinking deeper... Please wait.")
    best_score = float('-inf')
    best_col = None
    alpha = float('-inf') ## Lower bound
    beta = float('inf') ## Higher bound
    valid_cols = allValidColumns(grid)
    if not valid_cols: # safety check
        return None 
    #Check for immediate winning moves for the AI
    for col in valid_cols:
        temp_grid = simulateMove(col, AI_mark, grid)
        if canWin(temp_grid, AI_mark):
            print("Computer found a winning move!")
            return col
    #Check for immediate blocking moves for the opponent
    for col in valid_cols:
        temp_grid = simulateMove(col, opponent_mark, grid)
        if canWin(temp_grid, opponent_mark):
            print("Computer is blocking a threat!")
            return col
    ## Check for Double Threat    
    for col in valid_cols:
        new_grid = simulateMove(col, AI_mark, grid)
        # Check if this AI move creates a double threat for human
        if causesDoubleThreat(new_grid, AI_mark):
            score = float('inf')  # prefer moves creating double threats
        # Check if this AI move allows opponent double threat in next turn
        elif causesDoubleThreat(new_grid, opponent_mark):
            score = float('-inf')  # avoid moves that allow opponent double threats
        else:    
            score = minimax(new_grid, depth-1, False, AI_mark, alpha, beta)
        if score > best_score:
            best_score = score
            best_col = col
        alpha = max(alpha, best_score)    
    return best_col
# ---- Game Loop ----
def playGame(rows, cols):
    'Run the main Connect Four game loop'
    ## Set up Grid and define players
    grid = [['-' for _ in range(cols)] for _ in range(rows)]
    players = [('Player', 'R'), ('Computer', 'Y')]
    print('Computer (Y) is using much strong AI.')
    dispGrid(grid)
    print(f"{players[0][0]} = {colorize(players[0][1])} | {players[1][0]} = {colorize(players[1][1])}")
    print('-'*25)
    # Decide turn order
    while True:
        choice = input('Enter F to take 1st chance or S for 2nd chance: ').strip().lower()
        if choice in ['f', 's']:
            break
        print('Enter F or S only!')
    turn = 0 if choice == 'f' else 1
    # Main loop
    while True:
        current_player, mark = players[turn % 2]
        if turn % 2 == 0:  # Human turn
            while True:
                try:
                    user_pick = int(input(f'{current_player} ({mark}), choose a column (0-{cols-1}): '))
                    if user_pick not in range(cols):
                        print(f'Enter a number between 0 and {cols-1}!')
                        continue
                    break
                except ValueError:
                    print(f'Invalid input. Enter a number between 0 and {cols-1}.')
            if validMove(grid, user_pick, mark):
                updateDisplay(grid)
            else:
                print(f'Invalid move. Column {user_pick} is full.')
                continue
        else:  # AI turn
            computer_pick = getBestMove(grid, 'Y')
            if computer_pick is None:
                print('No valid moves left for Computer. Game over!')
                return
            validMove(grid, computer_pick, mark)
            print('Computer is choosing.....')
            print(f"{current_player}({mark}) chooses column {computer_pick}.")
            updateDisplay(grid)
        ## Check for Win and Game Over    
        if canWin(grid, mark):
            print(f'{current_player}({mark}) won!')
            return
        if not hasEmptySlot(grid):
            print('All columns are full. Game is ended as draw!')
            return
        turn = (turn + 1) % 2  # alternate turns

if __name__ == '__main__':
    rows, cols = 6, 7  # standard Connect Four size
    while True:
        op = input('Do you want to play (Y/N): ').strip().lower()
        if op not in ['y', 'n', 'yes', 'no']:
            print('Enter Y or N only!')
            continue
        if op in ['y', 'yes']:
            clearScreen()
            playGame(rows, cols)
            print("=" * 40)
            print('Wanna Try Again?')
        else:
            print('Ok, maybe next time.')
            break