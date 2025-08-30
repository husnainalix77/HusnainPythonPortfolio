"""Checkers(Draughts) Game - Coded and Documented - Husnain Maroof ML Engineer - 12 Sep, 2025.""" 
import os
import platform
import time
class Checkers:
    """A class representing the game of Checkers with rules and mechanics."""
    players: list[tuple[str, str]] = [('Human', 'R'), ('Computer', 'B')]
    letters: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    def __init__(self, N: int) -> None:
        """
        Initialize a Checkers board of size N x N.
        
        Args:
            N (int): Size of the board (usually 8 for standard Checkers).
        """
        self.N = N
        self.grid = self.setUpGrid()
        self.turn = 0
        
    def clear_screen(self):
        """
        Clears the console screen based on the operating system.
        """
        os_name = platform.system()
        if os_name == 'Windows':  # For Windows
            os.system('cls')
        else:  # For Mac, Linux, and others
            os.system('clear')
            
    def setUpGrid(self) -> list[list[str]]:
        """
        Create and initialize the grid with Red ('R') and Black ('B') pieces.
        
        Returns:
            list[list[str]]: A 2D list representing the Checkers board.
        """
        grid = [['-' if (i + j) % 2 == 1 else '.' for j in range(self.N)] for i in range(self.N)]
        row_top = (self.N // 2) - 1
        for i in range(row_top):
            for j in range(self.N):
                if (i + j) % 2 == 1:
                    grid[i][j] = 'B'

        row_bottom = (self.N // 2) + 1
        for i in range(row_bottom, self.N):
            for j in range(self.N):
                if (i + j) % 2 == 1:
                    grid[i][j] = 'R'
        return grid
    
    @classmethod
    def pieces(cls) -> list[str]:
        """Return a list of all valid piece symbols."""
        return ['-', '.', 'B', 'BK', 'R', 'RK']
    
    @staticmethod
    def getColor(cell: str) -> str:
        """
        Args:
            cell (str): The cell value ('R', 'B', 'RK', 'BK', '-', '.').

        Returns:
            str: A colored Unicode symbol or placeholder for the cell.
        """
        BLACK_B = "\033[30m●\033[0m"        # black circle for normal B
        RED_R   = "\033[38;5;196m●\033[0m"  # red circle for normal R
        BLACK_K = "\033[1;30m♔\033[0m"      # black king with crown
        RED_K   = "\033[1;38;5;196m♔\033[0m" # red king with crown
        if cell == '-': return '   '
        if cell == '.': return ' . '
        if cell == 'B': return f" {BLACK_B} "
        if cell == 'R': return f" {RED_R} "
        if cell == 'BK': return f" {BLACK_K} "
        if cell == 'RK': return f" {RED_K} "
        return f" {cell} "
 
    def __str__(self) -> str:
        """
        Return a pretty-printed string of the board with Unicode formatting.

        Returns:
            str: The current board in human-readable format.
        """
        horizontal = "───"
        col_header = "   " + " ".join(f" {self.letters[i]} " for i in range(self.N))
        top_border = "  ┌" + "┬".join([horizontal] * self.N) + "┐"
        mid_border = "  ├" + "┼".join([horizontal] * self.N) + "┤"
        bottom_border = "  └" + "┴".join([horizontal] * self.N) + "┘"
        lines = [col_header, top_border]
        for i, row in enumerate(self.grid):
            row_str = f"{i+1:>2}│" + "│".join(Checkers.getColor(cell) for cell in row) + "│"
            lines.append(row_str)
            if i < self.N - 1:
                lines.append(mid_border)
        lines.append(bottom_border)
        return "\n".join(lines)
    
    def __repr__(self) -> str:
        """
        Return an unambiguous string representation of the Checkers object.

        Returns:
            str: Representation in the form 'Checkers(N)'.
        """
        return f'CheckersAI({self.N})'
    
    def validMove(self, user_mark: str, start_pos: str, end_pos: str, grid: list[list[str]] | None = None)-> str | bool:
        """
        Validate and execute a move on the board.

        Args:
            user_mark (str): The player's piece ('R' or 'B').
            start_pos (str): The starting position (e.g., "A3").
            end_pos (str): The ending position (e.g., "B4").
            grid (list[list[str]], optional): Grid to validate on. Defaults to self.grid.

        Returns:
            str | bool: 
                - 'simple' for a normal move,
                - 'capture' for a capturing move,
                - 'RK' or 'BK' if the piece becomes a king,
                - False if the move is invalid.
        """
        if grid is None:
            grid = self.grid
        if len(start_pos) < 2 or len(end_pos) < 2:
            print("Invalid input format. Use like E6.")
            return False  
        opponent_mark = 'B' if user_mark == 'R' else 'R'    
        try:
            row_1 = int(start_pos[1:]) - 1
            row_2 = int(end_pos[1:]) - 1
            col_1 = ord(start_pos[0]) - ord('A')
            col_2 = ord(end_pos[0]) - ord('A')
        except (ValueError, IndexError):
            return False
        if not (0 <= row_1 < self.N and 0 <= col_1 < self.N and
                0 <= row_2 < self.N and 0 <= col_2 < self.N):
            return False 
        ## if destination square is not playable
        if grid[row_2][col_2] != '-':
            return False
        piece = grid[row_1][col_1]
        if piece != user_mark and piece != f'{user_mark}K': ## if piece not is B and BK or not R and RK
            return False
        ## King Check
        isKing = piece.endswith('K')
        ## Simple Move, one step
        if abs(row_2 - row_1 ) == 1 and abs(col_2 - col_1) == 1:
            if isKing or (user_mark == 'R' and row_2 < row_1) or (user_mark == 'B' and row_2 > row_1):
                grid[row_2][col_2] = piece
                grid[row_1][col_1] = '-'
                if not isKing: ## King Promotion
                    if user_mark == 'R' and row_2 == 0:
                        grid[row_2][col_2] = 'RK'
                        return 'RK'
                    elif user_mark == 'B' and row_2 == self.N - 1:
                        grid[row_2][col_2] = 'BK'
                        return 'BK'
                return 'simple'
            return False 
        ## Capture Move, one step
        if abs(row_2 - row_1 ) == 2 and abs(col_2 - col_1) == 2:
            jump_row = (row_1 + row_2) // 2
            jump_col = (col_1 + col_2) // 2
            if grid[jump_row][jump_col] in [opponent_mark, f'{opponent_mark}K'] and grid[row_2][col_2] =='-':
                if isKing or (user_mark == 'R' and row_2 < row_1) or (user_mark == 'B' and row_2 > row_1):
                    grid[row_2][col_2] = piece
                    grid[row_1][col_1] = '-'
                    grid[jump_row][jump_col] = '-'
                    if not isKing: ## King Promotion
                        if user_mark == 'R' and row_2 == 0:
                            grid[row_2][col_2] = 'RK'
                            return 'RK'
                        elif user_mark == 'B' and row_2 == self.N - 1:
                            grid[row_2][col_2] = 'BK'
                            return 'BK'
                    return 'capture'
            return False                 
        return False   
    
    def canCapturePieces(self, current_pos: str, user_mark: str, grid = None) -> bool:
        """
        Check if a given piece can capture any opponent piece.

        Args:
            current_pos (str): Current position of the piece (e.g., "C5").
            user_mark (str): The player's piece ('R' or 'B').

        Returns:
            bool: True if a capture is possible, False otherwise.
        """
        if grid is None:
            grid = self.grid
        try:
            row = int(current_pos[1:]) - 1
            col = ord(current_pos[0]) - ord('A')
        except (ValueError, IndexError):
            return False
        piece = self.grid[row][col]
        isKing = piece.endswith('K')
        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)] if isKing else \
                     [(-2, -2), (-2, 2)] if user_mark == 'R' else [(2, -2), (2, 2)]
        opponent_mark = 'B' if user_mark == 'R' else 'R'
        for dr, dc in directions:
            next_row, next_col = row + dr, col + dc
            if 0 <= next_row < self.N and 0 <= next_col < self.N:
                jumped_row, jumped_col = (row + next_row) // 2, (col + next_col) // 2 ## At center, there will be opponent
                if self.grid[jumped_row][jumped_col] in [opponent_mark, f'{opponent_mark}K']\
                    and self.grid[next_row][next_col] == '-':
                    return True
        return False
    
    def allAvailableSimpleMoves(self, user_mark: str, grid = None) -> list[tuple[str, str]]:
        """
        Get all simple (non-capturing) moves for the player.

        Args:
            user_mark (str): The player's piece ('R' or 'B').

        Returns:
            list[tuple[str, str]]: List of tuples (start_pos, end_pos) for all simple moves.
        """
        if grid is None:
            grid = self.grid
        moves = []
        for r in range(self.N):
            for c in range(self.N):
                cell = grid[r][c]
                if cell == user_mark or cell == f'{user_mark}K':
                    start_pos = self.letters[c] + str(r + 1)
                    isKing = cell.endswith('K')
                    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if isKing else \
                                [(1, -1), (1, 1)] if user_mark == 'B' else [(-1, -1), (-1, 1)]
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.N and 0 <= nc < self.N and grid[nr][nc] == '-':
                            end_pos = self.letters[nc] + str(nr + 1)
                            moves.append((start_pos, end_pos))
        return moves

    def allAvailableCaptures(self, user_mark: str, grid =None ) -> list[str]:
        """
        Get all board positions from where the player can make captures.

        Args:
            user_mark (str): The player's piece ('R' or 'B').

        Returns:
            list[str]: List of positions (e.g., ["D6", "E3"]) where captures are possible.
        """
        if grid is None:
            grid = self.grid
        all_captures = []
        for r in range(self.N):
            for c in range(self.N):
                cell = grid[r][c]
                if cell == user_mark or cell == f'{user_mark}K':
                    pos = self.letters[c] + str(r+1)
                    if self.canCapturePieces(pos, user_mark, grid):
                        all_captures.append(pos)
        return all_captures  
       
    def isWinner(self, user_mark: str, grid = None) -> bool: 
        """
        Check if the given player has won the game.

        A player wins if the opponent has no remaining pieces
        or no valid legal moves.

        Args:
            user_mark (str): The player's piece ('R' or 'B').

        Returns:
            bool: True if the player has won, False otherwise.
        """
        if grid is None:
            grid = self.grid
        opponent_mark = 'B' if user_mark == 'R' else 'R'
        if not any(cell in [opponent_mark, f'{opponent_mark}K'] for row in grid for cell in row):
            return True
        ## Check for any legal move
        if not self.allAvailableCaptures(opponent_mark) and\
            not self.allAvailableSimpleMoves(opponent_mark):
                return True
        return False    
    
    def isDraw(self, grid = None) -> bool:
        """
        Check if the game is a draw.

        A game is drawn if neither 'R' nor 'B' has won.

        Returns:
            bool: True if the game is a draw, False otherwise.
        """
        # If either side has already won, it's not a draw
        if grid is None:
            grid = self.grid
        if self.isWinner('R') or self.isWinner('B'):
            return False
        #Both players have no legal moves
        if (not self.allAvailableCaptures('R') and not self.allAvailableSimpleMoves('R') and
            not self.allAvailableCaptures('B') and not self.allAvailableSimpleMoves('B')):
            return True
        # Board is filled with pieces, but no moves
        if all(cell != '-' for row in grid for cell in row):
            return True
        return False 
            
    def playGame(self) -> None:
        """
        Start and run a full game of Checkers in the console.

        The human plays as Red ('R') and the computer plays as Black ('B').
        Human moves are collected through user input.
        """
        print(self)
        print('\nRed: Human\tBlack: AI')
        print("Squares with '.' are non-playable.")
        print('Only Diagonal Movement is allowed. Move should be like E6 -> D5.')
        print('-'*40)
        time.sleep(0.7)
        while True:
            current_player, mark = self.players[self.turn % 2]
            all_captures = self.allAvailableCaptures(mark)
            turn_finished = False
            if mark == 'R':  # Human Turn
                if all_captures:
                    print(f"Capture(s) available. You must start from one of {','.join(all_captures)}")
                    start_pos = input(f'{current_player}({mark}), enter your starting point: ').strip().upper()
                    while start_pos not in all_captures:
                        print(f"You must choose from: {','.join(all_captures)}")
                        start_pos = input(f'{current_player}({mark}), enter your starting point: ').strip().upper()

                    current_pos = start_pos
                    # Multi-capture loop
                    while True:
                        end_pos = input(f'{current_player}({mark}), enter your ending point from {current_pos}: ').strip().upper()
                        temp_grid = [row.copy() for row in self.grid]
                        move = self.validMove(mark, current_pos, end_pos, temp_grid)
                        if move not in ['capture', f'{mark}K']:
                            print('Invalid capture move. Try again.')
                            continue
                        # Commit the move
                        move = self.validMove(mark, current_pos, end_pos)
                        self.clear_screen()
                        print(self)
                        if move == f'{mark}K':
                            print('You have become King!')

                        current_pos = end_pos
                        if self.canCapturePieces(current_pos, mark):
                            print('You can capture again with the same piece.')
                            continue
                        else:
                            print('No more captures. Turn ends now.')
                            turn_finished = True
                            break
                else:
                    # Simple move loop
                    print('No captures are available. You can make simple move.')
                    while True:
                        start_pos = input(f'{current_player}({mark}), enter your starting point: ').strip().upper()
                        end_pos = input(f'{current_player}({mark}), enter your ending point: ').strip().upper()
                        temp_grid = [row.copy() for row in self.grid]
                        move = self.validMove(mark, start_pos, end_pos, temp_grid)
                        if move in ['simple', f'{mark}K']:
                            self.validMove(mark, start_pos, end_pos)  # commit
                            if move == f'{mark}K':
                                print('You have become King!')
                            self.clear_screen()    
                            print(self)
                            print('Move Completed. Turn ends.')
                            turn_finished = True
                            break
                        else:
                            print('Invalid Move! Try again.')
                 
            else:  # AI Turn 
                self.aiMove(mark) 
                turn_finished = True 
            if self.isWinner(mark):
                print(f'{current_player}({mark}) won!')
                print('='*50)
                print('Game is Over')
                break  
            if self.isDraw():
                print('Game is Draw!')
                break 
            if turn_finished:
                self.turn = (self.turn + 1) % 2  
                     
