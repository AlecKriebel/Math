import unittest

from one_active_kinetic_depth import certificate


class OneActiveKineticDepthTest(unittest.TestCase):
    def test_post_rank_one_hamiltonian_cycle_table(self) -> None:
        result = certificate()
        self.assertEqual(result["post_rank_one_pairs"], 92)
        self.assertEqual(result["one_active_incidences"], 272)
        self.assertEqual(result["normalized_profiles"], 12)
        self.assertEqual(
            result["structural_family_histogram"],
            {
                "inactive_quadratic_plus_mixed": 200,
                "reversible_mixed_kill_plus_mixed": 72,
            },
        )
        self.assertEqual(
            result["zero_contest_case_histogram"],
            {
                "direct_enabled_top": 230,
                "frozen_singleton_face": 10,
                "zero_source_seed_path": 32,
            },
        )
        self.assertEqual(result["hamiltonian_orientation_pairs"], 2660)
        self.assertEqual(
            result["creation_not_strictly_deeper_than_service"], []
        )
        self.assertTrue(result["zero_contest_support_dichotomy_certified"])
        self.assertTrue(result["arbitrary_strong_orientation_certified"])
        self.assertTrue(result["local_corrected_factorial_episode_certified"])
        self.assertTrue(result["pair_level_recurrence_certified"])
        self.assertTrue(result["analytic_recurrence_certified"])
        self.assertFalse(result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
