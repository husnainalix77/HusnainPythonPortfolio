# Nine Men's Morris Game - Enhanced UI Version
class Board:
    """Represents the Nine Men's Morris board with display and piece management."""
    PLAYERS = ["W", "B"]
    
    # ANSI Color Codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    WHITE_PIECE = "\033[1;31m"  # Bold Red for 'W'
    BLACK_PIECE = "\033[1;36m"  # Bold Cyan for 'B'
    BOARD_LINE = "\033[90m"     # Dark Grey for lines
    EMPTY_POS = "\033[0;37m"    # Dim white for numbers
    LINE_COLOR = "\033[38;5;67m" # Elegant blue

    def __init__(self):
        """Initialize the board with positions 1 to 24."""
        self.board = list(range(1, 25))
        
    def _get_colored_symbol(self, pos_val):
        """Return the board symbol with proper color formatting."""
        if pos_val == "W":
            return f"{self.WHITE_PIECE} W{self.RESET}"   # always 2-width
        elif pos_val == "B":
            return f"{self.BLACK_PIECE} B{self.RESET}"   # always 2-width
        else:
            return f"{self.EMPTY_POS}{pos_val:2}{self.RESET}"  # always 2-width
        
    def show_title(self):
        """Display the game title with decorative lines."""
        print(f"{self.BOLD}{self.LINE_COLOR}")
        print("     ╔══════════════════════════════════════╗")
        print("     ║        NINE MEN'S MORRIS GAME        ║")
        print("     ╚══════════════════════════════════════╝")
        print(self.RESET)    
        
    def disp_board(self):
        """Display the current state of the board with colors and lines."""
        self.show_title()
        b = [self._get_colored_symbol(x) for x in self.board]
        line = self.BOARD_LINE
        res = self.RESET
        
        print(f"{b[0]} {line}————————————————————— {res}{b[1]} {line}———————————————————{res}{b[2]}")
        print(f"{line}|                        |                      |{res}")
        print(f"{line}|       {res}{b[3]} {line}————————————— {res}{b[4]} {line}—————————————{res}{b[5]} {line}    |{res}")
        print(f"{line}|       |                |              |       |{res}")
        print(f"{line}|       |       {res}{b[6]} {line}—————{res}{b[7]} {line}————— {res}{b[8]} {line}    |       |")
        print(f"{line}|       |       |               |       |       |{res}")
        print(f"{res}{b[9]} {line}———— {res}{b[10]} {line}———— {res}{b[11]} {line}             {res}{b[12]} {line}———— {res}{b[13]} {line}———— {res}{b[14]}")
        print(f"{line}|       |       |               |       |       |{res}")
        print(f"{line}|       |       {res}{b[15]} {line}————— {res}{b[16]} {line}————— {res}{b[17]} {line}   |       |{res}")
        print(f"{line}|       |               |               |       |{res}")
        print(f"{line}|       {res}{b[18]} {line}————————————— {res}{b[19]} {line}————————————— {res}{b[20]} {line}   |")
        print(f"{line}|                       |                       |{res}")
        print(f"{b[21]} {line}————————————————————— {res}{b[22]} {line}—————————————————— {res}{b[23]}\n")

    def is_position_empty(self, pos_num):
        """Check if a board position is empty."""
        return self.board[pos_num - 1] not in Board.PLAYERS
    
    def fill_position(self, pos_num, player_num):
        """Place a player's symbol at the specified position."""
        self.board[pos_num - 1] = Board.PLAYERS[player_num - 1] 
    
    def get_board_state(self):
        """Return a copy of the current board state."""
        return self.board.copy()

    def set_board_state(self, state):
        """Set the board to a given state."""
        self.board = state.copy()