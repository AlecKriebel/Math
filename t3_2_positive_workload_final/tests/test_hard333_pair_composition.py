from __future__ import annotations

import unittest

import hard333_pair_composition as composition


class Hard333PairCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = composition.certificate()

    def test_exact_317_16_partition(self) -> None:
        parent = self.result["parent_hard_333"]
        common = self.result["candidate_common_w_317"]
        switch = self.result["remaining_switch_16"]
        self.assertEqual((parent["pairs"], parent["positive"], parent["signed"]), (333, 299, 34))
        self.assertEqual((common["pairs"], common["positive"], common["signed"]), (317, 283, 34))
        self.assertEqual((switch["pairs"], switch["positive"], switch["signed"]), (16, 16, 0))

    def test_exact_failure_and_potential_histograms(self) -> None:
        common = self.result["candidate_common_w_317"]
        self.assertEqual(common["failure_incidence_histogram"], {"1": 1054, "2": 646, "3": 90})
        self.assertEqual(
            common["two_active_incidence_histogram"],
            {
                "closed_rank_one_top_phase": 78,
                "promotion_dormant_top": 391,
                "promotion_enabled_top_seed": 177,
            },
        )
        self.assertEqual(
            common["all_active_incidence_histogram"],
            {"directed_triple": 24, "safe_reversible_two_node": 66},
        )
        self.assertEqual(
            common["correction_family_histogram"],
            {
                "arbitrary_fixed_ell": 287,
                "directed_triple_adjusted_ell": 8,
                "reversible_top_adjusted_ell": 22,
            },
        )
        self.assertTrue(common["all_closed_and_all_active_top_masks_match"])

    def test_switch_fingerprints(self) -> None:
        switch = self.result["remaining_switch_16"]
        self.assertEqual(switch["pair_sha256"], composition.EXPECTED_SWITCH_16_SHA256)
        self.assertEqual(switch["H_b_pair_sha256"], composition.EXPECTED_HB_12_SHA256)
        self.assertEqual(switch["H_w_pair_sha256"], composition.EXPECTED_HW_4_SHA256)

    def test_claim_neutral_after_317(self) -> None:
        after = self.result["claim_neutral_after_common_317"]
        self.assertEqual((after["pairs"], after["positive"], after["signed"]), (16, 16, 0))
        self.assertEqual(after["pair_sha256"], composition.EXPECTED_AFTER_317_SHA256)

    def test_all_claim_flags_false(self) -> None:
        self.assertFalse(self.result["local_repaired_hard_kernel_independently_audited"])
        self.assertFalse(self.result["common_w_317_pair_recurrence_certified"])
        self.assertFalse(self.result["switch_16_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
