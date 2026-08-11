from __future__ import annotations

import unittest

import rank_two_linear_switch_13 as branch


class RankTwoLinearSwitch13Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = branch.certificate()

    def test_exact_twenty_split(self) -> None:
        self.assertEqual(len(branch.linear_switch_twenty()), 20)
        self.assertEqual(len(branch.selected_pairs()), 13)
        self.assertEqual(len(branch.mixed_profile_seven()), 7)
        self.assertFalse(branch.selected_pairs() & branch.mixed_profile_seven())
        self.assertEqual(
            branch.selected_pairs() | branch.mixed_profile_seven(),
            branch.linear_switch_twenty(),
        )

    def test_exact_selector_hashes(self) -> None:
        self.assertEqual(
            self.result["all_active_only_13"]["pair_sha256"],
            branch.EXPECTED_PAIR_SHA256,
        )
        self.assertEqual(
            self.result["mixed_profile_7"]["pair_sha256"],
            branch.EXPECTED_MIXED_SEVEN_SHA256,
        )

    def test_rank_two_workload_premises(self) -> None:
        scope = self.result["all_active_only_13"]
        self.assertEqual(scope["failed_incidences"], 13)
        self.assertEqual(scope["failed_active_profile"], [3])
        self.assertEqual(scope["top_size_histogram"], {"4": 8, "5": 4, "6": 1})
        self.assertEqual(
            scope["workload_histogram"],
            {"1,1,1": 11, "1,2,1": 1, "2,1,1": 1},
        )
        self.assertTrue(scope["all_lower_supports_are_0_C"])
        self.assertTrue(scope["all_top_reactions_preserve_H_w"])

    def test_exact_passing_boundary_obstruction(self) -> None:
        obstruction = self.result["passing_boundary_obstruction"]
        self.assertEqual(obstruction["common_descriptor_weight"], [0, 1, 0])
        self.assertEqual(obstruction["common_descriptor_caps"], [0, 2, 0])
        self.assertTrue(obstruction["all_13_affine_feasible"])
        self.assertTrue(
            obstruction["all_13_universal_tier_condition_passes"]
        )
        self.assertEqual(obstruction["C_population"], 0)
        self.assertEqual(obstruction["exact_H_generator"], "w_C*kappa_0C > 0")

    def test_post_26_disjoint_arithmetic(self) -> None:
        arithmetic = self.result["pair_arithmetic"]
        self.assertEqual(
            arithmetic["selected_13"]["post_26_certified_overlap"], 0
        )
        self.assertEqual(
            (
                arithmetic["claim_neutral_remainder_after_13"]["positive"],
                arithmetic["claim_neutral_remainder_after_13"]["signed"],
                arithmetic["claim_neutral_remainder_after_13"]["total"],
            ),
            (720, 36, 756),
        )

    def test_claim_flags_remain_false(self) -> None:
        self.assertFalse(self.result["common_potential_switch_closed"])
        self.assertFalse(self.result["candidate_13_pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
