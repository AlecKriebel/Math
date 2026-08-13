import sys
import unittest


sys.path.insert(0, "src")

import two_active_dormant_407_certificate as dormant


class Dormant407CertificateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = dormant.certificate()

    def test_exact_selector(self) -> None:
        self.assertEqual(
            self.result["selected_incidences"],
            {
                "total": 407,
                "positive": 369,
                "signed": 38,
                "sha256": dormant.EXPECTED_INCIDENCE_SHA256,
            },
        )
        self.assertEqual(
            self.result["selected_pairs"],
            {
                "total": 333,
                "positive": 299,
                "signed": 34,
                "sha256": dormant.EXPECTED_PAIR_SHA256,
            },
        )

    def test_normalized_support_exhaustion(self) -> None:
        normalization = self.result["normalization"]
        self.assertEqual(
            normalization["ratio_histogram"],
            {"1:2": 37, "1:3": 333, "4:5": 37},
        )
        self.assertEqual(normalization["proper_top_intersection"], ["VI"])
        self.assertEqual(
            normalization["row_sha256"],
            dormant.EXPECTED_NORMALIZED_ROW_SHA256,
        )
        templates = self.result["normalized_templates"]
        self.assertEqual(templates["total"], 188)
        self.assertEqual(
            templates["ratio_histogram"],
            {"1:2": 17, "1:3": 154, "4:5": 17},
        )
        self.assertEqual(templates["support_templates_ignoring_ratio"], 154)
        self.assertTrue(templates["ratio_1_2_equals_ratio_4_5_support_menu"])
        self.assertEqual(
            templates["physical_multiplicity_histogram"],
            {1: 17, 2: 147, 4: 24},
        )
        self.assertEqual(
            templates["sha256"],
            dormant.EXPECTED_NORMALIZED_TEMPLATE_SHA256,
        )

    def test_resistance_partition_and_exception(self) -> None:
        self.assertEqual(
            self.result["base_maximum_histogram"],
            {"2U": 296, "U": 111},
        )
        partition = self.result["candidate_resistance_partition"]
        self.assertEqual(partition["incidences"], {0: 395, 1: 10, 2: 2})
        self.assertEqual(partition["templates"], {0: 182, 1: 5, 2: 1})
        self.assertEqual(partition["maximum_down_resistance"], 2)
        exceptional = self.result["exceptional_birth_death_comparison_block"]
        self.assertEqual(exceptional["normalized_ratio"], [1, 3])
        self.assertEqual(exceptional["proper_support"], ["2U", "VI"])
        self.assertEqual(
            (exceptional["incidences"], exceptional["pairs"]),
            (12, 12),
        )
        self.assertEqual(
            exceptional["pair_sha256"],
            dormant.EXPECTED_EXCEPTIONAL_PAIR_SHA256,
        )

    def test_complete_one_active_partition(self) -> None:
        one_active = self.result["one_active_dimension"]
        self.assertEqual((one_active["incidences"], one_active["pairs"]), (1104, 333))
        self.assertEqual(
            one_active["incidence_sha256"],
            dormant.EXPECTED_ONE_ACTIVE_INCIDENCE_SHA256,
        )
        self.assertEqual(
            one_active["classified_sha256"],
            dormant.EXPECTED_ONE_ACTIVE_CLASSIFIED_SHA256,
        )
        self.assertEqual(one_active["profiles"], 527)
        self.assertEqual(
            one_active["family_histogram"],
            {
                "direct_physical_C": 99,
                "exact_family_ii": 48,
                "generalized_family_ii": 951,
                "open_whole": 6,
            },
        )
        partition = self.result["hard_pair_one_active_partition"]
        self.assertEqual(
            (
                partition["generalized_family_ii_pairs"],
                partition["exact_family_ii_hard_only_pairs"],
            ),
            (317, 16),
        )
        self.assertEqual(
            partition["exact_family_ii_hard_only_pair_sha256"],
            dormant.EXPECTED_HARD_ONLY_PAIR_SHA256,
        )
        self.assertTrue(partition["union_is_all_333_hard_pairs"])

    def test_generalized_family_ii_normalization_and_handoff(self) -> None:
        generalized = self.result["generalized_family_ii"]
        self.assertEqual(
            (generalized["incidences"], generalized["pairs"]),
            (951, 317),
        )
        self.assertEqual(
            generalized["incidence_sha256"],
            dormant.EXPECTED_GENERALIZED_ONE_ACTIVE_INCIDENCE_SHA256,
        )
        self.assertEqual(
            generalized["pair_sha256"],
            dormant.EXPECTED_GENERALIZED_PAIR_SHA256,
        )
        self.assertEqual(
            generalized["normalization"]["spectator_cap_histogram"],
            {"0": 317, "1": 317, "2": 317},
        )
        self.assertEqual(
            generalized["normalization"]["row_sha256"],
            dormant.EXPECTED_GENERALIZED_NORMALIZED_ROW_SHA256,
        )
        self.assertEqual(
            generalized["support_templates"],
            {
                "total": 146,
                "sha256": dormant.EXPECTED_GENERALIZED_SUPPORT_TEMPLATE_SHA256,
            },
        )
        self.assertEqual(
            generalized["support_cap_templates"],
            {
                "total": 438,
                "sha256": (
                    dormant.EXPECTED_GENERALIZED_SUPPORT_CAP_TEMPLATE_SHA256
                ),
            },
        )

        handoff = self.result["one_to_two_active_promotion_handoff"]
        self.assertEqual(
            (
                handoff["mapped_source_incidences"],
                handoff["distinct_target_incidences"],
                handoff["distinct_target_pairs"],
                handoff["source_multiplicity_per_target"],
            ),
            (951, 317, 317, 3),
        )
        self.assertEqual(
            handoff["map_sha256"], dormant.EXPECTED_PROMOTION_MAP_SHA256
        )
        self.assertEqual(
            handoff["target_incidence_sha256"],
            dormant.EXPECTED_PROMOTION_TARGET_INCIDENCE_SHA256,
        )
        self.assertEqual(
            handoff["target_normalized_row_sha256"],
            dormant.EXPECTED_PROMOTION_TARGET_NORMALIZED_ROW_SHA256,
        )
        self.assertEqual(handoff["target_templates"], 146)
        self.assertEqual(
            handoff["target_template_sha256"],
            dormant.EXPECTED_PROMOTION_TARGET_TEMPLATE_SHA256,
        )
        self.assertEqual(
            handoff["target_resistance_histogram"], {0: 305, 1: 10, 2: 2}
        )
        self.assertTrue(handoff["all_targets_are_exact_hard_1_to_3_rows"])
        self.assertTrue(handoff["normalized_supports_identical_at_handoff"])
        self.assertTrue(handoff["boundary_entry_jump_charged_analytically_in_note"])

    def test_repaired_start_weighted_green_premises(self) -> None:
        premises = self.result["repaired_start_weighted_green_premises"]
        self.assertEqual(premises["exact_proper_pair_templates"], 17)
        self.assertEqual(
            premises["source_histogram"], {"0": 6, "2U": 6, "U": 5}
        )
        self.assertTrue(
            premises["every_exact_pair_has_an_ifree_lower_source"]
        )
        self.assertTrue(
            premises["maximal_degree_is_taken_after_zero_macro_contraction"]
        )
        self.assertEqual(premises["polynomial_green_start_exponent"], "r+1")
        self.assertEqual(
            premises["factorial_theta_strictly_below"], "1/2"
        )

    def test_withdrawn_green_and_pathwise_claims_have_exact_witnesses(self) -> None:
        green = self.result["withdrawn_uniform_green_counterexample"]
        self.assertEqual(green["proper"], ["U", "I", "VI"])
        self.assertEqual(green["lower"], ["0", "2U", "UI"])
        self.assertEqual(
            green["states_U_I_relative_V"][-1], [2, 0, 1]
        )
        self.assertEqual(green["reachable_positive_debt_bases"], "U=2+2k")
        self.assertTrue(green["uniform_unweighted_green_bound_is_false"])

        pathwise = self.result["withdrawn_pathwise_h_counterexample"]
        self.assertEqual(pathwise["old_V_service"], -1)
        self.assertEqual(pathwise["delta_3V_plus_U"], 1)
        self.assertTrue(pathwise["pathwise_weighted_order_descent_is_false"])

    def test_unweighted_boundary_repair_exponents_and_reset_scope(self) -> None:
        repair = self.result["repaired_boundary_exponent_arithmetic"]
        self.assertEqual(repair["delta"], "1/8")
        self.assertEqual(
            repair["raw_unweighted_three_insertion_power"], "-9/4"
        )
        self.assertEqual(
            repair["completed_boundary_probability_power"], "-1/4"
        )
        self.assertEqual(
            repair["boundary_cost_over_service_power"], "-1/8"
        )
        self.assertTrue(repair["raw_weighted_all_r_claim_withdrawn"])
        self.assertTrue(repair["exact_state_regenerations_reset_local_J"])
        self.assertTrue(repair["nonexact_neutral_returns_stay_in_the_raw_block"])
        self.assertTrue(repair["exceptional_zeta_macro_uses_cumulative_A"])

    def test_service_endpoint_entropy_failure_and_logarithmic_repair(self) -> None:
        witness = self.result[
            "withdrawn_service_inclusive_entropy_drift_counterexample"
        ]
        self.assertEqual(witness["proper"], ["2U", "VI"])
        self.assertEqual(witness["lower"], ["0", "I", "2I", "UI"])
        self.assertEqual(
            witness["contracted_service_macro"], ["0->I", "VI->2U"]
        )
        self.assertEqual(witness["actual_spectator_endpoint"], "u+2")
        self.assertEqual(
            witness["entropy_increment_asymptotic"], "2*log(u)+O(1)"
        )
        self.assertTrue(witness["service_inclusive_negative_drift_is_false"])

        repair = self.result["repaired_service_endpoint_entropy_premises"]
        self.assertEqual(repair["continuation_operator"], "Q")
        self.assertEqual(repair["actual_terminal_service_operator"], "S")
        self.assertEqual(
            repair["service_boundary_majorant"], "B_ell+C*log(u+e)"
        )
        self.assertTrue(repair["actual_service_endpoint_retained"])
        self.assertTrue(repair["bounded_compact_resolvent_corrector"])
        self.assertEqual(
            repair["actual_endpoint_entropy_upper_bound"],
            "C*log(u+e)+O(1)",
        )
        self.assertEqual(repair["tier_endpoint_cost"], "o(log(n))")
        self.assertEqual(
            repair["paid_interruption_probability"], "n^(-1+o(1))"
        )
        self.assertEqual(
            repair["paid_interruption_endpoint_moments"], "n^o(1)"
        )
        self.assertEqual(
            repair["fourth_power_negative_term"], "-c*G^3*log(n)"
        )
        self.assertEqual(repair["pair_counts_promoted"], 0)

    def test_unbounded_paid_interruption_weighted_contraction(self) -> None:
        premises = self.result[
            "paid_interruption_weighted_contraction_premises"
        ]
        self.assertEqual(premises["support_templates"], 146)
        self.assertEqual(premises["maximum_paid_lower_source_molecularity"], 2)
        self.assertEqual(premises["i_increasing_ordered_edge_occurrences"], 705)
        self.assertEqual(
            premises["quadratic_i_increasing_ordered_edge_occurrences"], 253
        )
        self.assertEqual(
            premises["quadratic_i_increasing_edge_types"],
            [
                ["2U", "2I"],
                ["2U", "I"],
                ["2U", "UI"],
                ["2U", "VI"],
                ["UI", "2I"],
            ],
        )
        self.assertEqual(
            premises["exact_quadratic_witness"],
            {
                "proper": ["U", "I", "VI"],
                "lower": ["0", "2U", "2I"],
                "paid_edge": "2U->2I",
            },
        )
        self.assertTrue(premises["linear_only_i_increase_premise_is_false"])
        self.assertEqual(
            premises["correct_total_paid_over_top_ratio"], "O(n^(-1/3))"
        )
        self.assertEqual(
            premises["correct_i_birth_over_top_ratio"],
            "O(n^(-1/3)/I)",
        )
        self.assertEqual(
            premises["first_paid_tier_factor"], "n^(-1+o(1))"
        )
        self.assertEqual(
            premises["subsequent_paid_return_control"],
            "asymmetric physical-step Feynman-Kac inequality",
        )
        self.assertEqual(
            premises["exact_reserve_coordinate"],
            "R=V-n before first service",
        )
        self.assertEqual(
            premises["nonterminal_fast_step"],
            {"delta_R": -1, "max_delta_I": 1},
        )
        self.assertTrue(premises["fast_at_zero_reserve_is_terminal_service"])
        self.assertEqual(premises["asymmetric_mark_order"], "1<a_I<a_R")
        self.assertEqual(
            premises["actual_terminal_reward"],
            "z0^J*(1+U+I+R)^r",
        )
        self.assertEqual(
            premises["symmetric_mark_counterexample"],
            {
                "proper": ["0", "I", "2I", "VI"],
                "lower": ["U", "2U"],
                "proper_orientation": "0->I->VI->2I->0",
                "lower_orientation": "U<->2U",
                "paid_edge": "I->VI",
                "fast_edge": "VI->2I",
                "after_k_paid": "(I,J,R)=(1,k,k)",
                "after_t_fast": "(I,R)=(1+t,k-t)",
                "symmetric_exponent": "I+R=k+1",
            },
        )
        self.assertEqual(
            premises["symmetric_mark_witness_support_templates"], 1
        )
        self.assertTrue(
            premises["symmetric_i_plus_r_mark_strict_drift_is_false"]
        )
        self.assertTrue(premises["whole_phase_pointwise_ratio_mix_withdrawn"])
        self.assertTrue(premises["i_zero_macros_contracted_separately"])
        self.assertTrue(
            premises["actual_terminal_endpoint_in_feynman_kac_reward"]
        )
        self.assertEqual(
            premises["all_reaction_boundary_method"],
            "arbitrary fixed endpoint moment at included physical boundary",
        )
        self.assertTrue(premises["all_paid_orders_summed_by_neumann_series"])
        self.assertEqual(premises["direct_i_birth_tail"], "factorial")
        self.assertEqual(premises["total_i_j_r_tail"], "exponential")
        self.assertEqual(premises["endpoint_and_duration_moments"], "n^o(1)")
        self.assertEqual(premises["pair_counts_promoted"], 0)

    def test_claim_boundary(self) -> None:
        self.assertTrue(
            self.result["arbitrary_orientation_graph_theorem_candidate_written"]
        )
        self.assertTrue(
            self.result["aggregate_resolvent_theorem_candidate_written"]
        )
        self.assertTrue(
            self.result[
                "generalized_one_active_resolvent_theorem_candidate_written"
            ]
        )
        self.assertEqual(
            self.result["independent_analytic_audit_status"],
            "repaired_candidate_pending_independent_reaudit",
        )
        self.assertTrue(
            self.result[
                "uniform_unweighted_unbounded_spectator_green_bound_withdrawn"
            ]
        )
        self.assertTrue(
            self.result["pathwise_3V_plus_U_service_descent_withdrawn"]
        )
        self.assertTrue(
            self.result["weighted_all_r_three_insertion_bound_withdrawn"]
        )
        self.assertTrue(self.result["bounded_entropy_coboundary_repair_written"])
        self.assertTrue(
            self.result["service_inclusive_negative_entropy_drift_withdrawn"]
        )
        self.assertTrue(
            self.result["logarithmic_actual_service_endpoint_charge_written"]
        )
        self.assertTrue(
            self.result["finite_paid_interruption_hierarchy_withdrawn"]
        )
        self.assertTrue(self.result["linear_only_i_increase_premise_withdrawn"])
        self.assertTrue(self.result["symmetric_i_plus_r_mark_drift_withdrawn"])
        self.assertTrue(self.result["full_weighted_paid_neumann_sum_written"])
        self.assertFalse(self.result["analytic_theorem_independently_audited"])
        self.assertFalse(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
