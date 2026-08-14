#!/usr/bin/env python3
"""Exact audit of the cross-fitness forest and neutral-pole checkpoint.

This is a fixed symbolic sanity check on a weighted three-path.  It does not
enumerate graphs, forests, or parameter values.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp


r, t = sp.symbols("r t", positive=True)


def subset_data(rule: str):
    """Return the transient Dirichlet matrix and fixation column on P3."""

    zero = sp.Integer(0)
    one = sp.Integer(1)
    weights = (
        (zero, one, zero),
        (one, zero, t),
        (zero, t, zero),
    )
    degrees = tuple(sum(row, zero) for row in weights)
    states = tuple(
        frozenset(choice)
        for size in (1, 2)
        for choice in combinations(range(3), size)
    )
    index = {state: position for position, state in enumerate(states)}
    laplacian = sp.zeros(len(states))
    fixation = sp.zeros(len(states), 1)

    for state, row_index in index.items():
        changes = {}
        for target in range(3):
            mutant_weight = sum(
                (weights[source][target] for source in state), zero
            )
            resident_weight = degrees[target] - mutant_weight

            if rule == "Bd":
                if target not in state:
                    rate = r * sum(
                        (
                            weights[source][target] / degrees[source]
                            for source in state
                        ),
                        zero,
                    )
                    next_state = frozenset(set(state) | {target})
                else:
                    rate = sum(
                        (
                            weights[source][target] / degrees[source]
                            for source in range(3)
                            if source not in state
                        ),
                        zero,
                    )
                    next_state = frozenset(set(state) - {target})
            elif rule == "dB":
                denominator = r * mutant_weight + resident_weight
                if target not in state:
                    rate = r * mutant_weight / denominator
                    next_state = frozenset(set(state) | {target})
                else:
                    rate = resident_weight / denominator
                    next_state = frozenset(set(state) - {target})
            else:
                raise ValueError(rule)

            if rate:
                changes[next_state] = changes.get(next_state, zero) + rate

        laplacian[row_index, row_index] = sum(changes.values(), zero)
        for next_state, rate in changes.items():
            if len(next_state) == 3:
                fixation[row_index] += rate
            elif next_state:
                laplacian[row_index, index[next_state]] -= rate

    selector = sp.zeros(len(states), 1)
    for vertex in range(3):
        selector[index[frozenset({vertex})]] = sp.Rational(1, 3)
    return states, laplacian, fixation, selector


def complete_bd():
    return r**2 / (r**2 + r + 1)


def complete_db():
    return 2 * r / (3 * (r + 1))


def audit_rule(rule: str):
    states, laplacian, fixation, selector = subset_data(rule)
    determinant = sp.factor(laplacian.det())
    marked_numerator = sp.factor(
        (selector.T * laplacian.adjugate() * fixation)[0]
    )
    committor = laplacian.inv() * fixation
    fixation_probability = sp.factor((selector.T * committor)[0])
    assert determinant != 0
    assert sp.factor(marked_numerator / determinant - fixation_probability) == 0
    return states, laplacian, fixation_probability, determinant, marked_numerator


def main() -> None:
    _, _, rho_b, delta_b, numerator_b = audit_rule("Bd")
    _, _, rho_d, delta_d, numerator_d = audit_rule("dB")

    expected_b = r**2 * (
        3 * r**3 * t**3
        + 6 * r**3 * t**2
        + 3 * r**3 * t
        + 6 * r**2 * t**3
        + 12 * r**2 * t**2
        + 6 * r**2 * t
        + r * t**4
        + 5 * r * t**3
        + 9 * r * t**2
        + 5 * r * t
        + r
        + 2 * t**4
        + 4 * t**3
        + 6 * t**2
        + 4 * t
        + 2
    ) / (
        3
        * (r + 2)
        * (r**2 * t + r**2 + r * t + t**2 + t)
        * (r**2 * t**2 + r**2 * t + r * t + t + 1)
    )
    expected_d = (5 * r**2 * t + 3 * r * t**2 + 3 * r + t) / (
        9 * (r + t) * (r * t + 1)
    )
    assert sp.factor(rho_b - expected_b) == 0
    assert sp.factor(rho_d - expected_d) == 0

    # Exact neutral forest derivatives after the determinant quotient.
    weak_b = sp.factor(sp.diff(rho_b, r).subs(r, 1))
    weak_d = sp.factor(sp.diff(rho_d, r).subs(r, 1))
    assert weak_b == 20 * t * (t + 1) ** 2 / (9 * (t**2 + 3 * t + 1) ** 2)
    assert weak_d == 4 * t / (9 * (t + 1) ** 2)
    assert sp.diff(complete_bd(), r).subs(r, 1) == sp.Rational(1, 3)
    assert sp.diff(complete_db(), r).subs(r, 1) == sp.Rational(1, 6)

    # The dB likelihood score is indicator(up)-W_j(A)/d_j.
    x, degree = sp.symbols("x degree", positive=True)
    up_rate = r * x / (degree + (r - 1) * x)
    down_rate = (degree - x) / (degree + (r - 1) * x)
    assert sp.simplify(
        sp.diff(sp.log(up_rate), r).subs(r, 1) - (1 - x / degree)
    ) == 0
    assert sp.simplify(
        sp.diff(sp.log(down_rate), r).subs(r, 1) + x / degree
    ) == 0

    # Check the normalized endpoint clearing before any specialization of r.
    kappa_b = complete_bd()
    kappa_d = complete_db()
    gain_b = sp.factor(rho_b / kappa_b - 1)
    gain_d = sp.factor(rho_d / kappa_d - 1)
    support = sp.factor(gain_d + (r - 1) * gain_b)
    clearing = sp.factor(
        kappa_b * delta_b * numerator_d
        + (r - 1) * kappa_d * delta_d * numerator_b
        - r * kappa_b * kappa_d * delta_b * delta_d
    )
    assert sp.factor(clearing - kappa_b * kappa_d * delta_b * delta_d * support) == 0

    # A compact exact P3 sign check, with no parameter sweep.
    expected_gain_b = (r - 1) / ((r + 2) * (2 * r**2 + r + 2))
    expected_gain_d = -(r - 1) / (6 * r)
    assert sp.factor(gain_b.subs(t, 1) - expected_gain_b) == 0
    assert sp.factor(gain_d.subs(t, 1) - expected_gain_d) == 0
    expected_support = -(
        (r - 1) * (2 * r**3 - r**2 + 10 * r + 4)
    ) / (6 * r * (r + 2) * (2 * r**2 + r + 2))
    assert sp.factor(support.subs(t, 1) - expected_support) == 0

    # The hybrid evaluation point and the exact ordinary-leaf pole.
    hybrid = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    lo = sp.Rational(3, 2)
    hi = sp.Rational(151, 100)
    assert sp.Poly(hybrid, r).count_roots(lo, hi) == 1
    assert hybrid.subs(r, lo) > 0 > hybrid.subs(r, hi)

    sigma, lam = sp.symbols("sigma lam", positive=True)
    pair_leaf_b = 2 * (sigma - 1) / (1 + sigma * (r**2 - 1)) + lam / (r - 1)
    pair_leaf_d = 2 * (r * (2 - r) - sigma) / (
        sigma + 2 * r * (r - 1)
    ) - lam
    assert sp.limit((r - 1) * pair_leaf_b, r, 1, dir="+") == lam
    assert sp.simplify(
        sp.limit(pair_leaf_d, r, 1, dir="+")
        - (2 * (1 - sigma) / sigma - lam)
    ) == 0

    print("PASS exact Bd/dB transient Dirichlet systems")
    print("PASS exact adjugate two-root forest ratios")
    print("PASS exact neutral derivatives and dB likelihood scores")
    print("PASS exact normalized endpoint forest clearing")
    print("PASS unique hybrid root in (3/2,151/100)")
    print("PASS exact pair-leaf neutral pole")
    print("NO graph or forest enumeration performed")


if __name__ == "__main__":
    main()
