import unittest

import outside_mixed_remaining_18496_certificate as certificate


class OutsideMixedRemaining18496CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = certificate.certificate()

    def test_exact_pair_pipeline(self) -> None:
        self.assertEqual(self.result["strict_invariant_residual_pairs"], 18_832)
        self.assertEqual(self.result["removed_levelset_pairs"], 336)
        self.assertEqual(self.result["remaining_pairs"], 18_496)
        self.assertEqual(self.result["pairs_with_no_failure"], 11_842)
        self.assertEqual(self.result["pairs_with_failure"], 6_654)

    def test_only_three_failure_profiles_remain(self) -> None:
        self.assertEqual(
            self.result["failure_profile_histogram"],
            {"AA": 3_084, "B/B": 3_618, "B/F0": 15_204},
        )
        self.assertEqual(
            self.result["failure_active_count_histogram"],
            {1: 18_822, 2: 3_084},
        )

    def test_two_active_rows_are_available_available(self) -> None:
        self.assertEqual(
            self.result["two_active_ordered_kind_histogram"],
            {
                "C/C": 72,
                "C/Q": 156,
                "C/U": 660,
                "Q/U": 1_200,
                "U/U": 996,
            },
        )

    def test_pair_level_profile_split(self) -> None:
        self.assertEqual(
            self.result["failed_pair_profile_set_histogram"],
            {
                "AA": 12,
                "AA+B/B+B/F0": 156,
                "AA+B/F0": 1_428,
                "B/B": 2_874,
                "B/B+B/F0": 366,
                "B/F0": 1_818,
            },
        )

    def test_no_dynamic_enumeration_or_recurrence_claim(self) -> None:
        self.assertFalse(
            self.result["orientation_rate_population_or_history_enumeration"]
        )
        self.assertFalse(self.result["recurrence_claim"])


if __name__ == "__main__":
    unittest.main()
