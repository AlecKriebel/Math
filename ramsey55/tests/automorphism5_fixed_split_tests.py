#!/usr/bin/env python3
"""Structural tests for the order-5 fixed-vertex split search."""

from __future__ import annotations

import importlib.util
import itertools
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
SPEC = importlib.util.spec_from_file_location(
    "automorphism5_fixed_split_search",
    ROOT / "src" / "automorphism5_fixed_split_search.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load order-5 search module")
search = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(search)


class Automorphism5FixedSplitTests(unittest.TestCase):
    def test_exact_orbit_formula_fingerprint(self) -> None:
        edge_variable, orbits = search.edge_orbits()
        signatures = search.ramsey_signatures(edge_variable)
        self.assertEqual(len(edge_variable), 903)
        self.assertEqual(len(orbits), 183)
        self.assertEqual(Counter(map(len, orbits)), Counter({5: 180, 1: 3}))
        self.assertEqual(len(signatures), 192_054)
        self.assertEqual(
            Counter(map(len, signatures)),
            Counter({2: 8, 3: 24, 5: 24, 6: 280, 7: 3096,
                     8: 2632, 9: 42_000, 10: 143_990}),
        )
        self.assertEqual(
            search.dimacs_sha256(len(orbits), signatures),
            search.EXPECTED_DIMACS_SHA256,
        )

    def test_fixed_split_type_counts_and_realizations(self) -> None:
        expected = {"edgeless": 21, "one_edge": 38}
        for fixed_pattern, count in expected.items():
            representatives = search.fixed_split_types(fixed_pattern)
            self.assertEqual(len(representatives), count)
            for representative in representatives:
                subsets = search.subsets_from_counts(representative)
                self.assertEqual(tuple(map(len, subsets)), (4, 4, 4))
                self.assertEqual(
                    search.membership_counts(subsets), representative
                )

    def test_type_cover_matches_exhaustive_labeled_triples(self) -> None:
        first = frozenset(range(4))
        four_subsets = tuple(
            frozenset(subset)
            for subset in itertools.combinations(range(8), 4)
        )
        groups = {
            "edgeless": tuple(itertools.permutations(range(3))),
            "one_edge": ((0, 1, 2), (1, 0, 2)),
        }
        for fixed_pattern, group in groups.items():
            exhaustive = {
                search.canonical_counts(
                    search.membership_counts((first, second, third)), group
                )
                for second in four_subsets
                for third in four_subsets
            }
            self.assertEqual(
                exhaustive, set(search.fixed_split_types(fixed_pattern))
            )

    def test_each_split_assigns_four_cycles_per_fixed_vertex(self) -> None:
        edge_variable, _ = search.edge_orbits()
        for fixed_pattern in ("edgeless", "one_edge"):
            for counts in search.fixed_split_types(fixed_pattern):
                assumptions = search.assumptions_for_split(
                    fixed_pattern, counts, edge_variable
                )
                self.assertEqual(len(assumptions), 27)
                self.assertEqual(len(set(map(abs, assumptions))), 27)
                truth = {abs(literal): literal > 0 for literal in assumptions}
                for fixed_vertex in search.FIXED_VERTICES:
                    incident = [
                        edge_variable[(5 * cycle, fixed_vertex)]
                        for cycle in range(8)
                    ]
                    self.assertEqual(sum(truth[var] for var in incident), 4)

    def test_all_ones_internal_orientation_quotient(self) -> None:
        edge_variable, _ = search.edge_orbits()
        orientations = search.internal_orientation_types((1,) * 8)
        self.assertEqual(len(orientations), 80)
        for orientation in orientations:
            literals = search.internal_orientation_assumptions(
                orientation, edge_variable
            )
            self.assertEqual(len(literals), 16)
            self.assertEqual(len(set(map(abs, literals))), 16)
            truth = {abs(literal): literal > 0 for literal in literals}
            for cycle in range(8):
                first = edge_variable[(5 * cycle, 5 * cycle + 1)]
                second = edge_variable[(5 * cycle, 5 * cycle + 2)]
                self.assertNotEqual(truth[first], truth[second])


if __name__ == "__main__":
    unittest.main()
