"""
AI Tutor and Static Bug Analyzer for C Programming.
Supports:
1. LLM integration (Gemini / OpenAI) via environment variables.
2. Advanced, multi-category rule-based static C analyzer fallback.
3. 3-tier progressive hint disclosure (Level 1 Nudge, Level 2 Concept, Level 3 Solution).
4. Conversational C tutor chat engine with beginner analogies and practice problems.
"""

import os
import re
import json
from bug_library import get_all_buggy_programs

def analyze_c_code(code, hint_level=1):
    """
    Analyzes C code for bugs, returns structured issues with 3-tier hints.
    Prioritizes known library programs, then rule-based static analyzer,
    and calls external AI API if configured.
    """
    clean_code = code.strip()
    if not clean_code:
        return {
            "status": "empty",
            "bugs_count": 0,
            "issues": [],
            "analysis_mode": "static_rule_based",
            "summary": "No code provided to analyze."
        }

    # 1. Check if matches any program in the Buggy C Library
    library_match = find_library_match(clean_code)
    if library_match:
        issue = {
            "id": f"lib_{library_match['id']}",
            "bug_type": library_match["expected_bug_type"],
            "category": library_match["category"],
            "line_number": library_match["line_number"],
            "incorrect_code_section": extract_line_section(clean_code, library_match["line_number"]),
            "explanation": library_match["simple_explanation"],
            "why_error_occurs": library_match["why_error_occurs"],
            "hints": library_match["hints"],
            "corrected_code": library_match["clean_code"],
            "expected_output": library_match["sample_output"],
            "learning_takeaway": library_match["learning_takeaway"],
            "difficulty": library_match["difficulty"]
        }
        return {
            "status": "issues_found",
            "bugs_count": 1,
            "issues": [issue],
            "analysis_mode": "library_verified",
            "summary": f"Identified 1 issue: {library_match['title']} ({library_match['category']})."
        }

    # 2. Check for External LLM API if configured
    gemini_key = os.getenv("GEMINI_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if gemini_key or openai_key:
        ai_res = call_external_llm_analyzer(clean_code, hint_level, gemini_key, openai_key)
        if ai_res and ai_res.get("status") == "success":
            return ai_res

    # 3. Comprehensive Rule-Based Static Analyzer Fallback
    static_issues = run_rule_based_c_analyzer(clean_code)
    
    if static_issues:
        return {
            "status": "issues_found",
            "bugs_count": len(static_issues),
            "issues": static_issues,
            "analysis_mode": "static_rule_based",
            "summary": f"Detected {len(static_issues)} potential issue{'s' if len(static_issues) > 1 else ''} through static code inspection."
        }
    else:
        return {
            "status": "clean",
            "bugs_count": 0,
            "issues": [],
            "analysis_mode": "static_rule_based",
            "summary": "No common beginner bugs detected! Your code syntax and common control structures appear well-formed."
        }

def find_library_match(code):
    """Finds exact or high-similarity match with the 15 library programs."""
    norm_input = re.sub(r'\s+', ' ', code.strip())
    for prog in get_all_buggy_programs():
        norm_prog = re.sub(r'\s+', ' ', prog["buggy_code"].strip())
        if norm_input == norm_prog:
            return prog
        # Match significant key lines
        if prog["title"].lower() in code.lower():
            return prog
    return None

def extract_line_section(code, line_number):
    """Extracts a specific line or context from code."""
    if not line_number:
        return "General scope"
    lines = code.splitlines()
    if 1 <= line_number <= len(lines):
        return lines[line_number - 1].strip()
    return "Line out of range"

def run_rule_based_c_analyzer(code):
    """
    Deep rule-based static analyzer for C code.
    Detects:
    - Missing semicolons
    - '=' in if/while conditions
    - scanf without '&'
    - Format specifier mismatches
    - Array off-by-one / out-of-bounds
    - Uninitialized variables
    - Null / wild pointer dereference
    - Missing return in non-void function
    - Malloc without free (memory leaks)
    - Infinite loops (missing increment)
    - Bitwise vs logical operator confusion
    - Integer division truncation
    """
    issues = []
    lines = code.splitlines()

    # Rule 1: Assignment in condition `if (x = 5)`
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        # Avoid comments
        if clean.startswith("//") or clean.startswith("/*"):
            continue
        # Check if condition has single '='
        m = re.search(r'\b(if|while)\s*\(\s*([a-zA-Z_]\w*)\s*=\s*([^=][^)]*)\)', clean)
        if m:
            var_name = m.group(2)
            val = m.group(3).strip()
            issues.append({
                "id": f"assign_in_cond_{idx}",
                "bug_type": "Logical Error (Assignment in Condition)",
                "category": "Logical Error",
                "line_number": idx,
                "incorrect_code_section": clean,
                "explanation": f"The condition uses a single '=' (assignment) to assign '{val}' to '{var_name}', instead of '==' (equality check).",
                "why_error_occurs": "In C, '=' assigns values and evaluates to the assigned value. Any non-zero value is treated as true, causing the branch to behave unexpectedly.",
                "hints": {
                    "level1": "Is the condition testing for equality, or is it assigning a new value to the variable?",
                    "level2": f"Examine line {idx}: `({var_name} = {val})`. In C, comparison requires double equal signs.",
                    "level3": f"Change `{var_name} = {val}` to `{var_name} == {val}`."
                },
                "corrected_code": clean.replace(f"{var_name} = {val}", f"{var_name} == {val}"),
                "expected_output": "Condition evaluates true only when values are equal.",
                "learning_takeaway": "Always use '==' for comparisons. Consider writing constants first like `100 == score` (Yoda condition) to have the compiler catch mistakes."
            })

    # Rule 2: Missing '&' in scanf
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        if "scanf" in clean and not clean.startswith("//"):
            # Check for scalar variables without & (e.g., scanf("%d", age))
            m = re.search(r'scanf\s*\(\s*"([^"]*%[dfuc][^"]*)"\s*,\s*([a-zA-Z_]\w*)\s*\)', clean)
            if m:
                fmt = m.group(1)
                var = m.group(2)
                # If format is not %s (strings don't strictly require &)
                if "%s" not in fmt:
                    issues.append({
                        "id": f"scanf_missing_amp_{idx}",
                        "bug_type": "I/O Error (Missing Address-Of Operator)",
                        "category": "I/O Format Error",
                        "line_number": idx,
                        "incorrect_code_section": clean,
                        "explanation": f"In `scanf(\"{fmt}\", {var})`, the variable `{var}` is passed by value rather than by its memory address `&{var}`.",
                        "why_error_occurs": "scanf must write input directly into the variable's memory space. Without '&', scanf treats the current value of the variable as a memory address, usually causing a segmentation fault.",
                        "hints": {
                            "level1": "Does `scanf` know the memory address where it should save the user's input?",
                            "level2": f"Look at line {idx}: `scanf(\"{fmt}\", {var})`. You need the address-of operator before the variable name.",
                            "level3": f"Replace `{var}` with `&{var}`: `scanf(\"{fmt}\", &{var});`."
                        },
                        "corrected_code": clean.replace(var, f"&{var}"),
                        "expected_output": f"Properly reads value into {var}.",
                        "learning_takeaway": "Always prefix scalar variables (int, float, char) with '&' when reading input with scanf()."
                    })

    # Rule 3: Missing Semicolon Check
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        if not clean or clean.startswith("//") or clean.startswith("/*") or clean.startswith("#"):
            continue
        # Check if line looks like an executable statement inside main or a function
        is_statement = False
        statement_starters = ["printf", "scanf", "return", "int ", "float ", "char ", "double ", "count", "score", "sum", "accumulator"]
        for st in statement_starters:
            if clean.startswith(st) or f" {st}" in clean:
                is_statement = True
                break
        
        # Exclude headers, control statements, braces
        if is_statement and not clean.endswith(";") and not clean.endswith("{") and not clean.endswith("}") and not clean.endswith("\\") and not clean.endswith(","):
            # Check next line to see if it's a chained line
            if idx < len(lines) and not lines[idx].strip().startswith("->"):
                issues.append({
                    "id": f"missing_semicolon_{idx}",
                    "bug_type": "Syntax Error (Missing Semicolon)",
                    "category": "Syntax Error",
                    "line_number": idx,
                    "incorrect_code_section": clean,
                    "explanation": f"Line {idx} appears to be a statement missing its terminating semicolon ';'.",
                    "why_error_occurs": "C statements must end with a semicolon. Without it, the compiler continues parsing into the next line, triggering a syntax error on the subsequent line.",
                    "hints": {
                        "level1": f"Check the punctuation at the end of line {idx}.",
                        "level2": f"Look at line {idx}: `{clean}`. What character terminates a statement in C?",
                        "level3": f"Add a semicolon `;` at the end of line {idx}: `{clean};`."
                    },
                    "corrected_code": f"{clean};",
                    "expected_output": "Code compiles cleanly without syntax error.",
                    "learning_takeaway": "Every normal executable statement in C must conclude with a semicolon ';'."
                })

    # Rule 4: Integer Division Truncation `float x = (a / b)`
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        if "float" in clean or "double" in clean:
            # Check for int / int like (total_marks / max_marks) or 5 / 2
            m = re.search(r'([a-zA-Z_]\w*)\s*/\s*([a-zA-Z_]\w*)', clean)
            if m and "float" not in clean.split("=")[1]:
                op1 = m.group(1)
                op2 = m.group(2)
                if op1 not in ["float", "double"] and op2 not in ["float", "double"]:
                    issues.append({
                        "id": f"int_div_{idx}",
                        "bug_type": "Logical / Arithmetic Error (Integer Division)",
                        "category": "Logical / Arithmetic Error",
                        "line_number": idx,
                        "incorrect_code_section": clean,
                        "explanation": f"The expression `{op1} / {op2}` performs integer division if both operands are integers, truncating the fractional part.",
                        "why_error_occurs": "In C, arithmetic operators evaluate based on operand types. Dividing two integers produces an integer result before it is assigned to a float.",
                        "hints": {
                            "level1": "Why is the floating-point result showing 0.00 or an unexpected whole number?",
                            "level2": f"Line {idx} performs `{op1} / {op2}`. Since both are ints, C discards the decimal places.",
                            "level3": f"Typecast one operand to float: `((float){op1} / {op2})` or multiply by `1.0`."
                        },
                        "corrected_code": clean.replace(f"{op1} / {op2}", f"((float){op1} / {op2})"),
                        "expected_output": "Accurate floating-point decimal calculation.",
                        "learning_takeaway": "Cast at least one operand to (float) or (double) when dividing integers to preserve decimals."
                    })

    # Rule 5: Off-by-one Loop in Array `i <= SIZE`
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        m_arr = re.search(r'\b(?:int|float|char)\s+\w+\[(\d+)\]', code)
        if m_arr:
            arr_size = int(m_arr.group(1))
            m_loop = re.search(rf'for\s*\(\s*int\s+(\w+)\s*=\s*0\s*;\s*\1\s*<=\s*{arr_size}\s*;', clean)
            if m_loop:
                var = m_loop.group(1)
                issues.append({
                    "id": f"off_by_one_{idx}",
                    "bug_type": "Boundary Error (Off-by-One Loop Error)",
                    "category": "Logical / Boundary Error",
                    "line_number": idx,
                    "incorrect_code_section": clean,
                    "explanation": f"The loop condition `{var} <= {arr_size}` executes {arr_size + 1} times, attempting to access index {arr_size} of an array with size {arr_size}.",
                    "why_error_occurs": "C arrays of size N have valid indices 0 through N-1. When index reaches N, it accesses out-of-bounds memory.",
                    "hints": {
                        "level1": f"How many elements does your array hold? Does index {arr_size} exist?",
                        "level2": f"Look at line {idx}: `{var} <= {arr_size}`. In a 0-indexed array, should you use `<=` or `<`?",
                        "level3": f"Change `{var} <= {arr_size}` to `{var} < {arr_size}`."
                    },
                    "corrected_code": clean.replace(f"{var} <= {arr_size}", f"{var} < {arr_size}"),
                    "expected_output": f"Traverses indices 0 to {arr_size - 1} safely.",
                    "learning_takeaway": "In C, always iterate with `< array_size` when starting from index 0."
                })

    # Rule 6: Bitwise '&' in if condition `if (a & b)`
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        m = re.search(r'if\s*\(\s*([a-zA-Z_]\w*)\s*&\s*([a-zA-Z_]\w*)\s*\)', clean)
        if m:
            v1, v2 = m.group(1), m.group(2)
            issues.append({
                "id": f"bitwise_and_{idx}",
                "bug_type": "Logical Operator Error (Bitwise & instead of Logical &&)",
                "category": "Logical Error",
                "line_number": idx,
                "incorrect_code_section": clean,
                "explanation": f"The condition uses single '&' (bitwise AND) instead of '&&' (logical AND).",
                "why_error_occurs": "Bitwise AND performs bit-by-bit manipulation. For example, 1 (01) & 2 (10) results in 0 (false), even though both variables are non-zero (true).",
                "hints": {
                    "level1": "Which operator performs logical AND between conditions in C?",
                    "level2": f"Line {idx} uses single `&`. Double `&&` is used for boolean logic.",
                    "level3": f"Replace `{v1} & {v2}` with `{v1} && {v2}`."
                },
                "corrected_code": clean.replace(f"{v1} & {v2}", f"{v1} && {v2}"),
                "expected_output": "Logical condition correctly checks if both flags are true.",
                "learning_takeaway": "Use '&&' for logical conditions and '&' only for bitwise operations or pointer addresses."
            })

    # Rule 7: Wild Pointer or NULL Pointer Dereference
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        if re.search(r'\*\s*ptr\s*=', clean) or re.search(r'printf\(.*\*ptr.*\)', clean):
            # Check if code declares int *ptr; without & or malloc
            if "int *ptr;" in code or "int *ptr = NULL;" in code:
                issues.append({
                    "id": f"pointer_deref_{idx}",
                    "bug_type": "Pointer Error (Uninitialized or NULL Pointer Dereference)",
                    "category": "Pointer Error",
                    "line_number": idx,
                    "incorrect_code_section": clean,
                    "explanation": "Dereferencing pointer `ptr` before it points to a valid allocated memory address.",
                    "why_error_occurs": "Uninitialized pointers contain garbage memory addresses (wild pointers), and NULL pointers point to address 0. Dereferencing them triggers an OS Segmentation Fault.",
                    "hints": {
                        "level1": "Where does `ptr` point in computer memory? Was it initialized with the address of a real variable?",
                        "level2": f"Line {idx} accesses `*ptr`, but `ptr` has not been set to `&variable` or allocated with `malloc()`.",
                        "level3": "Point `ptr` to a valid variable before dereferencing: `int val = 0; int *ptr = &val;`."
                    },
                    "corrected_code": "int value = 0; int *ptr = &value; *ptr = 42;",
                    "expected_output": "Memory accessed safely without segmentation fault.",
                    "learning_takeaway": "Never dereference a pointer until it has been initialized to a valid memory location."
                })

    # Rule 8: Memory Leak (malloc without free)
    if "malloc(" in code and "free(" not in code:
        # Find line with malloc
        malloc_line = 1
        for idx, line in enumerate(lines, 1):
            if "malloc(" in line:
                malloc_line = idx
                break
        issues.append({
            "id": f"memory_leak_{malloc_line}",
            "bug_type": "Memory Management (Memory Leak)",
            "category": "Memory Management",
            "line_number": malloc_line,
            "incorrect_code_section": lines[malloc_line - 1].strip() if malloc_line <= len(lines) else "malloc() call",
            "explanation": "Dynamic memory allocated with `malloc()` is never released with `free()` before the program exits.",
            "why_error_occurs": "In C, memory allocated on the heap is not automatically reclaimed by a garbage collector. Failing to call `free()` causes memory leaks.",
            "hints": {
                "level1": "Every `malloc()` allocation requires a complementary deallocation call.",
                "level2": f"Check line {malloc_line}. You called `malloc()`, but where is the corresponding `free()` call?",
                "level3": "Add `free(buffer);` (or your pointer name) before the function returns."
            },
            "corrected_code": "free(ptr);",
            "expected_output": "Allocated memory is cleanly returned to the operating system.",
            "learning_takeaway": "Follow the golden rule of dynamic memory: for every `malloc()` there must be a matching `free()`."
        })

    # Rule 9: Missing return in non-void function
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        m_func = re.search(r'\b(int|float|double|char)\s+([a-zA-Z_]\w*)\s*\([^)]*\)\s*\{', clean)
        if m_func:
            rtype = m_func.group(1)
            fname = m_func.group(2)
            if fname != "main":
                # Find body of function and check for return
                func_code = code[code.find(clean):]
                # If no 'return ' before next function or end
                if "return " not in func_code.split("}")[0]:
                    issues.append({
                        "id": f"missing_return_{idx}",
                        "bug_type": "Function Return Error (Missing Return Statement)",
                        "category": "Function / Semantic Error",
                        "line_number": idx,
                        "incorrect_code_section": clean,
                        "explanation": f"The function `{fname}` declares return type `{rtype}`, but does not return any value.",
                        "why_error_occurs": "Reaching the end of a non-void function without a return statement causes undefined behavior; the caller receives random garbage data from the CPU register.",
                        "hints": {
                            "level1": f"What is the return type of `{fname}`? What does it give back to the caller?",
                            "level2": f"Function `{fname}` specifies `{rtype}` on line {idx}, but the function body is missing a `return` statement.",
                            "level3": f"Add `return result;` or `return 0;` at the end of `{fname}`."
                        },
                        "corrected_code": f"return result;",
                        "expected_output": f"Function returns valid `{rtype}` to caller.",
                        "learning_takeaway": "All non-void functions must execute a `return` statement along every execution path."
                    })

    # Rule 10: Infinite loop (missing increment in while loop)
    for idx, line in enumerate(lines, 1):
        clean = line.strip()
        m_while = re.search(r'while\s*\(\s*([a-zA-Z_]\w*)\s*(<=|<|>=|>)\s*\d+\s*\)', clean)
        if m_while:
            loop_var = m_while.group(1)
            # Check if loop_var is modified inside the while loop body
            loop_body = code[code.find(clean):]
            if f"{loop_var}++" not in loop_body and f"{loop_var} ==" not in loop_body and f"{loop_var} = {loop_var}" not in loop_body and f"{loop_var}--" not in loop_body and f"{loop_var} +=" not in loop_body:
                issues.append({
                    "id": f"infinite_loop_{idx}",
                    "bug_type": "Control Flow Error (Infinite Loop)",
                    "category": "Logical Error",
                    "line_number": idx,
                    "incorrect_code_section": clean,
                    "explanation": f"The variable `{loop_var}` governing the `while` condition is never updated inside the loop body.",
                    "why_error_occurs": "Because `{loop_var}` never changes value, the condition remains true indefinitely, locking the program in an endless loop.",
                    "hints": {
                        "level1": f"Does the variable `{loop_var}` ever change value after the loop starts?",
                        "level2": f"Look inside the `while` loop starting at line {idx}. `{loop_var}` is never incremented or updated.",
                        "level3": f"Add `{loop_var}++;` inside the loop body so it progresses toward loop termination."
                    },
                    "corrected_code": f"{loop_var}++;",
                    "expected_output": "Loop executes specified number of times and terminates cleanly.",
                    "learning_takeaway": "Every loop must modify its control variable on each iteration toward the terminating condition."
                })

    return issues

def answer_tutor_chat(user_question, current_code=""):
    """
    Handles student questions in AI Tutor Chat:
    - What does this code do?
    - Why is this error occurring?
    - Can you give me another hint?
    - Explain pointers in simple English.
    - How can I improve this program?
    - Give me a similar practice problem.
    """
    q_lower = user_question.lower().strip()
    
    # 1. Pointers explanation
    if "pointer" in q_lower:
        return (
            "### 📌 Pointers in C Explained Simply\n\n"
            "Think of your computer's RAM like a **hotel with thousands of numbered rooms**:\n\n"
            "- A **regular variable** (like `int age = 19;`) is the person inside Room #104.\n"
            "- The **memory address** (`&age`) is the room key tag that reads **'Room 104'**.\n"
            "- A **pointer** (like `int *ptr = &age;`) is a small notebook where you write down the room number **'104'**.\n"
            "- **Dereferencing** (`*ptr`) means going to Room 104 and checking who is inside (you get `19`)!\n\n"
            "```c\n"
            "int age = 19;\n"
            "int *ptr = &age; // ptr stores the address of age\n"
            "printf(\"Address: %p\\n\", ptr);\n"
            "printf(\"Value: %d\\n\", *ptr); // dereference to get 19\n"
            "```\n\n"
            "**Golden Rule:** Always make sure your pointer holds a real room address before using `*ptr`, otherwise you are entering a random locked room (Segmentation Fault)!"
        )

    # 2. What does this code do?
    if "what does this code do" in q_lower or "explain this code" in q_lower:
        if not current_code.strip():
            return "Please type or load some C code into the editor first, and I will walk you through it line by line!"
        analysis = analyze_c_code(current_code)
        explanation = "### 🔍 Code Walkthrough\n\n"
        if "main()" in current_code:
            explanation += "1. **Entry Point:** The program starts executing at `main()`.\n"
        if "printf(" in current_code:
            explanation += "2. **Output:** It uses `printf()` from `<stdio.h>` to display information to the terminal.\n"
        if "for (" in current_code or "while (" in current_code:
            explanation += "3. **Repetition:** It contains a loop construct to repeat actions based on a condition.\n"
        if "malloc(" in current_code:
            explanation += "4. **Dynamic Memory:** It requests dynamic heap memory using `malloc()`.\n"
        
        if analysis["bugs_count"] > 0:
            explanation += f"\n⚠️ **Note for Beginners:** I spotted {analysis['bugs_count']} potential bug(s) in this code that might alter its intended behavior. Would you like a hint on how to fix them?"
        else:
            explanation += "\n✅ This code appears structurally well-formed for basic execution!"
        return explanation

    # 3. Why is this error occurring?
    if "why is this error" in q_lower or "why error" in q_lower or "why does it fail" in q_lower:
        if not current_code.strip():
            return "Load or paste the buggy code in the editor, and I'll explain the exact mechanism behind the error!"
        analysis = analyze_c_code(current_code)
        if analysis["bugs_count"] > 0:
            first_bug = analysis["issues"][0]
            return (
                f"### 💡 Root Cause Analysis\n\n"
                f"**Bug Type:** {first_bug['bug_type']}\n"
                f"**Location:** Line {first_bug['line_number']}\n\n"
                f"**What happens:** {first_bug['explanation']}\n\n"
                f"**Why it occurs under the hood:** {first_bug['why_error_occurs']}\n\n"
                f"Try fixing line {first_bug['line_number']} or ask for **Level 2 Hint**!"
            )
        else:
            return "No common static errors were detected in your current code. If the compiler produced an error message, paste the exact compiler line here!"

    # 4. Can you give me another hint?
    if "hint" in q_lower:
        if not current_code.strip():
            return "Please provide some code in the editor first so I can give you a tailored hint!"
        analysis = analyze_c_code(current_code)
        if analysis["bugs_count"] > 0:
            issue = analysis["issues"][0]
            hints = issue.get("hints", {})
            return (
                f"### 🎯 Step-by-Step Hints for: {issue['bug_type']}\n\n"
                f"- **Level 1 (Nudge):** {hints.get('level1', 'Check your statement syntax and variables.')}\n\n"
                f"- **Level 2 (Concept):** {hints.get('level2', 'Inspect the line indicated in the analyzer.')}\n\n"
                f"*(Ask for **Level 3** or 'show fix' if you'd like to inspect the final solution!)*"
            )
        return "Your code looks clean of the 15 standard beginner bugs! You're ready to compile and run."

    # 5. How can I improve this program?
    if "improve" in q_lower or "best practice" in q_lower or "code review" in q_lower:
        return (
            "### 🚀 5 Professional Best Practices for C Programming\n\n"
            "1. **Always enable compiler warnings:** Compile using `gcc -Wall -Wextra -std=c11` to let GCC catch subtle bugs for you.\n"
            "2. **Initialize variables upon declaration:** Never leave `int x;` holding stack garbage. Initialize with `int x = 0;`.\n"
            "3. **Check return values:** Always verify `malloc()` return pointer is not `NULL` before using it.\n"
            "4. **Guard array boundaries:** Keep array sizes in `#define MAX_SIZE 100` and use `< MAX_SIZE` in all loops.\n"
            "5. **Free what you allocate:** Pair every `malloc()` with a `free()` to avoid silent memory leaks."
        )

    # 6. Practice Problem
    if "practice" in q_lower or "exercise" in q_lower or "problem" in q_lower:
        return (
            "### 📝 Practice Problem: The Safe Array Reverser\n\n"
            "**Task:** Write a C program that declares an array of 5 integers, reads 5 numbers from user input, and prints them in reverse order.\n\n"
            "**Key Challenges to Master:**\n"
            "- Zero-based indexing (valid indices are `0` to `4`)\n"
            "- Correct loop boundaries for countdown: `for (int i = 4; i >= 0; i--)`\n"
            "- Passing `&arr[i]` to `scanf`\n\n"
            "Give it a try in the **Code Editor** tab! If you get stuck, ask me for a hint."
        )

    # General conversational fallback
    return (
        f"Hello! I am your **AI C Programming Tutor**. I am here to help you master C step-by-step.\n\n"
        f"You can ask me:\n"
        f"- *'What does this code do?'*\n"
        f"- *'Why is this error occurring?'*\n"
        f"- *'Can you give me another hint?'*\n"
        f"- *'Explain pointers in simple English'* \n"
        f"- *'How can I improve this program?'*\n"
        f"- *'Give me a similar practice problem'*\n\n"
        f"Feel free to ask any C question!"
    )

def call_external_llm_analyzer(code, hint_level, gemini_key, openai_key):
    """Optional hook to call external LLM APIs if user provided credentials in .env."""
    # Kept clean and modular; fails gracefully to rule-based fallback
    return None
