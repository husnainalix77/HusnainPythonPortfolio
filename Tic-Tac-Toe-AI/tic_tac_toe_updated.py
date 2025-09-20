## This code is documented and edited on 20 Sep, 2025 - Husnain Maroof ML Engineer . 
import os
import time
import platform
import random

class TicTacToe:
    """NxN Tic Tac Toe game class with Human vs Computer."""
    ORANGE = '\033[38;5;166m'
    BLUE = '\033[34m'
    RESET = '\033[0m'
    players = [('Human','X' ), ('Computer', 'O')]
    def __init__(self, N):
        """Initialize the game board and set random first turn."""
        self.N = N
        self.grid = self.setUpGrid()
        self.turn = random.randint(0, 1)
        
    def setUpGrid(self):
        """Return an NxN grid with numbered slots."""
        N = self.N 
        grid = [[j for j in range(i, i + N)] for i in range(1, N*N, N)]   
        return grid 
    
    def dispGrid(self):
        """Display the board in a formatted table with colored marks."""
        N = self.N
        max_num = N * N
        cell_width = len(str(max_num)) + 2

        top_border = "╔" + "╦".join("═" * cell_width for _ in range(N)) + "╗"
        mid_border = "╠" + "╬".join("═" * cell_width for _ in range(N)) + "╣"
        bottom_border = "╚" + "╩".join("═" * cell_width for _ in range(N)) + "╝"

        print(top_border)
        for i, row in enumerate(self.grid):
            colored_row = []
            for cell in row:
                if cell == 'X':
                    colored_row.append(f"{self.ORANGE}{str(cell).center(cell_width)}{self.RESET}")
                elif cell == 'O':
                    colored_row.append(f"{self.BLUE}{str(cell).center(cell_width)}{self.RESET}")
                else:
                    colored_row.append(f"{str(cell).center(cell_width)}")
            
            row_str = "║" + "║".join(colored_row) + "║"
            print(row_str)
            
            if i < N - 1:
                print(mid_border)
        print(bottom_border)

    def updateDisplay(self):
        """Clear the console and redraw the board."""
        current_os = platform.system()
        if current_os == 'Windows':
            os.system('cls')
        else:
            os.system('clear') 
        time.sleep(0.1)    
        self.dispGrid()       
            
    def getColumn(self, col_num, grid = None):
        """Return a list of values in a specified column."""
        if grid is None:
            grid = self.grid
        return list(map(lambda row: row[col_num], grid))
    
    def isSlotEmpty(self, slot, grid = None):
        """Check if a slot is empty; return (row, col) if yes, else False."""
        if grid is None:
            grid = self.grid
        N = self.N    
        col = (slot - 1) % N 
        row = (slot - 1) // N
        if grid[row][col] != 'X' and grid[row][col] != 'O': 
            return row, col
        return False   
     
    def fillSlot(self, mark, slot, grid = None):
        """Fill a slot with a mark; return True if successful."""
        if grid is None:
            grid = self.grid
        pos = self.isSlotEmpty(slot, grid)
        if not pos:
            return False
        row, col = pos
        grid[row][col] = mark
        return True    

    def isWinner(self, mark, grid = None):
        """Check if a given mark has won the game."""
        if grid is None:
                grid = self.grid  
        N = self.N              
        ## Horizontal Win Check
        for row in grid:
            if len(set(row)) == 1 and mark in set(row):
                return True
        ## Vertical Win Check
        for col_num in range(N):
            col = self.getColumn(col_num, grid)
            if len(set(col)) == 1 and mark in set(col):
                return True
        ## Diagonals Win Check
        main_diag = [grid[m][m] for m in range(N)] 
        sec_diag = [grid[s][N - s - 1] for s in range(N)]
        if (len(set(main_diag)) == 1 and mark in set(main_diag))\
            or (len(set(sec_diag)) == 1 and mark in set(sec_diag)):
            return True
        ## Not Won Yet
        return False
    
    def hasEmptySlot(self, grid = None):
        """Return True if any empty slots remain."""
        if grid is None:
            grid = self.grid
        N = self.N    
        for row in grid:
            for r in row:
                if r in list(range(1, N*N + 1)):
                    return True
        return False        
                    
    def playGame(self):
        """Run the main game loop until win or draw."""
        self.dispGrid()
        N = self.N 
        while True:
            current_player, mark = self.players[self.turn % 2]
            if mark == 'X':
                while True:
                    print(f'====== {current_player} Turn =======')
                    try:
                        slot = int(input(f'Enter slot to fill (1-{N * N}): '))
                    except ValueError:
                        print('Enter Numeric Values Only!')
                        continue
                    if slot not in range(1, N * N + 1):
                        print(f'Please enter 1-{N*N} only!')
                        continue 
                    break
                if not self.fillSlot(mark, slot):
                    self.updateDisplay()
                    print(f'Slot {slot} is already filled. Choose Another one.')
                    continue
                
            else: ## AI Turn
                print(f'====== {current_player} Turn ======\nComputer is thinking.....')
                computer_pick = self.getBestSlot(self.grid, 'O')
                self.fillSlot(mark, computer_pick)
                print(f"{current_player} ({mark}) chooses slot {computer_pick}.")
            if self.isWinner(mark):
                self.dispGrid()
                print(f'{current_player} ({mark}) won the game!')
                break
            if not self.hasEmptySlot():
                self.dispGrid()
                print('All slots are filled. Game is draw!')
                break
            self.updateDisplay()
            self.turn = (self.turn + 1) % 2
            time.sleep(0.2)
            
