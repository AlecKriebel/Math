#!/usr/bin/env python3

import unittest

import verify_lp333_order3_shell3_cubic_character as cubic


class CubicCharacterTests(unittest.TestCase):
    def test_complete_replay(self) -> None:
        result = cubic.verify()
        self.assertEqual(result["targets_rank_five"], 22)
        self.assertEqual(result["invariant_basis_checks"], 676)
        self.assertEqual(result["channel_convention_checks"], 240)
        self.assertEqual(result["wedge_checks"], 625)
        self.assertEqual(result["shell3_controls"], 6)
        self.assertEqual(result["cubic_scalars"], [31, 6, 4, 14, 36, 11])

    def test_wedge_coordinate(self) -> None:
        for left in ((1, 0), (0, 1), (2, -3), (-4, 5)):
            for right in ((1, 1), (3, -2), (-2, 0)):
                wedge = cubic.add(
                    cubic.multiply(left, cubic.conjugate(right)),
                    cubic.scale(
                        -1,
                        cubic.multiply(right, cubic.conjugate(left)),
                    ),
                )
                determinant = cubic.determinant(left, right)
                self.assertEqual(wedge, (-determinant, -2 * determinant))

    def test_character_row_is_new_for_every_target(self) -> None:
        self.assertTrue(
            all(cubic.target_character_rank(target) == 5 for target in cubic.TARGETS)
        )


if __name__ == "__main__":
    unittest.main()
