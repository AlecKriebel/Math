from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import rank_one_carrier_certificate as certificate


class RankOneCarrierCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = certificate.certificate()

    def test_exact_incidence_partition(self):
        self.assertEqual(
            (
                self.result["rank_one_incidences"],
                self.result["seeded_incidences"],
                self.result["top_activation_incidences"],
                self.result["lower_activation_incidences"],
                self.result["finite_zero_boundary_incidences"],
            ),
            (930, 893, 2, 25, 10),
        )
        self.assertEqual(self.result["multichannel_direct_coverage"], 895)
        self.assertEqual(self.result["candidate_activation_coverage"], 25)

    def test_maximal_lower_layer_is_a_strict_weight_one_layer(self):
        self.assertTrue(self.result["all_maximal_lower_tiers_proper"])
        self.assertTrue(self.result["all_maximal_lower_weights_one"])

    def test_activation_templates_used_by_the_analytic_note(self):
        self.assertEqual(
            self.result["lower_activation_top_support_histogram"],
            {
                "2A,2B": 5,
                "2A,2B,AB": 9,
                "2A,AB": 5,
                "2B,AB": 5,
                "B,2A": 1,
            },
        )
        self.assertTrue(
            self.result[
                "top_activation_has_quadratic_top_source_and_only_weight_zero_lower_competitors"
            ]
        )

    def test_local_endpoint_scope_is_separate_from_recurrence(self):
        self.assertFalse(self.result["analytic_theorem_certified"])
        self.assertTrue(
            self.result["corrected_factorial_local_endpoint_certified"]
        )
        self.assertFalse(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])

    def test_frozen_dormant_geometry_hash(self):
        self.assertEqual(
            self.result["dormant_geometry_sha256"],
            "e645359a8ec1432f7093a703bccf4f309601d86ee5600582803677262f5ad5b2",
        )


if __name__ == "__main__":
    unittest.main()
