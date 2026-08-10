from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import two_active_promotion_shape as shape


class TwoActivePromotionShapeCertificate(unittest.TestCase):
    def test_exact_partition(self) -> None:
        result = shape.certificate()
        self.assertEqual(result["promotion_incidences"], 1416)
        self.assertEqual(result["promotion_pairs"], 803)
        self.assertEqual(result["no_wholly_top_incidences"], 1366)
        self.assertEqual(result["wholly_top_incidences"], 50)
        self.assertEqual(result["finite_shell_incidences"], 42)
        self.assertEqual(result["poisson_phase_incidences"], 8)
        self.assertEqual(result["pair_overlap_between_modes"], 13)

    def test_hash_and_claim_boundary(self) -> None:
        result = shape.certificate()
        self.assertEqual(result["rows_sha256"], shape.EXPECTED_ROWS_SHA256)
        self.assertFalse(result["analytic_theorem_certified"])


if __name__ == "__main__":
    unittest.main()
