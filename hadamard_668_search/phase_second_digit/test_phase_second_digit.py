#!/usr/bin/env python3
"""Focused regressions for the second placement digit and six-form pencil."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
SEARCH_ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(SEARCH_ROOT))

import verify_phase_second_digit as second  # noqa: E402
import verify_phase_second_digit_pencil as pencil  # noqa: E402


STRUCTURED_THEOREM_SEMANTIC_SHA256 = (
    "aa6dbb0c3272e8695e3c8beff8381702a9f7f5a2505716138086d8074aa20d5c"
)


class PhaseSecondDigitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.second_certificate = second.build_certificate()
        cls.pencil_certificate = pencil.build_certificate()

    def test_second_digit_semantic_certificate(self) -> None:
        self.assertEqual(
            second.compact_hash(self.second_certificate),
            second.EXPECTED_SEMANTIC_SHA256,
        )
        self.assertEqual(self.second_certificate["profiles"], 5)
        for audit in self.second_certificate["audits"]:
            first = audit["first_digit"]
            layer = audit["second_digit"]
            self.assertEqual(
                (first["variables"], first["rank"], first["affine_dimension"]),
                (54, 18, 36),
            )
            self.assertEqual(layer["equations"], 20)
            self.assertEqual(layer["polar_span_rank"], 18)
            self.assertEqual(layer["zero_polar_combination_dimension"], 2)
            self.assertEqual(layer["zero_polar_affine_rank"], 0)
            self.assertEqual(layer["common_radical_nullity"], 0)
            self.assertEqual(layer["polynomial_coefficient_rank"], 18)
            self.assertEqual(layer["polynomial_augmented_rank"], 18)

    def test_only_two_structural_zero_rows(self) -> None:
        for audit in self.second_certificate["audits"]:
            records = audit["second_digit"]["zero_polar_combinations"]
            supports = tuple(
                tuple(
                    index
                    for index, coefficient in enumerate(
                        record["equation_coefficients"]
                    )
                    if coefficient
                )
                for record in records
            )
            self.assertEqual(supports, ((0,), (7,)))
            self.assertTrue(
                all(
                    record["constant"] == 0
                    and not any(record["linear"])
                    for record in records
                )
            )

    def test_pencil_semantic_certificate(self) -> None:
        self.assertEqual(
            pencil.compact_hash(self.pencil_certificate),
            pencil.EXPECTED_SEMANTIC_SHA256,
        )
        expected_ranks = (
            (19, 19, 16, 19, 19, 16),
            (19, 19, 19, 15, 17, 20),
            (17, 18, 19, 19, 19, 17),
            (17, 15, 19, 18, 21, 19),
            (17, 16, 19, 21, 16, 19),
        )
        expected_zero_fibers = (
            205_891_130_500_326,
            205_891_148_037_879,
            205_891_197_461_892,
            205_891_052_378_499,
            205_891_125_717_357,
        )
        expected_corrections = (-1, 10, 41, -50, -4)
        for index, audit in enumerate(self.pencil_certificate["audits"]):
            self.assertEqual(
                tuple(
                    form["polar_rank"]
                    for form in audit["structured_forms"]
                ),
                expected_ranks[index],
            )
            self.assertTrue(
                all(
                    form["collapsed_phase_autocorrelation_factorization"]
                    and form["linear_nonzero_on_polar_radical"]
                    for form in audit["structured_forms"]
                )
            )
            sparse = audit["sparse_projective_audit"]
            self.assertEqual(sparse["projective_combinations_tested"], 3_588)
            self.assertEqual(sparse["rank_below_28_count"], 6)
            self.assertTrue(
                sparse["rank_below_28_exactly_structured_family"]
            )
            gauss = audit["gauss_fiber_audit"]
            self.assertEqual(
                gauss["joint_zero_fiber_count"],
                expected_zero_fibers[index],
            )
            self.assertEqual(
                gauss["joint_zero_fiber_correction"],
                expected_corrections[index],
            )
            self.assertTrue(gauss["all_target_fibers_nonempty"])
            self.assertEqual(gauss["fiber_count_sum"], 3 ** 36)

    def test_exact_gauss_primitives(self) -> None:
        pencil.verify_gauss_primitives()

    def test_compact_stored_certificate(self) -> None:
        stored = json.loads(
            (HERE / "phase_second_digit_certificate.json").read_text()
        )
        self.assertEqual(
            stored["second_digit_semantic_sha256"],
            second.EXPECTED_SEMANTIC_SHA256,
        )
        self.assertEqual(
            stored["pencil_semantic_sha256"],
            pencil.EXPECTED_SEMANTIC_SHA256,
        )
        self.assertEqual(
            stored["structured_theorem_semantic_sha256"],
            STRUCTURED_THEOREM_SEMANTIC_SHA256,
        )
        for compact, full_second, full_pencil in zip(
            stored["profiles"],
            self.second_certificate["audits"],
            self.pencil_certificate["audits"],
        ):
            self.assertEqual(compact["label"], full_second["label"])
            self.assertEqual(
                compact["individual_polar_rank_histogram"],
                full_second["second_digit"]["polar_rank_histogram"],
            )
            self.assertEqual(
                compact["structured_polar_ranks"],
                [
                    form["polar_rank"]
                    for form in full_pencil["structured_forms"]
                ],
            )
            self.assertEqual(
                compact["structured_common_radical_nullity"],
                full_pencil["structured_common_radical_nullity"],
            )
            gauss = full_pencil["gauss_fiber_audit"]
            for key in (
                "joint_zero_fiber_count",
                "joint_zero_fiber_correction",
                "minimum_fiber_correction",
                "maximum_fiber_correction",
                "distinct_fiber_counts",
            ):
                self.assertEqual(compact[key], gauss[key])


if __name__ == "__main__":
    unittest.main()
