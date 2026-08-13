from __future__ import annotations

import unittest

import hard_physical188_common_w as theorem


class HardPhysical188CommonW(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = theorem.certificate()

    def test_partition(self) -> None:
        self.assertEqual(self.result["normalized_templates"], 188)
        self.assertEqual(
            self.result["partition"],
            {
                "exact_carrier": 19,
                "nonexact_mixed": 145,
                "nonexact_no_history": 16,
                "nonexact_separated": 8,
            },
        )

    def test_ratios(self) -> None:
        self.assertEqual(
            self.result["ratio_histogram"],
            {"1:2": 17, "1:3": 154, "4:5": 17},
        )

    def test_hashes(self) -> None:
        self.assertEqual(self.result["rows_sha256"], theorem.EXPECTED_ROWS_SHA256)
        self.assertEqual(
            self.result["payload_sha256"], theorem.EXPECTED_PAYLOAD_SHA256
        )

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["physical188_composition_independently_audited"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
