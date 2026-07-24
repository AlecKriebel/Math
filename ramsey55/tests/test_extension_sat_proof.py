#!/usr/bin/env python3
"""Regression and adversarial checks for the extension DPLL certificate."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

from extension_sat_proof_check import (  # noqa: E402
    MAGIC,
    TreeChecker,
    decode_short_graph6,
    extension_clauses,
    selected_graph6_line,
)


GRAPH = ROOT / "data" / "exoo42_constructed.g6"
PROOF = ROOT / "results" / "extension_sat_proof_exoo42.bin"
CATALOG = ROOT / "data" / "r55_42some.g6"


class ExtensionSatProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.adjacency = decode_short_graph6(GRAPH.read_bytes())
        cls.clauses, cls.k4_count, cls.i4_count = extension_clauses(cls.adjacency)
        cls.raw = PROOF.read_bytes()
        if cls.raw[:8] != MAGIC:
            raise AssertionError("test proof has wrong magic")
        cls.tree = cls.raw[13:]

    def test_formula_and_complete_tree(self) -> None:
        self.assertEqual(len(self.adjacency), 42)
        self.assertEqual(self.k4_count, 1148)
        self.assertEqual(self.i4_count, 1170)
        self.assertEqual(len(self.clauses), 2318)
        stats = TreeChecker(self.tree, 42, self.clauses).run()
        self.assertEqual(stats.nodes, 39)
        self.assertEqual(stats.branches, 19)
        self.assertEqual(stats.leaves, 20)
        self.assertEqual(stats.max_depth, 5)

    def test_truncation_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "truncated"):
            TreeChecker(self.tree[:-1], 42, self.clauses).run()

    def test_trailing_byte_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "trailing"):
            TreeChecker(self.tree + b"\xff", 42, self.clauses).run()

    def test_invalid_branch_is_rejected(self) -> None:
        corrupted = bytes([254]) + self.tree[1:]
        with self.assertRaisesRegex(ValueError, "invalid branch"):
            TreeChecker(corrupted, 42, self.clauses).run()

    def test_catalog_line_selection(self) -> None:
        raw = CATALOG.read_bytes()
        first = selected_graph6_line(raw, 1)
        second = selected_graph6_line(raw, 2)
        self.assertNotEqual(first, second)
        self.assertEqual(len(decode_short_graph6(first)), 42)
        self.assertEqual(len(decode_short_graph6(second)), 42)
        with self.assertRaisesRegex(ValueError, "outside"):
            selected_graph6_line(raw, 0)
        with self.assertRaisesRegex(ValueError, "outside"):
            selected_graph6_line(raw, 329)


if __name__ == "__main__":
    unittest.main()
