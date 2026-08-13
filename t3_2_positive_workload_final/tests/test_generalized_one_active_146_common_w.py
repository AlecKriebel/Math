from __future__ import annotations

import unittest

import generalized_one_active_146_common_w as theorem


class GeneralizedOneActive146Composition(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = theorem.certificate()

    def test_partition(self) -> None:
        self.assertEqual(self.result["support_templates"], 146)
        self.assertEqual(
            self.result["category_histogram"],
            {
                "exact_cloud": 17,
                "mixed_nonexact": 111,
                "no_history": 12,
                "separated": 6,
            },
        )

    def test_inputs(self) -> None:
        self.assertTrue(self.result["local_input_theorems_independently_audited"])

    def test_hashes(self) -> None:
        self.assertEqual(self.result["rows_sha256"], theorem.EXPECTED_ROWS_SHA256)
        self.assertEqual(
            self.result["payload_sha256"], theorem.EXPECTED_PAYLOAD_SHA256
        )

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["composition_theorem_independently_audited"])
        self.assertFalse(self.result["generalized_146_common_w_certified"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
