"""
AI Coding Tutor for C Programming - Flask Application.
Complete web application supporting 10 modules:
- Dashboard, Code Editor, AI Bug Analyzer, Buggy C Library,
- AI Tutor Chat, Debugging Checklist, Beginner Mistakes Guide,
- Quiz Module, Learning Progress, and Research Documentation / Prompts.
"""

import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import (
    init_db, record_analysis, save_rating, get_ratings_summary,
    record_compilation, save_quiz_attempt, get_quiz_history,
    get_checklist_status, update_checklist_item, get_dashboard_stats
)
from bug_library import get_all_buggy_programs, get_buggy_program_by_id
from ai_tutor import analyze_c_code, answer_tutor_chat
from compiler import compile_and_run_c, detect_c_compiler
from quiz_data import get_all_quiz_questions, grade_quiz
from mistakes_data import get_all_mistakes
from checklist_data import get_all_checklist_items
from prompts_data import get_all_prompts

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

# Initialize database tables on startup
init_db()

# ----------------- PAGE ROUTES -----------------

@app.route("/")
def index():
    """Home Dashboard."""
    stats = get_dashboard_stats()
    ratings_summary, _ = get_ratings_summary()
    compiler_info = detect_c_compiler()
    return render_template(
        "index.html",
        stats=stats,
        ratings=ratings_summary,
        compiler=compiler_info,
        page_title="Dashboard"
    )

@app.route("/editor")
def editor():
    """C Code Editor with compiler, diagnostics, and sample loader."""
    program_id = request.args.get("load")
    initial_code = ""
    program_title = "Custom Program"

    if program_id:
        prog = get_buggy_program_by_id(program_id)
        if prog:
            initial_code = prog["buggy_code"]
            program_title = prog["title"]

    programs = get_all_buggy_programs()
    compiler_info = detect_c_compiler()
    return render_template(
        "editor.html",
        programs=programs,
        initial_code=initial_code,
        program_title=program_title,
        compiler=compiler_info,
        page_title="C Code Editor"
    )

@app.route("/analyzer")
def analyzer():
    """AI Bug Analyzer with 3-tier progressive hints."""
    programs = get_all_buggy_programs()
    ratings_summary, _ = get_ratings_summary()
    return render_template(
        "analyzer.html",
        programs=programs,
        ratings=ratings_summary,
        page_title="AI Bug Analyzer"
    )

@app.route("/library")
def library():
    """Buggy C Program Library (15 beginner programs)."""
    programs = get_all_buggy_programs()
    categories = sorted(list(set(p["category"] for p in programs)))
    return render_template(
        "library.html",
        programs=programs,
        categories=categories,
        page_title="Buggy C Library"
    )

@app.route("/chat")
def chat():
    """AI Tutor Chat."""
    return render_template("chat.html", page_title="AI Tutor Chat")

@app.route("/checklist")
def checklist():
    """Interactive C Debugging Checklist."""
    items = get_all_checklist_items()
    status_map = get_checklist_status()
    # Enrich items with completion status
    for item in items:
        item["completed"] = status_map.get(item["id"], False)

    completed_count = sum(1 for item in items if item["completed"])
    total_count = len(items)
    percentage = round((completed_count / total_count) * 100) if total_count > 0 else 0

    return render_template(
        "checklist.html",
        items=items,
        completed_count=completed_count,
        total_count=total_count,
        percentage=percentage,
        page_title="Debugging Checklist"
    )

@app.route("/mistakes")
def mistakes():
    """Common Beginner Mistakes Guide."""
    mistakes_list = get_all_mistakes()
    return render_template(
        "mistakes.html",
        mistakes=mistakes_list,
        page_title="Common Mistakes Guide"
    )

@app.route("/quiz")
def quiz():
    """12-Question C Programming Quiz."""
    questions = get_all_quiz_questions()
    history = get_quiz_history()
    return render_template(
        "quiz.html",
        questions=questions,
        history=history,
        page_title="C Knowledge Quiz"
    )

@app.route("/progress")
def progress():
    """Learning Progress & Analytics."""
    stats = get_dashboard_stats()
    quiz_history = get_quiz_history()
    ratings_summary, recent_ratings = get_ratings_summary()
    return render_template(
        "progress.html",
        stats=stats,
        quiz_history=quiz_history,
        ratings=ratings_summary,
        recent_ratings=recent_ratings,
        page_title="Learning Progress"
    )

