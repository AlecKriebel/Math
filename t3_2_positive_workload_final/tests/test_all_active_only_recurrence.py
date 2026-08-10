from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import all_active_only_recurrence as branch


class AllActiveOnlyRecurrenceCertificate(unittest.TestCase):
    def test_exact_branch_count_and_hash(self) -> None:
        result = branch.certificate()
        self.assertEqual(result["support_pairs"], 51)
        self.assertEqual(result["positive_pairs"], 51)
        self.assertEqual(result["signed_pairs"], 0)
        self.assertEqual(result["failed_incidences"], 209)
        self.assertEqual(result["pair_sha256"], branch.EXPECTED_PAIR_SHA256)

    def test_claim_boundary(self) -> None:
        result = branch.certificate()
        self.assertTrue(result["analytic_theorem_certified"])
        self.assertFalse(result["global_t3_2_certified"])

    def test_analytic_premises_are_frozen(self) -> None:
        result = branch.certificate()
        self.assertTrue(
            result["all_failed_incidences_are_certified_all_active_incidences"]
        )
        self.assertTrue(result["all_failed_incidences_use_the_fixed_whole_top"])
        self.assertTrue(result["all_boundary_descriptors_pass_the_tier_condition"])


if __name__ == "__main__":
    unittest.main()
