# Mastermind Number Guessing Game

**Author:** Husnain Maroof  
**Description:** A Python terminal-based **number guessing game inspired by the Mastermind concept**, where the player must guess a secret multi-digit number within a limited number of attempts using logical clues.

---

## Overview

This program generates a **random 4-digit secret number**, and the player must guess the number within **10 attempts**.

After each guess, the program provides hints to help the player move closer to the correct number:

- Digits that are **correct and in the correct position**
- Digits that are **correct but in the wrong position**
- Notification if **none of the digits match**

The objective is to deduce the secret number using these clues.

---

## Game Rules

- The secret number is randomly generated between **1000 and 9999**
- The player has **10 turns** to guess the number
- Each guess must be a **valid 4-digit number**
- After each guess, feedback is given to guide the player

---

## Hint System

The game provides two types of hints:

### 1. Correct Digit in Correct Position
If a digit is correct and in the correct place, it is revealed in the partially discovered number.

Example:

Number: 4--2


---

## Features

- Random secret number generation
- Input validation
- Intelligent hint system
- Turn limit system
- Partial number reveal
- Smooth gameplay using timed delays

---

## Technologies Used

- Python
- Random number generation
- Lists and string manipulation
- Control flow logic
- Time delays for improved user experience

---

## How to Run

```bash
python mastermind_game.py