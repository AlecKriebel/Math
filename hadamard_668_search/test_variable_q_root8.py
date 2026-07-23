import unittest

from seed import ELIAHOU_Q, ELIAHOU_S
from variable_q_base import special_to_base
from variable_q_root8 import (
    ENERGY,
    Root8Report,
    TIGHT_ROOT8_TARGET,
    coordinate_group_sizes,
    distance_between,
    minimum_seed_distance_to_rational_sphere,
    minimum_seed_distance_with_margins,
    margin_quad_witness,
    root8_coordinates,
    root8_report,
    tight_root8_witness,
)


class PrimitiveEighthRootTests(unittest.TestCase):
    def setUp(self) -> None:
        self.seed = special_to_base(ELIAHOU_S, ELIAHOU_Q)

    def test_seed_coordinates_and_energy(self) -> None:
        self.assertEqual(
            tuple(root8_coordinates(sequence) for sequence in self.seed),
            (
                (11, -11, 19, -1),
                (11, -11, 19, 1),
                (-9, 11, 1, 0),
                (-11, 9, 1, 0),
            ),
        )
        self.assertEqual(
            tuple(coordinate_group_sizes(len(sequence)) for sequence in self.seed),
            ((21, 21, 21, 21),) * 2 + ((21, 21, 21, 20),) * 2,
        )
        self.assertEqual(root8_report(self.seed), Root8Report(1614, 0))

    def test_exact_distance_bound_and_tight_relaxation_witness(self) -> None:
        distance, target = minimum_seed_distance_to_rational_sphere(self.seed)
        self.assertEqual(distance, 33)
        self.assertEqual(sum(value * value for value in target), ENERGY)

        witness = tight_root8_witness(self.seed)
        self.assertEqual(distance_between(self.seed, witness), 33)
        self.assertEqual(
            tuple(root8_coordinates(sequence) for sequence in witness),
            TIGHT_ROOT8_TARGET,
        )
        self.assertEqual(root8_report(witness), Root8Report(ENERGY, 0))

    def test_exact_margins_raise_the_sharp_distance_to_34(self) -> None:
        self.assertEqual(
            minimum_seed_distance_with_margins(self.seed),
            (34, 1350, 66),
        )
        witness = margin_quad_witness(self.seed)
        self.assertEqual(distance_between(self.seed, witness), 34)
        self.assertEqual(root8_report(witness), Root8Report(ENERGY, 0))
        ordinary = tuple(map(sum, witness))
        alternating = tuple(
            sum(value if index % 2 == 0 else -value for index, value in enumerate(sequence))
            for sequence in witness
        )
        self.assertEqual(sum(value * value for value in ordinary), ENERGY)
        self.assertEqual(sum(value * value for value in alternating), ENERGY)

        from variable_q_base import base_correlations, base_quad_products

        self.assertEqual(
            base_quad_products(*witness), base_quad_products(*self.seed)
        )
        self.assertTrue(any(base_correlations(*witness)[1:]))


if __name__ == "__main__":
    unittest.main()
