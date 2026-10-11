import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from campusflow import tickets


class TestPriority(unittest.TestCase):
    def test_rule1_critical(self):
        self.assertEqual(tickets.calculate_priority("high", 10), "critical")
        self.assertEqual(tickets.calculate_priority("high", 15), "critical")

    def test_rule2_high(self):
        self.assertEqual(tickets.calculate_priority("high", 2), "high")
        self.assertEqual(tickets.calculate_priority("low", 10), "high")

    def test_rule3_medium(self):
        self.assertEqual(tickets.calculate_priority("medium", 1), "medium")
        self.assertEqual(tickets.calculate_priority("low", 3), "medium")

    def test_rule4_low(self):
        self.assertEqual(tickets.calculate_priority("low", 2), "low")

    def test_boundaries(self):
        self.assertEqual(tickets.calculate_priority("high", 9), "high")
        self.assertEqual(tickets.calculate_priority("low", 9), "medium")


class TestValidation(unittest.TestCase):
    def test_affected_users_rejects(self):
        for bad in ["0", "-1", "3.5", "abc", "", "   "]:
            self.assertIsNone(tickets.parse_affected_users(bad), msg=bad)

    def test_affected_users_accepts(self):
        self.assertEqual(tickets.parse_affected_users("15"), 15)

    def test_category_case(self):
        self.assertEqual(tickets.normalize_category("NETWORK"), "Network")
        self.assertEqual(tickets.normalize_category(" network "), "Network")
        self.assertIsNone(tickets.normalize_category("banana"))

    def test_urgency_case(self):
        self.assertEqual(tickets.normalize_urgency("HIGH"), "high")
        self.assertIsNone(tickets.normalize_urgency("urgent"))

    def test_blank_title_rejected(self):
        t, err = tickets.create_ticket([], "   ", "Network", "high", "5")
        self.assertIsNone(t)
        self.assertIsNotNone(err)


class TestId(unittest.TestCase):
    def test_first_id(self):
        self.assertEqual(tickets.next_id([]), "T001")

    def test_id_after_gap(self):
        existing = [{"id": "T001"}, {"id": "T003"}]
        self.assertEqual(tickets.next_id(existing), "T004")


if __name__ == "__main__":
    unittest.main()