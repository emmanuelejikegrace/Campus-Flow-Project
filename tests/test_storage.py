import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from campusflow import storage


class TestStorage(unittest.TestCase):
    def test_missing_file_returns_empty(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "nope.json")
            self.assertEqual(storage.load(path), [])

    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.json")
            data = [{"id": "T001", "title": "x"}]
            storage.save(data, path)
            self.assertEqual(storage.load(path), data)

    def test_corrupt_raises(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "bad.json")
            with open(path, "w") as f:
                f.write("{not valid json")
            with self.assertRaises(RuntimeError):
                storage.load(path)


if __name__ == "__main__":
    unittest.main()