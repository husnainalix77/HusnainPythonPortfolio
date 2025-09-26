# ================================================================
# Quarto Game with AI (Minimax + Alpha-Beta Pruning)
# Author : Husnain Maroof (ML Engineer)
# Date   : September 20-26, 2025
# Notes  : This project implements the full Quarto game logic with
#          AI opponent using minimax and alpha-beta pruning.
# ================================================================
import random
import os
from collections import Counter
class Quarto:
    """
    Core Quarto game class.
    Handles board setup, rules, piece selection, placement, and winner detection.
    """
    attributes = {
        "T": "Tall",
        "S": "Short",
        "L": "Light",
        "D": "Dark",
        "Q": "Square",
        "R": "Round",
        "O": "Hollow",
        "H": "Solid"
    }
    
    def __init__(self):
        self.N = 4
        self.grid = self.setUpGrid()
        self.turn = 0
        self.ai_placer = None
        self.human_placer = None
        self.ai_chooser = None
        self.human_chooser = None
        self.pieces = [
            "TLQO", "TLQH", "TLRO", "TLRH",
            "TDQO", "TDQH", "TDRO", "TDRH",
            "SLQO", "SLQH", "SLRO", "SLRH",
            "SDQO", "SDQH", "SDRO", "SDRH"
        ]
    
    def setUpGrid(self):
        """Create and return an empty NxN grid for the game."""
        return [['.' for _ in range(self.N)] for _ in range(self.N)]
    
    def __str__(self):
        """Return a string representation of the board with all pieces in green."""
        cell_width = 5
        top = "┌" + "┬".join(["─" * cell_width] * self.N) + "┐"
        mid = "├" + "┼".join(["─" * cell_width] * self.N) + "┤"
        bottom = "└" + "┴".join(["─" * cell_width] * self.N) + "┘"
        rows = [top]

        GREEN = '\033[32m'
        RESET = '\033[0m'

        for row in self.grid:
            row_str = "│"
            for cell in row:
                if cell == '.':
                    display_cell = f"{cell:^{cell_width}}"
                else:
                    display_cell = f"{GREEN}{cell:^{cell_width}}{RESET}"
                row_str += display_cell + "│"
            rows.append(row_str)
            rows.append(mid)
        rows[-1] = bottom  # replace the last mid with bottom
        return "\n".join(rows)
    
    def selectPiece(self, current_player):
        """
        Allow a human player to select a piece from available pieces.
        Removes chosen piece from the pool and returns it.
        """
        print(f"Available pieces: {', '.join(self.pieces)}")
        while True:
            piece = input(f'{current_player}, select a piece (e.g., TLQO): ').strip().upper()  
            if len(piece) != self.N:
                print('Too short length for input')
                continue
            if piece in self.pieces: ## if valid piece
                self.pieces.remove(piece)
                return piece
            else:
                print("Invalid piece. Please select from the available pieces.")
                continue    
    
    def selectRowCol(self):
        """Prompt human player for a valid (row, col) position on the grid."""
        while True:
            row = input(f'Enter row (0-{self.N-1}): ').strip()
            col = input(f'Enter column (0-{self.N-1}): ').strip()
            if not (row.isdigit() and col.isdigit()):
                print(f'Row and column must be numbers between 0 and {self.N-1} .')
                continue
            row, col = int(row), int(col)
            if not (0 <= row < self.N and 0 <= col < self.N):
                print(f'Row and column must be between 0 and {self.N-1}.')
                continue
            return row, col
    
    def getColumn(self, col, grid):
        """Return the column as a list from the grid."""
        return list(zip(*grid))[col]
        
    def isSlotEmpty(self, row, col, grid = None):
        """Check if a specific slot is empty ('.')."""
        if grid is None:
            grid = self.grid
        return grid[row][col] == '.'
    
    def fillSlot(self, piece, row, col, grid = None):
        """
        Place a piece in the grid if the slot is empty.
        Returns True if successful, False otherwise.
        """
        if grid is None:
            grid = self.grid
        if self.isSlotEmpty(row, col, grid): ## If slot is empty
            grid[row][col] = piece
            return True
        return False
    
    def isWinner(self, grid=None):
        """
        Check if there is a winning line in the grid.
        A line is winning if all 4 pieces share at least one attribute.
        """
        if grid is None:
            grid = self.grid
        N = self.N

        def checkLineWin(line):
            if '.' in line:
                return False
            for k in Quarto.attributes.keys():
                count = 0
                for r in line:
                    if k in r:
                        count += 1
                if count == N: ## All pieces share this attribute
                    return True
            return False    
        
        for row in grid:
            if checkLineWin(row):
                return True
        for col in range(N):
            if checkLineWin(self.getColumn(col, grid)):
                return True  
        if checkLineWin([grid[i][i] for i in range(N)]):
            return True
        if checkLineWin([grid[i][N - i - 1] for i in range(N)]):
            return True    
        return False  
        
    def hasEmptySlots(self, grid = None):
        """Return True if at least one empty slot ('.') exists in the grid."""
        if grid is None:
            grid = self.grid
        return any('.' in row for row in grid)   
    
    def playGame(self):
        """Main game loop handling human vs AI turns."""
        print('Welcome to Quarto!')
        print('Player 2 is Computer.\n')
        print(self)
        choice = input('\nYou want 1st or 2nd turn(f/s)? ').strip().upper()
        while choice not in ['F', 'S']:
            print('Enter F or S only!')
            choice = input('>').strip().upper()
        piece_to_place = None    
        player_a_turn = (choice == 'F') 
        if player_a_turn:  # Human first
            self.human_chooser, self.ai_placer = 'A', 'B'
            self.ai_chooser, self.human_placer = 'B', 'A'
        else:              # AI first
            self.ai_chooser, self.human_placer = 'A', 'B'
            self.human_chooser, self.ai_placer = 'B', 'A'
            
        while True:
            chooser, placer = ('A', 'B') if player_a_turn else ('B', 'A')
            ## Choosing a Piece
            if chooser == 'A':
                print(f"{chooser}'s Turn to choose a piece ")
                piece_to_place = self.selectPiece(chooser)
            else:
                print('Computer is choosing piece....')
                piece_to_place = self.chooseBestPiece(self.grid, self.pieces, placer)
                os.system('cls')
                print(f"Computer selects piece for you: {piece_to_place}")
                self.pieces.remove(piece_to_place)
            print(self)
            ## Placing a Piece
            if placer == 'A':
                print(f"{placer}'s Turn to place a piece ")
                row, col = self.selectRowCol()
                while not self.fillSlot(piece_to_place, row, col):
                    print('Slot is not empty, choose another slot.')
                    row, col = self.selectRowCol()
                    os.system('cls')
            else:
                print('Computer is thinking....')
                pos = self.chooseBestPlacement(self.grid, chooser, placer, piece_to_place)
                if pos is None:
                    print("No valid moves left for computer to place.")
                    break
                row, col = pos
                self.fillSlot(piece_to_place, row, col)
                os.system('cls')
                print(f"Computer placed {piece_to_place} at ({row}, {col}).")
            print(self)
        
            
            if self.isWinner():
                print('Human Won!' if placer == 'A' else 'Computer Won!')
                break
            if not self.hasEmptySlots():
                print('All slots are filled. Game is draw!')
                break
            player_a_turn = not player_a_turn ## Switch turns
            
