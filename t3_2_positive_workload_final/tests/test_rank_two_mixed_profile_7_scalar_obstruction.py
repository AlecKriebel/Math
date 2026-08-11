from __future__ import annotations

import unittest

import rank_two_mixed_profile_7_scalar_obstruction as obstruction


class RankTwoMixedProfile7ScalarObstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = obstruction.certificate()

    def test_every_pair_has_a_zero_cap_axis(self) -> None:
        self.assertEqual(self.result["selector"]["pairs"], 7)
        self.assertEqual(self.result["selector"]["zero_cap_axis_rows"], 8)
        self.assertEqual(
            len({str(row["pair"]) for row in obstruction.dormant_axis_rows()}),
            7,
        )

    def test_only_birth_is_enabled(self) -> None:
        for row in obstruction.dormant_axis_rows():
            self.assertEqual(row["enabled_reactions"], ["0->A"])
            self.assertEqual(row["delta_uncorrected_factorial"], 0)
            self.assertEqual(row["delta_W"], 0)
            self.assertEqual(row["delta_H"], 1)

    def test_exact_positive_generator_formula(self) -> None:
        self.assertEqual(
            self.result["obstruction"]["axis_generator"],
            "L V=kappa_0A*(phi(n+1)-phi(n))>0",
        )

    def test_claim_flags_false(self) -> None:
        self.assertFalse(self.result["recurrence_obstruction_claimed"])
        self.assertFalse(
            self.result["candidate_7_pair_recurrence_certified"]
        )
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
