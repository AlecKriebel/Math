#!/usr/bin/env python3
"""Tests for fixed-vertex degree clauses in prime automorphism CNFs."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


orbit = load("prime_degree_orbit", ROOT / "src" / "automorphism_orbit_cnf.py")
degree = load(
    "prime_degree_generator",
    ROOT / "src" / "prime_automorphism_degree_cnf.py",
)


class PrimeAutomorphismDegreeCnfTests(unittest.TestCase):
    def records(self, prime: int, cycles: int):
        permutation = orbit.canonical_permutation(prime, cycles)
        _, orbits = orbit.edge_orbit_table(permutation)
        return degree.fixed_vertex_degree_records(orbits, prime * cycles)

    def test_maximal_cycle_degree_counts(self) -> None:
        cases = (
            (19, 2, 5, 6, 32, 32, 160),
            (17, 2, 9, 10, 508, 516, 4644),
            (11, 3, 10, 12, 276, 3820, 38200),
        )
        for (
            prime,
            cycles,
            fixed_count,
            incident_count,
            allowed,
            invalid,
            total_clauses,
        ) in cases:
            with self.subTest(prime=prime):
                records = self.records(prime, cycles)
                self.assertEqual(len(records), fixed_count)
                self.assertTrue(
                    all(
                        len(record["weighted_variables"]) == incident_count
                        and record["allowed_assignment_count"] == allowed
                        and record["invalid_assignment_count"] == invalid
                        for record in records
                    )
                )
                self.assertEqual(
                    len(degree.degree_clauses(records)), total_clauses
                )

    def test_allowed_histograms_stay_inside_degree_interval(self) -> None:
        for prime, cycles in ((19, 2), (17, 2), (11, 3)):
            for record in self.records(prime, cycles):
                self.assertTrue(record["allowed_degree_histogram"])
                self.assertTrue(
                    all(
                        18 <= int(observed) <= 24
                        for observed in record["allowed_degree_histogram"]
                    )
                )

    def test_thirteen_cubed_has_no_allowed_fixed_degree(self) -> None:
        records = self.records(13, 3)
        self.assertEqual(len(records), 4)
        self.assertTrue(
            all(
                record["allowed_assignment_count"] == 0
                and record["invalid_assignment_count"] == 64
                for record in records
            )
        )


if __name__ == "__main__":
    unittest.main()
