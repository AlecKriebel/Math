from __future__ import annotations

import unittest

import global_t3_2_final_union as final_union


class GlobalT32FinalUnionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = final_union.certificate()

    def test_baseline_and_zero_remainder(self) -> None:
        self.assertEqual(
            self.result["baseline"],
            {
                "pairs": 2511,
                "positive": 2312,
                "signed": 199,
                "pair_sha256": self.result["baseline"]["pair_sha256"],
            },
        )
        self.assertTrue(self.result["pairwise_disjoint"])
        self.assertTrue(self.result["union_equals_baseline"])
        self.assertEqual(self.result["remaining_pairs"], 0)

    def test_late_branch_counts(self) -> None:
        branches = self.result["branches"]
        self.assertEqual(branches["universal_one_active_net_1212"]["pairs"], 1212)
        self.assertEqual(branches["exact_common_w_26"]["pairs"], 26)
        self.assertEqual(branches["easy_common_w_416"]["pairs"], 416)
        self.assertEqual(branches["rank_two_scalar_13"]["pairs"], 13)
        self.assertEqual(branches["rank_two_stopped_7"]["pairs"], 7)
        self.assertEqual(branches["hard_common_w_333"]["pairs"], 333)

    def test_hashes_and_claim_boundary(self) -> None:
        self.assertEqual(self.result["rows_sha256"], final_union.EXPECTED_ROWS_SHA256)
        self.assertEqual(
            self.result["payload_sha256"], final_union.EXPECTED_PAYLOAD_SHA256
        )
        self.assertFalse(self.result["hard333_pair_recurrence_input_certified"])
        self.assertFalse(self.result["global_t3_2_theorem_independently_audited"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
