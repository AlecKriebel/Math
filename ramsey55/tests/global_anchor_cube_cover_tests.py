#!/usr/bin/env python3
"""Tests for the exact degree-19/20 Ramsey-anchor cube cover."""

from __future__ import annotations

import itertools
import random
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from global_anchor_cube_cover import (  # noqa: E402
    DEGREES,
    anchor_signature,
    anchor_structure_units,
    appended_clauses,
    canonical_matrices,
    cube_units,
    feasible_matrix,
    lex_nondecreasing_clauses,
    local_degree_counters,
    matrix_orbit,
    matrix_units,
    signature_sort_clauses,
    witness_selector_clauses,
)


def accepts(clauses, assignment) -> bool:
    return all(
        any(assignment.get(abs(literal), False) == (literal > 0) for literal in clause)
        for clause in clauses
    )


class GlobalAnchorCubeCoverTests(unittest.TestCase):
    def test_exact_orbit_census(self) -> None:
        representatives = canonical_matrices()
        self.assertEqual(len(representatives), 143)
        covered: set[int] = set()
        for representative in representatives:
            orbit = set(matrix_orbit(representative))
            self.assertEqual(representative, min(orbit))
            self.assertTrue(all(feasible_matrix(matrix) for matrix in orbit))
            self.assertTrue(covered.isdisjoint(orbit))
            covered.update(orbit)
        self.assertEqual(len(covered), 35_714)
        self.assertEqual(
            covered,
            {
                matrix
                for matrix in range(1 << 16)
                if feasible_matrix(matrix)
            },
        )

    def test_unit_layouts(self) -> None:
        representative = canonical_matrices()[0]
        for degree in DEGREES:
            anchors = anchor_structure_units(degree)
            matrix = matrix_units(degree, representative)
            cube = cube_units(degree, representative)
            self.assertEqual(len(anchors), 12)
            self.assertEqual(len(matrix), 16)
            self.assertEqual(len(cube), 156)
            self.assertEqual(len(set(map(abs, cube))), len(cube))

    def test_lex_template_exhaustive_small_and_random_width8(self) -> None:
        for width in range(1, 6):
            left_variables = tuple(range(1, width + 1))
            right_variables = tuple(range(width + 1, 2 * width + 1))
            clauses = tuple(
                lex_nondecreasing_clauses(left_variables, right_variables)
            )
            self.assertEqual(len(clauses), 2**width - 1)
            for left in range(1 << width):
                for right in range(1 << width):
                    assignment = {
                        left_variables[index]: bool(
                            left & (1 << (width - 1 - index))
                        )
                        for index in range(width)
                    }
                    assignment.update(
                        {
                            right_variables[index]: bool(
                                right & (1 << (width - 1 - index))
                            )
                            for index in range(width)
                        }
                    )
                    self.assertEqual(
                        accepts(clauses, assignment), left <= right
                    )

        generator = random.Random(20260724)
        left_variables = tuple(range(1, 9))
        right_variables = tuple(range(9, 17))
        clauses = tuple(
            lex_nondecreasing_clauses(left_variables, right_variables)
        )
        for _ in range(1_000):
            left = generator.randrange(256)
            right = generator.randrange(256)
            assignment = {
                left_variables[index]: bool(left & (1 << (7 - index)))
                for index in range(8)
            }
            assignment.update(
                {
                    right_variables[index]: bool(right & (1 << (7 - index)))
                    for index in range(8)
                }
            )
            self.assertEqual(accepts(clauses, assignment), left <= right)

    def test_signature_sort_counts_and_primary_range(self) -> None:
        for degree in DEGREES:
            clauses = tuple(signature_sort_clauses(degree))
            self.assertEqual(len(clauses), 26 * 255)
            self.assertTrue(
                all(1 <= abs(literal) <= 903 for clause in clauses for literal in clause)
            )
            for vertex in itertools.chain(
                range(8, degree + 1), range(degree + 8, 43)
            ):
                signature = anchor_signature(degree, vertex)
                self.assertEqual(len(signature), 8)
                self.assertEqual(len(set(signature)), 8)

    def test_local_counter_intervals(self) -> None:
        for degree in DEGREES:
            counters, _next_variable = local_degree_counters(degree)
            side_a_counter_count = 2 * degree
            for index in range(0, side_a_counter_count, 2):
                upper, nonedges = counters[index : index + 2]
                self.assertEqual((upper.bound, nonedges.bound), (13, 17))
                self.assertEqual(
                    len(upper.input_literals), degree - 1
                )
                for internal_degree in range(degree):
                    self.assertEqual(
                        internal_degree <= upper.bound
                        and degree - 1 - internal_degree <= nonedges.bound,
                        degree - 18 <= internal_degree <= 13,
                    )
            side_b_size = 42 - degree
            for index in range(side_a_counter_count, len(counters), 2):
                upper, nonedges = counters[index : index + 2]
                self.assertEqual((upper.bound, nonedges.bound), (17, 13))
                self.assertEqual(
                    len(upper.input_literals), side_b_size - 1
                )
                for internal_degree in range(side_b_size):
                    self.assertEqual(
                        internal_degree <= upper.bound
                        and side_b_size - 1 - internal_degree <= nonedges.bound,
                        side_b_size - 14 <= internal_degree <= 17,
                    )

    def test_union_append_counts(self) -> None:
        expected = {
            19: (41_607, 16_888, 32_516, 82_444),
            20: (41_223, 16_696, 32_132, 82_252),
        }
        for degree in DEGREES:
            clauses = tuple(appended_clauses(degree))
            strengthened_clauses = tuple(
                appended_clauses(
                    degree, include_local_degree_counters=True
                )
            )
            counters, next_variable = local_degree_counters(degree)
            (
                appended_count,
                auxiliary_count,
                counter_clause_count,
                last_variable,
            ) = expected[degree]
            self.assertEqual(len(clauses), 9_091)
            self.assertEqual(len(strengthened_clauses), appended_count)
            self.assertEqual(len(clauses[140]), 143)
            witnesses = tuple(witness_selector_clauses(degree))
            self.assertEqual(len(witnesses), 32)
            self.assertEqual(len(witnesses[0]), 5)
            self.assertEqual(len(witnesses[16]), 5)
            self.assertEqual(len(counters), 84)
            self.assertEqual(
                sum(counter.auxiliary_count for counter in counters),
                auxiliary_count,
            )
            self.assertEqual(
                sum(counter.clause_count for counter in counters),
                counter_clause_count,
            )
            self.assertEqual(next_variable - 1, last_variable)


if __name__ == "__main__":
    unittest.main()
