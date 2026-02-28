# Button Men Dice Game (Python GUI)

**Developer:** Husnain Maroof  
**Date:** Feb 25–28, 2026.  

A **turn-based strategy dice combat game** implemented in Python using **Tkinter for the graphical interface**.  
The game includes **animated dice rolling**, **character-based dice sets**, and an **AI opponent** that makes probabilistic attack decisions instead of random moves.

---

## Overview

In this game, each player selects a **character** with a predefined set of dice.  
Each die represents strength depending on its number of sides.

Players take turns:

1. Selecting one of their dice to attack
2. Choosing an opponent’s die as the target
3. Rolling both dice
4. Capturing the opponent’s die if their roll is **greater than or equal to** the opponent's roll

The player who **eliminates all opponent dice wins the battle**.

---

## Game Features

### Graphical Interface
- Built using **Tkinter**
- Interactive dice buttons
- Real-time battle log
- Smooth dice rolling animations

### AI Opponent
The AI evaluates attacks using probability-based logic:

- Expected value of roll difference
- Probability of winning the roll
- Target prioritization
- Overkill penalty to avoid wasting strong dice

This results in a **strategic AI instead of a random one**.

### Dice Rolling Animation
Before showing the final result:

- Dice display rapidly changing values
- Creates a **real-time rolling animation effect**
- Final roll determines capture outcome

### Character System

Each character has a unique set of dice.

| Character | Dice |
|-----------|------|
| Titanus | d12, d20 |
| Viper | d6, d18 |
| Rift | d10, d16 |
| Bauer | d4, d6, d8 |
| Hammer | d10, d12, d14 |
| Shore | d5, d7, d9 |
| Stark | d3, d11, d13 |
| Sentinel | d4, d6, d10, d14 |
| Tempest | d3, d8, d11, d15 |
| Legion | d2, d4, d6, d8, d10 |

Different characters create different **strategic gameplay styles** depending on dice sizes and counts.

---

## Game Flow

1. Splash screen appears
2. Player selects a character
3. AI randomly selects its character
4. Both players roll dice to determine who starts
5. Players alternate turns attacking opponent dice
6. Captured dice are removed from play
7. When a player loses all dice, the opponent wins

---

## Technologies Used

- **Python**
- **Tkinter GUI**
- Object-Oriented Programming
- Probability-based AI decision system
- Event-driven animations using `after()`

---

## Core Classes

### `Die`
Represents a die with a configurable number of sides.

### `Player`
Handles:
- Dice management
- AI character selection
- AI attack decision logic

### `ButtonMenGUI`
Responsible for:
- User interface
- Dice animations
- Turn handling
- Game state updates

---

## Running the Game

```bash
python button_men_dice_game.py