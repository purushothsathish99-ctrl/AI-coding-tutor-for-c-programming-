/**
 * AI Bug Analyzer Client Controller
 * Manages 3-tier progressive hint revelation, bug taxonomy rendering,
 * and 5-star student feedback rating.
 */

let activeAnalysisId = null;
let currentIssues = [];
let activeHintLevel = 1;

document.addEventListener("DOMContentLoaded", () => {
    // Check if code was passed from the editor via sessionStorage
    const storedCode = sessionStorage.getItem("c_tutor_active_code");
    const analyzerInput = document.getElementById("analyzerCodeInput");

    if (storedCode && analyzerInput) {
        analyzerInput.value = storedCode;
        // Auto-trigger analysis
        performAnalysis();
    }

    // Program dropdown loader
    const progSelect = document.getElementById("analyzerProgramSelect");
    if (progSelect) {
        progSelect.addEventListener("change", (e) => {
            const progId = e.target.value;
            if (!progId) return;

            fetch(`/api/program/${progId}`)
                .then(res => res.json())
                .then(data => {
                    if (data.status === "success" && data.program) {
                        analyzerInput.value = data.program.buggy_code;
                        performAnalysis();
                    }
                });
        });
    }

    // Analyze Button
    const runBtn = document.getElementById("runAnalyzerBtn");
    if (runBtn) {
        runBtn.addEventListener("click", () => performAnalysis());
    }

    // Rating Form Submission
    const ratingForm = document.getElementById("tutorRatingForm");
    if (ratingForm) {
        ratingForm.addEventListener("submit", handleRatingSubmission);
    }
});

