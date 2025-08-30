# This program is like used for online quizzes. It will pick
# MCQs from 3 different files labeled as# Easy, Medium and Hard. First MCQ
# should be from Medium file and if the user answers is wrong then next should
# come from easy otherwise from hard.This pattern should continue up till the
# end of the quiz. The user shouldn’t be aware of what difficulty level a particular MCQ belongs to.
# Each difficulty level have differentmarks.

def load_questions(file_name):
    'Load all questions from a text file into a list'
    questions = []
    with open(file_name, 'r') as f:
        for line in f:
            q = line.strip().split('\t')  # question + 4 options + answer
            if len(q) == 6:
                questions.append(q)
    return questions

def run_quiz():
    'Run the adaptive difficulty quiz with automatic file switching'
    total_correct = 0
    total_wrong = 0
    total_marks = 0
    total_questions = 10
    asked = 0
    # Load all questions
    questions_bank = {
        'easy.txt': load_questions('easy.txt'),
        'medium.txt': load_questions('medium.txt'),
        'hard.txt': load_questions('hard.txt')
    }
    # Track current index for each file
    indices = {'easy.txt': 0, 'medium.txt': 0, 'hard.txt': 0}

    # Marks for each difficulty
    marks = {'easy.txt': 5, 'medium.txt': 10, 'hard.txt': 20}

    # Start with medium
    current_file = 'medium.txt'

    while asked < total_questions:
        # If the current file is exhausted, switch to another available file
        available_files = [f for f in ['easy.txt', 'medium.txt', 'hard.txt'] if indices[f] < len(questions_bank[f])]
        if not available_files:
            print("All files are exhausted. Ending quiz.")
            break

        if indices[current_file] >= len(questions_bank[current_file]):
            # Switch to the next available file
            current_file = available_files[0]

        # Get the next question from current file
        q = questions_bank[current_file][indices[current_file]]
        indices[current_file] += 1

        # Display question
        print(f"\n{q[0]}")
        print(q[1])
        print(q[2])
        print(q[3])
        print(q[4])

        ans = input("Answer (a/b/c/d): ").strip().lower()

        # Check answer
        if ans == q[5].lower():
            print("Correct!")
            total_correct += 1
            total_marks += marks[current_file]

            # Adaptive difficulty: correct → harder
            if current_file == 'medium.txt' and 'hard.txt' in available_files:
                current_file = 'hard.txt'
            elif current_file == 'easy.txt' and 'medium.txt' in available_files:
                current_file = 'medium.txt'
            elif current_file == 'hard.txt':
                current_file = 'hard.txt'
        else:
            print(f"Wrong! Correct answer: {q[5]}")
            total_wrong += 1
            # Adaptive difficulty: wrong → easier
            if current_file == 'medium.txt' and 'easy.txt' in available_files:
                current_file = 'easy.txt'
            elif current_file == 'hard.txt' and 'medium.txt' in available_files:
                current_file = 'medium.txt'
            elif current_file == 'easy.txt':
                current_file = 'easy.txt'

        asked += 1
    # Save results
    with open("result.txt", "a") as f:
        f.write(f"Total Correct: {total_correct}\n")
        f.write(f"Total Wrong: {total_wrong}\n")
        f.write(f"Total Marks: {total_marks}\n\n")

    print("\n===== Quiz Finished =====")
    print("Results saved in result.txt")

# Main Program
if __name__ == "__main__":
    run_quiz() # Author: Husnain Maroof