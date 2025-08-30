# Students CGPA Management System

**Author:** Husnain Maroof  
**Date:** 8 Oct, 2025  

A **Python-based academic record management system** designed to calculate, analyze, and manage student **GPA and CGPA records** efficiently.  
The program reads student data from a file, computes semester GPA and overall CGPA, and provides multiple analysis options such as sorting, searching, filtering, and class statistics.

---

## Overview

This system processes student academic records stored in a file and performs the following tasks:

- Calculate **current semester GPA**
- Calculate **overall CGPA**
- Display all students with their academic statistics
- Sort students by GPA ranking
- Filter students within a GPA range
- Search student records
- Compute class averages
- Save updated results to a new file

The program uses **NumPy for numerical calculations** and **Colorama for colored terminal output**.

---

## Features

### 1. Student Record Loading
Student data is loaded from a file named: **students.txt**


---

## Menu Options

The system provides a **menu-driven interface** with the following features:

| Option | Description |
|------|-------------|
| 1 | View all students with their GPA and CGPA |
| 2 | Sort students by current semester GPA |
| 3 | Show students within a specific GPA range |
| 4 | Search for a student by name |
| 5 | Display class average GPA and CGPA |
| 6 | Save all results to a file |
| 7 | Exit the program |

---

## GPA Ranking

Students can be sorted in **descending order based on GPA**, allowing easy identification of top performers in the class.

---

## GPA Range Filtering

Users can filter students within a specific GPA range.


If the student exists, the full record will be displayed.

---

## Class Statistics

The program calculates:

- **Average GPA**
- **Average CGPA**

This provides an overview of the **overall academic performance of the class**.

---

## Saving Results

All processed student records can be saved to a file: **students_updated.txt**


---

## Technologies Used

- **Python**
- **NumPy** (numerical computation)
- **Colorama** (colored terminal interface)
- File Handling
- Lists and Dictionaries
- Menu-driven program design

---

## How to Run

Run the program using Python:

```bash
python cgpa_of_whole_class.py

