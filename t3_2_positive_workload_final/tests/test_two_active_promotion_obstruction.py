from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import two_active_promotion_obstruction as obstruction


class TwoActivePromotionObstructionCertificate(unittest.TestCase):
    def test_suppressed_carrier_orbit(self) -> None:
        result = obstruction.certificate()
        self.assertEqual(result["suppressed_no_whole_incidences"], 4)
        self.assertEqual(result["suppressed_no_whole_pairs"], 4)
        self.assertEqual(
            result["suppressed_rows_sha256"],
            obstruction.EXPECTED_SUPPRESSED_SHA256,
        )
        self.assertTrue(
            all(
                row["isolated_block_weight_reward"] == 3
                for row in result["suppressed_rows"]
            )
        )

    def test_disjoint_pair_level_selector(self) -> None:
        result = obstruction.certificate()
        self.assertEqual(result["selector_pairs"], 36)
        self.assertEqual(result["selector_positive_pairs"], 32)
        self.assertEqual(result["selector_signed_pairs"], 4)
        self.assertEqual(
            result["selector_category_histogram"],
            {
                "promotion_dormant_top": 16,
                "promotion_enabled_top_seed": 20,
            },
        )
        self.assertEqual(
            result["selector_whole_top_histogram"],
            {"no_whole_top": 8, "with_whole_top": 28},
        )
        self.assertEqual(
            result["selector_seeded_whole_support_histogram"],
            {"A,BC": 6, "B,AC": 6, "none": 8},
        )
        self.assertEqual(
            result["selector_dormant_whole_support_histogram"],
            {"A,B": 5, "B,2A": 11},
        )
        self.assertEqual(
            result["selector_dormant_enabled_source_histogram"],
            {"0": 7, "0,A": 4, "A": 3, "none": 2},
        )
        self.assertEqual(
            result["selector_dormant_disabled_finite_class_incidences"], 2
        )
        self.assertEqual(
            result["selector_dormant_priority_split"],
            {
                "unique_zero_source": 7,
                "active_A_source": 7,
                "disabled_finite_class": 2,
            },
        )
        self.assertTrue(result["each_selector_pair_has_one_feasible_failure"])
        self.assertEqual(result["ordered_prior_overlap"], 0)
        self.assertEqual(result["suppressed_regression_overlap"], 0)
        self.assertEqual(result["independent_audits_passed"], 2)
        self.assertTrue(result["analytic_promotion_theorem_certified"])
        self.assertTrue(result["pair_level_recurrence_certified"])
        self.assertFalse(result["global_t3_2_certified"])
        self.assertEqual(
            (
                result["positive_remainder_before"],
                result["positive_remainder_after"],
                result["signed_remainder_before"],
                result["signed_remainder_after"],
            ),
            (1871, 1839, 191, 187),
        )


if __name__ == "__main__":
    unittest.main()
