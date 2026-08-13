import sys
import unittest


sys.path.insert(0, "src")

import two_active_dormant_407_two_level_repair as repair


class TwoLevelRepairTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = repair.repair_certificate()

    def test_failed_snapshot_is_frozen_not_silently_patched(self) -> None:
        self.assertEqual(
            self.result["frozen_failed_snapshot_sha256"],
            repair.FROZEN_FAILED_HASHES,
        )
        self.assertEqual(
            self.result["frozen_failure_verdict"], "FAIL-as-written"
        )
        self.assertEqual(
            self.result["frozen_failure_scope"],
            "proof failure, not a recurrence or T3-2 counterexample",
        )

    def test_complete_146_template_two_level_partition(self) -> None:
        menu = self.result["exact_menu_partition"]
        self.assertEqual(menu["support_templates"], 146)
        self.assertEqual(menu["base_open_exact"], 17)
        self.assertEqual(menu["exact_without_ifree_proper_source"], 20)
        self.assertEqual(menu["larger_proper_support"], 109)
        self.assertEqual(17 + 20 + 109, 146)
        self.assertEqual(
            menu["base_open_source_histogram"],
            {"0": 6, "U": 5, "2U": 6},
        )
        self.assertEqual(
            menu["base_open_cut_histogram"],
            {
                "0": {"1": 1, "2": 5},
                "U": {"2": 5},
                "2U": {"0": 1, "1": 5},
            },
        )
        self.assertEqual(
            menu["base_open_rows_sha256"],
            "64643b70b556e250b9bb01ff48fea3594e0fa5665ca3877f3517d2ccfbb812fd",
        )

    def test_unique_exception_and_first_defect_degree(self) -> None:
        exceptional = self.result["exceptional_template"]
        self.assertEqual(set(exceptional["proper"]), {"2U", "VI"})
        self.assertEqual(
            set(exceptional["lower"]), {"0", "I", "2I", "UI"}
        )
        self.assertEqual(exceptional["base_source_degree"], 2)
        self.assertEqual(exceptional["lower_cut_degree"], 0)
        self.assertEqual(
            exceptional["apparent_nested_effective_rate"], "O(U^4/n)"
        )
        self.assertEqual(
            exceptional["dangerous_nested_then_fast"],
            "exact physical self return",
        )
        self.assertEqual(
            exceptional["nonself_effective_rate"], "O(U^3/n)"
        )
        self.assertTrue(
            exceptional["degree_one_first_defect_edges_are_U_nonincreasing"]
        )
        self.assertEqual(
            exceptional["positive_U_first_defect_edge_source_degree"], 0
        )
        self.assertEqual(
            exceptional["positive_U_continuing_base_rate"], "O(U^2/n)"
        )
        self.assertEqual(
            exceptional["positive_U_terminal_service_rate_can_be"],
            "O(U^3/n)",
        )
        self.assertEqual(
            exceptional["degree_one_positive_terminal_service_states"],
            (
                [20, 0, 0],
                [18, 1, 1],
                [17, 2, 1],
                [19, 1, 0],
                [21, 0, -1],
            ),
        )
        self.assertEqual(
            exceptional["terminal_factorial_method"],
            "theta_minus<theta_zero<theta_plus gap",
        )

    def test_arbitrary_nested_null_word_is_exact_physical_self(self) -> None:
        for duplicates in (0, 1, 2, 7):
            states = repair.exact_self_word_states(
                n=10**6, u=40, duplicates=duplicates
            )
            self.assertEqual(states[0], states[-1])
            self.assertEqual(states[0], [40, 0, 0])
            self.assertEqual(
                max(state[1] for state in states), duplicates + 1
            )
            self.assertEqual(
                max(state[2] for state in states), duplicates + 1
            )

    def test_outer_kernel_uses_only_physical_state(self) -> None:
        state = self.result["two_level_state"]
        self.assertEqual(
            state["reset"],
            "only at an included physical I=R=0 base return",
        )
        self.assertEqual(state["outer"], "physical one-species base (U,n,0)")
        self.assertEqual(state["upward_terminal"], "an I=0 return with V>n")
        self.assertEqual(
            state["outer_outcome_partition"],
            [
                "exact physical self return",
                "nonexact continuing I=R=0 return",
                "strict service",
                "upward I=0,R>0 return",
                "physical boundary",
            ],
        )
        self.assertEqual(
            state["perturbed_terminal_kernel"],
            "strict service plus upward return",
        )
        self.assertEqual(state["terminal_and_boundary_marks"], ["U", "I", "R"])
        self.assertFalse(state["global_paid_counter_used"])
        self.assertFalse(state["finite_paid_cap_used"])

        erasure = self.result["self_loop_erasure"]
        self.assertEqual(
            erasure["criterion"], "exact equality of the complete physical state"
        )
        self.assertTrue(
            erasure["raw_diagonal_includes_opening_selection_probability"]
        )
        self.assertTrue(erasure["raw_renewal_includes_no_interruption_base_exit"])
        self.assertTrue(erasure["boundary_hits_inside_a_loop_retained"])
        self.assertTrue(erasure["physical_loop_duration_retained"])
        self.assertTrue(erasure["performed_before_weighted_and_duration_norms"])
        self.assertEqual(
            erasure["projection_scope"], "descriptor-local physical kernel only"
        )
        self.assertFalse(
            erasure["global_reflected_debt_mark_equality_asserted"]
        )
        self.assertTrue(erasure["common_W_depends_only_on_physical_population"])
        self.assertEqual(erasure["fixed_population_global_mark_fiber"], "finite")
        self.assertFalse(erasure["mark_corrector_inserted"])
        self.assertEqual(erasure["fiber_finiteness_use"], "properness only")
        self.assertTrue(erasure["physical_law_incoming_mark_independent"])

        inner = self.result["inner_open_excursion"]
        self.assertEqual(inner["state"], ["U", "I", "R", "local_N"])
        self.assertEqual(
            inner["admissible_initial_data"],
            "base opening N=0,I+R<=2 or post-first-slow N=1,I+R<=5",
        )
        self.assertFalse(inner["arbitrary_initial_I_R_polynomial_bound_claimed"])
        self.assertEqual(inner["mark_order"], "1<a_I<a_R")
        self.assertEqual(inner["terminal_reward"], "(1+U+I+R)^q")
        self.assertFalse(inner["terminal_contains_local_N"])
        self.assertEqual(inner["polynomial_endpoint_order"], "q -> q")
        self.assertTrue(inner["all_local_interruption_orders_summed"])

    def test_log_refined_critical_degree_ledger(self) -> None:
        primitive = self.result["positive_continuing_primitive_ledger"]
        self.assertEqual(primitive["templates"], 146)
        self.assertEqual(
            primitive["orientation_menu"],
            "complete directed support supergraph",
        )
        self.assertEqual(
            primitive["actual_strong_orientation_relation"], "subgraph"
        )
        self.assertEqual(
            primitive["outer_denominator"],
            "post-diagonal cut/service degree",
        )
        self.assertEqual(primitive["primitive_positive_continuing_paths"], 1308)
        self.assertEqual(
            primitive["relative_power_jump_histogram"],
            {
                "-2,1": 158,
                "-2,2": 170,
                "-2,3": 58,
                "-2,4": 36,
                "-1,1": 316,
                "-1,2": 140,
                "-1,3": 20,
                "0,1": 238,
                "0,2": 98,
                "1,1": 73,
                "2,1": 1,
            },
        )
        self.assertEqual(
            primitive["exact_pair_outer_degree_histogram"],
            {
                "0|VI,1": 1,
                "0|VI,2": 5,
                "U|VI,2": 5,
                "2U|VI,0": 1,
                "2U|VI,1": 5,
                "I|VI,1": 1,
                "I|VI,2": 6,
                "2I|VI,1": 1,
                "2I|VI,2": 5,
                "UI|VI,1": 1,
                "UI|VI,2": 6,
            },
        )
        self.assertEqual(
            primitive["maximum_opening_plus_defect_source_degree"], 3
        )
        self.assertFalse(primitive["degree_two_plus_degree_two_positive_path"])
        self.assertEqual(primitive["maximum_positive_jump"], 4)
        self.assertEqual(primitive["critical_twice_weighted_power"], 5)
        self.assertEqual(
            primitive["path_ledger_sha256"],
            "07b3a03c77ce5d58c87130f6344e8dc6e36d92cf5f99a59b46603fd31144057f",
        )

        exact_returns = self.result["interrupted_exact_return_ledger"]
        self.assertEqual(exact_returns["templates"], 146)
        self.assertTrue(exact_returns["pure_nested_class_removed_first"])
        self.assertEqual(
            exact_returns["one_defect_interrupted_exact_returns"], 1560
        )
        self.assertEqual(
            exact_returns["relative_power_histogram"],
            {"-2": 164, "-1": 482, "0": 636, "1": 278},
        )
        self.assertEqual(exact_returns["maximum_relative_power"], 1)
        self.assertEqual(
            exact_returns["rows_sha256"],
            "dd867ec4bb0457e7157054211af8247a99edafb59ee8dd00f9ea574666422afb",
        )

        ledger = self.result["outer_degree_ledger"]
        self.assertEqual(ledger["cutoff"], "floor(n^(1/3)/log(n+e))")
        self.assertEqual(ledger["cutoff_weight"], "n^(1/3+o(1))")
        self.assertEqual(
            ledger["uniform_outer_neumann_norm"], "O(log(n)^(-3))"
        )
        self.assertEqual(
            ledger["factorial_exponent_condition"], "theta<1/2"
        )
        self.assertEqual(
            ledger["factorial_positive_bound_at_cutoff"],
            "n^(-(1-theta)/3+o(1))",
        )
        self.assertTrue(ledger["same_weight_continuation_green"])
        self.assertTrue(ledger["terminal_weight_gap_only"])
        self.assertEqual(
            ledger["multi_slow_prefix_bound"],
            "subsumed by the all-k invariant",
        )
        self.assertEqual(
            ledger["extra_slow_geometric_ratio"],
            "O((1+U)^3/n)=o(1) after I occupation",
        )
        self.assertIn(
            "pairs with one reserve-consuming fast firing",
            ledger["reserve_fast_count_for_k_slow"],
        )
        self.assertEqual(
            ledger["positive_U_continuing_rate_exceptional"],
            "O((1+U)^2/n)",
        )
        self.assertEqual(
            ledger["positive_U_terminal_service_rate_exceptional"],
            "O((1+U)^3/n)",
        )
        self.assertEqual(
            ledger["factorial_terminal_method"],
            "theta_minus<theta_zero<theta_plus two-weight gap",
        )
        self.assertEqual(
            ledger["primitive_positive_weighted_power"], "2+theta<5/2"
        )
        self.assertEqual(
            ledger["primitive_positive_bound_at_cutoff"],
            "n^(-(1-theta)/3+o(1)) <= n^(-1/6+o(1))",
        )
        self.assertEqual(
            ledger["all_k_coupled_invariant"],
            "r+j<=2*k+1 and r+theta*j<=2*k+theta",
        )
        self.assertEqual(
            ledger["r_le_2k_scope"],
            "positive continuing or interrupted exact returns only",
        )
        self.assertFalse(ledger["negative_return_r_le_2k_claimed"])
        self.assertIn("pair each VI cleanup", ledger["all_k_proof_method"])
        self.assertIn("P(N>=m|opened)", ledger["all_orders_open_race"])
        self.assertEqual(ledger["all_orders_I_occupation_cost"], "C^k*k^k")
        self.assertEqual(
            ledger["factorial_continuation_geometric_ratio"],
            "C*L^3/n=o(1)",
        )
        self.assertEqual(
            ledger["pure_renewal_amplification"]["proper_subset"], "O(1)"
        )
        self.assertIn(
            "N>=2", ledger["pure_renewal_amplification"]["unique_exact_pair_d_0"]
        )
        self.assertIn(
            "historical positive-debt",
            ledger["compact_nontrapping_basis"],
        )
        self.assertIn(
            "(I-Z_pure)^-1 Z_int",
            ledger["interrupted_diagonal_renewal"],
        )
        self.assertIn("L^3/n", ledger["interrupted_diagonal_norm"])
        self.assertEqual(
            ledger["first_nonself_insertion_from_subpower_start"],
            "n^(-1+o(1))",
        )

        boundary = self.result["boundary_and_duration"]
        self.assertEqual(boundary["boundary"], ["U", "I", "R"])
        self.assertEqual(
            boundary["exact_handoff_boundary"],
            "I=R=0 outer-base U boundary only",
        )
        self.assertEqual(
            boundary["open_phase_U_boundary"],
            "auxiliary charged boundary",
        )
        self.assertEqual(
            boundary["unperturbed_terminal_partition"],
            ["strict service", "outer-base promotion", "physical boundary"],
        )
        self.assertFalse(boundary["no_interruption_upward_return"])
        self.assertFalse(boundary["paid_counter_boundary"])
        self.assertTrue(boundary["every_fixed_endpoint_order"])
        self.assertTrue(boundary["every_fixed_physical_duration_order"])
        self.assertTrue(boundary["rare_event_endpoint_weighted_entropy"])
        self.assertTrue(boundary["rare_event_includes_interrupted_terminals"])
        self.assertTrue(boundary["zero_slow_service_I_R_uniformly_bounded"])
        self.assertTrue(boundary["full_physical_G_entropy_split"])
        self.assertEqual(
            boundary["duration_method"],
            "competing physical hazard after diagonal renewal",
        )
        self.assertTrue(boundary["hard_sections_3_to_6_log_refinement_uniform"])

    def test_historical_positive_debt_scope(self) -> None:
        scope = self.result["historical_scope"]
        self.assertEqual(scope["normalized_no_history_supports"], 12)
        self.assertEqual(scope["physical_incidences"], 84)
        self.assertEqual(scope["pairs"], 28)
        self.assertIn("D_V>0", scope["required_local_start"])
        self.assertIn("finite", scope["D_V_zero_alternative"])
        self.assertEqual(scope["witness"]["proper"], ["I", "VI"])
        self.assertEqual(scope["witness"]["lower"], ["0", "U", "2U"])
        self.assertTrue(scope["witness"]["face_invariant"])
        self.assertFalse(scope["witness"]["V_changes_on_face"])
        self.assertFalse(scope["witness"]["strict_service_possible_on_face"])
        self.assertEqual(
            scope["rows_sha256"],
            "f56f470b58326b30dd90a7e08b39faa5709443d90a02db317eea32f1dc043666",
        )
        self.assertEqual(
            scope["pair_payloads_sha256"],
            "b287c027577bdde30e90d42ad3878d02d016794ff0d85133ab7f16a1bf60a23d",
        )

    def test_fresh_audit_obligations_are_explicit(self) -> None:
        obligations = self.result["independent_audit_obligations"]
        self.assertEqual(len(obligations), 6)
        self.assertIn("two-stage raw diagonal renewal", obligations[0])
        self.assertIn("same-order inner", obligations[1])
        self.assertIn("exceptional first-defect", obligations[2])
        self.assertIn("146-support fixed-cut", obligations[3])
        self.assertIn("service/upward/boundary", obligations[3])
        self.assertIn("finite one-defect ledger used only as regression", obligations[4])
        self.assertIn("all-k coupled source-endpoint invariant", obligations[4])
        self.assertIn("three-weight terminal gap", obligations[4])
        self.assertIn("historical positive-debt scope", obligations[5])
        self.assertIn("exact no-fast promotion", obligations[5])
        self.assertIn("charged open boundaries", obligations[5])

    def test_claim_boundary(self) -> None:
        self.assertEqual(self.result["pair_counts_promoted"], 0)
        self.assertFalse(self.result["descriptor_local_recurrence_certified"])
        self.assertEqual(
            self.result["certification_flags"],
            {
                "analytic_theorem_independently_audited": False,
                "pair_level_recurrence_certified": False,
                "global_t3_2_certified": False,
            },
        )


if __name__ == "__main__":
    unittest.main()
