#!/usr/bin/env python3
"""Standard-library regression and tamper tests for both K7 verifiers."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from experiments.four_point_depth_projection.k7_product_audit import (
    verify_candidate_k7_product as direct,
)
from experiments.four_point_depth_projection.k7_product_audit import (
    verify_candidate_k7_via_k6_faces as via_faces,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


class CandidateK7VerificationTests(unittest.TestCase):
    def test_direct_verifier_passes_exactly(self) -> None:
        report = direct.verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["candidate_sha256"], direct.CANDIDATE_SHA256)
        self.assertEqual(report["positive_atoms"], 53)
        self.assertEqual(report["minimum_positive_scaled_fifth_minor"], 6)
        self.assertEqual(report["product_rows"], 560)
        self.assertEqual(report["zero_product_rows"], 65)
        self.assertEqual(report["edge_marginal"], (
            "exact alpha/40 per uniformly sampled K7 edge"
        ))
        self.assertEqual(report["triangle_marginal"], (
            "exact nu/1560 per uniformly sampled K7 triangle"
        ))

    def test_ldlt_and_deleted_k6_verifier_passes_exactly(self) -> None:
        report = via_faces.verify()
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["candidate_sha256"], via_faces.CANDIDATE_SHA256)
        self.assertEqual(report["positive_atoms"], 53)
        self.assertEqual(report["minimum_positive_ldl_pivot"], "3/22")
        self.assertEqual(report["product_rows_via_k6_faces"], 560)
        self.assertEqual(report["zero_product_rows"], 65)
        self.assertEqual(report["edge_marginal"], "exact alpha/40")
        self.assertEqual(report["triangle_marginal"], "exact nu/1560")

    def test_sum_preserving_weight_tamper_reaches_marginal_equations(self) -> None:
        """Rehash a weight perturbation and ensure exact marginals reject it."""

        candidate = json.loads(via_faces.CANDIDATE.read_text())
        first = Q(candidate["atoms"][0]["weight"])
        second = Q(candidate["atoms"][1]["weight"])
        epsilon = second / 2
        candidate["atoms"][0]["weight"] = str(first + epsilon)
        candidate["atoms"][1]["weight"] = str(second - epsilon)
        tampered_weights = [
            Q(atom["weight"]) for atom in candidate["atoms"]
        ]
        self.assertTrue(all(weight > 0 for weight in tampered_weights))
        self.assertEqual(sum(tampered_weights), 1)

        # The two atoms have different exact sufficient statistics, so this
        # sum-preserving transfer necessarily changes at least one marginal.
        first_edges = Counter(candidate["atoms"][0][direct.EDGE_KEY])
        second_edges = Counter(candidate["atoms"][1][direct.EDGE_KEY])
        first_triangles = Counter(
            candidate["atoms"][0]["triangle_orbit_indices"]
        )
        second_triangles = Counter(
            candidate["atoms"][1]["triangle_orbit_indices"]
        )
        self.assertTrue(
            first_edges != second_edges
            or first_triangles != second_triangles
        )

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "candidate_weight_tamper.json"
            write_json(path, candidate)
            tampered_sha = digest(path)
            # If the marginal checks did not reject the perturbation, this
            # sentinel would be reached at the later product-row stage.
            with mock.patch.object(via_faces, "CANDIDATE", path), (
                mock.patch.object(
                    via_faces, "CANDIDATE_SHA256", tampered_sha
                )
            ), mock.patch.object(
                via_faces.direction_source,
                "capacity_families",
                side_effect=RuntimeError(
                    "tampered weights passed both exact marginals"
                ),
            ):
                with self.assertRaises(AssertionError):
                    via_faces.verify()

    def test_rehashed_edge_and_pool_tamper_reaches_gram_check(self) -> None:
        """Synchronize pool authentication, then fail exact rank-five PSD."""

        candidate = json.loads(direct.CANDIDATE.read_text())
        active_index = candidate["active_pool_indices"][0]
        original_color = candidate["atoms"][0][direct.EDGE_KEY][0]
        self.assertEqual(original_color, 4)
        candidate["atoms"][0][direct.EDGE_KEY][0] = 0

        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            pool_path = temporary / "tampered_pool.csv"
            lines = direct.POOL.read_text().splitlines()
            fields = lines[active_index + 1].split(",")
            self.assertEqual(int(fields[0]), original_color)
            fields[0] = "0"
            lines[active_index + 1] = ",".join(fields)
            pool_path.write_text("\n".join(lines) + "\n")
            tampered_pool_sha = digest(pool_path)

            candidate["pool_sha256"] = tampered_pool_sha
            candidate_path = temporary / "candidate_edge_tamper.json"
            write_json(candidate_path, candidate)
            tampered_candidate_sha = digest(candidate_path)

            # Catalog authentication now succeeds because both files carry
            # the same modified edge.  A sentinel at triangle reconstruction
            # proves the preceding exact Gram test is what rejects the atom.
            with mock.patch.object(
                direct, "POOL_SHA256", tampered_pool_sha
            ), mock.patch.object(
                direct, "CANDIDATE_SHA256", tampered_candidate_sha
            ), mock.patch.object(
                direct,
                "triangle_indices",
                side_effect=RuntimeError(
                    "tampered edge unexpectedly passed rank-five Gram check"
                ),
            ):
                with self.assertRaises(AssertionError):
                    direct.verify(
                        pool_path=pool_path,
                        candidate_path=candidate_path,
                    )


if __name__ == "__main__":
    unittest.main()
