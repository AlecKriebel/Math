#!/usr/bin/env python3
"""Tests for lossless complement/relabel global Ramsey branches."""

from __future__ import annotations

import itertools
import random
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from global_ramsey_branches import (  # noqa: E402
    BRANCH_DEGREES,
    branch_units,
    normalize_vertex_zero,
    write_branch_cnf,
)


def graph_from_mask(order: int, mask: int) -> list[int]:
    adjacency = [0] * order
    for index, (left, right) in enumerate(
        itertools.combinations(range(order), 2)
    ):
        if (mask >> index) & 1:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return adjacency


class GlobalRamseyBranchTests(unittest.TestCase):
    def test_normalization_exhaustive_through_order_six(self) -> None:
        checked = 0
        for order in range(2, 7):
            for mask in range(1 << (order * (order - 1) // 2)):
                graph = graph_from_mask(order, mask)
                normalized, _, degree = normalize_vertex_zero(graph)
                self.assertLessEqual(degree, (order - 1) // 2)
                self.assertEqual(normalized[0].bit_count(), degree)
                self.assertTrue(
                    all((normalized[0] >> vertex) & 1 for vertex in range(1, degree + 1))
                )
                self.assertTrue(
                    all(
                        not (normalized[0] >> vertex) & 1
                        for vertex in range(degree + 1, order)
                    )
                )
                checked += 1
        self.assertEqual(checked, 33_866)

    def test_production_units_fix_neighbor_prefix(self) -> None:
        for degree in BRANCH_DEGREES:
            units = branch_units(43, degree)
            self.assertEqual(len(units), 42)
            self.assertEqual(units[:degree], tuple(range(1, degree + 1)))
            self.assertEqual(
                units[degree:],
                tuple(-variable for variable in range(degree + 1, 43)),
            )

    def test_branch_cnf_materialization(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "base.cnf"
            base.write_text(
                "c base\np cnf 50 2\n1 2 0\n-1 3 0\n",
                encoding="ascii",
            )
            import hashlib

            output = root / "branch.cnf"
            result = write_branch_cnf(
                base,
                output,
                degree=18,
                expected_base_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),
            )
            lines = output.read_text(encoding="ascii").splitlines()
            self.assertIn("p cnf 50 44", lines)
            self.assertEqual(lines[-42:], [f"{x} 0" for x in branch_units(43, 18)])
            self.assertEqual(result["unit_clause_count"], 42)

    def test_random_order43_solution_degree_normalization_range(self) -> None:
        rng = random.Random(20260723)
        for _ in range(100):
            graph = [0] * 43
            for left, right in itertools.combinations(range(43), 2):
                if rng.getrandbits(1):
                    graph[left] |= 1 << right
                    graph[right] |= 1 << left
            normalized, _, degree = normalize_vertex_zero(graph)
            self.assertLessEqual(degree, 21)
            self.assertEqual(normalized[0].bit_count(), degree)


if __name__ == "__main__":
    unittest.main()
