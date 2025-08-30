# ----------------------------------------------------------
# Students CGPA Management System
# Author: Husnain Maroof
# Date: 8 Oct, 2025
# Description: A Python program to calculate, sort, and manage 
# student GPA and CGPA records efficiently.
# ----------------------------------------------------------

import numpy as np
import sys
from colorama import Fore, Style, init
## Initialize colorama
init(autoreset=True)
grade_mapping = {
        'A': 4.0,
        'A-': 3.7,
        'B+': 3.3,
        'B': 3.0,
        'B-': 2.7,
        'C+': 2.3,
        'C': 2.0,
        'C-': 1.7,
        'D+': 1.3,
        'D': 1.0,
        'D-': 0.7,
        'F': 0.0
    }  
        
def show_menu():
    """Display the main menu of the Student CGPA Management System."""
    print(Fore.CYAN + Style.BRIGHT + "\n========= STUDENT CGPA MANAGEMENT SYSTEM =========")
    print(Style.BRIGHT + "Please choose an option:\n")
    print(Fore.YELLOW + "1." + Style.RESET_ALL + " View all students with their GPA and CGPA")
    print(Fore.YELLOW + "2." + Style.RESET_ALL + " Sort students by current semester GPA (High → Low)")
    print(Fore.YELLOW + "3." + Style.RESET_ALL + " Show students within a specific GPA range")
    print(Fore.YELLOW + "4." + Style.RESET_ALL + " Search for a student by name")
    print(Fore.YELLOW + "5." + Style.RESET_ALL + " Show class average GPA and CGPA")
    print(Fore.YELLOW + "6." + Style.RESET_ALL + " Save all results to a file")
    print(Fore.YELLOW + "7." + Style.RESET_ALL + Fore.RED+ " Exit")
    print(Fore.CYAN + "==================================================")
         
def load_all_students(file_name):
    """Load student data from file and return a list of students records."""
    all_students = []
    try:
        file = open(file_name, 'r')
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found. Please check the filename or path.")
    except PermissionError:
        print(f"Error: Permission denied while accessing '{file_name}'.")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
    else:
        for student in file:
            student = student.strip()
            if not student or student.startswith('#'):
                continue
            data = [d.strip() for d in student.split(',')]
            all_students.append(data)
    finally:
        if 'file' in locals() and not file.closed:
            file.close()
    return all_students

def calculate_gpa(mapping, grades, credit_hours):
    """Calculate GPA from grades and credit hours."""
    ## gpa = total_grade_points / total_credit_hours  
    valid_indices = [i for i, g in enumerate(grades) if g in mapping]
    if not valid_indices:
        return 0.0
    gpa_values = np.array([mapping[grades[i]] for i in valid_indices])
    credit_hours = np.array([float(credit_hours[i]) for i in valid_indices])
    total_gpoints = np.sum(gpa_values * credit_hours)
    total_credits = np.sum(credit_hours)
    return round(total_gpoints / total_credits, 2) if total_credits else 0.0

def calculate_cgpa(prev_cgpa, prev_credit_hours, current_gpa, current_credit_hours):
    """Calculate cumulative CGPA using previous CGPA and current semester GPA."""
    ## New CGPA= (Prev CGPA×Prev Credits)+(Semester GPA×Semester Credits)/(Prev Credits + Semester Credits)
    if prev_credit_hours + current_credit_hours == 0:
        return 0.0
    cgpa = ((prev_cgpa * prev_credit_hours) + (current_gpa * current_credit_hours))\
        /(prev_credit_hours + current_credit_hours)
    return round(cgpa, 2)  
  
def store_students_cgpa(all_students):
    """Compute and return a list of all students' CGPAs."""
    students_cgpa = []
    for student in all_students:
        gpa = calculate_gpa(grade_mapping, student[3:11], student[11:])
        current_credits = sum([float(ch) for ch in student[11:]])
        cgpa = calculate_cgpa(float(student[1]), float(student[2]), gpa, current_credits)
        students_cgpa.append(cgpa)
    return students_cgpa 

def store_students_gpa(all_students):
    """Compute and return a list of all students' GPAs."""
    students_gpa = []
    for student in all_students:
        gpa = calculate_gpa(grade_mapping, student[3:11], student[11:])
        students_gpa.append(gpa)
    return students_gpa    
            
def disp_gpa_cgpa(all_students, students_gpa, students_cgpa):
    """Display all students with their current GPA and overall CGPA."""
    print("\n" + "-" * 65)
    print(f"{'Sr#':<5}{'Name':<20}{'Current GPA':>15}{'Overall CGPA':>15}")
    print("-" * 65)
    for idx, student in enumerate(all_students):
        print(f"{idx+1:<5}{student[0]:<20}{students_gpa[idx]:>15.2f}{students_cgpa[idx]:>15.2f}")
        
