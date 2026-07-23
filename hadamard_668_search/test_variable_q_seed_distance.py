from __future__ import annotations

import unittest

from variable_q_base import base_quad_products
from variable_q_seed_distance import (
    SEED,
    build_model,
    closest_margin_targets,
    minimum_class_flips,
    verify_witness,
)


class VariableQSeedDistanceTests(unittest.TestCase):
    def test_margin_only_radius_eight_is_unique_and_breaks_quad_parity(self) -> None:
        distance, witnesses = closest_margin_targets()
        self.assertEqual(distance, 8)
        self.assertEqual(
            witnesses,
            (
                (
                    287,
                    ((-18, 18), (0, 0), (3, 1), (-1, -3)),
                ),
            ),
        )
        target = witnesses[0][1]
        requirements = tuple(
            minimum_class_flips(sequence, margins)
            for sequence, margins in zip(SEED, target, strict=True)
        )
        self.assertEqual(
            requirements,
            (((0, 0), (8, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0))),
        )
        long_products, short_products = base_quad_products(*SEED)
        self.assertEqual(long_products, (-1,) + (1,) * 41)
        self.assertEqual(short_products, (1,) * 41)
        # Each long endpoint pair contains exactly one odd A coordinate.
        # Therefore the eight forced odd-coordinate flips occupy eight
        # distinct quads and toggle their already-correct products.
        odd_quad_indices = {
            min(index, 83 - index) for index in range(1, 84, 2)
        }
        self.assertEqual(len(odd_quad_indices), 42)

    def test_relaxation_model_validates(self) -> None:
        for layers in (
            {},
            {"small_roots": True},
            {"compression_7": True},
            {"compression_7_alternating": True},
            {
                "small_roots": True,
                "compression_7": True,
                "compression_7_alternating": True,
            },
        ):
            model, _variables = build_model(**layers)
            self.assertEqual(model.validate(), "")

    def test_published_seed_fails_the_minimal_relaxation_at_ordinary_norm(self) -> None:
        with self.assertRaisesRegex(ValueError, "ordinary norm identity"):
            verify_witness(
                SEED,
                small_roots=False,
                compression_7=False,
                compression_7_alternating=False,
            )


if __name__ == "__main__":
    unittest.main()
