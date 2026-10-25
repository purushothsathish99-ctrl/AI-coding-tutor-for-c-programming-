"""
Automated Tests for AI Bug Analyzer & Tutor Scaffolding.
Verifies detection across all 15 bug categories, progressive 3-tier hints,
and conversational tutoring chatbot responses.
"""

import unittest
from ai_tutor import analyze_c_code, answer_tutor_chat
from bug_library import get_all_buggy_programs, get_buggy_program_by_id

class TestAnalyzerModule(unittest.TestCase):

    def test_library_all_15_programs_detected(self):
        """Verifies that all 15 curated buggy C programs are recognized and categorized."""
        programs = get_all_buggy_programs()
        self.assertEqual(len(programs), 15, "Expected exactly 15 library programs")

        for prog in programs:
            res = analyze_c_code(prog["buggy_code"], hint_level=1)
            self.assertEqual(res["status"], "issues_found", f"Failed to identify issue in Program {prog['id']}: {prog['title']}")
            self.assertGreaterEqual(res["bugs_count"], 1)

            # Check 3-tier hints presence
            issue = res["issues"][0]
            self.assertIn("level1", issue["hints"])
            self.assertIn("level2", issue["hints"])
            self.assertIn("level3", issue["hints"])
            self.assertTrue(len(issue["hints"]["level1"]) > 10)
            self.assertTrue(len(issue["hints"]["level2"]) > 10)
            self.assertTrue(len(issue["hints"]["level3"]) > 10)

    def test_missing_semicolon_detection(self):
        """Tests static detection of missing semicolon on statement lines."""
        code = """#include <stdio.h>
int main() {
    int age = 19;
    printf("Age: %d\\n", age)
    return 0;
}"""
        res = analyze_c_code(code)
        self.assertEqual(res["status"], "issues_found")
        types = [i["bug_type"] for i in res["issues"]]
        self.assertTrue(any("Semicolon" in t for t in types))

    def test_assignment_in_if_condition(self):
        """Tests logical bug detection when '=' is used instead of '=='."""
        code = """#include <stdio.h>
int main() {
    int score = 45;
    if (score = 100) {
        printf("Pass\\n");
    }
    return 0;
}"""
        res = analyze_c_code(code)
        self.assertEqual(res["status"], "issues_found")
        types = [i["bug_type"] for i in res["issues"]]
        self.assertTrue(any("Assignment in Condition" in t for t in types))

    def test_scanf_missing_ampersand(self):
        """Tests detection of missing address-of operator '&' in scanf."""
        code = """#include <stdio.h>
int main() {
    int val;
    scanf("%d", val);
    return 0;
}"""
        res = analyze_c_code(code)
        self.assertEqual(res["status"], "issues_found")
        types = [i["bug_type"] for i in res["issues"]]
        self.assertTrue(any("Missing Address-Of" in t for t in types))

    def test_integer_division_detection(self):
        """Tests arithmetic truncation bug detection."""
        code = """#include <stdio.h>
int main() {
    int total = 450, max = 500;
    float pct = total / max;
    return 0;
}"""
        res = analyze_c_code(code)
        self.assertEqual(res["status"], "issues_found")
        types = [i["bug_type"] for i in res["issues"]]
        self.assertTrue(any("Integer Division" in t for t in types))

    def test_clean_code_validation(self):
        """Tests that well-formed C code returns a clean status."""
        code = """#include <stdio.h>
int main() {
    int count = 10;
    printf("Total items: %d\\n", count);
    return 0;
}"""
        res = analyze_c_code(code)
        self.assertEqual(res["status"], "clean")
        self.assertEqual(res["bugs_count"], 0)

    def test_tutor_chat_responses(self):
        """Tests conversational AI tutor responses for beginner questions."""
        # Pointers explanation
        ptr_reply = answer_tutor_chat("Explain pointers in simple English.")
        self.assertIn("hotel", ptr_reply.lower())
        self.assertIn("dereferencing", ptr_reply.lower())

        # What does this code do
        code_reply = answer_tutor_chat("What does this code do?", current_code="#include <stdio.h>\nint main() { printf(\"Hi\"); return 0; }")
        self.assertIn("Entry Point", code_reply)
        self.assertIn("printf()", code_reply)

        # Practice problem
        practice_reply = answer_tutor_chat("Give me a practice problem")
        self.assertIn("Practice Problem", practice_reply)

if __name__ == "__main__":
    unittest.main()
