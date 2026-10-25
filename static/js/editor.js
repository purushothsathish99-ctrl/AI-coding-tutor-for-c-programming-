/**
 * Editor Module for AI Coding Tutor for C Programming
 * Integrates Monaco Editor / textarea fallback, compiler requests, and sample loading.
 */

let editorInstance = null;
let currentCode = "";

const DEFAULT_C_CODE = `#include <stdio.h>

int main() {
    printf("Hello, C Programming World!\\n");
    return 0;
}
`;

document.addEventListener("DOMContentLoaded", () => {
    initEditor();
    bindEditorActions();
});

function initEditor() {
    const container = document.getElementById("monacoEditorContainer");
    const fallback = document.getElementById("fallbackCodeArea");
    const initialCodeVal = window.initialCodeData || DEFAULT_C_CODE;

    // Check if Monaco loader is present
    if (window.monaco) {
        setupMonaco(initialCodeVal);
    } else if (window.require) {
        window.require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' } });
        window.require(['vs/editor/editor.main'], () => {
            setupMonaco(initialCodeVal);
        }, () => {
            enableFallbackEditor(initialCodeVal);
        });
    } else {
        enableFallbackEditor(initialCodeVal);
    }
}

function setupMonaco(code) {
    const container = document.getElementById("monacoEditorContainer");
    if (!container) return;

    try {
        editorInstance = monaco.editor.create(container, {
            value: code,
            language: 'c',
            theme: 'vs-dark',
            automaticLayout: true,
            fontSize: 14,
            fontFamily: "'Fira Code', 'JetBrains Mono', Consolas, monospace",
            minimap: { enabled: false },
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            roundedSelection: true,
            cursorBlinking: 'smooth',
            padding: { top: 12, bottom: 12 }
        });

        // Hide fallback textarea
        const fallback = document.getElementById("fallbackCodeArea");
        if (fallback) fallback.style.display = "none";
        container.style.display = "block";
    } catch (e) {
        enableFallbackEditor(code);
    }
}

function enableFallbackEditor(code) {
    const container = document.getElementById("monacoEditorContainer");
    const fallback = document.getElementById("fallbackCodeArea");
    if (container) container.style.display = "none";
    if (fallback) {
        fallback.style.display = "block";
        fallback.value = code;
    }
}

function getEditorCode() {
    if (editorInstance) {
        return editorInstance.getValue();
    }
    const fallback = document.getElementById("fallbackCodeArea");
    return fallback ? fallback.value : "";
}

function setEditorCode(code) {
    if (editorInstance) {
        editorInstance.setValue(code);
    }
    const fallback = document.getElementById("fallbackCodeArea");
    if (fallback) {
        fallback.value = code;
    }
}

function bindEditorActions() {
    // 1. Sample Program Selector
    const sampleSelect = document.getElementById("sampleProgramSelect");
    if (sampleSelect) {
        sampleSelect.addEventListener("change", (e) => {
            const progId = e.target.value;
            if (!progId) return;

            fetch(`/api/program/${progId}`)
                .then(res => res.json())
                .then(data => {
                    if (data.status === "success" && data.program) {
                        setEditorCode(data.program.buggy_code);
                        showToast(`Loaded: ${data.program.title}`, "info");
                        // Clear previous outputs
                        clearOutputs();
                    }
                })
                .catch(() => showToast("Error loading program", "error"));
        });
    }

    // 2. Reset Button
    const resetBtn = document.getElementById("resetCodeBtn");
    if (resetBtn) {
        resetBtn.addEventListener("click", () => {
            if (confirm("Reset editor to initial template?")) {
                setEditorCode(DEFAULT_C_CODE);
                clearOutputs();
                showToast("Editor reset to default C boilerplate", "info");
            }
        });
    }

    // 3. Clear Button
    const clearBtn = document.getElementById("clearCodeBtn");
    if (clearBtn) {
        clearBtn.addEventListener("click", () => {
            setEditorCode("");
            clearOutputs();
            showToast("Editor cleared", "info");
        });
    }

    // 4. Output Tab Switching
    const tabBtns = document.querySelectorAll(".output-tab-btn");
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const tabKey = btn.dataset.tab;
            document.querySelectorAll(".output-tab-panel").forEach(p => p.style.display = "none");
            const activePanel = document.getElementById(`panel_${tabKey}`);
            if (activePanel) activePanel.style.display = "block";
        });
    });

    // 5. Compile & Run Button
    const runBtn = document.getElementById("compileRunBtn");
    if (runBtn) {
        runBtn.addEventListener("click", handleCompileAndRun);
    }

    // 6. Analyze Code Button
    const analyzeBtn = document.getElementById("analyzeCodeBtn");
    if (analyzeBtn) {
        analyzeBtn.addEventListener("click", () => {
            const code = getEditorCode();
            sessionStorage.setItem("c_tutor_active_code", code);
            window.location.href = "/analyzer";
        });
    }
}

