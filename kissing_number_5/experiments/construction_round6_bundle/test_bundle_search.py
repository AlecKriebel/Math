"""Tests for the round-6 numerical search and independent checker."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from . import bundle_search
from .check_bundle import check_run


class BundleSearchTests(unittest.TestCase):
    def test_smooth_gradient(self):
        rng = np.random.default_rng(123)
        x = bundle_search.unit_rows(rng.normal(size=(7, 5)))
        flat = x.ravel()
        value, gradient = bundle_search.smooth_max_value_gradient(
            flat, 7, 31.0
        )
        direction = rng.normal(size=flat.shape)
        direction /= np.linalg.norm(direction)
        epsilon = 2e-7
        plus = bundle_search.smooth_max_value_gradient(
            flat + epsilon * direction, 7, 31.0
        )[0]
        minus = bundle_search.smooth_max_value_gradient(
            flat - epsilon * direction, 7, 31.0
        )[0]
        finite_difference = (plus - minus) / (2.0 * epsilon)
        self.assertAlmostEqual(value, value)
        self.assertAlmostEqual(finite_difference, float(gradient @ direction), 7)

    def test_bundle_direction_is_tangent(self):
        rng = np.random.default_rng(456)
        x = bundle_search.unit_rows(rng.normal(size=(9, 5)))
        direction, record = bundle_search.solve_proximal_bundle(
            x, radius=0.04, band=0.05, max_cuts=60
        )
        self.assertLessEqual(np.linalg.norm(direction), 0.041)
        self.assertLess(np.max(np.abs(np.sum(direction * x, axis=1))), 2e-13)
        self.assertAlmostEqual(
            sum(record["dual_support_weights"]), 1.0, places=10
        )

    def test_d5_diagnostics_and_independent_check(self):
        x = bundle_search.d5_roots()
        stored = bundle_search.diagnostics(x)
        run = {"n": 40, "best": stored}
        self.assertAlmostEqual(check_run(run), 0.5, places=14)
        self.assertEqual(stored["active_1e-08"]["edge_count"], 240)

    def test_loader_understands_round4_and_round5_shapes(self):
        x = bundle_search.d5_roots()[:6]
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            round4 = directory / "round4.json"
            round5 = directory / "round5.json"
            round4.write_text(
                json.dumps({"runs": [{"n": 6, "coordinates": x.tolist()}]})
            )
            round5.write_text(
                json.dumps(
                    {
                        "runs": [
                            {
                                "n": 6,
                                "best": {"coordinates_float64": x.tolist()},
                            }
                        ]
                    }
                )
            )
            self.assertEqual(len(bundle_search.load_runs(round4)), 1)
            self.assertEqual(len(bundle_search.load_runs(round5)), 1)


if __name__ == "__main__":
    unittest.main()
