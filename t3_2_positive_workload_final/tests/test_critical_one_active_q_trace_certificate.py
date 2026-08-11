from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import critical_one_active_q_trace_certificate as critical


class CriticalOneActiveQTraceCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = critical.certificate()

    def test_exact_pair_scope_and_disjointness(self) -> None:
        self.assertEqual(self.result["pairs"], 15)
        self.assertEqual(self.result["positive_pairs"], 15)
        self.assertEqual(self.result["signed_pairs"], 0)
        self.assertEqual(self.result["prior_certified_overlap"], 0)
        self.assertEqual(self.result["pair_sha256"], critical.EXPECTED_PAIR_SHA256)

    def test_exact_failure_split(self) -> None:
        self.assertEqual(self.result["failed_incidences"], 83)
        self.assertEqual(self.result["critical_q_incidences"], 75)
        self.assertEqual(self.result["companion_incidences"], 8)
        self.assertEqual(
            sorted(self.result["companion_template_histogram"].values()),
            [2, 2, 2, 2],
        )
        self.assertEqual(self.result["rows_sha256"], critical.EXPECTED_ROWS_SHA256)

    def test_certified_claim_boundary(self) -> None:
        self.assertEqual(self.result["independent_audits_passed"], 2)
        self.assertTrue(self.result["analytic_critical_trace_certified"])
        self.assertTrue(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])
        self.assertEqual(
            (
                self.result["positive_remainder_before"],
                self.result["positive_remainder_after"],
                self.result["signed_remainder"],
            ),
            (1835, 1820, 187),
        )


if __name__ == "__main__":
    unittest.main()
