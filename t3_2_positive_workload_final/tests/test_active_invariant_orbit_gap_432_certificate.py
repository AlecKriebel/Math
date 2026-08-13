import unittest

import active_invariant_orbit_gap_432_certificate as gap
import s_tier_superlevel_interface as superlevel
import stoichiometric_gate_feasibility as feasibility


class ActiveInvariantOrbitGap432Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = gap.certificate()

    def test_exact_dependency_bytes(self) -> None:
        self.assertEqual(
            self.result["dependency_sha256"],
            gap.EXPECTED_DEPENDENCY_SHA256,
        )

    def test_seed_orbit_subtraction_is_literal(self) -> None:
        self.assertEqual(self.result["positive_seed_pairs"], 4_761)
        self.assertEqual(self.result["signed_seed_pairs"], 408)
        self.assertEqual(self.result["inherited_seed_pairs"], 5_169)
        self.assertEqual(self.result["active_invariant_seed_pairs"], 110)
        self.assertEqual(self.result["active_invariant_orbit_pairs"], 714)
        self.assertEqual(self.result["other_seed_orbit_pairs"], 27_462)
        self.assertEqual(self.result["orbit_overlap_pairs"], 282)
        self.assertEqual(self.result["full_inherited_seed_orbit_pairs"], 27_894)
        self.assertEqual(self.result["exclusive_orbit_gap_pairs"], 432)
        self.assertEqual(
            gap.active_invariant_orbit() - gap.other_seed_orbit(),
            gap.exclusive_orbit_gap_pairs(),
        )

    def test_pair_manifest_and_fingerprint_are_exact(self) -> None:
        self.assertEqual(len(self.result["gap_pair_manifest"]), 432)
        self.assertEqual(
            self.result["exclusive_orbit_gap_pair_sha256"],
            gap.EXPECTED_GAP_PAIR_SHA256,
        )
        self.assertEqual(
            self.result["exclusive_orbit_gap_pair_sha256"],
            "5516d6071b2b9d07b0e4e02613b9caee217ba3ebb0082e21f2bc664e6247ea36",
        )

    def test_corrected_cut_and_affine_split(self) -> None:
        self.assertEqual(self.result["tier_descriptors"], 259)
        self.assertEqual(
            self.result["pairs_with_no_feasible_corrected_cut_failure"],
            360,
        )
        self.assertEqual(
            self.result["pairs_with_feasible_corrected_cut_failure"],
            72,
        )
        self.assertEqual(
            self.result["feasible_corrected_cut_failure_rows"],
            192,
        )
        self.assertEqual(len(self.result["no_failure_pair_manifest"]), 360)
        self.assertEqual(len(self.result["failed_pair_manifest"]), 72)
        self.assertEqual(
            self.result["no_failure_pair_sha256"],
            gap.EXPECTED_NO_FAILURE_PAIR_SHA256,
        )
        self.assertEqual(
            self.result["failed_pair_sha256"],
            gap.EXPECTED_FAILED_PAIR_SHA256,
        )
        for pair, descriptor in gap.feasible_corrected_cut_failures():
            self.assertTrue(feasibility.descriptor_feasible(pair, descriptor))
            self.assertFalse(
                superlevel.universal_strong_orientation_condition(
                    pair,
                    descriptor,
                )
            )

    def test_every_failure_is_exactly_b_f0_or_b_b(self) -> None:
        self.assertEqual(
            self.result["failure_category_histogram"],
            {"B/B": 12, "B/F0": 180},
        )
        self.assertEqual(
            self.result["active_mask_histogram"],
            {"1": 64, "2": 64, "4": 64},
        )
        self.assertEqual(
            self.result["weight_histogram"],
            {"0,0,1": 64, "0,1,0": 64, "1,0,0": 64},
        )
        self.assertEqual(
            self.result["failure_count_per_pair_histogram"],
            {"1": 12, "3": 60},
        )
        for pair, descriptor in gap.feasible_corrected_cut_failures():
            self.assertIn(
                gap.category_pair(pair, descriptor),
                (("B", "B"), ("B", "F0")),
            )

    def test_secondary_support_diagnostics(self) -> None:
        self.assertEqual(
            self.result["cap_histogram"],
            {
                "0,0,2": 24,
                "0,1,2": 10,
                "0,2,0": 24,
                "0,2,1": 10,
                "0,2,2": 20,
                "1,0,2": 10,
                "1,2,0": 10,
                "2,0,0": 24,
                "2,0,1": 10,
                "2,0,2": 20,
                "2,1,0": 10,
                "2,2,0": 20,
            },
        )
        self.assertEqual(
            self.result["full_deficiency_histogram"],
            {"0": 174, "1": 192, "2": 60, "3": 6},
        )
        self.assertEqual(self.result["strictly_positive_invariant_pairs"], 0)

    def test_exact_invariant_geometry_and_failure_alignment(self) -> None:
        self.assertEqual(
            self.result["stoichiometric_rank_histogram"],
            {"2": 432},
        )
        self.assertEqual(
            self.result["invariant_zero_coordinate_histogram"],
            {"0": 144, "1": 144, "2": 144},
        )
        self.assertEqual(
            self.result["failure_zero_active_alignment_histogram"],
            {
                "zero=0,active=0": 64,
                "zero=1,active=1": 64,
                "zero=2,active=2": 64,
            },
        )
        self.assertTrue(
            self.result["all_failure_active_coordinates_equal_invariant_zero"]
        )
        self.assertEqual(
            self.result["invariant_manifest_sha256"],
            gap.EXPECTED_INVARIANT_MANIFEST_SHA256,
        )
        self.assertEqual(
            self.result["aligned_failure_row_sha256"],
            gap.EXPECTED_ALIGNED_FAILURE_ROW_SHA256,
        )
        for pair in gap.exclusive_orbit_gap_pairs():
            invariant = gap.primitive_invariant(pair)
            self.assertEqual(sum(value == 0 for value in invariant), 1)
            self.assertEqual(sum(value > 0 for value in invariant), 2)

    def test_non_dz_failed_pairs_are_exactly_two_symmetry_orbits(self) -> None:
        self.assertEqual(self.result["non_deficiency_zero_failed_pairs"], 24)
        self.assertEqual(
            self.result["non_deficiency_zero_failed_pair_sha256"],
            gap.EXPECTED_NON_DZ_FAILED_PAIR_SHA256,
        )
        self.assertEqual(
            self.result["non_deficiency_zero_failed_orbit_split"],
            {
                "type_I": {
                    "representative": (("A", "AB"), ("2A", "2C", "AC")),
                    "pairs": 12,
                    "sha256": gap.EXPECTED_TYPE_I_ORBIT_SHA256,
                },
                "type_II": {
                    "representative": (("A", "AB"), ("C", "2A", "BC")),
                    "pairs": 12,
                    "sha256": gap.EXPECTED_TYPE_II_ORBIT_SHA256,
                },
            },
        )

    def test_failure_manifest_and_claim_scope_are_frozen(self) -> None:
        self.assertEqual(len(self.result["failure_rows"]), 192)
        self.assertEqual(
            self.result["failure_row_sha256"],
            gap.EXPECTED_FAILURE_ROW_SHA256,
        )
        self.assertEqual(
            self.result["failure_row_sha256"],
            "cad3bdf8e900cbb6f978e11d30e28bba7a7a57de055d9b9787f7dd53fbc91615",
        )
        self.assertEqual(
            self.result["annotated_failure_row_sha256"],
            gap.EXPECTED_ANNOTATED_FAILURE_ROW_SHA256,
        )
        self.assertFalse(self.result["recurrence_claim"])
        self.assertFalse(
            self.result["orientation_rate_population_or_history_enumeration"]
        )


if __name__ == "__main__":
    unittest.main()
