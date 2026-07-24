#!/usr/bin/env python3
"""Tests for the weighted degree layer in the 3^14 1 certificate."""

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
    "automorphism3_degree_producer",
    ROOT / "src" / "automorphism3_fourteen_cycle_degree_certificate.py",
)
checker = load(
    "automorphism3_degree_checker",
    ROOT / "verify" / "automorphism3_fourteen_cycle_degree_cnf_check.py",
)


class Automorphism3DegreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.orbits, _, _, _ = producer.base.build_formula("6-reduced")

    def test_degree_terms_match_independent_builder(self) -> None:
        expected = checker.independent_degree_terms(self.orbits)
        self.assertEqual(producer.degree_terms(self.orbits), expected)

    def test_degree_encodings_match_clause_for_clause(self) -> None:
        produced, next_produced, metadata = producer.weighted_degree_clauses(
            self.orbits, 302
        )
        expected, next_expected, final_states = (
            checker.independent_degree_encoding(self.orbits, 302)
        )
        self.assertEqual(produced, expected)
        self.assertEqual(next_produced, next_expected)
        self.assertEqual(metadata["final_state_variables"], final_states)
        self.assertEqual(metadata["auxiliary_variable_count"], 14 * 41 * 25)

    def test_weighted_state_semantics(self) -> None:
        clauses, _, metadata = producer.weighted_degree_clauses(
            self.orbits, 302
        )
        final_units = {
            (low,) for low, _ in metadata["final_state_variables"]
        } | {
            (-high,) for _, high in metadata["final_state_variables"]
        }
        for primary_value in (False, True):
            truth = {
                variable: primary_value for variable in range(1, 302)
            }
            next_state = 302
            final_sums: list[int] = []
            for terms in producer.degree_terms(self.orbits):
                total = 0
                for primary, weight in terms:
                    if truth[primary]:
                        total += weight
                    for threshold in range(1, 26):
                        truth[next_state] = total >= threshold
                        next_state += 1
                final_sums.append(total)
            for clause in clauses:
                if clause in final_units:
                    continue
                self.assertTrue(
                    any(
                        truth[abs(literal)] == (literal > 0)
                        for literal in clause
                    )
                )
            self.assertEqual(final_sums, [42 if primary_value else 0] * 14)


if __name__ == "__main__":
    unittest.main()
