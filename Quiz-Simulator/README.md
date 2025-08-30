# Adaptive MCQ Quiz System

**Author:** Husnain Maroof  
**Description:** A Python program that simulates an **adaptive online quiz system**.  
Questions are automatically selected from **three difficulty levels** (Easy, Medium, Hard) and the difficulty changes dynamically based on the user's performance.

---

## Overview

This program mimics the behavior of **adaptive online quizzes** often used in learning platforms.

The quiz system:

- Loads MCQs from **three separate text files**
- Starts with a **medium difficulty question**
- Adjusts the difficulty depending on whether the user answers correctly or incorrectly
- Assigns **different marks** depending on difficulty
- Saves the final results to a **result file**

The user **does not know the difficulty level** of the questions being asked.

---

## Adaptive Difficulty Logic

The quiz dynamically changes the difficulty based on the user's answer:

| Current Level | Correct Answer → Next | Wrong Answer → Next |
|---------------|----------------------|---------------------|
| Medium | Hard | Easy |
| Easy | Medium | Easy |
| Hard | Hard | Medium |

This creates a **performance-based adaptive testing system**.

---

## Question File Format

Each question file must contain questions in the following **tab-separated format**:

What is 2+2? a) 2 b) 3 c) 4 d) 5 c

easy.txt
medium.txt
hard.txt


Each line represents **one MCQ**.

---

## Marking Scheme

Different difficulty levels give different marks:

| Difficulty | Marks |
|-----------|------|
| Easy | 5 |
| Medium | 10 |
| Hard | 20 |

---

## Quiz Rules

- Total questions in the quiz: **10**
- Quiz starts with **Medium difficulty**
- Difficulty changes based on **user performance**
- If questions in a file are exhausted, the program **automatically switches to another available file**

---

## Result Storage

After the quiz finishes, the program saves results in a file.

---

## How to Run

Run the program using Python:

```bash
python adaptive_quiz.py
