# 21 Number Game (Human vs Computer) — Updated Version

**Author:** Husnain Maroof  

A **Python terminal-based strategic counting game** where a human player competes against the computer.  
Players alternately say **1–3 sequential numbers**, and the player who is forced to say **21 loses the game**.

This updated version improves **input validation, user interaction, and gameplay control**, making the game more robust and fair.

---

## Overview

The program simulates the classic **21 counting game** between a human player and a computer opponent.

Players take turns adding **1, 2, or 3 consecutive numbers** to the counting sequence starting from **1**.

The objective is to **force the opponent to say 21**.

---

## Game Rules

1. The counting sequence starts at **1**.
2. Each player can add **1–3 numbers** during their turn.
3. Numbers must follow **strict sequential order**.
4. The player who says **21 loses**.

---

## Computer Strategy

The computer uses a **safe-number strategy** to try to control the game.


If the computer reaches one of these numbers, it can force the opponent toward **21**.

If a strategic move is not possible, the computer chooses a **random number between 1 and 3**.

---

## Improvements in the Updated Version

This version introduces several enhancements:

### Stronger Input Validation
- Prevents invalid numbers from being entered
- Ensures sequential order is maintained
- Automatically ends the game if the player cheats

### Sequential Input Checking
If the player enters a number that does not follow the correct sequence, turns passed.


The game continues until **21 is reached**.

---

## Features

- Human vs computer gameplay
- Strategic computer opponent
- Sequential input validation
- Safe-number strategy
- Controlled user input
- Graceful exit handling
- Real-time number display
- Turn-based gameplay

---

## Technologies Used

- Python
- Lists
- Random module
- Time delays (`time.sleep`)
- System exit handling (`sys.exit`)
- Control flow logic

---

## How to Run

```bash
python 21_number_game_part2.py


