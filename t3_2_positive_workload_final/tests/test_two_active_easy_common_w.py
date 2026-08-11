from __future__ import annotations

from collections import Counter
import unittest

import two_active_easy_common_w as common_w


class EasyPromotionCommonWTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = common_w.certificate()

    def test_exact_promotion_partition(self) -> None:
        partition = self.result["promotion_partition"]
        self.assertEqual(partition["incidences"], 1350)
        self.assertEqual(partition["pairs"], 749)
        self.assertEqual(
            partition["family_histogram"],
            {
                "dormant_finite_rank_one": 6,
                "dormant_no_whole": 407,
                "dormant_poisson_access_word": 8,
                "seeded_access_word": 929,
            },
        )
        self.assertEqual(
            partition["whole_top_phase_histogram"],
            {
                "finite_rank_one_whole_top": 10,
                "no_whole_top": 1332,
                "rank_two_poisson_whole_top": 8,
            },
        )
        self.assertEqual(
            partition["seed_status_by_whole_top_phase"],
            {
                "enabled": {
                    "finite_rank_one_whole_top": 4,
                    "no_whole_top": 925,
                },
                "dormant": {
                    "finite_rank_one_whole_top": 6,
                    "no_whole_top": 407,
                    "rank_two_poisson_whole_top": 8,
                },
            },
        )
        self.assertEqual(partition["easy_943"]["incidences"], 943)
        self.assertEqual(partition["easy_943"]["pairs"], 555)
        self.assertEqual(partition["hard_407"]["incidences"], 407)
        self.assertEqual(partition["hard_407"]["pairs"], 333)
        self.assertEqual(
            partition["hard_407"]["active_weight_profile_histogram"],
            {"1,2": 37, "1,3": 333, "4,5": 37},
        )
        self.assertTrue(
            partition["hard_407"][
                "proper_top_is_single_inactive_plus_active_complex"
            ]
        )

    def test_maximal_fully_easy_pair_selector(self) -> None:
        selector = self.result["fully_easy_pair_selector"]
        self.assertEqual(
            (selector["pairs"], selector["positive"], selector["signed"]),
            (416, 414, 2),
        )
        self.assertEqual(
            selector["pair_sha256"], common_w.EXPECTED_FULLY_EASY_PAIR_SHA256
        )
        self.assertEqual(selector["promotion_incidences"], 762)
        self.assertEqual(
            selector["promotion_family_histogram"],
            {
                "dormant_finite_rank_one": 6,
                "dormant_poisson_access_word": 8,
                "seeded_access_word": 748,
            },
        )
        self.assertEqual(
            selector["failure_active_count_profiles"],
            {"1,2": 377, "1,2,3": 39},
        )

    def test_one_active_structural_partition(self) -> None:
        extension = self.result["one_active_structural_extension"]
        self.assertEqual(extension["incidences"], 1455)
        self.assertEqual(extension["profiles"], 736)
        self.assertEqual(
            extension["family_histogram"],
            {
                "direct_physical_C": 1356,
                "family_i": 65,
                "exact_family_ii": 0,
                "family_iii": 10,
                "open_whole": 24,
                "generalized_family_ii": 0,
            },
        )
        self.assertEqual(
            extension["graph_category_histogram"],
            {
                "family_i_origin_down_0": 65,
                "family_iii_origin_down_0": 6,
                "family_iii_origin_down_1": 4,
                "mixed_C_source_direct_down_0": 1356,
                "open_wholly_top_down_1": 24,
            },
        )
        self.assertEqual(
            extension["exact_normalized_signature_overlap_with_prior_1227"],
            {
                "incidences": 0,
                "pairs": 0,
                "pair_sha256": (
                    "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
                ),
            },
        )

    def test_no_generalized_family_ii_pair_obstruction(self) -> None:
        extension = self.result["one_active_structural_extension"]
        self.assertEqual(
            extension["pairs_with_every_row_outside_generalized_family_ii"],
            416,
        )
        self.assertTrue(
            extension[
                "every_direct_row_has_physical_C_source_in_mixed_phase"
            ]
        )
        self.assertEqual(
            extension["outside_generalized_family_ii_pair_sha256"],
            common_w.EXPECTED_FULLY_EASY_PAIR_SHA256,
        )
        empty = extension["family_pair_unions"]["generalized_family_ii"]
        self.assertEqual(empty["pairs"], 0)
        self.assertEqual(
            empty["pair_sha256"],
            "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        )

    def test_closed_rank_one_and_all_active_interfaces(self) -> None:
        interfaces = self.result["other_interfaces"]
        self.assertEqual(
            interfaces["closed_rank_one_two_active"],
            {
                "incidences": 117,
                "pairs": 39,
                "activation_histogram": {
                    "lower_layer_activation_needed": 2,
                    "lower_top_seeded": 115,
                },
            },
        )
        self.assertEqual(
            interfaces["all_active"],
            {
                "incidences": 117,
                "pairs": 39,
                "safe_reversible_two_node_pairs": 23,
                "directed_triple_pairs": 16,
                "shape_incidence_histogram": {"2,1,0": 69, "3,1,1": 48},
            },
        )
        self.assertEqual(
            Counter(row["activation_category"] for row in common_w.closed_rank_one_rows()),
            {"lower_top_seeded": 115, "lower_layer_activation_needed": 2},
        )
        self.assertEqual(
            interfaces["dormant_whole_promotion"],
            {
                "pairs": 14,
                "closed_rank_one_pair_overlap": 0,
                "all_active_pair_overlap": 0,
            },
        )
        self.assertTrue(
            interfaces["closed_rank_one_all_active_top_masks_identical"]
        )

    def test_common_potential_menu_is_disjoint_and_exhaustive(self) -> None:
        menu = self.result["common_potential_menu"]
        self.assertEqual(
            {name: row["pairs"] for name, row in menu.items()},
            {
                "arbitrary_fixed_ell": 371,
                "reversible_rate_adjusted_ell": 29,
                "directed_triple_rate_adjusted_ell": 16,
            },
        )
        self.assertEqual(
            menu["arbitrary_fixed_ell"]["pair_sha256"],
            "77b42a7079d38c1b83b322b1e46fa4ea61dc4a7203a33760dd856b0a883ebca4",
        )
        self.assertEqual(
            menu["reversible_rate_adjusted_ell"]["pair_sha256"],
            "d5026791e3166315e347a6d4b938f1d9f8315a898f785d1ace92026286437392",
        )
        self.assertEqual(
            menu["directed_triple_rate_adjusted_ell"]["pair_sha256"],
            "3d1a90f712f00ed4d343a97dcfc10b218a779a26640789dec232799d727f2712",
        )

    def test_certified_pair_arithmetic(self) -> None:
        self.assertEqual(
            self.result["certified_pair_arithmetic"],
            {
                "before": {"positive": 733, "signed": 36, "total": 769},
                "new_exact_416": {
                    "positive": 414,
                    "signed": 2,
                    "total": 416,
                    "pair_sha256": common_w.EXPECTED_FULLY_EASY_PAIR_SHA256,
                },
                "after": {
                    "positive": 319,
                    "signed": 34,
                    "total": 353,
                    "pair_sha256": common_w.EXPECTED_POST_416_PAIR_SHA256,
                },
            },
        )

    def test_arbitrary_ell_counterexample_is_frozen(self) -> None:
        row = self.result["arbitrary_ell_counterexample"]
        self.assertEqual(
            row["pair"], [["A", "B"], ["0", "C", "AC", "BC"]]
        )
        self.assertEqual(row["whole_rates"], {"A->B": 2, "B->A": 1})
        self.assertEqual(row["exact_expected_B_at_T"], "5N/4")
        self.assertEqual(
            row["required_detailed_balance_constraint"],
            "ell_B-ell_A=-log(2)",
        )
        self.assertFalse(row["arbitrary_ell_valid_for_finite_shell"])

    def test_frozen_hashes(self) -> None:
        self.assertEqual(
            self.result["hashes"],
            {
                "promotion_rows_sha256": common_w.EXPECTED_PROMOTION_ROWS_SHA256,
                "easy_rows_sha256": common_w.EXPECTED_EASY_ROWS_SHA256,
                "hard_rows_sha256": common_w.EXPECTED_HARD_ROWS_SHA256,
                "fully_easy_promotion_rows_sha256": (
                    common_w.EXPECTED_FULLY_EASY_PROMOTION_ROWS_SHA256
                ),
                "one_active_rows_sha256": common_w.EXPECTED_ONE_ACTIVE_ROWS_SHA256,
                "one_active_classified_sha256": (
                    common_w.EXPECTED_ONE_ACTIVE_CLASSIFIED_SHA256
                ),
                "one_active_profiles_sha256": (
                    common_w.EXPECTED_ONE_ACTIVE_PROFILES_SHA256
                ),
                "closed_rank_one_rows_sha256": (
                    common_w.EXPECTED_CLOSED_RANK_ONE_ROWS_SHA256
                ),
                "all_active_rows_sha256": common_w.EXPECTED_ALL_ACTIVE_ROWS_SHA256,
            },
        )
        self.assertEqual(
            self.result["payload_sha256"], common_w.EXPECTED_PAYLOAD_SHA256
        )

    def test_scoped_claim_flags_and_global_boundary(self) -> None:
        self.assertTrue(self.result["exact_arithmetic_replayed"])
        self.assertTrue(self.result["independent_audit_passed"])
        for name in (
            "analytic_easy_943_common_w_certified",
            "analytic_one_active_structural_extension_certified",
            "analytic_closed_rank_one_power_lift_certified",
            "analytic_directed_triple_power_lift_certified",
            "exact_416_pair_recurrence_certified",
        ):
            self.assertTrue(self.result[name], name)
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
