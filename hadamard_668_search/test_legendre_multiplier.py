"""Regression tests for the order-three multiplier LP(333) sublane."""

from __future__ import annotations

import unittest

from search_legendre_333_cp_sat import fixed_compression_distance_bounds
from search_legendre_333_multiplier import (
    build_multiplier_model,
    canonical_lag,
    invariant_translation_offsets,
    invariant_distance_edge_upper_bound,
    multiplier_orbits,
    representative_lags,
)


class MultiplierModelTests(unittest.TestCase):
    def test_order_three_orbits_partition_indices(self) -> None:
        orbits = multiplier_orbits(121)
        self.assertEqual(len(orbits), 113)
        self.assertEqual(sorted(value for orbit in orbits for value in orbit), list(range(333)))
        self.assertEqual(sum(len(orbit) == 1 for orbit in orbits), 3)
        self.assertEqual(sum(len(orbit) == 3 for orbit in orbits), 110)

    def test_representative_lags_cover_all_lags(self) -> None:
        representatives = representative_lags(121)
        self.assertEqual(len(representatives), 56)
        self.assertEqual(set(representatives), {canonical_lag(lag, 121) for lag in range(1, 167)})

    def test_invariant_translation_subgroups(self) -> None:
        self.assertEqual(invariant_translation_offsets(10), tuple(range(0, 333, 37)))
        self.assertEqual(invariant_translation_offsets(121), (0, 111, 222))

    def test_multiplier_112_has_elementary_lag_111_obstruction(self) -> None:
        # Invariance forces at least 222 of the 333 shifted pairs to agree,
        # while the fixed compression requires each distance to be >=112.
        self.assertEqual(invariant_distance_edge_upper_bound(112, 111), 111)
        self.assertEqual(
            fixed_compression_distance_bounds(111), ((112, 222), (112, 222))
        )

    def test_compact_full_model_validates(self) -> None:
        model, _, _, _ = build_multiplier_model(121)
        self.assertEqual(model.validate(), "")
        stats = model.model_stats()
        self.assertIn("#kTable: 1", stats)
        self.assertIn("#kBoolXor", stats)


if __name__ == "__main__":
    unittest.main()