class QuartoAI(Quarto):
    """
    AI extension of Quarto.
    Implements minimax with alpha-beta pruning, evaluation function,
    and logic for choosing the best piece and placement.
    """
    def __init__(self):
        super().__init__()
        
    def getAvailablePieces(self):
        """Return the list of pieces still available."""
        return self.pieces
    
    def getAvailableRowCol(self, grid):
        """Return a list of all empty (row, col) positions in the grid."""
        return [(i, j) for i in range(self.N) for j in range(self.N) if grid[i][j] == '.']
    
    def getAdaptiveDepth(self, grid):
        """Adjust search depth based on how many empty slots are left."""
        empty_slots = sum(row.count('.') for row in grid)
        if empty_slots >= 14:
            return 4  # Shallower depth for early game
        elif empty_slots >= 10:
            return 5
        elif empty_slots >= 6:
            return 6
        else:
            return 7
    
    def isTerminal(self, grid):
        """Check if the game has ended (win or draw)."""
        return self.isWinner(grid) or not self.hasEmptySlots(grid)
    
    def countAttributes(self, line):
        """Count how many times each attribute appears in a line."""
        # Counter counts how many times each element appears in an iterable.
        chars = (c for piece in line if piece != '.' for c in piece) 
        return dict(Counter(chars))
    
    def evaluateBoard(self, grid, placer, chooser):
        """
        Heuristic evaluation of the board:
        - Winning and losing states handled first.
        - Lines checked for threats and opportunities.
        - Considers both placer (immediate outcome) and chooser (future control).
        - Adds positional bonuses (center > edge > corner).
        """
        # --- Terminal conditions ---
        if self.isWinner(grid):
            if placer == self.ai_placer:   # AI wins
                return 100000
            if placer == self.human_placer:  # Human wins
                return -100000
        if not self.hasEmptySlots(grid):
            return 0  # Draw

        score = 0
        N = self.N

        # --- Collect all rows, cols, diagonals ---
        lines_list = list(grid)  # copy of rows
        for c in range(N):
            lines_list.append(self.getColumn(c, grid))
        lines_list.append([grid[i][i] for i in range(N)])              # main diagonal
        lines_list.append([grid[i][N - 1 - i] for i in range(N)])      # anti-diagonal

        # --- Line evaluation ---
        for line in lines_list:
            counts = self.countAttributes(line)
            empty = line.count('.')

            for attr, count in counts.items():
                # Immediate win/loss threat
                if count == N - 1 and empty == 1:
                    score += 500 if placer == self.ai_placer else -500
                    break  # avoid double-counting this line
                # Medium-term potential (chooser matters here)
                elif count == N - 2 and empty == 2:
                    score += 100 if chooser == self.ai_chooser else -100
                # Weak influence
                elif count == N - 3 and empty == 3:
                    score += 35 if chooser == self.ai_chooser else -35

        # --- Positional bonuses ---
        # Center control (strong bonus)
        for r, c in ((1, 1), (1, 2), (2, 1), (2, 2)):
            if grid[r][c] != '.':
                score += 80 if placer == self.ai_placer else -80

        # Edge positions (mild bonus)
        edge_positions = ((0,1),(0,2),(1,0),(2,0),(3,1),(3,2),(1,3),(2,3))
        for r, c in edge_positions:
            if grid[r][c] != '.':
                score += 20 if placer == self.ai_placer else -20

        # Corner positions (smallest bonus)
        corner_positions = ((0,0), (0,3), (3,0), (3,3))
        for r, c in corner_positions:
            if grid[r][c] != '.':
                score += 40 if placer == self.ai_placer else -40

        return score

    def simulateMove(self, piece, row, col, grid):
        """Return a new grid with the given piece placed at (row, col)."""
        new_grid = [r.copy() for r in grid]  
        new_grid[row][col] = piece
        return new_grid  
    
    def minimax(self, grid, depth, isPlacingPhase, chooser, placer, alpha, beta, piece):
        """
        Minimax with alpha-beta pruning.
        - If placing phase: maximize score (AI tries to place at best).
        - If choosing phase: minimize score (AI tries to give worst piece).
        Roles swap each turn:
        placer -> chooser, chooser -> placer
        """
        if depth == 0 or self.isTerminal(grid):
            return self.evaluateBoard(grid, placer, chooser)

        if isPlacingPhase:
            best_val = float('-inf')
            for row, col in self.getAvailableRowCol(grid):
                new_grid = self.simulateMove(piece, row, col, grid)
                # swap roles after placement
                score = self.minimax(
                    new_grid,
                    depth - 1,
                    False,
                    placer,   # placer becomes chooser
                    chooser,  # chooser becomes placer
                    alpha, beta,
                    None
                )
                best_val = max(best_val, score)
                alpha = max(alpha, score)
                if beta <= alpha:  # prune
                    break
            return best_val
        
        else:  # choosing phase
            best_val = float('inf')
            for next_piece in self.getAvailablePieces():
                # swap roles after choosing
                score = self.minimax(
                    grid,
                    depth - 1,
                    True,
                    placer,   # placer becomes chooser
                    chooser,  # chooser becomes placer
                    alpha, beta,
                    next_piece
                )
                best_val = min(best_val, score)
                beta = min(beta, score)
                if beta <= alpha:  # prune
                    break
            return best_val
        
    def chooseBestPlacement(self, grid, chooser, placer, piece):
        """
        Choose the best slot to place the given piece.
        Uses minimax and checks for immediate wins first.
        """
        depth = self.getAdaptiveDepth(grid)
        available_positions = self.getAvailableRowCol(grid)
        if not available_positions:
            return None  # No available positions
        ## Immediate Win Check for AI
        for row, col in available_positions:
            new_grid = self.simulateMove(piece, row, col, grid)
            if self.isWinner(new_grid):
                return (row, col)
        ## Otherwise, use minimax to find best scoring move    
        best_score, best_move = float('-inf'), None
        alpha, beta = float('-inf'), float('inf')
        for row, col in available_positions:
            new_grid = self.simulateMove(piece, row, col, grid)
            # next is choosing phase
            # swap: placer becomes chooser
            # swap: chooser becomes placer
            score = self.minimax(new_grid, depth, False, placer, chooser, alpha, beta, None)
            if score > best_score:
                best_score, best_move = score, (row, col)
            alpha = max(alpha, best_score)
            if beta <= alpha:  # prune
                break
        return best_move 
    
    def chooseBestPiece(self, grid, remaining_pieces, opponent):
        """
         Choose the best piece to give to the opponent.
         Avoids pieces that cause immediate loss.
        Uses minimax to minimize opponent's advantage.
        """
        best_piece, best_score = None, float('inf')
        depth = self.getAdaptiveDepth(grid)
        safe_pieces = []

        # Check for immediate loss pieces
        for piece in remaining_pieces:
            unsafe = False
            for row, col in self.getAvailableRowCol(grid):
                new_grid = self.simulateMove(piece, row, col, grid)
                if self.isWinner(new_grid):
                    unsafe = True
                    break
            if not unsafe:
                safe_pieces.append(piece)

        # If no safe pieces, pick random
        if not safe_pieces:
            return random.choice(remaining_pieces) if remaining_pieces else None

        # Evaluate only safe pieces with minimax
        for piece in safe_pieces:
            score = self.minimax(
                grid, depth, True, self.ai_chooser, opponent,
                float('-inf'), float('inf'), piece
            )
            if score < best_score:
                best_score, best_piece = score, piece
        return best_piece
    
## Main Program    
if __name__ == "__main__":
    game = QuartoAI()
    game.playGame() 
# --------------------------
# End of Quarto Game Code
# Written by: Husnain Maroof
# --------------------------