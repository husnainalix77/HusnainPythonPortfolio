# ----------------------------------------------------------
# Maze Game
# Author: Husnain Maroof
# Date: 11 Oct, 2025
# Description: This Python program generates a solvable maze of variable size (5x5, 8x8, or 10x10) 
# using depth-first search. The player navigates through the maze to reach the exit.
# ----------------------------------------------------------
import random 
import os
import time
from colorama import Fore, Style, init
init(autoreset=True)

class Maze:
    """Class to generate, display, and solve a maze game."""
    DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)] # Down, Up, Right, Left
    def __init__(self, N):
        """
        Initialize the maze.
        Args:
            N (int): Size of the NxN maze.
        """
        self.__N = N
        self.__board = self.__generateMaze()
        self.__player_pos = (0, 0)
        self.__moves = {
            'w': self.__moveUp,
            's': self.__moveDown,
            'a': self.__moveLeft,
            'd': self.__moveRight
                }

    def dispBoard(self):
        """
        Display the maze inside a Unicode box.
        Player is blue, exit is green, start is magenta, walls are light black blocks, paths are empty.
        Works for any maze size (N x N).
        """
        N = self.__N
        # Determine inner width (each cell is 2 chars for walls/paths)
        inner_width = N * 2
        # Top border
        print('╔' + '═' * inner_width + '╗')

        for r, row in enumerate(self.__board):
            line = ''
            for c, cell in enumerate(row):
                if (r, c) == self.__player_pos:
                    line += Fore.YELLOW + 'P ' + Style.RESET_ALL
                elif cell == 'E':
                    line += Fore.RED + ' E' + Style.RESET_ALL
                elif cell == 'S':
                    line += Fore.MAGENTA + 'S ' + Style.RESET_ALL
                elif cell == 'X':
                    line += Fore.LIGHTBLACK_EX + '██' + Style.RESET_ALL
                else:  # path
                    line += '  '
            print(f'║{line}║')  # left & right borders
        # Bottom border
        print('╚' + '═' * inner_width + '╝')
                
    def __generateMaze(self):
        """
        Generate a solvable maze using depth-first search.
        Returns:
            list[list[str]]: 2D list representing the maze, with 'X' as walls, '_' as paths,
                             'S' as start, and 'E' as exit.
        """
        N = self.__N
        board = [list('X' * N) for _ in range(N)]
        # DFS to carve paths
        def dfs(r, c, visited):
            visited.add((r, c))
            board[r][c] = '_'
            dirs = Maze.DIRECTIONS[:]  # copy directions
            random.shuffle(dirs)       # shuffle directions at each step
            for dr, dc in dirs:
                nr, nc = r + dr * 2, c + dc * 2
                if 0 <= nr < N and 0 <= nc < N and (nr, nc) not in visited:
                    board[r + dr][c + dc] = '_'
                    dfs(nr, nc, visited)

        dfs(0, 0, set())  # start DFS from top-left corner
        board[0][0] = 'S' # start
        board[N-1][N-1] = 'E' # exit
        # Force-connect exit if DFS missed it (important for even N)
        if board[N-2][N-1] == 'X' and board[N-1][N-2] == 'X':
            # carve either up or left to ensure exit reachable
            if random.choice([True, False]):
                board[N-2][N-1] = '_'
            else:
                board[N-1][N-2] = '_'
        elif board[N-2][N-1] == 'X':
            board[N-2][N-1] = '_'
        elif board[N-1][N-2] == 'X':
            board[N-1][N-2] = '_'
        return board

    def __moveDown(self):
        """
        Move the player down by one cell if possible.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        board = self.__board
        row, col = self.__player_pos
        if row +1 < self.__N and board[row+1][col] in ['_', 'E']:
            self.__player_pos = (row + 1, col)
            return True
        return False  
    
    def __moveUp(self):
        """
        Move the player up by one cell if possible.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        board = self.__board
        row, col = self.__player_pos
        if row - 1 >= 0 and board[row - 1][col] in ['_', 'E']:
            self.__player_pos = (row - 1, col)
            return True
        return False  
    
    def __moveRight(self):
        """
        Move the player right by one cell if possible.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        board = self.__board
        row, col = self.__player_pos
        if col + 1 < self.__N and board[row][col + 1] in ['_', 'E']:
            self.__player_pos = (row, col + 1)
            return True
        return False 
     
    def __moveLeft(self):
        """
        Move the player left by one cell if possible.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        board = self.__board
        row, col = self.__player_pos
        if col - 1 >= 0 and board[row][col - 1] in ['_', 'E']:
            self.__player_pos = (row, col - 1)
            return True
        return False 
     
    def isWinner(self):
        """
        Check if the player has reached the exit.

        Returns:
            bool: True if player reached exit, False otherwise.
        """
        return self.__player_pos == (self.__N - 1, self.__N -1)
        
    def solveMaze(self):
        """
        Main game loop: displays the maze, accepts user input for movement, and tracks time.
        """
        Maze.showCommands()
        self.dispBoard()
        start_time = time.time()  # Start timer
        while True:
            user_pick = input(Style.BRIGHT+'Enter your move (w/s/a/d): '+Style.RESET_ALL).strip().lower()
            if user_pick not in self.__moves.keys():
                print(Fore.YELLOW+'Follow the instructions.'+Style.RESET_ALL)
                continue
            if not self.__moves[user_pick]():
                print(Fore.LIGHTRED_EX+'Invalid Move! The way is blocked.'+Style.RESET_ALL)
                continue
            os.system('cls' if os.name == 'nt' else 'clear')
            if self.isWinner():
                self.dispBoard()
                end_time = time.time()  # Stop timer
                total_time = end_time - start_time
                print(Fore.GREEN+f'You solved the maze! Total time taken: {total_time:.2f} seconds.')
                break
            Maze.showCommands()
            self.dispBoard() 
             
    def get_player_pos(self):
        """Return the current player position (row, col)."""
        return self.__player_pos
    
    def get_board(self):
        """Return a copy of the maze board."""
        # Return a deep copy to prevent external modifications
        return [row[:] for row in self.__board]

    @staticmethod
    def showCommands():
        """Display movement commands for the user."""
        print('Commands are as follows :\n')
        print(f"{Fore.CYAN}'W' or 'w'{Style.RESET_ALL} : {Fore.YELLOW}Move Up{Style.RESET_ALL}")
        print(f"{Fore.CYAN}'S' or 's'{Style.RESET_ALL} : {Fore.YELLOW}Move Down{Style.RESET_ALL}")
        print(f"{Fore.CYAN}'A' or 'a'{Style.RESET_ALL} : {Fore.YELLOW}Move Left{Style.RESET_ALL}")
        print(f"{Fore.CYAN}'D' or 'd'{Style.RESET_ALL} : {Fore.YELLOW}Move Right{Style.RESET_ALL}\n")      
        
## Main Program 
if __name__ =='__main__':
    print(Fore.MAGENTA + "This Maze Game was coded by Husnain Maroof.\n" + Style.RESET_ALL)
    print(Fore.CYAN+'1.'+Style.RESET_ALL+' Beginner (5x5) Maze')
    print(Fore.CYAN+'2.'+Style.RESET_ALL+' Medium (8x8) Maze')
    print(Fore.CYAN+'3.'+Style.RESET_ALL+' Advanced (10x10) Maze\n')
    while True:
        choice = input(Fore.YELLOW+'Choose Difficulty Level: '+Style.RESET_ALL).strip()
        if choice not in ['1', '2', '3']:
            print(Fore.LIGHTRED_EX+'Invalid choice!'+Style.RESET_ALL)
            continue
        if choice == '1':
            N = 5
            break
        elif choice == '2':
            N = 8
            break
        else:
            N = 10
            break
    os.system('cls' if os.name == 'nt' else 'clear')   
    maze = Maze(N)  
    maze.solveMaze()
    


    