#!/usr/bin/env python3
"""Regression tests for the alternating Gram construction search."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

import gram_inventory
import gram_search
import gram_verify


HERE = Path(__file__).resolve().parent


class GramSearchTests(unittest.TestCase):
    def test_warm_start_inventory_values(self) -> None:
        expected = {
            41: 0.5149946525121660,
            42: 0.5182411558622624,
            43: 0.5247244770145227,
            44: 0.5274711925359574,
        }
        for n, expected_maximum in expected.items():
            points, _ = gram_search.load_warm_start(n)
            actual = gram_search.objective(points)["maximum_inner_product"]
            self.assertAlmostEqual(actual, expected_maximum, places=14)

    def test_rank_projection_is_correlation_rank_five(self) -> None:
        rng = np.random.default_rng(12345)
        matrix = rng.normal(size=(41, 41))
        matrix = 0.5 * (matrix + matrix.T)
        points, gram, _ = gram_search.project_psd_rank_correlation(matrix)
        self.assertEqual(points.shape, (41, 5))
        self.assertLessEqual(np.max(np.abs(np.diag(gram) - 1.0)), 5e-15)
        eigenvalues = np.linalg.eigvalsh(gram)
        self.assertGreaterEqual(eigenvalues[0], -2e-14)
        self.assertLessEqual(np.max(np.abs(eigenvalues[:-5])), 2e-14)

    def test_plain_halfspace_projection_moves_only_valid_direction(self) -> None:
        points, _ = gram_search.load_warm_start(41)
        gram = points @ points.T
        schedule = gram_search.SCHEDULES[0]
        corrected, memory = gram_search.halfspace_correction(
            gram, np.zeros_like(gram), schedule
        )
        upper = np.triu_indices(41, 1)
        before = gram[upper]
        after = corrected[upper]
        self.assertTrue(np.all(after <= before + 1e-16))
        self.assertTrue(np.all(after[before <= 0.5] == before[before <= 0.5]))
        self.assertTrue(np.all(after[before > 0.5] < before[before > 0.5]))
        self.assertTrue(np.all(memory == 0.0))

    def test_multi_entry_kick_is_seeded_and_symmetric(self) -> None:
        points, _ = gram_search.load_warm_start(42)
        gram = points @ points.T
        left = gram_search.multi_entry_kick(
            gram,
            np.random.default_rng(777),
            amplitude=0.004,
            edge_count=17,
            active_band=0.02,
        )
        right = gram_search.multi_entry_kick(
            gram,
            np.random.default_rng(777),
            amplitude=0.004,
            edge_count=17,
            active_band=0.02,
        )
        self.assertTrue(np.array_equal(left, right))
        self.assertTrue(np.array_equal(left, left.T))
        changed = np.count_nonzero(np.triu(left != gram, 1))
        self.assertEqual(changed, 17)
        self.assertTrue(np.array_equal(np.diag(left), np.ones(42)))

    def test_inventory_excludes_nonfive_dimensional_coordinates(self) -> None:
        payload = {
            "coordinates_float64": np.zeros((41, 6)).tolist(),
            "child": {"coordinates": np.zeros((42, 5)).tolist()},
        }
        found = list(gram_inventory.iter_coordinate_arrays(payload))
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0][1].shape, (42, 5))

    def test_production_result_verifies(self) -> None:
        path = HERE / "gram_search_results.json"
        if not path.exists():
            self.skipTest("production result not generated")
        result = gram_verify.verify(path)
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["candidate_at_or_below_threshold_found"])

    def test_verifier_rejects_tampered_maximum(self) -> None:
        path = HERE / "gram_search_results.json"
        if not path.exists():
            self.skipTest("production result not generated")
        payload = json.loads(path.read_text())
        payload["best_by_n"]["41"]["best_objective"][
            "maximum_inner_product"
        ] -= 1e-5
        with tempfile.TemporaryDirectory() as temporary:
            tampered = Path(temporary) / "tampered.json"
            tampered.write_text(json.dumps(payload))
            with self.assertRaises(AssertionError):
                gram_verify.verify(tampered)


if __name__ == "__main__":
    unittest.main()
