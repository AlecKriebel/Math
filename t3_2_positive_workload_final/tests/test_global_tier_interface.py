import unittest

import global_atlas_interface_closure as closure
import global_tier_interface as tier


class GlobalTierInterfaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = tier.certificate()

    def test_exact_arrangement_counts(self):
        self.assertEqual(len(tier.comparison_normals()), 21)
        self.assertEqual(len(tier.simplex_vertices()), 37)
        self.assertEqual(len(tier.arrangement_candidates()), 5128)
        self.assertEqual(len(tier.tier_types()), 193)
        self.assertEqual(len(tier.tier_descriptors()), 259)
        self.assertEqual(
            self.result["certificate_sha256"],
            "c8ed2dd0834f6e94057e11d96900cf0fb5e1daca713cafa74f9963483eb62ad4",
        )

    def test_positive_residual_split(self):
        result = self.result["positive"]
        self.assertEqual(result["input_residual_pairs"], 3531)
        self.assertEqual(result["universally_tier_certified"], 1219)
        self.assertEqual(result["not_universally_tier_certified"], 2312)
        self.assertEqual(result["certified_modulo_A_B_exchange"], 757)
        self.assertEqual(result["remaining_modulo_A_B_exchange"], 1340)
        self.assertEqual(result["greedy_obstruction_descriptors"], 17)
        self.assertEqual(
            result["greedy_obstruction_descriptors_modulo_A_B_exchange"],
            12,
        )
        self.assertEqual(
            result["remaining_sha256"],
            "0297ba35311c757cd5c6ec548d2af18410dfd37e791c7679de932fe4bf38695b",
        )
        self.assertEqual(
            sum(row["universally_tier_certified"] for row in result["by_shielded_support"]),
            1219,
        )
        self.assertEqual(
            sum(row["remaining"] for row in result["by_shielded_support"]),
            2312,
        )

    def test_signed_residual_split(self):
        result = self.result["signed"]
        self.assertEqual(result["input_residual_pairs"], 358)
        self.assertEqual(result["universally_tier_certified"], 159)
        self.assertEqual(result["not_universally_tier_certified"], 199)
        self.assertEqual(result["greedy_obstruction_descriptors"], 4)
        self.assertEqual(
            result["remaining_sha256"],
            "1a9c06123645855d3b4f23d4886b0ada3c3ff3614fc94a7d22c01f411c1355c8",
        )
        self.assertEqual(
            sum(row["universally_tier_certified"] for row in result["by_shielded_support"]),
            159,
        )
        self.assertEqual(
            sum(row["remaining"] for row in result["by_shielded_support"]),
            199,
        )
        service = result["exact_service_superset_audit"]
        self.assertEqual(service["remaining_signed_pairs_containing_C_2C"], 38)
        self.assertEqual(service["of_which_contain_0_C_2C"], 5)
        self.assertEqual(service["remaining_signed_pairs_without_C_2C"], 161)
        self.assertEqual(service["inclusion_minimal_pair_count"], 10)
        actual_minimal = {
            (tuple(row["shielded"]), tuple(row["available"]))
            for row in service["inclusion_minimal_pairs"]
        }
        expected_minimal = {
            (shielded, available)
            for shielded, extras in (
                (("0", "2A", "BC"), (("A", "C", "2C"),)),
                (("0", "A", "BC"), (("C", "2A", "2C"),)),
                (("A", "2A", "BC"), ()),
                (("0", "A", "2A", "BC"), ()),
            )
            for available in extras
        } | {
            (shielded, available)
            for shielded in (
                ("0", "2A", "BC"),
                ("0", "A", "BC"),
                ("A", "2A", "BC"),
                ("0", "A", "2A", "BC"),
            )
            for available in (("C", "2C", "AB"), ("C", "2C", "AC"))
        }
        self.assertEqual(actual_minimal, expected_minimal)
        self.assertEqual(
            service["adjacent_sha256"],
            "114d7d2baa132be2b3c957159a016588dcd70e3a7a4a853eee5d9761a03a9816",
        )

    def test_second_family_matches_analytic_proposition(self):
        passed, failed = tier.tier_split(closure.POSITIVE_SHIELDED_MASKS)
        second_passed = frozenset(
            pair for pair in passed if pair[0] == closure.SECOND_SHIELDED_MASK
        )
        second_failed = frozenset(
            pair for pair in failed if pair[0] == closure.SECOND_SHIELDED_MASK
        )
        self.assertEqual(
            second_passed,
            closure.second_family_tier_certified_pairs(),
        )
        self.assertEqual(len(second_passed), 12)
        self.assertEqual(len(second_failed), 37)

    def test_every_reported_obstruction_really_fails(self):
        for masks in (
            closure.POSITIVE_SHIELDED_MASKS,
            closure.SIGNED_SHIELDED_MASKS,
        ):
            _, failed = tier.tier_split(masks)
            for pair in failed:
                descriptor = tier.obstruction(pair)
                self.assertIsNotNone(descriptor)
                self.assertFalse(
                    tier.universal_orientation_tier_condition(pair, descriptor)
                )
                cycles = tier.obstruction_cycles(pair, descriptor)
                for mask, edges in zip(pair, cycles):
                    nodes = {index for edge in edges for index in edge}
                    self.assertEqual(nodes, set(tier._nodes(mask)))
                    self.assertEqual(len(edges), len(nodes))
                self.assertFalse(
                    tier.has_top_s_descending_source(pair, descriptor, cycles)
                )

    def test_canonical_analytic_gate_table(self):
        result = self.result["analytic_gate_table"]
        self.assertEqual(result["remaining_positive_pairs"], 2312)
        self.assertEqual(result["remaining_signed_pairs"], 199)
        self.assertEqual(result["remaining_total_pairs"], 2511)
        self.assertEqual(result["canonical_descriptor_gates"], 12)
        self.assertEqual(result["exact_physical_time_pairs_removed_before_table"], 3)
        gates = result["gates"]
        self.assertEqual(
            {(tuple(gate["weight"]), tuple(gate["caps"])) for gate in gates},
            set(tier.canonical_gate_keys()),
        )
        for gate in gates:
            promotion = gate["mechanisms"]["disabled_source_promotion"]
            flat = gate["mechanisms"]["flat_top_linkage"]
            if len(gate["active_coordinates"]) == 3:
                self.assertEqual(promotion, 0)
                self.assertGreater(flat, 0)
            else:
                self.assertGreater(promotion, 0)
                self.assertGreater(flat, 0)

    def test_one_active_interface_counts_and_invariants(self):
        interface = self.result["one_active_interface"]
        self.assertEqual(interface["one_active_descriptors"], 27)

        positive = interface["families"]["positive"]
        self.assertEqual(positive["pairs_with_any_one_active_obstruction"], 2087)
        self.assertEqual(positive["pairs_with_only_one_active_obstructions"], 1081)
        self.assertEqual(positive["classwise_invariant_closures"], 67)
        self.assertEqual(positive["remaining_after_classwise_invariant"], 2245)
        self.assertEqual(positive["remaining_with_only_one_active_obstructions"], 1014)
        self.assertEqual(positive["still_has_a_multi_active_obstruction"], 1231)
        self.assertEqual(
            positive["invariant_closed_sha256"],
            "f353c0306e3a629c2828ebbc3a4d9d0a5f5e39967729eac3ce12c6cbff9ed596",
        )
        self.assertEqual(
            positive["remaining_sha256"],
            "b823a53653dd549ad73d53ff9bcd2dcc6ce414a4900edcbe9534a31d9db11ed4",
        )
        self.assertEqual(
            [row["pairs_with_an_axis_obstruction"] for row in positive["axes"]],
            [822, 908, 881],
        )
        self.assertEqual(
            [row["disabled_source_promotion"] for row in positive["axes"]],
            [746, 832, 811],
        )
        self.assertEqual(
            [row["flat_top_linkage"] for row in positive["axes"]],
            [76, 76, 70],
        )

        signed = interface["families"]["signed"]
        self.assertEqual(signed["pairs_with_any_one_active_obstruction"], 195)
        self.assertEqual(signed["pairs_with_only_one_active_obstructions"], 151)
        self.assertEqual(signed["classwise_invariant_closures"], 0)
        self.assertEqual(signed["remaining_after_classwise_invariant"], 199)
        self.assertEqual(signed["remaining_with_only_one_active_obstructions"], 151)
        self.assertEqual(signed["still_has_a_multi_active_obstruction"], 48)
        self.assertEqual(
            [row["pairs_with_an_axis_obstruction"] for row in signed["axes"]],
            [0, 116, 118],
        )
        self.assertEqual(
            [row["disabled_source_promotion"] for row in signed["axes"]],
            [0, 116, 118],
        )
        self.assertEqual(
            [row["flat_top_linkage"] for row in signed["axes"]],
            [0, 0, 0],
        )

    def test_zero_cap_axis_selector(self):
        selector = self.result["zero_cap_axis_selector"]
        self.assertEqual(
            {
                (tuple(row["weight"]), tuple(row["caps"]))
                for row in selector["allowed_obstruction_keys"]
            },
            tier.ZERO_CAP_AXIS_KEYS,
        )
        self.assertEqual(selector["positive"]["selected"], 596)
        self.assertEqual(
            selector["positive"]["sha256"],
            "73de3c2e5cbef71de1a003b75a0c593fe7eef8e18a9d34b88c3816f0a98512e6",
        )
        self.assertTrue(
            selector["positive"]["disjoint_from_flat_axis_invariant_set"]
        )
        self.assertEqual(selector["signed"]["selected"], 151)
        self.assertEqual(
            selector["signed"]["sha256"],
            "748bce431e84296b43e9fca18982d7e6ad353ee78efbeba01570dcd9325173d4",
        )
        self.assertTrue(
            selector["signed"]["disjoint_from_flat_axis_invariant_set"]
        )


if __name__ == "__main__":
    unittest.main()
