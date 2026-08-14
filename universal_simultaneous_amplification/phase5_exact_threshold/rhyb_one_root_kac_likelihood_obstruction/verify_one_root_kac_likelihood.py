#!/usr/bin/env python3
"""Exact replay for the active one-root scalar likelihood obstruction.

This script checks symbolic identities and one explicitly named weighted
three-path.  It performs no graph enumeration or kernel optimization and
does not claim the open D-KAC sign.
"""

from __future__ import annotations

from collections import defaultdict

import sympy as sp


R = sp.symbols("r", positive=True)
X = sp.symbols("x", nonnegative=True)
LO = sp.Rational(3, 2)
HI = sp.Rational(151, 100)

# The graph u--1--v--17--w.  Scaling all weights is immaterial.
WEIGHTS = (
    (sp.Integer(0), sp.Integer(1), sp.Integer(0)),
    (sp.Integer(1), sp.Integer(0), sp.Integer(17)),
    (sp.Integer(0), sp.Integer(17), sp.Integer(0)),
)


def fixation_vector(rule: str, fitness: sp.Expr) -> tuple[sp.Expr, ...]:
    """Solve the exact six transient states of the original Moran chain."""

    order = 3
    full = (1 << order) - 1
    degree = [sum(row) for row in WEIGHTS]
    states = list(range(1, full))
    index = {state: row for row, state in enumerate(states)}
    matrix = sp.eye(len(states))
    rhs = sp.zeros(len(states), 1)

    for state in states:
        mutant = [(state >> vertex) & 1 for vertex in range(order)]
        transition: dict[int, sp.Expr] = defaultdict(lambda: sp.Integer(0))

        if rule == "Bd":
            total_fitness = order + (fitness - 1) * sum(mutant)
            for parent in range(order):
                for target in range(order):
                    if not WEIGHTS[parent][target]:
                        continue
                    probability = (
                        (fitness if mutant[parent] else 1)
                        * WEIGHTS[parent][target]
                        / (total_fitness * degree[parent])
                    )
                    destination = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transition[destination] += probability
        elif rule == "dB":
            for target in range(order):
                denominator = sum(
                    WEIGHTS[parent][target]
                    * (fitness if mutant[parent] else 1)
                    for parent in range(order)
                )
                for parent in range(order):
                    if not WEIGHTS[parent][target]:
                        continue
                    probability = (
                        WEIGHTS[parent][target]
                        * (fitness if mutant[parent] else 1)
                        / (order * denominator)
                    )
                    destination = (
                        state | (1 << target)
                        if mutant[parent]
                        else state & ~(1 << target)
                    )
                    transition[destination] += probability
        else:
            raise ValueError(rule)

        row = index[state]
        for destination, probability in transition.items():
            if destination == full:
                rhs[row] += probability
            elif destination:
                matrix[row, index[destination]] -= probability

    solution = next(iter(sp.linsolve((matrix, rhs))))
    return tuple(sp.factor(sp.cancel(value)) for value in solution)


