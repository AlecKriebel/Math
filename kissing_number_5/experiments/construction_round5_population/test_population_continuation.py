import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from .check_population import recompute
from .population_continuation import (
    align_parent,
    crossover,
    diagnostics,
    inverse_chord_objective,
    load_coordinate_runs,
    max_inner_product,
    unit_rows,
)
from .probe_tukey_depth import probe


class PopulationContinuationTests(unittest.TestCase):
    def test_gradient(self):
        rng = np.random.default_rng(123)
        x = unit_rows(rng.normal(size=(9, 5)))
        direction = rng.normal(size=x.shape)
        direction -= np.sum(direction * x, axis=1)[:, None] * x
        value, gradient = inverse_chord_objective(x.ravel(), 9, 7.0)
        self.assertTrue(np.isfinite(value))
        step = 2e-7
        plus = inverse_chord_objective(
            (x + step * direction).ravel(), 9, 7.0
        )[0]
        minus = inverse_chord_objective(
            (x - step * direction).ravel(), 9, 7.0
        )[0]
        numerical = (plus - minus) / (2.0 * step)
        analytic = float(gradient @ direction.ravel())
        self.assertAlmostEqual(numerical, analytic, places=7)

    def test_alignment_preserves_gram(self):
        rng = np.random.default_rng(456)
        x = unit_rows(rng.normal(size=(12, 5)))
        q, _ = np.linalg.qr(rng.normal(size=(5, 5)))
        permutation = rng.permutation(len(x))
        moving = x[permutation] @ q
        aligned, assignment = align_parent(x, moving)
        self.assertEqual(sorted(assignment.tolist()), list(range(len(x))))
        self.assertLess(float(np.max(np.abs(aligned - x))), 2e-12)
        self.assertAlmostEqual(
            max_inner_product(aligned), max_inner_product(moving), places=13
        )

    def test_crossover_releases_unit_coordinates(self):
        rng = np.random.default_rng(789)
        first = unit_rows(rng.normal(size=(15, 5)))
        second = unit_rows(rng.normal(size=(15, 5)))
        child, record = crossover(first, second, rng, 0.1)
        self.assertEqual(child.shape, first.shape)
        self.assertLess(
            float(np.max(np.abs(np.sum(child * child, axis=1) - 1.0))),
            3e-15,
        )
        self.assertIn(record["mode"], {"extrapolated_blend", "hyperplane_splice"})

    def test_checker_rejects_modified_maximum(self):
        rng = np.random.default_rng(321)
        x = unit_rows(rng.normal(size=(10, 5)))
        run = {"n": 10, "best": diagnostics(x)}
        self.assertAlmostEqual(recompute(run), max_inner_product(x), places=14)
        run["best"]["maximum"] += 1e-7
        with self.assertRaises(AssertionError):
            recompute(run)

    def test_tukey_probe_on_cross_polytope(self):
        x = np.vstack([np.eye(5), -np.eye(5)])
        result = probe(x)
        self.assertEqual(result["minimum_open_positive_count_found"], 1)
        self.assertEqual(result["negative_count"], 1)
        self.assertEqual(result["boundary_count"], 8)

    def test_load_list_shaped_coordinate_artifact(self):
        rng = np.random.default_rng(999)
        x = unit_rows(rng.normal(size=(7, 5)))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "coordinates.json"
            path.write_text(json.dumps([{"coordinates": x.tolist()}]))
            loaded = load_coordinate_runs(path)
        self.assertEqual(len(loaded), 1)
        self.assertLess(float(np.max(np.abs(loaded[0][0] - x))), 2e-15)


if __name__ == "__main__":
    unittest.main()
