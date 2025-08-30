# Bulls and Cows Game

## Overview
A terminal-based **Bulls and Cows** number guessing game in Python.
The player tries to guess a randomly generated 4-digit number with unique digits
within a limited number of attempts.

## Files
| File | Description |
|---|---|
| `bulls_cows_game.py` | Complete game with bulls/cows logic and input validation |

## How to Run
```bash
python bulls_cows_game.py
```
> No external libraries required. Python 3.x only.

## How to Play
- A random **4-digit number with unique digits** is generated
- You choose how many attempts you want
- After each guess you get feedback:
  - 🐂 **Bull** — correct digit in correct position
  - 🐄 **Cow** — correct digit in wrong position
- Guess the number before you run out of attempts!

## Example
```
Enter number of tries: 8
No. of attempts left: 8
Enter a guess (with unique digits): 1234
Response: 1 bulls, 2 cows.
```

## Features
- ✅ Randomly generated 4-digit number with unique digits
- ✅ Player chooses number of attempts
- ✅ Bulls & cows feedback after every guess
- ✅ Input validation (numeric, 4-digit, unique digits)
- ✅ Win/lose message with reveal of correct number

## Concepts Used
- Procedural Programming
- Random Module
- String & Set Operations
- Input Validation
- Game Loop Logic

## Author
**Husnain Maroof**  
Mechatronics & Control Engineering, UET Lahore  
GitHub: [husnainalix77](https://github.com/husnainalix77)