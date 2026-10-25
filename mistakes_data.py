"""
Beginner Mistakes Guide Data for C Programming Tutor.
Documents the 10 most frequent beginner C mistakes, explanations, and prevention rules.
"""

COMMON_MISTAKES = [
    {
        "id": 1,
        "title": "Semicolon Immediately After 'if' or 'for'",
        "category": "Syntax & Control Flow",
        "description": "Placing a stray semicolon right after an 'if' or 'for' header silently empties the body.",
        "wrong_code": """// Wrong: Semicolon terminates the if statement immediately!
if (score >= 50);
{
    printf("You passed!\\n"); // This block ALWAYS runs!
}""",
        "fixed_code": """// Correct: No semicolon after if condition
if (score >= 50) {
    printf("You passed!\\n");
}""",
        "why_wrong": "In C, a solitary semicolon ';' constitutes an empty null statement. `if (score >= 50);` means 'if score >= 50 do nothing'. The curly brace block below it becomes an unconditional block that always runs.",
        "prevention": "Never put a semicolon after `if (...)`, `for (...)`, or `while (...)` headers unless deliberately writing an empty loop."
    },
    {
        "id": 2,
        "title": "Using '=' (Assignment) Instead of '==' (Equality)",
        "category": "Logical Error",
        "description": "Writing single '=' inside an if condition assigns a value rather than testing equality.",
        "wrong_code": """int logged_in = 0;
// Wrong: Assigns 1 to logged_in, evaluates to 1 (TRUE)
if (logged_in = 1) {
    printf("Access Granted!\\n"); // Always triggers!
}""",
        "fixed_code": """int logged_in = 0;
// Correct: '==' tests equality without modifying logged_in
if (logged_in == 1) {
    printf("Access Granted!\\n");
}""",
        "why_wrong": "In C, an assignment is an expression whose value is the assigned number. `(logged_in = 1)` evaluates to 1 (true). Any non-zero value evaluates to true in C.",
        "prevention": "Enable GCC warnings with `-Wall`. You can also use Yoda conditions like `if (1 == logged_in)` so accidental assignment causes a compile error."
    },
    {
        "id": 3,
        "title": "Missing the '&' Address-of Operator in scanf()",
        "category": "Input / Output",
        "description": "Passing a variable by value to scanf() causes it to treat the variable's value as a pointer.",
        "wrong_code": """int age;
// Wrong: Missing '&'. Passes random garbage value of age as pointer!
scanf("%d", age);""",
        "fixed_code": """int age;
// Correct: Passes memory address of age
scanf("%d", &age);""",
        "why_wrong": "C passes function arguments by value. `scanf()` requires a memory address to write data into. Without `&`, it writes into an arbitrary memory location, causing a crash.",
        "prevention": "Always verify that every scalar argument in `scanf` has `&` (unless it is already a pointer or a string array name)."
    },
    {
        "id": 4,
        "title": "Integer Division Fractional Truncation",
        "category": "Arithmetic & Types",
        "description": "Dividing two integers always produces an integer in C, throwing away the decimal fraction.",
        "wrong_code": """int correct = 3, total = 4;
// Wrong: 3 / 4 is integer division yielding 0, so ratio becomes 0.0
float ratio = correct / total;""",
        "fixed_code": """int correct = 3, total = 4;
// Correct: Explicitly cast one operand to float to trigger floating division
float ratio = (float)correct / total; // Evaluates to 0.75""",
        "why_wrong": "In C, the operator type is determined solely by the operands, not by the variable receiving the result. `int / int` always yields an `int` with fractions truncated toward zero.",
        "prevention": "Cast at least one operand: `(float)a / b` or multiply by `1.0f * a / b`."
    },
    {
        "id": 5,
        "title": "Off-by-One Array Indexing (0 to N vs 0 to N-1)",
        "category": "Arrays & Memory",
        "description": "Accessing index N on an array of size N writes past the allocated array boundaries.",
        "wrong_code": """int marks[5];
// Wrong: Loop runs for i = 0, 1, 2, 3, 4, 5. marks[5] is out of bounds!
for (int i = 0; i <= 5; i++) {
    marks[i] = 100;
}""",
        "fixed_code": """int marks[5];
// Correct: Strictly use '< 5' to iterate indices 0, 1, 2, 3, 4
for (int i = 0; i < 5; i++) {
    marks[i] = 100;
}""",
        "why_wrong": "C arrays are strictly 0-indexed. An array declared with size 5 has slots `[0]`, `[1]`, `[2]`, `[3]`, and `[4]`. Accessing `marks[5]` corrupts adjacent stack variables.",
        "prevention": "Use the standard idiom: `for (int i = 0; i < SIZE; i++)`. Notice the strict `<` (less than) operator."
    },
    {
        "id": 6,
        "title": "Using Uninitialized Local Variables",
        "category": "Runtime & Stack",
        "description": "Local variables in C are not initialized to zero automatically; they contain stack garbage.",
        "wrong_code": """int sum; // Contains random bits left on the CPU stack
for (int i = 1; i <= 5; i++) {
    sum += i; // Garbage + 1 + 2 + 3...
}""",
        "fixed_code": """int sum = 0; // Explicitly initialized to 0
for (int i = 1; i <= 5; i++) {
    sum += i;
}""",
        "why_wrong": "Unlike some modern managed languages, C does not zero out memory for local variables for performance reasons. Reading uninitialized memory causes unpredictable bugs.",
        "prevention": "Adopt the habit of initializing variables immediately upon declaration: `int count = 0;`."
    },
    {
        "id": 7,
        "title": "Dereferencing Uninitialized or NULL Pointers",
        "category": "Pointers",
        "description": "Writing to `*ptr` when `ptr` has not been assigned a valid address causes a Segmentation Fault.",
        "wrong_code": """int *ptr; // Wild pointer containing arbitrary address
*ptr = 25; // Crash! Writing to random OS memory""",
        "fixed_code": """int val = 0;
int *ptr = &val; // Valid pointer assigned address of val
*ptr = 25;       // Safely updates val to 25""",
        "why_wrong": "Pointers do not create memory for storing data; they only store memory addresses. Dereferencing an invalid or NULL address triggers a memory access violation.",
        "prevention": "Always initialize pointers either to `NULL` or to `&variable`. Check `if (ptr != NULL)` before dereferencing."
    },
    {
        "id": 8,
        "title": "Memory Leaks (malloc without matching free)",
        "category": "Memory Management",
        "description": "Allocating heap memory with malloc() without freeing it retains memory until process exit.",
        "wrong_code": """void load_scores() {
    int *arr = (int *)malloc(1000 * sizeof(int));
    // Function exits without free(arr). Memory is leaked forever!
}""",
        "fixed_code": """void load_scores() {
    int *arr = (int *)malloc(1000 * sizeof(int));
    if (arr == NULL) return;
    // ... work with arr ...
    free(arr); // Cleanly release heap memory
}""",
        "why_wrong": "Heap memory allocated via `malloc()` or `calloc()` is not automatically collected. If repeated in a loop or long-running program, the OS will eventually run out of RAM.",
        "prevention": "Write your `free(ptr);` statement at the same time you write `malloc()`."
    },
    {
        "id": 9,
        "title": "Missing 'break' in Switch Statements (Fallthrough)",
        "category": "Control Flow",
        "description": "Omitting break statements in switch cases causes unwanted execution of all subsequent cases.",
        "wrong_code": """switch (option) {
    case 1:
        printf("Starting game...\\n");
        // Missing break! Continues straight into case 2!
    case 2:
        printf("Exiting game...\\n");
}""",
        "fixed_code": """switch (option) {
    case 1:
        printf("Starting game...\\n");
        break; // Exits switch safely
    case 2:
        printf("Exiting game...\\n");
        break;
}""",
        "why_wrong": "In C, switch statements fall through by default. If a case doesn't end with `break`, control cascades down through all remaining cases regardless of the condition.",
        "prevention": "Always end every `case` with a `break;` statement unless you are intentionally implementing fallthrough."
    },
    {
        "id": 10,
        "title": "Missing Header Files like <stdio.h> or <stdlib.h>",
        "category": "Preprocessor & Declarations",
        "description": "Calling functions like printf(), scanf(), or malloc() without including their prototypes.",
        "wrong_code": """// Missing #include <stdio.h>
int main() {
    printf("Hello World\\n"); // Compiler issues implicit declaration warning
    return 0;
}""",
        "fixed_code": """#include <stdio.h>  // Declares printf, scanf, etc.
#include <stdlib.h> // Declares malloc, free, exit, etc.

int main() {
    printf("Hello World\\n");
    return 0;
}""",
        "why_wrong": "Without header prototypes, the compiler assumes default return types and parameter conventions (implicit function declarations), which can cause ABI mismatches.",
        "prevention": "Always include standard headers at the very top of your `.c` files."
    }
]

def get_all_mistakes():
    return COMMON_MISTAKES
