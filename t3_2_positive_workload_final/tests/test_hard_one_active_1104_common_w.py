import unittest

import hard_one_active_1104_common_w as theorem


class HardOneActive1104CommonWTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = theorem.certificate()
        cls.rows = theorem.coverage_rows()

    def test_exact_partition(self) -> None:
        self.assertEqual(self.payload["one_active_incidences"], 1104)
        self.assertEqual(
            self.payload["family_histogram"],
            {
                "direct_physical_C": 99,
                "exact_family_ii": 48,
                "generalized_family_ii": 951,
                "open_whole": 6,
            },
        )
        self.assertEqual(
            self.payload["analytic_route_histogram"],
            {
                "abstract_mixed_fast_schur_extension": 44,
                "audited_direct_C_multiservice": 99,
                "audited_generalized_146": 951,
                "audited_open_all_clock_multiservice": 6,
                "zero_inactive_absorbing_face": 4,
            },
        )

    def test_exact_family_ii_is_inside_abstract_mixed_class(self) -> None:
        exact = [
            row for row in self.rows
            if row["structural_family"] == "exact_family_ii"
        ]
        self.assertEqual(len(exact), 48)
        self.assertEqual(
            self.payload["exact_family_ii_graph_category_histogram"],
            {"family_ii_axis_down_0": 40, "family_ii_axis_no_history": 8},
        )
        self.assertEqual(
            self.payload["exact_family_ii_translated_support_templates"], 8
        )
        for row in exact:
            premises = row["premises"]
            self.assertTrue(premises["at_least_one_linkage_is_mixed"])
            self.assertTrue(premises["proper_is_not_exact_base_open_pair"])
            self.assertTrue(premises["all_complexes_in_abstract_mixed_menu"])

    def test_no_history_label_is_repaired_not_assumed(self) -> None:
        repair = self.payload["axis_no_history_repair"]
        self.assertEqual(repair["old_label_count"], 8)
        self.assertEqual(repair["actually_frozen_zero_inactive_rows"], 4)
        self.assertEqual(
            repair["positive_spectator_rows_rerouted_to_mixed_schur"], 4
        )
        self.assertTrue(repair["old_eight_row_exclusion_is_false"])
        witness = repair["counterhistory"]
        self.assertEqual(witness["states_U_relativeV_I"][0], [1, 0, 0])
        self.assertEqual(witness["states_U_relativeV_I"][-1], [1, 2, 0])
        self.assertEqual(witness["positive_reflected_debt_created"], 2)

    def test_predicate_routes_and_claim_boundary(self) -> None:
        for row in self.rows:
            route = row["analytic_route"]
            premises = row["premises"]
            if route == "audited_direct_C_multiservice":
                self.assertTrue(
                    premises["mixed_linkage_contains_physical_active_source_C"]
                )
                self.assertTrue(premises["same_linkage_contains_lower_target"])
                self.assertTrue(
                    premises["background_uniform_tagged_service_minorization"]
                )
                self.assertTrue(
                    premises["all_active_bearing_complexes_have_one_C"]
                )
                self.assertTrue(premises["stripped_top_menu_subset_0_A_B"])
                self.assertTrue(
                    premises[
                        "service_targets_have_inactive_molecularity_at_most_two"
                    ]
                )
                self.assertTrue(premises["direct_multiservice_predicate"])
            elif route == "audited_open_all_clock_multiservice":
                self.assertTrue(premises["whole_phase_is_C_AC"])
                self.assertTrue(premises["BC_stopping_rule_is_autonomous_of_A"])
                self.assertTrue(
                    premises["designated_zero_source_launch_allowed_at_B_zero"]
                )
                self.assertTrue(
                    premises["defect_excludes_designated_zero_source_launch"]
                )
                self.assertTrue(
                    premises["open_all_clock_multiservice_predicate"]
                )
            elif route == "zero_inactive_absorbing_face":
                self.assertTrue(premises["no_source_enabled_at_U_I_zero"])
                self.assertTrue(
                    premises["positive_debt_impossible_in_a_closed_class"]
                )

        self.assertTrue(
            self.payload["analytic_one_active_1104_theorem_written"]
        )
        self.assertTrue(
            self.payload[
                "analytic_one_active_1104_theorem_independently_audited"
            ]
        )
        self.assertTrue(
            self.payload[
                "direct_open_multiservice_strict_independent_audit_passed"
            ]
        )
        self.assertFalse(self.payload["hard_pair_recurrence_certified"])
        self.assertFalse(self.payload["global_t3_2_certified"])

    def test_multiservice_repair_is_frozen(self) -> None:
        proof_hashes = self.payload["proof_hashes"]
        self.assertEqual(
            proof_hashes["prior_1104_scope_audit_sha256"],
            theorem.PRIOR_1104_SCOPE_AUDIT_SHA256,
        )
        self.assertEqual(
            proof_hashes["direct_open_multiservice_note_sha256"],
            theorem.DIRECT_OPEN_MULTISERVICE_NOTE_SHA256,
        )
        self.assertEqual(
            proof_hashes["direct_open_multiservice_audit_sha256"],
            theorem.DIRECT_OPEN_MULTISERVICE_AUDIT_SHA256,
        )

    def test_frozen_hashes(self) -> None:
        self.assertEqual(self.payload["rows_sha256"], theorem.EXPECTED_ROWS_SHA256)
        self.assertEqual(
            self.payload["payload_sha256"], theorem.EXPECTED_PAYLOAD_SHA256
        )


if __name__ == "__main__":
    unittest.main()
