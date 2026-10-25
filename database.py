"""
Database module for AI Coding Tutor for C Programming.
Uses SQLite for persisting:
- Code analysis history
- Tutor quality ratings
- Quiz attempts & scores
- Interactive debugging checklist items
- Student statistics
"""

import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "c_tutor.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database with required tables and default seed data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Analysis History
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        code_snippet TEXT NOT NULL,
        program_title TEXT DEFAULT 'Custom Code',
        bugs_found INTEGER DEFAULT 0,
        bug_categories TEXT,
        analysis_mode TEXT DEFAULT 'static_rule_based',
        hints_unlocked INTEGER DEFAULT 1,
        execution_status TEXT DEFAULT 'not_run',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Tutor Ratings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tutor_ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id INTEGER,
        clarity_score INTEGER CHECK(clarity_score BETWEEN 1 AND 5),
        usefulness_score INTEGER CHECK(usefulness_score BETWEEN 1 AND 5),
        accuracy_score INTEGER CHECK(accuracy_score BETWEEN 1 AND 5),
        fix_score INTEGER CHECK(fix_score BETWEEN 1 AND 5),
        feedback_comments TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (analysis_id) REFERENCES analysis_history (id)
    );
    """)

    # 3. Quiz Attempts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT DEFAULT 'Student',
        score INTEGER NOT NULL,
        total_questions INTEGER NOT NULL,
        percentage REAL NOT NULL,
        answers_json TEXT,
        completed_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 4. Debugging Checklist Progress
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checklist_progress (
        item_id TEXT PRIMARY KEY,
        is_completed INTEGER DEFAULT 0,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 5. Overall System Statistics Cache
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_stats (
        key TEXT PRIMARY KEY,
        value INTEGER DEFAULT 0
    );
    """)

    # Initialize stats if empty
    default_stats = [
        ('programs_analyzed', 0),
        ('bugs_identified', 0),
        ('hints_unlocked', 0),
        ('quizzes_taken', 0),
        ('code_compilations', 0)
    ]
    for key, val in default_stats:
        cursor.execute("INSERT OR IGNORE INTO system_stats (key, value) VALUES (?, ?)", (key, val))

    # Initialize default checklist items if empty
    default_checklist = [
        ("check_syntax", 0),
        ("check_semicolons", 0),
        ("init_variables", 0),
        ("verify_conditions", 0),
        ("check_loop_bounds", 0),
        ("check_array_indices", 0),
        ("validate_pointers", 0),
        ("check_return_values", 0),
        ("match_format_specifiers", 0),
        ("validate_scanf_input", 0),
        ("check_malloc_null", 0),
        ("free_allocated_memory", 0),
        ("compile_with_wall", 0),
        ("test_boundary_inputs", 0)
    ]
    for item_id, status in default_checklist:
        cursor.execute("INSERT OR IGNORE INTO checklist_progress (item_id, is_completed) VALUES (?, ?)", (item_id, status))

    conn.commit()
    conn.close()

def record_analysis(code, bugs_found, bug_categories, title="Custom Code", mode="static_rule_based", hints=1, exec_status="not_run"):
    """Records a code analysis run into the database and increments stats."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cats_str = json.dumps(bug_categories) if isinstance(bug_categories, list) else str(bug_categories)
    cursor.execute("""
        INSERT INTO analysis_history (timestamp, code_snippet, program_title, bugs_found, bug_categories, analysis_mode, hints_unlocked, execution_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), code, title, bugs_found, cats_str, mode, hints, exec_status))
    
    analysis_id = cursor.lastrowid

    # Update stats
    cursor.execute("UPDATE system_stats SET value = value + 1 WHERE key = 'programs_analyzed'")
    cursor.execute("UPDATE system_stats SET value = value + ? WHERE key = 'bugs_identified'", (bugs_found,))
    cursor.execute("UPDATE system_stats SET value = value + ? WHERE key = 'hints_unlocked'", (hints,))

    conn.commit()
    conn.close()
    return analysis_id

