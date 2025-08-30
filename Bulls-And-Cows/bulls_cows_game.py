import random 
import time

def uniqueDigits(num):
    'Checks if number has unique digits'
    if len(str(num)) == len(set(str(num))):
        return True
    return False

def generateNumber():
    'Generates a random number'
    while True:
        number= random.randrange(1000, 10000)
        if uniqueDigits(number):
            return str(number)
        
def numOfBullsCows(num, guess):
    'Calculates number of bulls and cows after each guess'
    bull_cow = [0,0]
    if guess == num:
        bull_cow[0], bull_cow[1] = len(num), 0
    else:
        for v1, v2 in zip(num, guess):
            if v2 in num:
                if v1 == v2: ## v2 in num in correct position
                    bull_cow[0]+=1
                else:
                    bull_cow[1]+=1  ## v2 in num in wrong position
                    
    return (bull_cow[0], bull_cow[1])                                 
            
## Main Program        
if __name__=='__main__' :
    number = generateNumber()
    max_turns = int(input('Enter number of tries: '))
    turns = 0
    isWinner = False
    
    while turns < max_turns:
        print(f'No. of attempts left: {max_turns-turns}')
        time.sleep(0.5)
        guess = input('Enter a guess (with unique digits): ')
        
        if not guess.isdigit() or not int(guess) in range(1000, 10000):
            print(f'Enter a valid {len(number)} digit number. ')
            continue
        
        if not uniqueDigits(guess):
            print(f'Please enter a {len(number)} digit number with unique digits.')
            continue
        
        turns += 1
        bull, cow = numOfBullsCows(number, guess)
        if bull == len(number):
            print('You guessed it right!')
            print(f'The number was: {number}')
            isWinner = True 
            break 
        
        else:
            print(f'Response: {bull} bulls, {cow} cows.')
        time.sleep(0.5)    
        
    ## if not guessed        
    if not isWinner:
        print(f'You lose.\nThe number was {number}')        
            
            
        
        
        
            
            
           