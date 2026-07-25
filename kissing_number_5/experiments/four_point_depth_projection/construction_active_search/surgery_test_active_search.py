#!/usr/bin/env python3
"""Regression tests for the hard active-contact surgery experiment."""

from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np

from experiments.four_point_depth_projection.construction_active_search import (
    surgery_active_search as search,
)


class SurgerySearchTests(unittest.TestCase):
    def test_random_greedy_is_deterministic_and_asymmetric(self):
        first = search.random_greedy_start(
            12, np.random.default_rng(12345), candidates_per_point=300
        )
        second = search.random_greedy_start(
            12, np.random.default_rng(12345), candidates_per_point=300
        )
        self.assertTrue(np.array_equal(first, second))
        self.assertLess(
            float(np.max(np.abs(first @ first.T + np.eye(12)))),
            2.1,
        )

    def test_tangent_chebyshev_step_does_not_worsen_random_cloud(self):
        x = search.unit_rows(np.random.default_rng(72).normal(size=(14, 5)))
        tangent, record = search.tangent_chebyshev_lp(
            x, radius=0.025, band=0.15
        )
        self.assertTrue(record["solver_success"])
        self.assertIsNotNone(tangent)
        candidate, step = search.best_retracted_candidate(x, tangent)
        self.assertLessEqual(search.maximum(candidate), search.maximum(x))
        if step["accepted"]:
            self.assertLess(search.hard_score(candidate), search.hard_score(x))

    def test_contact_jacobian_matches_centered_difference(self):
        rng = np.random.default_rng(17)
        x = search.unit_rows(rng.normal(size=(9, 5)))
        bases = search.tangent_bases(x)
        first = np.asarray([0, 2, 4], dtype=int)
        second = np.asarray([1, 6, 8], dtype=int)
        jacobian = search.contact_jacobian(x, first, second, bases)
        coefficients = rng.normal(size=4 * len(x))
        tangent = np.einsum(
            "nij,nj->ni", bases, coefficients.reshape(len(x), 4)
        )
        epsilon = 2e-7
        plus = search.retract(x, tangent, epsilon)
        minus = search.retract(x, tangent, -epsilon)
        finite = np.asarray(
            [
                (plus[i] @ plus[j] - minus[i] @ minus[j])
                / (2.0 * epsilon)
                for i, j in zip(first, second)
            ]
        )
        analytic = jacobian @ coefficients
        self.assertTrue(np.allclose(finite, analytic, atol=2e-8, rtol=2e-8))

    def test_gram_completion_remains_rank_five(self):
        x = search.unit_rows(np.random.default_rng(91).normal(size=(18, 5)))
        candidate, history = search.gram_clip_completion(
            x, target=0.55, rounds=3, blend=0.4
        )
        self.assertEqual(candidate.shape, (18, 5))
        self.assertEqual(len(history), 3)
        spectrum = np.linalg.eigvalsh(candidate @ candidate.T)
        self.assertLess(float(np.max(np.abs(spectrum[:-5]))), 2e-13)

    def test_d5_exact_float_configuration(self):
        rows = []
        for i in range(5):
            for j in range(i + 1, 5):
                for first in (-1.0, 1.0):
                    for second in (-1.0, 1.0):
                        row = np.zeros(5)
                        row[i] = first / np.sqrt(2.0)
                        row[j] = second / np.sqrt(2.0)
                        rows.append(row)
        x = np.asarray(rows)
        self.assertEqual(x.shape, (40, 5))
        self.assertLessEqual(search.maximum(x), 0.5000000000000001)
        diagnostics = search.diagnostics(x)
        # Normalizing binary64 approximations to 1/sqrt(2) can place an
        # algebraic 1/2 contact one ulp above 1/2.
        self.assertLessEqual(
            diagnostics["maximum_inner_product_binary64"],
            np.nextafter(0.5, np.inf),
        )

    def test_stored_input_cardinalities(self):
        root = Path(__file__).resolve().parents[3]
        expected_upper = {
            41: 0.5150,
            42: 0.5183,
            43: 0.5248,
            44: 0.5275,
        }
        for n, bound in expected_upper.items():
            x, provenance = search.load_stored_near_miss(n, root)
            self.assertEqual(x.shape, (n, 5))
            self.assertLess(search.maximum(x), bound)
            self.assertTrue(provenance)


if __name__ == "__main__":
    unittest.main()
