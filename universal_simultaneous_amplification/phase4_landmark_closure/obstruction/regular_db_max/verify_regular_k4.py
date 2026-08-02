#!/usr/bin/env python3
"""Exact certificate: K4 maximizes r=2 dB fixation among regular graphs.

The verifier constructs all labelled type-changing dB rates symbolically and
checks the proposed fixation function in every transient state.  It then
checks the exact tangent-square identity that proves the comparison.
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    a, b, c = sp.symbols("a b c", positive=True)
    weights = sp.Matrix(
        [
            [0, a, b, c],
            [a, 0, c, b],
            [b, c, 0, a],
            [c, b, a, 0],
        ]
    )
    variables = (a, b, c)
    edge_type = {
        frozenset((0, 1)): a,
        frozenset((2, 3)): a,
        frozenset((0, 2)): b,
        frozenset((1, 3)): b,
        frozenset((0, 3)): c,
        frozenset((1, 2)): c,
    }

    capital_a = sum(4 * x / (4 + x) for x in variables)
    value_one = sp.cancel(4 * capital_a / (4 + 5 * capital_a))
    value_three = sp.cancel(4 * (1 + capital_a) / (4 + 5 * capital_a))

    values = {0: sp.Integer(0), 15: sp.Integer(1)}
    for state in range(1, 15):
        cardinality = bin(state).count("1")
        if cardinality == 1:
            values[state] = value_one
        elif cardinality == 3:
            values[state] = value_three
        else:
            mutant_pair = frozenset(i for i in range(4) if (state >> i) & 1)
            x = edge_type[mutant_pair]
            upward_probability = 2 * (1 + x) / (4 + x)
            values[state] = sp.cancel(
                upward_probability * value_three
                + (1 - upward_probability) * value_one
            )

    # Since a+b+c=1, substitute c=1-a-b after building rates.  Every row is
    # checked directly from death--birth updating at mutant fitness two.
    substitution = {c: 1 - a - b}
    checked = 0
    for state in range(1, 15):
        mutant = [(state >> i) & 1 for i in range(4)]
        drift = 0
        for target in range(4):
            mutant_mass = sum(
                weights[target, source] * mutant[source] for source in range(4)
            )
            resident_mass = sum(
                weights[target, source] * (1 - mutant[source])
                for source in range(4)
            )
            denominator = 2 * mutant_mass + resident_mass
            if mutant[target]:
                changing_rate = resident_mass / denominator
                new_state = state & ~(1 << target)
            else:
                changing_rate = 2 * mutant_mass / denominator
                new_state = state | (1 << target)
            drift += changing_rate * (values[new_state] - values[state])
        assert sp.factor(sp.cancel(drift).subs(substitution)) == 0
        checked += 1

    # Strict concavity is retained as an exact sum of rational squares.  This
    # identity is the tangent inequality for x/(4+x) at x=1/3.
    tangent_slack = sum(
        4 * (3 * x - 1) ** 2 / (169 * (4 + x)) for x in variables
    )
    identity = sp.cancel(
        sp.Rational(3, 13)
        - sum(x / (4 + x) for x in variables)
        - tangent_slack
    )
    assert sp.factor(identity.subs(substitution)) == 0

    baseline = sp.Rational(3, 7)
    gap = sp.cancel(baseline - value_one)
    gap_certificate = sp.cancel(
        16
        * sum((3 * x - 1) ** 2 / (4 + x) for x in variables)
        / (91 * (4 + 5 * capital_a))
    )
    assert sp.factor((gap - gap_certificate).subs(substitution)) == 0
    assert sp.cancel(value_one.subs({a: sp.Rational(1, 3), b: sp.Rational(1, 3), c: sp.Rational(1, 3)})) == baseline

    print(f"PASS: {checked} labelled transient dB equations checked exactly")
    print("rho_dB(G,2) = 4 A/(4+5 A), A=sum_x 4x/(4+x)")
    print("PASS: complete-graph gap is an exact positive rational-square sum")


if __name__ == "__main__":
    main()
