"""
Automated Tests for Database Operations (SQLite).
Tests schema initialization, analysis recording, ratings, quiz scores, and checklist state.
"""

import os
import unittest
import database

class TestDatabaseModule(unittest.TestCase):
    def setUp(self):
        # Initialize DB
        database.init_db()

    def test_database_init(self):
        """Verifies tables are created and initial stats exist."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row["name"] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("analysis_history", tables)
        self.assertIn("tutor_ratings", tables)
        self.assertIn("quiz_attempts", tables)
        self.assertIn("checklist_progress", tables)
        self.assertIn("system_stats", tables)

    def test_record_analysis_and_stats(self):
        """Verifies that recording an analysis persists data and updates counters."""
        init_stats = database.get_dashboard_stats()
        prog_count_before = init_stats["programs_analyzed"]

        aid = database.record_analysis(
            code="#include <stdio.h>\nint main() { return 0; }",
            bugs_found=1,
            bug_categories=["Syntax Error"],
            title="Unit Test Code",
            mode="static_rule_based",
            hints=1
        )
        self.assertIsNotNone(aid)
        self.assertGreater(aid, 0)

        updated_stats = database.get_dashboard_stats()
        self.assertEqual(updated_stats["programs_analyzed"], prog_count_before + 1)

    def test_save_rating(self):
        """Verifies student tutor rating storage."""
        rid = database.save_rating(
            analysis_id=1,
            clarity=5,
            usefulness=4,
            accuracy=5,
            fix=4,
            comments="Very clear explanation of off-by-one errors."
        )
        self.assertIsNotNone(rid)

        summary, recent = database.get_ratings_summary()
        self.assertGreater(summary["total_ratings"], 0)
        self.assertGreaterEqual(summary["avg_clarity"], 1.0)

    def test_checklist_toggle(self):
        """Verifies checklist status update and percentage calculation."""
        database.update_checklist_item("check_syntax", True)
        status_map = database.get_checklist_status()
        self.assertTrue(status_map.get("check_syntax"))

        database.update_checklist_item("check_syntax", False)
        status_map = database.get_checklist_status()
        self.assertFalse(status_map.get("check_syntax"))

    def test_quiz_attempt_recording(self):
        """Verifies quiz scoring persistence."""
        attempt_id, percentage = database.save_quiz_attempt(
            student_name="Test Student",
            score=10,
            total_questions=12,
            answers_dict={"1": 1, "2": 2}
        )
        self.assertIsNotNone(attempt_id)
        self.assertAlmostEqual(percentage, 83.3, places=1)

        history = database.get_quiz_history()
        self.assertGreater(len(history), 0)
        self.assertEqual(history[0]["student_name"], "Test Student")

if __name__ == "__main__":
    unittest.main()
