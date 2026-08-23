from __future__ import annotations

import unittest

import sympy as sp

from src.exact_markov import (
    R,
    average_single_mutant_fixation,
    check_lumping,
    complete_baseline,
    complete_graph_weights,
    sign_certificate_on_r_gt_one,
    transition_matrix,
)


class ExactMarkovTests(unittest.TestCase):
    def test_complete_graph_formulas(self) -> None:
        for n in (2, 3, 4):
            weights = complete_graph_weights(n)
            for rule in ("Bd", "dB"):
                actual = average_single_mutant_fixation(weights, rule)
                expected = complete_baseline(n, rule)
                self.assertEqual(sp.simplify(actual - expected), 0)

    def test_every_transition_row_sums_to_one(self) -> None:
        weights = ((0, 1, 2), (1, 0, 3), (2, 3, 0))
        for rule in ("Bd", "dB"):
            for row in transition_matrix(weights, rule):
                self.assertEqual(sp.simplify(sum(row.values()) - 1), 0)

    def test_complete_graph_lumps_by_mutant_count(self) -> None:
        n = 4
        cells = [
            [mask for mask in range(1 << n) if bin(mask).count("1") == count]
            for count in range(n + 1)
        ]
        for rule in ("Bd", "dB"):
            quotient = check_lumping(
                transition_matrix(complete_graph_weights(n), rule), cells
            )
            self.assertEqual(len(quotient), n + 1)
            for row in quotient:
                self.assertEqual(sp.simplify(sum(row) - 1), 0)

    def test_incomplete_support_strong_limit(self) -> None:
        # Positive-weight support is the path 0--1--2, with support degrees 1,2,1.
        weights = ((0, 1, 0), (1, 0, 2), (0, 2, 0))
        actual = average_single_mutant_fixation(weights, "dB")
        expected_limit = sp.Rational(1, 3) * (
            sp.Rational(1, 2) + sp.Rational(2, 3) + sp.Rational(1, 2)
        )
        self.assertEqual(sp.limit(actual, R, sp.oo), expected_limit)
        self.assertLess(expected_limit, sp.Rational(2, 3))

    def test_weighted_triangle_first_strong_correction(self) -> None:
        weights = ((0, 1, 2), (1, 0, 3), (2, 3, 0))
        degrees = [sum(row) for row in weights]
        obstruction_sum = sum(
            sp.Rational(degrees[i] + degrees[j], weights[i][j]) - 2
            for i in range(3)
            for j in range(i + 1, 3)
        )
        predicted = obstruction_sum / (3**2 * (3 - 2))
        actual = average_single_mutant_fixation(weights, "dB")
        extracted = sp.limit(R * (sp.Rational(2, 3) - actual), R, sp.oo)
        self.assertEqual(predicted, sp.Rational(8, 9))
        self.assertEqual(extracted, predicted)
        self.assertGreater(predicted, sp.Rational(2, 3))

    def test_sturm_sign_certificate(self) -> None:
        polynomial = sp.Poly((R - 1) ** 2 * (R**2 + R + 1), R)
        certificate = sign_certificate_on_r_gt_one(polynomial)
        self.assertEqual(certificate["sign"], 1)
        self.assertEqual(certificate["root_count"], 0)
        self.assertEqual(certificate["endpoint_multiplicity"], 2)


if __name__ == "__main__":
    unittest.main()
