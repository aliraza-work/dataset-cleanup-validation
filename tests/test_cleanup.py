import unittest
from src.cleanup import clean

class CleanupTests(unittest.TestCase):
    def test_flags_missing_and_duplicates(self):
        rows = [
            {"id": "1", "name": "Ali"},
            {"id": "1", "name": "Ali"},
            {"id": "", "name": "Sara"},
        ]
        result = clean(rows, ["id", "name"])
        self.assertEqual(result["stats"]["cleaned"], 1)
        self.assertEqual(result["stats"]["flagged"], 2)

if __name__ == "__main__":
    unittest.main()
