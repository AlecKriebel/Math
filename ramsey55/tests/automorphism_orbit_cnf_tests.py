#!/usr/bin/env python3
"""Tests for prime-order automorphism orbit encodings."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


producer = load("automorphism_producer", ROOT / "src" / "automorphism_orbit_cnf.py")
auditor = load(
    "automorphism_auditor", ROOT / "verify" / "automorphism_orbit_cnf_check.py"
)


class PrimeAutomorphismEncodingTests(unittest.TestCase):
    def test_invalid_cycle_types_are_rejected(self) -> None:
        for prime, cycles in ((1, 1), (4, 1), (7, 0), (7, 7)):
            with self.assertRaises(ValueError):
                producer.canonical_permutation(prime, cycles)

    def test_edge_orbits_partition_all_edges(self) -> None:
        permutation = producer.canonical_permutation(7, 6)
        table, orbits = producer.edge_orbit_table(permutation)
        self.assertEqual(len(table), 903)
        self.assertEqual(sum(map(len, orbits)), 903)
        self.assertEqual(len(orbits), 129)
        self.assertEqual(sorted(map(len, orbits)), [7] * 129)

    def test_independent_reconstruction_matches_producer(self) -> None:
        permutation = producer.canonical_permutation(7, 6)
        table, orbits = producer.edge_orbit_table(permutation)
        signatures = producer.ramsey_signatures(table)
        independent_permutation, independent_orbits, independent_clauses = (
            auditor.independently_build(7, 6)
        )
        expected_clauses = []
        for signature in signatures:
            expected_clauses.append(signature)
            expected_clauses.append(tuple(-variable for variable in signature))
        self.assertEqual(permutation, independent_permutation)
        self.assertEqual(orbits, independent_orbits)
        self.assertEqual(tuple(expected_clauses), independent_clauses)


if __name__ == "__main__":
    unittest.main()
