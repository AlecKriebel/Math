#!/usr/bin/env python3
"""Tests for the greedy full normalizer quotient."""

from __future__ import annotations

import importlib.util
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
    "automorphism3_greedy_producer",
    ROOT / "src" / "automorphism3_fourteen_cycle_greedy_certificate.py",
)
checker = load(
    "automorphism3_greedy_checker",
    ROOT / "verify" / "automorphism3_fourteen_cycle_greedy_cnf_check.py",
)


class Automorphism3GreedyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.orbits, _, _, cls.edge_variable = producer.base.build_formula(
            "6-reduced"
        )

    def test_oriented_profiles_cycle_through_phase_patterns(self) -> None:
        for cycle in range(1, 14):
            profiles = [
                producer.oriented_profile(
                    self.edge_variable, cycle, range(1), shift
                )
                for shift in range(3)
            ]
            self.assertEqual(len(profiles[0]), 4)
            self.assertEqual(
                {profiles[0][0]}, {profiles[1][0], profiles[2][0]}
            )
            self.assertEqual(
                set(profiles[0][1:]),
                set(profiles[1][1:]),
            )

    def test_producer_matches_independent_checker(self) -> None:
        for root_cycles in (6, 7):
            produced, produced_next, produced_metadata = (
                producer.greedy_normalizer_clauses(
                    self.edge_variable, root_cycles, 20_000
                )
            )
            expected, expected_next, expected_metadata = (
                checker.independent_greedy_normalizer(
                    self.orbits, root_cycles, 20_000
                )
            )
            self.assertEqual(produced, expected)
            self.assertEqual(produced_next, expected_next)
            self.assertEqual(produced_metadata, expected_metadata)

    def test_cover_audit(self) -> None:
        audit = checker.greedy_cover_audit()
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["phase_patterns_checked"], 8)


if __name__ == "__main__":
    unittest.main()
