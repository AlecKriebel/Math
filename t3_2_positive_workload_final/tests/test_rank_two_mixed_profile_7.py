from __future__ import annotations

from collections import Counter
import unittest

import rank_two_mixed_profile_7 as branch


class RankTwoMixedProfile7Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = branch.certificate()

    def test_exact_selector(self) -> None:
        self.assertEqual(
            self.result["selector"],
            {
                "pairs": 7,
                "pair_sha256": branch.EXPECTED_PAIR_SHA256,
                "one_active_incidences": 40,
                "two_active_incidences": 0,
                "all_active_incidences": 7,
                "failed_active_profile": [1, 3],
            },
        )

    def test_exact_normalized_menus(self) -> None:
        rows = branch.one_active_rows()
        self.assertEqual(
            Counter(",".join(row["normalized_supports"][1]) for row in rows),
            {
                "2A,2B,AB,AC,BC": 10,
                "2A,2B,AC,BC": 10,
                "2A,AB,AC,BC": 10,
                "2B,AB,AC,BC": 10,
            },
        )
        self.assertTrue(
            all(row["lower_birth_death_support"] == ["0", "A"] for row in rows)
        )
        self.assertTrue(
            all(set(row["carrier_nodes"]) == {"AC", "BC"} for row in rows)
        )

    def test_family_i_origin_route(self) -> None:
        self.assertTrue(
            all(
                row["graph_category"] == "family_i_origin_down_0"
                for row in branch.one_active_rows()
            )
        )

    def test_pf_cut_premise(self) -> None:
        premise = self.result["orientation_independent_pf_premise"]
        self.assertTrue(premise["killed_carrier_generator_is_transient"])
        self.assertEqual(
            premise["candidate_generator_bound"],
            "L_top R >= c*X*R-K*R^2",
        )

    def test_claim_neutral_arithmetic(self) -> None:
        arithmetic = self.result["pair_arithmetic"]
        self.assertEqual(
            (
                arithmetic["claim_neutral_remainder_after_7"]["positive"],
                arithmetic["claim_neutral_remainder_after_7"]["signed"],
                arithmetic["claim_neutral_remainder_after_7"]["total"],
            ),
            (713, 36, 749),
        )

    def test_all_claim_flags_false(self) -> None:
        self.assertFalse(
            self.result["analytic_stopped_wedge_independently_certified"]
        )
        self.assertFalse(self.result["interior_service_access_certified"])
        self.assertFalse(self.result["candidate_7_pair_recurrence_certified"])
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
