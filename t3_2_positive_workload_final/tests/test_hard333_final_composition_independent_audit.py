from __future__ import annotations

import unittest

import hard333_final_composition_independent_audit as audit


class Hard333FinalCompositionIndependentAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = audit.certificate()

    def test_frozen_targets_and_dependencies(self) -> None:
        self.assertEqual(self.result["target_hashes"], audit.TARGET_HASHES)
        self.assertEqual(
            self.result["dependency_hashes"], audit.DEPENDENCY_HASHES
        )

    def test_independent_exhaustion_replay(self) -> None:
        self.assertEqual(self.result["pairs"], 333)
        self.assertEqual(self.result["failed_incidences"], 1960)
        self.assertEqual(
            self.result["active_count_histogram"],
            {"1": 1104, "2": 702, "3": 154},
        )
        self.assertEqual(
            self.result["independent_failure_rows_sha256"],
            self.result["candidate_failure_rows_sha256"],
        )
        self.assertEqual(self.result["physical_dormant_normalized_templates"], 188)

    def test_literal_correction_masks(self) -> None:
        masks = self.result["literal_correction_mask_replay"]
        self.assertEqual(masks["rankone_pairs"], 38)
        self.assertEqual(masks["rankone_pairs_with_one_mask"], 38)
        self.assertEqual(masks["all_active_pairs"], 46)
        self.assertEqual(masks["all_active_pairs_with_one_mask"], 46)
        self.assertEqual(masks["rankone_all_active_overlap_pairs"], 38)
        self.assertEqual(masks["overlap_pairs_with_identical_mask"], 38)
        self.assertEqual(masks["correction_relevant_pairs"], 46)
        self.assertEqual(masks["correction_relevant_pairs_with_one_literal_mask"], 46)
        self.assertEqual(masks["H_b_pairs"], 12)
        self.assertEqual(masks["H_w_pairs"], 4)
        self.assertEqual(masks["H_w_pairs_without_rankone_mask"], 4)
        self.assertEqual(
            masks["pair_correction_histogram"],
            {
                "arbitrary_fixed_ell": 291,
                "directed_triple_adjusted_ell": 8,
                "reversible_top_adjusted_ell": 34,
            },
        )

    def test_proof_first_verdict_and_boundary(self) -> None:
        self.assertEqual(self.result["audit_verdict"], "STRICT PASS")
        self.assertTrue(
            self.result["hard333_fixed_class_theorem_independently_audited"]
        )
        self.assertTrue(self.result["hard333_pair_recurrence_theorem_established"])
        self.assertTrue(self.result["candidate_flags_were_not_modified"])
        self.assertFalse(self.result["global_t3_2_certified"])
        self.assertTrue(all(self.result["proof_obligations"].values()))


if __name__ == "__main__":
    unittest.main()
