"""
Buggy C Program Library for AI Coding Tutor.
Contains 15 beginner-level educational buggy C programs covering syntax,
logical errors, runtime crashes, undefined behavior, pointers, and memory leaks.
"""

BUGGY_PROGRAMS = [
    {
        "id": 1,
        "title": "Missing Semicolon in Statement",
        "category": "Syntax Error", 
        "difficulty": "Beginner",
        "expected_bug_type": "Syntax Error",
        "line_number": 6,
        "buggy_code": """#include <stdio.h>

int main() {
    int age = 19;
    printf("Welcome to C programming!\\n")
    printf("Your age is: %d\\n", age);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    int age = 19;
    printf("Welcome to C programming!\\n");
    printf("Your age is: %d\\n", age);
    return 0;
}""",
        "simple_explanation": "In C, every executable statement must terminate with a semicolon (;). Line 5 (or statement on line 5) is missing its closing semicolon, causing the compiler to flag a syntax error on line 6.",
        "why_error_occurs": "The C compiler relies on semicolons as statement terminators to parse tokens into complete grammatical sentences. Without a semicolon, the compiler thinks `printf(...)` continues into the next token.",
        "hints": {
            "level1": "Inspect the line endings inside `main()`. Does every statement end with the standard C statement terminator?",
            "level2": "Look closely at line 5: `printf(\"Welcome to C programming!\\n\")`. What symbol is missing before moving to line 6?",
            "level3": "Add a semicolon `;` at the end of line 5: `printf(\"Welcome to C programming!\\n\");`."
        },
        "sample_input": "None (No user input required)",
        "sample_output": "Welcome to C programming!\nYour age is: 19",
        "learning_takeaway": "In C, statements do not automatically end at line breaks. Always check semicolons when GCC outputs `expected ';' before ...`."
    },
    {
        "id": 2,
        "title": "Incorrect Variable Declaration & Type Mismatch",
        "category": "Syntax / Semantic Error",
        "difficulty": "Beginner",
        "expected_bug_type": "Variable Declaration Error",
        "line_number": 5,
        "buggy_code": """#include <stdio.h>

int main() {
    // Attempting to declare a variable without a data type
    count = 10;
    printf("Total items: %d\\n", count);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    // Properly declare the variable with an integer data type
    int count = 10;
    printf("Total items: %d\\n", count);
    return 0;
}""",
        "simple_explanation": "The variable `count` is assigned a value before it has been declared with a data type like `int`.",
        "why_error_occurs": "C is a statically typed language. The compiler must allocate specific memory (e.g., 4 bytes for an integer) and therefore needs to know the type before any identifier is used.",
        "hints": {
            "level1": "Has the variable `count` been introduced to the compiler with its storage type?",
            "level2": "Check line 5. You assigned `count = 10;`, but C requires declaring the type (like `int`, `float`, or `char`) first.",
            "level3": "Change line 5 from `count = 10;` to `int count = 10;` to declare and initialize it simultaneously."
        },
        "sample_input": "None",
        "sample_output": "Total items: 10",
        "learning_takeaway": "Variables in C must be explicitly declared with a type before usage. Undeclared identifiers trigger `error: 'count' undeclared`."
    },
    {
        "id": 3,
        "title": "Incorrect if Condition (Assignment vs Equality)",
        "category": "Logical Error",
        "difficulty": "Beginner",
        "expected_bug_type": "Logical Error",
        "line_number": 6,
        "buggy_code": """#include <stdio.h>

int main() {
    int score = 45;
    // Bug: '=' assigns 100 instead of comparing with '=='
    if (score = 100) {
        printf("Perfect score! You passed with honors.\\n");
    } else {
        printf("Keep practicing!\\n");
    }
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    int score = 45;
    // Correct: '==' checks for equality
    if (score == 100) {
        printf("Perfect score! You passed with honors.\\n");
    } else {
        printf("Keep practicing!\\n");
    }
    return 0;
}""",
        "simple_explanation": "The `if` condition uses the single equals sign `=` (assignment) rather than the double equals `==` (equality test). As a result, `score` is overwritten with 100 and the condition evaluates as true (non-zero).",
        "why_error_occurs": "In C, an assignment expression `(score = 100)` evaluates to the assigned value (100). Any non-zero numeric value in C is considered logically TRUE, so the `if` block always executes regardless of the original score.",
        "hints": {
            "level1": "Notice that the output says 'Perfect score' even though score is initialized to 45. Is the condition checking equality or performing an assignment?",
            "level2": "Look at the operator inside `if (score = 100)`. In C, `=` is for assignment and `==` is for comparison.",
            "level3": "Replace `score = 100` with `score == 100` on line 6."
        },
        "sample_input": "None",
        "sample_output": "Keep practicing!",
        "learning_takeaway": "A single `=` assigns values; double `==` compares values. Enable GCC warning `-Wparentheses` to catch accidental assignments."
    },
    {
        "id": 4,
        "title": "Off-by-One Loop Error in Array Traversal",
        "category": "Logical / Boundary Error",
        "difficulty": "Beginner",
        "expected_bug_type": "Array Boundary Error",
        "line_number": 7,
        "buggy_code": """#include <stdio.h>

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    int sum = 0;
    // Bug: loop condition 'i <= 5' runs 6 times for a 5-element array
    for (int i = 0; i <= 5; i++) {
        sum += numbers[i];
    }
    printf("Calculated sum: %d\\n", sum);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    int sum = 0;
    // Correct: loop condition 'i < 5' visits indices 0, 1, 2, 3, 4
    for (int i = 0; i < 5; i++) {
        sum += numbers[i];
    }
    printf("Calculated sum: %d\\n", sum);
    return 0;
}""",
        "simple_explanation": "The array has 5 elements, which are indexed from 0 to 4. The loop condition `i <= 5` allows `i` to reach 5, accessing `numbers[5]` which is outside the array boundary.",
        "why_error_occurs": "C arrays are 0-indexed. An array of size N has indices 0 through N-1. Accessing `numbers[5]` accesses unallocated memory containing unpredictable garbage values.",
        "hints": {
            "level1": "How many items are in `numbers`? What is the index of the very last element in a 5-item C array?",
            "level2": "Check line 7: `for (int i = 0; i <= 5; i++)`. When `i == 5`, does `numbers[5]` exist?",
            "level3": "Change the loop condition from `i <= 5` to `i < 5` so the loop terminates after index 4."
        },
        "sample_input": "None",
        "sample_output": "Calculated sum: 150",
        "learning_takeaway": "C arrays of size N have valid indices 0 to N-1. Always use `< N` when iterating through an array starting at 0."
    },
    {
        "id": 5,
        "title": "Infinite Loop Due to Missing State Update",
        "category": "Logical Error",
        "difficulty": "Beginner",
        "expected_bug_type": "Infinite Loop Error",
        "line_number": 6,
        "buggy_code": """#include <stdio.h>

int main() {
    int counter = 1;
    // Bug: counter is never incremented, so counter <= 5 is always true
    while (counter <= 5) {
        printf("Iteration: %d\\n", counter);
        // Missing counter increment!
    }
    printf("Loop finished!\\n");
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    int counter = 1;
    // Correct: counter is incremented inside the loop body
    while (counter <= 5) {
        printf("Iteration: %d\\n", counter);
        counter++;
    }
    printf("Loop finished!\\n");
    return 0;
}""",
        "simple_explanation": "The `while` loop checks `counter <= 5`, but inside the loop body, `counter` is never modified. It remains 1 forever, resulting in an infinite loop.",
        "why_error_occurs": "A `while` loop requires its control condition variables to eventually change towards the termination state. Without `counter++`, the condition is constantly true.",
        "hints": {
            "level1": "What happens to the variable `counter` while the loop is executing?",
            "level2": "The loop body prints `counter`, but does not change its value. How will `counter <= 5` ever become false?",
            "level3": "Add `counter++;` (or `counter = counter + 1;`) inside the `while` block after the `printf` statement."
        },
        "sample_input": "None",
        "sample_output": "Iteration: 1\nIteration: 2\nIteration: 3\nIteration: 4\nIteration: 5\nLoop finished!",
        "learning_takeaway": "Every loop must make progress toward its exit condition on every iteration. Always ensure loop control variables are updated."
    },
    {
        "id": 6,
        "title": "Incorrect Loop Boundary (Wrong Decrement Direction)",
        "category": "Logical / Boundary Error",
        "difficulty": "Beginner",
        "expected_bug_type": "Logical Loop Error",
        "line_number": 5,
        "buggy_code": """#include <stdio.h>

int main() {
    // Countdown from 5 down to 1
    // Bug: loop increments 'i++' while condition is 'i > 0' starting at 5
    for (int i = 5; i > 0; i++) {
        printf("%d... ", i);
        if (i > 10) { // Safety break to prevent freeze in demonstration
            printf("\\nStopped runaway loop!\\n");
            break;
        }
    }
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    // Correct: loop decrements 'i--' to count down to 1
    for (int i = 5; i > 0; i--) {
        printf("%d... ", i);
    }
    printf("Blastoff!\\n");
    return 0;
}""",
        "simple_explanation": "To count down from 5 to 1, the variable `i` should be decremented with `i--`. Using `i++` causes `i` to grow larger (5, 6, 7...), moving further away from 0.",
        "why_error_occurs": "The condition tests `i > 0`. Because 5 is greater than 0, and incrementing `i` makes it even greater, the loop will never reach 0 naturally.",
        "hints": {
            "level1": "Look at the direction of the loop step. Are we counting upwards or downwards?",
            "level2": "Line 5 starts `i = 5` and tests `i > 0`, but the step expression is `i++`. What operator decreases a variable by 1?",
            "level3": "Change the step expression from `i++` to `i--` in the `for` statement header."
        },
        "sample_input": "None",
        "sample_output": "5... 4... 3... 2... 1... Blastoff!",
        "learning_takeaway": "Ensure the loop direction (increment vs decrement) aligns with the termination condition."
    },
    {
        "id": 7,
        "title": "Integer Division Truncation Mistake",
        "category": "Logical / Arithmetic Error",
        "difficulty": "Beginner",
        "expected_bug_type": "Arithmetic Truncation Error",
        "line_number": 7,
        "buggy_code": """#include <stdio.h>

int main() {
    int total_marks = 450;
    int max_marks = 500;
    // Bug: total_marks / max_marks is integer division (450 / 500 = 0)
    float percentage = (total_marks / max_marks) * 100;
    printf("Percentage: %.2f%%\\n", percentage);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    int total_marks = 450;
    int max_marks = 500;
    // Correct: cast one operand to float to trigger floating-point division
    float percentage = ((float)total_marks / max_marks) * 100;
    printf("Percentage: %.2f%%\\n", percentage);
    return 0;
}""",
        "simple_explanation": "Both `total_marks` and `max_marks` are integers. In C, dividing an integer by an integer performs integer division which drops the fractional part (450 / 500 = 0), yielding 0.00%.",
        "why_error_occurs": "Type rules in C determine operation types based on operands, not the receiving variable type. Even though `percentage` is a `float`, `(total_marks / max_marks)` finishes integer division before assignment.",
        "hints": {
            "level1": "Why does the calculation output `0.00%` when 450 / 500 should be 0.9?",
            "level2": "In C, `int / int` produces an `int`. How can you tell the compiler to perform a floating-point division?",
            "level3": "Typecast either operand to float: `((float)total_marks / max_marks) * 100` or multiply by `100.0` first."
        },
        "sample_input": "None",
        "sample_output": "Percentage: 90.00%",
        "learning_takeaway": "Dividing two integers in C always discards fractions. Use explicit type casting `(float)a / b` when decimals are required."
    },
    {
        "id": 8,
        "title": "Incorrect Operator Usage (Bitwise & vs Logical &&)",
        "category": "Logical Error",
        "difficulty": "Beginner",
        "expected_bug_type": "Logical Operator Error",
        "line_number": 7,
        "buggy_code": """#include <stdio.h>

int main() {
    int has_id = 1;      // 0001 in binary
    int is_registered = 2; // 0010 in binary
    // Bug: single '&' is bitwise AND, so 1 & 2 evaluates to 0 (False)
    if (has_id & is_registered) {
        printf("Access granted to the examination hall.\\n");
    } else {
        printf("Access denied!\\n");
    }
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    int has_id = 1;
    int is_registered = 2;
    // Correct: double '&&' is logical AND
    if (has_id && is_registered) {
        printf("Access granted to the examination hall.\\n");
    } else {
        printf("Access denied!\\n");
    }
    return 0;
}""",
        "simple_explanation": "The condition uses the bitwise AND operator `&` instead of the logical AND operator `&&`. Because bitwise `1 & 2` is `0`, the student is denied access even though both flags are true (non-zero).",
        "why_error_occurs": "`&` performs binary bit-by-bit conjunction. Binary `0001 & 0010` produces `0000` (zero, which C interprets as false). Logical `&&` checks whether both truth values are non-zero.",
        "hints": {
            "level1": "Both variables are non-zero (true), yet access is denied. What operator is being used to combine them?",
            "level2": "Notice the single `&` on line 7. Single `&` is bitwise AND; what operator is used for boolean logical AND?",
            "level3": "Replace `has_id & is_registered` with `has_id && is_registered` on line 7."
        },
        "sample_input": "None",
        "sample_output": "Access granted to the examination hall.",
        "learning_takeaway": "Use `&&` for boolean logical AND conditions, and reserve single `&` for bitwise operations or pointer addresses."
    },
    {
        "id": 9,
        "title": "Array Out-of-Bounds Write (Buffer Overrun)",
        "category": "Runtime / Undefined Behavior",
        "difficulty": "Intermediate",
        "expected_bug_type": "Buffer Overflow / Out-of-Bounds Error",
        "line_number": 7,
        "buggy_code": """#include <stdio.h>

int main() {
    int scores[3] = {85, 90, 78};
    // Bug: Valid indices are 0, 1, 2. Writing to scores[3] corrupts adjacent stack memory
    scores[3] = 95;
    printf("Third score: %d\\n", scores[2]);
    printf("Illegal access score[3]: %d\\n", scores[3]);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    // Correct: Allocate enough space for 4 items if index 3 is needed
    int scores[4] = {85, 90, 78, 95};
    printf("Third score: %d\\n", scores[2]);
    printf("Fourth score: %d\\n", scores[3]);
    return 0;
}""",
        "simple_explanation": "An array declared as `scores[3]` has room for exactly 3 integers: `scores[0]`, `scores[1]`, and `scores[2]`. Assigning to `scores[3]` writes past the allocated boundary.",
        "why_error_occurs": "C does not perform automatic array bounds checking at compile-time or runtime. Writing out of bounds triggers Undefined Behavior, which can corrupt the stack or cause segmentation faults.",
        "hints": {
            "level1": "Examine the size specified in the declaration of `scores`. How many elements can it hold?",
            "level2": "Index 3 represents the 4th element, but the array is only declared with size 3 (`scores[3]`).",
            "level3": "Increase the array size declaration to `int scores[4]` or avoid accessing index 3."
        },
        "sample_input": "None",
        "sample_output": "Third score: 78\nFourth score: 95",
        "learning_takeaway": "C does not check array bounds. Writing beyond the boundary corrupts adjacent memory and causes elusive bugs."
    },
    {
        "id": 10,
        "title": "Uninitialized Variable Usage (Garbage Value)",
        "category": "Runtime / Undefined Behavior",
        "difficulty": "Beginner",
        "expected_bug_type": "Uninitialized Variable Error",
        "line_number": 5,
        "buggy_code": """#include <stdio.h>

int main() {
    // Bug: 'accumulator' is declared but never initialized to 0
    int accumulator;
    for (int i = 1; i <= 5; i++) {
        accumulator += i;
    }
    printf("Sum from 1 to 5 is: %d\\n", accumulator);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    // Correct: Initialize accumulator to 0 before accumulating
    int accumulator = 0;
    for (int i = 1; i <= 5; i++) {
        accumulator += i;
    }
    printf("Sum from 1 to 5 is: %d\\n", accumulator);
    return 0;
}""",
        "simple_explanation": "The variable `accumulator` is used in `accumulator += i` without having an initial value set. In C, local variables hold whatever garbage data was previously in that memory location.",
        "why_error_occurs": "In C, local automatic variables are not zero-initialized by default. Reading an uninitialized local variable invokes undefined behavior and yields random garbage numbers.",
        "hints": {
            "level1": "What initial value does `accumulator` have before the loop starts adding to it?",
            "level2": "Look at line 5: `int accumulator;`. Because no initial value is provided, it contains random stack garbage.",
            "level3": "Initialize `accumulator` to 0 on line 5: `int accumulator = 0;`."
        },
        "sample_input": "None",
        "sample_output": "Sum from 1 to 5 is: 15",
        "learning_takeaway": "Always initialize variables before using them in calculations. Local variables in C default to indeterminate garbage values."
    },
    {
        "id": 11,
        "title": "Incorrect Pointer Usage (Wild / Unassigned Pointer)",
        "category": "Pointer Error",
        "difficulty": "Intermediate",
        "expected_bug_type": "Wild Pointer Dereference",
        "line_number": 6,
        "buggy_code": """#include <stdio.h>

int main() {
    // Bug: ptr is a wild pointer; it holds an arbitrary address
    int *ptr;
    *ptr = 42; // Writing to random unassigned memory!
    printf("Value: %d\\n", *ptr);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    // Correct: Point ptr to the address of a valid allocated variable
    int value = 0;
    int *ptr = &value;
    *ptr = 42;
    printf("Value: %d\\n", *ptr);
    return 0;
}""",
        "simple_explanation": "A pointer variable `ptr` was declared without being initialized to point to any valid memory address. Dereferencing it with `*ptr = 42` attempts to write to an arbitrary memory address.",
        "why_error_occurs": "Pointers store memory addresses. When uninitialized, `ptr` holds a random bit pattern (wild pointer). Attempting to dereference it usually results in an OS crash (segmentation fault) or memory corruption.",
        "hints": {
            "level1": "Where does `ptr` point? Has it been given the address of any existing integer variable?",
            "level2": "Line 5 declares `int *ptr;` but doesn't point it to anything using the address-of operator `&`.",
            "level3": "Declare an `int target;` and initialize `ptr` with `&target` before assigning `*ptr = 42;`."
        },
        "sample_input": "None",
        "sample_output": "Value: 42",
        "learning_takeaway": "Never dereference an uninitialized pointer. Always initialize pointers to a valid address or `NULL`."
    },
    {
        "id": 12,
        "title": "Null Pointer Dereference (Segmentation Fault)",
        "category": "Pointer Error",
        "difficulty": "Intermediate",
        "expected_bug_type": "Null Pointer Dereference",
        "line_number": 7,
        "buggy_code": """#include <stdio.h>

int main() {
    int *ptr = NULL;
    // Bug: Dereferencing NULL pointer without checking if it is valid
    printf("Attempting to access pointer value...\\n");
    printf("Value is: %d\\n", *ptr);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    int actual_val = 100;
    int *ptr = &actual_val;
    // Correct: Check if pointer is non-null before dereferencing
    printf("Attempting to access pointer value...\\n");
    if (ptr != NULL) {
        printf("Value is: %d\\n", *ptr);
    } else {
        printf("Error: Pointer is NULL!\\n");
    }
    return 0;
}""",
        "simple_explanation": "The pointer `ptr` is set to `NULL` (address 0x0). The program then tries to read `*ptr`, which causes an immediate crash / Segmentation Fault.",
        "why_error_occurs": "`NULL` points to address 0, which is protected by the operating system virtual memory management. Dereferencing NULL triggers a CPU page fault exception.",
        "hints": {
            "level1": "What value was assigned to `ptr` on line 4? Can you read data from address 0?",
            "level2": "Line 4 explicitly set `ptr = NULL;`. Dereferencing `*ptr` on line 7 causes a segmentation fault.",
            "level3": "Point `ptr` to a valid variable address (e.g. `int x = 100; ptr = &x;`) and guard access with `if (ptr != NULL)`."
        },
        "sample_input": "None",
        "sample_output": "Attempting to access pointer value...\nValue is: 100",
        "learning_takeaway": "Always verify that a pointer is not `NULL` before attempting to read or write through it."
    },
    {
        "id": 13,
        "title": "Incorrect Function Return Value & Missing Return",
        "category": "Function / Semantic Error",
        "difficulty": "Beginner",
        "expected_bug_type": "Missing Return Value Error",
        "line_number": 7,
        "buggy_code": """#include <stdio.h>

// Bug: Function declares return type 'int' but fails to return any value
int calculate_cube(int n) {
    int result = n * n * n;
    // Missing 'return result;'
}

int main() {
    int ans = calculate_cube(3);
    printf("Cube of 3 is: %d\\n", ans);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

// Correct: Function returns the computed integer
int calculate_cube(int n) {
    int result = n * n * n;
    return result;
}

int main() {
    int ans = calculate_cube(3);
    printf("Cube of 3 is: %d\\n", ans);
    return 0;
}""",
        "simple_explanation": "The function `calculate_cube` has return type `int`, but it reaches the end of its body without returning a value.",
        "why_error_occurs": "In C, reaching the end of a non-void function without a `return` statement leaves the CPU register (e.g., EAX/RAX) with indeterminate data, producing undefined behavior.",
        "hints": {
            "level1": "What is the return type of `calculate_cube`? Does the function actually pass anything back to `main`?",
            "level2": "The function signature is `int calculate_cube(int n)`, but the function body is missing a `return` keyword.",
            "level3": "Add `return result;` at the end of the `calculate_cube` function before the closing brace."
        },
        "sample_input": "None",
        "sample_output": "Cube of 3 is: 27",
        "learning_takeaway": "If a function specifies a non-void return type, every control path must conclude with a `return` statement."
    },
    {
        "id": 14,
        "title": "Memory Allocation & Missing Deallocation (Memory Leak)",
        "category": "Memory Management",
        "difficulty": "Intermediate",
        "expected_bug_type": "Memory Leak / Allocation Error",
        "line_number": 9,
        "buggy_code": """#include <stdio.h>
#include <stdlib.h>

void process_data() {
    // Allocate 100 integers on the heap
    int *buffer = (int *)malloc(100 * sizeof(int));
    if (buffer == NULL) return;
    buffer[0] = 42;
    printf("Processed value: %d\\n", buffer[0]);
    // Bug: Missing free(buffer); heap memory is leaked when function exits!
}

int main() {
    process_data();
    printf("Data processed successfully.\\n");
    return 0;
}""",
        "clean_code": """#include <stdio.h>
#include <stdlib.h>

void process_data() {
    // Allocate 100 integers on the heap
    int *buffer = (int *)malloc(100 * sizeof(int));
    if (buffer == NULL) return;
    buffer[0] = 42;
    printf("Processed value: %d\\n", buffer[0]);
    // Correct: Release dynamic memory back to the operating system
    free(buffer);
}

int main() {
    process_data();
    printf("Data processed successfully.\\n");
    return 0;
}""",
        "simple_explanation": "Memory allocated on the heap using `malloc()` must be released back to the OS using `free()`. Because `free(buffer)` was omitted, that heap memory remains claimed forever (memory leak).",
        "why_error_occurs": "Unlike languages with automatic garbage collectors, C requires explicit manual memory management. Any heap memory not explicitly freed remains consumed until process termination.",
        "hints": {
            "level1": "Every call to `malloc()` or `calloc()` on the heap must have a matching release call. Is there one?",
            "level2": "Look at `process_data()`. Dynamic memory is stored in `buffer`, but where is the call to `free()`?",
            "level3": "Add `free(buffer);` at the end of `process_data()` before returning."
        },
        "sample_input": "None",
        "sample_output": "Processed value: 42\nData processed successfully.",
        "learning_takeaway": "Every `malloc` must have a corresponding `free`. Failing to free dynamic memory causes memory leaks."
    },
    {
        "id": 15,
        "title": "Incorrect Input/Output Format Specifier & Missing &",
        "category": "I/O Format Error",
        "difficulty": "Beginner",
        "expected_bug_type": "I/O Specifier & Address Error",
        "line_number": 7,
        "buggy_code": """#include <stdio.h>

int main() {
    int age;
    printf("Enter your age: ");
    // Bug: Missing '&' in scanf; passes the value of age (garbage) instead of its address
    scanf("%d", age);
    printf("You entered age: %d\\n", age);
    return 0;
}""",
        "clean_code": """#include <stdio.h>

int main() {
    int age;
    printf("Enter your age: ");
    // Correct: Pass '&age' (the memory address) so scanf can write into it
    scanf("%d", &age);
    printf("You entered age: %d\\n", age);
    return 0;
}""",
        "simple_explanation": "In `scanf(\"%d\", age)`, the variable `age` is passed by value rather than by address `&age`. `scanf` expects a pointer to store the user's input.",
        "why_error_occurs": "Because C passes arguments by value, `scanf` receives the uninitialized content of `age` as a memory address and attempts to write to it, causing memory corruption or segmentation fault.",
        "hints": {
            "level1": "Does `scanf` know where in computer memory to store the user's input?",
            "level2": "Look at line 7: `scanf(\"%d\", age);`. In C, `scanf` requires the address-of operator `&` for non-pointer types.",
            "level3": "Change `scanf(\"%d\", age);` to `scanf(\"%d\", &age);`."
        },
        "sample_input": "19",
        "sample_output": "Enter your age: You entered age: 19",
        "learning_takeaway": "Always pass the address `&variable` to `scanf` for standard scalar variables (int, float, char)."
    }
]

def get_all_buggy_programs():
    """Returns the complete list of 15 buggy programs."""
    return BUGGY_PROGRAMS

def get_buggy_program_by_id(program_id):
    """Retrieves a specific buggy program by its unique ID."""
    for prog in BUGGY_PROGRAMS:
        if prog["id"] == int(program_id):
            return prog
    return None
