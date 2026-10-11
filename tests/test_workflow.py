import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from campusflow import tickets, workflow


def make_open_assigned():
    t = {
        "id": "T001", "title": "x", "category": "Network",
        "urgency": "low", "affected_users": 1, "priority": "low",
        "status": "open", "assigned_to": "Ada",
    }
    return [t]


class TestWorkflow(unittest.TestCase):
    def test_unassigned_cannot_start(self):
        t = make_open_assigned()
        t[0]["assigned_to"] = None
        ok, _ = workflow.start_progress(t, "T001")
        self.assertFalse(ok)
        self.assertEqual(t[0]["status"], "open")

    def test_assigned_can_start(self):
        t = make_open_assigned()
        ok, _ = workflow.start_progress(t, "T001")
        self.assertTrue(ok)
        self.assertEqual(t[0]["status"], "in_progress")

    def test_resolve_requires_in_progress(self):
        t = make_open_assigned()
        ok, _ = workflow.resolve(t, "T001")
        self.assertFalse(ok)

        workflow.start_progress(t, "T001")
        ok, _ = workflow.resolve(t, "T001")
        self.assertTrue(ok)
        self.assertEqual(t[0]["status"], "resolved")

    def test_reopen_requires_resolved(self):
        t = make_open_assigned()
        ok, _ = workflow.reopen(t, "T001")
        self.assertFalse(ok)

        workflow.start_progress(t, "T001")
        workflow.resolve(t, "T001")
        ok, _ = workflow.reopen(t, "T001")
        self.assertTrue(ok)
        self.assertEqual(t[0]["status"], "open")

    def test_assign_rejects_unknown_id(self):
        ok, _ = workflow.assign([], "T999", "Ada")
        self.assertFalse(ok)

    def test_assign_rejects_blank_name(self):
        t = make_open_assigned()
        ok, _ = workflow.assign(t, "T001", "   ")
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()