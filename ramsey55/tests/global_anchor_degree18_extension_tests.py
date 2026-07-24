#!/usr/bin/env python3
"""Tests for the standalone degree-18 Ramsey-anchor extension."""

from __future__ import annotations

import itertools
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "verify"))

import global_anchor_degree18_extension as production
import global_anchor_degree18_extension_check as checker


def accepts(
    clauses: tuple[tuple[int, ...], ...], assignment: dict[int, bool]
) -> bool:
    return all(
        any(assignment[abs(literal)] == (literal > 0) for literal in clause)
        for clause in clauses
    )


class GlobalAnchorDegree18ExtensionTests(unittest.TestCase):
    def test_exact_orbit_census_matches_independent_checker(self) -> None:
        representatives = production.canonical_matrices()
        independent, owner = checker.representatives_and_owner()
        self.assertEqual(representatives, independent)
        self.assertEqual(len(representatives), 143)
        self.assertEqual(len(owner), 35_714)
        self.assertEqual(
            set(owner),
            {
                matrix
                for matrix in range(1 << 16)
                if production.feasible_matrix(matrix)
            },
        )

    def test_degree18_boundary_proof_obligations(self) -> None:
        audit = checker.proof_obligation_audit()
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["A_size"], 18)
        self.assertEqual(audit["A_R44_slack"], 0)
        self.assertEqual(audit["B_size"], 24)
        self.assertEqual(audit["witness_anchor_intersection_sizes"], [0, 1])
        self.assertEqual(
            audit["witness_location_labels"], [None, 0, 1, 2, 3]
        )

    def test_common_cube_and_selector_layouts(self) -> None:
        common = production.common_units()
        self.assertEqual(len(common), 54)
        self.assertEqual(len(set(map(abs, common))), 54)
        representative = production.canonical_matrices()[0]
        cube = production.cube_units(representative)
        self.assertEqual(len(cube), 70)
        self.assertEqual(len(set(map(abs, cube))), 70)
        self.assertEqual(
            cube,
            checker.common_units() + checker.matrix_units(representative),
        )

    def test_witness_selector_exhaustiveness_and_clause_counts(self) -> None:
        triangles, independent = production.witness_patterns()
        self.assertEqual(len(triangles), 5)
        self.assertEqual(len(independent), 5)
        self.assertTrue(
            all(len(pattern) == 3 for pattern in (*triangles, *independent))
        )
        self.assertEqual(
            (triangles, independent), checker.witness_patterns()
        )
        witness_clauses = tuple(production.witness_selector_clauses())
        self.assertEqual(len(witness_clauses), 32)
        self.assertEqual(len(witness_clauses[0]), 5)
        self.assertEqual(len(witness_clauses[16]), 5)

    def test_lex_template_and_signature_sorting(self) -> None:
        for width in range(1, 6):
            left_variables = tuple(range(1, width + 1))
            right_variables = tuple(range(width + 1, 2 * width + 1))
            clauses = tuple(
                production.lex_nondecreasing_clauses(
                    left_variables, right_variables
                )
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
        sort_clauses = tuple(production.signature_sort_clauses())
        self.assertEqual(len(sort_clauses), 26 * 255)
        for vertex in itertools.chain(range(8, 19), range(26, 43)):
            signature = production.anchor_signature(vertex)
            self.assertEqual(len(signature), 8)
            self.assertEqual(len(set(signature)), 8)

    def test_union_counts_and_independent_stream_hash(self) -> None:
        additions = tuple(production.appended_clauses())
        representatives, _owner = checker.representatives_and_owner()
        independent = tuple(checker.appended_clauses(representatives))
        self.assertEqual(additions, independent)
        self.assertEqual(len(additions), 9_005)
        self.assertEqual(
            production.BASE_CLAUSE_COUNT + len(additions), 2_061_137
        )
        self.assertEqual(production.BASE_VARIABLE_COUNT + 153, 65_556)
        self.assertEqual(
            production.clause_stream_sha256(additions),
            checker.clause_hash(independent),
        )


if __name__ == "__main__":
    unittest.main()