def active_excess_audit() -> None:
    """Derive both excesses and prove positivity on [3/2,151/100]."""

    bd = fixation_vector("Bd", R)
    db = fixation_vector("dB", R)
    singleton_masks = (1, 2, 4)
    rho_b = sp.factor(sum(bd[mask - 1] for mask in singleton_masks) / 3)
    rho_d = sp.factor(sum(db[mask - 1] for mask in singleton_masks) / 3)
    baseline = (R - 1) / R
    beta_b = sp.factor(rho_b - baseline)
    beta_d = sp.factor(rho_d - baseline)

    n_b = (
        -155450 * R**4
        - 77725 * R**3
        + 532446 * R**2
        + 16524 * R
        + 33048
    )
    d_b = (
        3
        * R
        * (R + 2)
        * (18 * R**2 + 17 * R + 306)
        * (306 * R**2 + 17 * R + 18)
    )
    n_d = -68 * R**3 - 1587 * R**2 + 2474 * R + 153
    d_d = 9 * R * (R + 17) * (17 * R + 1)
    assert sp.factor(beta_b - n_b / d_b) == 0
    assert sp.factor(beta_d - n_d / d_d) == 0

    # After r=3/2+x, every coefficient of each derivative is negative.
    shifted_b_prime = sp.Poly(sp.expand(sp.diff(n_b, R).subs(R, LO + X)), X)
    shifted_d_prime = sp.Poly(sp.expand(sp.diff(n_d, R).subs(R, LO + X)), X)
    assert all(coefficient < 0 for coefficient in shifted_b_prime.all_coeffs())
    assert all(coefficient < 0 for coefficient in shifted_d_prime.all_coeffs())
    assert n_b.subs(R, HI) == sp.Rational(392527662741, 2000000)
    assert n_d.subs(R, HI) == sp.Rational(4512579, 125000)
    assert n_b.subs(R, HI) > 0
    assert n_d.subs(R, HI) > 0

    assert beta_b.subs(R, LO) == sp.Rational(1275, 26474)
    assert beta_d.subs(R, LO) == sp.Rational(170, 17649)

    # Reciprocal-fitness singleton fixation is the stationary dual atom.
    # Its strict positivity also follows directly from irreducibility; the
    # exact values below independently audit it at the rational endpoint.
    bd_reciprocal = fixation_vector("Bd", 1 / LO)
    db_reciprocal = fixation_vector("dB", 1 / LO)
    assert all(bd_reciprocal[mask - 1] > 0 for mask in singleton_masks)
    assert all(db_reciprocal[mask - 1] > 0 for mask in singleton_masks)


def event_clock_and_departure_audit() -> None:
    """Check the algebraic normalizations in the two event formulas."""

    r, t_i, total, rank, order, baseline = sp.symbols(
        "r t_i T k s p", positive=True
    )
    reward = rank / order - baseline

    # Bd: root exit q=r t_i and graphical attempt rate r T(A).
    assert sp.factor(r * t_i * reward / (r * total) - t_i * reward / total) == 0
    # dB: root exit q=1 and event rate |A|.
    assert sp.factor(reward / rank - (rank - order * baseline) / (order * rank)) == 0

    degree = [sum(row) for row in WEIGHTS]
    transition = [
        [sp.Rational(WEIGHTS[i][j], degree[i]) for j in range(3)]
        for i in range(3)
    ]
    temperature_center = sum(transition[source][1] for source in range(3))
    assert temperature_center == 2
    assert sp.factor(r * temperature_center - 2 * r) == 0


def singular_mass_audit() -> None:
    """Verify the positive dB two-leaf burst missing from one Bd arrow."""

    z = sp.Rational(1, 18)
    geometric_hit = lambda value: value / (R - (R - 1) * value)
    both = sp.factor(1 - geometric_hit(z) - geometric_hit(1 - z))
    claimed = sp.factor(
        (R**2 - 1)
        * z
        * (1 - z)
        / ((R - (R - 1) * z) * (1 + (R - 1) * z))
    )
    assert sp.factor(both - claimed) == 0
    assert both.subs(R, LO) > 0
    assert both.subs(R, HI) > 0

    # Set-theoretic first-jump support at the centre root.
    center = {1}
    leaves = {0, 2}
    bd_destinations = set()
    for source in leaves:
        bd_destinations.add(frozenset({source}))
        bd_destinations.add(frozenset(center | {source}))
    assert frozenset(leaves) not in bd_destinations


