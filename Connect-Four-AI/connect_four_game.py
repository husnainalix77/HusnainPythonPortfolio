## Connect Four Game (Human vs Strong AI) — Coded & Documented By Husnain Maroof, 08 Sep, 2025.

import random
import time
import os
import platform

def colorize(cell):
    'Return the cell with color if its R, Y, or -'
    if cell == 'R':
        return f"\033[91m{cell}\033[0m"   # bright red
    elif cell == 'Y':
        return f"\033[93m{cell}\033[0m"   # bright yellow
    elif cell == '-':
        return f"\033[96m{cell}\033[0m"   # bright cyan for empty
    return cell

def colorize_column_number(num):
    'Return the column number in cyan'
    return f"\033[94m{num}\033[0m"

def disp_grid(grid):
    'Display the game grid in a nice Unicode box format'
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

def clear_screen():
    'Clear the terminal screen (cross-platform)'
    current_system = platform.system()
    if current_system == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def update_display(grid):
    'Pause briefly, clear screen, and redraw the grid'
    time.sleep(0.3)
    clear_screen()
    disp_grid(grid)

def get_column(grid, col_num):
    'Return the values of a specific column as a list'
    return [row[col_num] for row in grid]

def is_valid_move(grid, c, mark):
    'Try placing a mark in column c. Return True if successful'
    n = len(grid) - 1
    col = get_column(grid, c)
    for r, data in enumerate(col[::-1]):  # search bottom-up
        if data == '-':
            grid[n-r][c] = mark
            return True
    return False  # column full

def check_win(grid, mark):
    'Check if player with mark has a winning 4-in-a-row'
    rows, cols = len(grid), len(grid[0])
    # Vertical
    for col in range(cols):
        column = get_column(grid, col)
        for r in range(rows - 3):
            if all(column[r+i] == mark for i in range(4)):
                return True
    # Horizontal
    for row in grid:
        for c in range(cols - 3):
            if all(row[c+i] == mark for i in range(4)):
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

def has_empty_slot(grid):
    'Return True if there is at least one empty slot in the grid'
    for c in range(len(grid[0])):
        if '-' in get_column(grid, c):
            return True
    return False

# ---- Simulation helpers ----
def simulate_move_on(grid, col, mark):
    'Simulate placing mark in column `col` on a copy of grid.Returns new grid, or None if the column is full'

    new_grid = [row[:] for row in grid]
    n = len(new_grid) - 1
    col_data = get_column(new_grid, col)
    for r, data in enumerate(col_data[::-1]):  # bottom-up
        if data == '-':
            new_grid[n-r][col] = mark
            return new_grid
    return None  # column full

# ---- Strong AI ----
def get_best_move(grid, ai_mark, human_mark):
    """
    Decide the best move for the AI:
    1. Win immediately if possible
    2. Block human's immediate win
    3. Prefer center, then outward
    4. Avoid moves that give the human an immediate win
    5. Fallback to random valid column
    """
    cols = len(grid[0])

    # 1. Try immediate win
    for col in range(cols):
        new_grid = simulate_move_on(grid, col, ai_mark)
        if new_grid and check_win(new_grid, ai_mark):
            return col

    # 2. Block human immediate win
    for col in range(cols):
        new_grid = simulate_move_on(grid, col, human_mark)
        if new_grid and check_win(new_grid, human_mark):
            return col

    # 3. Search order: center first, then left/right alternates
    center = cols // 2
    search_order = [center]
    for offset in range(1, cols // 2 + 1):
        if center - offset >= 0:
            search_order.append(center - offset)
        if center + offset < cols:
            search_order.append(center + offset)

    # 4. Choose a safe move (does not allow human to win next turn)
    for col in search_order:
        new_grid = simulate_move_on(grid, col, ai_mark)
        if not new_grid:
            continue
        human_can_win = False
        for opp_col in range(cols):
            opp_grid = simulate_move_on(new_grid, opp_col, human_mark)  # check after AI move
            if opp_grid and check_win(opp_grid, human_mark):
                human_can_win = True
                break
        if not human_can_win:
            return col

    # 5. Fallback random valid column
    valid_cols = [c for c in range(cols) if '-' in get_column(grid, c)]
    return random.choice(valid_cols)

# ---- Game Loop ----
def playGame(rows, cols):
    'Run the main Connect Four game loop'
    grid = [['-' for _ in range(cols)] for _ in range(rows)]
    players = [('Player', 'R'), ('Computer', 'Y')]
    print('Computer(Y) is using strong AI.')
    disp_grid(grid)

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
                    user_pick = int(input(f'{current_player}({mark}), choose a column (0-{cols-1}): '))
                    if user_pick not in range(cols):
                        print(f'Enter a number between 0 and {cols-1}!')
                        continue
                    break
                except ValueError:
                    print(f'Invalid input. Enter a number between 0 and {cols-1}.')
            if is_valid_move(grid, user_pick, mark):
                update_display(grid)
                if check_win(grid, mark):
                    print(f'{current_player}({mark}) won!')
                    return
                if not has_empty_slot(grid):
                    print('All columns are full. Game over!')
                    return
            else:
                print(f'Invalid move. Column {user_pick} is full.')
                continue

        else:  # AI turn
            computer_pick = get_best_move(grid, 'Y', 'R')
            is_valid_move(grid, computer_pick, mark)
            print(f"{current_player}({mark}) chooses column {computer_pick}.")
            time.sleep(1)
            update_display(grid)
            if check_win(grid, mark):
                print(f'{current_player}({mark}) won!')
                return
            if not has_empty_slot(grid):
                print('All columns are full. Game over!')
                return

        turn = (turn + 1) % 2  # alternate turns

if __name__ == '__main__':
    rows, cols = 6, 7  # Standard Connect Four size
    while True:
        op = input('Do you want to play (Y/N): ').strip().lower()
        if op not in ['y', 'n']:
            print('Enter Y or N only!')
            continue
        if op == 'y':
            playGame(rows, cols)
            print("=" * 40)
        else:
            print('Ok, maybe next time.')
            break
