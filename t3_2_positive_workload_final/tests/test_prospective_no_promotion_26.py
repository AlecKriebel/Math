from __future__ import annotations

import unittest

import prospective_no_promotion_26 as selector


class ProspectiveNoPromotion26Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = selector.certificate()

    def test_parent_and_pair_counts_are_frozen(self) -> None:
        self.assertEqual(
            self.payload["prospective_parent_795"],
            {
                "pairs": 795,
                "pair_sha256": selector.EXPECTED_PARENT_795_SHA256,
            },
        )
        self.assertEqual(
            self.payload["selected_pairs"],
            {
                "total": 26,
                "positive": 26,
                "signed": 0,
                "pair_sha256": selector.EXPECTED_PAIR_SHA256,
            },
        )

    def test_incidence_partition_and_hashes(self) -> None:
        self.assertEqual(
            self.payload["selected_incidences"],
            {
                "total": 124,
                "one_active": 30,
                "two_active": 0,
                "all_active": 94,
                "all_sha256": selector.EXPECTED_ALL_INCIDENCE_SHA256,
                "one_active_sha256": selector.EXPECTED_ONE_INCIDENCE_SHA256,
                "all_active_sha256": selector.EXPECTED_THREE_INCIDENCE_SHA256,
            },
        )

    def test_one_active_rows_use_only_existing_proof_shapes(self) -> None:
        self.assertEqual(
            self.payload["one_active_structural_routing"],
            {
                "family_iii_origin_down_0": 8,
                "family_iii_origin_no_history": 2,
                "mixed_C_source_direct_down_0": 20,
            },
        )

    def test_fixed_safe_reversible_top_histograms(self) -> None:
        self.assertEqual(
            self.payload["all_active_top_pair_histogram"],
            {"2A,BC": 8, "AC,BC": 18},
        )
        self.assertEqual(
            self.payload["all_active_top_incidence_histogram"],
            {"2A,BC": 40, "AC,BC": 54},
        )

    def test_selector_is_maximal_without_a_promotion_kernel(self) -> None:
        self.assertEqual(
            self.payload["maximal_no_two_active_split"],
            {
                "no_two_active_pairs": 46,
                "factorial_compatible_pairs": 26,
                "linear_workload_switch_pairs": 20,
                "linear_workload_switch_pair_sha256": (
                    selector.EXPECTED_NO_TWO_LINEAR_20_SHA256
                ),
            },
        )
        self.assertEqual(
            self.payload["two_active_maximality"],
            {
                "pairs_with_two_active_failure": 749,
                "all_have_a_promotion_failure": True,
                "pair_sha256": selector.EXPECTED_ALL_TWO_ACTIVE_749_SHA256,
            },
        )

    def test_claim_flags_remain_false(self) -> None:
        for key in (
            "one_active_graph_scope_extension_certified",
            "powered_all_active_lift_certified",
            "pair_level_recurrence_certified",
            "global_t3_2_certified",
        ):
            self.assertFalse(self.payload[key])

    def test_payload_hash_is_frozen(self) -> None:
        self.assertEqual(
            self.payload["payload_sha256"],
            selector.EXPECTED_PAYLOAD_SHA256,
        )


if __name__ == "__main__":
    unittest.main()
