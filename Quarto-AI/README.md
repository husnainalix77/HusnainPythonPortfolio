# Quarto Game with AI (Minimax + Alpha-Beta Pruning)

**Author:** Husnain Maroof  
**Role:** ML Engineer  
**Development Date:** September 20–26, 2025  

This project implements the complete **Quarto board game** with an **AI opponent** that uses **Minimax search with Alpha–Beta pruning** and an **adaptive heuristic evaluation function**.

The game runs in the **terminal** and allows a human player to compete against an intelligent computer opponent.

---

# Project Overview

**Quarto** is a two-player abstract strategy game played on a **4×4 board** with **16 unique pieces**.

Each piece has **four attributes**, and a player wins by creating a row, column, or diagonal of **four pieces sharing at least one common attribute**.

Unlike many board games, in Quarto:

- Players **place the piece chosen by the opponent**.
- Each turn consists of two phases:
  1. **Choosing a piece for the opponent**
  2. **Placing the piece given by the opponent**

This adds a strong strategic layer to the game.

This implementation includes an **AI player capable of both selecting pieces and placing them intelligently**.

---

# Game Features

- Human vs AI gameplay
- Full **Quarto game rules**
- AI decision-making using **Minimax**
- **Alpha–Beta pruning optimization**
- **Adaptive search depth**
- Board evaluation using heuristic scoring
- Immediate win detection
- Prevention of giving opponent winning pieces
- Terminal board display with Unicode formatting
- Colored pieces for visual clarity

---

# Game Pieces

Each of the **16 pieces** has four binary attributes:

| Attribute | Values |
|----------|--------|
| Height | Tall (T) / Short (S) |
| Color | Light (L) / Dark (D) |
| Shape | Square (Q) / Round (R) |
| Structure | Hollow (O) / Solid (H) |


---

# Technologies Used

- Python
- Object-Oriented Programming
- Minimax Algorithm
- Alpha-Beta Pruning
- Heuristic Evaluation Functions
- Recursive Search Algorithms

---

# How to Run

Clone the repository:

```bash
git clone https://github.com/husnainalix77/HusnainPythonPortfolio.git
