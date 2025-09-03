# 15 Puzzle Game — NxN Sliding Puzzle

## Overview
A terminal-based NxN sliding puzzle game where the player arranges numbered tiles
in ascending order by sliding them into the blank space.
The board is always generated as a **solvable configuration** using inversion counting logic.

## Files
| File | Description |
|---|---|
| `15_puzzle_game.py` | Complete sliding puzzle with move validation and win detection |

## How to Run
```bash
python 15_puzzle_game.py
```
> No external libraries required. Python 3.x only.

## Controls
| Key | Action |
|---|---|
| `W` | Move blank Up |
| `S` | Move blank Down |
| `A` | Move blank Left |
| `D` | Move blank Right |
| No diagonal movement allowed |

## Features
- ✅ Configurable NxN board (default 4×4)
- ✅ Guaranteed solvable puzzle generation using inversion counting
- ✅ Move counter tracking total moves taken
- ✅ Win detection with completion timestamp
- ✅ Clean screen refresh after every move
- ✅ Cross-platform screen clearing (Windows & Linux/macOS)
- ✅ Input validation with helpful error messages

## Solvability Logic
- **Odd N** → Solvable if total inversions are even
- **Even N** → Solvable if (inversions + blank row from bottom) is odd

## Concepts Used
- Procedural Programming
- 2D List Manipulation
- Inversion Counting Algorithm
- OS & Platform Detection
- DateTime Module
- Input Validation

## Author
**Husnain Maroof**  
Mechatronics & Control Engineering, UET Lahore  
GitHub: [husnainalix77](https://github.com/husnainalix77)