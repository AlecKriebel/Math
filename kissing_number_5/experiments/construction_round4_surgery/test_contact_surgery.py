import importlib.util
from pathlib import Path
import unittest

import numpy as np


PATH = Path(__file__).with_name("contact_surgery.py")
SPEC = importlib.util.spec_from_file_location("contact_surgery", PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ContactSurgeryTests(unittest.TestCase):
    def test_d5(self):
        roots = MODULE.d5_roots()
        self.assertEqual(roots.shape, (40, 5))
        self.assertLess(
            float(np.max(np.abs(np.sum(roots * roots, axis=1) - 1.0))),
            1e-14,
        )
        self.assertAlmostEqual(MODULE.max_inner_product(roots), 0.5, places=14)

    def test_full_gradient(self):
        rng = np.random.default_rng(17)
        raw = rng.normal(size=(7, 5))
        beta = 31.0
        value, gradient = MODULE.smooth_full(raw.ravel(), 7, beta)
        self.assertTrue(np.isfinite(value))
        direction = rng.normal(size=raw.size)
        direction /= np.linalg.norm(direction)
        epsilon = 1e-6
        plus = MODULE.smooth_full(
            raw.ravel() + epsilon * direction, 7, beta
        )[0]
        minus = MODULE.smooth_full(
            raw.ravel() - epsilon * direction, 7, beta
        )[0]
        finite_difference = (plus - minus) / (2.0 * epsilon)
        analytic = float(gradient @ direction)
        self.assertLess(abs(finite_difference - analytic), 2e-8)

    def test_hole_gradient(self):
        rng = np.random.default_rng(23)
        fixed = MODULE.unit_rows(rng.normal(size=(13, 5)))
        raw = rng.normal(size=5)
        beta = 47.0
        value, gradient = MODULE.smooth_hole(raw, fixed, beta)
        self.assertTrue(np.isfinite(value))
        direction = rng.normal(size=5)
        direction /= np.linalg.norm(direction)
        epsilon = 1e-6
        plus = MODULE.smooth_hole(
            raw + epsilon * direction, fixed, beta
        )[0]
        minus = MODULE.smooth_hole(
            raw - epsilon * direction, fixed, beta
        )[0]
        finite_difference = (plus - minus) / (2.0 * epsilon)
        analytic = float(gradient @ direction)
        self.assertLess(abs(finite_difference - analytic), 2e-8)


if __name__ == "__main__":
    unittest.main()
