import unittest

import one_active_fourth_power_pair_composition as composition


class OneActiveFourthPowerPairCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = composition.certificate()
        cls.sets = composition.pair_sets()

    def test_exact_candidate_overlap_and_new_counts(self):
        self.assertEqual(self.payload["candidate_one_active_incidences"], 3297)
        self.assertEqual(
            self.payload["counts"],
            {
                "candidate_1227": {
                    "positive": 1076,
                    "signed": 151,
                    "total": 1227,
                },
                "already_certified_overlap_15": {
                    "positive": 15,
                    "signed": 0,
                    "total": 15,
                },
                "new_disjoint_1212": {
                    "positive": 1061,
                    "signed": 151,
                    "total": 1212,
                },
                "remainder_after_795": {
                    "positive": 759,
                    "signed": 36,
                    "total": 795,
                },
            },
        )

    def test_exact_set_identity(self):
        candidate = self.sets["candidate_1227"]
        overlap = self.sets["already_certified_overlap_15"]
        new = self.sets["new_disjoint_1212"]
        self.assertFalse(overlap & new)
        self.assertEqual(candidate, overlap | new)

    def test_frozen_pair_fingerprints(self):
        hashes = self.payload["fingerprints"]
        self.assertEqual(
            hashes["candidate_1227"], composition.EXPECTED_CANDIDATE_SHA256
        )
        self.assertEqual(
            hashes["already_certified_overlap_15"],
            composition.EXPECTED_OVERLAP_SHA256,
        )
        self.assertEqual(
            hashes["new_disjoint_1212"], composition.EXPECTED_NEW_SHA256
        )
        self.assertEqual(
            hashes["remainder_after_795"], composition.EXPECTED_AFTER_SHA256
        )

    def test_common_potential_and_analytic_inputs(self):
        self.assertEqual(
            self.payload["common_potential"],
            {
                "factorial_linear_correction": 0,
                "power": 4,
                "proper_on_population_space": True,
            },
        )
        inputs = self.payload["analytic_inputs"]
        self.assertTrue(inputs["affine_feasible_failures_all_one_active"])
        self.assertTrue(
            inputs["arbitrary_orientation_graph_resistance_certified"]
        )
        self.assertTrue(
            inputs["all_23_physical_kernel_interface_certified_locally"]
        )
        self.assertEqual(inputs["random_up_overshoot_uses_q_strictly_above"], 8)
        self.assertTrue(inputs["all_species_reflected_finite_target_used"])
        self.assertTrue(inputs["classwise_family_ii_cap_constants"])

    def test_pair_theorem_is_certified_but_global_claim_stays_false(self):
        self.assertTrue(self.payload["composition_note_complete_for_audit"])
        self.assertEqual(
            self.payload["independent_audit"],
            {
                "verdict": "pass",
                "confidence": "0.91",
                "audited_note_sha256": (
                    "652e41ccd7ae36183862a798fcdfd3bd5acf92ab2528bb356816d14df003b09a"
                ),
            },
        )
        self.assertTrue(self.payload["candidate_1227_recurrence_certified"])
        self.assertTrue(
            self.payload["new_disjoint_1212_recurrence_certified"]
        )
        self.assertFalse(self.payload["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