function performAnalysis(requestedLevel = 1) {
    const codeArea = document.getElementById("analyzerCodeInput");
    const code = codeArea ? codeArea.value.trim() : "";

    if (!code) {
        showToast("Please enter or paste some C code to analyze!", "error");
        return;
    }

    activeHintLevel = requestedLevel;
    const runBtn = document.getElementById("runAnalyzerBtn");
    if (runBtn) {
        runBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Analyzing...`;
        runBtn.disabled = true;
    }

    fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: code,
            hint_level: activeHintLevel,
            title: "Analyzer Code"
        })
    })
    .then(res => res.json())
    .then(data => {
        if (runBtn) {
            runBtn.innerHTML = `<i class="fas fa-search"></i> Run AI Analysis`;
            runBtn.disabled = false;
        }

        activeAnalysisId = data.analysis_id;
        currentIssues = data.issues || [];
        renderAnalysisResults(data);
    })
    .catch(err => {
        if (runBtn) {
            runBtn.innerHTML = `<i class="fas fa-search"></i> Run AI Analysis`;
            runBtn.disabled = false;
        }
        showToast("Analysis error: " + err.message, "error");
    });
}

function renderAnalysisResults(data) {
    const resultsContainer = document.getElementById("analysisResultsContainer");
    if (!resultsContainer) return;

    if (data.bugs_count === 0) {
        resultsContainer.innerHTML = `
            <div class="card" style="border-color: var(--success); background: rgba(16, 185, 129, 0.05); padding: 32px; text-align: center;">
                <div style="font-size: 48px; color: var(--success); margin-bottom: 16px;"><i class="fas fa-check-circle"></i></div>
                <h3 style="color: #fff; margin-bottom: 8px;">No Common Beginner Bugs Detected!</h3>
                <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 20px;">
                    Your C code passed our static syntactic and common structural bug checks. You can now compile and test your program in the Code Editor!
                </p>
                <a href="/editor" class="btn btn-primary"><i class="fas fa-terminal"></i> Open in Code Editor</a>
            </div>
        `;
        // Hide rating card if clean
        document.getElementById("ratingSection").style.display = "none";
        return;
    }

    let html = `
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px;">
            <div>
                <h3 style="color: #fff; font-size: 18px;">Identified Issues (${data.bugs_count})</h3>
                <span style="font-size: 12px; color: var(--primary-cyan);">Mode: ${data.analysis_mode}</span>
            </div>
            <div class="badge badge-rose"><i class="fas fa-exclamation-triangle"></i> Bugs Found</div>
        </div>
    `;

    data.issues.forEach((issue, idx) => {
        const hints = issue.hints || {};
        html += `
            <div class="card" style="border-left: 4px solid var(--primary-cyan); margin-bottom: 24px;">
                <div class="card-header">
                    <div class="card-title">
                        <span class="badge badge-amber">${issue.category || 'General'}</span>
                        <span>${issue.bug_type}</span>
                    </div>
                    ${issue.line_number ? `<span class="badge badge-cyan"><i class="fas fa-map-pin"></i> Line ${issue.line_number}</span>` : ''}
                </div>
                <div class="card-body">
                    <!-- Problem Section -->
                    <div style="margin-bottom: 16px;">
                        <h4 style="font-size: 13px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px;">Incorrect Code Section:</h4>
                        <pre style="background: #090d16; padding: 12px; border-radius: 6px; font-family: var(--font-mono); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2);"><code>${escapeHtml(issue.incorrect_code_section || 'N/A')}</code></pre>
                    </div>

                    <!-- Explanation -->
                    <div style="margin-bottom: 16px;">
                        <h4 style="font-size: 13px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px;">Simple-English Explanation:</h4>
                        <p style="color: var(--text-main); font-size: 14px; line-height: 1.5;">${issue.explanation}</p>
                    </div>

                    <!-- Why it occurs -->
                    <div style="margin-bottom: 20px;">
                        <h4 style="font-size: 13px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 4px;">Why the Error Occurs:</h4>
                        <p style="color: var(--text-secondary); font-size: 13.5px; line-height: 1.5;">${issue.why_error_occurs}</p>
                    </div>

                    <!-- 3-Tier Progressive Hint Container -->
                    <div class="hint-container">
                        <div class="hint-tier-nav">
                            <button type="button" class="hint-tier-tab ${activeHintLevel === 1 ? 'active' : ''}" onclick="switchHintTier(${idx}, 1)">
                                <i class="fas fa-lightbulb"></i> Level 1: Subtle Hint
                            </button>
                            <button type="button" class="hint-tier-tab ${activeHintLevel === 2 ? 'active' : ''}" onclick="switchHintTier(${idx}, 2)">
                                <i class="fas fa-compass"></i> Level 2: Concept & Line
                            </button>
                            <button type="button" class="hint-tier-tab ${activeHintLevel === 3 ? 'active' : ''}" onclick="switchHintTier(${idx}, 3)">
                                <i class="fas fa-check-double"></i> Level 3: Solution & Fix
                            </button>
                        </div>
                        <div class="hint-body" id="hintBody_${idx}">
                            ${renderHintTierContent(hints, activeHintLevel, issue)}
                        </div>
                    </div>

                    <!-- Expected output & Takeaway -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 18px;">
                        <div style="background: rgba(15, 23, 42, 0.6); padding: 14px; border-radius: 8px; border: 1px solid var(--border-subtle);">
                            <h5 style="color: var(--primary-cyan); font-size: 12px; text-transform: uppercase; margin-bottom: 6px;"><i class="fas fa-terminal"></i> Expected Output:</h5>
                            <pre style="font-family: var(--font-mono); font-size: 12px; color: #a5f3fc; white-space: pre-wrap;">${escapeHtml(issue.expected_output || 'Program executes without crashing.')}</pre>
                        </div>
                        <div style="background: rgba(16, 185, 129, 0.05); padding: 14px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2);">
                            <h5 style="color: var(--success); font-size: 12px; text-transform: uppercase; margin-bottom: 6px;"><i class="fas fa-graduation-cap"></i> Learning Takeaway:</h5>
                            <p style="font-size: 13px; color: #d1fae5; line-height: 1.4;">${issue.learning_takeaway || 'Always test edge cases and compile with -Wall.'}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    resultsContainer.innerHTML = html;
    document.getElementById("ratingSection").style.display = "block";
}

function switchHintTier(issueIdx, level) {
    activeHintLevel = level;
    const issue = currentIssues[issueIdx];
    if (!issue) return;

    // Update active tab styles
    const tabs = document.querySelectorAll(`.hint-tier-nav button`);
    tabs.forEach((tab, tIdx) => {
        if (tIdx === (level - 1)) tab.classList.add("active");
        else tab.classList.remove("active");
    });

    const body = document.getElementById(`hintBody_${issueIdx}`);
    if (body) {
        body.innerHTML = renderHintTierContent(issue.hints || {}, level, issue);
    }
}

function renderHintTierContent(hints, level, issue) {
    if (level === 1) {
        return `
            <div>
                <span class="hint-badge-level" style="background: rgba(56, 189, 248, 0.2); color: var(--primary-cyan);">Level 1 Hint (Subtle Nudge)</span>
                <p style="font-size: 14.5px; color: #e2e8f0; line-height: 1.5;">${hints.level1 || 'Inspect the statement syntax and variable scope.'}</p>
                <div style="margin-top: 14px;">
                    <button class="btn btn-outline btn-sm" onclick="switchHintTier(0, 2)"><i class="fas fa-arrow-right"></i> Need more guidance? Unlock Level 2</button>
                </div>
            </div>
        `;
    } else if (level === 2) {
        return `
            <div>
                <span class="hint-badge-level" style="background: rgba(245, 158, 11, 0.2); color: var(--warning);">Level 2 Hint (Concept & Faulty Line)</span>
                <p style="font-size: 14.5px; color: #e2e8f0; line-height: 1.5;">${hints.level2 || 'Review the faulty line indicated above.'}</p>
                <div style="margin-top: 14px;">
                    <button class="btn btn-outline btn-sm" onclick="switchHintTier(0, 3)"><i class="fas fa-eye"></i> Ready for solution? Unlock Level 3</button>
                </div>
            </div>
        `;
    } else {
        return `
            <div>
                <span class="hint-badge-level" style="background: rgba(16, 185, 129, 0.2); color: var(--success);">Level 3 Solution (Corrected Code & Explanation)</span>
                <p style="font-size: 14px; color: #cbd5e1; margin-bottom: 12px;">${hints.level3 || 'Here is the corrected syntax:'}</p>
                <pre style="background: #090d16; padding: 14px; border-radius: 6px; font-family: var(--font-mono); color: #86efac; border: 1px solid rgba(16, 185, 129, 0.25);"><code>${escapeHtml(issue.corrected_code || 'See clean code in Buggy Library')}</code></pre>
            </div>
        `;
    }
}

function handleRatingSubmission(e) {
    e.preventDefault();
    if (!activeAnalysisId) {
        showToast("Please analyze a program first before submitting feedback!", "error");
        return;
    }

    const clarity = document.querySelector("input[name='clarity']:checked")?.value || 5;
    const usefulness = document.querySelector("input[name='usefulness']:checked")?.value || 5;
    const accuracy = document.querySelector("input[name='accuracy']:checked")?.value || 5;
    const fix = document.querySelector("input[name='fix']:checked")?.value || 5;
    const comments = document.getElementById("ratingComments")?.value || "";

    fetch("/api/rate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            analysis_id: activeAnalysisId,
            clarity: parseInt(clarity),
            usefulness: parseInt(usefulness),
            accuracy: parseInt(accuracy),
            fix: parseInt(fix),
            comments: comments
        })
    })
    .then(res => res.json())
    .then(data => {
        showToast("Thank you for rating the AI Tutor!", "success");
        const submitBtn = document.getElementById("submitRatingBtn");
        if (submitBtn) {
            submitBtn.textContent = "Feedback Submitted ✓";
            submitBtn.disabled = true;
        }
    })
    .catch(() => showToast("Failed to submit rating", "error"));
}

function escapeHtml(text) {
    if (!text) return "";
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
