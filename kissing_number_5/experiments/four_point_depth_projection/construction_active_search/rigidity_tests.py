#!/usr/bin/env python3
"""Regression and tamper tests for active-rigidity construction artifacts."""

from __future__ import annotations

import copy
import json
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

import rigidity_softmode_search as search
import rigidity_verify as verify


DIRECTORY = Path(__file__).resolve().parent
RESULTS = DIRECTORY / "rigidity_softmode_results.json"


def d5_roots() -> np.ndarray:
    roots = []
    for first in range(5):
        for second in range(first + 1, 5):
            for first_sign in (-1.0, 1.0):
                for second_sign in (-1.0, 1.0):
                    row = np.zeros(5)
                    row[first] = first_sign / math.sqrt(2.0)
                    row[second] = second_sign / math.sqrt(2.0)
                    roots.append(row)
    return np.asarray(roots)


class GeometryTests(unittest.TestCase):
    def test_d5_known_example(self):
        roots = d5_roots()
        self.assertEqual(roots.shape, (40, 5))
        self.assertAlmostEqual(search.maximum_inner_product(roots), 0.5)

    def test_rotation_rows_annihilate_gram_derivatives(self):
        rng = np.random.default_rng(2026072319)
        x = search.unit_rows(rng.normal(size=(9, 5)))
        rotations = search.rotation_rows(x)
        self.assertEqual(rotations.shape, (10, 45))
        for velocity in rotations.reshape(10, 9, 5):
            derivative = velocity @ x.T + x @ velocity.T
            self.assertLess(float(np.max(np.abs(derivative))), 2e-15)


class ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(RESULTS.read_text())

    def write_payload(self, payload: dict) -> Path:
        temporary = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        json.dump(payload, temporary)
        temporary.close()
        return Path(temporary.name)

    def test_independent_checker_accepts_result(self):
        result = verify.check(RESULTS)
        self.assertTrue(result["all_checks_passed"])
        self.assertEqual([run["n"] for run in result["runs"]], [41, 42, 43, 44])
        self.assertFalse(result["runs"][0]["reached_half"])
        self.assertTrue(result["runs"][2]["beat_baseline"])
        self.assertTrue(result["runs"][3]["beat_baseline"])

    def test_coordinate_tamper_is_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["runs"][0]["trials"][0]["coordinates_float64"][0][0] += 1e-4
        path = self.write_payload(payload)
        self.addCleanup(path.unlink)
        with self.assertRaisesRegex(AssertionError, "hash mismatch"):
            verify.check(path)

    def test_reported_maximum_tamper_is_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["runs"][2]["best"]["diagnostics"][
            "maximum_inner_product"
        ] -= 1e-4
        path = self.write_payload(payload)
        self.addCleanup(path.unlink)
        with self.assertRaisesRegex(AssertionError, "maximum mismatch"):
            verify.check(path)

    def test_threshold_flag_tamper_is_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["runs"][3]["reached_half"] = True
        path = self.write_payload(payload)
        self.addCleanup(path.unlink)
        with self.assertRaisesRegex(AssertionError, "threshold flag mismatch"):
            verify.check(path)


if __name__ == "__main__":
    unittest.main()
