#!/usr/bin/env python3
"""Regression and tamper tests for thermal population construction search."""

from __future__ import annotations

import copy
import json
import math
import tempfile
import unittest
from pathlib import Path

import numpy as np

import thermal_population_escape as search
import thermal_verify as verifier


DIRECTORY = Path(__file__).resolve().parent
PORTFOLIO = DIRECTORY / "thermal_portfolio.json"


def d5_roots() -> np.ndarray:
    rows = []
    for first in range(5):
        for second in range(first + 1, 5):
            for first_sign in (-1.0, 1.0):
                for second_sign in (-1.0, 1.0):
                    row = np.zeros(5)
                    row[first] = first_sign / math.sqrt(2.0)
                    row[second] = second_sign / math.sqrt(2.0)
                    rows.append(row)
    return np.asarray(rows)


class ThermalGeometryTests(unittest.TestCase):
    def test_d5_threshold_energy(self):
        roots = d5_roots()
        self.assertAlmostEqual(search.maximum(roots), 0.5)
        self.assertLess(search.threshold_energy(roots), 1e-28)

    def test_threshold_gradient_finite_difference(self):
        rng = np.random.default_rng(2026075199)
        x = search.unit_rows(rng.normal(size=(9, 5)))
        inherited = search.active_edges(x, 1e-5)
        mask = np.zeros((len(x), len(x)))
        mask[inherited[:, 0], inherited[:, 1]] = 1.0
        mask += mask.T
        top = search.maximum(x)
        energy, bias_energy, gradient = search.threshold_energy_gradient(
            x, mask, top, 0.7, 0.025
        )
        direction = rng.normal(size=x.shape)
        direction -= np.sum(direction * x, axis=1)[:, None] * x
        epsilon = 1e-7

        def combined(points):
            base, bias, _ = search.threshold_energy_gradient(
                points, mask, top, 0.7, 0.025
            )
            return base + 0.7 * bias

        plus = combined(search.unit_rows(x + epsilon * direction))
        minus = combined(search.unit_rows(x - epsilon * direction))
        numerical = (plus - minus) / (2.0 * epsilon)
        analytic = float(np.sum(gradient * direction))
        self.assertAlmostEqual(energy + 0.7 * bias_energy, combined(x))
        self.assertLess(abs(numerical - analytic), 2e-6)


class ThermalArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(PORTFOLIO.read_text())

    def temporary_payload(self, payload: dict) -> Path:
        handle = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        json.dump(payload, handle)
        handle.close()
        return Path(handle.name)

    def test_portfolio_verifies(self):
        checked = verifier.verify(PORTFOLIO)
        self.assertTrue(checked["all_coordinate_checks_passed"])
        self.assertFalse(checked["binary64_threshold_hit"])
        self.assertEqual(len(checked["runs"]), 8)

    def test_seeds_and_basin_melting_are_recorded(self):
        expected = [
            (41, "mild", 2026075100),
            (41, "strong", 2026075101),
            (42, "mild", 2026075200),
            (42, "strong", 2026075201),
            (43, "mild", 2026075300),
            (43, "strong", 2026075301),
            (44, "mild", 2026075400),
            (44, "strong", 2026075401),
        ]
        self.assertEqual(
            [
                (run["n"], run["regime"], run["seed"])
                for run in self.payload["runs"]
            ],
            expected,
        )
        for run in self.payload["runs"]:
            self.assertTrue(
                any(
                    stage["minimum_old_graph_jaccard"] == 0.0
                    for stage in run["stage_records"]
                )
            )

    def test_coordinate_tamper_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["runs"][0]["best"]["coordinates_float64"][0][0] += 1e-4
        path = self.temporary_payload(payload)
        self.addCleanup(path.unlink)
        with self.assertRaisesRegex(AssertionError, "hash mismatch"):
            verifier.verify(path)

    def test_origin_hash_tamper_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["runs"][0]["origin_sha256"] = "0" * 64
        path = self.temporary_payload(payload)
        self.addCleanup(path.unlink)
        with self.assertRaisesRegex(AssertionError, "origin hash mismatch"):
            verifier.verify(path)

    def test_threshold_flag_tamper_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["binary64_threshold_hit"] = True
        path = self.temporary_payload(payload)
        self.addCleanup(path.unlink)
        with self.assertRaisesRegex(AssertionError, "global threshold"):
            verifier.verify(path)


if __name__ == "__main__":
    unittest.main()
