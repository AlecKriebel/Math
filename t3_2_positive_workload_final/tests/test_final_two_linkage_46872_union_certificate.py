import unittest

import final_two_linkage_46872_union_certificate as target
import outside_mixed_remaining_18496_certificate as remainder


class FinalTwoLinkage46872UnionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = target.certificate()

    def test_dependency_bytes_are_exact(self) -> None:
        self.assertEqual(
            self.result["dependency_sha256"],
            target.EXPECTED_DEPENDENCY_SHA256,
        )

    def test_exact_universe(self) -> None:
        self.assertEqual(self.result["ordered_disjoint_support_pairs"], 46_872)
        self.assertEqual(
            self.result["universe_sha256"],
            target.EXPECTED_UNIVERSE_SHA256,
        )
        self.assertEqual(self.result["mixed_orbit_pairs"], 27_894)
        self.assertEqual(self.result["outside_mixed_pairs"], 18_978)

    def test_five_disjoint_branches(self) -> None:
        self.assertEqual(
            self.result["branch_manifest"],
            [
                {
                    "branch": "other_mixed_orbit",
                    "pairs": 27_462,
                    "sha256": target.EXPECTED_OTHER_MIXED_ORBIT_SHA256,
                },
                {
                    "branch": "active_orbit_gap",
                    "pairs": 432,
                    "sha256": target.EXPECTED_ACTIVE_ORBIT_GAP_SHA256,
                },
                {
                    "branch": "strict_positive_invariant",
                    "pairs": 146,
                    "sha256": target.EXPECTED_STRICT_INVARIANT_SHA256,
                },
                {
                    "branch": "levelset_residual",
                    "pairs": 336,
                    "sha256": target.EXPECTED_LEVELSET_SHA256,
                },
                {
                    "branch": "outside_mixed_remainder",
                    "pairs": 18_496,
                    "sha256": target.EXPECTED_REMAINDER_SHA256,
                },
            ],
        )
        self.assertTrue(self.result["pairwise_disjoint"])
        self.assertTrue(self.result["union_equals_universe"])
        self.assertEqual(
            self.result["branch_manifest_sha256"],
            target.EXPECTED_BRANCH_MANIFEST_SHA256,
        )

    def test_remainder_split(self) -> None:
        self.assertEqual(
            self.result["outside_mixed_remainder_split"],
            {
                "no_failure": 11_842,
                "failure": 6_654,
                "no_failure_sha256": remainder.EXPECTED_NO_FAILURE_PAIR_SHA256,
                "failure_sha256": remainder.EXPECTED_FAILED_PAIR_SHA256,
            },
        )

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["recurrence_claim"])
        self.assertFalse(
            self.result["orientation_rate_population_or_history_enumeration"]
        )


if __name__ == "__main__":
    unittest.main()
