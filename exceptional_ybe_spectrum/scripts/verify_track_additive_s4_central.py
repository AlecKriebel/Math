#!/usr/bin/env python3
"""Exact rejection of the two central rank-six S4-equivariant projections."""

from __future__ import annotations

import itertools

import sympy as sp


def parity(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


def main():
    permutations = list(itertools.permutations(range(4)))
    matchings = [
        frozenset((frozenset((0, 1)), frozenset((2, 3)))),
        frozenset((frozenset((0, 2)), frozenset((1, 3)))),
        frozenset((frozenset((0, 3)), frozenset((1, 2)))),
    ]

    # Rational bases e_i-e_last for the standard permutation quotients.
    basis_four = sp.zeros(4, 3)
    basis_three = sp.zeros(3, 2)
    for column in range(3):
        basis_four[column, column] = 1
        basis_four[3, column] = -1
    for column in range(2):
        basis_three[column, column] = 1
        basis_three[2, column] = -1

    standard = sp.zeros(12)
    twisted = sp.zeros(12)
    for permutation in permutations:
        permutation_four = sp.zeros(4)
        for index in range(4):
            permutation_four[permutation[index], index] = 1
        representation_three = (permutation_four * basis_four)[:3, :]

        permutation_three = sp.zeros(3)
        for index, matching in enumerate(matchings):
            image = frozenset(
                frozenset(permutation[element] for element in pair)
                for pair in matching
            )
            permutation_three[matchings.index(image), index] = 1
        representation_two = (permutation_three * basis_three)[:2, :]

        representation = sp.kronecker_product(
            representation_two,
            representation_three,
            representation_two,
        )
        character = sum(
            permutation[index] == index for index in range(4)
        ) - 1
        standard += sp.Rational(character, 8) * representation
        twisted += (
            sp.Rational(parity(permutation) * character, 8)
            * representation
        )

    assert standard * standard == standard
    assert twisted * twisted == twisted
    assert standard * twisted == sp.zeros(12)
    assert sp.trace(standard) == 6
    assert sp.trace(twisted) == 6

    for label, projector, expected in (
        ("standard", standard, sp.Rational(-5, 12)),
        ("twisted", twisted, sp.Rational(5, 12)),
    ):
        involution = sp.eye(12) - 2 * projector
        first = sp.kronecker_product(involution, sp.eye(6))
        second = sp.kronecker_product(sp.eye(6), involution)
        residual = (
            first * second * first
            - second * first * second
            - sp.Rational(1, 3) * (first - second)
        )
        assert residual[0, 1] == expected
        print(
            f"{label} central projector: rank 6; "
            f"exact residual[0,1] = {residual[0, 1]}"
        )

    print("Both central S4-equivariant half-rank choices fail exactly.")
    print("All assertions passed (exact rational SymPy arithmetic).")


if __name__ == "__main__":
    main()
