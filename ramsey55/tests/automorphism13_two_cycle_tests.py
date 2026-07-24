#!/usr/bin/env python3
"""Structural tests for the 13^2 1^17 automorphism search."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SPEC = importlib.util.spec_from_file_location(
    "automorphism13_two_cycle_search",
    ROOT / "src" / "automorphism13_two_cycle_search.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load order-13 search module")
search = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(search)
CERT_SPEC = importlib.util.spec_from_file_location(
    "automorphism13_two_cycle_certificate",
    ROOT / "src" / "automorphism13_two_cycle_certificate.py",
)
if CERT_SPEC is None or CERT_SPEC.loader is None:
    raise RuntimeError("could not load order-13 certificate module")
certificate = importlib.util.module_from_spec(CERT_SPEC)
CERT_SPEC.loader.exec_module(certificate)


class Automorphism13TwoCycleTests(unittest.TestCase):
    def test_exact_formula_fingerprint(self) -> None:
        _, edge_variable, orbits, signatures = search.formula()
        self.assertEqual(len(edge_variable), 903)
        self.assertEqual(len(orbits), 195)
        self.assertEqual(Counter(map(len, orbits)), Counter({13: 59, 1: 136}))
        self.assertEqual(len(signatures), 76_132)
        self.assertEqual(
            Counter(map(len, signatures)),
            Counter({4: 216, 5: 1950, 6: 2382, 7: 12_484,
                     8: 35_620, 9: 2340, 10: 21_140}),
        )
        self.assertEqual(
            search.dimacs_sha256(len(orbits), signatures),
            search.EXPECTED_DIMACS_SHA256,
        )

    def test_group_size_split_and_assumptions(self) -> None:
        _, edge_variable, _, _ = search.formula()
        self.assertEqual(search.normalized_group_sizes(), tuple(range(9)))
        for group_size in search.normalized_group_sizes():
            literals = search.group_assumptions(group_size, edge_variable)
            self.assertEqual(len(literals), 34)
            self.assertEqual(len(set(map(abs, literals))), 34)
            truth = {abs(literal): literal > 0 for literal in literals}
            first_count = 0
            for fixed_vertex in search.FIXED_VERTICES:
                first = edge_variable[(0, fixed_vertex)]
                second = edge_variable[(13, fixed_vertex)]
                self.assertNotEqual(truth[first], truth[second])
                first_count += truth[first]
            self.assertEqual(first_count, group_size)

    def test_cycle_exchange_covers_all_labeled_group_sizes(self) -> None:
        self.assertEqual(
            {min(size, 17 - size) for size in range(18)},
            set(search.normalized_group_sizes()),
        )

    def test_symmetry_breaking_clause_shape(self) -> None:
        _, edge_variable, _, _ = search.formula()
        clauses = certificate.symmetry_breaking_clauses(edge_variable)
        self.assertEqual(len(clauses), 51)
        self.assertEqual(Counter(map(len, clauses)), Counter({2: 50, 1: 1}))
        first = [
            edge_variable[(0, fixed_vertex)]
            for fixed_vertex in search.FIXED_VERTICES
        ]
        self.assertEqual(clauses[-1], (-first[8],))
        for group_size in range(9):
            truth = {
                edge_variable[(0, fixed_vertex)]: index < group_size
                for index, fixed_vertex in enumerate(search.FIXED_VERTICES)
            }
            truth.update(
                {
                    edge_variable[(13, fixed_vertex)]: index >= group_size
                    for index, fixed_vertex in enumerate(search.FIXED_VERTICES)
                }
            )
            self.assertTrue(
                all(
                    any(
                        truth[abs(literal)] == (literal > 0)
                        for literal in clause
                    )
                    for clause in clauses
                )
            )


if __name__ == "__main__":
    unittest.main()
