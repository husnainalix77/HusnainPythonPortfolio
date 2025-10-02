# ----------------------------------------------------------
# Boggle Game (Human vs AI)
# Author: Husnain Maroof
# Date: 2 October 2025
# Description: Full implementation of a 4x4 Boggle game 
# with AI word generation, dictionary validation, 
# scoring, and time-limited gameplay.
# ----------------------------------------------------------
import random
import time 
# Standard 4x4 Boggle Dice Set
DICE_SET = [
    ['A', 'A', 'E', 'E', 'G', 'N'],
    ['A', 'B', 'B', 'J', 'O', 'O'],
    ['A', 'C', 'H', 'O', 'P', 'S'],
    ['A', 'F', 'F', 'K', 'P', 'S'],
    ['A', 'O', 'O', 'T', 'T', 'W'],
    ['C', 'I', 'M', 'O', 'T', 'U'],
    ['D', 'E', 'I', 'L', 'R', 'X'],
    ['D', 'E', 'L', 'R', 'V', 'Y'],
    ['D', 'I', 'S', 'T', 'T', 'Y'],
    ['E', 'E', 'G', 'H', 'N', 'W'],
    ['E', 'E', 'I', 'N', 'S', 'U'],
    ['E', 'H', 'R', 'T', 'V', 'W'],
    ['E', 'I', 'O', 'S', 'S', 'T'],
    ['E', 'L', 'R', 'T', 'T', 'Y'],
    ['H', 'I', 'M', 'N', 'Qu', 'U'], # Note: 'Qu' is treated as one tile
    ['H', 'L', 'N', 'N', 'R', 'Z']
]
    
def setUpGrid(N, Dice):
    """Create an NxN Boggle grid with random dice rolls."""
    flat = [random.choice(die) for die in Dice]
    random.shuffle(flat)
    grid = [flat[i:i+N] for i in range(0, N*N, N)]
    return grid

def hasManyRareLetters(grid):
    """Return True if grid has more than 2 rare letters (J, Q, X, Z, Qu)."""
    letters = 'JQXZ'
    count = sum(1 for row in grid for c in row if c in letters or c == 'Qu')
    return count > 2

def hasLessVowels(grid):
    """Return True if grid has fewer than 3 vowels."""
    vowels = 'AEIOU'
    count = sum(c in vowels for row in grid for c in row) 
    return count < 3 
    
def dispGrid(grid):
    """Print the grid in a formatted, color-coded box style."""
    N = len(grid)
    cell_width = 3 
    RESET = "\033[0m"
    VOWEL_COLOR = "\033[93m"    # Bright Yellow 
    QU_COLOR = "\033[91m"       # Bright Red
    CONSONANT_COLOR = "\033[97m" # Bright White
    VOWELS = 'AEIOU'
    top = "┌" + "┬".join(["─" * cell_width] * N) + "┐"
    mid = "├" + "┼".join(["─" * cell_width] * N) + "┤"
    bottom = "└" + "┴".join(["─" * cell_width] * N) + "┘"
    print(top)
    for r, row in enumerate(grid):
        colored_tiles = []
        for c in row:
            if c == 'Qu':
                color = QU_COLOR
            elif c in VOWELS:
                color = VOWEL_COLOR
            else:
                color = CONSONANT_COLOR
            colored_c = f"{color}{c:^{cell_width}}{RESET}"
            colored_tiles.append(colored_c)
        print("│" + "│".join(colored_tiles) + "│")
        
        if r < N - 1:
            print(mid)
    print(bottom)
    
def loadWords(file_name):
    """
    all_words: full dictionary words (len >= 3).
    all_prefixes: all possible word beginnings (prefixes).
    Used in DFS to prune invalid paths early. 
    Example: "CAT" -> {"C","CA","CAT"}.
    """
    all_words = set() 
    all_prefixes = set() 
    try:
        with open(file_name, 'r') as f:
            for line in f:
                word = line.strip().upper()
                if len(word) >= 3:
                    all_words.add(word)
                    for i in range(1, len(word) + 1):
                        all_prefixes.add(word[:i])
    except FileNotFoundError:
        print(f"Dictionary file '{file_name}' not found. Check the file path.")
        exit()
    return all_words, all_prefixes
        
# --- WORD GENERATION FUNCTIONS ---

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1), 
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1)
]

def findAllWordsDFS(r, c, current_word, visited, grid, words_set, prefixes_set, found_words):
    """Recursive DFS to find all words starting from (r, c)."""
    N = len(grid)
    # Pruning Check
    if current_word not in prefixes_set:
        return
    # Word Found Check
    if current_word in words_set:
        found_words.add(current_word)
    # Recursive Step
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc 
        if 0 <= nr < N and 0 <= nc < N and (nr, nc) not in visited:
            tile = grid[nr][nc]
            new_word = current_word + tile
            
            findAllWordsDFS(nr, nc, new_word, visited | {(nr, nc)}, 
                            grid, words_set, prefixes_set, found_words)

