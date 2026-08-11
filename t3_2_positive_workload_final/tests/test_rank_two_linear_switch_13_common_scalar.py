from __future__ import annotations

from collections import Counter
import unittest

import rank_two_linear_switch_13_common_scalar as scalar


class RankTwoLinearSwitch13CommonScalarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = scalar.certificate()

    def test_exact_selector(self) -> None:
        self.assertEqual(
            self.result["selector"],
            {"pairs": 13, "pair_sha256": scalar.EXPECTED_PAIR_SHA256},
        )

    def test_power_split(self) -> None:
        self.assertEqual(
            Counter(row["scalar_power"] for row in scalar.scalar_rows()),
            {6: 11, 5: 2},
        )

    def test_all_active_strict_power_gap(self) -> None:
        self.assertEqual(
            Counter(
                row["all_active_exponents"]["strict_power_gap"]
                for row in scalar.scalar_rows()
            ),
            {"1": 11, "1/2": 2},
        )
        self.assertTrue(
            all(
                row["all_active_exponents"][
                    "lower_birth_is_strictly_lower_order"
                ]
                for row in scalar.scalar_rows()
            )
        )

    def test_C_bounded_coercive_sources(self) -> None:
        for row in scalar.scalar_rows():
            boundary = row["C_bounded_passing_exponents"]
            self.assertEqual(
                boundary["positive_LHq_power"],
                boundary["negative_LW_power_before_log_gap"],
            )
            self.assertIn("g(H)->infinity", boundary["strict_margin"])

    def test_certified_pair_arithmetic(self) -> None:
        self.assertEqual(
            self.result["certified_pair_arithmetic"],
            {
                "before": {
                    "positive": 319,
                    "signed": 34,
                    "total": 353,
                    "pair_sha256": scalar.EXPECTED_POST_416_PAIR_SHA256,
                },
                "new_exact_13": {
                    "positive": 13,
                    "signed": 0,
                    "total": 13,
                    "pair_sha256": scalar.EXPECTED_PAIR_SHA256,
                },
                "after": {
                    "positive": 306,
                    "signed": 34,
                    "total": 340,
                    "pair_sha256": scalar.EXPECTED_POST_13_PAIR_SHA256,
                },
            },
        )

    def test_scoped_claim_flags_true_global_false(self) -> None:
        self.assertTrue(self.result["independent_audit_passed"])
        self.assertTrue(
            self.result["analytic_common_scalar_independently_certified"]
        )
        self.assertTrue(self.result["exact_13_pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
