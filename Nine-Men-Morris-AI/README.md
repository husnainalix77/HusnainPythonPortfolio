
# Nine Men's Morris — Human vs AI

## Overview
A fully console-based implementation of the classic board game **Nine Men's Morris**,
where a Human plays against an AI opponent across all three phases of the game.
The AI is powered by the **Minimax algorithm with Alpha-Beta Pruning** and a
**six-factor heuristic evaluation function**, making it capable of strategic
planning, mill formation, threat detection, and smart captures.
The project is built using **pure Object-Oriented Programming** across 5 modules
with a colored terminal UI using ANSI escape codes.

**Developer:** Husnain Maroof | **Version:** 1.0 | **Date:** March 13–19, 2026

---

## Files
| File | Role |
|---|---|
| `game.py` | Main game controller — manages phases, turns, input flow, and win detection |
| `board.py` | Board state management, ANSI colored display, and position operations |
| `player.py` | Human player class — input handling, piece placement and tracking |
| `ai_player.py` | AI player — Minimax, Alpha-Beta Pruning, heuristics, and capture logic |
| `mill_logic.py` | Static game rules — mill detection, adjacency map, capture validation, win checks |

---

## How to Run
```bash
python game.py
```
> ✅ No external libraries required. Python 3.x only.  
> ✅ All 5 files must be in the same folder.

---

## How to Play
The board has **24 positions** numbered 1–24 displayed in the terminal with colored pieces and connecting lines.
- **W** → Human pieces (Bold Red) | **B** → AI pieces (Bold Cyan)
- Form a **mill** (3 pieces in a straight line) to capture one opponent piece
- Win by reducing opponent to **2 pieces** or blocking all their moves

---

## Game Phases
| Phase | Trigger | Description |
|---|---|---|
| **Phase 1 — Placing** | Start of game | Both players place all 9 pieces one at a time |
| **Phase 2 — Moving** | After all pieces placed | Slide pieces to adjacent empty positions only |
| **Phase 3 — Flying** | Player reaches 3 pieces | That player can move to any empty position |

---

## AI Design

### Decision Pipeline (in order)
```
1. Immediate Win   → If AI can win this turn, do it
2. Mill Formation  → If AI can form a mill, place there
3. Block           → If human is about to form a mill, block it
4. Minimax         → Otherwise, run full Minimax search
```

### Minimax with Alpha-Beta Pruning
Searches the game tree recursively across all three phases with **adaptive depth**:

| Empty Positions | Search Depth |
|---|---|
| ≥ 20 | 4 |
| ≥ 15 | 5 |
| ≥ 10 | 6 |
| < 10 | 7 |

### Six-Factor Heuristic Evaluation
| Factor | What it Measures | Weight |
|---|---|---|
| **Piece Count** | Difference in pieces remaining | 50 |
| **Completed Mills** | Number of active mills formed | 100 |
| **Potential Mills** | Two pieces aligned with one empty slot | 30 |
| **Double Mills** | Pieces part of two potential mills at once | 40 |
| **Mobility** | Number of valid moves available | 10 |
| **Blocked Pieces** | Pieces with no adjacent empty positions | 20 |

---

## OOP Design
```
Player                   ← Base class (input, piece tracking)
    └── AIPlayer         ← Minimax, heuristics, capture logic

Board                    ← Board state, ANSI colored display
Mill_Logic               ← Static rules (mills, adjacency, captures, win checks)
Game                     ← Main controller (Phase 1, Phase 2/3, turn switching)
```

---

## Concepts Used
- Object-Oriented Programming (Inheritance, Encapsulation, Static Methods)
- Minimax Algorithm with Alpha-Beta Pruning
- Adaptive Search Depth
- Multi-Factor Weighted Heuristic Evaluation
- Game Tree Search and State Simulation
- ANSI Color Codes for Terminal UI
- Modular Design across Multiple Files

---

## Author
**Husnain Maroof**  
Mechatronics & Control Engineering, UET Lahore  
GitHub: [husnainalix77](https://github.com/husnainalix77)