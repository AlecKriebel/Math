#!/usr/bin/env python3

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from catalog42_e2_extension_cnf import build_formula  # noqa: E402
from catalog42_e2_extension_cnf_check import (  # noqa: E402
    complement,
    contains_clique,
    expected_formula,
)
from graph_io import decode_graph6  # noqa: E402


class Catalog42E2ExtensionCnfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lines = [
            line.strip()
            for line in (ROOT / "data" / "r55_42some.g6")
            .read_text(encoding="ascii")
            .splitlines()
            if line.strip() and not line.startswith("#")
        ]

    def test_independent_formulas_match(self) -> None:
        expected_counts = {
            1: (9291, 25435),
            42: (9311, 25490),
            256: (9363, 25633),
        }
        for line_number, expected in expected_counts.items():
            core = decode_graph6(self.lines[line_number - 1])
            production = build_formula(core)
            independent = expected_formula(core)
            self.assertEqual(production, independent)
            self.assertEqual((production[0], len(production[1])), expected)

    def test_every_relaxation_has_five_definition_clauses(self) -> None:
        for line_number in [1, 42, 256]:
            core = decode_graph6(self.lines[line_number - 1])
            _, _, counts = build_formula(core)
            self.assertEqual(
                counts["definition_clause_count"],
                5 * counts["constraint_count"],
            )

    def test_recursive_core_validation(self) -> None:
        core = decode_graph6(self.lines[0])
        self.assertFalse(contains_clique(core, 5))
        self.assertFalse(contains_clique(complement(core), 5))
        complete_five = [(1 << 5) - 1 - (1 << vertex) for vertex in range(5)]
        self.assertTrue(contains_clique(complete_five, 5))


if __name__ == "__main__":
    unittest.main()
