#!/usr/bin/env python3
"""Exact algebra checks for the cubic optional-potential reduction.

This verifier does not claim universal cubic feasibility.  It proves the
optional-stopping normalization, reconstructs every dB drift row directly,
and gives a two-row rational contradiction to the degree-one strengthening.
"""

from __future__ import annotations

import sympy as sp


def optional_stopping_normalization() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    initial_average = sp.Rational(1, 2) * (1 + 1 / n)
    full_value = 2 ** (1 - n)
    bound = sp.factor((1 - initial_average) / (1 - full_value))
    baseline = sp.factor(
        (n - 1) * 2 ** (n - 2) / (n * (2 ** (n - 1) - 1))
    )
    assert sp.simplify(bound - baseline) == 0


def direct_drift_row(weights, mask, coefficients, subsets):
    """Return the common-positive-factor-cleared dB drift over QQ."""
    n = len(weights)
    degrees = [sum(row) for row in weights]

    def set_value(state):
        return 1 + sum(
            coefficient
            for coefficient, subset in zip(coefficients, subsets)
            if all(state >> vertex & 1 for vertex in subset)
        )

    value = set_value(mask)
    drift = 0
    for vertex in range(n):
        mutant_mass = sum(
            weights[vertex][source]
            for source in range(n) if mask >> source & 1
        )
        x = sp.cancel(mutant_mass / degrees[vertex])
        if mask >> vertex & 1:
            loss = sp.cancel((1 - x) / (1 + x))
            drift += 2 * loss * (2 * set_value(mask & ~(1 << vertex)) - value)
        else:
            gain = sp.cancel(2 * x / (1 + x))
            drift += gain * (set_value(mask | (1 << vertex)) - 2 * value)
    return sp.factor(drift)


def degree_one_triangle_obstruction() -> None:
    # Lexicographic edge weights (01,02,12)=(1,1,2).
    weights = (
        (sp.Integer(0), sp.Integer(1), sp.Integer(1)),
        (sp.Integer(1), sp.Integer(0), sp.Integer(2)),
        (sp.Integer(1), sp.Integer(2), sp.Integer(0)),
    )
    a0, a1, a2 = sp.symbols("a0 a1 a2", real=True)
    coefficients = (a0, a1, a2)
    subsets = ((0,), (1,), (2,))
    substitution = {a2: 1 - a0 - a1}

    singleton_zero = sp.factor(
        direct_drift_row(weights, 1 << 0, coefficients, subsets).subs(substitution)
    )
    complement_zero = sp.factor(
        direct_drift_row(weights, (1 << 1) | (1 << 2), coefficients, subsets)
        .subs(substitution)
    )
    assert sp.simplify(singleton_zero + (7 * a0 - 3) / 2) == 0
    assert sp.simplify(complement_zero - 2 * (5 * a0 - 3) / 5) == 0
    # Nonnegative drift would require simultaneously a0<=3/7 and a0>=3/5.
    assert sp.Rational(3, 5) > sp.Rational(3, 7)


def polynomial_row_cross_check() -> None:
    # A nontrivial rational cubic set function on a rational K4.  The point
    # is identity of the direct update calculation and the displayed generic
    # add/delete row, not positivity of this arbitrary coefficient choice.
    weights = tuple(tuple(sp.Integer(value) for value in row) for row in (
        (0, 1, 2, 3),
        (1, 0, 5, 7),
        (2, 5, 0, 11),
        (3, 7, 11, 0),
    ))
    subsets = tuple(
        subset
        for order in range(1, 4)
        for subset in __import__("itertools").combinations(range(4), order)
    )
    coefficients = tuple(sp.Rational(i - 7, 13) for i in range(len(subsets)))
    for mask in range(1, 15):
        direct = direct_drift_row(weights, mask, coefficients, subsets)
        # Reconstruct the same row by literal full F differences.  The
        # common 2^(-k-1)/n factor is deliberately omitted on both sides.
        n = 4

        def G(state):
            return 1 + sum(
                coefficient
                for coefficient, subset in zip(coefficients, subsets)
                if all(state >> vertex & 1 for vertex in subset)
            )

        degrees = [sum(row) for row in weights]
        literal = 0
        for vertex in range(n):
            mutant_mass = sum(
                weights[vertex][source]
                for source in range(n) if mask >> source & 1
            )
            x = sp.Rational(mutant_mass, degrees[vertex])
            if mask >> vertex & 1:
                literal += 2 * (1 - x) / (1 + x) * (
                    2 * G(mask & ~(1 << vertex)) - G(mask)
                )
            else:
                literal += 2 * x / (1 + x) * (
                    G(mask | (1 << vertex)) - 2 * G(mask)
                )
        assert sp.factor(direct - literal) == 0


def main() -> None:
    optional_stopping_normalization()
    degree_one_triangle_obstruction()
    polynomial_row_cross_check()
    print("PASS: exact optional-stopping normalization")
    print("PASS: exact dB polynomial drift rows")
    print("PASS: degree-one potential refuted by triangle (1,1,2)")
    print("OPEN: universal degree-three feasibility")


if __name__ == "__main__":
    main()
