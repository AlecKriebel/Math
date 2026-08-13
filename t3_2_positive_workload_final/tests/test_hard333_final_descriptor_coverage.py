from __future__ import annotations

import unittest

import hard333_final_descriptor_coverage as coverage


class Hard333FinalDescriptorCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = coverage.certificate()

    def test_exact_dimensions(self) -> None:
        self.assertEqual(self.result["pairs"], 333)
        self.assertEqual(self.result["failed_incidences"], 1960)
        self.assertEqual(
            self.result["active_count_histogram"],
            {"1": 1104, "2": 702, "3": 154},
        )

    def test_exact_local_routes(self) -> None:
        self.assertEqual(
            self.result["analytic_route_histogram"],
            {
                "H_b12_guard_free_shell_resolvent": 16,
                "H_w4_dyadic_activation_return": 4,
                "abstract_mixed_fast_schur_extension": 44,
                "audited_direct_C_multiservice": 99,
                "audited_generalized_146": 951,
                "audited_open_all_clock_multiservice": 6,
                "directed_triple_powered_generator": 24,
                "enabled181_access_word": 181,
                "physical188_macroscopic_carrier": 407,
                "rankone114_powered_endpoint": 114,
                "safe_reversible_powered_generator": 110,
                "zero_inactive_absorbing_face": 4,
            },
        )

    def test_one_pair_fixed_correction(self) -> None:
        self.assertEqual(
            self.result["pair_correction_histogram"],
            {
                "arbitrary_fixed_ell": 291,
                "directed_triple_adjusted_ell": 8,
                "reversible_top_adjusted_ell": 34,
            },
        )
        self.assertEqual(self.result["physical_dormant_normalized_templates"], 188)

    def test_audited_one_active_input_is_frozen(self) -> None:
        source = self.result["audited_one_active_1104_input"]
        self.assertEqual(
            source["proof_hashes"],
            {
                "theorem_sha256": coverage.ONE_ACTIVE_1104_NOTE_SHA256,
                "source_sha256": coverage.ONE_ACTIVE_1104_SOURCE_SHA256,
                "test_sha256": coverage.ONE_ACTIVE_1104_TEST_SHA256,
            },
        )
        self.assertEqual(source["rows_sha256"], coverage.ONE_ACTIVE_1104_ROWS_SHA256)
        self.assertEqual(
            source["payload_sha256"], coverage.ONE_ACTIVE_1104_PAYLOAD_SHA256
        )
        self.assertTrue(source["strict_scope_audit_passed"])

    def test_switch_masks_and_corrections_are_literal(self) -> None:
        self.assertEqual(
            self.result["switch_mask_compatibility"],
            {
                "switch_pairs": 16,
                "switch_pairs_with_one_all_active_mask": 16,
                "rankone_overlap_pairs": 12,
                "rankone_overlap_pairs_with_one_identical_mask": 12,
                "H_w_pairs_with_no_rankone_mask": 4,
                "all_switch_mask_assertions_passed": True,
            },
        )
        self.assertEqual(
            self.result["correction_compatibility"],
            {
                "rankone_rows_checked": 114,
                "rankone_correction_mismatches": 0,
                "all_active_rows_checked": 154,
                "all_active_correction_mismatches": 0,
                "all_114_plus_154_corrections_match_pair_fixed_choice": True,
            },
        )

    def test_hashes_and_claim_boundary(self) -> None:
        self.assertEqual(
            self.result["pair_rows_sha256"], coverage.EXPECTED_PAIR_ROWS_SHA256
        )
        self.assertEqual(
            self.result["failure_rows_sha256"],
            coverage.EXPECTED_FAILURE_ROWS_SHA256,
        )
        self.assertEqual(
            self.result["payload_sha256"], coverage.EXPECTED_PAYLOAD_SHA256
        )
        self.assertFalse(self.result["hard333_composition_independently_audited"])
        self.assertFalse(self.result["hard333_pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
