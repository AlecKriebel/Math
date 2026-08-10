import unittest

import three_active_gluing_gate as gate


class ThreeActiveGluingGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = gate.certificate()

    def test_fixed_top_is_pairwise_global(self):
        self.assertTrue(
            self.result["all_active_local_analytic_theorem_certified"]
        )
        self.assertFalse(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])
        self.assertEqual(self.result["all_active_failed_pairs"], 403)
        self.assertEqual(
            self.result["pairs_with_one_fixed_top_side_and_support"],
            403,
        )
        self.assertEqual(self.result["full_rank_three_pairs"], 403)
        self.assertEqual(self.result["distinct_fixed_top_supports"], 35)
        self.assertEqual(
            self.result["certificate_sha256"],
            gate.EXPECTED_CERTIFICATE_SHA256,
        )

    def test_rate_adjusted_entropy_branch(self):
        branch = self.result["direct_entropy_branch"]
        self.assertEqual(branch["two_node_rank_one_failed_incidences"], 966)
        self.assertEqual(branch["direct_entropy_safe_incidences"], 950)
        self.assertEqual(branch["curvature_obstructed_incidences"], 16)
        self.assertEqual(branch["two_node_rank_one_pairs"], 288)
        self.assertEqual(branch["fully_direct_entropy_safe_pairs"], 276)
        self.assertEqual(branch["pairs_requiring_a_shell_seam"], 12)
        self.assertEqual(branch["safe_incidences_on_seam_pairs"], 44)

    def test_curvature_obstructions_have_exact_linear_workload_descent(self):
        branch = self.result["obstruction_workload_branch"]
        self.assertEqual(branch["incidences"], 16)
        self.assertEqual(branch["pairs"], 12)
        self.assertEqual(branch["workloads"], [(2, 1, 3), (2, 3, 1)])
        self.assertEqual(len(branch["rows"]), 16)

    def test_only_two_seam_pairs_have_global_linear_workload_descent(self):
        branch = self.result["global_linear_workload_branch"]
        self.assertEqual(branch["globally_closed_pairs"], 2)
        self.assertEqual(branch["globally_closed_obstruction_incidences"], 2)
        self.assertEqual(branch["remaining_pairs"], 10)
        self.assertEqual(branch["remaining_obstruction_incidences"], 14)
        self.assertEqual(len(branch["minimal_counterexamples"]), 10)
        self.assertTrue(
            all(
                row["descriptor_weight"] == [1, 1, 1]
                for row in branch["minimal_counterexamples"]
            )
        )

    def test_rate_dependent_linear_family_closes_all_twelve_seam_pairs(self):
        branch = self.result["rate_dependent_linear_workload_branch"]
        self.assertEqual(branch["all_seam_pairs"], 12)
        self.assertEqual(
            branch["class_counts"],
            {
                "double_and_mixed": 8,
                "double_only": 2,
                "mixed_only": 2,
            },
        )
        self.assertTrue(
            branch["all_have_a_positive_rate_dependent_linear_workload"]
        )
        self.assertEqual(len(branch["rows"]), 12)

    def test_arbitrary_directed_triple_top_has_factorial_linear_branch(self):
        branch = self.result["rank_one_triple_factorial_linear_branch"]
        self.assertEqual(branch["failed_incidences"], 279)
        self.assertEqual(branch["pairs"], 91)
        self.assertEqual(
            branch["top_support_histogram"],
            {
                "2A,2B,AB": 270,
                "2A,2C,AC": 6,
                "2B,2C,BC": 3,
            },
        )
        self.assertTrue(branch["all_lower_linkages_have_a_top_species_source"])
        self.assertTrue(
            branch[
                "all_have_one_rate_dependent_factorial_linear_all_active_potential"
            ]
        )

    def test_rank_two_top_has_exact_positive_linear_workload(self):
        branch = self.result["rank_two_linear_workload_branch"]
        self.assertEqual(branch["failed_incidences"], 24)
        self.assertEqual(branch["pairs"], 24)
        self.assertEqual(branch["top_size_histogram"], {"4": 17, "5": 6, "6": 1})
        self.assertEqual(
            branch["workload_histogram"],
            {"1,1,1": 22, "1,2,1": 1, "2,1,1": 1},
        )
        self.assertTrue(branch["all_have_exact_global_positive_linear_workload"])

    def test_two_and_all_active_rank_one_top_corrections_are_compatible(self):
        branch = self.result["two_active_rate_correction_compatibility"]
        self.assertEqual(branch["all_active_pairs"], 403)
        self.assertEqual(branch["two_active_rank_one_pairs"], 310)
        self.assertEqual(branch["overlap_pairs"], 298)
        self.assertTrue(branch["all_overlap_pairs_have_one_identical_top_mask"])
        self.assertEqual(branch["top_size_histogram"], {"2": 207, "3": 91})
        self.assertEqual(branch["curvature_seam_overlap_pairs"], 12)
        self.assertEqual(branch["common_corrected_factorial_candidate_pairs"], 286)
        self.assertEqual(
            branch["top_support_histogram"],
            {
                "2A,2B": 63,
                "2A,2B,AB": 88,
                "2A,2C,AC": 2,
                "2A,AB": 63,
                "2A,BC": 12,
                "2B,2C,BC": 1,
                "2B,AB": 63,
                "B,2A": 6,
            },
        )

    def test_linear_selector_seam(self):
        seam = self.result["selector_seam"]
        self.assertEqual(seam["whole_top_support"], ["2A", "BC"])
        self.assertEqual(seam["common_population_dominance"], ["B", "A", "C"])
        self.assertEqual(
            seam["failed_weights"],
            [[2, 3, 1], [3, 4, 2], [3, 5, 1], [4, 5, 3], [7, 10, 4]],
        )

    def test_fixed_epsilon_curvature_obstructions(self):
        self.assertEqual(self.result["curvature_obstruction_incidences"], 16)
        self.assertEqual(self.result["curvature_obstruction_pairs"], 12)
        self.assertEqual(
            self.result["curvature_excess_histogram"],
            {"1": 12, "2": 4},
        )
        self.assertEqual(
            self.result["curvature_top_supports"],
            [["2A", "BC"]],
        )
        counter = self.result["fixed_epsilon_counterexample"]
        self.assertEqual(counter["weight"], [3, 1, 5])
        self.assertEqual(counter["integer_state_family"], ["N^3", "N", "N^5"])

    def test_shell_potential_is_not_global(self):
        counter = self.result["shell_potential_pass_counterexample"]
        self.assertEqual(counter["weight"], [3, 1, 1])
        self.assertEqual(counter["integer_state_family"], ["N^3", "N", "N"])
        self.assertEqual(
            counter["strong_lower_cycle"],
            ["A->2C", "2C->B", "B->0", "0->A"],
        )

    def test_no_single_shell_power_glues_the_two_regimes(self):
        counter = self.result["shell_power_counterexample"]
        self.assertEqual(
            counter["strong_lower_cycle"],
            ["2B->AB", "AB->A", "A->0", "0->2B"],
        )
        self.assertEqual(counter["failed_required_power"], "p>=1/5")
        self.assertEqual(counter["pass_required_power"], "p<1/11")
        self.assertEqual(counter["pass_shell_center_exponents"], [10, 9, 11])

    def test_no_fixed_gap_per_shell_hinge_glues_the_two_regimes(self):
        counter = self.result["fixed_gap_hinge_counterexample"]
        self.assertEqual(counter["gap_to_shell_ratio"], "(log N)/N -> 0")
        self.assertEqual(
            counter["positive_shell_drift_order"],
            "N^20 log N",
        )
        self.assertIn("every fixed c>0", counter["conclusion"])


if __name__ == "__main__":
    unittest.main()
