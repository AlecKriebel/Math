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
            "fail_as_written_start_weighted_green_repair_open",
        )
        self.assertTrue(
            self.result[
                "uniform_unweighted_unbounded_spectator_green_bound_withdrawn"
            ]
        )
        self.assertFalse(self.result["analytic_theorem_independently_audited"])
        self.assertFalse(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
