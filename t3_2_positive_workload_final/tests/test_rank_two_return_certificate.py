from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import rank_two_return_certificate as certificate


class RankTwoReturnCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = certificate.certificate()

    def test_exact_partition(self):
        self.assertEqual(
            (
                self.result["rank_two_incidences"],
                self.result["support_pairs"],
                self.result["lower_supports"],
                self.result["with_2c_supports"],
                self.result["ac_only_vertical_supports"],
                self.result["c_present_linear_phase_supports"],
                self.result["dormant_activation_supports"],
            ),
            (42, 14, 14, 10, 4, 3, 1),
        )

    def test_vertical_supports(self):
        supports = {tuple(row) for row in self.result["supports"]}
        for support in (
            ("0", "A", "AC"),
            ("0", "C", "AC"),
            ("A", "C", "AC"),
            ("0", "A", "C", "AC"),
        ):
            self.assertIn(support, supports)

    def test_independently_audited_scope_and_overlap_arithmetic(self):
        self.assertTrue(self.result["analytic_theorem_certified"])
        self.assertEqual(self.result["previous_exact_residual_overlap"], 0)
        self.assertEqual(self.result["new_positive_table_pairs"], 14)
        self.assertEqual(self.result["new_signed_table_pairs"], 0)
        self.assertEqual(
            (
                self.result["positive_remainder_before"],
                self.result["positive_remainder_after"],
                self.result["signed_remainder_before"],
                self.result["signed_remainder_after"],
            ),
            (2169, 2155, 191, 191),
        )

    def test_frozen_support_hash(self):
        self.assertEqual(
            self.result["support_sha256"],
            "ec552cc5f008cbb881c52dfc054d4ea1034357bebe525c6be06b389dd019540c",
        )


if __name__ == "__main__":
    unittest.main()
