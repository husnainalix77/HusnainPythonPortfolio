# Mancala AI Game (Human vs AI)

A terminal-based implementation of the ancient board game **Mancala**, where a human player competes against an AI opponent.  
The AI uses classical game-search algorithms to make intelligent moves.

---

## Features

- Human vs AI gameplay
- Minimax search algorithm
- Alpha-Beta pruning optimization
- Adaptive search depth
- Capture and bonus-turn mechanics
- Terminal-based game board

---

## Game Rules (Simplified)

- The board contains **6 pits for each player** and **2 stores**.
- Each pit initially contains **4 stones**.
- Players choose a pit and distribute stones counter-clockwise.
- Landing in your **store gives a bonus turn**.
- Landing in an **empty pit on your side captures opponent stones**.
- The game ends when one side of pits becomes empty.

The player with the **most stones in their store wins**.

---

## AI Strategy

The AI uses:

- **Minimax Algorithm**
- **Alpha-Beta Pruning**
- **Heuristic Evaluation Function**

The evaluation function considers:

- Score difference between stores
- Potential capture opportunities
- Extra move opportunities
- Stone distribution on both sides

---
