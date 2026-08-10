from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import rank_one_no_promotion_branch as branch


class RankOneNoPromotionBranchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = branch.certificate()

    def test_exact_local_partition(self):
        self.assertEqual(self.result["rank_one_pairs"], 310)
        self.assertEqual(self.result["rank_one_pairs_with_promotion"], 77)
        self.assertEqual(self.result["no_promotion_local_pairs"], 233)
        self.assertEqual(
            self.result["local_all_active_branch_histogram"],
            {
                "directed_triple_factorial_linear": 67,
                "no_all_active_failure": 12,
                "safe_reversible_rate_adjusted": 154,
            },
        )
        self.assertTrue(
            self.result[
                "dimension_at_least_two_common_potential_certified"
            ]
        )

    def test_one_active_boundary_is_not_silently_promoted(self):
        self.assertEqual(
            self.result["feasible_failure_active_count_histogram"],
            {"1,2,3": 92, "2": 12, "2,3": 129},
        )
        self.assertEqual(self.result["pairs_with_one_active_obstruction"], 92)
        self.assertEqual(
            self.result["candidate_pair_level_composable_pairs"], 141
        )
        self.assertEqual(self.result["pair_level_recurrent_pairs"], 141)
        self.assertEqual(
            self.result["candidate_all_active_branch_histogram"],
            {
                "directed_triple_factorial_linear": 57,
                "no_all_active_failure": 12,
                "safe_reversible_rate_adjusted": 72,
            },
        )
        self.assertTrue(self.result["pair_level_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])
        self.assertEqual(
            self.result["ordered_prior_overlap"],
            {
                "affine_151": 0,
                "rank_two_14": 0,
                "all_active_only_51": 0,
                "h_b_seam_12": 0,
            },
        )
        self.assertEqual(
            (
                self.result["positive_remainder_before"],
                self.result["positive_remainder_after"],
                self.result["signed_remainder_before"],
                self.result["signed_remainder_after"],
            ),
            (2104, 1963, 191, 191),
        )

    def test_exact_hashes(self):
        self.assertEqual(
            self.result["local_pair_sha256"],
            branch.EXPECTED_LOCAL_PAIR_SHA256,
        )
        self.assertEqual(
            self.result["candidate_pair_sha256"],
            branch.EXPECTED_CANDIDATE_PAIR_SHA256,
        )
        self.assertEqual(
            self.result["rows_sha256"],
            branch.EXPECTED_ROWS_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
