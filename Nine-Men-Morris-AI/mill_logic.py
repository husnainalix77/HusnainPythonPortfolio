from board import Board

class Mill_Logic:
    """Provides logic for mills, adjacency, and captures in Nine Men's Morris."""
    
    MILLS = [
             (0, 1, 2), (0, 9, 21), (1, 4, 7), (2, 14, 23),
             (3, 4, 5), (3, 10, 18), (5, 13, 20), (6, 7, 8),
             (6, 11, 15), (8, 12, 17), (9, 10, 11), (12, 13, 14),
             (15, 16, 17), (18, 19, 20), (16, 19, 22),(21, 22, 23)
            ] # All possible mill combinations on the board

    ADJENCIES = {
              0: [1, 9],
              1: [0, 2, 4],
              2: [1, 14],
              3: [4, 10],
              4: [1, 3, 5, 7],
              5: [4, 13],
              6: [7, 11],
              7: [4, 6, 8],
              8: [7, 12],
              9: [10, 21],
              10: [9, 11, 3, 18],
              11: [10, 6, 15],
              12: [8, 13, 17],
              13: [12, 5, 14, 20],
              14: [13, 2, 23],
              15: [11, 16], 
              16: [15, 17, 19], 
              17: [16, 12],
              18: [10, 19],
              19: [16, 18, 20, 22],
              20: [13, 19],
              21: [9, 22],
              22: [21, 19, 23],
              23: [22, 14]
} # Adjacency mapping for each board position
    
    @staticmethod
    def can_form_mill(symbol, board_obj, pos_num):
        """Check how many mills a symbol can form by placing at a position."""
        mills_count = 0
        
        for mill in Mill_Logic.MILLS:
            if (pos_num - 1) in mill:
                if all(board_obj.board[m] == symbol for m in mill):
                    mills_count += 1
                    
        return mills_count 
    
    @staticmethod
    def all_inside_mill(board_obj, opp_player_symbol):
        """Check if all opponent's pieces are inside mills."""
        all_pos = [p for p in range(24) if board_obj.board[p] == opp_player_symbol]
        
        for pos in all_pos:
            in_a_mill = False
            for mill in Mill_Logic.MILLS:
                if pos in mill and all(board_obj.board[m] == opp_player_symbol for m in mill):
                    in_a_mill = True
                    break
            if not in_a_mill:
                return False
            
        return True 
    
    @staticmethod
    def can_capture_piece(board_obj, opp_player_symbol):
        """Prompt player to capture an opponent's piece legally."""
        all_milled = Mill_Logic.all_inside_mill(board_obj, opp_player_symbol)
        
        while True:
            try:
                pos_num = int(input("Enter Position of Opponent Piece to Capture: "))
            except ValueError:
                print("Enter integer value only.")
                continue
            
            in_mill = any(
                (pos_num - 1) in mill and all(board_obj.board[m] == opp_player_symbol for m in mill) for mill in Mill_Logic.MILLS)
            
            if board_obj.board[pos_num - 1] == opp_player_symbol and (all_milled or not in_mill):
                
                board_obj.board[pos_num - 1] = pos_num
                print(f"Successfully, captured piece at poistion {pos_num}.")
                return True
            
            print("Invalid choice. Try again.")
            
    @staticmethod        
    def is_adjacent_to(start_pos, end_pos):
        """Check if two positions are adjacent on the board."""
        return (end_pos - 1) in Mill_Logic.ADJENCIES[start_pos - 1] # if end_pos in adjency of start_pos
    
    @staticmethod 
    def has_valid_moves(board_obj, opp_player_symbol):
        """Check if opponent has any valid moves available."""
        all_pos = [p for p in range(24) if board_obj.board[p] == opp_player_symbol]
        return any(board_obj.board[a] not in Board.PLAYERS for p in all_pos for a in Mill_Logic.ADJENCIES[p]) 
        # if any adjency of player_pos is empty
    
    @staticmethod
    def has_two_pieces(player_num, board_obj):
        """Check if the opponent has one or two pieces left."""
        opp_player = player_num % 2 + 1
        opp_pieces = sum(1 for p in range(24) if board_obj.board[p] == Board.PLAYERS[opp_player - 1])
        return 0 < opp_pieces <= 2
           
