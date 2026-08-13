from __future__ import annotations

from collections import Counter
import unittest

import hard333_switch_16_scalar_obstruction as obstruction


class Hard333Switch16ScalarObstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = obstruction.certificate()

    def test_exact_switch_selector(self) -> None:
        selector = self.result["selector"]
        self.assertEqual(
            (selector["pairs"], selector["positive"], selector["signed"]),
            (16, 16, 0),
        )
        self.assertEqual(
            selector["pair_sha256"], obstruction.EXPECTED_SWITCH_PAIR_SHA256
        )
        self.assertEqual(
            selector["branch_histogram"],
            {"H_b_curvature_12": 12, "H_w_rank_two_4": 4},
        )
        self.assertEqual(
            selector["failure_incidence_histogram"],
            {"1": 50, "2": 56, "3": 64},
        )

    def test_hard_rows_and_all_active_rows_are_frozen(self) -> None:
        rows = obstruction.switch_rows()
        self.assertEqual(len(rows), 16)
        self.assertEqual(
            Counter(
                row["hard_dormant_row"]["resistance"] for row in rows
            ),
            {0: 4, 1: 10, 2: 2},
        )
        self.assertEqual(
            sum(len(row["all_active_incidences"]) for row in rows), 64
        )
        self.assertEqual(
            sum(
                item["curvature_excess"] > 0
                for row in rows
                for item in row["all_active_incidences"]
            ),
            16,
        )
        self.assertTrue(
            all(row["direct_branch_scalar_interval_is_empty"] for row in rows)
        )

    def test_H_b_exact_exponent_conflict(self) -> None:
        witness = self.result["H_b_exact_obstruction"]
        self.assertTrue(witness["top_is_exactly_H_B_neutral"])
        self.assertEqual(
            witness["all_active_curvature_center"]["necessary_power"],
            "q>21/5",
        )
        self.assertEqual(
            witness["hard_service_scale"]["necessary_power"], "q<=4"
        )
        self.assertEqual(
            witness["hard_service_scale"]["exact_HB_increment"], 1
        )
        self.assertTrue(witness["empty_power_interval"])

    def test_H_w_exact_exponent_conflict(self) -> None:
        witness = self.result["H_w_exact_obstruction"]
        self.assertTrue(witness["top_is_exactly_H_neutral"])
        self.assertEqual(
            witness["all_active_flat_sequence"]["necessary_power"], "q>5"
        )
        self.assertEqual(
            witness["hard_service_scale"]["necessary_power"], "q<=14/3"
        )
        self.assertEqual(
            witness["hard_service_scale"][
                "exact_total_increment_on_rare_birth_endpoint"
            ],
            1,
        )
        self.assertTrue(witness["empty_power_interval"])

    def test_claim_flags_remain_false(self) -> None:
        for key in (
            "independent_analytic_audit_passed",
            "regenerative_switch_transfer_certified",
            "switch_16_pair_recurrence_certified",
            "global_t3_2_certified",
        ):
            self.assertFalse(self.result[key])


if __name__ == "__main__":
    unittest.main()
