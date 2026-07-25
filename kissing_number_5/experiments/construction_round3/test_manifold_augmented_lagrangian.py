"""Numerical unit tests for the round-3 discovery program."""

from __future__ import annotations

import unittest
from pathlib import Path

import numpy as np

from .manifold_augmented_lagrangian import (
    augmented_value_gradient,
    d_roots,
    diagnostics,
    e6_roots,
    e7_roots,
    e8_roots,
    make_initial,
    project_to_scaled_simplex,
    retract,
    riesz_value_gradient,
    tangent_projection,
    unit_rows,
)


HERE = Path(__file__).resolve()
WARM41 = HERE.parents[1] / "input" / "spherical_codes_5_41.txt"


class ManifoldSearchTests(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(2026072303)
        self.x = unit_rows(self.rng.normal(size=(8, 5)))

    def directional_check(self, function, relative_tolerance=3e-6):
        value, gradient = function(self.x)
        direction = tangent_projection(
            self.x, self.rng.normal(size=self.x.shape)
        )
        direction /= np.linalg.norm(direction)
        epsilon = 2e-6
        plus = function(retract(self.x, direction, epsilon))[0]
        minus = function(retract(self.x, direction, -epsilon))[0]
        finite_difference = (plus - minus) / (2 * epsilon)
        analytic = float(np.sum(gradient * direction))
        self.assertAlmostEqual(value, function(self.x)[0], places=14)
        self.assertLess(
            abs(finite_difference - analytic),
            relative_tolerance * max(1.0, abs(analytic)),
        )

    def test_unit_rows_and_retraction(self):
        direction = tangent_projection(
            self.x, self.rng.normal(size=self.x.shape)
        )
        y = retract(self.x, direction, 0.2)
        np.testing.assert_allclose(np.sum(y * y, axis=1), 1.0, atol=2e-15)
        np.testing.assert_allclose(
            np.sum(self.x * direction, axis=1), 0.0, atol=2e-15
        )

    def test_scaled_simplex(self):
        a = np.asarray([0.8, 0.7, -0.4, 0.1])
        projected, theta = project_to_scaled_simplex(a, 0.25)
        self.assertAlmostEqual(float(np.sum(projected)), 0.25, places=14)
        np.testing.assert_allclose(projected, np.maximum(a - theta, 0))

    def test_augmented_gradient(self):
        pairs = len(self.x) * (len(self.x) - 1) // 2
        multipliers = np.full(pairs, 1 / pairs)

        def function(y):
            value, gradient, _, _ = augmented_value_gradient(
                y, multipliers, 13.0
            )
            return value, gradient

        self.directional_check(function)

    def test_riesz_gradient(self):
        self.directional_check(lambda y: riesz_value_gradient(y, 7.0))

    def test_root_counts_and_norms(self):
        for roots, shape in (
            (d_roots(6), (60, 6)),
            (e6_roots(), (72, 6)),
            (e7_roots(), (126, 7)),
            (e8_roots(), (240, 8)),
        ):
            self.assertEqual(roots.shape, shape)
            np.testing.assert_allclose(
                np.sum(roots * roots, axis=1), 1.0, atol=2e-14
            )

    def test_deterministic_initializers(self):
        for kind in (
            "random",
            "warm41",
            "d6proj",
            "e6proj",
            "e7proj",
            "round2best",
        ):
            first = make_initial(41, 17, kind, WARM41, 100)
            second = make_initial(41, 17, kind, WARM41, 100)
            self.assertEqual(first.shape, (41, 5))
            np.testing.assert_array_equal(first, second)

    def test_diagnostics_include_explicit_graph(self):
        report = diagnostics(self.x)
        graph = report["active_graphs"]["1e-08"]
        self.assertEqual(graph["edge_count"], len(graph["edges_zero_based"]))
        self.assertEqual(len(graph["degree_sequence"]), len(self.x))
        self.assertEqual(
            sum(graph["degree_sequence"]), 2 * graph["edge_count"]
        )


if __name__ == "__main__":
    unittest.main()
