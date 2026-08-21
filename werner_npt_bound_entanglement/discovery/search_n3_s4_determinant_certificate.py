#!/usr/bin/env python3
"""Search a finite S4 certificate for the unshifted n=3 determinant.

The four-replica determinant operator is

    O = p^{tensor 3} - r^{tensor 3},

with

    p=(2-(13))(2-(24)),
    r=(2-(14))(2-(23))(12)(34)

in the local S4 group algebra.  On the product vector
u1 tensor u2 tensor v1 tensor v2, the three global swaps (12), (34),
and (12)(34) have zero expectation because both displayed frames are
orthonormal.  This script tests whether adding scalar multiples of those
zero constraints makes O positive in every triple of S4 irreducibles.

It uses the Young seminormal representations.  Floating-point output is
discovery evidence only.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np
from scipy.optimize import differential_evolution, minimize


PARTITIONS = ((4,), (3, 1), (2, 2), (2, 1, 1), (1, 1, 1, 1))


def cells(shape: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        (row, column)
        for row, length in enumerate(shape)
        for column in range(length)
    )


def standard_tableaux(shape: tuple[int, ...]):
    positions = cells(shape)
    out = []
    for values in itertools.permutations(range(1, 5)):
        tableau = dict(zip(positions, values, strict=True))
        good = True
        for (row, column), value in tableau.items():
            if (row, column + 1) in tableau:
                good &= value < tableau[row, column + 1]
            if (row + 1, column) in tableau:
                good &= value < tableau[row + 1, column]
        if good:
            out.append(tuple(values))
    return positions, out


def adjacent_representations(shape: tuple[int, ...]):
    positions, tableaux = standard_tableaux(shape)
    lookup = {tableau: index for index, tableau in enumerate(tableaux)}
    matrices = []
    for label in (1, 2, 3):
        matrix = np.zeros((len(tableaux), len(tableaux)))
        for index, tableau in enumerate(tableaux):
            position_by_value = {
                value: positions[offset]
                for offset, value in enumerate(tableau)
            }
            first = position_by_value[label]
            second = position_by_value[label + 1]
            axial = (second[1] - second[0]) - (first[1] - first[0])
            matrix[index, index] = 1 / axial
            if abs(axial) != 1:
                swapped = list(tableau)
                first_offset = swapped.index(label)
                second_offset = swapped.index(label + 1)
                swapped[first_offset], swapped[second_offset] = (
                    swapped[second_offset],
                    swapped[first_offset],
                )
                other = lookup[tuple(swapped)]
                matrix[other, index] = np.sqrt(1 - 1 / axial**2)
        matrices.append(matrix)
    return matrices


def compose(left: tuple[int, ...], right: tuple[int, ...]):
    """Return left after right, with permutations stored by images."""
    return tuple(left[right[index]] for index in range(4))


def adjacent_word(permutation: tuple[int, ...]):
    current = list(range(4))
    word = []
    # Right multiplication by adjacent position swaps; reverse at the end.
    for target_position in range(4):
        wanted = permutation[target_position]
        position = current.index(wanted)
        while position > target_position:
            current[position - 1], current[position] = (
                current[position],
                current[position - 1],
            )
            word.append(position)
            position -= 1
    assert tuple(current) == permutation
    return tuple(reversed(word))


def transposition(first: int, second: int):
    permutation = list(range(4))
    permutation[first - 1], permutation[second - 1] = (
        permutation[second - 1],
        permutation[first - 1],
    )
    return tuple(permutation)


def representation(shape: tuple[int, ...], permutation: tuple[int, ...]):
    adjacent = adjacent_representations(shape)
    out = np.eye(adjacent[0].shape[0])
    for generator in adjacent_word(permutation):
        out = out @ adjacent[generator - 1]
    return out


def kron3(first, second, third):
    return np.kron(np.kron(first, second), third)


def local_data(shape: tuple[int, ...]):
    identity = np.eye(len(standard_tableaux(shape)[1]))
    swaps = {
        pair: representation(shape, transposition(*pair))
        for pair in ((1, 2), (3, 4), (1, 3), (2, 4), (1, 4), (2, 3))
    }
    p = (2 * identity - swaps[1, 3]) @ (2 * identity - swaps[2, 4])
    r = (
        (2 * identity - swaps[1, 4])
        @ (2 * identity - swaps[2, 3])
        @ swaps[1, 2]
        @ swaps[3, 4]
    )
    return p, r, swaps[1, 2], swaps[3, 4]


def blocks():
    data = {shape: local_data(shape) for shape in PARTITIONS}
    out = []
    for shapes in itertools.product(PARTITIONS, repeat=3):
        first, second, third = (data[shape] for shape in shapes)
        p = kron3(first[0], second[0], third[0])
        r = kron3(first[1], second[1], third[1])
        swap12 = kron3(first[2], second[2], third[2])
        swap34 = kron3(first[3], second[3], third[3])
        out.append(
            (
                shapes,
                (p - r + (p - r).T) / 2,
                swap12,
                swap34,
                swap12 @ swap34,
            )
        )
    return out


def worst_eigenvalue(parameters: np.ndarray, all_blocks) -> float:
    lambda_pair, lambda_both = parameters
    worst = np.inf
    for _, operator, swap12, swap34, swap_both in all_blocks:
        shifted = (
            operator
            + lambda_pair * (swap12 + swap34)
            + lambda_both * swap_both
        )
        worst = min(worst, np.linalg.eigvalsh(shifted)[0])
    return float(worst)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=float, default=100)
    args = parser.parse_args()
    all_blocks = blocks()

    result = differential_evolution(
        lambda point: -worst_eigenvalue(point, all_blocks),
        [(-args.bound, args.bound), (-args.bound, args.bound)],
        tol=1e-10,
        polish=True,
        seed=0,
    )
    point = result.x
    value = worst_eigenvalue(point, all_blocks)
    print("best", point, "worst eigenvalue", value)
    failures = []
    for shapes, operator, swap12, swap34, swap_both in all_blocks:
        shifted = (
            operator
            + point[0] * (swap12 + swap34)
            + point[1] * swap_both
        )
        minimum = np.linalg.eigvalsh(shifted)[0]
        if minimum < value + 1e-7:
            failures.append((shapes, minimum))
    print("active", failures)


if __name__ == "__main__":
    main()
