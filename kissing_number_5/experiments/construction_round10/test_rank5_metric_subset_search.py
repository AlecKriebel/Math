#!/usr/bin/env python3
"""Tests for the round-10 structured numerical search and checker."""

from __future__ import annotations

import unittest

import numpy as np

from .rank5_metric_subset_search import (
    e6_roots,
    initial_map,
    local_subset_swaps,
    map_smoothmax_value_gradient,
    mapped_points,
    maximum_inner_product,
)


class RankFiveMetricSubsetTests(unittest.TestCase):
    def test_e6_shell(self) -> None:
        roots, labels = e6_roots()
        self.assertEqual(roots.shape, (72, 6))
        self.assertEqual(len(labels), 72)
        self.assertLessEqual(maximum_inner_product(roots), 0.500000000001)

    def test_general_map_gradient(self) -> None:
        roots, _ = e6_roots()
        matrix, _ = initial_map(roots, "E6", 2026072401, 1)
        selected = roots[np.arange(41)]
        _, gradient = map_smoothmax_value_gradient(
            matrix.ravel(), selected, 37.0
        )
        rng = np.random.default_rng(7)
        direction = rng.normal(size=gradient.shape)
        direction /= np.linalg.norm(direction)
        step = 2e-6
        plus = map_smoothmax_value_gradient(
            matrix.ravel() + step * direction, selected, 37.0
        )[0]
        minus = map_smoothmax_value_gradient(
            matrix.ravel() - step * direction, selected, 37.0
        )[0]
        finite_difference = (plus - minus) / (2.0 * step)
        self.assertAlmostEqual(
            finite_difference, float(gradient @ direction), places=7
        )

    def test_local_swaps_do_not_worsen_smooth_score_proxy(self) -> None:
        roots, _ = e6_roots()
        matrix, _ = initial_map(roots, "E6", 2026072402, 2)
        mapped = mapped_points(roots, matrix)
        subset = np.arange(41)
        initial = maximum_inner_product(mapped[subset])
        improved, _ = local_subset_swaps(
            mapped, subset, beta=1000.0, max_swaps=4
        )
        # At beta 1000 the smooth-score descent can change the literal maximum
        # by tiny amounts, so allow a conservative log(number of pairs)/beta.
        allowance = np.log(41 * 40 / 2) / 1000.0 + 1e-12
        self.assertLessEqual(
            maximum_inner_product(mapped[improved]), initial + allowance
        )


if __name__ == "__main__":
    unittest.main()
