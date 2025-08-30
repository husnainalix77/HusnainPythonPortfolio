import random

# Hangman Game - Husnain Maroof- August, 2025.
# Colors for terminal
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
PURPLE = "\033[95m"
RESET = "\033[0m"

def choose_word(all_categories, category_names):
    """Picks a random word from different categories."""
    category_index = random.randint(0, len(all_categories)-1)
    word = random.choice(all_categories[category_index]).lower()
    print(YELLOW+f"It is a '{category_names[category_index]}' category."+RESET)
    return word

def add_word(letter, word, current_state):
    """Adds word if it is valid letter"""
    
    if letter in word:       
        for idx, ch in enumerate(word): 
            if ch == letter:
                current_state[idx] = letter
        return True 
    return False  

def display_title():
    """Displays game title after each attempt."""
    print(CYAN+"\n===== WORD GUESSING GAME (Hangman) ====="+RESET) 
    
def display_game_state(attempts, guessed_letters, current_state):
    """Displays game state after each attempt."""
    print(CYAN+f"\nAttempts left: {attempts}"+RESET)

    if len(guessed_letters) >= 1:
        print("Guessed letters so far:", ', '.join(sorted(guessed_letters)))

    print(PURPLE+"Word:", ' '.join(current_state)+RESET)    
    
def get_guess():
    """Verifies the guessed word."""
    while True:
        guess = input("Enter a character: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha():
            print("Enter only one valid character")
            continue
        
        return guess             

## Main Program    
if __name__ == "__main__":
    countries = ['Pakistan', 'Japan', 'Turkey', 'India', 'England', 'Brazil', 'Canada']
    animals = ['Elephant', 'Tiger', 'Kangaroo', 'Panda', 'Dolphin', 'Cheetah', 'Rabbit']
    fruits = ['Apple', 'Banana', 'Mango', 'Strawberry', 'Pineapple', 'Orange', 'Grapes']

    all_categories =[countries, animals, fruits]
    category_names=['Countries', 'Animals', 'Fruits']
    
    while True:  
        
        display_title()
        word = choose_word(all_categories, category_names)
        attempts = len(word) + 2
        current_state = ['-'] * len(word)
        guessed_letters=set()

        while True:
            if attempts==0:
                print(RED + "\n❌ Out of attempts!" + RESET)
                print(RED + f"The word was: {word.upper()}" + RESET)
                break
            
            print("-" * 35)
            display_game_state(attempts, guessed_letters, current_state)
            guess = get_guess()
            
            if guess in guessed_letters:
                print(f"You already guessed '{guess}'.") 
                continue
            
            if add_word(guess, word, current_state):
                print(GREEN + f"Good guess! '{guess}' is in the word." + RESET)
                                                                
            else:
                print(RED + "Wrong guess!" + RESET)
                attempts-=1    
                
            guessed_letters.add (guess)   
            # If word is completely guessed
            if '-' not in current_state:
                print("Word : "+''.join(current_state)) 
                print(GREEN + "\n🎉 YOU WON!" + RESET)
                print(GREEN + "You guessed the word: " + ''.join(current_state).upper() + RESET)
                break ## To break inner loop
        op = input('Do you want to play again (yes/no): ').strip().lower()
        if op == 'no':
            print('Thanks for playing!')
            break ## to break outer loop