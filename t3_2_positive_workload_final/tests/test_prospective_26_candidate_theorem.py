from __future__ import annotations

from collections import Counter
import unittest

import prospective_26_candidate_theorem as candidate


class CandidateCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = candidate.certificate()

    def test_selector_counts_and_hash(self) -> None:
        self.assertEqual(
            self.result["selector"],
            {
                "pairs": 26,
                "pair_sha256": (
                    "393474671be0bf095868e66cbcbf3164d941b99191517f172a41f157e20b21af"
                ),
                "one_active_incidences": 30,
                "two_active_incidences": 0,
                "all_active_incidences": 94,
            },
        )

    def test_exact_one_active_partition(self) -> None:
        rows = candidate.one_active_rows()
        self.assertEqual(
            Counter(row["graph_category"] for row in rows),
            {
                "mixed_C_source_direct_down_0": 20,
                "family_iii_origin_down_0": 8,
                "family_iii_origin_no_history": 2,
            },
        )
        self.assertEqual(len(candidate.normalized_profiles()), 15)
        self.assertTrue(all(row["normalized_caps"] == [0, 0] for row in rows))

    def test_claim_neutral_pair_arithmetic_and_disjointness(self) -> None:
        self.assertEqual(
            self.result["prospective_pair_arithmetic"],
            {
                "authoritative_prospective_parent": {
                    "positive": 759,
                    "signed": 36,
                    "total": 795,
                    "pair_sha256": (
                        "6a1327e6c38bfcab30d334691415ba457e84d45d1dfe53d81df4c02aad868123"
                    ),
                },
                "selected_candidate": {
                    "positive": 26,
                    "signed": 0,
                    "total": 26,
                    "pair_sha256": (
                        "393474671be0bf095868e66cbcbf3164d941b99191517f172a41f157e20b21af"
                    ),
                    "subset_of_parent": True,
                    "prior_certified_overlap": 0,
                },
                "claim_neutral_remainder_after_candidate": {
                    "positive": 733,
                    "signed": 36,
                    "total": 769,
                    "pair_sha256": candidate.EXPECTED_AFTER_769_SHA256,
                },
            },
        )

    def test_direct_rows_have_the_physical_active_source(self) -> None:
        rows = (
            row
            for row in candidate.one_active_rows()
            if row["graph_category"]
            == "mixed_C_source_direct_down_0"
        )
        self.assertTrue(
            all(row["direct_active_source_linkage_sides"] for row in rows)
        )

    def test_family_iii_rows_have_exact_origin_dichotomy(self) -> None:
        rows = candidate.one_active_rows()
        down = tuple(
            row
            for row in rows
            if row["graph_category"] == "family_iii_origin_down_0"
        )
        no_history = tuple(
            row
            for row in rows
            if row["graph_category"] == "family_iii_origin_no_history"
        )
        self.assertTrue(
            all(
                any(
                    "0" in lower and len(lower) > 1
                    for lower in row["lower_supports"]
                )
                for row in down
            )
        )
        self.assertTrue(
            all(
                all("0" not in lower for lower in row["lower_supports"])
                for row in no_history
            )
        )

    def test_all_active_cofactor_premise(self) -> None:
        rows = candidate.all_active_rows()
        self.assertEqual(
            Counter(",".join(row["top_support"]) for row in rows),
            {"2A,BC": 40, "AC,BC": 54},
        )
        self.assertTrue(all(row["direct_entropy_safe"] for row in rows))
        self.assertTrue(
            all(
                cofactor["at_or_below_lower_maximum"]
                for row in rows
                for cofactor in row["curvature_cofactors"]
            )
        )

    def test_fixed_pair_top_and_rate_adjustment(self) -> None:
        tops = candidate.pair_tops()
        self.assertEqual(len(tops), 26)
        self.assertTrue(all(len(row["top_support"]) == 2 for row in tops))
        self.assertEqual(
            {tuple(row["canonical_top_reaction_vector"]) for row in tops},
            {(-2, 1, 1), (-1, 1, 0)},
        )
        self.assertTrue(
            all(
                row["rate_adjustment_constraint"]
                == "ell_dot_(z-y)=-log(kappa_yz/kappa_zy)"
                for row in tops
            )
        )

    def test_discrete_endpoint_identity(self) -> None:
        samples = candidate.discrete_endpoint_identity_samples()
        self.assertEqual(len(samples), 4)
        self.assertTrue(all(row["identity_holds"] for row in samples))

    def test_frozen_hashes(self) -> None:
        self.assertEqual(
            self.result["hashes"],
            {
                "one_active_rows_sha256": candidate.EXPECTED_ONE_ROWS_SHA256,
                "normalized_profiles_sha256": (
                    candidate.EXPECTED_NORMALIZED_PROFILES_SHA256
                ),
                "all_active_rows_sha256": (
                    candidate.EXPECTED_ALL_ACTIVE_ROWS_SHA256
                ),
                "pair_tops_sha256": candidate.EXPECTED_PAIR_TOPS_SHA256,
            },
        )
        self.assertEqual(
            self.result["payload_sha256"], candidate.EXPECTED_PAYLOAD_SHA256
        )

    def test_scoped_flags_promoted_but_global_remains_false(self) -> None:
        self.assertEqual(self.result["independent_audit_verdict"], "PASS")
        self.assertTrue(
            self.result[
                "analytic_one_active_scope_extension_certified"
            ]
        )
        self.assertTrue(
            self.result["analytic_powered_all_active_lift_certified"]
        )
        self.assertTrue(
            self.result["candidate_26_pair_recurrence_certified"]
        )
        self.assertFalse(self.result["global_t3_2_certified"])


if __name__ == "__main__":
    unittest.main()
