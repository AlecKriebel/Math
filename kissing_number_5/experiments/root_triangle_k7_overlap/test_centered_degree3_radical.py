#!/usr/bin/env python3

from fractions import Fraction
import json
from pathlib import Path
import unittest

from experiments.root_triangle_k7_overlap.derive_centered_degree3_radical import (
    evaluate_current_kernel_on_h_row,
    sample_rows,
)
from experiments.root_triangle_k7_overlap.search_root_triangle_degree3_psd import (
    invariant_monomial_orbits,
)


HERE = Path(__file__).resolve().parent
RADICAL = HERE / "centered_degree3_radical.json"


class CenteredDegreeThreeRadicalTests(unittest.TestCase):
    def test_scope_is_exact_sample_only(self):
        payload = json.loads(RADICAL.read_text())
        self.assertEqual(
            payload["status"],
            "EXACT-SAMPLE-CERTIFIED ONLY — UNIVERSALITY CONJECTURAL",
        )
        self.assertIn(
            "does not by itself prove a universal polynomial identity",
            payload["scope_warning"],
        )

    def test_holdout_evaluation_never_uses_binary_float(self):
        payload = json.loads(RADICAL.read_text())
        orbits = invariant_monomial_orbits(3)
        degrees = tuple(sum(orbit[0]) for orbit in orbits)
        row = sample_rows((9102471,), 1, orbits)[0]
        vector = tuple(payload["radical_vectors"][0])

        exact_value = evaluate_current_kernel_on_h_row(
            vector, row, degrees
        )
        self.assertIsInstance(exact_value, Fraction)
        self.assertEqual(exact_value, 0)

        # This is the precise regression that originally produced a false
        # holdout failure: `/` coerces the summands to binary floats.
        legacy_float_value = sum(
            coefficient * entry / 10**degree
            for coefficient, entry, degree in zip(vector, row, degrees)
        )
        self.assertNotEqual(legacy_float_value, 0.0)


if __name__ == "__main__":
    unittest.main()
