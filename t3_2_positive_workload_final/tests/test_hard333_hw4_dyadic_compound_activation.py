from __future__ import annotations

from collections import Counter
import unittest

import hard333_hw4_dyadic_compound_activation as candidate


class Hard333HW4DyadicCompoundActivationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = candidate.certificate()

    def test_exact_selector_and_height_geometry(self) -> None:
        selector = self.result["selector"]
        self.assertEqual(
            (selector["pairs"], selector["positive"], selector["signed"]),
            (4, 4, 0),
        )
        self.assertEqual(selector["pair_sha256"], candidate.EXPECTED_PAIR_SHA256)
        self.assertEqual(
            selector["activation_resistance_histogram"], {"1": 2, "2": 2}
        )
        rows = candidate.geometry_rows()
        self.assertEqual(len(rows), 4)
        self.assertEqual(
            Counter(row["weighted_transverse_coordinate"] for row in rows),
            {"R=2Y+C": 2, "R=Y+2C": 2},
        )
        self.assertTrue(
            all(sorted(row["complex_heights"].values()) == [2, 2, 3, 4]
                for row in rows)
        )
        self.assertTrue(
            all(row["comparison_with_total_transverse_mass"] == "M<=R<=2M"
                for row in rows)
        )
        for row in rows:
            if row["activation_seed_resistance"] == 2:
                self.assertEqual(row["minimum_height_complexes"],
                                 ["2C", "XY"])
                self.assertEqual(row["strictly_higher_complexes"],
                                 ["YC", "2Y"])
                self.assertEqual(row["complex_heights"],
                                 {"2Y": 4, "2C": 2, "YC": 3, "XY": 2})
            else:
                self.assertEqual(row["minimum_height_complexes"],
                                 ["2Y", "XC"])
                self.assertEqual(row["strictly_higher_complexes"],
                                 ["YC", "2C"])
                self.assertEqual(row["complex_heights"],
                                 {"2Y": 2, "2C": 4, "YC": 3, "XC": 2})

    def test_all_strong_digraphs_have_bounded_minimum_cut(self) -> None:
        cut = self.result["finite_minimum_cut"]
        self.assertEqual(cut["strong_simple_digraphs"], 1606)
        self.assertEqual(
            cut["distance_profile"],
            {
                "both_minimum_nodes_cut_directly": 1234,
                "one_minimum_node_needs_one_zero_height_transfer": 372,
            },
        )
        self.assertEqual(cut["maximum_minimum_class_cut_length"], 2)
        self.assertEqual(
            cut["direct_source_profile"],
            {
                "both_direct": 1234,
                "single_direct_A": 186,
                "single_direct_B": 186,
            },
        )
        self.assertEqual(
            sum(row["count"] for row in cut["direct_zero_edge_profile"]),
            1606,
        )
        for row in cut["direct_zero_edge_profile"]:
            self.assertTrue(row["direct_A"] or row["A_to_B_zero"])
            self.assertTrue(row["direct_B"] or row["B_to_A_zero"])
        self.assertEqual(
            cut["profile_sha256"], candidate.EXPECTED_CUT_PROFILE_SHA256
        )

    def test_sparse_mass_dip_is_exactly_neutralized(self) -> None:
        regression = self.result["mass_dip_regression"]
        self.assertFalse(regression["old_one_level_mass_comparison_valid"])
        self.assertEqual(regression["problem_edge"], "2C->XY")
        self.assertEqual(regression["exact_weighted_increment_on_problem_edge"], 0)
        self.assertGreater(regression["minimum_cut_weighted_reward"], 0)

    def test_dyadic_contract_retains_all_reactions(self) -> None:
        ascent = self.result["candidate_compound_quadratic_ascent"]
        self.assertTrue(ascent["all_reactions_retained"])
        self.assertEqual(ascent["minimum_propensity_bound"], "Lambda_min>=c*R^2")
        self.assertIn("epsilon+1/R", ascent["clock_comparison"])
        self.assertEqual(len(ascent["source_balance"]), 3)
        self.assertIn("need not", ascent["withdrawn_pointwise_cut_claim"])
        self.assertIn("exp(-c*r)", ascent["dyadic_block"])
        self.assertIn("actual endpoint", ascent["full_attempt_restart"])
        endpoint = self.result["candidate_service_and_return"]
        self.assertEqual(endpoint["duration_and_endpoint_order"],
                         "one uniform integer p>8")
        self.assertEqual(endpoint["fractional_stop"],
                         "n<=rho*n0 or n>=2*n0")

    def test_all_claim_flags_false(self) -> None:
        for key in (
            "weighted_minimum_class_contraction_certified",
            "event_skeleton_source_balance_certified",
            "dyadic_quadratic_ascent_certified",
            "deterministic_service_integral_certified",
            "single_macroepisode_service_certified",
            "fractional_return_iteration_certified",
            "common_W_endpoint_certified",
            "H_w_4_pair_recurrence_certified",
            "global_t3_2_certified",
        ):
            self.assertFalse(self.result[key])


if __name__ == "__main__":
    unittest.main()