def likelihood_moment_audit() -> None:
    """Check the general repeated-source moment and active L2 divergence."""

    r, z, ell, exponent, n = sp.symbols(
        "r z ell q n", positive=True
    )
    geometric_ratio = (r - 1) / r
    def term(index: sp.Expr) -> sp.Expr:
        return (
            sp.Rational(1, 1)
            / r
            * geometric_ratio ** (index - 1)
            * z**index
            * (ell / z) ** (exponent * index)
        )

    first_term = ell**exponent * z ** (1 - exponent) / r
    term_ratio = geometric_ratio * ell**exponent * z ** (1 - exponent)
    assert sp.simplify(term(1) - first_term) == 0
    assert sp.simplify(sp.powsimp(term(n + 1) / term(n), force=True) - term_ratio) == 0

    witness_ratio = sp.factor(
        ((R - 1) / R)
        * sp.Rational(1, 2) ** 2
        / sp.Rational(1, 18)
    )
    assert sp.factor(witness_ratio - 9 * (R - 1) / (2 * R)) == 0
    assert sp.factor(witness_ratio - 1) == (7 * R - 9) / (2 * R)
    assert (7 * LO - 9) > 0

    # The nth all-weak-source contribution to E_C Lambda^2.
    def explicit_term(index: sp.Expr) -> sp.Expr:
        return (
            1
            / R
            * ((R - 1) / R) ** (index - 1)
            * sp.Rational(1, 18) ** index
            * 9 ** (2 * index)
        )

    assert sp.simplify(explicit_term(1) - sp.Rational(9, 2) / R) == 0
    assert sp.simplify(
        explicit_term(n + 1) / explicit_term(n) - witness_ratio
    ) == 0


def signed_hellinger_audit() -> None:
    """Verify the exact remainder and exhibit both of its signs."""

    c1, c2, a1, a2, y1, y2 = sp.symbols(
        "c1 c2 a1 a2 y1 y2", real=True
    )
    mean_l = c1 * a1**2 * y1 + c2 * a2**2 * y2
    mean_c = c1 * y1 + c2 * y2
    hellinger = c1 * a1 * y1 + c2 * a2 * y2
    remainder = (
        sp.Rational(1, 2)
        * (
            c1 * c2 * y1 * y2 * (a1 - a2) ** 2
            + c2 * c1 * y2 * y1 * (a2 - a1) ** 2
        )
    )
    assert sp.expand(mean_l * mean_c - hellinger**2 - remainder) == 0

    # A normalized two-atom likelihood: E_C Lambda=1.
    normalized = {
        c1: sp.Rational(3, 8),
        c2: sp.Rational(5, 8),
        a1: sp.Rational(3, 2),
        a2: sp.Rational(1, 2),
    }
    assert sp.factor(
        (c1 * a1**2 + c2 * a2**2).subs(normalized) - 1
    ) == 0

    positive_reward = sp.factor(remainder.subs(normalized | {y1: 1, y2: 1}))
    signed_reward = sp.factor(remainder.subs(normalized | {y1: 2, y2: -1}))
    assert positive_reward > 0
    assert signed_reward < 0
    assert mean_l.subs(normalized | {y1: 2, y2: -1}) > 0
    assert mean_c.subs(normalized | {y1: 2, y2: -1}) > 0

    singleton_reward = sp.factor(sp.Rational(1, 3) - (R - 1) / R)
    doubleton_reward = sp.factor(sp.Rational(2, 3) - (R - 1) / R)
    assert sp.factor(singleton_reward - (3 - 2 * R) / (3 * R)) == 0
    assert sp.factor(doubleton_reward - (3 - R) / (3 * R)) == 0
    assert singleton_reward.subs(R, HI) < 0
    assert doubleton_reward.subs(R, HI) > 0


def main() -> None:
    event_clock_and_departure_audit()
    active_excess_audit()
    singular_mass_audit()
    likelihood_moment_audit()
    signed_hellinger_audit()
    print("PASS: exact Bd/dB Kac event-clock normalizations")
    print("PASS: active weighted-P3 excesses on 3/2 <= r <= 151/100")
    print("PASS: exact macro-cycle support singularity")
    print("PASS: canonical marked likelihood has infinite L2 moment")
    print("PASS: signed Hellinger remainder is indefinite")
    print("OPEN: universal one-root D-KAC sign")


if __name__ == "__main__":
    main()
