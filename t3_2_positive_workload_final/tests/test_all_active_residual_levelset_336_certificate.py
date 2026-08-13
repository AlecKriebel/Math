import unittest

import all_active_residual_levelset_336_certificate as residual


class AllActiveResidualLevelset336Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = residual.certificate()

    def test_exact_pipeline_counts(self) -> None:
        self.assertEqual(
            self.result["all_ordered_disjoint_support_pairs"],
            46_872,
        )
        self.assertEqual(self.result["mixed_atlas_seed_pairs"], 5_169)
        self.assertEqual(self.result["mixed_atlas_orbit_pairs"], 27_894)
        self.assertEqual(self.result["outside_mixed_atlas_pairs"], 18_978)
        self.assertEqual(
            self.result["removed_by_strictly_positive_invariant"],
            146,
        )
        self.assertEqual(
            self.result["after_strictly_positive_invariant_pairs"],
            18_832,
        )
        self.assertEqual(self.result["active_only_invariant_gap_pairs_retained"], 68)
        self.assertEqual(self.result["active_only_gap_selected_incidences"], 0)
        self.assertEqual(
            self.result["removed_by_deficiency_zero_after_invariant"],
            0,
        )
        self.assertEqual(self.result["all_active_descriptors"], 169)

    def test_corrected_failures_equal_levelset_family(self) -> None:
        self.assertEqual(
            self.result["corrected_feasible_failing_incidences"],
            336,
        )
        self.assertEqual(self.result["distinct_pairs"], 336)
        self.assertEqual(self.result["geometric_incidences"], 336)
        self.assertTrue(self.result["selected_equals_geometric"])

    def test_exact_levelset_geometry_histograms(self) -> None:
        self.assertEqual(
            self.result["weight_histogram"],
            {
                "1,1,1": 312,
                "1,1,2": 8,
                "1,2,1": 8,
                "2,1,1": 8,
            },
        )
        self.assertEqual(
            self.result["top_size_histogram"],
            {3: 154, 4: 126, 5: 48, 6: 8},
        )
        self.assertEqual(self.result["top_rank_histogram"], {2: 336})
        self.assertEqual(
            self.result["top_deficiency_histogram"],
            {0: 154, 1: 126, 2: 48, 3: 8},
        )
        self.assertEqual(
            self.result["lower_support_histogram"],
            {
                "0,A,B": 86,
                "0,A,B,C": 78,
                "0,A,C": 86,
                "0,B,C": 86,
            },
        )
        self.assertEqual(
            self.result["full_deficiency_histogram"],
            {1: 120, 2: 130, 3: 66, 4: 18, 5: 2},
        )
        self.assertEqual(self.result["top_side_histogram"], {0: 168, 1: 168})
        self.assertEqual(self.result["top_quadratic_only"], 312)
        self.assertEqual(self.result["top_with_unary"], 24)

    def test_frozen_fingerprints(self) -> None:
        self.assertEqual(
            self.result["incidence_sha256"],
            "d0c31db81db2400e0ead6e4a1a86b237fbf3b8bbb597340856a2756e9f6c884d",
        )
        self.assertEqual(
            self.result["independent_cross_encoding_sha256"],
            "2bd4025f29d20ea4af467d46704c598652c9332ac4e32df18669cb7eb75c75a0",
        )

    def test_homogeneous_dead_ray_symbolic_exhaustion(self) -> None:
        self.assertEqual(self.result["homogeneous_dead_ray_count"], 360)
        self.assertEqual(
            self.result["homogeneous_dead_ray_kernel_histogram"],
            {
                "common_catalyst": 48,
                "dyadic": 144,
                "two_carrier": 168,
            },
        )
        self.assertEqual(
            self.result["homogeneous_dead_ray_bulk_in_lower"],
            270,
        )
        self.assertEqual(
            self.result["homogeneous_common_catalyst_lower_patterns"],
            {
                "X,Y": 12,
                "X,Y,Z": 12,
                "X,Z": 12,
                "Y,Z": 12,
            },
        )
        self.assertEqual(
            self.result["homogeneous_dead_ray_sha256"],
            "c968fadc060af8225121efc84aa17380e11c41e677ed107d2d078c63d0f241fe",
        )

    def test_each_selected_row_has_the_analytic_geometry(self) -> None:
        for pair, descriptor in residual.selected_incidences():
            geometry = residual.levelset_geometry(pair, descriptor)
            self.assertIsNotNone(geometry)
            side, top, lower, scale = geometry  # type: ignore[misc]
            self.assertEqual(top, pair[side])
            self.assertEqual(lower, pair[1 - side])
            self.assertGreater(scale, 0)


if __name__ == "__main__":
    unittest.main()
