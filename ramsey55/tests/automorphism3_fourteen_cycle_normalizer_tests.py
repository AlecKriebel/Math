#!/usr/bin/env python3
"""Tests for the C3 normalizer symmetry clauses."""

from __future__ import annotations

import importlib.util
import itertools
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


producer = load(
    "automorphism3_normalizer_producer",
    ROOT / "src" / "automorphism3_fourteen_cycle_normalizer_certificate.py",
)
checker = load(
    "automorphism3_normalizer_checker",
    ROOT / "verify" / "automorphism3_fourteen_cycle_normalizer_cnf_check.py",
)


class Automorphism3NormalizerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.orbits, _, _, cls.edge_variable = producer.base.build_formula(
            "6-reduced"
        )

    def test_every_triple_has_a_monotone_rotation(self) -> None:
        for bits in itertools.product((False, True), repeat=3):
            rotations = [
                tuple(bits[(index + shift) % 3] for index in range(3))
                for shift in range(3)
            ]
            canonical = max(rotations)
            self.assertGreaterEqual(canonical[0], canonical[1])
            self.assertGreaterEqual(canonical[1], canonical[2])

    def test_producer_and_independent_checker_match(self) -> None:
        for root_cycles in (6, 7):
            produced, produced_next, produced_metadata = (
                producer.normalizer_clauses(
                    self.edge_variable, root_cycles, 20_000
                )
            )
            expected, expected_next, expected_metadata = (
                checker.independent_normalizer(
                    self.orbits, root_cycles, 20_000
                )
            )
            self.assertEqual(produced, expected)
            self.assertEqual(produced_next, expected_next)
            self.assertEqual(produced_metadata, expected_metadata)
            self.assertEqual(
                len(produced), 1_340 if root_cycles == 6 else 1_322
            )

    def test_lexicographic_comparator_semantics(self) -> None:
        clauses, next_variable = producer.lexicographic_ge_clauses(
            (1, 2, 3), (4, 5, 6), 7
        )
        self.assertEqual(next_variable, 9)
        for left in itertools.product((False, True), repeat=3):
            for right in itertools.product((False, True), repeat=3):
                truth = {
                    1: left[0], 2: left[1], 3: left[2],
                    4: right[0], 5: right[1], 6: right[2],
                    7: left[0] == right[0],
                    8: left[:2] == right[:2],
                }
                satisfied = all(
                    any(
                        truth[abs(literal)] == (literal > 0)
                        for literal in clause
                    )
                    for clause in clauses
                )
                self.assertEqual(satisfied, left >= right)

    def test_normalizer_cover_audit(self) -> None:
        audit = checker.normalizer_cover_audit()
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["three_bit_patterns_checked"], 8)
        self.assertEqual(audit["ordered_key_pairs_checked"], 64)


if __name__ == "__main__":
    unittest.main()
