# 2048 Game – Python Console Version

**Coded by Husnain Maroof, Machine Learning Engineer – 02 Sep, 2025**

A fully playable **2048 game** implemented in Python, running in the console with a clean Unicode-based grid. Players can move tiles using keyboard commands, merge numbers, and try to reach the 2048 tile.

---

## Table of Contents

- [Overview](#overview)  
- [Features](#features)  
- [Controls](#controls)  
- [Gameplay Instructions](#gameplay-instructions)  
- [Dependencies](#dependencies)  
- [How to Run](#how-to-run)  
- [License](#license)  

---

## Overview

2048 is a popular single-player sliding block puzzle game. The objective is to slide numbered tiles on a grid to combine them and create a tile with the number **2048**.  

This console implementation features:  
- Clear Unicode grid display  
- Automatic addition of new tiles after valid moves  
- Full support for tile merging in all directions  
- Game over detection and 2048 win check  

---

## Features

- **Grid Size:** Default 4x4, easily adjustable.  
- **Tile Movement:** Supports moving tiles **up, down, left, and right**.  
- **Merging Mechanics:** Consecutive tiles with the same value combine automatically.  
- **Random Tile Addition:** Adds a new tile (2) after every valid move.  
- **Game End Conditions:** Detects if no moves or merges are left.  
- **Win Detection:** Alerts the player when the 2048 tile is reached.  

---

## Controls

| Key | Action       |
|-----|--------------|
| W/w | Move Up      |
| S/s | Move Down    |
| A/a | Move Left    |
| D/d | Move Right   |

---

## Gameplay Instructions

1. Run the script in your console.  
2. Tiles appear randomly on the grid at the start.  
3. Use **W, A, S, D** keys to slide tiles in the desired direction.  
4. When two tiles of the same number collide, they merge into one.  
5. The game continues until:
   - You reach the **2048 tile**, or  
   - No empty spaces or possible merges remain (game over).  
6. Decide whether to continue playing after reaching 2048.  

---

## Dependencies

- Python 3.x  
- Works in Windows console (uses `os.system('cls')`), for Linux/macOS replace with `clear`.  

---

## How to Run

1. Clone this repository:  
   ```bash
   git clone https://github.com/husnainalix77/HusnainPythonPortfolio.git