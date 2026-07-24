#!/usr/bin/env python3
"""Regression tests for the exact structured shell-two family audits."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import verify_f27_submodule_families as f27  # noqa: E402
import verify_structured_phase_families as feature  # noqa: E402


class StructuredFeatureFamilyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.certificate = feature.build_certificate()

    def test_semantic_hash(self) -> None:
        self.assertEqual(
            feature.compact_hash(self.certificate),
            feature.EXPECTED_SEMANTIC_SHA256,
        )

    def test_exact_family_totals(self) -> None:
        expected = {
            "quadratic_c3": (2187, 0, 0),
            "crt4_additive": (27, 0, 0),
            "antipodal_additive": (59049, 0, 0),
            "cocyclic_multiaffine": (177147, 0, 0),
            "opposite_planar_c3_envelope": (5103, 2916, 0),
            "opposite_twisted_c6": (177147, 174960, 0),
            "opposite_helical_c4": (178605, 1458, 1),
        }
        actual = {
            record["name"]: (
                record["total_first_digit_distinct_placements"],
                record["total_proper_supergroup_free_placements"],
                record["total_second_digit_survivors"],
            )
            for record in self.certificate["families"]
        }
        self.assertEqual(actual, expected)

    def test_unique_digit_two_control_is_h8_fixed(self) -> None:
        record = next(
            family
            for family in self.certificate["families"]
            if family["name"] == "opposite_helical_c4"
        )
        hit_audits = [
            audit
            for audit in record["audits"]
            if audit["second_digit_survivors"]
        ]
        self.assertEqual(len(hit_audits), 1)
        audit = hit_audits[0]
        self.assertEqual(audit["profile"], "h2-422220-0")
        self.assertEqual(
            audit["minimal_supergroup_fixed_counts"]["8"],
            audit["first_digit_distinct_placements"],
        )
        self.assertEqual(audit["proper_supergroup_free_placements"], 0)
        self.assertEqual(audit["exact_phase_survivors"], 0)
        witness = audit["second_digit_witness_records"][0]
        self.assertEqual(
            witness["trit_sha256"],
            "854a5af491580697ce9f91f3dbe93b06f5ec79a3dbe918a055aac9fb75377325",
        )
        self.assertEqual(
            witness["lambda_digit_3"],
            (0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 1, 0, 0, 2, 0),
        )


class F27MinimalSubmoduleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.certificate = f27.build_certificate()

    def test_semantic_hash(self) -> None:
        self.assertEqual(
            feature.compact_hash(self.certificate),
            f27.EXPECTED_SEMANTIC_SHA256,
        )

    def test_submodule_and_survivor_census(self) -> None:
        self.assertEqual(self.certificate["minimal_submodules_total"], 56)
        self.assertEqual(
            self.certificate["total_distinct_first_digit_placements"], 436
        )
        self.assertEqual(
            self.certificate["total_proper_supergroup_free_placements"], 6
        )
        self.assertEqual(
            self.certificate["total_second_digit_survivors"], 0
        )
        self.assertEqual(
            tuple(
                (
                    audit["compatible_submodule_pairs"],
                    audit["distinct_first_digit_placements"],
                    audit["proper_supergroup_free_placements"],
                )
                for audit in self.certificate["audits"]
            ),
            (
                (0, 0, 0),
                (4, 108, 0),
                (58, 221, 6),
                (58, 107, 0),
                (0, 0, 0),
            ),
        )


class CompactSummaryTests(unittest.TestCase):
    def test_pinned_summary_hashes(self) -> None:
        summary = json.loads(
            (HERE / "certificate_summary.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            summary["feature_family_semantic_sha256"],
            feature.EXPECTED_SEMANTIC_SHA256,
        )
        self.assertEqual(
            summary["f27_submodule_semantic_sha256"],
            f27.EXPECTED_SEMANTIC_SHA256,
        )
        self.assertFalse(
            summary["unique_digit_two_control"][
                "exact_phase_equations_zero"
            ]
        )


if __name__ == "__main__":
    unittest.main()
