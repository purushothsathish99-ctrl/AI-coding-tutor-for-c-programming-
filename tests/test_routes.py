"""
Automated Integration Tests for Flask Routes & JSON Endpoints.
Verifies all 10 user views render successfully (HTTP 200) and API endpoints function correctly.
"""

import unittest
import json
from app import app
import database

class TestAppRoutes(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()
        database.init_db()

    def test_all_10_pages_render(self):
        """Verifies HTTP 200 on all 10 core views."""
        routes = [
            "/",
            "/editor",
            "/analyzer",
            "/library",
            "/chat",
            "/checklist",
            "/mistakes",
            "/quiz",
            "/progress",
            "/docs",
            "/prompts"
        ]
        for route in routes:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed to render")

    def test_api_analyze_endpoint(self):
        """Verifies /api/analyze POST endpoint."""
        payload = {
            "code": "#include <stdio.h>\nint main() { printf(\"Test\") return 0; }",
            "hint_level": 1,
            "title": "API Test"
        }
        res = self.client.post("/api/analyze", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("bugs_count", data)
        self.assertIn("issues", data)
        self.assertIn("analysis_id", data)

    def test_api_chat_endpoint(self):
        """Verifies /api/chat POST endpoint."""
        payload = {
            "message": "Explain pointers in simple English",
            "code": ""
        }
        res = self.client.post("/api/chat", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("hotel", data["reply"].lower())

    def test_api_quiz_submit_endpoint(self):
        """Verifies /api/quiz/submit POST endpoint and grading."""
        payload = {
            "student_name": "Integration Tester",
            "answers": {
                "1": 1,  # Option 1 is correct for Q1
                "2": 2   # Option 2 is correct for Q2
            }
        }
        res = self.client.post("/api/quiz/submit", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["total"], 12)
        self.assertGreaterEqual(data["score"], 2)
        self.assertIn("percentage", data)

    def test_api_checklist_toggle_endpoint(self):
        """Verifies /api/checklist/toggle POST endpoint."""
        payload = {
            "item_id": "check_syntax",
            "completed": True
        }
        res = self.client.post("/api/checklist/toggle", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertGreater(data["total"], 0)

    def test_api_rate_endpoint(self):
        """Verifies /api/rate POST endpoint."""
        payload = {
            "analysis_id": 1,
            "clarity": 5,
            "usefulness": 5,
            "accuracy": 4,
            "fix": 5,
            "comments": "Super helpful!"
        }
        res = self.client.post("/api/rate", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")

    def test_api_program_detail_endpoint(self):
        """Verifies /api/program/<id> GET endpoint."""
        res = self.client.get("/api/program/1")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["program"]["id"], 1)

if __name__ == "__main__":
    unittest.main()
