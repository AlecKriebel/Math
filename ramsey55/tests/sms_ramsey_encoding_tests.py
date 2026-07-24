#!/usr/bin/env python3
"""Focused tests for the SMS-compatible Ramsey encoding."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

from sms_ramsey_encoding import edge_variable
from sms_ramsey_cnf_check import (
    edge_table,
    expected_formula,
    sequential_counter_clauses,
)
from sms_symmetry_clauses_check import check_record


def evaluate(clause: tuple[int, ...], assignment: dict[int, bool]) -> bool:
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


class SmsRamseyEncodingTests(unittest.TestCase):
    def test_edge_numbering_matches_upper_triangle(self) -> None:
        for order in range(2, 12):
            expected = edge_table(order)
            for pair, variable in expected.items():
                self.assertEqual(edge_variable(order, *pair), variable)

    def test_sequential_counter_canonical_semantics(self) -> None:
        # Exhaust all primary inputs for several nontrivial intervals.
        for input_count, lower, upper in ((4, 2, 2), (5, 2, 3), (6, 1, 4)):
            inputs = list(range(1, input_count + 1))
            clauses_iter, next_variable = sequential_counter_clauses(
                inputs,
                upper,
                upper,
                lower,
                input_count + 1,
            )
            clauses = list(clauses_iter)
            for bits in itertools.product((False, True), repeat=input_count):
                assignment = {
                    variable: bits[variable - 1] for variable in inputs
                }
                # Reconstruct PySMS's prefix-threshold meaning.  The first
                # allocated auxiliary is unused because row[0][0] is replaced
                # by inputs[0].
                first_auxiliary = input_count + 1
                assignment[first_auxiliary] = False
                rows: list[list[int]] = []
                cursor = first_auxiliary
                for _ in inputs:
                    rows.append(list(range(cursor, cursor + upper)))
                    cursor += upper
                rows[0][0] = inputs[0]
                true_count = 0
                for index, value in enumerate(bits):
                    true_count += int(value)
                    for threshold in range(upper):
                        assignment[rows[index][threshold]] = (
                            true_count >= threshold + 1
                        )
                self.assertEqual(cursor, next_variable)
                observed = all(evaluate(clause, assignment) for clause in clauses)
                self.assertEqual(observed, lower <= sum(bits) <= upper)

    def test_known_small_formula_counts_and_order(self) -> None:
        variables, clauses, stream, counts = expected_formula(
            order=5,
            independent_size=3,
            clique_size=3,
            degree_lower=2,
            degree_upper=2,
        )
        materialized = list(stream)
        self.assertEqual(variables, 50)
        self.assertEqual(clauses, 150)
        self.assertEqual(len(materialized), clauses)
        self.assertEqual(counts["primary_variable_count"], 10)
        # Degree clauses precede positive independent-set clauses, which
        # precede negative clique clauses in GraphEncodingBuilder.
        first_ramsey = counts["degree_clause_count"]
        self.assertTrue(all(x > 0 for x in materialized[first_ramsey]))
        self.assertTrue(all(x < 0 for x in materialized[-1]))

    def test_standard_row_lex_symmetry_witness(self) -> None:
        # Swap vertices 0 and 1.  The first moved upper-triangle edge is
        # (0,2), whose image is (1,2).
        check_record([[[-1, 0, 2], [1, 1, 2]], [1, 0, 2, 3]], 4)
        with self.assertRaises(ValueError):
            check_record([[[-1, 0, 2], [1, 0, 3]], [1, 0, 2, 3]], 4)


if __name__ == "__main__":
    unittest.main()
