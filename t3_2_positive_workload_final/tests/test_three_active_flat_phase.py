import unittest
from itertools import combinations

import global_atlas_interface_closure as closure
import three_active_flat_phase as three


class ThreeActiveFlatPhaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = three.certificate()

    def test_global_counts_and_hashes(self):
        result = self.result
        self.assertEqual(result["incidences"], 1269)
        self.assertEqual(result["distinct_pairs"], 403)
        self.assertEqual(result["positive_incidences"], 1263)
        self.assertEqual(result["positive_pairs"], 401)
        self.assertEqual(result["signed_incidences"], 6)
        self.assertEqual(result["signed_pairs"], 2)
        self.assertEqual(result["distinct_descriptor_weights"], 39)
        self.assertEqual(result["unique_whole_top_supports"], 35)
        self.assertEqual(result["whole_top_support_orbits_under_S3"], 15)
        self.assertEqual(
            result["incidence_sha256"],
            "a662edcf046c5f759e21ff4a67e4041caf648d32f4ff8eee097bbcee517ac8b7",
        )
        self.assertEqual(
            result["certificate_sha256"],
            "9d43550b31e319a9bc8684877fd32c10502ffdd7979fefb3bdf552a2e9256fb1",
        )

    def test_every_incidence_has_one_whole_top_linkage(self):
        for pair, descriptor in three.feasible_all_active_incidences():
            side, top = three.whole_top_linkage(pair, descriptor)
            self.assertIn(side, (0, 1))
            self.assertEqual(top, pair[side])
            top_nodes = three.tier._nodes(top)
            values = {
                sum(
                    descriptor.weight[coordinate]
                    * closure.COMPLEXES[node][coordinate]
                    for coordinate in range(3)
                )
                for node in top_nodes
            }
            self.assertEqual(len(values), 1)
            other_nodes = three.tier._nodes(pair[1 - side])
            top_d, top_s = three.tier.tier_sets(pair, descriptor)
            self.assertEqual(top_d, top_s)
            self.assertFalse(other_nodes & top_d)

            lower_levels = {
                sum(
                    descriptor.weight[coordinate]
                    * closure.COMPLEXES[node][coordinate]
                    for coordinate in range(3)
                )
                for node in other_nodes
            }
            self.assertGreaterEqual(len(lower_levels), 2)
            maximum = max(lower_levels)
            maximum_sources = {
                node
                for node in other_nodes
                if sum(
                    descriptor.weight[coordinate]
                    * closure.COMPLEXES[node][coordinate]
                    for coordinate in range(3)
                )
                == maximum
            }
            self.assertNotEqual(
                {closure.NAMES[node] for node in maximum_sources},
                {"0"},
            )

    def test_five_exact_top_shapes(self):
        self.assertEqual(
            [
                (
                    row["top_rank"],
                    row["top_deficiency"],
                    row["top_support_size"],
                    row["incidences"],
                    row["unique_top_supports"],
                )
                for row in self.result["analytic_shapes"]
            ],
            [
                (1, 0, 2, 966, 8),
                (1, 1, 3, 279, 3),
                (2, 1, 4, 17, 17),
                (2, 2, 5, 6, 6),
                (2, 3, 6, 1, 1),
            ],
        )
        self.assertEqual(self.result["full_rank_histogram"], {"3": 1269})
        self.assertEqual(
            self.result["full_deficiency_histogram"],
            {"1": 668, "2": 410, "3": 155, "4": 33, "5": 3},
        )

    def test_only_two_rank_two_supports_use_a_unary_complex(self):
        self.assertEqual(
            self.result["exceptional_nonquadratic_rank_two_supports"],
            [["A", "2B", "2C", "BC"], ["B", "2A", "2C", "AC"]],
        )

    def test_exact_rank_two_quadratic_families(self):
        quadratic = {"2A", "2B", "2C", "AB", "AC", "BC"}
        rows = self.result["top_supports"]
        rank_two_quadratic = {
            frozenset(row["support"])
            for row in rows
            if row["rank"] == 2 and row["molecularity_two_only"]
        }
        expected = {
            frozenset(support)
            for size in (4, 5, 6)
            for support in combinations(quadratic, size)
        }
        self.assertEqual(rank_two_quadratic, expected)


if __name__ == "__main__":
    unittest.main()
