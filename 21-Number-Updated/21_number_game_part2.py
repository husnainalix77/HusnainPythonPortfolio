import random
import time
import sys
print('Player 2 is computer')
while True:
    try:
        op = input('Do you want to play game? (yes/no): ').strip().lower()
        if op not in ['yes', 'no']:
            print('Please type yes or no only')
            continue
        break
    except KeyboardInterrupt:
        print("Input cancelled. Exiting...")
        sys.exit()

num = []        
turn = None

if op == 'yes':

    while True:
        choice = input("Enter 'F' to take the first chance or 'S' for computer: ").strip().lower()
        if choice == 'f':
            turn = 'user' 
            break
        elif choice == 's':
            turn = 'computer'
            break
        else:
            print('Please type f or s only')

    safe_nums = [0, 4, 8, 12, 16, 20]

    # Main game loop
    while True:
        # Computer's turn
        if turn == 'computer':
            last_num = num[-1] if num else 0
            next_safe = 21
            for s in safe_nums:
                if s > last_num:
                    next_safe = s
                    break
            computer_pick = next_safe - last_num

            if computer_pick not in range(1, 4):
                computer_pick = random.randint(1, 3)

            new_nums = list(range(last_num + 1, min(22, last_num + computer_pick + 1)))
            num.extend(new_nums)

            print('Computer is choosing...')
            for n in new_nums:
                print(n)
                time.sleep(0.7)

            print(f"Computer: {new_nums}")
            print("Order of inputs after computer turn:")
            print(num)

            if num[-1] >= 21:
                print('Computer chose 21. You won!')
                break

            turn = 'user'
            time.sleep(1)

        # User's turn
        elif turn == 'user':
            while True:
                try:
                    print('How many values do you wish to enter (1-3)? ')
                    user_pick=int(input('> '))
                    if user_pick not in range(1, 4):
                        print('Enter values 1-3 only!')
                        continue
                    break
                
                except KeyboardInterrupt:
                    print("Input cancelled. Exiting...")
                    sys.exit()
            if num:
                if user_pick + num[-1] > 21:
                    user_pick = 21 - num[-1]                 
            for v in range(user_pick): 
                last_num = num[-1] if num else 0 
                n=int(input('Enter values: '))
                if n != last_num + 1:
                    print(f'Invalid value: {n}. Expected {last_num+1}')
                    print('Computer wins')
                    print(f"Game Over! Final sequence: {num}")
                    sys.exit()
                else:              
                    num.append(n)
                    
            print(f'You: {num[-user_pick:]}')
            
            time.sleep(0.7)
            print("Order of inputs after your turn:")
            print(num)                 

            if num[-1] >= 21:
                print('You chose 21. Computer won!')
                break

            turn = 'computer'  
            time.sleep(1)           

else:
    print("Ok, maybe next time")

# End of game
print(f"Game Over! Final sequence: {num}")






