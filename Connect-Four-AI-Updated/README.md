# Connect Four Game (Human vs Strong AI)

**Coded & Updated by Husnain Maroof**  
Machine Learning Enthusiast  
Updated Version — 16 September 2025

---

## Project Overview

This project is an **advanced terminal-based implementation of the classic Connect Four game** where a human player competes against a **strong AI opponent**.

This version is an **updated and significantly improved version** of my previous Connect Four project. The AI logic and board evaluation strategy have been redesigned to make the computer opponent much stronger and more strategic.

The game runs directly in the terminal and uses **colored discs and Unicode grid formatting** for a clean visual experience.

---

## What's New in This Updated Version

The following improvements have been added in this update:

### 1. Stronger AI using Minimax
The computer player now uses the **Minimax algorithm** to search possible future game states and choose the best move.

### 2. Alpha–Beta Pruning
To improve efficiency, **alpha–beta pruning** is implemented.  
This significantly reduces the number of states the AI needs to evaluate.

### 3. Adaptive Search Depth
The AI dynamically adjusts its search depth depending on the number of remaining moves.

| Empty Slots | AI Depth |
|--------------|----------|
| Early Game | Depth 5 |
| Mid Game | Depth 6–7 |
| End Game | Depth 8 |

This allows the AI to think **deeper in the endgame** while maintaining good performance.

### 4. Improved Board Evaluation Function

The board evaluation now considers:

- 3-in-a-row streaks
- 2-in-a-row streaks
- Open-ended streaks
- Center column preference
- Immediate win detection
- Blocking opponent wins

### 5. Double Threat Detection

The AI checks for **double threats**, meaning moves that create **two simultaneous winning opportunities**.  
These moves are prioritized since they are extremely powerful in Connect Four strategy.

### 6. Smart Move Ordering

Columns are searched starting from the **center column first**, because center positions are statistically stronger in Connect Four.

---

## Game Features

- Human vs Computer gameplay
- Strong AI opponent
- Colored discs in terminal
- Unicode formatted game board
- Adaptive AI thinking depth
- Detection of winning streaks
- Draw detection
- Replay option

---

## Technologies Used

- **Python**
- Terminal ANSI color formatting
- Minimax Algorithm
- Alpha–Beta Pruning
- Heuristic Evaluation Functions

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/yourusername/ConnectFour-AI.git