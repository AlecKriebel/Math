#!/usr/bin/env python3
"""Focused tests for the order-three histogram lift audit."""

from __future__ import annotations

import unittest

from verify_lp333_order3_lift_catalog import (
    INCIDENCE,
    INTERSECTIONS,
    TRIPLES,
    aggregate_catalog,
    audit_catalog,
    build_histogram_model,
    replay_histogram,
    solve_histogram,
    transform_aggregate_c2,
    verify_catalog_c2_action,
)


class OrderThreeLiftCatalogTests(unittest.TestCase):
    def test_triple_tables_are_exact(self) -> None:
        self.assertEqual(len(TRIPLES), 84)
        self.assertEqual(len(set(TRIPLES)), 84)
        self.assertTrue(all(len(block) == 3 for block in TRIPLES))
        self.assertTrue(all(sum(row) == 3 for row in INCIDENCE))
        for index, block in enumerate(TRIPLES):
            points = set(block)
            expected = tuple(
                sum((point + lag) % 9 in points for point in points)
                for lag in range(1, 5)
            )
            self.assertEqual(INTERSECTIONS[index], expected)

    def test_histogram_model_size(self) -> None:
        aggregate = aggregate_catalog()[695]
        model, variables = build_histogram_model(aggregate)
        self.assertEqual(tuple(len(group) for group in variables), (84,) * 4)
        self.assertEqual(len(model.proto.variables), 336)
        self.assertEqual(len(model.proto.constraints), 26)
        self.assertEqual(model.validate(), "")

    def test_corrected_c2_catalog_orbits(self) -> None:
        self.assertEqual(
            verify_catalog_c2_action(),
            {"catalog_words": 1_756, "fixed_words": 4, "orbits": 880},
        )
        for word in aggregate_catalog()[::251]:
            self.assertEqual(
                transform_aggregate_c2(transform_aggregate_c2(word)), word
            )

    def test_representative_catalog_rows_lift_and_replay(self) -> None:
        catalog = aggregate_catalog()
        for index in (0, 695, len(catalog) - 1):
            status, witness, _ = solve_histogram(
                catalog[index], time_limit=2.0, workers=4
            )
            self.assertIn(status, ("FEASIBLE", "OPTIMAL"))
            self.assertIsNotNone(witness)
            replay_histogram(catalog[index], witness or ())

    def test_small_range_audit_has_complete_coverage(self) -> None:
        result = audit_catalog(
            start=695,
            stop=698,
            time_limit=2.0,
            workers=4,
            progress_interval=0,
        )
        self.assertEqual(result["tested"], 3)
        self.assertEqual(result["feasible"], 3)
        self.assertEqual(result["infeasible_indices"], ())
        self.assertEqual(result["unknown_indices"], ())


if __name__ == "__main__":
    unittest.main()
