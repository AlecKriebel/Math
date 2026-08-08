#!/usr/bin/env python3
"""Exact labelled-chain check of the order-four orbit profile in the note."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    x = sp.symbols("x", real=True)
    a = sp.Rational(7, 10)
    midpoint_cross = sp.Rational(3, 20)
    displacement = x / 20
    weights = [
        [0, a, midpoint_cross + displacement, midpoint_cross - displacement],
        [a, 0, midpoint_cross - displacement, midpoint_cross + displacement],
        [midpoint_cross + displacement, midpoint_cross - displacement, 0, a],
        [midpoint_cross - displacement, midpoint_cross + displacement, a, 0],
    ]

    size = 4
    full = (1 << size) - 1
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.zeros(len(states))
    boundary = sp.zeros(len(states), 1)

    for state in states:
        row = index[state]
        for target in range(size):
            context = state & ~(1 << target)
            mass = sum(
                (
                    weights[target][source]
                    for source in range(size)
                    if context >> source & 1
                ),
                sp.Integer(0),
            )
            mutant_probability = 2 * mass / (1 + mass)
            if state >> target & 1:
                next_state = context
                rate = 1 - mutant_probability
            else:
                next_state = state | (1 << target)
                rate = mutant_probability
            matrix[row, row] += rate
            if next_state == full:
                boundary[row] += rate
            elif next_state:
                matrix[row, index[next_state]] -= rate

    committor = matrix.inv() * boundary
    fixation = sp.factor(
        sum((committor[index[1 << vertex]] for vertex in range(size)), sp.Integer(0))
        / size
    )
    expected = (101 * x**2 - 71629) / (2 * (69 * x**2 - 85241))
    assert sp.factor(fixation - expected) == 0
    second = sp.factor(sp.diff(fixation, x, 2))
    expected_second = 3666940 * (207 * x**2 + 85241) / (69 * x**2 - 85241) ** 3
    assert sp.factor(second - expected_second) == 0
    print("PASS: exact K4 transposition-orbit profile and curvature")
    print("fixation =", fixation)
    print("second_derivative =", second)


if __name__ == "__main__":
    main()
