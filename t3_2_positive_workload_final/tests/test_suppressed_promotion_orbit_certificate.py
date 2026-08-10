from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import suppressed_promotion_orbit_certificate as orbit


class SuppressedPromotionOrbitCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = orbit.certificate()

    def test_exact_orbit_and_disjointness(self) -> None:
        self.assertEqual(self.result["pairs"], 4)
        self.assertEqual(self.result["positive_pairs"], 4)
        self.assertEqual(self.result["signed_pairs"], 0)
        self.assertEqual(self.result["prior_certified_overlap"], 0)
        self.assertEqual(
            self.result["pair_sha256"], orbit.EXPECTED_PAIR_SHA256
        )

    def test_every_feasible_failure(self) -> None:
        self.assertEqual(self.result["failed_incidences"], 28)
        self.assertEqual(self.result["one_active_incidences"], 12)
        self.assertEqual(self.result["two_active_incidences"], 16)
        self.assertEqual(
            self.result["profile_histogram"],
            {
                "0,0,1": 12,
                "0,1,1": 4,
                "0,1,2": 4,
                "0,1,3": 4,
                "0,4,5": 4,
            },
        )
        self.assertEqual(
            self.result["one_active_cap_histogram"],
            {"0,0,2": 4, "0,1,2": 4, "0,2,2": 4},
        )
        self.assertEqual(self.result["whole_top_two_active_incidences"], 4)
        self.assertEqual(
            self.result["no_whole_top_two_active_incidences"], 12
        )
        self.assertTrue(self.result["all_inactive_i_caps_zero"])
        self.assertEqual(
            self.result["rows_sha256"], orbit.EXPECTED_ROWS_SHA256
        )

    def test_claim_boundary(self) -> None:
        self.assertEqual(self.result["independent_audits_passed"], 2)
        self.assertTrue(self.result["analytic_shell_theorem_certified"])
        self.assertTrue(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])
        self.assertEqual(
            (
                self.result["positive_remainder_before"],
                self.result["positive_remainder_after"],
                self.result["signed_remainder"],
            ),
            (1839, 1835, 187),
        )

    def test_cleaned_macro_reward_signs(self) -> None:
        self.assertEqual(
            self.result["macro_q_changes"],
            {
                "0->I": -1,
                "0->2I": -2,
                "0->I+U": 0,
                "I+U->0": 0,
                "I+U->I": -1,
                "I+U->2I": -2,
            },
        )
        rewards = self.result["macro_reward_coefficients"]
        for edge in ("0->I", "0->2I", "0->I+U"):
            self.assertLess(rewards["one_active_001"][edge], 0)
            self.assertLess(rewards["deep_v_013"][edge], 0)
        for edge in ("I+U->0", "I+U->I", "I+U->2I"):
            self.assertLess(rewards["equal_depth_011"][edge], 0)
            self.assertLess(rewards["deep_parallel_045"][edge], 0)
        self.assertEqual(
            rewards["critical_012"], self.result["macro_q_changes"]
        )


if __name__ == "__main__":
    unittest.main()
