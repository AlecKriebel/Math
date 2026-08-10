import unittest

import global_atlas_interface_closure as closure


class GlobalAtlasInterfaceClosureTests(unittest.TestCase):
    def test_global_branch_counts_are_exact(self):
        result = closure.certificate()

        self.assertEqual(result["positive"]["chart_instances"], 11070)
        self.assertEqual(result["positive"]["unique_ordered_support_pairs"], 4761)
        self.assertEqual(
            result["positive"]["branch_counts"],
            {
                "common_active_invariant": 110,
                "exact_seven_support_seam": 6,
                "exact_signed_service_seam": 2,
                "exact_residual_pair": 1,
                "finite_strict_invariant": 187,
                "full_deficiency_zero": 924,
                "residual": 3531,
            },
        )

        self.assertEqual(result["signed_service_geometric_pairs"], 5)
        self.assertEqual(result["signed_service_deficiency_zero_overlap"], 3)
        self.assertEqual(result["signed_service_new_positive_table_pairs"], 2)
        self.assertEqual(result["signed_service_pairs_in_signed_available_table"], 0)
        self.assertEqual(result["exact_residual_pair_new_positive_table_pairs"], 1)
        self.assertEqual(result["exact_residual_pair_pairs_in_signed_available_table"], 0)
        self.assertEqual(result["signed"]["chart_instances"], 645)
        self.assertEqual(result["signed"]["unique_ordered_support_pairs"], 408)
        self.assertEqual(
            result["signed"]["branch_counts"],
            {
                "full_deficiency_zero": 50,
                "residual": 358,
            },
        )

    def test_second_deficiency_one_family_is_exact(self):
        result = closure.verify_second_family()

        self.assertEqual(result["workload"], [1, 1, 0])
        self.assertEqual(result["compatible_available_supports"], 49)
        self.assertEqual(result["minimal_available_supports"], 9)
        self.assertEqual(result["tier_certified_supersets"], 12)
        self.assertEqual(result["remaining_after_tier_lemma"], 37)

    def test_second_family_rank_and_deficiency_formula(self):
        for available in closure.second_family_supports():
            rows = closure.full_rows(closure.SECOND_SHIELDED_MASK, available)
            self.assertEqual(len(rows), 3)
            self.assertEqual(
                closure.full_deficiency(closure.SECOND_SHIELDED_MASK, available),
                available.bit_count() - 1,
            )
            self.assertFalse(
                closure.has_positive_active_invariant(
                    closure.SECOND_SHIELDED_MASK,
                    available,
                )
            )

    def test_tier_subfamily_has_the_claimed_support_geometry(self):
        certified = closure.second_family_tier_certified_supports()
        self.assertEqual(len(certified), 12)
        for available in certified:
            names = set(closure.support(available))
            self.assertTrue({"2A", "2B"}.issubset(names))
            self.assertTrue({"C", "2C"}.intersection(names))

        self.assertTrue(
            certified.isdisjoint(closure.second_family_minimal_supports())
        )


if __name__ == "__main__":
    unittest.main()