def findAllAiWords(grid, words_set, prefixes_set):
    """Runs the optimized DFS from every cell to find all AI words."""
    found_words = set()
    N = len(grid)
    for r in range(N):
        for c in range(N):
            start_tile = grid[r][c]
            findAllWordsDFS(r, c, start_tile, {(r, c)}, 
                            grid, words_set, prefixes_set, found_words)
                            
    return {word for word in found_words if 3 <= len(word) <= 8}

def isValidWord(word, words_set, grid):
    """Check if a word can be formed on the grid."""
    if word not in words_set: # Word must be in words set
        return False
    N = len(grid)
    def dfs(r, c , idx, visited):
        if idx == len(word): # Complete word found
            return True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc 
            if (0 <= nr < N and 0 <= nc < N) and (nr, nc) not in visited:
                tile = grid[nr][nc] 
                if word[idx:].startswith(tile):
                    if dfs(nr, nc, idx + len(tile), visited | {(nr, nc)}):
                        return True 
        return False
    
    for r in range(N):
        for c in range(N):
            cell = grid[r][c]
            if word.startswith(cell):
                if dfs(r, c, len(cell), {(r, c)}):
                    return True
    return False 
    
def assignPoints(user_words, opponent_words):
    """Return score for words not found by opponent, using Boggle rules."""
    total_points = 0
    for word in user_words:
        if word not in opponent_words:
            if len(word) in [3, 4]:
                total_points += 1
            elif len(word) == 5:
                total_points += 2
            elif len(word) == 6:
                total_points += 3
            elif len(word) == 7:
                total_points += 5
            else: 
                total_points += 11
    return total_points 
    
# Main program
if __name__ == "__main__":
    N = 4
    TIME_LIMIT = 180 # 3 minutes in seconds
    # --- Setup Grid ---
    grid = setUpGrid(N, DICE_SET)
    while hasLessVowels(grid) or hasManyRareLetters(grid):
        grid = setUpGrid(N, DICE_SET)
    dispGrid(grid)
    # --- Load Dictionary ---
    print("Loading dictionary and generating prefix set...")
    words_set, prefixes_set = loadWords('words_alpha.txt')
    user_words= set()
    # --- AI is making words ---
    print('AI is generating words.')
    ai_words = findAllAiWords(grid, words_set, prefixes_set)
    print(f'AI found {len(ai_words)} words! The 3-minute timer starts now.')
    # --- Start Timer ---
    start_time = time.time()
    end_time = start_time + TIME_LIMIT
    # --- User Input Loop ---
    while time.time() < end_time:
        # Calculate remaining time for display
        remaining_seconds = int(end_time - time.time())
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        # Display the timer prominently
        timer_display = f"\n\033[92mTIME LEFT: {minutes:02d}:{seconds:02d}\033[0m"
        print(timer_display)
        user_word = input('Make word from grid (type END to finish): ').strip().upper()
        if user_word == 'END':
            break
        if not user_word:
            print('You entered nothing!')
            continue
        # 1. Dictionary Check
        if user_word not in words_set:
            print(f'"{user_word}" is not in the dictionary.')
            continue
        # 2. Length Check
        if not (3 <= len(user_word) <= 8):
            print('Words must be between 3 and 8 letters long.')
            continue
        # 3. Grid Path Check
        if isValidWord(user_word, words_set, grid):
            if user_word in user_words:
                print(f'"{user_word}" has already been entered.')
            else:
                user_words.add(user_word) 
                print(f'\033[96m"{user_word}" is a valid word! Added to your list.\033[0m')
        else:
             print(f'"{user_word}" cannot be formed on the grid.')
    # --- Timer Ended ---
    if time.time() >= end_time:
        print("\n\033[91mTIME'S UP! The game has ended.\033[0m")
    else:
        print("\nGame ended early.")

    # --- Score Calculation ---
    print("\n--- Final Scores ---")
    user_points = assignPoints(user_words, ai_words)
    ai_points = assignPoints(ai_words, user_words)
    
    print(f"Words Found: You ({len(user_words)}), AI ({len(ai_words)})")
    print(f"Your Score: {user_points}")
    print(f"AI Score: {ai_points}")

    if user_points > ai_points:
        print('You Won the game. Congratulations!')
    elif ai_points > user_points:
        print('OOPS! AI Won.') 
    else:
        print('It is a draw.')