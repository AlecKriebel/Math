import unittest

import other_mixed_orbit_27462_certificate as target


class OtherMixedOrbit27462Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = target.certificate()

    def test_dependencies(self) -> None:
        self.assertEqual(
            self.result["dependency_sha256"],
            target.EXPECTED_DEPENDENCY_SHA256,
        )

    def test_seed_subtraction(self) -> None:
        self.assertEqual(self.result["inherited_seed_pairs"], 5_169)
        self.assertEqual(self.result["excluded_active_invariant_seeds"], 110)
        self.assertEqual(self.result["eligible_seed_pairs"], 5_059)
        self.assertEqual(
            self.result["eligible_seed_sha256"],
            target.EXPECTED_ELIGIBLE_SEED_SHA256,
        )

    def test_exact_seed_partition(self) -> None:
        self.assertEqual(
            [row["pairs"] for row in self.result["branch_manifest"]],
            [187, 974, 9, 1_378, 2_511],
        )
        self.assertTrue(self.result["eligible_seed_partition_exact"])
        self.assertEqual(
            self.result["branch_manifest_sha256"],
            target.EXPECTED_BRANCH_MANIFEST_SHA256,
        )

    def test_exact_orbit(self) -> None:
        self.assertEqual(self.result["other_mixed_orbit_pairs"], 27_462)
        self.assertEqual(
            self.result["other_mixed_orbit_sha256"],
            target.EXPECTED_OTHER_ORBIT_SHA256,
        )

    def test_claim_boundary(self) -> None:
        self.assertFalse(self.result["recurrence_claim"])
        self.assertFalse(
            self.result["orientation_rate_population_or_history_enumeration"]
        )


if __name__ == "__main__":
    unittest.main()
