#!/usr/bin/env python3
"""Regression and tamper tests for the deflation construction portfolio."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "deflate_results.json"
sys.path.insert(0, str(HERE))
import deflate_verify  # noqa: E402


class DeflationPortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(RESULTS.read_text())

    def check_payload(self, payload: dict) -> dict:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "candidate.json"
            path.write_text(json.dumps(payload))
            return deflate_verify.check(path)

    def test_independent_checker_passes(self) -> None:
        result = deflate_verify.check(RESULTS)
        self.assertTrue(result["all_checks_passed"])
        self.assertFalse(result["any_threshold_candidate_found"])
        self.assertEqual(result["run_count"], 40)

    def test_portfolio_contains_warm_and_fresh_starts(self) -> None:
        origins = [run["origin"] for run in self.payload["runs"]]
        self.assertEqual(origins.count("warm_perturbed"), 20)
        self.assertEqual(origins.count("fresh_asymmetric_gaussian"), 20)
        for n in range(41, 45):
            seeds = [
                run["seed"] for run in self.payload["runs"] if run["n"] == n
            ]
            self.assertEqual(
                seeds,
                list(
                    range(
                        2026072700 + 100 * (n - 41),
                        2026072710 + 100 * (n - 41),
                    )
                ),
            )

    def test_every_stored_factor_is_unit_and_rank_at_most_five(self) -> None:
        records = [
            (
                run["n"],
                run["best_coordinates_float64"],
                run["best_diagnostics"],
            )
            for run in self.payload["runs"]
        ] + [
            (
                int(n),
                record["coordinates_float64"],
                record["diagnostics"],
            )
            for n, record in self.payload["best_by_n"].items()
        ]
        for n, coordinates, diagnostics in records:
            points = np.asarray(coordinates, dtype=np.float64)
            self.assertEqual(points.shape, (n, 5))
            self.assertLessEqual(
                float(
                    np.max(
                        np.abs(np.sum(points * points, axis=1) - 1.0)
                    )
                ),
                2e-14,
            )
            gram = points @ points.T
            spectrum = np.linalg.eigvalsh(gram)
            self.assertGreaterEqual(float(spectrum[0]), -6e-12)
            self.assertLessEqual(
                float(np.max(np.abs(spectrum[:-5]))), 6e-12
            )
            self.assertEqual(diagnostics["numerical_rank_at_1e-10"], 5)

    def test_three_deflation_windows_and_edge_states_per_run(self) -> None:
        for run in self.payload["runs"]:
            homotopy = run["homotopy"]
            self.assertEqual(len(homotopy["deflation_events"]), 3)
            for event in homotopy["deflation_events"]:
                self.assertGreater(event["reentry_epoch"], event["delete_epoch"])
                self.assertEqual(
                    len(event["deleted_edges"]),
                    event["deleted_edge_count"],
                )
            edge_count = run["n"] * (run["n"] - 1) // 2
            for values in homotopy["final_edge_state"].values():
                self.assertEqual(len(values), edge_count)

    def test_no_significant_record_improvement(self) -> None:
        expected = {
            "41": 0.5149946525121660,
            "42": 0.5182411558622624,
            "43": 0.5247096018290193,
            "44": 0.5274577123235322,
        }
        for n, maximum in expected.items():
            record = self.payload["best_by_n"][n]
            self.assertAlmostEqual(
                record["diagnostics"]["maximum_inner_product"],
                maximum,
                places=14,
            )
            self.assertFalse(record["strictly_beats_warm_record"])
            self.assertFalse(record["reaches_one_half_binary64"])
            self.assertIsNone(record["winning_restart"])

    def test_checker_rejects_coordinate_hash_maximum_flag_seed_and_source(
        self,
    ) -> None:
        mutations = []

        coordinate = copy.deepcopy(self.payload)
        coordinate["runs"][0]["best_coordinates_float64"][0][0] += 1e-4
        mutations.append(coordinate)

        hash_tamper = copy.deepcopy(self.payload)
        hash_tamper["best_by_n"]["42"]["diagnostics"][
            "coordinate_little_endian_float64_sha256"
        ] = "0" * 64
        mutations.append(hash_tamper)

        maximum = copy.deepcopy(self.payload)
        maximum["runs"][20]["best_diagnostics"][
            "maximum_inner_product"
        ] += 1e-5
        mutations.append(maximum)

        flag = copy.deepcopy(self.payload)
        flag["best_by_n"]["44"]["reaches_one_half_binary64"] = True
        mutations.append(flag)

        seed = copy.deepcopy(self.payload)
        seed["runs"][11]["seed"] += 1
        mutations.append(seed)

        source = copy.deepcopy(self.payload)
        source["runs"][30]["warm_source"]["source_file_sha256"] = "f" * 64
        mutations.append(source)

        for payload in mutations:
            with self.assertRaises(AssertionError):
                self.check_payload(payload)

    def test_checker_rejects_corrupt_edge_state_and_deflation_manifest(
        self,
    ) -> None:
        negative_slack = copy.deepcopy(self.payload)
        negative_slack["runs"][0]["homotopy"]["final_edge_state"][
            "slack_at_one_half"
        ][0] = -0.1
        with self.assertRaises(AssertionError):
            self.check_payload(negative_slack)

        duplicate_edge = copy.deepcopy(self.payload)
        event = duplicate_edge["runs"][1]["homotopy"][
            "deflation_events"
        ][0]
        event["deleted_edges"][1] = event["deleted_edges"][0]
        with self.assertRaises(AssertionError):
            self.check_payload(duplicate_edge)


if __name__ == "__main__":
    unittest.main()
