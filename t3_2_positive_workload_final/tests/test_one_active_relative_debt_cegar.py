import unittest

import one_active_relative_debt_cegar as cegar


class FamilyIIAxisCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = cegar.family_ii_axis_certificate()

    def test_exact_scope(self):
        self.assertEqual(self.result["incidences"], 30)
        self.assertEqual(self.result["physical_pairs"], 10)
        self.assertEqual(self.result["normalized_profiles"], 15)
        self.assertEqual(self.result["normalized_support_types"], 5)

    def test_cap_two_is_an_availability_category(self):
        self.assertEqual(
            [cegar.normalized_spectator_cap(value) for value in (0, 1, 2, 3, 17)],
            [0, 1, 2, 2, 2],
        )
        with self.assertRaises(ValueError):
            cegar.normalized_spectator_cap(-1)

    def test_frozen_fingerprints(self):
        self.assertEqual(
            self.result["rows_sha256"], cegar.FAMILY_II_ROWS_SHA256
        )
        self.assertEqual(
            self.result["pairs_sha256"], cegar.FAMILY_II_PAIRS_SHA256
        )

    def test_exact_resistance_claim(self):
        self.assertTrue(self.result["spectator_is_linkage_invariant"])
        self.assertEqual(
            self.result["normalized_cap_semantics"],
            "cap 0 means a_Gamma=0; cap 1 means a_Gamma=1; "
            "cap 2 means arbitrary fixed a_Gamma>=2",
        )
        self.assertEqual(
            self.result["arbitrary_strong_orientation_relative_down_depth"],
            0,
        )
        self.assertEqual(
            self.result[
                "arbitrary_strong_orientation_relative_up_depth_lower_bound"
            ],
            1,
        )
        self.assertTrue(self.result["graph_resistance_lemma_certified"])

    def test_claim_boundary(self):
        self.assertFalse(self.result["aggregate_kernel_certified"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


class FullGraphArchitectureCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = cegar.graph_architecture_certificate()

    def test_exact_architecture_partition(self):
        self.assertEqual(self.result["candidate_pairs"], 1227)
        self.assertEqual(self.result["candidate_incidences"], 3297)
        self.assertEqual(
            self.result["category_histogram"],
            {
                "family_i_origin_down_0": 710,
                "family_i_origin_down_1": 75,
                "family_i_origin_no_history": 185,
                "family_ii_axis_down_0": 24,
                "family_ii_axis_no_history": 6,
                "family_iii_origin_down_0": 234,
                "family_iii_origin_down_1": 40,
                "family_iii_origin_down_2": 16,
                "family_iii_origin_no_history": 90,
                "mixed_C_source_direct_down_0": 1695,
                "open_wholly_top_down_1": 210,
                "open_wholly_top_no_history": 12,
            },
        )
        self.assertEqual(
            self.result["rows_sha256"], cegar.ARCHITECTURE_ROWS_SHA256
        )

    def test_exact_graph_claim(self):
        self.assertEqual(self.result["relative_down_depth_upper_bound"], 2)
        self.assertTrue(
            self.result["same_base_up_depth_is_strictly_larger"]
        )
        self.assertTrue(
            self.result[
                "arbitrary_strong_orientation_graph_theorem_certified"
            ]
        )
        self.assertEqual(
            self.result["direct_C_phase_histogram"],
            {"lower_only_plus_mixed": 1030, "two_mixed": 665},
        )
        self.assertEqual(
            self.result["wholly_top_phase_histogram"],
            {"depth_one": 210, "no_history": 12},
        )
        self.assertEqual(
            self.result["wholly_top_normalized_support_types"],
            {"total": 37, "depth_one": 35, "no_history": 2},
        )
        self.assertEqual(
            self.result["finite_mixed_carrier_bound"],
            {
                "inactive_mass": "M_t <= M_0 + 3*K + 4",
                "family_ii_initial_mass": (
                    "M_0=a_Gamma is arbitrary but fixed on the class"
                ),
                "active_overshoot": "r_plus <= K + 1",
                "boundary_above_M0_plus_10_requires_interruptions": 3,
                "weighted_green_bound_certified": False,
            },
        )

    def test_population_bound_four_counterexample(self):
        row = self.result["population_five_counterexample"]
        self.assertFalse(row["population_bound_four_valid"])
        self.assertEqual(row["maximum_inactive_population"], 5)
        self.assertEqual(row["trace"][-1]["relative_reward"], -1)
        self.assertEqual(row["trace"][-1]["cost"], 2)

    def test_full_claim_boundary(self):
        self.assertFalse(self.result["aggregate_kernel_certified"])
        self.assertFalse(self.result["promotion_contract_certified"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
