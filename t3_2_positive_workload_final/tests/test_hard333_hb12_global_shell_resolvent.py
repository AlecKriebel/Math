from __future__ import annotations

from collections import Counter
import unittest

import hard333_hb12_global_shell_resolvent as candidate


class Hard333HB12GlobalShellResolventTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = candidate.certificate()

    def test_exact_selector_and_gap_histogram(self) -> None:
        selector = self.result["selector"]
        self.assertEqual(
            (selector["pairs"], selector["positive"], selector["signed"]),
            (12, 12, 0),
        )
        self.assertEqual(selector["pair_sha256"], candidate.EXPECTED_PAIR_SHA256)
        self.assertEqual(selector["curvature_incidences"], 16)
        self.assertEqual(
            selector["relaxation_over_killing_excess_histogram"],
            {"1": 12, "2": 4},
        )

    def test_every_row_has_exact_gap_excess(self) -> None:
        rows = candidate.resolvent_rows()
        self.assertEqual(len(rows), 16)
        for row in rows:
            self.assertEqual(
                row["top_relaxation_gap_exponent"]
                - row["lower_hazard_exponent"],
                row["relaxation_over_killing_excess"],
            )
            self.assertTrue(row["top_balance_identity"])
            self.assertTrue(row["lower_hazard_is_finite_factorial_tilt_sum"])

    def test_exact_dominant_lower_source_partition(self) -> None:
        histogram = Counter(
            tuple(row["dominant_lower_sources"])
            for row in candidate.resolvent_rows()
        )
        self.assertEqual(
            histogram,
            {
                ("AB",): 5,
                ("AC",): 5,
                ("A",): 2,
                ("A", "2B"): 1,
                ("A", "2C"): 1,
                ("2B",): 1,
                ("2C",): 1,
            },
        )

    def test_false_guard_is_withdrawn(self) -> None:
        witness = self.result["withdrawn_guard"]
        self.assertTrue(witness["old_log_largest_guard_reaches_B_zero"])
        self.assertFalse(witness["old_q_ratio_uniform_on_guard"])
        self.assertFalse(witness["pathwise_boundary_avoidance_required_by_repair"])
        self.assertEqual(
            self.result["candidate_same_state_regeneration"]["stopping_rule"],
            "the first lower-linkage reaction; no guard",
        )

    def test_exact_lower_dimensional_menu(self) -> None:
        routing = self.result["lower_dimensional_routing"]
        self.assertEqual(
            routing["failure_incidence_histogram"], {"1": 38, "2": 48, "3": 60}
        )
        self.assertEqual(
            routing["two_active_48"],
            {
                "closed_rank_one_top_phase": 36,
                "promotion_dormant_top": 12,
            },
        )
        self.assertEqual(
            routing["one_active_38"],
            {"direct_physical_C": 2, "generalized_family_ii": 36},
        )

    def test_all_claim_flags_false(self) -> None:
        for key in (
            "stationary_size_bias_moment_lemma_certified",
            "same_state_kac_moment_lemma_certified",
            "guard_free_killed_resolvent_certified",
            "terminal_lower_jump_moments_certified",
            "duration_moments_certified",
            "uniform_terminal_reward_certified",
            "pointwise_core_complement_certified",
            "common_W_endpoint_certified",
            "H_b_12_pair_recurrence_certified",
            "global_t3_2_certified",
        ):
            self.assertFalse(self.result[key])


if __name__ == "__main__":
    unittest.main()
