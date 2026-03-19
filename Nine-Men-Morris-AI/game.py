# Nine Men's Morris Game
# Developed by Husnain Maroof
# Version: 1.0 | March 13–19, 2026
# Purpose: Console-based implementation with enhanced UI and game logic

from board import Board
from player import Player
from mill_logic import Mill_Logic
from ai_player import AIPlayer
import random
import os, time

class Game:
    """
    Main class to run the Nine Men's Morris game.
    Handles game phases, turns, player input, AI moves, and game flow.
    """
    def __init__(self):
        """
        Initialize the game with board and players.
        Sets up Player 1 (human) and Player 2 (AI).
        """
        self.board_obj = Board() # Board class object
        self.player1   = Player(1) # Player class object 
        self.player2   = AIPlayer(2) # AI Player class object 
        self.current_player = None
        self.stale_moves = 0 
        self.board_history = []
    
    @staticmethod
    def turn_decide():
        """
        Ask the user who should go first.
        Returns:
            int: Player number who goes first (1 or 2)
        """
        while True:
            print("\nWhose goes first?")
            print("1. Player 1")
            print("2. Player 2")
            print("3. Random")
            try:
                choice = int(input("> "))
            except ValueError:
                print("Enter integer value only.")
                continue
                
            if choice not in [1, 2, 3]:
                print("Invalid Entry!")
                continue
            if choice == 3:
                return random.randint(1, 2)

            return choice  
        
    def switch_turn(self):
        """
        Switch the current player to the other player.
        """
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        
    @staticmethod
    def valid_entry(pos):
        """
        Check if a board position entry is valid.
        Args:
            pos (int): The position to check.
        Returns:
            bool: True if valid (1-24), False otherwise.
        """
        if pos not in range(1, 25):
                print("Invalid Entry!")
                return False
        return True    
        
    def phase_1(self):
        """
        Handles Phase 1 of the game (placing pieces on the board).
        - Player and AI take turns placing pieces.
        - Checks for mill formation and captures.
        - Ends when both players have placed all 9 pieces.
        """
        while True:
            if self.current_player.player_num == 1:
                pos_num = self.current_player.get_input()
                if not self.board_obj.is_position_empty(pos_num):
                    print(f"Position {pos_num} is already occupied. Choose other one.")
                    continue
            else: # AI
                pieces_placed = self.player1.pieces_placed + self.player2.pieces_placed
                pos_num = self.current_player.get_best_pos(self.board_obj, 2, pieces_placed) # AI Turn
                print(f"AI has chosen position {pos_num}.")    
            self.board_obj.fill_position(pos_num, self.current_player.player_num)
            self.current_player.increment_placed() # incrementing pieces for current player on board after valid move
            time.sleep(0.4)
            os.system('cls')
            self.board_obj.disp_board()

            mills_count = Mill_Logic.can_form_mill(self.current_player.symbol, self.board_obj, pos_num) # mills formation check
            if mills_count: # if at least one mill is formed
                if mills_count == 1:
                    print(f"Player {self.current_player.player_num} has formed {mills_count} mill.")
                else:
                    print(f"Player {self.current_player.player_num} has formed {mills_count} mills.")
        
                opp_symbol = self.player2.symbol if self.current_player == self.player1 else self.player1.symbol
                opp_player = self.player2 if self.current_player == self.player1 else self.player1
                
                if self.current_player == self.player2: # AI
                    pos = self.current_player.capture_opp_piece(self.board_obj, opp_symbol)
                    print(f"AI Captures your piece at position {pos}.")
                    self.board_obj.board[pos - 1] = pos
                    opp_player.decrement_pieces() # Decrement opposite player pieces
                    
                else:
                    
                    Mill_Logic.can_capture_piece(self.board_obj, opp_symbol) # capturing opponent piece
                    opp_player.decrement_pieces()  # decrement opponent piece after capture
                
                self.stale_moves = 0    
                    
                time.sleep(0.3)
                os.system('cls')
                self.board_obj.disp_board()
                
                # In Phase 1 you can only win after a capture
                if Mill_Logic.has_two_pieces(self.current_player.player_num, self.board_obj):
                    print(f"Player {self.current_player.player_num} has WON.")
            
                    exit()
                    
            else: # No mill - no capture
                self.stale_moves += 1    
            
            # Add current state to history
            self.board_history.append(tuple(self.board_obj.board))  
                     
            self.switch_turn() # switch turn 
            
            # Check threefold repetition
            if self.board_history.count(tuple(self.board_obj.board)) >= 3:
                print("Draw — same position repeated 3 times.")
                exit() 
                 
            if self.stale_moves >= 50:
                print("Draw — 50 moves without a mill or capture.")
                exit()
            if self.player1.pieces_placed == 9 and self.player2.pieces_placed == 9: # phase 1 ends when both players have 9 pieces on board
                print("Time to move to phase 2.")
                break 
    
    def phase_2_3(self):
        """
        Handles Phase 2 (moving pieces) and Phase 3 (flying pieces if 3 remaining).
        - Players can move pieces to adjacent empty positions (or any empty for flying).
        - Checks for mill formation, captures, and win conditions.
        - Loops until game ends.
        """
        while True:
            if self.current_player == self.player1: # Human
                if self.current_player.pieces_on_board == 3:
                    print("You have entered flying mode! You can move to any empty position.")
                try:
                    start_pos = int(input(f"Player {self.current_player.player_num}, enter position of piece to move: "))
                except ValueError:
                    print("Enter Integer Value only.")
                    continue
                
                if not Game.valid_entry(start_pos):    
                    continue
                
                if self.board_obj.board[start_pos - 1] != self.current_player.symbol:
                    print("Position must contain your piece.")
                    continue

                try:
                    end_pos = int(input(f"Player {self.current_player.player_num}, enter position to move to: "))
                except ValueError:
                    print("Enter Integer Value only.")
                    continue
                
                if not Game.valid_entry(end_pos):    
                    continue

                if not self.board_obj.is_position_empty(end_pos):
                    print("Position must be empty.")
                    continue
                
                # If current player has more than 3 pieces — they are in Phase 2, so adjacency check is enforced.    
                if self.current_player.pieces_on_board > 3:
                    if not Mill_Logic.is_adjacent_to(start_pos, end_pos):
                        print(f"Position must be adjacent to {start_pos}. Try again.")
                        continue
                    
            else: # AI
                pieces_placed = self.player1.pieces_placed + self.player2.pieces_placed
                if self.current_player.pieces_on_board == 3:
                    print("AI has entered flying mode!")
                start_pos, end_pos = self.current_player.get_best_pos_2_3(self.board_obj, 2, pieces_placed)
                print(f"AI moved from {start_pos} to {end_pos}.") 
                time.sleep(0.4)      
            # If current player has exactly 3 pieces — they are in Phase 3 (flying), so the entire
            # if block is skipped and they can move to any empty position without adjacency restriction.            
            self.board_obj.board[start_pos - 1] = start_pos # Clear position
            self.board_obj.fill_position(end_pos, self.current_player.player_num)
            os.system('cls')
            self.board_obj.disp_board()

            mills_count = Mill_Logic.can_form_mill(self.current_player.symbol, self.board_obj, end_pos)
            if mills_count:
                print(f"Player {self.current_player.player_num} has formed {mills_count} mill(s).")
                opp_symbol = self.player2.symbol if self.current_player == self.player1 else self.player1.symbol
                opp_player = self.player2 if self.current_player == self.player1 else self.player1
                if self.current_player == self.player2:  # AI captures
                    pos = self.current_player.capture_opp_piece(self.board_obj, opp_symbol)
                    print(f"AI captures your piece at position {pos}.")
                    self.board_obj.board[pos - 1] = pos
                else:  # Human captures
                    Mill_Logic.can_capture_piece(self.board_obj, opp_symbol)
                self.stale_moves = 0    
                opp_player.decrement_pieces()
            
            else: # No mill - no capture
                self.stale_moves += 1    
                    
            os.system('cls')
            self.board_obj.disp_board()
            
            # Add current state to history
            self.board_history.append(tuple(self.board_obj.board))
            
            # Check threefold repetition
            if self.board_history.count(tuple(self.board_obj.board)) >= 3:
                print("Draw — same position repeated 3 times.")
                exit()       
                     
            if self.stale_moves >= 50:
                print("Draw — 50 moves without a mill or capture.")
                exit()
            # Opponent has <= 2 pieces → current player wins
            # Opponent has > 3 pieces but no valid moves → current player wins
            # Opponent has exactly 3 pieces → they can fly anywhere so no valid moves check applies — game continues
            opp_player = self.player2 if self.current_player == self.player1 else self.player1
            if Mill_Logic.has_two_pieces(self.current_player.player_num, self.board_obj) or \
            (opp_player.pieces_on_board > 3 and not Mill_Logic.has_valid_moves(self.board_obj, opp_player.symbol)):
                print(f"Player {self.current_player.player_num} has WON.")
                break

            self.switch_turn()  
            
    def run(self):
        """
        Run the game:
        - Decide starting player.
        - Execute Phase 1 and Phase 2/3 in order.
        """
        choice = self.turn_decide()
        print(f"Player {choice} goes first.")
        self.current_player = self.player1 if choice == 1 else self.player2
        self.phase_1()
        self.phase_2_3()

## Main Program
if __name__ =="__main__":  
    game = Game()
    game.run()                          
                