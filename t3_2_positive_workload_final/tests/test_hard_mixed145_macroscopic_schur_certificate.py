from __future__ import annotations

import unittest

import hard_mixed145_macroscopic_schur_certificate as theorem


class HardMixed145Premises(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = theorem.certificate()

    def test_scope(self) -> None:
        self.assertEqual(self.result["normalized_ratio_support_rows"], 145)
        self.assertEqual(
            self.result["ratio_histogram"],
            {"1:2": 13, "1:3": 119, "4:5": 13},
        )

    def test_gaps(self) -> None:
        self.assertEqual(
            self.result["maximum_base_degree_histogram"], {1: 39, 2: 106}
        )
        self.assertEqual(self.result["fast_gap_histogram"], {1: 132, 2: 13})
        self.assertGreaterEqual(self.result["minimum_fast_gap"], 1)

    def test_frozen_hashes(self) -> None:
        self.assertEqual(self.result["rows_sha256"], theorem.EXPECTED_ROWS_SHA256)
        self.assertEqual(
            self.result["payload_sha256"], theorem.EXPECTED_PAYLOAD_SHA256
        )

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["analytic_theorem_certified"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
