# Mancala Game (Human vs AI) - Coded by Husnain Maroof - 7-12 March, 2026.
import random
import os
import time
import platform
from colorama import Fore, Style, init
init(autoreset=True)

class Board:
    P1_STORE = 6
    P2_STORE = 13
    P1_PITS  = list(range(0, 6))
    P2_PITS  = list(range(7, 13))
    
    def __init__(self) -> None:
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
    
    def __str__(self) -> str:

        top_row = " │ ".join(Fore.RED + f"{self.board[i]:2}" + Style.RESET_ALL for i in Board.P2_PITS[::-1])
        bottom_row = " │ ".join(Fore.GREEN + f"{self.board[i]:2}" + Style.RESET_ALL for i in Board.P1_PITS)

        board_str = f"""
                    AI
        ┌────┬────┬────┬────┬────┬────┐
        │ {top_row} │
┌───────┘                              └───────┐
│  {self.board[Board.P2_STORE]:2}                                      {self.board[Board.P1_STORE]:2} │
└───────┐                              ┌───────┘
        │ {bottom_row} │
        └────┴────┴────┴────┴────┴────┘
                  Husnain
"""
        return board_str
    
    def get_state(self) -> list:
        return self.board.copy()

    def set_state(self, state: list) -> None:
        self.board = state.copy()
        
    @property
    def p1_score(self) -> int:
        return self.board[Board.P1_STORE]

    @property
    def p2_score(self) -> int:
        return self.board[Board.P2_STORE]    
    
    def get_pit(self, index: int) -> int:
        return self.board[index]
    
    def set_pit(self, index: int, value: int) -> None:
        self.board[index] = value  
    
    def is_pit_empty(self, index: int) -> bool:
        return self.board[index] == 0    
    
    def get_opposite_pit(self, index: int) -> int:
        return 12 - index  

    def is_side_empty(self) -> int | bool:
        if not any(self.board[p] for p in Board.P1_PITS):
            return 1 
        if not any(self.board[p] for p in Board.P2_PITS):
            return 2
        return False       
    
    def sweep_remaining(self, player_num: int) -> None:
        if player_num == 1:
            pits  = Board.P1_PITS
            store = Board.P1_STORE
        else:
            pits  = Board.P2_PITS
            store = Board.P2_STORE
        for i in pits:
            self.board[store] += self.board[i]
            self.board[i] = 0    
             
    def fill_pit(self, player_num: int, pit_num: int) -> int | None:
        if player_num == 1:
            current = pit_num
        else:
            current = pit_num + 7
        pit_value = self.get_pit(current)
        if pit_value == 0:
            print("Choose another pit!")
            return
        self.set_pit(current, 0)
        for _ in range(pit_value):
            current += 1
            if current == len(self.board):
                current = 0
            elif player_num == 2 and current == Board.P1_STORE:
                current = Board.P2_PITS[0]
            elif player_num == 1 and current == Board.P2_STORE:
                current = Board.P1_PITS[0] 
            self.board[current] += 1   
        return current   
    
    def check_capture(self, current_pit: int, player_num: int) -> bool:
        store = Board.P1_STORE if player_num == 1 else Board.P2_STORE
        valid_pits = Board.P1_PITS if player_num == 1 else Board.P2_PITS
        if self.board[current_pit] == 1 and current_pit != store and current_pit in valid_pits:
            opp_pit = self.get_opposite_pit(current_pit)
            if self.board[opp_pit] == 0:
                return False
            self.board[store] += self.board[current_pit] + self.board[opp_pit]
            self.set_pit(current_pit, 0)
            self.set_pit(opp_pit, 0)
            return True   
        return False
        
    def is_winner(self) -> bool:
        if self.p1_score > self.p2_score:        
            print("Player 1 won the game.")
        elif self.p2_score > self.p1_score:
            print("Player 2 won the game.")
        else:
            print("Game is ended in draw.")
        return True    
                   
class Player:
    
    def __init__(self, name: str, player_num: int) -> None:
        self.name = name
        self.player_num = player_num
        if player_num == 1:
            self.pit_indices = Board.P1_PITS
            self.store_index = Board.P1_STORE
            self.opponent_store = Board.P2_STORE
        else:
            self.pit_indices = Board.P2_PITS
            self.store_index = Board.P2_STORE
            self.opponent_store = Board.P1_STORE 
            
    @staticmethod        
    def show_menu() -> int:
        print("Who goes first?")
        print("1. Player 1")
        print("2. Player 2")
        print("3. Random")
        op = int(input(">>"))
        while op not in [1, 2, 3]:
            print("Choose from 1, 2 or 3")
            op = int(input(">>"))
        if op == 1 or op == 2:
            print(f"Player {op} goes first.")
        else:
            op = random.randint(1, 2)
            print(f"Player {op} goes first.")
        print(Fore.CYAN + Style.BRIGHT + "Welcome to the Mancala Ancient Game.")
        print("Please wait....")
        time.sleep(0.8) 
        os.system('cls')  
        return op
    
    def __repr__(self) -> str:
        return f"Player({self.name}, num={self.player_num})"  
            
                     
