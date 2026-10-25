# AI Coding Tutor for C Programming 🎓💻

An intelligent, pedagogical learning platform developed specifically for **first-year Computer Science and Engineering (CSE) students**. Unlike conventional AI assistants that immediately give away full answers and foster passive dependency, this platform guides students through **hint-first scaffolding**, root-cause explanations, live compiler diagnostics, interactive checklists, and structured quizzes.

---

## 🌟 Key Features & Modules

### 1. 📊 Home Dashboard (`/`)
- Real-time learning telemetry: Programs analyzed, bugs identified, hints unlocked, checklist completion %, and quiz averages.
- Live compiler status pill detecting GCC / Clang / MinGW on system PATH.
- Quick navigation tiles to all modules.
- Recent analysis history log.

### 2. 💻 C Code Editor (`/editor`)
- Integrated **Monaco Code Editor** with syntax highlighting (and automatic responsive fallback).
- **1-Click Buggy Program Loader** for all 15 curated library programs.
- **GCC Compilation Interface** running `-Wall -Wextra -std=c11 -O0` inside isolated ephemeral temporary directories.
- Split-panel output system:
  - **Program Output Console:** Displays actual standard output and standard error from execution.
  - **Compiler Diagnostics:** Structured parsing of GCC line-by-line warnings and syntax errors.
  - **Execution & Sandbox Details:** Telemetry covering process execution time (ms), exit codes, output size caps, and safety limits.
- Interactive standard input (`stdin`) drawer for testing programs that read input with `scanf()`.

### 3. 🔬 AI Bug Analyzer with 3-Tier Progressive Hints (`/analyzer`)
- Analyzes C code across **15 distinct bug classes** (syntax, logic, runtime, pointers, memory leaks, I/O).
- Structured diagnosis:
  1. **Bug Type & Category**
  2. **Exact Line Number**
  3. **Faulty Code Snippet**
  4. **Simple-English Explanation**
  5. **Why the Error Occurs Under the Hood**
  6. **3-Tier Progressive Hint Revelation:**
     - **Level 1 (Subtle Nudge):** Asks a guiding question pointing to the issue without revealing code.
     - **Level 2 (Concept & Line Focus):** Explains the underlying language rule (e.g. 0-based indexing or operator difference) and points directly to the faulty statement.
     - **Level 3 (Solution & Fix):** Shows the clean corrected C code with an in-depth breakdown.
  7. **Expected Program Output**
  8. **Key Learning Takeaway**
- **5-Star Tutor Quality Feedback Rating:** Allows students to rate explanation clarity, hint usefulness, bug accuracy, and fix correctness directly into SQLite.

### 4. 📚 Curated Buggy C Program Library (`/library`)
15 authentic beginner C programs with difficulty badges, filters, hints, clean source code, and sample I/O:
1. **Missing Semicolon in Statement** (`Syntax Error`)
2. **Incorrect Variable Declaration & Type Mismatch** (`Syntax / Semantic Error`)
3. **Incorrect `if` Condition (`=` vs `==`)** (`Logical Error`)
4. **Off-by-One Loop Error in Array Traversal** (`Logical / Boundary Error`)
5. **Infinite Loop Due to Missing State Update** (`Logical Error`)
6. **Incorrect Loop Boundary (Wrong Decrement Direction)** (`Logical / Boundary Error`)
7. **Integer Division Truncation Mistake** (`Logical / Arithmetic Error`)
8. **Incorrect Operator Usage (Bitwise `&` vs Logical `&&`)** (`Logical Error`)
9. **Array Out-of-Bounds Write (Buffer Overrun)** (`Runtime / Undefined Behavior`)
10. **Uninitialized Variable Usage (Garbage Value)** (`Runtime / Undefined Behavior`)
11. **Incorrect Pointer Usage (Wild / Unassigned Pointer)** (`Pointer Error`)
12. **Null Pointer Dereference (Segmentation Fault)** (`Pointer Error`)
13. **Incorrect Function Return Value & Missing Return** (`Function / Semantic Error`)
14. **Memory Allocation & Missing Deallocation (Memory Leak)** (`Memory Management`)
15. **Incorrect Input/Output Format Specifier & Missing `&` in `scanf`** (`I/O Format Error`)

### 5. 🤖 AI Tutor Conversational Chat (`/chat`)
- Interactive conversational tutor answering questions in beginner-friendly language.
- Preset quick prompt chips:
  - *"Explain pointers in simple English"* (uses the hotel room & key tag memory analogy).
  - *"What does this code do?"*
  - *"Why is this error occurring?"*
  - *"Can you give me another hint?"*
  - *"Give me a similar practice problem"*
  - *"How can I improve this program?"*

### 6. ✅ Interactive Debugging Checklist (`/checklist`)
- 12 comprehensive verification checks covering syntax, semicolons, variable initialization, loop bounds, pointers, `scanf` addresses, `malloc` NULL guards, and `-Wall` compilation flags.
- Interactive checkboxes with real-time progress bar and percentage tracking persisted in SQLite.
- Category filters (All, Pending, Completed).

### 7. ⚠️ 10 Common Beginner Mistakes Guide (`/mistakes`)
- Side-by-side code diffs showing the flawed idiom vs the correct C idiom.
- Explains *Why it is wrong* and the *Golden rule of prevention* for exams and lab sessions.

