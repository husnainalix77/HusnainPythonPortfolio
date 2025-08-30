# Rules for deciding the winner:
# Rock beats Scissors (Rock breaks Scissors)
# Scissors beats Paper (Scissors cut Paper)
# Paper beats Rock (Paper covers Rock)
# If both players choose the same move, the game is a draw (no winner).
import random
user_wins = 0
computer_wins = 0

options = ['rock','paper','scissors']

rules = {
    'rock':'scissors',
    'scissors':'paper',
    'paper':'rock'  
}  

while True :
    user_input = input('Type Rock/Paper/Scissors or Q to quit: ').lower()
    if user_input == 'q':
        break
    
    if user_input not in options:
        print('Please type Rock/Paper/Scissors')
        continue
    
    computer_input = random.choice(options)
    print(f'Computer\'s choice is : {computer_input}' )
    
    if user_input == computer_input:
        print(f"Both chose {user_input}. It's a tie!")
        
    elif rules[user_input] == computer_input:
        print(f"{user_input.capitalize()} beats {computer_input}. You won!")
        user_wins += 1
        
    else:
        print(f"{computer_input.capitalize()} beats {user_input}. You lost!")
        computer_wins += 1

print(f'You won {user_wins} times') 
print(f'Computer won {computer_wins} times')
print('Goodbye !')  