#!/usr/bin/env python3
"""Exact arithmetic audit of the polar-alignment depth improvement."""

from fractions import Fraction as F


def verify_exact_identity_reduction() -> None:
    # Arbitrary rational depth/simplex-sector values.
    delta = F(2, 25)
    y = F(1, 10)
    a = F(3, 50)
    N = 4 * delta + F(9, 4) * a + F(3, 4) * y
    assert 567 * a + 297 * y - 252 * (N - 4 * delta) == 108 * y


def verify_one_variable_minimum() -> None:
    delta = F(7, 100)
    boundary = 4 * delta

    def penalty(N: F) -> F:
        return 252 * (N - boundary) + 9 * delta * delta / (16 * N)

    assert penalty(boundary) == F(9, 64) * delta
    # Exact positive derivative floor used in the proof.
    assert 252 - F(9, 256) > 0
    assert penalty(boundary + F(1, 100)) > penalty(boundary)


def verify_final_constant() -> None:
    bound = F(216 * 64, 101385)
    assert bound == F(512, 3755)
    assert F(3, 22) - bound == F(1, 82610)
    assert F(101385, 64) * bound == 216


if __name__ == "__main__":
    verify_exact_identity_reduction()
    verify_one_variable_minimum()
    verify_final_constant()
    print("n=3 polar-alignment depth improvement: exact checks passed")