class AIPlayer(Player):
    
    def __init__(self, name: str, player_num: int) -> None:
        super().__init__(name, player_num)
    
    def getAdaptiveDepth(self, board_obj) -> int:
        board_state = board_obj.get_state()
        total_stones = sum(board_state[p] for p in (Board.P1_PITS + Board.P2_PITS))
        if total_stones > 30:
            return 4
        elif total_stones > 15:
            return 6   
        else:
            return 7
        
    def get_valid_pits(self, board_obj, player_num: int) -> list:
        pits = Board.P1_PITS if player_num == 1 else Board.P2_PITS
        state = board_obj.get_state()
        return [p for p in pits if state[p] != 0]
    
    def simulate_move(self, board_obj, pit: int, player_num: int):
        saved = board_obj.get_state()
        if player_num == 1:
            pit_num = pit
        else:
            pit_num = pit - 7
        last = board_obj.fill_pit(player_num, pit_num)
        new_state = board_obj.get_state()
        board_obj.set_state(saved)
        return new_state, last   

    def _calculate_landing(self, pit: int, stones: int, player_num: int) -> int:
        current = pit
        for _ in range(stones):
            current += 1
            if current == 14:
                current = 0
            if player_num == 2 and current == Board.P1_STORE:
                current += 1
            if player_num == 1 and current == Board.P2_STORE:
                current = 0
        return current

    def evaluate_board(self, board_obj) -> float:
        empty_side = board_obj.is_side_empty()
        if empty_side:
            saved = board_obj.get_state()
            board_obj.sweep_remaining(2 if empty_side == 1 else 1)
            diff = board_obj.p2_score - board_obj.p1_score
            board_obj.set_state(saved)
            if diff > 0:  return 1000
            if diff < 0:  return -1000
            return 0

        score = board_obj.p2_score - board_obj.p1_score
        human_pits = self.get_valid_pits(board_obj, 1)
        ai_pits    = self.get_valid_pits(board_obj, 2) 
        
        for p in ai_pits:
            if board_obj.board[p] == Board.P2_STORE - p:
                score += 3
        for p in human_pits:
            if board_obj.board[p] == Board.P1_STORE - p:
                score -= 3  
        
        for p in ai_pits:
            stones  = board_obj.board[p]
            landing = self._calculate_landing(p, stones, 2)
            if board_obj.board[landing] == 0 and landing in Board.P2_PITS:
                opposite = board_obj.get_opposite_pit(landing)
                if board_obj.board[opposite] > 0:
                    score += board_obj.board[opposite]       
        
        for p in human_pits:
            stones  = board_obj.board[p]
            landing = self._calculate_landing(p, stones, 1)
            if board_obj.board[landing] == 0 and landing in Board.P1_PITS:
                opposite = board_obj.get_opposite_pit(landing)
                if board_obj.board[opposite] > 0:
                    score -= board_obj.board[opposite]
                    
        ai_stones    = sum(board_obj.board[p] for p in Board.P2_PITS)
        human_stones = sum(board_obj.board[p] for p in Board.P1_PITS)
        score += 0.1 * (ai_stones - human_stones)            
        return score            
        
    def minimax(self, board_obj, depth: int, is_maximizing: bool, 
                alpha: float, beta: float, ai_player_num: int) -> float:
        if depth == 0 or board_obj.is_side_empty():
            return self.evaluate_board(board_obj)
        current_player = ai_player_num if is_maximizing else 1
        valid_pits = self.get_valid_pits(board_obj, current_player)
        if not valid_pits:
            return self.evaluate_board(board_obj)

        if is_maximizing:
            best = float('-inf')
            for pit in valid_pits:
                saved = board_obj.get_state()
                new_state, last = self.simulate_move(board_obj, pit, current_player)
                board_obj.set_state(new_state)
                board_obj.check_capture(last, current_player)
                if last == Board.P2_STORE:
                    score = self.minimax(board_obj, depth - 1, True, alpha, beta, ai_player_num)
                else:
                    score = self.minimax(board_obj, depth - 1, False, alpha, beta, ai_player_num)
                board_obj.set_state(saved)
                best  = max(best, score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best

        else:
            best = float('inf')
            for pit in valid_pits:
                saved = board_obj.get_state()
                new_state, last = self.simulate_move(board_obj, pit, current_player)
                board_obj.set_state(new_state)
                board_obj.check_capture(last, current_player)
                if last == Board.P1_STORE:
                    score = self.minimax(board_obj, depth - 1, False, alpha, beta, ai_player_num)
                else:
                    score = self.minimax(board_obj, depth - 1, True, alpha, beta, ai_player_num)
                board_obj.set_state(saved)
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best
        
    def get_best_pit(self, board_obj, player_num: int) -> int | None:
        depth      = self.getAdaptiveDepth(board_obj)
        best_score = float('-inf')
        best_pit   = None
        alpha      = float('-inf')
        beta       = float('inf')
        
        all_valid_pits = self.get_valid_pits(board_obj, player_num)
        if not all_valid_pits:
            return None 

        for pit in all_valid_pits:
            new_state, last = self.simulate_move(board_obj, pit, player_num)
            saved = board_obj.get_state()
            board_obj.set_state(new_state)
            board_obj.check_capture(last, player_num)
            if last == Board.P2_STORE:
                score = self.minimax(board_obj, depth - 1, True, alpha, beta, player_num)
            else:
                score = self.minimax(board_obj, depth - 1, False, alpha, beta, player_num)
            board_obj.set_state(saved)
            if score > best_score:
                best_score = score
                best_pit   = pit
            alpha = max(alpha, best_score)    
        return best_pit
  
class Game:

    def __init__(self, player1: Player, player2: AIPlayer) -> None:
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player_num = None
        
    @staticmethod    
    def clear_screen() -> None:
        current_os = platform.system()
        time.sleep(0.5) 
        if current_os == 'Windows':
            os.system('cls')
        else:
            os.system('clear') 
        
    @staticmethod
    def valid_input(player_num: int) -> int:
        while True:
            try:
                pit_num = int(input(Fore.YELLOW+f"Player {player_num}, choose a pit (1-6):"))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue 
            if not pit_num in list(range(1, 7)):      
                print("Choose 1-6 only.")
                continue
            return pit_num    

    def start(self) -> None:
        self.current_player_num = Player.show_menu()
        print(Fore.YELLOW+"         --------- Mancala ---------")
        print(self.board)
        self.game_loop()

    def game_loop(self) -> None:
        while True:
            if isinstance(self.player2, AIPlayer) and self.current_player_num == 2:
                print(Fore.YELLOW + "AI is thinking...")
                Game.clear_screen()
                pit_index   = self.player2.get_best_pit(self.board, 2)
                current_pit = self.board.fill_pit(2, pit_index - 7)
                print(Fore.CYAN+f"AI chose pit {pit_index - 6}.")
            else:
                pit_num     = Game.valid_input(self.current_player_num)    
                current_pit = self.board.fill_pit(self.current_player_num, pit_num - 1)
            if current_pit is None:
                continue
            Game.clear_screen()
            print(Fore.YELLOW+"         --------- Mancala ---------")
            print(self.board)
            print(Fore.CYAN + f"Score → Husnain: {self.board.p1_score} | AI: {self.board.p2_score}")
            if (current_pit == Board.P1_STORE and self.current_player_num == 1) or \
               (current_pit == Board.P2_STORE and self.current_player_num == 2):
                if self.current_player_num == 2:
                    print(Fore.MAGENTA + "AI gets a Bonus Turn!")
                else:
                    print(Fore.GREEN + "Bonus Turn for Husnain!")
                continue
            if self.board.check_capture(current_pit, self.current_player_num):
                if self.current_player_num == 2:
                    print(Fore.RED + "AI captured your stones!")
                else:
                    print(Fore.GREEN + "You captured AI's stones!")
            empty_side = self.board.is_side_empty()
            if empty_side:
                print(Fore.RED + Style.BRIGHT + "------Game is Over------")
                self.board.sweep_remaining(2 if empty_side == 1 else 1)
                Game.clear_screen()
                print(self.board)
                if self.board.is_winner():
                    break            
            self.current_player_num = self.current_player_num % 2 + 1

if __name__ == "__main__":
    P1 = Player("Husnain", 1)
    P2 = AIPlayer("AI", 2)
    game = Game(P1, P2)
    game.start()