@app.route("/docs")
def docs():
    """Research, Academic Documentation & GCC References."""
    return render_template("docs.html", page_title="Research & Documentation")

@app.route("/prompts")
def prompts():
    """AI Prompt Library for C Tutoring."""
    all_prompts = get_all_prompts()
    return render_template(
        "prompts.html",
        prompts=all_prompts,
        page_title="AI Prompt Library"
    )

# ----------------- JSON API ENDPOINTS -----------------

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """Performs static code analysis or AI bug detection with 3-tier hints."""
    data = request.get_json() or {}
    code = data.get("code", "")
    hint_level = int(data.get("hint_level", 1))
    title = data.get("title", "Custom Code")

    result = analyze_c_code(code, hint_level=hint_level)
    
    # Extract bug categories for stats tracking
    categories = [issue.get("category", "General") for issue in result.get("issues", [])]
    analysis_id = record_analysis(
        code=code,
        bugs_found=result.get("bugs_count", 0),
        bug_categories=categories,
        title=title,
        mode=result.get("analysis_mode", "static_rule_based"),
        hints=hint_level
    )
    result["analysis_id"] = analysis_id
    return jsonify(result)

@app.route("/api/compile", methods=["POST"])
def api_compile():
    """Compiles C code using safe GCC interface and executes inside sandbox."""
    data = request.get_json() or {}
    code = data.get("code", "")
    stdin_input = data.get("stdin", "")
    run_binary = data.get("run", True)

    result = compile_and_run_c(code, stdin_input=stdin_input, run_binary=run_binary)
    record_compilation()
    return jsonify(result)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Handles conversational questions from students."""
    data = request.get_json() or {}
    question = data.get("message", "")
    code = data.get("code", "")

    response_text = answer_tutor_chat(question, current_code=code)
    return jsonify({
        "status": "success",
        "reply": response_text
    })

@app.route("/api/rate", methods=["POST"])
def api_rate():
    """Saves student tutor quality feedback."""
    data = request.get_json() or {}
    analysis_id = data.get("analysis_id")
    clarity = int(data.get("clarity", 5))
    usefulness = int(data.get("usefulness", 5))
    accuracy = int(data.get("accuracy", 5))
    fix = int(data.get("fix", 5))
    comments = data.get("comments", "")

    rating_id = save_rating(analysis_id, clarity, usefulness, accuracy, fix, comments)
    return jsonify({
        "status": "success",
        "rating_id": rating_id,
        "message": "Thank you for your feedback! Your rating helps improve the AI tutor."
    })

@app.route("/api/quiz/submit", methods=["POST"])
def api_quiz_submit():
    """Evaluates submitted quiz answers and persists score."""
    data = request.get_json() or {}
    student_name = data.get("student_name", "Student").strip() or "Student"
    answers = data.get("answers", {})

    graded = grade_quiz(answers)
    attempt_id, percentage = save_quiz_attempt(
        student_name=student_name,
        score=graded["score"],
        total_questions=graded["total"],
        answers_dict=answers
    )
    graded["attempt_id"] = attempt_id
    graded["student_name"] = student_name
    return jsonify(graded)

@app.route("/api/checklist/toggle", methods=["POST"])
def api_checklist_toggle():
    """Updates checklist item status."""
    data = request.get_json() or {}
    item_id = data.get("item_id")
    is_completed = data.get("completed", False)

    if not item_id:
        return jsonify({"status": "error", "message": "Missing item_id"}), 400

    update_checklist_item(item_id, is_completed)
    status_map = get_checklist_status()
    total = len(status_map)
    completed = sum(1 for v in status_map.values() if v)
    percentage = round((completed / total) * 100) if total > 0 else 0

    return jsonify({
        "status": "success",
        "completed": completed,
        "total": total,
        "percentage": percentage
    })

@app.route("/api/program/<int:prog_id>")
def api_program_detail(prog_id):
    """Retrieves full details for a library program."""
    prog = get_buggy_program_by_id(prog_id)
    if not prog:
        return jsonify({"status": "error", "message": "Program not found"}), 404
    return jsonify({"status": "success", "program": prog})

@app.route("/api/compiler/status")
def api_compiler_status():
    """Returns host compiler availability and sandbox configuration."""
    return jsonify(detect_c_compiler())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
