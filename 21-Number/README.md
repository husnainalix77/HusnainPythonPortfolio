# 21 Number Game (Human vs Computer)

**Author:** Husnain Maroof  

A **Python terminal-based strategy game** where a human player competes against the computer by sequentially counting numbers. The objective is to **avoid saying the number 21**.

The player who is forced to say **21 loses the game**.

---

## Overview

This program simulates the classic **21 counting game** between a user and a computer opponent.

Players take turns saying **1 to 3 consecutive numbers** in order.  
The sequence starts from **1** and continues until someone reaches **21**.

- If the **user says 21**, the computer wins.
- If the **computer says 21**, the user wins.

The computer includes a **simple strategy** to try forcing the user to say 21.

---

## Game Rules

1. The counting sequence starts at **1**.
2. Each player can say **1, 2, or 3 numbers** on their turn.
3. Numbers must always continue sequentially.
4. The player who says **21 loses**.

---

## Computer Strategy

The computer attempts to control the game using **safe numbers**:

The sequence continues until someone reaches **21**.

---

## Features

- Human vs computer gameplay
- Strategic computer moves using safe numbers
- Random fallback when strategy is unavailable
- Turn-based interaction
- Input validation
- Graceful exit using keyboard interrupt
- Delayed output for better gameplay experience

---

## Technologies Used

- Python
- Lists
- Random number generation
- Time delays for gameplay pacing
- Control flow logic

---

## How to Run

Run the program using Python:

```bash
python 21_number_game.py