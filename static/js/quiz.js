/**
 * Quiz Module Client Controller
 * Manages question selection, grading submission, answer explanation reveals, and retry.
 */

document.addEventListener("DOMContentLoaded", () => {
    const quizForm = document.getElementById("quizForm");
    if (quizForm) {
        quizForm.addEventListener("submit", handleQuizSubmit);
    }

    const retakeBtn = document.getElementById("retakeQuizBtn");
    if (retakeBtn) {
        retakeBtn.addEventListener("click", resetQuiz);
    }
});

function handleQuizSubmit(e) {
    e.preventDefault();

    const form = document.getElementById("quizForm");
    const formData = new FormData(form);
    const answers = {};

    formData.forEach((val, key) => {
        if (key.startsWith("q_")) {
            const qId = key.replace("q_", "");
            answers[qId] = parseInt(val);
        }
    });

    const studentName = document.getElementById("studentNameInput")?.value || "Student";
    const totalQuestions = document.querySelectorAll(".quiz-question-card").length;

    if (Object.keys(answers).length < totalQuestions) {
        if (!confirm(`You have only answered ${Object.keys(answers).length} out of ${totalQuestions} questions. Do you still want to submit?`)) {
            return;
        }
    }

    const submitBtn = document.getElementById("submitQuizBtn");
    if (submitBtn) {
        submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Grading...`;
        submitBtn.disabled = true;
    }

    fetch("/api/quiz/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            student_name: studentName,
            answers: answers
        })
    })
    .then(res => res.json())
    .then(data => {
        renderQuizResults(data);
    })
    .catch(err => {
        if (submitBtn) {
            submitBtn.innerHTML = `<i class="fas fa-paper-plane"></i> Submit Answers`;
            submitBtn.disabled = false;
        }
        showToast("Error submitting quiz: " + err.message, "error");
    });
}

function renderQuizResults(data) {
    // Hide form, show results view
    document.getElementById("quizFormContainer").style.display = "none";
    const resultsView = document.getElementById("quizResultsView");
    resultsView.style.display = "block";

    // Set summary values
    document.getElementById("resScore").textContent = `${data.score} / ${data.total}`;
    document.getElementById("resPercentage").textContent = `${data.percentage}%`;

    const gradeBadge = document.getElementById("resGradeBadge");
    if (data.percentage >= 80) {
        gradeBadge.className = "badge badge-emerald";
        gradeBadge.textContent = "Mastery Achieved (Excellent)";
    } else if (data.percentage >= 50) {
        gradeBadge.className = "badge badge-cyan";
        gradeBadge.textContent = "Passing Score (Good Progress)";
    } else {
        gradeBadge.className = "badge badge-rose";
        gradeBadge.textContent = "Needs Review (Practice More)";
    }

    // Render detailed question breakdown
    const breakdownContainer = document.getElementById("answersBreakdownList");
    if (breakdownContainer) {
        let html = "";
        data.results.forEach((r, idx) => {
            const isCorrect = r.is_correct;
            html += `
                <div class="card" style="margin-bottom: 18px; border-left: 4px solid ${isCorrect ? 'var(--success)' : 'var(--danger)'};">
                    <div class="card-header" style="background: rgba(15, 23, 42, 0.4);">
                        <span style="font-weight: 600; font-size: 14px; color: #fff;">
                            ${idx + 1}. ${escapeHtml(r.question)}
                        </span>
                        <span class="badge ${isCorrect ? 'badge-emerald' : 'badge-rose'}">
                            <i class="fas ${isCorrect ? 'fa-check' : 'fa-times'}"></i> ${isCorrect ? 'Correct (+1)' : 'Incorrect (0)'}
                        </span>
                    </div>
                    <div class="card-body">
                        <div style="font-size: 13.5px; margin-bottom: 10px;">
                            <div><strong>Your Choice:</strong> <span style="color: ${isCorrect ? 'var(--success)' : 'var(--danger)'};">${r.selected_option !== -1 ? escapeHtml(r.options[r.selected_option]) : 'Not answered'}</span></div>
                            ${!isCorrect ? `<div><strong>Correct Answer:</strong> <span style="color: var(--success); font-weight: 600;">${escapeHtml(r.options[r.correct_option])}</span></div>` : ''}
                        </div>
                        <div style="background: rgba(56, 189, 248, 0.05); padding: 12px; border-radius: 6px; border: 1px solid var(--border-subtle); font-size: 13px; color: #cbd5e1;">
                            <strong style="color: var(--primary-cyan);"><i class="fas fa-info-circle"></i> Explanation:</strong> ${escapeHtml(r.explanation)}
                        </div>
                    </div>
                </div>
            `;
        });
        breakdownContainer.innerHTML = html;
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
    showToast(`Quiz completed! Score: ${data.score}/${data.total}`, "success");
}

function resetQuiz() {
    const form = document.getElementById("quizForm");
    if (form) form.reset();

    document.getElementById("quizResultsView").style.display = "none";
    document.getElementById("quizFormContainer").style.display = "block";

    const submitBtn = document.getElementById("submitQuizBtn");
    if (submitBtn) {
        submitBtn.innerHTML = `<i class="fas fa-paper-plane"></i> Submit Answers`;
        submitBtn.disabled = false;
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
}

function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
}
