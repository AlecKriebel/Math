#!/usr/bin/env python3
"""Exact coefficient certificate for a three-vertex dB inequality.

For an arbitrary positively weighted triangle L, let

    alpha(r) = (1/3) sum_i phi_i^dB(r),
    H        = sum_i 1/d_i,
    I(s)     = sum_i phi_i^dB(s)/d_i.

This script derives the six transient-state equations directly from the dB
rule and proves

    H * (alpha(r) - (1 - 1/r)) <= I(1/r) / r**2

for r >= 3/2.  The certificate is coefficient positivity after substituting
r = 3/2 + u.  It also checks that the threshold is sharp for the singular
triangle with edge weights (delta, 1, delta).
"""

from __future__ import annotations

from collections import defaultdict

import sympy as sp


r, u = sp.symbols("r u", positive=True)
a, b, c, delta = sp.symbols("a b c delta", positive=True)


def db_singletons(fitness: sp.Expr) -> list[sp.Expr]:
    """Solve the dB absorbing equations on edge weights a,b,c exactly."""
    weights = (
        (sp.Integer(0), a, b),
        (a, sp.Integer(0), c),
        (b, c, sp.Integer(0)),
    )
    transient = list(range(1, 7))
    index = {mask: position for position, mask in enumerate(transient)}
    matrix = sp.eye(6)
    rhs = sp.zeros(6, 1)

    for mask in transient:
        mutant = [(mask >> vertex) & 1 for vertex in range(3)]
        transitions: dict[int, sp.Expr] = defaultdict(lambda: sp.Integer(0))
        for target in range(3):
            denominator = sum(
                weights[parent][target]
                * (fitness if mutant[parent] else 1)
                for parent in range(3)
            )
            for parent in range(3):
                if not weights[parent][target]:
                    continue
                probability = (
                    sp.Rational(1, 3)
                    * weights[parent][target]
                    * (fitness if mutant[parent] else 1)
                    / denominator
                )
                if mutant[parent]:
                    new_mask = mask | (1 << target)
                else:
                    new_mask = mask & ~(1 << target)
                transitions[new_mask] += probability

        row = index[mask]
        for new_mask, probability in transitions.items():
            if new_mask == 7:
                rhs[row] += probability
            elif new_mask:
                matrix[row, index[new_mask]] -= probability

    solution = list(next(iter(sp.linsolve((matrix, rhs)))))
    return [sp.cancel(solution[index[1 << vertex]]) for vertex in range(3)]


def main() -> None:
    forward = db_singletons(r)
    reverse = db_singletons(1 / r)
    degrees = (a + b, a + c, b + c)
    alpha = sp.cancel(sum(forward) / 3)
    harmonic_degree = sum(1 / degree for degree in degrees)
    inverse_weighted_reverse = sum(
        value / degree for value, degree in zip(reverse, degrees)
    )

    difference = sp.cancel(
        inverse_weighted_reverse / r**2
        - harmonic_degree * (alpha - (1 - 1 / r))
    )
    numerator, denominator = sp.together(difference).as_numer_denom()

    denominator_poly = sp.Poly(sp.expand(denominator), r, a, b, c)
    assert all(coefficient > 0 for _, coefficient in denominator_poly.terms())

    shifted_numerator = sp.Poly(
        sp.expand(numerator.subs(r, u + sp.Rational(3, 2))),
        u,
        a,
        b,
        c,
    )
    assert len(shifted_numerator.terms()) == 261
    assert all(coefficient > 0 for _, coefficient in shifted_numerator.terms())

    # Sharpness: AB=BC=delta and AC=1.  Divide by H before taking the
    # singular limit, since H itself diverges like 1/(2 delta).
    singular_substitution = {a: delta, b: 1, c: delta}
    singular_alpha = sp.cancel(
        alpha.subs(singular_substitution, simultaneous=True)
    )
    singular_ratio = sp.cancel(
        (inverse_weighted_reverse / harmonic_degree).subs(
            singular_substitution, simultaneous=True
        )
    )
    assert sp.factor(
        sp.limit(singular_alpha, delta, 0, dir="+") - sp.Rational(1, 3)
    ) == 0
    assert sp.factor(sp.limit(singular_ratio, delta, 0, dir="+")) == 0
    singular_normalized_difference = sp.factor(
        sp.limit(
            difference.subs(singular_substitution, simultaneous=True)
            / harmonic_degree.subs(singular_substitution, simultaneous=True),
            delta,
            0,
            dir="+",
        )
    )
    assert singular_normalized_difference == (2 * r - 3) / (3 * r)

    print(
        "PASS: arbitrary weighted-triangle dB threshold certificate "
        "(261 positive shifted coefficients)"
    )


if __name__ == "__main__":
    main()
