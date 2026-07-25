from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import BitGraph  # noqa: E402
from verifier_b import Graph  # noqa: E402


class PublishedCatalogShapeTests(unittest.TestCase):
    def test_mmv2022_table9_is_exactly_2_plus_54_unique_records(self) -> None:
        path = CAMPAIGN / "instances" / "mmv2022_table9.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 56)
        self.assertEqual(len({row["catalog_id"] for row in rows}), 56)
        self.assertEqual(len({row["graph6"] for row in rows}), 56)
        self.assertEqual(sum(row["n"] == "10" for row in rows), 2)
        self.assertEqual(sum(row["n"] == "11" for row in rows), 54)
        for row in rows:
            with self.subTest(catalog_id=row["catalog_id"]):
                self.assertEqual(BitGraph.from_graph6(row["graph6"]).n, int(row["n"]))
                self.assertEqual(Graph.from_graph6(row["graph6"]).order, int(row["n"]))


if __name__ == "__main__":
    unittest.main()