### 8. 📝 C Concept Quiz Module (`/quiz`)
- 12 comprehensive multiple-choice questions covering C syntax, conditions, loops, pointers, memory, and compiler flags.
- Real-time score calculation and percentage grade.
- Detailed question-by-question answer key with educational explanations.
- Retake button and historical attempts log.

### 9. 📈 Learning Progress & Quality Reports (`/progress`)
- Aggregate learning telemetry and quiz score histories.
- Tutor quality rating breakdown (clarity, usefulness, accuracy, fix).
- Student comments log.

### 10. 📖 Academic Documentation & Prompt Library (`/docs` & `/prompts`)
- Formal academic specification: Abstract, Problem Statement, Objectives, FR/NFR, System Architecture Diagram, Schema, and References (GCC Manual, ISO C18 Standard).
- 7 reusable, pedagogical system prompt templates with copy-to-clipboard buttons.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Backend** | Python 3.13, Flask 3.1 |
| **Database** | SQLite 3 (`data/c_tutor.db`) |
| **Frontend** | Semantic HTML5, Vanilla CSS3 (Dark Navy `#090d16` & Cyan `#38bdf8` Theme), Modern Vanilla JavaScript |
| **Code Editor** | Monaco Editor (VS Code Editor Engine via CDN with textarea fallback) |
| **Compiler Interface**| GCC / Clang / MinGW-w64 with ephemeral directory sandboxing |
| **AI Integration** | Modular AI engine with multi-category static rule-based C analyzer fallback |
| **Test Suite** | Pytest (`pytest tests/ -v`) |

---

## 🔒 Security & Safe Execution Policy

To guarantee security when executing untrusted C code:
1. **Isolated Ephemeral Directories:** Every compilation and execution cycle takes place in an isolated temporary directory (`tempfile.mkdtemp()`) with guaranteed cleanup in a `finally:` block.
2. **Strict Timeouts:** Compilation is bounded by a 5.0-second timeout; program execution is capped at a 3.0-second timeout. Runaway infinite loops or blocking operations are immediately terminated.
3. **Output Truncation:** Terminal output is capped at 64 KB (65,536 bytes) to prevent browser buffer exhaustion from infinite `printf` statements.
4. **Honest Execution Transparency:** Never fabricates fake execution outputs. If GCC is not detected in the host environment, binary execution is disabled with clear setup instructions, while all static analysis, 3-tier hints, and quizzes continue to function seamlessly.

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10+ installed
- *(Optional for native binary execution)* GCC / MinGW-w64 compiler

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Install MinGW-w64 GCC Compiler on Windows
If you wish to enable native C binary compilation on Windows:
```powershell
winget install BrechtSanders.WinLibs.MCF.UCRT
```
*Add the `bin` directory (e.g. `C:\msys64\ucrt64\bin`) to your Windows System PATH.*

### 4. Run Automated Tests
```bash
python -m pytest tests/ -v
```
*(All 22 test suites will run and pass).*

### 5. Launch the Web Application
```bash
python app.py
```
Open your browser and navigate to:
**`http://127.0.0.1:5000/`**

---

## 🧪 Automated Test Suite Summary

The automated test suite in `tests/` verifies:
- `test_analyzer.py`: Detection across all 15 bug categories, progressive 3-tier hints disclosure, clean code validation, and AI tutor chat responses.
- `test_compiler.py`: Compiler detection, GCC diagnostics parser (`file.c:line:col: error:`), and execution security contracts.
- `test_database.py`: SQLite table creation, analysis telemetry, 5-star rating storage, quiz attempt grading, and checklist persistence.
- `test_routes.py`: HTTP 200 checks across all 10 views and JSON API endpoints (`/api/analyze`, `/api/compile`, `/api/chat`, `/api/quiz/submit`, `/api/checklist/toggle`, `/api/rate`).

---

## 🎓 College Demonstration Guide

For laboratory exams, viva voce, or mini-project presentations:
1. **Dashboard Overview (`/`):** Demonstrate the live statistics, system architecture overview, and host compiler status.
2. **Buggy Program Library (`/library`):** Filter by category (e.g. *Pointers* or *Logical Error*), expand hints, and click **"Open in Editor"**.
3. **Editor & Execution (`/editor`):** Show Monaco Editor with C syntax highlighting. Click **"Compile & Run"** to inspect compiler diagnostics and output.
4. **AI Bug Analyzer (`/analyzer`):** Click **"Run AI Analysis"**. Demonstrate progressive hint disclosure:
   - Click **Level 1** for the subtle guiding question.
   - Click **Level 2** for the concept and faulty line.
   - Click **Level 3** for the corrected code and explanation.
   - Submit a 5-star rating to demonstrate SQLite feedback logging.
5. **Interactive Tutor Chat (`/chat`):** Click *"Explain pointers in simple English"* to show the hotel room memory analogy.
6. **Debugging Checklist (`/checklist`):** Check off items to show real-time progress bar animations and database persistence.
7. **Concept Quiz (`/quiz`):** Answer questions, click submit, and review the detailed explanation key and score breakdown.