function handleCompileAndRun() {
    const code = getEditorCode();
    if (!code.trim()) {
        showToast("Please enter some C code before compiling!", "error");
        return;
    }

    const runBtn = document.getElementById("compileRunBtn");
    const originalText = runBtn.innerHTML;
    runBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Compiling...`;
    runBtn.disabled = true;

    const stdinInput = document.getElementById("stdinInputField") ? document.getElementById("stdinInputField").value : "";

    fetch("/api/compile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: code,
            stdin: stdinInput,
            run: true
        })
    })
    .then(res => res.json())
    .then(data => {
        runBtn.innerHTML = originalText;
        runBtn.disabled = false;
        renderExecutionResults(data);
    })
    .catch(err => {
        runBtn.innerHTML = originalText;
        runBtn.disabled = false;
        showToast("Execution request failed: " + err.message, "error");
    });
}

function renderExecutionResults(res) {
    const outputConsole = document.getElementById("outputConsole");
    const diagnosticsConsole = document.getElementById("diagnosticsConsole");
    const execDetailsConsole = document.getElementById("execDetailsConsole");

    // 1. Program Output Panel
    if (outputConsole) {
        if (res.executed) {
            outputConsole.textContent = res.program_output || "[Program finished with no output]";
            if (res.runtime_error) {
                outputConsole.textContent += `\n\n[Runtime Error: ${res.runtime_error}]`;
            }
        } else if (!res.compiled) {
            outputConsole.textContent = `[Compilation Failed]\nSwitch to 'Diagnostics' tab to inspect compiler warnings and errors.`;
        } else {
            outputConsole.textContent = res.compiler_output || "[No output]";
        }
    }

    // 2. Diagnostics Panel
    if (diagnosticsConsole) {
        let diagText = "";
        if (!res.compiler_available) {
            diagText = `[COMPILER NOTICE]\n${res.compiler_output}\n\n[ISOLATION & SECURITY]\n${res.isolation_note}`;
        } else {
            diagText = `Compiler: GCC/Clang\nStatus: ${res.compiled ? 'Compilation Succeeded' : 'Compilation Failed'}\n\n`;
            diagText += res.compiler_output || "No warnings or errors reported.";
        }
        diagnosticsConsole.textContent = diagText;
    }

    // 3. Execution Details Panel
    if (execDetailsConsole) {
        execDetailsConsole.innerHTML = `
            <div style="line-height: 1.8;">
                <div><strong>Compiler Available:</strong> ${res.compiler_available ? 'Yes (GCC/Clang)' : 'No (Host lacks GCC)'}</div>
                <div><strong>Compilation Status:</strong> ${res.compiled ? '<span style="color:var(--success)">Success (Exit 0)</span>' : '<span style="color:var(--danger)">Failed</span>'}</div>
                <div><strong>Execution Attempted:</strong> ${res.executed ? 'Yes' : 'No'}</div>
                <div><strong>Execution Time:</strong> ${res.execution_time_ms} ms</div>
                <div><strong>Exit Code:</strong> ${res.exit_code !== null ? res.exit_code : 'N/A'}</div>
                <div><strong>Sandbox Environment:</strong> ${res.isolation_note}</div>
            </div>
        `;
    }

    // Automatically switch to Diagnostics tab if compilation failed
    if (!res.compiled) {
        document.querySelector("[data-tab='diagnostics']").click();
        showToast("Compilation failed. Check diagnostics!", "error");
    } else {
        document.querySelector("[data-tab='output']").click();
        showToast("Compilation finished!", "success");
    }
}

function clearOutputs() {
    const outputConsole = document.getElementById("outputConsole");
    const diagnosticsConsole = document.getElementById("diagnosticsConsole");
    const execDetailsConsole = document.getElementById("execDetailsConsole");
    if (outputConsole) outputConsole.textContent = "Ready. Click 'Compile & Run' to execute code.";
    if (diagnosticsConsole) diagnosticsConsole.textContent = "No compiler diagnostics generated yet.";
    if (execDetailsConsole) execDetailsConsole.textContent = "Execution details will appear here after running.";
}
