from __future__ import annotations

import unittest

import hard_enabled181_access_word as theorem


class HardEnabled181AccessWord(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = theorem.certificate()

    def test_scope(self) -> None:
        self.assertEqual(self.result["incidences"], 181)
        self.assertEqual(self.result["pairs"], 139)

    def test_audited_parent_membership(self) -> None:
        self.assertTrue(self.result["all_rows_are_members_of_audited_seeded_929"])
        self.assertTrue(self.result["arbitrary_fixed_ell"])

    def test_hashes(self) -> None:
        self.assertEqual(self.result["rows_sha256"], theorem.EXPECTED_ROWS_SHA256)
        self.assertEqual(self.result["payload_sha256"], theorem.EXPECTED_PAYLOAD_SHA256)

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["enabled181_corollary_independently_audited"])
        self.assertFalse(self.result["pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
