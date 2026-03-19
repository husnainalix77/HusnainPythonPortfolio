from board import Board

class Player:
    """Represents a player in Nine Men's Morris game."""
    
    def __init__(self, player_num):
        """Initialize a player with number, symbol, and piece counts."""
        self.player_num = player_num
        self.symbol = Board.PLAYERS[player_num - 1]
        self.pieces_placed = 0    # tracks Phase 1 placements
        self.pieces_on_board = 9  # tracks current pieces during Phase 2/3
    
    def get_input(self):
        """Prompt player to enter a valid empty board position (1-24)."""
        while True:
            try:
                pos_num = int(input(f"Player {self.player_num}, enter an empty position (1-24): "))
            except ValueError:
                print("Enter integer value only.")
                continue  
            if pos_num not in list(range(1, 25)):
                print("The position must be between 1 and 24. Try again")
                continue 
            return pos_num
    
    def increment_placed(self):
        """Increase the count of pieces placed by the player."""
        self.pieces_placed += 1
    
    def decrement_pieces(self):
        """Decrease the count of player's pieces on the board."""
        self.pieces_on_board -= 1            
    