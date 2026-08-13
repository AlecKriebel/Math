from __future__ import annotations

from collections import Counter
import unittest

import hard333_hb12_killed_shell_transfer as candidate


class Hard333HB12KilledShellTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = candidate.certificate()

    def test_exact_selector_and_histograms(self) -> None:
        selector = self.result["selector"]
        self.assertEqual(
            (selector["pairs"], selector["positive"], selector["signed"]),
            (12, 12, 0),
        )
        self.assertEqual(selector["pair_sha256"], candidate.EXPECTED_PAIR_SHA256)
        self.assertEqual(selector["curvature_incidences"], 16)
        self.assertEqual(
            selector["curvature_excess_histogram"], {"1": 12, "2": 4}
        )
        self.assertEqual(
            selector["hard_resistance_histogram"], {"1": 10, "2": 2}
        )

    def test_exact_common_top_geometry(self) -> None:
        rows = candidate.geometry_rows()
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(row["top_support"] == ["2A", "BC"] for row in rows))
        self.assertTrue(all(row["top_rank"] == 1 for row in rows))
        self.assertTrue(all(row["top_reversible_two_node"] for row in rows))
        self.assertTrue(all(row["top_preserves_total_population"] for row in rows))
        self.assertTrue(
            all(row["top_preserves_neutral_workload"] for row in rows)
        )
        self.assertEqual(
            Counter(row["hard_dormant_resistance"] for row in rows),
            {1: 10, 2: 2},
        )

    def test_curvature_and_workload_split(self) -> None:
        rows = candidate.geometry_rows()
        self.assertEqual(
            Counter(
                incidence["curvature_excess"]
                for row in rows
                for incidence in row["curvature_incidences"]
            ),
            {1: 12, 2: 4},
        )
        self.assertEqual(
            {
                tuple(tuple(workload) for workload in row["neutral_workload_menu"])
                for row in rows
            },
            {((2, 1, 3),), ((2, 3, 1),)},
        )

    def test_invalid_shortcuts_are_explicitly_withdrawn(self) -> None:
        shortcuts = self.result["withdrawn_shortcuts"]
        self.assertFalse(shortcuts["global_mean_zero_poisson_gauge"]["valid"])
        self.assertFalse(shortcuts["raw_first_R_after_divergent_top_flux"]["valid"])
        self.assertFalse(
            shortcuts["single_hard_episode_repays_full_shell_mark"]["valid"]
        )
        self.assertTrue(
            self.result["candidate_local_episode"]["all_reactions_retained"]
        )

    def test_exact_lower_dimensional_routing(self) -> None:
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
            {"generalized_family_ii": 36, "direct_physical_C": 2},
        )
        self.assertTrue(routing["central_guard_reached_before_dimension_loss"])
        self.assertFalse(routing["single_dormant_handoff_is_exhaustive"])

    def test_all_claim_flags_false(self) -> None:
        for key in (
            "uniform_birth_death_moment_lemma_certified",
            "uniform_killed_lower_reward_certified",
            "guard_exit_charge_certified",
            "pointwise_core_complement_certified",
            "common_W_endpoint_certified",
            "H_b_12_pair_recurrence_certified",
            "global_t3_2_certified",
        ):
            self.assertFalse(self.result[key])


if __name__ == "__main__":
    unittest.main()
