# Boggle Game (Human vs AI)

**Author:** Husnain Maroof  
**Date:** 2 October 2025  

A complete **terminal-based implementation of the classic Boggle word game**, where a human player competes against an **AI word generator**.

The game uses a **4×4 randomized Boggle board**, validates words using a **dictionary dataset**, and applies **Depth-First Search (DFS)** to generate all possible valid words for the AI.

The player must find as many valid words as possible within **3 minutes**.

---

# Project Overview

Boggle is a word search game where players form words by connecting adjacent letters on a grid.

This implementation includes:

- Random board generation using **official Boggle dice**
- **AI word generation using DFS**
- **Dictionary validation**
- **Prefix pruning optimization**
- **Time-limited gameplay**
- **Automatic scoring system**

The AI finds all possible valid words on the board, while the human player tries to find as many words as possible before time runs out.

---

# Game Features

- Human vs AI gameplay
- Randomized **4×4 Boggle board**
- Official **Boggle dice configuration**
- Color-coded grid display
- AI word generation using **Depth-First Search**
- **Prefix pruning optimization** for faster search
- Dictionary-based word validation
- 3-minute timer
- Duplicate word detection
- Automatic scoring system

---

# Technologies Used

- **Python**
- Depth-First Search (DFS)
- Recursive algorithms
- Set data structures for fast lookup
- Prefix pruning optimization
- Terminal ANSI color formatting

---

# AI Algorithm

The AI uses an **optimized DFS search** to generate valid words.

### Steps

1. Start DFS from every grid cell.
2. Build words by moving to adjacent cells.
3. Avoid revisiting the same cell in a word path.
4. Use **prefix pruning** to stop exploring impossible paths early.
5. Store all valid words found in the dictionary.

### Search Directions

The DFS explores **8 directions**

---

# Grid Generation Logic

The board is generated using the **standard Boggle dice set**.

Additional constraints ensure good gameplay:

- The grid must contain **at least 3 vowels**
- The grid cannot contain **too many rare letters (J, Q, X, Z)**

This avoids boards that are too difficult.

---

# Word Validation

User words must satisfy:

1. Must exist in the **dictionary**
2. Must be **3–8 letters long**
3. Must be **formable on the board**
4. Cannot reuse the same grid tile
5. Cannot be entered twice

---

# Scoring Rules

The scoring system follows **official Boggle rules**.

| Word Length | Points |
|-------------|--------|
| 3–4 letters | 1 |
| 5 letters | 2 |
| 6 letters | 3 |
| 7 letters | 5 |
| 8+ letters | 11 |

Only words **not found by the opponent** count toward your score.

---

# Game Flow

1. The board is generated randomly.
2. The AI generates all possible valid words.
3. A **3-minute timer** begins.
4. The player enters words found on the grid.
5. Words are validated and stored.
6. When time ends, scores are calculated.

---

Place the file in the **same folder as the Python script**.

---

# How to Run

### 1. Clone the repository

```bash
git clone https://github.com/husnainalix77/Boggle-AI.git

