#!/usr/bin/env python3
"""Structural tests for the cycle type 3^14 1 certificate formula."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from collections import Counter
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


certificate = load(
    "automorphism3_fourteen_cycle_certificate",
    ROOT / "src" / "automorphism3_fourteen_cycle_certificate.py",
)
checker = load(
    "automorphism3_fourteen_cycle_checker",
    ROOT / "verify" / "automorphism3_fourteen_cycle_symmetry_cnf_check.py",
)


class Automorphism3FourteenCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.orbits, cls.base, _, cls.edge_variable = certificate.build_formula(
            "cover"
        )

    def test_exact_orbit_partition(self) -> None:
        self.assertEqual(len(self.orbits), 301)
        self.assertEqual(sum(map(len, self.orbits)), 903)
        self.assertEqual(Counter(map(len, self.orbits)), Counter({3: 301}))
        self.assertEqual(len(self.edge_variable), 903)

    def test_independent_formula_matches(self) -> None:
        variables, clauses, root_variables, base_count, full_base_count = (
            checker.expected_formula("cover")
        )
        self.assertEqual(variables, len(self.orbits))
        self.assertEqual(base_count, len(self.base))
        self.assertEqual(full_base_count, len(self.base))
        self.assertEqual(clauses[:base_count], self.base)
        self.assertEqual(
            root_variables, certificate.root_cycle_variables(self.edge_variable)
        )

    def test_cover_clause_shape(self) -> None:
        clauses = certificate.symmetry_clauses(self.edge_variable, "cover")
        self.assertEqual(Counter(map(len, clauses)), Counter({2: 13, 1: 2}))
        variables = certificate.root_cycle_variables(self.edge_variable)
        for length in range(15):
            truth = {
                variable: index < length
                for index, variable in enumerate(variables)
            }
            satisfied = all(
                any(truth[abs(literal)] == (literal > 0) for literal in clause)
                for clause in clauses
            )
            self.assertEqual(satisfied, length in {6, 7})

    def test_case_units(self) -> None:
        variables = certificate.root_cycle_variables(self.edge_variable)
        for length in (6, 7):
            clauses = certificate.symmetry_clauses(
                self.edge_variable, str(length)
            )
            self.assertEqual(len(clauses), 14)
            self.assertEqual(
                clauses,
                tuple(
                    (variable,) if index < length else (-variable,)
                    for index, variable in enumerate(variables)
                ),
            )

    def test_reduced_cases_match_independent_simplification(self) -> None:
        for length in (6, 7):
            mode = f"{length}-reduced"
            _, base, units, _ = certificate.build_formula(mode)
            _, clauses, _, base_count, full_base_count = (
                checker.expected_formula(mode)
            )
            self.assertLess(base_count, full_base_count)
            self.assertEqual(len(base), base_count)
            self.assertEqual(clauses[:base_count], base)
            self.assertEqual(clauses[base_count:], units)

    def test_degree_complement_cover_is_exhaustive(self) -> None:
        audit = checker.symmetry_cover_audit()
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["degree_allowed_m"], [6, 7, 8])
        self.assertEqual(audit["complement_normalized_m"], [6, 7])
        self.assertEqual(audit["cover_formula_prefix_lengths"], [6, 7])


if __name__ == "__main__":
    unittest.main()
