from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import global_tier_interface as tier
import stoichiometric_gate_feasibility as feasibility
import two_active_phase_gate as phase


class TwoActivePhaseGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = phase.certificate()

    def test_complete_disjoint_incidence_split(self):
        self.assertEqual(self.result["feasible_two_active_incidences"], 2388)
        self.assertEqual(
            sum(
                row["incidences"]
                for row in self.result["categories"].values()
            ),
            2388,
        )
        self.assertEqual(
            {category for _, _, category in phase.incidences()},
            set(self.result["categories"]),
        )

    def test_exact_counts(self):
        self.assertEqual(
            (self.result["pairs_with_a_feasible_two_active_failure"],
             self.result["positive_pairs"], self.result["signed_pairs"]),
            (1036, 996, 40),
        )
        expected = {
            "promotion_enabled_top_seed": (963, 584, 552, 32),
            "promotion_dormant_top": (453, 367, 333, 34),
            "closed_rank_one_top_phase": (930, 310, 308, 2),
            "coupled_rank_two_top_phase": (42, 14, 14, 0),
        }
        for category, counts in expected.items():
            row = self.result["categories"][category]
            self.assertEqual(
                (row["incidences"], row["pairs"],
                 row["positive_pairs"], row["signed_pairs"]),
                counts,
            )
        self.assertEqual(self.result["flat_and_promotion_pair_overlap"], 91)
        self.assertEqual(self.result["promotion_inactive_cap_histogram"], {0: 1416})
        self.assertEqual(
            self.result["flat_inactive_cap_histogram"],
            {0: 324, 1: 324, 2: 324},
        )
        self.assertEqual(
            {
                key: (row["incidences"], row["pairs"])
                for key, row in self.result[
                    "rank_one_activation_refinement"
                ].items()
            },
            {
                "lower_top_seeded": (893, 310),
                "top_phase_activates": (2, 2),
                "lower_layer_activation_needed": (25, 25),
                "zero_boundary_phase_only": (10, 10),
            },
        )
        self.assertEqual(
            self.result["rank_one_lower_maximum_weight_histogram"],
            {1: 930},
        )

    def test_every_row_is_feasible_and_failing(self):
        for pair, descriptor, category in phase.incidences():
            self.assertEqual(sum(value > 0 for value in descriptor.weight), 2)
            self.assertFalse(
                tier.universal_orientation_tier_condition(pair, descriptor)
            )
            self.assertTrue(feasibility.descriptor_feasible(pair, descriptor))
            self.assertEqual(phase.incidence_category(pair, descriptor), category)

    def test_flat_phase_rank_and_unique_top_linkage(self):
        for pair, descriptor, category in phase.incidences():
            if not category.endswith("top_phase"):
                continue
            whole = phase._whole_top_linkages(pair, descriptor)
            self.assertEqual(len(whole), 1)
            expected_rank = 1 if category.startswith("closed_rank_one") else 2
            self.assertEqual(phase._linkage_rank(whole[0]), expected_rank)

    def test_rank_two_support_is_exact(self):
        self.assertEqual(
            self.result["categories"]["coupled_rank_two_top_phase"]
            ["top_supports"],
            [["B", "2A", "BC"]],
        )
        self.assertEqual(self.result["rank_two_lower_partners"]["count"], 14)
        self.assertTrue(
            self.result["rank_two_lower_partners"]["all_cross_q_partition"]
        )

    def test_reachability_composition_selector_is_empty(self):
        row = self.result["reachability_aware_composition_selector"]
        self.assertEqual(
            (
                row["affine_branch_pairs"],
                row["one_active_after_affine_pairs"],
                row["branch_overlap"],
                row["prior_union_pairs"],
                row["prior_union_positive"],
                row["prior_union_signed"],
                row["remaining_after_prior_union"],
            ),
            (151, 1227, 0, 1378, 1219, 159, 1133),
        )
        self.assertEqual(
            (row["zero_boundary_incidences"], row["zero_boundary_pairs"]),
            (10, 10),
        )
        self.assertEqual(row["new_pairs_after_removing_one_active_failures"], 0)
        self.assertEqual(
            row["new_pair_sha256"],
            "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945",
        )

    def test_frozen_hash(self):
        self.assertEqual(
            self.result["all_incidence_sha256"],
            "908c15311c0d1240a8c79b0fb4b922ec1d33b9a497ffb7484be258a19d136273",
        )


if __name__ == "__main__":
    unittest.main()
