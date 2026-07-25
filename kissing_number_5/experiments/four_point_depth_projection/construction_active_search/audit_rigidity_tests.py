#!/usr/bin/env python3
"""Adversarial tests for the rigidity soft-mode artifacts.

The numerical and rigidity computations here do not import the search code.
Only the explicit checker-tampering tests import ``rigidity_verify``.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RESULTS = HERE / "rigidity_softmode_results.json"
sys.path.insert(0, str(HERE))
import rigidity_verify  # noqa: E402  (checker under audit, not search code)


def unit_rows(value: Any) -> np.ndarray:
    points = np.asarray(value, dtype=np.float64)
    return points / np.linalg.norm(points, axis=1)[:, None]


def literal_coordinate_hash(points: np.ndarray) -> str:
    little = np.asarray(points, dtype="<f8", order="C")
    return hashlib.sha256(little.tobytes(order="C")).hexdigest()


def coordinate_diagnostics(value: Any) -> dict[str, Any]:
    literal = np.asarray(value, dtype=np.float64)
    points = unit_rows(literal)
    gram = points @ points.T
    upper = np.triu_indices(len(points), 1)
    values = gram[upper]
    index = int(np.argmax(values))
    return {
        "hash": literal_coordinate_hash(literal),
        "maximum": float(values[index]),
        "maximizing_pair": [int(upper[0][index]), int(upper[1][index])],
        "pairs_above_half": int(np.count_nonzero(values > 0.5)),
        "maximum_norm_squared_error": float(
            np.max(np.abs(np.sum(literal * literal, axis=1) - 1.0))
        ),
    }


def active_edges(points: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    gram = points @ points.T
    np.fill_diagonal(gram, -np.inf)
    maximum = float(np.max(gram))
    edges = np.argwhere(np.triu(gram >= maximum - 1e-8, k=1))
    degrees = np.bincount(edges.ravel(), minlength=len(points))
    return maximum, edges, degrees


def tangent_quotient(
    points: np.ndarray, edges: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Independently build the contact derivative modulo rotations."""
    n = len(points)
    tangent_bases: list[np.ndarray] = []
    for point in points:
        _, _, right = np.linalg.svd(point.reshape(1, 5), full_matrices=True)
        tangent_bases.append(right[1:].T)

    derivative = np.zeros((len(edges), 4 * n))
    for row, (first, second) in enumerate(edges):
        derivative[row, 4 * first : 4 * first + 4] = (
            points[second] @ tangent_bases[first]
        )
        derivative[row, 4 * second : 4 * second + 4] = (
            points[first] @ tangent_bases[second]
        )

    rotations = []
    for first_coordinate in range(5):
        for second_coordinate in range(first_coordinate + 1, 5):
            velocity = np.zeros((n, 4))
            for point_index, point in enumerate(points):
                ambient = np.zeros(5)
                ambient[first_coordinate] = -point[second_coordinate]
                ambient[second_coordinate] = point[first_coordinate]
                velocity[point_index] = (
                    tangent_bases[point_index].T @ ambient
                )
            rotations.append(velocity.ravel())
    rotation_matrix = np.asarray(rotations).T
    complete_q, _ = np.linalg.qr(rotation_matrix, mode="complete")
    rotation_complement = complete_q[:, 10:]
    quotient = derivative @ rotation_complement
    return derivative, rotation_matrix, quotient


def baseline_points(n: int) -> np.ndarray:
    if n == 41:
        return unit_rows(
            np.loadtxt(
                REPO / "experiments/input/spherical_codes_5_41.txt",
                delimiter=",",
            )
        )
    if n in (42, 43):
        path = (
            REPO
            / "experiments/construction_round9_core_rattler/results/"
            "core_rattler_portfolio.json"
        )
        payload = json.loads(path.read_text())
        return unit_rows(
            payload["runs"][n - 41]["best"]["coordinates_float64"]
        )
    if n == 44:
        path = (
            REPO
            / "experiments/construction_round6_bundle/results/"
            "bundle_portfolio.json"
        )
        payload = json.loads(path.read_text())
        return unit_rows(
            payload["runs"][19]["best"]["coordinates_float64"]
        )
    raise ValueError(n)


class RigidityArtifactAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(RESULTS.read_text())

    def checker_result_for(self, payload: dict[str, Any]) -> dict[str, Any]:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "candidate.json"
            path.write_text(json.dumps(payload))
            return rigidity_verify.check(path)

    def test_independent_all_coordinate_hashes_and_maxima(self) -> None:
        for run in self.payload["runs"]:
            n = run["n"]
            for label, record in [
                ("best", run["best"]),
                *[
                    (f"trial {index}", trial)
                    for index, trial in enumerate(run["trials"])
                ],
            ]:
                actual = coordinate_diagnostics(record["coordinates_float64"])
                expected = record["diagnostics"]
                self.assertEqual(
                    actual["hash"],
                    expected["coordinate_little_endian_float64_sha256"],
                    (n, label),
                )
                self.assertAlmostEqual(
                    actual["maximum"],
                    expected["maximum_inner_product"],
                    places=14,
                    msg=f"N={n} {label}",
                )
                self.assertLessEqual(
                    actual["maximum_norm_squared_error"], 1e-14
                )

    def test_baselines_best_selection_and_flags(self) -> None:
        expected = {
            41: (0.5149946525121660, False),
            42: (0.5182411558622624, False),
            43: (0.5247096018290193, True),
            44: (0.5274577123235322, True),
        }
        for run in self.payload["runs"]:
            n = run["n"]
            baseline = baseline_points(n)
            # The producer normalizes once while loading and again inside its
            # diagnostics routine.  Reproduce that second binary64 operation
            # explicitly; it can change the literal coordinate hash by a bit.
            baseline_actual = coordinate_diagnostics(unit_rows(baseline))
            self.assertEqual(
                baseline_actual["hash"],
                run["baseline"]["coordinate_little_endian_float64_sha256"],
            )
            self.assertAlmostEqual(
                baseline_actual["maximum"],
                run["baseline"]["maximum_inner_product"],
                places=14,
            )
            best_actual = coordinate_diagnostics(
                run["best"]["coordinates_float64"]
            )
            self.assertAlmostEqual(best_actual["maximum"], expected[n][0], 14)
            self.assertEqual(run["beat_baseline"], expected[n][1])
            self.assertFalse(run["reached_half"])
            enumerated = [
                coordinate_diagnostics(trial["coordinates_float64"])[
                    "maximum"
                ]
                for trial in run["trials"]
            ]
            if expected[n][1]:
                self.assertAlmostEqual(best_actual["maximum"], min(enumerated), 14)
                best_hash = run["best"]["diagnostics"][
                    "coordinate_little_endian_float64_sha256"
                ]
                self.assertIn(
                    best_hash,
                    {
                        trial["diagnostics"][
                            "coordinate_little_endian_float64_sha256"
                        ]
                        for trial in run["trials"]
                    },
                )
            else:
                self.assertEqual(
                    best_actual["hash"], baseline_actual["hash"]
                )

    def test_n41_core_is_numerically_infinitesimally_rigid(self) -> None:
        run = next(run for run in self.payload["runs"] if run["n"] == 41)
        points = baseline_points(41)
        _, edges, degrees = active_edges(points)
        core_indices = np.flatnonzero(degrees > 0)
        self.assertTrue(np.array_equal(core_indices, np.arange(35)))
        self.assertEqual(len(edges), 153)
        core = points[core_indices]
        _, core_edges, _ = active_edges(core)
        derivative, rotations, quotient = tangent_quotient(core, core_edges)
        self.assertEqual(derivative.shape, (153, 140))
        self.assertEqual(np.linalg.matrix_rank(rotations), 10)
        self.assertLess(np.linalg.norm(derivative @ rotations), 5e-14)
        self.assertEqual(np.linalg.matrix_rank(derivative), 130)
        self.assertEqual(np.linalg.matrix_rank(quotient), 130)
        singular_values = np.linalg.svd(quotient, compute_uv=False)
        self.assertGreater(singular_values[-1], 0.13)
        structure = run["structure"]
        self.assertEqual(structure["active_vertex_count"], 35)
        self.assertEqual(structure["inactive_vertex_count"], 6)
        self.assertEqual(structure["active_core_edge_count"], 153)
        self.assertEqual(
            structure["active_core_constrained_rigidity_rank_binary64"],
            175,
        )
        self.assertEqual(
            structure["active_core_constrained_rigidity_nullity_binary64"],
            0,
        )
        self.assertEqual(structure["edge_deletion_count_per_trial"], 24)
        # 129 retained contacts leave at least 140-129-10 = 1
        # nonrotational tangent degree of freedom, independently of rank.
        self.assertEqual(153 - 24, 129)

        modes_by_seed: dict[int, dict[str, Any]] = {}
        for trial in run["trials"]:
            mode = trial["mode"]
            seed = mode["seed"]
            if seed in modes_by_seed:
                self.assertEqual(mode, modes_by_seed[seed])
            else:
                modes_by_seed[seed] = mode
        self.assertEqual(
            sorted(modes_by_seed), list(range(2026072301, 2026072309))
        )
        core_edge_set = {
            (int(first), int(second)) for first, second in core_edges
        }
        for mode in modes_by_seed.values():
            deleted = {
                (int(first), int(second))
                for first, second in mode["deleted_edges"]
            }
            self.assertEqual(len(deleted), 24)
            self.assertTrue(deleted <= core_edge_set)
            retained = np.asarray(
                sorted(core_edge_set - deleted), dtype=np.int64
            )
            self.assertEqual(retained.shape, (129, 2))
            _, _, released_quotient = tangent_quotient(core, retained)
            self.assertEqual(released_quotient.shape, (129, 130))
            self.assertEqual(np.linalg.matrix_rank(released_quotient), 129)
            self.assertEqual(mode["matrix_shape"], [174, 175])
            self.assertEqual(mode["matrix_rank_binary64"], 174)
            self.assertEqual(mode["nullity_binary64"], 1)

    def test_n42_inactive_vertices_and_n43_n44_soft_modes(self) -> None:
        expected = {
            42: {
                "edges": 173,
                "zeros": 2,
                "quotient_shape": (173, 158),
                "rank": 150,
            },
            43: {
                "edges": 172,
                "zeros": 0,
                "quotient_shape": (172, 162),
                "rank": 162,
            },
            44: {
                "edges": 182,
                "zeros": 0,
                "quotient_shape": (182, 166),
                "rank": 165,
            },
        }
        spectra: dict[int, np.ndarray] = {}
        for n, claim in expected.items():
            points = baseline_points(n)
            _, edges, degrees = active_edges(points)
            self.assertEqual(len(edges), claim["edges"])
            self.assertEqual(int(np.count_nonzero(degrees == 0)), claim["zeros"])
            derivative, rotations, quotient = tangent_quotient(points, edges)
            self.assertLess(np.linalg.norm(derivative @ rotations), 5e-14)
            self.assertEqual(quotient.shape, claim["quotient_shape"])
            self.assertEqual(np.linalg.matrix_rank(quotient), claim["rank"])
            spectra[n] = np.linalg.svd(quotient, compute_uv=False)

        # N=43 is full rank modulo rotations but has three clearly resolved
        # near-singular values.
        self.assertGreater(spectra[43][-1], 4e-8)
        self.assertLess(spectra[43][-1], 5e-8)
        self.assertGreater(spectra[43][-2], 1.2e-7)
        self.assertLess(spectra[43][-2], 1.4e-7)
        self.assertGreater(spectra[43][-3], 2.8e-7)
        self.assertLess(spectra[43][-3], 3.0e-7)

        # N=44 has one numerical nonrotational null direction and a separate
        # well-resolved near mode.
        self.assertLess(spectra[44][-1], 1e-12)
        self.assertGreater(spectra[44][-2], 1e-6)
        self.assertLess(spectra[44][-2], 2e-6)

    def test_one_solver_failure_is_disclosed_and_not_selected(self) -> None:
        failures = [
            trial
            for run in self.payload["runs"]
            for trial in run["trials"]
            if not trial["solver"]["success"]
        ]
        self.assertEqual(len(failures), 1)
        self.assertEqual(
            failures[0]["label"], "N44_tail1_sign-1_scale0.1"
        )
        best_hashes = {
            run["best"]["diagnostics"][
                "coordinate_little_endian_float64_sha256"
            ]
            for run in self.payload["runs"]
        }
        self.assertNotIn(
            failures[0]["diagnostics"][
                "coordinate_little_endian_float64_sha256"
            ],
            best_hashes,
        )

    def test_checker_rejects_coordinate_hash_maximum_and_flag_tampering(
        self,
    ) -> None:
        mutations = []

        coordinate = copy.deepcopy(self.payload)
        coordinate["runs"][0]["trials"][0]["coordinates_float64"][0][0] += 1e-4
        mutations.append(coordinate)

        hash_tamper = copy.deepcopy(self.payload)
        hash_tamper["runs"][1]["best"]["diagnostics"][
            "coordinate_little_endian_float64_sha256"
        ] = "0" * 64
        mutations.append(hash_tamper)

        maximum = copy.deepcopy(self.payload)
        maximum["runs"][2]["best"]["diagnostics"][
            "maximum_inner_product"
        ] += 1e-5
        mutations.append(maximum)

        reached = copy.deepcopy(self.payload)
        reached["runs"][3]["reached_half"] = True
        mutations.append(reached)

        beat = copy.deepcopy(self.payload)
        beat["runs"][2]["beat_baseline"] = False
        mutations.append(beat)

        for payload in mutations:
            with self.assertRaises(AssertionError):
                self.checker_result_for(payload)

    def test_checker_scope_does_not_cover_structure_modes_or_baseline_source(
        self,
    ) -> None:
        tampered = copy.deepcopy(self.payload)
        tampered["runs"][0]["structure"][
            "active_core_constrained_rigidity_rank_binary64"
        ] = 0
        tampered["runs"][2]["trials"][0]["mode"][
            "matrix_rank_binary64"
        ] = 0
        tampered["runs"][2]["baseline"]["maximum_inner_product"] = 0.6
        # The existing true flag remains internally consistent with 0.6.
        result = self.checker_result_for(tampered)
        self.assertTrue(result["all_checks_passed"])


if __name__ == "__main__":
    unittest.main()
