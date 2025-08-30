import random
import time
    
num = random.randrange(1000, 10000) ## You can change this range, if you change, change in while loop too!
secret_num = list(str(num))
max_turns = 10
turns = 0

while turns < max_turns:
    guessed_digits = ['-']*len(secret_num)
    count_digits = 0 ## We just want unique correct digits everytime, not previous ones
    guess = input(f'Guess {len(secret_num)} digit number: ')  
    
    if not guess.isdigit() or int(guess) not in range(1000, 10000):
        print(f'Enter a valid {len(secret_num)}  digit number')
        continue
    
    turns +=1
    guess_list = list(guess)
    
    if guess_list == secret_num:
        if turns == 1:
            print(f"Great! You guessed the number in just 1 try! You're a Mastermind!")
            time.sleep(0.5)
            print(f'The number was: {num}')
        else:
            guessed_digits = guess_list
            print(f"Number: {''.join(guessed_digits)}")
            print(f'It took only {turns} tries to guess the number')
            print("You've become a Mastermind!")
            time.sleep(0.5)
            print(f'The number was: {num}')
        break   
      
    else: ## To find correct digits
        correct_digits= [] ## To keep track of correct digits but with wrong places
        secret_copy = secret_num.copy() 
        guess_copy = guess_list.copy()      
        
        for i in range(len(guess_list)):
            if guess_list[i] == secret_num[i]:
                count_digits += 1
                guessed_digits[i] = guess_list[i]
                guess_copy[i] = None ## That correct digit with correct place, gets assigned None (Removed)
                secret_copy[i] = None 
                
        for j in range(len(guess_list)): ## Here we will add correct digits with wrong places in above list
            if guess_copy[j] is not None and guess_copy[j] in secret_copy: 
                correct_digits.append(guess_copy[j])
                secret_copy[secret_copy.index(guess_copy[j])] = None 
                
        if not (count_digits or correct_digits):
            print('None of the digits in your input match.')
            
        else:
            if count_digits:
                print(f'Not quite the number. But you did get {count_digits}  digit(s) correct!')
                print('Also these digits in your input were correct.')
                time.sleep(0.5)
                print(f"Number: {''.join(guessed_digits)}")
                
            if correct_digits:
                print(f"The correct digit(s) but with wrong place(s): {', '.join(correct_digits)}")
    print()
    time.sleep(0.7)  
             
if secret_num != guess_list:
    print('You lose!')  
    print(f'The number was: {num}')                            
                 
                
                    
                
                
            
        
           
                
       
    

 



                
        
    