def save_rating(analysis_id, clarity, usefulness, accuracy, fix, comments=""):
    """Saves student feedback rating."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tutor_ratings (analysis_id, clarity_score, usefulness_score, accuracy_score, fix_score, feedback_comments)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (analysis_id, clarity, usefulness, accuracy, fix, comments))
    rating_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return rating_id

def get_ratings_summary():
    """Returns average ratings and recent feedback entries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(*) as total_ratings,
            AVG(clarity_score) as avg_clarity,
            AVG(usefulness_score) as avg_usefulness,
            AVG(accuracy_score) as avg_accuracy,
            AVG(fix_score) as avg_fix
        FROM tutor_ratings
    """)
    summary = dict(cursor.fetchone())
    
    cursor.execute("""
        SELECT * FROM tutor_ratings ORDER BY created_at DESC LIMIT 10
    """)
    recent = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return summary, recent

def record_compilation():
    """Increments compilation stats."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE system_stats SET value = value + 1 WHERE key = 'code_compilations'")
    conn.commit()
    conn.close()

def save_quiz_attempt(student_name, score, total_questions, answers_dict):
    """Records quiz score and percentage."""
    percentage = round((score / total_questions) * 100, 1) if total_questions > 0 else 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_attempts (student_name, score, total_questions, percentage, answers_json)
        VALUES (?, ?, ?, ?, ?)
    """, (student_name, score, total_questions, percentage, json.dumps(answers_dict)))
    
    attempt_id = cursor.lastrowid
    cursor.execute("UPDATE system_stats SET value = value + 1 WHERE key = 'quizzes_taken'")
    conn.commit()
    conn.close()
    return attempt_id, percentage

def get_quiz_history():
    """Retrieves all quiz attempts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quiz_attempts ORDER BY completed_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def get_checklist_status():
    """Returns dictionary of checklist item statuses."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_id, is_completed FROM checklist_progress")
    rows = cursor.fetchall()
    conn.close()
    return {row["item_id"]: bool(row["is_completed"]) for row in rows}

def update_checklist_item(item_id, is_completed):
    """Toggles or sets checklist item completion."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO checklist_progress (item_id, is_completed, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(item_id) DO UPDATE SET is_completed = ?, updated_at = CURRENT_TIMESTAMP
    """, (item_id, 1 if is_completed else 0, 1 if is_completed else 0))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    """Retrieves aggregate statistics for the dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM system_stats")
    stats = {row["key"]: row["value"] for row in cursor.fetchall()}

    # Calculate checklist progress percentage
    cursor.execute("SELECT COUNT(*) as total, SUM(is_completed) as completed FROM checklist_progress")
    check_row = cursor.fetchone()
    total_check = check_row["total"] or 1
    completed_check = check_row["completed"] or 0
    checklist_pct = round((completed_check / total_check) * 100)

    # Average quiz score
    cursor.execute("SELECT AVG(percentage) as avg_score, COUNT(*) as count FROM quiz_attempts")
    quiz_row = cursor.fetchone()
    avg_quiz = round(quiz_row["avg_score"], 1) if quiz_row["avg_score"] is not None else 0

    # Recent analyses
    cursor.execute("SELECT * FROM analysis_history ORDER BY id DESC LIMIT 5")
    recent_analyses = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "programs_analyzed": stats.get("programs_analyzed", 0),
        "bugs_identified": stats.get("bugs_identified", 0),
        "hints_unlocked": stats.get("hints_unlocked", 0),
        "quizzes_taken": stats.get("quizzes_taken", 0),
        "code_compilations": stats.get("code_compilations", 0),
        "checklist_percentage": checklist_pct,
        "completed_checklist_items": completed_check,
        "total_checklist_items": total_check,
        "average_quiz_score": avg_quiz,
        "recent_analyses": recent_analyses
    }
