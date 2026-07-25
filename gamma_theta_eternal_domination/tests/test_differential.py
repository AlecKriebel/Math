from __future__ import annotations

import sys
import unittest
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from search.differential import compare_graph  # noqa: E402


class DifferentialSmokeTest(unittest.TestCase):
    def test_named_and_published_graphs_all_k(self) -> None:
        for record in ("A_", "Bg", "Dhc", "IEhbtj{ro", "IEhbtn{ro"):
            with self.subTest(graph6=record):
                compare_graph(record, check_all_guard_counts=True)


if __name__ == "__main__":
    unittest.main()
