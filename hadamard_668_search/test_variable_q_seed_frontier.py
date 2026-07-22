from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from search_variable_q_seed_frontier import (
    SHARD_287_MINIMUM_TARGET,
    _quadratic_norm_rows,
    build_quad_orbit_root_model,
    build_target_model,
    select_prior_survivors,
)
from verify_variable_q_seed_quad_radius import check_radius
from verify_variable_q_seed_radius import SEED


class VariableQSeedFrontierTests(unittest.TestCase):
    def test_quadratic_norm_tables_are_exact(self) -> None:
        for cross_sign in (-1, 0, 1):
            expected = {
                (first, second, first * first + cross_sign * first * second + second * second)
                for first in range(-4, 5)
                for second in range(-4, 5)
                if first * first
                + cross_sign * first * second
                + second * second
                <= 334
            }
            self.assertEqual(set(_quadratic_norm_rows(4, cross_sign)), expected)

    def test_all_radius_fourteen_frontier_models_validate(self) -> None:
        radius = 14
        check = check_radius(radius)
        frontier = tuple(
            record
            for record in check.targets
            if record.quad_distance is not None
            and record.quad_distance <= radius
        )
        self.assertEqual(len(frontier), 18)
        for record in frontier:
            self.assertIsNotNone(record.long_distance)
            self.assertIsNotNone(record.short_distance)
            model, _variables = build_target_model(
                record.target,
                radius,
                pair_distance_lower_bounds=(
                    int(record.long_distance),
                    int(record.short_distance),
                ),
            )
            self.assertEqual(model.validate(), "")

    def test_pair_distance_bounds_are_checked(self) -> None:
        record = next(
            record
            for record in check_radius(14).targets
            if record.quad_distance is not None and record.quad_distance <= 14
        )
        with self.assertRaises(ValueError):
            build_target_model(
                record.target,
                14,
                pair_distance_lower_bounds=(14, 2),
            )

    def test_quad_orbit_root_model_validates(self) -> None:
        record = next(
            record
            for record in check_radius(14).targets
            if record.quad_distance is not None and record.quad_distance <= 14
        )
        model, encoding = build_quad_orbit_root_model(
            record.target,
            14,
            pair_distance_lower_bounds=(
                int(record.long_distance),
                int(record.short_distance),
            ),
        )
        self.assertEqual(model.validate(), "")
        self.assertEqual(len(encoding.orbits), 60)
        self.assertEqual(
            sum(len(orbit.physical_groups) for orbit in encoding.orbits),
            84,
        )
        covered = set()
        for orbit in encoding.orbits:
            representative = orbit.physical_groups[0]
            for physical in orbit.physical_groups:
                self.assertEqual(
                    tuple(index for index, _coordinate in physical),
                    tuple(index for index, _coordinate in representative),
                )
                self.assertEqual(
                    tuple(coordinate % 12 for _index, coordinate in physical),
                    tuple(
                        coordinate % 12
                        for _index, coordinate in representative
                    ),
                )
                self.assertEqual(
                    tuple(SEED[index][coordinate] for index, coordinate in physical),
                    tuple(
                        SEED[index][coordinate]
                        for index, coordinate in representative
                    ),
                )
                for cell in physical:
                    self.assertNotIn(cell, covered)
                    covered.add(cell)
            if len(representative) == 4:
                self.assertTrue(all(mask.bit_count() % 2 == 0 for mask in orbit.masks))
        self.assertEqual(len(covered), 334)

    def test_optional_layers_validate(self) -> None:
        record = next(
            record
            for record in check_radius(14).targets
            if record.quad_distance is not None and record.quad_distance <= 14
        )
        for layers in (
            {"small_root_encoding": "multiplication"},
            {"compression_7": True},
            {"compression_7_alternating": True},
            {
                "compression_7": True,
                "compression_7_alternating": True,
                "full_correlations": True,
            },
        ):
            model, _variables = build_target_model(record.target, 14, **layers)
            self.assertEqual(model.validate(), "")

    def test_radius_sixteen_shard_287_reduction_validates(self) -> None:
        model, _variables = build_target_model(SHARD_287_MINIMUM_TARGET, 16)
        self.assertEqual(model.validate(), "")

    def test_exact_distance_interval_validates(self) -> None:
        record = next(
            record
            for record in check_radius(17).targets
            if record.quad_distance is not None
            and record.quad_distance <= 17
            and record.margin_distance % 2 == 1
        )
        model, _variables = build_target_model(
            record.target, 17, minimum_distance=17
        )
        self.assertEqual(model.validate(), "")

    def test_select_prior_survivors(self) -> None:
        radius = 14
        frontier = tuple(
            record
            for record in check_radius(radius).targets
            if record.quad_distance is not None
            and record.quad_distance <= radius
        )
        source = {
            "kind": "variable-q-seed-frontier-filter",
            "radius": radius,
            "minimum_distance": 0,
            "results": [
                {
                    "shard": record.shard,
                    "target": record.target,
                    "status": (
                        "OPTIMAL"
                        if index in (2, 7)
                        else "UNKNOWN"
                        if index == 11
                        else "INFEASIBLE"
                    ),
                }
                for index, record in enumerate(frontier)
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "frontier.json"
            path.write_text(json.dumps(source), encoding="utf-8")
            selected, digest = select_prior_survivors(
                frontier, path, radius=radius, minimum_distance=0
            )
            unresolved, _digest = select_prior_survivors(
                frontier,
                path,
                radius=radius,
                minimum_distance=0,
                selection_mode="unresolved",
            )
            timeouts, _digest = select_prior_survivors(
                frontier,
                path,
                radius=radius,
                minimum_distance=0,
                selection_mode="timeouts",
            )
        self.assertEqual(selected, (frontier[2], frontier[7]))
        self.assertEqual(unresolved, (frontier[2], frontier[7], frontier[11]))
        self.assertEqual(timeouts, (frontier[11],))
        self.assertEqual(len(digest), 64)


if __name__ == "__main__":
    unittest.main()
