from __future__ import annotations

from collections import Counter
import unittest

import hard333_hw4_fractional_return as candidate


class Hard333HW4FractionalReturnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = candidate.certificate()

    def test_exact_selector(self) -> None:
        selector = self.result["selector"]
        self.assertEqual(
            (selector["pairs"], selector["positive"], selector["signed"]),
            (4, 4, 0),
        )
        self.assertEqual(selector["pair_sha256"], candidate.EXPECTED_PAIR_SHA256)
        self.assertEqual(
            selector["activation_resistance_histogram"], {"1": 2, "2": 2}
        )

    def test_service_zero_geometry(self) -> None:
        rows = candidate.geometry_rows()
        self.assertEqual(len(rows), 4)
        self.assertEqual(
            Counter(row["unique_service_zero_dormant_vertex"] for row in rows),
            {"A": 2, "B": 2},
        )
        self.assertEqual(
            Counter(row["activation_seed_resistance"] for row in rows),
            {1: 2, 2: 2},
        )
        self.assertTrue(all(row["top_rank"] == 2 for row in rows))
        self.assertTrue(all(row["top_preserves_total_population"] for row in rows))
        self.assertTrue(all(row["all_active_workload"] == [1, 1, 1] for row in rows))

    def test_claim_neutral_arithmetic(self) -> None:
        arithmetic = self.result["claim_neutral_arithmetic"]
        self.assertEqual(
            (
                arithmetic["candidate_H_w_4"]["pairs"],
                arithmetic["claim_neutral_after"]["pairs"],
            ),
            (4, 12),
        )
        self.assertEqual(
            arithmetic["claim_neutral_after"]["pair_sha256"],
            candidate.EXPECTED_AFTER_PAIR_SHA256,
        )
        self.assertTrue(arithmetic["claim_neutral_after"]["equals_exact_H_b_12"])

    def test_full_chain_and_endpoint_contracts_are_frozen(self) -> None:
        self.assertTrue(
            self.result["one_macroepisode_contract"]["all_reactions_retained"]
        )
        self.assertEqual(
            self.result["repeated_fractional_return_contract"][
                "required_endpoint_order"
            ],
            "choose integer m>8",
        )
        self.assertIn(
            "n_tau<=rho*n0",
            self.result["common_W_endpoint"]["contraction_envelope"],
        )

    def test_all_claim_flags_false(self) -> None:
        for key in (
            "independent_analytic_audit_passed",
            "single_macroepisode_service_certified",
            "fractional_return_iteration_certified",
            "common_W_endpoint_certified",
            "H_w_4_pair_recurrence_certified",
            "global_t3_2_certified",
        ):
            self.assertFalse(self.result[key])


if __name__ == "__main__":
    unittest.main()
