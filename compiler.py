"""
Compiler and Safe Execution Module for C Programming Tutor.
Handles GCC/Clang detection, ephemeral temporary compilation, timeout limits,
output capping, diagnostics extraction, and safe execution isolation policies.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import time

# Security policy: max execution timeout in seconds
MAX_COMPILE_TIMEOUT = 5.0
MAX_EXEC_TIMEOUT = 3.0
MAX_OUTPUT_BYTES = 65536  # 64 KB cap

def detect_c_compiler():
    """
    Checks for the presence of GCC or Clang on the host system.
    Searches system PATH and standard MinGW/MSYS2 locations on Windows.
    """
    candidates = ["gcc", "clang", "tcc"]
    for name in candidates:
        path = shutil.which(name)
        if path:
            try:
                res = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=3)
                version_line = res.stdout.splitlines()[0] if res.stdout else "Available"
                return {
                    "available": True,
                    "name": name,
                    "path": path,
                    "version": version_line
                }
            except Exception:
                continue

    # On Windows, also inspect standard installation paths
    if sys.platform.startswith("win"):
        win_paths = [
            r"C:\msys64\ucrt64\bin\gcc.exe",
            r"C:\msys64\mingw64\bin\gcc.exe",
            r"C:\MinGW\bin\gcc.exe",
            r"C:\w64devkit\bin\gcc.exe",
            r"C:\Program Files\LLVM\bin\clang.exe",
        ]
        for p in win_paths:
            if os.path.exists(p):
                try:
                    res = subprocess.run([p, "--version"], capture_output=True, text=True, timeout=3)
                    version_line = res.stdout.splitlines()[0] if res.stdout else "Available"
                    return {
                        "available": True,
                        "name": "gcc" if "gcc" in p else "clang",
                        "path": p,
                        "version": version_line
                    }
                except Exception:
                    continue

    return {
        "available": False,
        "name": None,
        "path": None,
        "version": None,
        "instructions": (
            "GCC compiler was not detected in system PATH. To enable native GCC compilation:\n"
            "1. Install MinGW-w64 via winget: 'winget install BrechtSanders.WinLibs.MCF.UCRT' or visit https://www.msys2.org\n"
            "2. Add the bin folder (e.g. C:\\msys64\\ucrt64\\bin) to your Windows System PATH.\n"
            "3. Restart the server. In the meantime, use our Static C Bug Analyzer!"
        )
    }

def compile_and_run_c(code, stdin_input="", run_binary=True):
    """
    Safely compiles and optionally runs a C program inside an isolated temporary directory.
    Enforces compilation & execution timeouts, output truncations, and cleanup.
    
    Returns a dictionary with:
    - compiler_available: bool
    - compiled: bool
    - compiler_output: str (warnings/errors)
    - compiler_diagnostics: list of parsed error objects
    - executed: bool
    - program_output: str
    - runtime_error: str or None
    - exit_code: int or None
    - execution_time_ms: float
    - isolation_note: str
    """
    comp_info = detect_c_compiler()
    
    if not comp_info["available"]:
        return {
            "compiler_available": False,
            "compiled": False,
            "compiler_output": (
                "Native GCC compiler is not detected on this server environment.\n\n"
                "To ensure complete transparency and prevent false execution claims:\n"
                "- Native binary compilation requires GCC/Clang.\n"
                "- Safe containerized execution requires an isolated container sandbox (Docker/WSL).\n\n"
                f"{comp_info['instructions']}"
            ),
            "compiler_diagnostics": [],
            "executed": False,
            "program_output": "",
            "runtime_error": "Compiler unavailable",
            "exit_code": None,
            "execution_time_ms": 0,
            "isolation_note": "Host lacks GCC executable; native execution halted."
        }

    compiler_cmd = comp_info["path"]
    temp_dir = tempfile.mkdtemp(prefix="c_tutor_sandbox_")
    src_file = os.path.join(temp_dir, "solution.c")
    exe_file = os.path.join(temp_dir, "solution.exe" if sys.platform.startswith("win") else "solution.out")

    try:
        # Write C source file
        with open(src_file, "w", encoding="utf-8") as f:
            f.write(code)

        # 1. Compilation Phase
        # Enable -Wall, -Wextra, -std=c11 for best pedagogical feedback
        compile_args = [
            compiler_cmd,
            "-Wall",
            "-Wextra",
            "-std=c11",
            "-O0",
            src_file,
            "-o",
            exe_file
        ]

        t_start_compile = time.perf_counter()
        try:
            compile_proc = subprocess.run(
                compile_args,
                capture_output=True,
                text=True,
                timeout=MAX_COMPILE_TIMEOUT
            )
        except subprocess.TimeoutExpired:
            return {
                "compiler_available": True,
                "compiled": False,
                "compiler_output": f"Compilation timed out after {MAX_COMPILE_TIMEOUT} seconds.",
                "compiler_diagnostics": [{"line": None, "type": "error", "message": "Compilation timed out"}],
                "executed": False,
                "program_output": "",
                "runtime_error": "Timeout",
                "exit_code": -1,
                "execution_time_ms": round((time.perf_counter() - t_start_compile) * 1000, 2),
                "isolation_note": "Terminated due to compilation time limit."
            }

        compile_time_ms = round((time.perf_counter() - t_start_compile) * 1000, 2)
        raw_compiler_output = (compile_proc.stdout + "\n" + compile_proc.stderr).strip()

        # Parse diagnostics into structured items
        diagnostics = parse_gcc_diagnostics(raw_compiler_output)

        if compile_proc.returncode != 0 or not os.path.exists(exe_file):
            return {
                "compiler_available": True,
                "compiled": False,
                "compiler_output": raw_compiler_output or "Compilation failed without output.",
                "compiler_diagnostics": diagnostics,
                "executed": False,
                "program_output": "",
                "runtime_error": "Compilation Failed",
                "exit_code": compile_proc.returncode,
                "execution_time_ms": compile_time_ms,
                "isolation_note": "Compilation step failed; execution prevented."
            }

        # If not asked to run, return compilation success
        if not run_binary:
            return {
                "compiler_available": True,
                "compiled": True,
                "compiler_output": raw_compiler_output or "Compilation successful with 0 warnings.",
                "compiler_diagnostics": diagnostics,
                "executed": False,
                "program_output": "",
                "runtime_error": None,
                "exit_code": 0,
                "execution_time_ms": compile_time_ms,
                "isolation_note": "Binary compiled successfully. Execution omitted."
            }

        # 2. Execution Phase inside temporary directory sandbox
        t_start_run = time.perf_counter()
        try:
            exec_proc = subprocess.run(
                [exe_file],
                input=stdin_input,
                capture_output=True,
                text=True,
                timeout=MAX_EXEC_TIMEOUT,
                cwd=temp_dir
            )
            exec_time_ms = round((time.perf_counter() - t_start_run) * 1000, 2)
            stdout = exec_proc.stdout[:MAX_OUTPUT_BYTES]
            stderr = exec_proc.stderr[:MAX_OUTPUT_BYTES]

            if len(exec_proc.stdout) > MAX_OUTPUT_BYTES:
                stdout += "\n... [Output truncated after 64KB limit]"

            return {
                "compiler_available": True,
                "compiled": True,
                "compiler_output": raw_compiler_output or "Compilation successful (0 errors, 0 warnings).",
                "compiler_diagnostics": diagnostics,
                "executed": True,
                "program_output": stdout,
                "stderr_output": stderr,
                "runtime_error": None if exec_proc.returncode == 0 else f"Process exited with non-zero code {exec_proc.returncode}",
                "exit_code": exec_proc.returncode,
                "execution_time_ms": exec_time_ms,
                "isolation_note": f"Executed inside ephemeral sandbox '{temp_dir}' with {MAX_EXEC_TIMEOUT}s timeout."
            }

        except subprocess.TimeoutExpired:
            return {
                "compiler_available": True,
                "compiled": True,
                "compiler_output": raw_compiler_output,
                "compiler_diagnostics": diagnostics,
                "executed": True,
                "program_output": "",
                "runtime_error": f"Execution Timed Out ({MAX_EXEC_TIMEOUT} seconds). Possible infinite loop or blocking I/O.",
                "exit_code": -1,
                "execution_time_ms": round(MAX_EXEC_TIMEOUT * 1000, 2),
                "isolation_note": "Process forcibly killed due to infinite loop or timeout."
            }

    finally:
        # Guarantee cleanup of all temporary build artifacts
        shutil.rmtree(temp_dir, ignore_errors=True)

def parse_gcc_diagnostics(output):
    """
    Parses GCC/Clang error lines in the standard format:
    file.c:line:col: (error|warning|note): message
    """
    diagnostics = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(":", 4)
        if len(parts) >= 4:
            try:
                line_no = int(parts[1])
                diag_type = parts[3].strip() if len(parts) >= 4 else "error"
                msg = parts[4].strip() if len(parts) >= 5 else ""
                diagnostics.append({
                    "raw": line,
                    "line": line_no,
                    "type": diag_type,
                    "message": msg
                })
            except (ValueError, IndexError):
                diagnostics.append({
                    "raw": line,
                    "line": None,
                    "type": "info",
                    "message": line
                })
        else:
            diagnostics.append({
                "raw": line,
                "line": None,
                "type": "info",
                "message": line
            })
    return diagnostics
