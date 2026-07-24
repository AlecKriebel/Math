#!/usr/bin/env python3
"""Unit tests for the distance-41 anti-fold reduction."""

from __future__ import annotations

import unittest

import verify_eliahou_adjacent42_repair as adjacent
import verify_eliahou_antifold42 as antifold


class EliahouAntifold42Tests(unittest.TestCase):
    def test_seed_antifold_matches_aperiodic_reduction(self) -> None:
        base = adjacent.eliahou_base()
        direct = antifold.negacyclic_norm_coefficients(
            antifold.antifold_quadruple(base)
        )
        derived = antifold.antifold_correlations_from_aperiodic(
            adjacent.base_correlations(base)
        )
        self.assertEqual(direct, derived)
        self.assertEqual(direct[0], 654)

    def test_negacyclic_reflection_rule(self) -> None:
        coefficients = antifold.negacyclic_norm_coefficients(
            antifold.antifold_quadruple(adjacent.eliahou_base())
        )
        self.assertEqual(coefficients[21], 0)
        for lag in range(1, 21):
            self.assertEqual(coefficients[42 - lag], -coefficients[lag])

    def test_both_endpoint_orientations_have_one_antifold(self) -> None:
        antifold.verify_orientation_independence()

    def test_boundary_has_39_binary_support_variables_selected(self) -> None:
        long_catalog, short_catalog = adjacent.q_pair_signature_catalogs()
        pair_cases = [
            ("L", index)
            for signature in ((-2, 0), (0, 2))
            for index in long_catalog[signature]
        ] + [
            ("S", index)
            for index in short_catalog[(0, 0)]
        ]
        self.assertEqual(len(pair_cases), 39)
        counts = {}
        for block, index in pair_cases:
            long_cells, short_cells = antifold.available_s_support_cells(
                block, index
            )
            count = len(long_cells) + len(short_cells)
            counts[count] = counts.get(count, 0) + 1
        self.assertEqual(counts, {78: 38, 79: 1})

    def test_any_boundary_support_has_target_zero_lag(self) -> None:
        block = "L"
        index = 0
        long_cells, short_cells = antifold.available_s_support_cells(
            block, index
        )
        long_support = long_cells[:19]
        short_support = short_cells[:20]
        rows = antifold.boundary_antifold_rows(
            block, index, long_support, short_support
        )
        coefficients = antifold.negacyclic_norm_coefficients(rows)
        self.assertEqual(coefficients[0], 334)


if __name__ == "__main__":
    unittest.main()
