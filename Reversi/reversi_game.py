## Reversi(Othello) Game - Coded and Edited - by Husnain Maroof- on 9 Sep, 2025.
import time
import os
class Reversi:
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    players = [('Human', 'B'), ('Computer', 'W')]
    def __init__(self, N):
        self.N = N
        self.grid = self.setUpGrid()
        self.turn = 0
        # Precompute column lookup for fast string->index mapping
        self.col_map = {ch: i for i, ch in enumerate(self.letters[:self.N])}
    # ------------------ Board Setup ------------------
    def setUpGrid(self):
        'Sets up standard NxN grid'
        grid = [['-' for _ in range(self.N)] for _ in range(self.N)]
        mid = self.N // 2
        grid[mid-1][mid-1] = 'B'
        grid[mid-1][mid]   = 'W'
        grid[mid][mid-1]   = 'W'
        grid[mid][mid]     = 'B'
        return grid

    def getColor(self, cell):
        'Sets color for black pieces'
        if cell == 'B':
            return f"\033[90m{cell}\033[0m"
        return cell

    def dispGrid(self, highlight_moves_for=None):
        'Displays grid in unicode format and highlights available valid moves'
        headers = "   " + "   ".join(self.letters[:self.N])
        print("\n" + headers)
        print("  ╔" + "═══╦" * (self.N-1) + "═══╗")       
        valid_moves = []
        if highlight_moves_for:
            valid_moves = self.availableValidMoves(highlight_moves_for)
        
        for r in range(self.N):
            row_str = f"{r+1} ║"
            for c in range(self.N):
                cell = self.grid[r][c]
                move_str = self.letters[c] + str(r+1)
                if move_str in valid_moves:
                    row_str += ' * '  # Highlights valid move
                else:
                    row_str += f' {self.getColor(cell)} '
                row_str += '║'
            print(row_str)
            if r != self.N-1:
                print("  ╠" + "═══╬" * (self.N-1) + "═══╣")
        print("  ╚" + "═══╩" * (self.N-1) + "═══╝")

    def updateDisplay(self):
        'Updates display after each valid move'
        time.sleep(0.1)
        os.system('cls')  
  
    # ------------------ Move Validation ------------------
    def isValidMove(self, user_move, mark, grid=None, simulateMove=False):
        'Checks Validation of Move'
        if grid is None: ## if grid is not passed, uses original grid
            grid = self.grid
        row = int(user_move[1:]) - 1
        col = self.col_map[user_move[0]]
        if grid[row][col] != '-':
            return False

        opponent_mark = 'W' if mark == 'B' else 'B'
        directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)] ## Piece can flip opponent piece in 8 directions
        to_flip = []

        for dr, dc in directions:
            r, c = row + dr, col + dc
            path = []
            while 0 <= r < self.N and 0 <= c < self.N:
                if grid[r][c] == opponent_mark:
                    path.append((r,c))
                elif grid[r][c] == mark:
                    if path:
                        to_flip.extend(path)
                    break
                else:
                    break
                r += dr
                c += dc

        if to_flip: ## if at least one valid move found
            if not simulateMove:
                grid[row][col] = mark
                for r,c in to_flip:
                    grid[r][c] = mark
            return True
        return False

    def availableValidMoves(self, mark, grid=None):
        'Gives all available valid moves'
        if grid is None:
            grid = self.grid
        valid_moves = []
        for r in range(self.N):
            for c in range(self.N):
                user_move = self.letters[c] + str(r+1)
                if self.isValidMove(user_move, mark, grid, simulateMove=True):
                    valid_moves.append(user_move)
        return valid_moves

    # ------------------ Game Status ------------------
    def isGameOver(self):
        'Game is over when no valid move or no - is left'
        if '-' not in [cell for row in self.grid for cell in row]:
            return True
        for mark in ['B', 'W']:
            if self.availableValidMoves(mark): ## if at least one valid move found
                return False
        return True

    def countPieces(self, grid=None):
        'Counts number of pieces'
        if grid is None:
            grid = self.grid
        flat = [cell for row in grid for cell in row]
        black = flat.count('B')
        white = flat.count('W')
        return black, white

    def getWinner(self):
        'Decides winner based on number of pieces'
        black, white = self.countPieces()
        if black > white:
            return f'Human(B) won the game.\nBlack: {black}\tWhite: {white}'
        elif white > black:
            return f'Computer(W) won the game.\nBlack: {black}\tWhite: {white}'
        else:
            return f'Game is draw.\nBlack: {black}\tWhite: {white}'
        
    def isTerminal(self, grid): ## Will be used for evaluateBoard function
        if '-' not in [cell for row in grid for cell in row]:
            return True
        if not self.availableValidMoves('B', grid) and not self.availableValidMoves('W', grid):
            return True
        return False    

    # ------------------ AI: Minimax ------------------
    def evaluateBoard(self, grid=None):
        'Board Evaluation Criteria'
        if grid is None:
            grid = self.grid
        ai_mark, human_mark = 'W', 'B'
        score = 0
        N = self.N
    # 1. Piece Count: Simple score based on the number of pieces.
        human_pieces, ai_pieces = self.countPieces(grid)
        score += (ai_pieces - human_pieces) * 10
    # 2. Mobility: Score based on the number of available moves.
        ai_moves = len(self.availableValidMoves(ai_mark, grid))
        human_moves = len(self.availableValidMoves(human_mark, grid))
        score += (ai_moves - human_moves) * 50

    # 3. Corner Control: Highly valuable.
        corners = [(0, 0), (0, N - 1), (N - 1, 0), (N - 1, N - 1)]
        for r, c in corners:
            if grid[r][c] == ai_mark:
                score += 200
            elif grid[r][c] == human_mark:
                score -= 200

    # 4. Edge Control: Differentiate between safe and dangerous edges.
        edge_squares = set()
        dangerous_squares = set()
        for i in range(1, N - 1):
            # Top and bottom edges
            edge_squares.add((0, i))
            edge_squares.add((N - 1, i))
            # Left and right edges
            edge_squares.add((i, 0))
            edge_squares.add((i, N - 1))
    # Squares adjacent to corners, which are dangerous. Penalty for AI
    # Dangerous squares are the ones that are adjacent to a corner,
    # but are not corners themselves. Placing a piece on one of these squares can allow the opponent to capture a
    # corner on their next move
    
        dangerous_squares.update([(0, 1), (1, 0), (1, 1),
                                (0, N - 2), (1, N - 1), (1, N - 2),
                                (N - 1, 1), (N - 2, 0), (N - 2, 1),
                                (N - 1, N - 2), (N - 2, N - 1), (N - 2, N - 2)])
        for r in range(N):
            for c in range(N):
                if (r, c) in dangerous_squares: ## if ai in dangerous squares, penalty is for ai
                    if grid[r][c] == ai_mark:
                        score -= 50
                    elif grid[r][c] == human_mark: # if human in dangerous squares, reward is for human
                        score += 50
                elif (r, c) in edge_squares: 
                    if grid[r][c] == ai_mark:
                        score += 20
                    elif grid[r][c] == human_mark:
                        score -= 20
        return score
        
    def getAdaptiveDepth(self):
        'Adjust depth dynamically based on remaining empty squares'
        empty = sum(row.count('-') for row in self.grid)
        
        if empty <= 12:  # Endgame is considered when 12 or fewer empty squares are left
            # In the endgame, perform a deep search to find the optimal move.
            return empty
        elif empty > 40:    # Opening phase
            return 4
        elif empty > 20:   # Midgame
            return 5
        else:              # Late-midgame
            return 6  

    def simulateMove(self, move, mark, grid):
        'Simulates the specific move and updates grid'
        new_grid = [row.copy() for row in grid]
        self.isValidMove(move, mark, new_grid)
        return new_grid

    def minimax(self, grid, depth, maximizingPlayer, AI_mark, alpha, beta):
        'Implements Minimax Algorithm for givrn Depth'
        opponent_mark = 'W' if AI_mark == 'B' else 'B'
        if depth == 0 or self.isTerminal(grid):
            return self.evaluateBoard(grid)
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in self.availableValidMoves(AI_mark, grid):
                new_grid = self.simulateMove(move, AI_mark, grid)
                eval = self.minimax(new_grid, depth-1, False, AI_mark, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if alpha>=beta:
                    break ## Beta Pruning
            return maxEval
        else:
            minEval = float('inf')
            for move in self.availableValidMoves(opponent_mark, grid):
                new_grid = self.simulateMove(move, opponent_mark, grid)
                eval = self.minimax(new_grid, depth-1, True, AI_mark, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha Pruning
            return minEval

    def getBestMove(self, AI_mark):
        'Gives AI Best Move'
        depth = self.getAdaptiveDepth()
        if depth > 6:
            print("Computer is thinking deeper (endgame)... Please wait.")
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf') ## Lower bound
        beta = float('inf') ## Higher bound
        
        for move in self.availableValidMoves(AI_mark, self.grid):
            new_grid = self.simulateMove(move, AI_mark, self.grid)
            score = self.minimax(new_grid, depth-1, False, AI_mark, alpha, beta)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)    
        return best_move

    # ------------------ Main Game Loop ------------------
    def playGame(self):
        'Full Playable Reversi Game with AI'
        print('Player 2 is Computer(W).')
        print('Alphabets = column, numbers = row')
        while True:
            current_player, mark = self.players[self.turn % 2]
            valid_moves = self.availableValidMoves(mark) ## Gets all valid moves for B or W (based on turn)
            if mark == 'B':  # Human
                if valid_moves:
                    self.dispGrid(mark) 
                    while True:
                        user_move = input(f'{current_player}({mark}), enter move (e.g D3): ').strip().upper()
                        if len(user_move)<2 or user_move[0] not in self.letters[:self.N]:
                            print('Invalid input. Follow the instructions.')
                            continue
                        try:
                            row_num = int(user_move[1:])
                        except ValueError:
                            print('Row must be number.')
                            continue
                        if row_num < 1 or row_num > self.N:
                            print(f'Row must be 1-{self.N}')
                            continue
                        if user_move not in valid_moves:
                            print('Invalid move.')
                            continue
                        self.isValidMove(user_move, mark)
                        break
                else:
                    print(f"{current_player}({mark}) has no valid moves. Turn passes.")
                    time.sleep(0.1)
                    self.turn = (self.turn + 1) % 2
                    continue    
            else:  # AI
                if valid_moves:
                    self.dispGrid()
                    computer_move = self.getBestMove(mark)
                    self.isValidMove(computer_move, mark)
                    print(f"{current_player}({mark}) plays: {computer_move}")
                else:
                    print(f"{current_player}({mark}) has no valid moves, turn skipped.")

            if self.isGameOver():
                self.dispGrid()
                print('Game over!')
                print('='*40)
                print(self.getWinner())
                break
            self.turn = (self.turn+1)%2
            self.updateDisplay()
           

# ------------------ Run Game ------------------
if __name__ == '__main__':
    N = 8
    game = Reversi(N)
    game.playGame()
