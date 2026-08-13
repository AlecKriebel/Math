from __future__ import annotations

import unittest

import hard_nonexact169_corollary_certificate as theorem


class HardNonexact169Premises(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = theorem.certificate()

    def test_scope(self) -> None:
        self.assertEqual(self.result["nonexact_rows"], 169)
        self.assertEqual(
            self.result["category_histogram"],
            {"mixed": 145, "no_history": 16, "separated": 8},
        )

    def test_gap(self) -> None:
        self.assertGreaterEqual(self.result["minimum_fast_gap"], 1)
        self.assertEqual(self.result["fast_gap_histogram"], {1: 153, 2: 16})

    def test_hashes(self) -> None:
        self.assertEqual(self.result["rows_sha256"], theorem.EXPECTED_ROWS_SHA256)
        self.assertEqual(
            self.result["payload_sha256"], theorem.EXPECTED_PAYLOAD_SHA256
        )

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["corollary_independently_audited"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
