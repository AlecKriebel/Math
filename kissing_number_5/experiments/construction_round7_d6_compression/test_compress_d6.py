"""Unit tests for the dimension-compression search."""

from __future__ import annotations

import unittest

import numpy as np

from . import compress_d6


class CompressionTests(unittest.TestCase):
    def test_exact_d6_enumeration(self):
        roots, labels = compress_d6.d6_roots()
        self.assertEqual(roots.shape, (60, 6))
        self.assertEqual(len(set(map(tuple, labels))), 60)
        self.assertLess(
            np.max(np.abs(np.sum(roots * roots, axis=1) - 1.0)), 3e-16
        )
        values = compress_d6.pair_values(roots)
        self.assertAlmostEqual(float(np.max(values)), 0.5, places=14)
        for first in range(60):
            for second in range(first + 1, 60):
                self.assertLessEqual(
                    compress_d6.exact_pair_numerator(
                        labels[first], labels[second]
                    ),
                    1,
                )

    def test_collapse_gradient(self):
        rng = np.random.default_rng(1234)
        x = compress_d6.unit_rows(rng.normal(size=(9, 6)))
        flat = x.ravel()
        value, gradient = compress_d6.collapse_value_gradient(
            flat, 9, 6, 47.0, 0.23
        )
        direction = rng.normal(size=flat.shape)
        direction /= np.linalg.norm(direction)
        epsilon = 2e-7
        plus = compress_d6.collapse_value_gradient(
            flat + epsilon * direction, 9, 6, 47.0, 0.23
        )[0]
        minus = compress_d6.collapse_value_gradient(
            flat - epsilon * direction, 9, 6, 47.0, 0.23
        )[0]
        observed = (plus - minus) / (2 * epsilon)
        self.assertAlmostEqual(value, value)
        self.assertAlmostEqual(observed, float(gradient @ direction), 7)

    def test_projection_discards_bottom_covariance_direction(self):
        rng = np.random.default_rng(5678)
        x = compress_d6.unit_rows(rng.normal(size=(20, 6)))
        x[:, -1] *= 1e-4
        x = compress_d6.unit_rows(x)
        projected, record = compress_d6.project_to_five(x)
        self.assertEqual(projected.shape, (20, 5))
        self.assertLess(
            np.max(np.abs(np.sum(projected * projected, axis=1) - 1.0)),
            3e-15,
        )
        self.assertLess(
            record["six_dimensional_covariance_eigenvalues"][0], 1e-6
        )

    def test_subset_families_are_exact_and_distinct(self):
        rng = np.random.default_rng(9012)
        families = compress_d6.subset_initializations(43, rng)
        self.assertEqual(len(families), 4)
        label_sets = []
        for _, points, labels in families:
            self.assertEqual(points.shape, (43, 6))
            self.assertEqual(len(labels), 43)
            self.assertLessEqual(compress_d6.max_inner(points), 0.5 + 1e-15)
            label_sets.append(frozenset(map(tuple, labels)))
        self.assertEqual(len(set(label_sets)), 4)


if __name__ == "__main__":
    unittest.main()
