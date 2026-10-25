"""
Quiz module data for AI Coding Tutor for C Programming.
Contains 12 comprehensive multiple-choice questions covering syntax, loops,
conditions, pointers, arrays, functions, memory management, and debugging.
"""

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Which of the following statements about C syntax and statements is correct?",
        "options": [
            "Every preprocessor directive like #include must end with a semicolon (;)",
            "Every normal C statement inside a function must terminate with a semicolon (;)",
            "Function definitions like int main() must end with a semicolon before the opening brace",
            "Semicolons are purely optional in modern C standards"
        ],
        "correct_answer": 1,
        "category": "Syntax",
        "explanation": "In C, statements (such as variable assignments, function calls, and return statements) must end with a semicolon. Preprocessor directives (#include, #define) do NOT end with a semicolon."
    },
    {
        "id": 2,
        "question": "What is the result of evaluating the condition in: if (score = 100) { ... } when score is initially 45?",
        "options": [
            "It produces a compile-time syntax error",
            "The condition evaluates to false because 45 does not equal 100",
            "The condition assigns 100 to score, evaluates to true (non-zero), and enters the if block",
            "The variable score remains 45 and the else block executes"
        ],
        "correct_answer": 2,
        "category": "Conditions & Logical Errors",
        "explanation": "In C, '=' is the assignment operator. The expression (score = 100) sets score to 100 and evaluates to 100. Any non-zero integer is treated as true in C, so the if-block always executes."
    },
    {
        "id": 3,
        "question": "Given the declaration int numbers[5] = {1, 2, 3, 4, 5};, what are the valid array index bounds?",
        "options": [
            "1 to 5",
            "0 to 5",
            "0 to 4",
            "-1 to 4"
        ],
        "correct_answer": 2,
        "category": "Arrays & Indexing",
        "explanation": "C arrays use zero-based indexing. An array of size N has valid indices from 0 up to N-1. For size 5, valid indices are 0, 1, 2, 3, and 4."
    },
    {
        "id": 4,
        "question": "What will be printed by the statement: printf(\"%d\\n\", 7 / 2); in C?",
        "options": [
            "3.5",
            "3",
            "4",
            "Compilation Error"
        ],
        "correct_answer": 1,
        "category": "Arithmetic & Type Conversion",
        "explanation": "Because both 7 and 2 are integer literals, C executes integer division. Integer division truncates any fractional portion toward zero, producing 3."
    },
    {
        "id": 5,
        "question": "Why is it dangerous to write into an uninitialized pointer like int *p; *p = 50;?",
        "options": [
            "The compiler will automatically convert the pointer into an array",
            "The pointer holds a random memory address (wild pointer) and dereferencing it causes memory corruption or a crash",
            "It will only print a warning and automatically allocate 4 bytes on the heap",
            "C initializes all pointers to a safe buffer automatically"
        ],
        "correct_answer": 1,
        "category": "Pointers",
        "explanation": "Local pointer variables contain indeterminate garbage memory addresses upon declaration. Dereferencing an uninitialized pointer attempts to read or write to random memory, causing a segmentation fault or undefined behavior."
    },
    {
        "id": 6,
        "question": "What does dereferencing a NULL pointer (e.g., int *ptr = NULL; printf(\"%d\", *ptr);) typically cause?",
        "options": [
            "It prints 0 safely",
            "It allocates memory automatically at address 0",
            "An immediate runtime crash, typically a Segmentation Fault or Access Violation",
            "It returns the memory address of the operating system"
        ],
        "correct_answer": 2,
        "category": "Pointers & Memory",
        "explanation": "Address 0 (NULL) is designated as invalid and protected by the operating system's memory management unit. Attempting to read or write at address 0 triggers a CPU page fault, crashing the program."
    },
    {
        "id": 7,
        "question": "When reading an integer from user input with scanf, which code snippet is correct?",
        "options": [
            "scanf(\"%d\", age);",
            "scanf(\"%d\", &age);",
            "scanf(\"%f\", age);",
            "scanf(\"int\", &age);"
        ],
        "correct_answer": 1,
        "category": "Input / Output",
        "explanation": "scanf requires the memory address of the variable where the scanned data should be stored. For non-pointer scalar variables like int, the address-of operator '&' is mandatory."
    },
    {
        "id": 8,
        "question": "What occurs when dynamically allocated memory with malloc() is never passed to free()?",
        "options": [
            "The operating system immediately terminates the program",
            "A memory leak occurs, meaning heap memory remains occupied until the program terminates",
            "malloc() automatically frees memory when leaving the function scope",
            "The program automatically switches to stack allocation"
        ],
        "correct_answer": 1,
        "category": "Memory Management",
        "explanation": "Heap memory allocated via malloc() or calloc() persists across function calls and scopes. If not released with free(), that memory remains leaked, which can degrade system performance over time."
    },
    {
        "id": 9,
        "question": "What is the primary cause of an infinite loop in a while loop?",
        "options": [
            "Using braces {} around the loop body",
            "Failing to update the loop control condition variable inside the loop body",
            "Declaring the variable outside the while loop",
            "Using a condition with more than two comparisons"
        ],
        "correct_answer": 1,
        "category": "Loops & Control Flow",
        "explanation": "A while loop repeats as long as its condition remains true. If the variables governing that condition are never modified towards the termination state within the loop, the loop runs endlessly."
    },
    {
        "id": 10,
        "question": "What happens if a non-void function in C (e.g., int calculate(int x)) fails to execute a return statement?",
        "options": [
            "The compiler always replaces the missing value with 0",
            "The function returns undefined / garbage data found in the CPU return register",
            "The program halts and prompts the user to enter a return number",
            "The function automatically changes its signature to void"
        ],
        "correct_answer": 1,
        "category": "Functions",
        "explanation": "Under the C standard, reaching the closing brace of a value-returning function without an explicit return statement results in Undefined Behavior. The caller receives whatever indeterminate data happens to reside in the return register."
    },
    {
        "id": 11,
        "question": "What does the GCC compiler flag '-Wall' do?",
        "options": [
            "It builds a security wall that prevents malicious memory exploits",
            "It enables all commonly recommended compiler warnings to help catch potential bugs",
            "It turns off all warnings so the code compiles faster",
            "It formats the code according to the GNU style guide"
        ],
        "correct_answer": 1,
        "category": "Compiler & Debugging",
        "explanation": "The '-Wall' flag instructs GCC to enable a broad set of useful warnings, alerting you to uninitialized variables, unused variables, misplaced semicolons, and operator precedence risks before runtime."
    },
    {
        "id": 12,
        "question": "What is the difference between single '&' and double '&&' in C?",
        "options": [
            "'&' is logical AND; '&&' is bitwise AND",
            "'&' is bitwise AND (or address-of); '&&' is logical AND with short-circuit evaluation",
            "'&' is used for floats; '&&' is used for integers",
            "There is no difference in modern C compilers"
        ],
        "correct_answer": 1,
        "category": "Operators",
        "explanation": "Single '&' performs bitwise AND between binary representations (or extracts an address when used as a unary prefix). Double '&&' evaluates logical truth values with short-circuit evaluation."
    }
]

def get_all_quiz_questions():
    """Returns the 12 quiz questions without exposing the correct answer to the client directly."""
    sanitized = []
    for q in QUIZ_QUESTIONS:
        sanitized.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "category": q["category"]
        })
    return sanitized

def grade_quiz(answers):
    """
    Evaluates submitted answers.
    answers: dict mapping question id (str or int) to selected option index (int).
    Returns score, total, percentage, and detailed feedback per question.
    """
    score = 0
    total = len(QUIZ_QUESTIONS)
    results = []

    for q in QUIZ_QUESTIONS:
        qid_str = str(q["id"])
        selected = answers.get(qid_str)
        if selected is not None:
            try:
                selected = int(selected)
            except (ValueError, TypeError):
                selected = -1
        else:
            selected = -1

        is_correct = (selected == q["correct_answer"])
        if is_correct:
            score += 1

        results.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "selected_option": selected,
            "correct_option": q["correct_answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"],
            "category": q["category"]
        })

    percentage = round((score / total) * 100, 1)
    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "results": results
    }