## AI Class            
class CheckersAI(Checkers):
    def __init__(self, N):
        """
    Initialize the Checkers AI with a board of size N x N.

    Args:
        N (int): Size of the board (usually 8 for standard Checkers).
    """
        super().__init__(N)
    def isSafeLanding(self, r: int, c: int, grid: list[list[str]], AI_mark: str) -> bool:
        """
        Check if a piece landing at (r,c) is safe:
        1. No opponent can capture it immediately.
        2. Adjacent diagonals are empty to avoid easy attacks or block.
        """
        opponent_mark = 'R' if AI_mark == 'B' else 'B'
        
        # Step 1: Existing capture check
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        for dr, dc in directions:
            opp_r, opp_c = r + dr, c + dc
            land_r, land_c = r - dr, c - dc
            if 0 <= opp_r < self.N and 0 <= opp_c < self.N and 0 <= land_r < self.N and 0 <= land_c < self.N:
                if grid[opp_r][opp_c] in [opponent_mark, f'{opponent_mark}K'] and grid[land_r][land_c] == '-':
                    return False  # immediate capture possible
        
        # Step 2: Check adjacency around landing
        for dr, dc in directions:
            adj_r, adj_c = r + dr, c + dc
            if 0 <= adj_r < self.N and 0 <= adj_c < self.N:
                if grid[adj_r][adj_c] in [opponent_mark, f'{opponent_mark}K']:
                    return False  # adjacent opponent piece present
        
        return True

        
    def isStartOfCaptureChain(self, start_pos: str, user_mark: str, grid=None) -> bool:
        """Return True if moving AI piece here allows opponent to start multi-capture."""
        if grid is None:
            grid = self.grid
        r, c = int(start_pos[1:]) - 1, ord(start_pos[0]) - ord('A')
        piece = grid[r][c]   # <- read actual piece, e.g. 'R' or 'RK'
        isKing = piece.endswith('K')

        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)] if isKing else \
                    [(-2, -2), (-2, 2)] if piece.startswith('R') else [(2, -2), (2, 2)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.N and 0 <= nc < self.N:
                jumped_r, jumped_c = (r + nr)//2, (c + nc)//2
                if grid[jumped_r][jumped_c] in [user_mark, f'{user_mark}K'] and grid[nr][nc] == '-':
                    landing_pos = self.letters[nc] + str(nr+1)
                    temp_grid = [row.copy() for row in grid]
                    temp_grid[nr][nc] = piece
                    temp_grid[r][c] = '-'
                    if self.canCapturePieces(landing_pos, user_mark, temp_grid):
                        return True
        return False

        
    def evaluateBoard(self, grid=None) -> int:
        """Enhanced evaluation for AI strength."""
        if grid is None:
            grid = self.grid  
        opponent_mark = 'R'
        ai_mark = 'B'
        score = 0
        N = self.N
        #Endgame Logic
        total_pieces = sum(1 for row in grid for cell in row if cell in ['B', 'BK', 'R', 'RK'])
        is_endgame = total_pieces < 8  # A threshold to define the endgame
        # Define center positions for control bonus
        center_rows = [N//2 - 1, N//2, N//2 + 1, N//2 + 2] if N >= 8 else [N//2 - 1, N//2]
        center_cols = [N//2 - 1, N//2, N//2 + 1, N//2 + 2] if N >= 8 else [N//2 - 1, N//2]
        
        
        # Helper functions

        def canBeCapturedBy(pos, opp_mark, grid): ## assume opp-mark = R
            N = self.N 
            r, c = pos
            directions = [(-1,-1), (-1,1), (1,-1), (1,1)]# opponent piece adjacent
            for dr, dc in directions:
                opp_r, opp_c = r + dr, c + dc             # opponent piece location
                land_r, land_c = r - dr, c - dc          # landing spot for capture
                if 0 <= opp_r < N and 0 <= opp_c < N and 0 <= land_r < N and 0 <= land_c < N:
                    if grid[opp_r][opp_c] in [opp_mark, f'{opp_mark}K'] and grid[land_r][land_c] == '-':
                        return True
            return False

        def isConnected(r, c, mark, grid):
            directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    if grid[nr][nc].startswith(mark):
                        return True
            return False
        for r in range(N):
            for c in range(N):
                cell = grid[r][c]
                # Step 1: Piece and King Value ---
                if cell == ai_mark:
                    score += 50
                    if is_endgame:
                        score += 20
                elif cell == f'{ai_mark}K':
                    score += 100
                    if is_endgame:
                        score += 20
                elif cell == opponent_mark:
                    score -= 5
                    if is_endgame:
                        score -= 20
                elif cell == f'{opponent_mark}K':
                    score -= 15
                    if is_endgame:
                        score -= 30
       
                #  Step 2: Back Row Safety ---
                if r == N-1 and cell == ai_mark:
                    score += 30
                if r == 0 and cell == opponent_mark:
                    score -= 30
                #  Step 3: Promotion Potential ---
                # B moves down, closer to bottom (N-1) → higher score
                if cell == ai_mark:
                    score += r * 5
                # R moves up, closer to top (0) → higher score, so subtract less
                elif cell == opponent_mark:
                    score -= (N - r - 1) * 5
                # Step 4 cont.: King Central Bonus ---
                if r in center_rows and c in center_cols:
                    if cell.endswith('K'):
                        score += 20 if cell.startswith(ai_mark) else -20
                # for King Safety
                if cell == f'{ai_mark}K':
                    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.N and 0 <= nc < self.N and grid[nr][nc] == f'{opponent_mark}K':
                            score -= 70  # Apply a high penalty for being adjacent to opponent's king
                elif cell == f'{opponent_mark}K':
                    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.N and 0 <= nc < self.N and grid[nr][nc] == f'{ai_mark}K':
                            score += 70 # Reward for being adjacent to opponent's king  
                                  
                #Check for King Mobility
                if cell == f'{ai_mark}K':
                    king_moves = 0
                    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.N and 0 <= nc < self.N and grid[nr][nc] == '-':
                            king_moves += 1
                    if king_moves < 2:  # Penalize if the king has fewer than 2 open squares
                        score -= 40
                elif cell == f'{opponent_mark}K':
                    king_moves = 0
                    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.N and 0 <= nc < self.N and grid[nr][nc] == '-':
                            king_moves += 1
                    if king_moves < 2:
                        score += 40        

                # --- Step 7: Threat & Safety Awareness ---
                # For AI pieces
                if cell in [ai_mark, f'{ai_mark}K']:
                    # 1. Penalize if AI piece can be captured
                    if canBeCapturedBy((r, c), opponent_mark, grid):
                        score -= 2000 if not cell.endswith('K') else 5000  # harsher for kings

                    # 2. Penalize if AI moving here would land next to opponent (unsafe landing)
                    if not self.isSafeLanding(r, c, grid, ai_mark):
                        score -= 1500

                    # 3. Penalize if AI move starts a capture chain for human
                    current_pos = self.letters[c] + str(r + 1)
                    if self.isStartOfCaptureChain(current_pos, opponent_mark, grid):
                        score -= 15000  # heavy penalty

                # For Human pieces
                elif cell in [opponent_mark, f'{opponent_mark}K']:
                    # 1. Reward AI if human piece can be captured safely
                    if canBeCapturedBy((r, c), ai_mark, grid):
                        score += 2000 if not cell.endswith('K') else 5000

                    # 2. Penalize human landing on squares that are safe for AI to capture
                    if not self.isSafeLanding(r, c, grid, opponent_mark):
                        score += 1500

                    # 3. Penalize human move if it starts a chain of captures that AI can exploit
                    current_pos = self.letters[c] + str(r + 1)
                    if self.isStartOfCaptureChain(current_pos, ai_mark, grid):
                        score += 15000  # reward AI for forcing a bad human setup


                    
                #  Step 6: Piece Connectivity ---
                if cell.startswith(ai_mark) and isConnected(r, c, ai_mark, grid):
                    score += 500
                if cell.startswith(opponent_mark) and isConnected(r, c, opponent_mark, grid):
                    score -= 500
        #  Step 7: Mobility / Capture Moves ---
        ai_simple_moves = self.allAvailableSimpleMoves(ai_mark)
        opponent_simple_moves = self.allAvailableSimpleMoves(opponent_mark)
        ai_capture_moves = self.allAvailableCaptures(ai_mark)
        opponent_capture_moves = self.allAvailableCaptures(opponent_mark)
    
        score += len(ai_simple_moves) * 20
        score -= len(opponent_simple_moves) * 20
        score += len(ai_capture_moves) * 1000
        score -= len(opponent_capture_moves) * 1000
        return score

    def availableValidMoves(self, player_mark: str, grid: list[list[str]]) -> list[tuple[str, str]]:
        """
        Efficiently generate all valid moves (captures + simple moves) for a given player
        on the provided grid by checking only legal directions.
        """
        N = self.N
        letters = self.letters
        capture_moves = []

        opponent_mark = 'R' if player_mark == 'B' else 'B'

        # Get positions that can capture
        captures = self.allAvailableCaptures(player_mark, grid)
        for start_pos in captures:
            r = int(start_pos[1:]) - 1
            c = ord(start_pos[0]) - ord('A')
            piece = grid[r][c]
            isKing = piece.endswith('K')
            # Determine directions
            directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)] if isKing else \
                        [(-2, -2), (-2, 2)] if player_mark == 'R' else [(2, -2), (2, 2)]

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    jumped_r, jumped_c = (r + nr) // 2, (c + nc) // 2
                    if grid[jumped_r][jumped_c] in [opponent_mark, f'{opponent_mark}K'] and grid[nr][nc] == '-':
                        end_pos = letters[nc] + str(nr + 1)
                        capture_moves.append((start_pos, end_pos))

        # Simple moves
        simple_moves = self.allAvailableSimpleMoves(player_mark, grid)
        return [*capture_moves, *simple_moves]

    
    def getAdaptiveDepth(self) -> int:
        """
    Dynamically determine the AI's search depth based on remaining pieces.

    Returns:
        int: Recommended depth for minimax search.
    """
        total_pieces = sum(row.count('R') + row.count('B') + row.count('RK') + row.count('BK') for row in self.grid)
        capture_moves = len(self.allAvailableCaptures('B')) + len(self.allAvailableCaptures('R'))
        if capture_moves >= 3:
            return 6
        if total_pieces > 18:        # Early Opening
            return 4 
        elif total_pieces > 12:      # Midgame
            return 5
        elif total_pieces > 6:       # Late Midgame
            return 6 
        else:
            return 7
        
    def simulateMove(self, move: tuple[str, str], mark: str, grid: list[list[str]]) -> list[list[str]] | None:
        """
        Simulate applying a move on a copy of the board.

        Args:
            move (tuple[str, str]): The move as (start_pos, end_pos).
            mark (str): The player's piece ('R' or 'B').
            grid (list[list[str]]): The current board configuration.

        Returns:
            list[list[str]] | None: New grid after move, or None if invalid.
        """
        start_pos, end_pos = move
        new_grid = [row.copy() for row in grid]
        if self.validMove(mark, start_pos, end_pos, new_grid):
            return new_grid

    def minimax(self, grid: list[list[str]], depth: int, maximizingPlayer: bool, 
            AI_mark: str, alpha: float, beta: float) -> int:
        """
        Perform minimax search with alpha-beta pruning and quiescence search.
        """
        # Safeguard: terminate recursion if depth reaches 0
        if depth <= 0:
            return self.evaluateBoard(grid)
        # Check for game end conditions
        if self.isWinner('R', grid) or self.isWinner('B', grid) or self.isDraw(grid):
            return self.evaluateBoard(grid)
        opponent_mark = 'R' if AI_mark == 'B' else 'B'
        player_mark = AI_mark if maximizingPlayer else opponent_mark
        moves = self.availableValidMoves(player_mark, grid)

    # Sort moves: prioritize captures, then evaluation
        moves.sort(
        key=lambda move: (
            self.validMove(player_mark, move[0], move[1], [row.copy() for row in grid]) == 'capture',
            self.evaluateBoard(self.simulateMove(move, player_mark, [row.copy() for row in grid]))
        ),
        reverse=maximizingPlayer
    )
        if maximizingPlayer:
            maxEval = float('-inf')
            for move in moves:
                new_grid = self.simulateMove(move, AI_mark, grid)
                if new_grid is None:
                    continue
                # Always reduce depth to avoid infinite recursion
                eval_score = self.minimax(new_grid, depth - 1, False, AI_mark, alpha, beta)

                maxEval = max(maxEval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return maxEval

        else:  # Minimizing player
            minEval = float('inf')

            for move in moves:
                new_grid = self.simulateMove(move, opponent_mark, grid)
                if new_grid is None:
                    continue
                # Always reduce depth to avoid infinite recursion
                eval_score = self.minimax(new_grid, depth - 1, True, AI_mark, alpha, beta)

                minEval = min(minEval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return minEval

    def getBestMove(self, AI_mark: str) -> tuple[str, str] | None:
        """
        Select the best move for AI using minimax with adaptive depth.

        Args:
            AI_mark (str): The AI's piece ('B').

        Returns:
            tuple[str, str] | None: The best move as (start_pos, end_pos), or None if no move.
        """
        depth = self.getAdaptiveDepth()
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta =  float('inf')
        # Get all valid moves and sort them for initial evaluation
        moves = self.availableValidMoves(AI_mark, self.grid)
        # Prioritize capture moves first
        moves.sort(key=lambda move: (self.validMove(AI_mark, move[0], move[1], [row.copy() for row in self.grid]) == 'capture',\
            self.evaluateBoard(self.simulateMove(move, AI_mark, [row.copy() for row in self.grid]))),
           reverse=True)

        for move in moves:
            new_grid = self.simulateMove(move, AI_mark, self.grid)
            if new_grid is None:
                continue
            eval_score = self.minimax(new_grid, depth - 1, False, AI_mark, alpha, beta)
            if eval_score > best_score:
                best_score = eval_score
                best_move = move
                alpha = max(alpha, eval_score) # Update alpha in the main loop
        return best_move
        
    def aiMove(self, AI_mark):
        """Execute the best move for AI"""
        move = self.getBestMove(AI_mark)
        self.clear_screen()
        if move:
            start_pos, end_pos = move
            self.validMove(AI_mark, start_pos, end_pos)
            print(self)
            print('-'*10 + f'AI moves {start_pos} -> {end_pos}' + '-'*10)    
            r, c = int(end_pos[1:])-1, ord(end_pos[0])-ord('A')
            if self.grid[r][c].endswith('K'):
                print("AI became King!")
        else:
            print(f"AI ({AI_mark}) has no valid moves.")
            
## Main Program  
if __name__=='__main__':
    N: int = 8
    if N < 4:
        raise ValueError("Checkers board must be at least 4x4")
    game: CheckersAI = CheckersAI(N)
    game.playGame()
       
    
    