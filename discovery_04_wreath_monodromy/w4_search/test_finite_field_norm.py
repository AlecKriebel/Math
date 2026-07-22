#!/usr/bin/env python3
"""Deterministic algebra tests for the bounded W4 norm evaluator."""

from __future__ import annotations

import unittest

from finite_field_norm import CubicAlgebra, _det_mod, discriminant, reconstruct


def forward_map(
    algebra: CubicAlgebra,
    point: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    """The announced Keller map, independently transcribed for testing."""
    x, y, z = point
    xy = algebra.mul(x, y)
    u = algebra.add(algebra.one(), xy)
    u2 = algebra.square(u)
    u3 = algebra.mul(u2, u)
    x2 = algebra.square(x)
    x3 = algebra.mul(x2, x)
    y2 = algebra.square(y)
    four_plus = algebra.add(algebra.constant(4), algebra.scale(xy, 3))
    first = algebra.add(
        algebra.mul(u3, z),
        algebra.mul(algebra.mul(y2, u), four_plus),
    )
    second = algebra.add(
        algebra.add(y, algebra.scale(algebra.mul(algebra.mul(x, u2), z), 3)),
        algebra.scale(algebra.mul(algebra.mul(x, y2), four_plus), 3),
    )
    third = algebra.sub(
        algebra.sub(algebra.scale(x, 2), algebra.scale(algebra.mul(x2, y), 3)),
        algebra.mul(x3, z),
    )
    return first, second, third


class CubicAlgebraTests(unittest.TestCase):
    prime = 101

    def setUp(self) -> None:
        self.field = CubicAlgebra(self.prime)
        coefficients = tuple(
            self.field.constant(value) for value in (2, 3, 5, 1)
        )
        self.algebra = self.field.extend(coefficients)

    def test_generator_satisfies_defining_cubic(self) -> None:
        u = self.algebra.generator()
        value = self.algebra.add(
            self.algebra.add(
                self.algebra.power(u, 3),
                self.algebra.scale(self.algebra.square(u), 5),
            ),
            self.algebra.add(self.algebra.scale(u, 3), self.algebra.constant(2)),
        )
        self.assertEqual(value, self.algebra.zero())

    def test_inverse_and_norm_multiplicativity(self) -> None:
        u = self.algebra.generator()
        left = self.algebra.add(
            self.algebra.constant(7),
            self.algebra.add(
                self.algebra.scale(u, 2),
                self.algebra.scale(self.algebra.square(u), 3),
            ),
        )
        right = self.algebra.add(
            self.algebra.constant(11), self.algebra.scale(self.algebra.square(u), 4)
        )
        inverse = self.algebra.inverse(left)
        self.assertEqual(self.algebra.mul(left, inverse), self.algebra.one())
        self.assertEqual(
            self.algebra.norm(self.algebra.mul(left, right)),
            self.algebra.norm(left) * self.algebra.norm(right) % self.prime,
        )

    def test_nested_generator_relation_and_embedded_norm(self) -> None:
        u = self.algebra.generator()
        nested = self.algebra.extend(
            (
                self.algebra.add(self.algebra.constant(3), u),
                self.algebra.constant(4),
                self.algebra.scale(u, 2),
                self.algebra.constant(1),
            )
        )
        v = nested.generator()
        u_up = nested.embed(u)
        relation_value = nested.add(
            nested.add(
                nested.power(v, 3),
                nested.mul(nested.scale(u_up, 2), nested.square(v)),
            ),
            nested.add(
                nested.scale(v, 4), nested.add(nested.constant(3), u_up)
            ),
        )
        self.assertEqual(relation_value, nested.zero())
        element = self.algebra.add(self.algebra.constant(7), u)
        self.assertEqual(
            nested.norm(nested.embed(element)),
            pow(self.algebra.norm(element), 3, self.prime),
        )

    def test_inverse_reconstruction_recovers_target(self) -> None:
        # The root relation is 2t^3-2t^2+2t-s=0 for s=7.
        s_value = 7
        field = self.field
        tower = field.extend(
            tuple(
                field.constant(value)
                for value in (-s_value, 2, -2, 2)
            )
        )
        target = (
            tower.constant(1),
            tower.constant(2),
            tower.constant(s_value),
        )
        inverse_point = reconstruct(tower, *target, tower.generator())
        self.assertEqual(forward_map(tower, inverse_point), target)
        # Also exercise the reduced discriminant in the same quotient.
        self.assertEqual(len(discriminant(tower, inverse_point)), tower.dimension)

    def test_prime_square_determinant_retains_first_order_term(self) -> None:
        prime = 7
        modulus = prime * prime

        def matrix(parameter: int) -> list[list[int]]:
            return [[1, parameter], [parameter, 2]]

        # det = 2-s^2 has a simple zero at s=3 mod 7, with derivative
        # -2s = 1 mod 7.  The p-adic difference recovers that derivative.
        at_s = _det_mod(matrix(3), modulus)
        at_s_plus_p = _det_mod(matrix(3 + prime), modulus)
        difference = (at_s_plus_p - at_s) % modulus
        self.assertEqual(difference % prime, 0)
        self.assertEqual(difference // prime, 1)

        # A final nonunit pivot must not be discarded by determinant code.
        self.assertEqual(_det_mod([[1, 0], [0, 3 * prime]], modulus), 3 * prime)


if __name__ == "__main__":
    unittest.main()
