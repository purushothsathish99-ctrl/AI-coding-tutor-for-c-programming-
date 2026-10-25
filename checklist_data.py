"""
Debugging Checklist Data for C Programming Tutor.
Contains 12 comprehensive beginner-friendly debugging verification steps.
"""

DEBUGGING_CHECKLIST = [
    {
        "id": "check_syntax",
        "title": "Check Syntax and Semicolons",
        "category": "Syntax",
        "icon": "fas fa-terminal",
        "description": "Inspect every statement ending. Ensure each statement inside a function concludes with a semicolon (;) and braces {} are properly balanced.",
        "tip": "Check lines immediately preceding any compiler error message."
    },
    {
        "id": "init_variables",
        "title": "Declare and Initialize Variables",
        "category": "Variables",
        "icon": "fas fa-cube",
        "description": "Ensure every variable has a declared data type (int, float, char) and is explicitly initialized before reading or accumulating values.",
        "tip": "Uninitialized local variables contain unpredictable stack garbage values."
    },
    {
        "id": "verify_conditions",
        "title": "Verify Conditions and Operators",
        "category": "Logic",
        "icon": "fas fa-code-branch",
        "description": "Double check all `if`, `while`, and `for` condition statements. Ensure you used '==' for comparison and NOT '=' (assignment), and '&&' for logical AND.",
        "tip": "Writing `if (x = 5)` assigns 5 to x and always evaluates to true."
    },
    {
        "id": "check_loop_bounds",
        "title": "Check Loop Boundaries and Progression",
        "category": "Loops",
        "icon": "fas fa-redo",
        "description": "Verify loop starting conditions, termination boundaries, and step expressions (i++ vs i--). Confirm the loop makes progress toward terminating.",
        "tip": "Check for missing counter increments that trigger infinite loops."
    },
    {
        "id": "check_array_indices",
        "title": "Check Array Index Bounds (0 to N-1)",
        "category": "Arrays",
        "icon": "fas fa-list-ol",
        "description": "Remember C is 0-indexed. An array of size N has indices 0 to N-1. Check that your loops use `< N` rather than `<= N`.",
        "tip": "Accessing index N on an array of size N is an off-by-one boundary violation."
    },
    {
        "id": "validate_pointers",
        "title": "Validate Pointers Before Dereferencing",
        "category": "Pointers",
        "icon": "fas fa-crosshairs",
        "description": "Ensure pointers point to a valid memory address (&variable or heap buffer). Check `if (ptr != NULL)` before attempting to read or write through `*ptr`.",
        "tip": "Dereferencing NULL or a wild pointer causes an instant Segmentation Fault."
    },
    {
        "id": "check_return_values",
        "title": "Check Function Return Values",
        "category": "Functions",
        "icon": "fas fa-reply",
        "description": "Verify that non-void functions have an explicit `return` along every possible execution path, and that `main()` concludes with `return 0;`.",
        "tip": "Omitting return in non-void functions causes undefined behavior."
    },
    {
        "id": "match_format_specifiers",
        "title": "Match Format Specifiers with Data Types",
        "category": "I/O",
        "icon": "fas fa-percentage",
        "description": "Confirm that format specifiers in printf/scanf match the variable types: %d for int, %f for float, %lf for double, %c for char, and %s for strings.",
        "tip": "Printing a float with %d prints meaningless integer bit interpretations."
    },
    {
        "id": "validate_scanf_input",
        "title": "Validate Input and Pass Addresses to scanf()",
        "category": "I/O",
        "icon": "fas fa-keyboard",
        "description": "Ensure every scalar variable in `scanf` is passed by address with `&variable`. Check the return value of scanf to confirm successful input conversion.",
        "tip": "Forgetting '&' in `scanf(\"%d\", val)` crashes because val is treated as an address."
    },
    {
        "id": "check_malloc_null",
        "title": "Check Memory Allocation Return for NULL",
        "category": "Memory",
        "icon": "fas fa-microchip",
        "description": "Always check if `malloc()` or `calloc()` returned NULL before writing into the memory block. Handle out-of-memory errors gracefully.",
        "tip": "If the system cannot allocate requested memory, malloc returns NULL."
    },
    {
        "id": "free_allocated_memory",
        "title": "Free Dynamically Allocated Memory Appropriately",
        "category": "Memory",
        "icon": "fas fa-trash-alt",
        "description": "Verify that every heap buffer allocated with `malloc` is deallocated using `free(ptr)` exactly once before exiting or discarding the pointer.",
        "tip": "After freeing, set `ptr = NULL;` to prevent dangling pointer bugs."
    },
    {
        "id": "compile_with_wall",
        "title": "Compile with Warnings (-Wall -Wextra)",
        "category": "Compiler",
        "icon": "fas fa-shield-alt",
        "description": "Compile your code with `gcc -Wall -Wextra -std=c11`. Treat every compiler warning as an error waiting to happen at runtime.",
        "tip": "Warnings alert you to uninitialized variables and misplaced operators before you run."
    }
]

def get_all_checklist_items():
    return DEBUGGING_CHECKLIST
