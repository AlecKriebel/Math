#!/usr/bin/env python3
"""Focused regression tests for the dependency-free sextic LP(333) checker."""

from __future__ import annotations

import unittest

import check_lp333_sextic_quotient as sextic


class SexticQuotientTests(unittest.TestCase):
    def test_classes_matrices_and_equation_count(self) -> None:
        equation_count, transition_mass = sextic.verify_classes_and_matrices()
        self.assertEqual(equation_count, 34)
        self.assertEqual(transition_mass, 222)

    def test_row_axis_catalog(self) -> None:
        self.assertEqual(
            sextic.verify_row_axis_lemma(),
            (972, 7_056, 28, 1_658_700, 298),
        )

    def test_explicit_skeleton(self) -> None:
        self.assertEqual(
            sextic.verify_skeleton(),
            (20, 784, 10, 120, 4_704, 10),
        )

    def test_quadratic_quotient_obstruction(self) -> None:
        self.assertEqual(
            sextic.verify_quadratic_residue_obstruction(),
            (-9, -8),
        )

    def test_shift_template_obstruction(self) -> None:
        self.assertEqual(
            sextic.verify_shift_template_obstruction(),
            (-1, 0, 0, 0, 0, 0, 0, 0, 0),
        )


if __name__ == "__main__":
    unittest.main()
