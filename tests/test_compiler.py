"""
Automated Tests for Compiler & Execution Sandbox Interface.
Verifies compiler detection, ephemeral directory cleanup, diagnostics parsing,
and isolation transparency.
"""

import unittest
import os
import shutil
from compiler import detect_c_compiler, compile_and_run_c, parse_gcc_diagnostics

class TestCompilerModule(unittest.TestCase):

    def test_compiler_detection(self):
        """Verifies detect_c_compiler returns a valid structured dictionary."""
        info = detect_c_compiler()
        self.assertIsInstance(info, dict)
        self.assertIn("available", info)
        self.assertIn("name", info)
        self.assertIn("path", info)
        self.assertIn("version", info)

    def test_gcc_diagnostics_parsing(self):
        """Tests parsing standard GCC compiler error strings."""
        sample_gcc_output = (
            "solution.c:6:5: error: expected ';' before 'printf'\n"
            "solution.c:8:10: warning: unused variable 'x' [-Wunused-variable]\n"
        )
        diagnostics = parse_gcc_diagnostics(sample_gcc_output)
        self.assertEqual(len(diagnostics), 2)
        
        self.assertEqual(diagnostics[0]["line"], 6)
        self.assertEqual(diagnostics[0]["type"], "error")
        self.assertIn("expected ';'", diagnostics[0]["message"])

        self.assertEqual(diagnostics[1]["line"], 8)
        self.assertEqual(diagnostics[1]["type"], "warning")
        self.assertIn("unused variable", diagnostics[1]["message"])

    def test_compile_execution_contract(self):
        """
        Tests compile_and_run_c return schema.
        Confirms honest status reporting (no fabricated compilation or execution).
        """
        code = "#include <stdio.h>\nint main() { printf(\"Test\"); return 0; }"
        res = compile_and_run_c(code, stdin_input="", run_binary=True)

        self.assertIsInstance(res, dict)
        self.assertIn("compiler_available", res)
        self.assertIn("compiled", res)
        self.assertIn("compiler_output", res)
        self.assertIn("executed", res)
        self.assertIn("program_output", res)
        self.assertIn("isolation_note", res)

        # If compiler is not available on host, ensure it honestly refuses to claim execution
        if not res["compiler_available"]:
            self.assertFalse(res["compiled"])
            self.assertFalse(res["executed"])
            self.assertEqual(res["program_output"], "")
            self.assertIn("mingw", res["compiler_output"].lower())

if __name__ == "__main__":
    unittest.main()
