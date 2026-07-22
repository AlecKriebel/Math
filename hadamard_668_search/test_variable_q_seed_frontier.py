from __future__ import annotations

import unittest

from search_variable_q_seed_frontier import (
    SHARD_287_MINIMUM_TARGET,
    _quadratic_norm_rows,
    build_target_model,
)
from verify_variable_q_seed_quad_radius import check_radius


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
            model, _variables = build_target_model(record.target, radius)
            self.assertEqual(model.validate(), "")

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


if __name__ == "__main__":
    unittest.main()