class TicTacToeAI(TicTacToe):
    """AI-enhanced Tic Tac Toe with Minimax and adaptive strategy."""
    def __init__(self, N):
        """Initialize the AI game by calling the parent constructor."""
        super().__init__(N) 
           
    def allStreaks(self, mark, grid = None):
        """Count lines with N-1 marks and no opponent marks."""
        if grid is None:
            grid = self.grid
        opponent_mark = 'X' if mark == 'O' else 'O'    
        count = 0    
        N = self.N    
        ## Horizontal    
        for row in grid:
            if row.count(mark) == N - 1 and row.count(opponent_mark) == 0:
                count += 1
        ## Vertical 
        for c in range(N):
            col = self.getColumn(c, grid)
            if col.count(mark) == N-1 and col.count(opponent_mark) == 0:
                count += 1
        ## Diagonals
        main_diag = [grid[m][m] for m in range(N)] 
        sec_diag = [grid[s][N - s - 1] for s in range(N)]
        if main_diag.count(mark) == N - 1 and main_diag.count(opponent_mark) == 0:
            count += 1
        if sec_diag.count(mark) == N - 1 and sec_diag.count(opponent_mark) == 0:
            count += 1    
        return count    
    
    def allValidSlots(self, grid = None):
        """Return a list of all empty slots."""
        if grid is None:
            grid = self.grid
        N = self.N
        allSlots = []
        for s in range(1, N*N + 1):
            if self.isSlotEmpty(s, grid):
                allSlots.append(s)
        return allSlots
    
    def isTerminal(self, grid):
        """Return a list of all empty slots."""
        if self.isWinner('X', grid) or self.isWinner('O', grid) or not self.hasEmptySlot(grid):
            return True
        return False
    
    def getAdaptiveDepth(self, grid):
        """Return search depth based on board size and remaining empty slots."""
        empty_slots = sum(1 for s in range(1, self.N*self.N + 1) if self.isSlotEmpty(s, grid))
        if self.N == 3:
            return 7
        elif self.N == 4:
            return min(6, empty_slots)  # moderate depth for 4x4
        else:  # N >= 5
            return min(5, empty_slots)  # limited depth for larger boards
    
    def evaluateBoard(self, grid = None):
        """Return a heuristic score of the board from AI's perspective."""
        if grid is None:
            grid = self.grid
        ai_mark = 'O'
        human_mark = 'X'
        score = 0    
        N = self.N
        ## Win Chcek
        if self.isWinner(ai_mark, grid):
            return 1000000
        if self.isWinner(human_mark, grid):
            return -1000000
        ## Center Control
        if N % 2 == 1:  # Odd N → single center
            mid = N // 2
            if grid[mid][mid] == ai_mark:
                score += 10000
            elif grid[mid][mid] == human_mark:
                score -= 10000
        else:  # Even N → 4 center cells
            mid = N // 2
            centers = [(mid-1, mid-1), (mid-1, mid), (mid, mid-1), (mid, mid)]
            for r, c in centers:
                if grid[r][c] == ai_mark:
                    score += 5000   # smaller weight per cell
                elif grid[r][c] == human_mark:
                    score -= 5000
                    
        ## N - 1 marks and one empty slot     
        score += self.allStreaks(ai_mark, grid) * 1000
        score -= self.allStreaks(human_mark, grid) * 1000
        ## Corners Control
        corner_directions = [(0, 0), (0, N-1), (N-1, 0), (N-1, N-1)]
        for row, col in corner_directions:
            if grid[row][col] == ai_mark:
                score += 500
            elif grid[row][col] == human_mark:
                score -= 500
        ## Edge Control
        edge_directions = []
        for i in range(1, N-1):
            ## Top Row
            edge_directions.append((0, i))
            ## Bottom Row
            edge_directions.append((N-1, i))
            ## Left Column
            edge_directions.append((i, 0)) 
            ## Right column
            edge_directions.append((i, N-1))
        ## Scan Edges    
        for row, col in edge_directions:
            if grid[row][col] == ai_mark:
                score += 100
            elif grid[row][col] == human_mark:
                score -= 100  
        return score         
            
    def simulateMove(self, mark, slot, grid = None):
        """Return a new grid with the given move applied."""
        if grid is None:
            grid = self.grid
        new_grid = [row.copy() for row in grid]  
        self.fillSlot(mark, slot, new_grid)  
        return new_grid 
           
    def minimax(self,grid, depth, maximizingPlayer, AI_mark, alpha, beta):
        """Return minimax value for the grid with alpha-beta pruning."""
        opponent_mark = 'X' if AI_mark == 'O' else 'O'
        valid_slots = self.allValidSlots(grid)
        if depth == 0 or self.isTerminal(grid):
            return self.evaluateBoard(grid)
        if maximizingPlayer:
            maxEval = float('-inf')
            for slot in valid_slots:
                new_grid = self.simulateMove(AI_mark, slot, grid)
                eval = self.minimax(new_grid, depth-1, False, AI_mark, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if alpha>=beta:
                    break ## Beta Pruning
            return maxEval
        else:
            minEval = float('inf')
            for slot in valid_slots:
                new_grid = self.simulateMove(opponent_mark, slot, grid)
                eval = self.minimax(new_grid, depth-1, True, AI_mark, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha Pruning
            return minEval

    def getBestSlot(self, grid, AI_mark):
        """Return the best move slot for the AI using minimax and heuristics."""
        opponent_mark = 'X' if AI_mark == 'O' else 'O'
        depth = self.getAdaptiveDepth(grid)
        best_score = float('-inf')
        best_slot = None
        alpha = float('-inf') ## Lower bound
        beta = float('inf') ## Higher bound
        valid_slots = self.allValidSlots(grid)
        if not valid_slots: # safety check
            return None 
        #Check for immediate winning moves for the AI
        for slot in valid_slots:
            temp_grid = self.simulateMove(AI_mark, slot, grid)
            if self.isWinner(AI_mark, temp_grid):
                print("Computer found a winning move!")
                return slot
        #Block for immediate winning moves for the human
        for slot in valid_slots:
            temp_grid = self.simulateMove(opponent_mark, slot, grid)
            if self.isWinner(opponent_mark, temp_grid):
                print("Computer is blocking a threat!")    
                return slot        
        ## Check for best slot   
        for slot in valid_slots:
            new_grid = self.simulateMove(AI_mark, slot, grid)
            score = self.minimax(new_grid, depth-1, False, AI_mark, alpha, beta)
            if score > best_score:
                best_score = score
                best_slot = slot
            alpha = max(alpha, best_score)    
        return best_slot
  
## Main Program        
if __name__ == '__main__':
    """Run a single NxN Tic Tac Toe game with AI against human."""
    N = 3  # You can change N to any value >= 3 for NxN Tic Tac Toe
    game = TicTacToeAI(N)
    game.playGame()  # Start the game loop



