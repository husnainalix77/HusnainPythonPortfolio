from player import Player
from mill_logic import Mill_Logic
import random

class AIPlayer(Player):
    """Represents an AI-controlled player with Minimax-based decision making."""
    
    def __init__(self, player_num):
        """Initialize AI player with given player number."""
        super().__init__(player_num)
        
    def get_pos(self, board_obj):
        """Return a random empty position for placement (Phase 1)."""
        return random.choice(self.get_all_empty_positions(board_obj))
    
    def get_capturable_opp_positions(self, board_obj, opp_symbol):
        """Return opponent pieces position that can legally be captured."""
        capturable = []
        for p in range(1, 25):
            if board_obj.board[p - 1] != opp_symbol:
                continue 
            in_mill = False
            for mill in Mill_Logic.MILLS:
                if (p - 1) in mill and all(board_obj.board[m] == opp_symbol for m in mill):
                    in_mill = True
            if not in_mill:
                capturable.append(p) 
        return capturable               
                    
 
    def get_best_capture_pos(self, board_obj, opp_symbol):
        """Return the best opponent piece to capture to maximize impact."""
        capturable_pos = self.get_capturable_opp_positions(board_obj, opp_symbol)
        best_pos = capturable_pos[0] # Fall back value
        best_score = -1
        
        for pos in capturable_pos:
            score_pos = 0
            for mill in Mill_Logic.MILLS:
                if (pos - 1) in mill:
                    score_pos += sum(1 for m in mill if board_obj.board[m] == opp_symbol)
                    # Pieces that are part of more filled mills get a higher score — capturing them is more impactful.
            if score_pos > best_score:
                best_score = score_pos
                best_pos = pos        
        return best_pos  
    
    def capture_opp_piece(self, board_obj, opp_symbol):
        """Select and return a position of opponent piece to capture."""
        all_milled = Mill_Logic.all_inside_mill(board_obj, opp_symbol)
        if all_milled:
            all_opp_pos = [p for p in range(1, 25) if board_obj.board[p - 1] == opp_symbol]
            return random.choice(all_opp_pos)
        
        return self.get_best_capture_pos(board_obj, opp_symbol)
    
    # --------------Minimax Algorithm Implementation-----------------------
    
    def get_all_empty_positions(self, board_obj):
        """Return all empty positions on the board."""
        all_empty_pos = [p for p in range(1, 25) if board_obj.board[p - 1] in list(range(1, 25))]
        return all_empty_pos
    
    def get_all_adjacent_moves(self, board_obj, player_symbol):
        """Return all valid adjacent moves for a player (Phase 2)."""
        adjacent_moves = []
        all_empty_pos = self.get_all_empty_positions(board_obj)
        for start_pos in range(1, 25):
            if board_obj.board[start_pos - 1] == player_symbol:
                for end_pos in all_empty_pos:
                    if (end_pos - 1) in Mill_Logic.ADJENCIES[start_pos - 1]:
                        adjacent_moves.append((start_pos, end_pos))
        return adjacent_moves   
    
    def get_all_flying_moves(self, board_obj, player_symbol):
        """Return all valid moves when player can fly (Phase 3)."""
        start_positions = [s for s in range(1, 25) if board_obj.board[s - 1] == player_symbol]
        all_empty_pos = self.get_all_empty_positions(board_obj)
        return [(s, e) for s in start_positions for e in all_empty_pos]
    
    def count_mills(self, board_obj, symbol):
        """Count the number of completed mills for a player symbol."""
        return sum(1 for mill in Mill_Logic.MILLS if all(board_obj.board[m] == symbol for m in mill))
    
    def count_potential_mills(self, board_obj, symbol):
        """Count potential mills (two pieces in line with one empty)."""
        count_potential_mills = 0

        for mill in Mill_Logic.MILLS:
            pieces = sum(1 for m in mill if board_obj.board[m] == symbol ) # player_pieces
            empty = sum(1 for m in mill if board_obj.board[m] not in ["W", "B"]) # empty
            if pieces == 2 and empty == 1:
                count_potential_mills += 1
        return count_potential_mills    
        
    def count_blocked_pieces(self, board_obj, symbol):
        """Count player pieces that cannot move (blocked). No movement to adjacent position."""
        total = 0
        for p in range(1, 25):
            if board_obj.board[p - 1] != symbol:
                continue
            is_blocked = True
            for adj in Mill_Logic.ADJENCIES[p - 1]:
                if board_obj.board[adj] not in ["W", "B"]:
                    is_blocked = False
            if is_blocked:
                total += 1   
        return total             
            
    
    def count_double_mills(self, board_obj, symbol):
        """Count player pieces that are part of two potential mills simultaneously."""
        player_pieces_pos = [p for p in range(1, 25) if board_obj.board[p - 1] == symbol] 
        double_mill_count = 0
        for pos in player_pieces_pos:
            count = 0
            for mill in Mill_Logic.MILLS:
                score_pos = 0
                empty = 0
                if (pos - 1) in mill:
                    score_pos += sum(1 for m in mill if board_obj.board[m] == symbol)
                    empty += sum(1 for m in mill if board_obj.board[m] not in ["W", "B"])
                if score_pos == 2 and empty == 1:
                    count += 1
            if count >= 2:
                double_mill_count += 1
        return double_mill_count   
    
    def count_threatened_pieces(self, board_obj, symbol, opp_symbol):
        """Count player pieces that are threatened by opponent forming mills."""
        threatened = 0
        for p in range(1, 25):
            if board_obj.board[p - 1] == symbol:
                for mill in Mill_Logic.MILLS:
                    if (p - 1) in mill:
                        opp_count = sum(1 for m in mill if board_obj.board[m] == opp_symbol)
                        if opp_count == 2:
                            threatened += 1
                            break
        return threatened             

    def evaluate_board(self, board_obj):
        """Compute a heuristic score for the board from AI perspective."""
        
        # Piece Count Difference (very important)
        ai_pieces = sum(1 for p in range(1, 25) if board_obj.board[p - 1] == "B")
        human_pieces = sum(1 for p in range(1, 25) if board_obj.board[p - 1] == "W")
        piece_score = ai_pieces - human_pieces
        
        # Complete Mills Count
        ai_mills = self.count_mills(board_obj, "B")
        human_mills = self.count_mills(board_obj, "W")
        mill_score = ai_mills - human_mills
        
        # Potential Mills (2 pieces aligned with 1 empty)
        ai_potential_mills = self.count_potential_mills(board_obj, "B")
        human_potential_mills = self.count_potential_mills(board_obj, "W")
        potential_score = ai_potential_mills - human_potential_mills
        
        # Double Mills
        ai_double_mills = self.count_double_mills(board_obj, "B")
        human_double_mills = self.count_double_mills(board_obj, "W")
        double_mill_score = ai_double_mills - human_double_mills
        
        # Mobility (Number of adjacent valid moves)
        
        ai_mobility = len(self.get_all_adjacent_moves(board_obj, "B"))
        human_mobility = len(self.get_all_adjacent_moves(board_obj, "W"))
        mobility_score = ai_mobility - human_mobility
        
        #  Blocked Opponent Pieces
        ai_blocked_pieces = self.count_blocked_pieces(board_obj, "B")
        human_blocked_pieces = self.count_blocked_pieces(board_obj, "W")
        blocked_score = ai_blocked_pieces - human_blocked_pieces
        
        # Threatened Pieces
        ai_threatened = self.count_threatened_pieces(board_obj, "B", "W")
        human_threatened = self.count_threatened_pieces(board_obj, "W", "B")
        threatened_score = human_threatened - ai_threatened
        
        # Valuable Positions
        POSITION_VALUES = [3,2,3,2,3,2,3,2,3,2,4,2,2,4,2,3,2,3,2,3,2,3,2,3]

        pos_score = sum(POSITION_VALUES[p] for p in range(24) if board_obj.board[p] == "B") - \
            sum(POSITION_VALUES[p] for p in range(24) if board_obj.board[p] == "W")
        
        # Endgame adjustments for opponent or AI flying
        human_pieces_count = sum(1 for p in range(24) if board_obj.board[p] == "W")
        ai_pieces_count    = sum(1 for p in range(24) if board_obj.board[p] == "B")

        if human_pieces_count == 3:  # opponent flying
            mill_score *= 2
            potential_score *= 2
            mobility_score = 0

        if ai_pieces_count == 3:  # AI flying
            mill_score *= 2
            potential_score *= 2
            mobility_score = 0
            blocked_score *= 2  # emphasize blocking opponent moves   

        return (piece_score * 15) + (mill_score * 15) + (potential_score * 7) + (mobility_score * 3) + \
       (blocked_score * 2) + (pos_score * 1) + (double_mill_score * 8) + (threatened_score * 4)
    
    def simulate_move(self, board_obj, pos, player_num):
        """Simulate placing a piece at a position and return old board state."""
        old_state = board_obj.get_board_state()
        board_obj.fill_position(pos, player_num) # change current board state
        return old_state  # just return old state so we can restore later
    
    def simulate_move_phase_2_3(self, board_obj, start_pos, end_pos, player_num):
        """Simulate moving a piece (Phase 2/3) and return old board state."""
        old_state = board_obj.get_board_state()
        board_obj.board[start_pos - 1] = start_pos  # clear start
        board_obj.fill_position(end_pos, player_num)  # fill end
        return old_state # just return old state so we can restore later
    
    def get_adaptive_depth(self, board_obj):
        """Return search depth based on board size and remaining empty slots."""
        empty_pos = sum(1 for pos in range(1, 25) if board_obj.board[pos - 1] in list(range(1,25)))
        if empty_pos >= 20: return 4
        if empty_pos >= 15: return 5
        if empty_pos >= 10: return 6
        return 7

    def minimax(self, board_obj, depth, is_maximizing, alpha, beta, phase, pieces_placed):
        """Full Implementation of Minimax Algorithm which gives Best Move."""
        if depth == 0: # Base Case
            return self.evaluate_board(board_obj)

        player_symbol  = "B" if is_maximizing else "W"
           
        if phase == 1: # Phase 1
            empty_pos = self.get_all_empty_positions(board_obj)
            
        # Phase 1
        if phase == 1:
            if is_maximizing: # AI
                best = float("-inf")
                for pos in empty_pos:
                    old_state = self.simulate_move(board_obj, pos, 2)
                    next_phase = 1 if pieces_placed + 1 < 18 else 2 # To keep track of phase
                    eval = self.minimax(board_obj, depth - 1, False, alpha, beta, next_phase, pieces_placed + 1)
                    board_obj.set_board_state(old_state)
                    best = max(best, eval)
                    alpha = max(alpha, best)
                    if beta <= alpha: # Beta Pruning
                        break
                return best    
            
            else: # Human
                best = float("+inf")
                for pos in empty_pos:
                    old_state = self.simulate_move(board_obj, pos, 1)
                    next_phase = 1 if pieces_placed + 1 < 18 else 2 # To keep track of phase
                    eval = self.minimax(board_obj, depth - 1, True, alpha, beta, next_phase, pieces_placed + 1)
                    board_obj.set_board_state(old_state)
                    best = min(best, eval)
                    beta = min(beta, best)
                    if beta <= alpha: # Alpha Pruning
                        break
                return best  
        
        # Phase 2/3
        else:
            if is_maximizing: # AI
                current_pieces = self.pieces_on_board
            else: # Human
                current_pieces = sum(1 for p in range(24) if board_obj.board[p] == "W")
                
            if current_pieces > 3:  # Phase 2
                moves = self.get_all_adjacent_moves(board_obj, player_symbol)
            else:  # Phase 3
                moves = self.get_all_flying_moves(board_obj, player_symbol)
            
            if is_maximizing: # AI
                best = float("-inf")
                for start_pos, end_pos in moves:
                    old_state = self.simulate_move_phase_2_3(board_obj, start_pos, end_pos, 2)
                    eval = self.minimax(board_obj, depth - 1, False, alpha, beta, 2, pieces_placed)
                    board_obj.set_board_state(old_state)
                    best = max(best, eval)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
                return best
            
            else: # Human
                best = float("+inf")
                for start_pos, end_pos in moves:
                    old_state = self.simulate_move_phase_2_3(board_obj, start_pos, end_pos, 1)
                    eval = self.minimax(board_obj, depth - 1, True, alpha, beta, 2, pieces_placed)
                    board_obj.set_board_state(old_state)
                    best = min(best, eval)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
                return best

    def get_best_pos(self, board_obj, player_num, pieces_placed):
        """Return best position for AI for phase 1."""
        depth = self.get_adaptive_depth(board_obj)
        best_score = float('-inf')
        best_pos = None
        alpha = float('-inf') # Lower bound
        beta = float('inf') # Higher bound
        all_valid_pos = self.get_all_empty_positions(board_obj)
        if not all_valid_pos: # Safety Check
            return None
        best_pos = random.choice(all_valid_pos) # random fallback (in the start, all positions are empty, we will get -inf)
        
        for pos in all_valid_pos:
            old_state = self.simulate_move(board_obj, pos, player_num)

            if Mill_Logic.can_form_mill("B", board_obj, pos):
                board_obj.set_board_state(old_state)
                print("AI is making a mill.")
                return pos
            board_obj.set_board_state(old_state)
            
        for pos in all_valid_pos:
            old_state = self.simulate_move(board_obj, pos, 1)

            if Mill_Logic.can_form_mill("W", board_obj, pos):
                board_obj.set_board_state(old_state)
                print("AI is blocking mill formation.")
                return pos   
            board_obj.set_board_state(old_state)
            
        # Choose best position
        for pos in all_valid_pos:
            old_state = self.simulate_move(board_obj, pos, player_num)
            score = self.minimax(board_obj, depth-1, False, alpha, beta, 1, pieces_placed)
            board_obj.set_board_state(old_state)

            if score > best_score:
                best_score = score
                best_pos = pos
            alpha = max(alpha, best_score)    
        return best_pos   
    
    def get_best_pos_2_3(self, board_obj, player_num, pieces_placed):
        """Return best start and end positions for AI for phase 2/3."""
        depth = self.get_adaptive_depth(board_obj)
        best_score = float('-inf')
        best_start_pos = None
        best_end_pos = None
        alpha = float('-inf')
        beta = float('inf')
        
        if self.pieces_on_board > 3: # Phase 2
            ai_moves = self.get_all_adjacent_moves(board_obj, self.symbol)
            phase = 2
        else: # Phase 3
            ai_moves = self.get_all_flying_moves(board_obj, self.symbol)
            phase = 2 # Minimax already handles Phase 3 internally
        
        if not ai_moves: # Safety Check
            return None, None
        best_start_pos, best_end_pos = random.choice(ai_moves) # Fall back value
        
        
        # AI win Check
        for start_pos, end_pos in ai_moves:
            old_state = self.simulate_move_phase_2_3(board_obj, start_pos, end_pos, player_num)
            if Mill_Logic.has_two_pieces(2, board_obj) or not Mill_Logic.has_valid_moves(board_obj, "W"):
                board_obj.set_board_state(old_state)
                print("AI found a winning move.")
                return start_pos, end_pos
            board_obj.set_board_state(old_state)
            
        # Choose Best Start and End Position
        for start_pos, end_pos in ai_moves:
            old_state = self.simulate_move_phase_2_3(board_obj, start_pos, end_pos, player_num)
            score = self.minimax(board_obj, depth - 1, False, alpha, beta, phase, pieces_placed) # Human Turn
            board_obj.set_board_state(old_state)
            
            if score > best_score:
                best_score = score
                best_start_pos = start_pos
                best_end_pos = end_pos
            alpha = max(alpha, best_score)    
        return best_start_pos, best_end_pos
                
