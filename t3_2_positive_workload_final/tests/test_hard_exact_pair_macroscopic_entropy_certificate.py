from __future__ import annotations

import unittest

import hard_exact_pair_macroscopic_entropy_certificate as theorem


class HardExactPairMacroscopicPremises(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = theorem.certificate()

    def test_exact_scope(self) -> None:
        self.assertEqual(self.result["exact_normalized_ratio_support_rows"], 19)
        self.assertEqual(
            self.result["ratio_histogram"],
            {"1:2": 1, "1:3": 17, "4:5": 1},
        )

    def test_entropy_maximizers(self) -> None:
        self.assertEqual(
            self.result["maximizer_histogram"],
            {"0|UI": 1, "2U": 10, "U": 8},
        )
        self.assertTrue(self.result["every_maximizer_set_proper"])
        self.assertGreaterEqual(self.result["minimum_maximum_phi"], 0)
        self.assertGreaterEqual(
            self.result["minimum_primitive_interruption_gap"], 1
        )

    def test_frozen_hashes(self) -> None:
        self.assertEqual(
            self.result["rows_sha256"], theorem.EXPECTED_ROWS_SHA256
        )
        self.assertEqual(
            self.result["payload_sha256"], theorem.EXPECTED_PAYLOAD_SHA256
        )

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["analytic_theorem_certified"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
