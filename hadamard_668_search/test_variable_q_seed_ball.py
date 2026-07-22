from __future__ import annotations

import unittest

from search_variable_q_seed_ball import build_model


class VariableQSeedBallTests(unittest.TestCase):
    def test_exact_unsharded_ball_models_validate(self) -> None:
        for flags in (
            {},
            {"compression_7": True},
            {"compression_7_alternating": True},
            {"compression_7": True, "compression_7_alternating": True},
        ):
            model, _variables = build_model(8, **flags)
            self.assertEqual(model.validate(), "")
            self.assertTrue(
                any(
                    constraint.name == "maximum_published_seed_hamming_distance"
                    for constraint in model.proto.constraints
                )
            )

    def test_negative_radius_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_model(-1)


if __name__ == "__main__":
    unittest.main()