def disp_gpa_ranking(all_students, mapping, students_gpa, students_cgpa):
    """Display students sorted by GPA in descending order."""
    s = sorted(all_students, key = lambda x: calculate_gpa(mapping, x[3:11], x[11:]), reverse = True)
    gpas = sorted(students_gpa,reverse = True)
    cgpas = sorted(students_cgpa,reverse = True)
    disp_gpa_cgpa(s, gpas, cgpas)

def filter_by_gpa_range(all_students, students_gpa, start, end):
    """Display students whose GPA falls within the given range."""
    found = False
    print(f"\n{'='*70}")
    print(f"Students with Current GPA between {start} and {end}")
    print(f"{'-'*70}")
    print(f"{'No.':<5}{'Name':<20}{'Current GPA':>15}")
    print(f"{'-'*70}")
    for idx, student in enumerate(all_students):
        gpa = students_gpa[idx]
        if start<= gpa and gpa <= end:
            found = True
            print(f"{idx+1:<5}{student[0]:<20}{gpa:>15.2f}")
    if not found:
        print('No student found with specified gpa range.')   
    print(f"{'='*70}")
                 
def disp_student_details(all_students, name):
    """Display details of a specific student by name."""
    found = False
    for student in all_students:
        if name.lower() == student[0].lower():
            found = True 
            print('\t'.join(student))  
    if not found:
        print(f'No such student is found with name: {name}')
        
def avg_gpa_cgpa(students_gpa, students_cgpa):
    """Display class average GPA and CGPA."""
    print("\n" + "-" * 40)
    print(f"{'Class GPA Summary':^40}")
    print("-" * 40)
    print(f"{'Average GPA:':<25}{np.mean(students_gpa):>10.2f}")
    print(f"{'Average CGPA:':<25}{np.mean(students_cgpa):>10.2f}")
    print("-" * 40)
    
def store_results(all_students, students_gpa, students_cgpa):
    """Save all student records (as tab-separated rows) to a text file."""
    with open('students_updated.txt', 'w', newline='') as file:
        # Write header
        header = [
            "Name", "Prev_CGPA", "Prev_Credit_Hours",
            "Grades", "Credit_Hours", "Current_GPA", "Overall_CGPA"
        ]
        file.write('\t'.join(header) + '\n')

        for idx, student in enumerate(all_students):
            name = student[0]
            prev_cgpa = student[1]
            prev_credits = student[2]
            grades = ', '.join(student[3:11])
            credits = ', '.join(student[11:])
            current_gpa = students_gpa[idx]
            overall_cgpa = students_cgpa[idx]
            # Create a list (one full row)
            row = [
                name, prev_cgpa, prev_credits, grades, credits,
                f"{current_gpa:.2f}", f"{overall_cgpa:.2f}"
            ]
            # Write row as tab-separated line
            file.write(f"{name:<20}{prev_cgpa:<10}{prev_credits:<10}{grades:<30}{credits:<20}{current_gpa:<10}{overall_cgpa:<10}\n")
    print("Results stored successfully in 'students_updated.txt'.")
                
## Main Program
if __name__ == '__main__':
    all_students = load_all_students('students.txt')  
    if not all_students:
        print(Fore.RED + "No student data loaded. Program exiting..." + Style.RESET_ALL)
        sys.exit()
    students_cgpa = store_students_cgpa(all_students)  
    students_gpa = store_students_gpa(all_students)
    show_menu()   
    while True:
        try:
            user_choice = int(input(Fore.RED+Style.NORMAL+'Enter your choice (1-7): '+Style.RESET_ALL))
        except ValueError:
            print('Enter numeric value only.') 
            continue
        if user_choice not in range(1, 8):
            print('Enter within 1 and 7 only. Try Again.')
            continue
        if user_choice == 7:
            print(Fore.CYAN+'Thanks for your time. Come again.'+Style.RESET_ALL)
            break
        if user_choice == 1:
            disp_gpa_cgpa(all_students, students_gpa, students_cgpa)
        elif user_choice == 2:
            disp_gpa_ranking(all_students, grade_mapping, students_gpa, students_cgpa)
        elif user_choice == 3:
            try:
                start, end = map(float, input("Enter min and max GPA separated by comma: ").split(','))
            except ValueError:
                print('Please enter two numbers separated by a comma, like: 2.5,3.3')
                continue
            filter_by_gpa_range(all_students, students_gpa, start, end)
        elif user_choice == 4:
            name = input('Enter name of student: ').strip()   
            if not name.replace(' ','').isalpha() or len(name)<3:
                print('Enter name only!')
                continue 
            disp_student_details(all_students, name) 
        elif user_choice == 5:
            avg_gpa_cgpa(students_gpa, students_cgpa)   
        else:
            store_results(all_students, students_gpa, students_cgpa) 
                
            
            
                
            
        
           

           
            