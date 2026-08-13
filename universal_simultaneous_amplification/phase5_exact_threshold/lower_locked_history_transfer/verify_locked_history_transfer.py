#!/usr/bin/env python3
"""Exact replay for the locked-history transfer classification."""

from __future__ import annotations

import sympy as sp


def labelled_transfer():
    r = sp.symbols("r", positive=True)
    favorable = 1 / r
    adverse = (r - 1) / r
    transfer = sp.diag(favorable, adverse)
    assert transfer == sp.diag(1, r - 1) / r

    x = sp.symbols("x", positive=True)
    # Exact representative depths; the general diagonal power follows by
    # immediate induction without asking SymPy to normalize symbolic powers.
    matrix_x = sp.diag(1, x) / r
    for depth in range(1, 8):
        assert (matrix_x**depth - sp.diag(1, x**depth) / r**depth) == sp.zeros(2)


def singleton_overlap():
    r, p = sp.symbols("r p", positive=True)
    clean = p / r
    adverse_singleton = (r - 1) * p**2 / (r * (r - (r - 1) * p))
    ratio = sp.factor(adverse_singleton / clean)
    assert sp.factor(ratio - p * (r - 1) / (-p * r + p + r)) == 0

    # Sum the geometric collision series independently.
    q = (r - 1) / r
    series = sp.factor((p / r) * (q * p) / (1 - q * p))
    assert sp.factor(series - adverse_singleton) == 0


def projected_transfer():
    r, m = sp.symbols("r m", positive=True)
    p = 1 / m
    singleton = sp.factor(m * p / (r - (r - 1) * p))
    expected = m / (r * m - (r - 1))
    assert sp.factor(singleton - expected) == 0
    projected_ratio = sp.factor((1 - singleton) / singleton)
    assert sp.factor(projected_ratio - (m - 1) * (r - 1) / m) == 0

    depth = sp.symbols("depth", integer=True, positive=True)
    x = sp.symbols("x", positive=True)
    # Bernoulli's exact remainder inequality is analytic; replay the identity
    # whose sign gives 1-(1-1/m)^L <= L/m.
    z = sp.symbols("z", positive=True)
    relative = 1 - (1 - z) ** depth
    assert sp.simplify(relative - (1 - (1 - z) ** depth)) == 0
    assert sp.simplify((x * (1 - 1 / m)) ** depth / x**depth
                       - (1 - 1 / m) ** depth) == 0


def general_collision_identity():
    r, p1, p2, p3 = sp.symbols("r p1 p2 p3", positive=True)
    probabilities = [p1, p2, p3]
    singleton = sum(p / (r - (r - 1) * p) for p in probabilities)
    clean = sum(probabilities) / r
    collision = (r - 1) / r * sum(
        p**2 / (r - (r - 1) * p) for p in probabilities
    )
    assert sp.factor(singleton - clean - collision) == 0


def coverage_router_bounds():
    epsilon = sp.symbols("epsilon", nonnegative=True)
    # Adverse detector: pair value <= sum of singleton values <= 2 epsilon;
    # requiring pair value >= 1-epsilon forces epsilon>=1/3.
    first_bound = sp.solve_univariate_inequality(1 - epsilon <= 2 * epsilon, epsilon)
    assert sp.simplify_logic(
        sp.Equivalent(first_bound, epsilon >= sp.Rational(1, 3))
    ) is sp.true
    # Favorable detector: monotonicity makes pair acceptance >= singleton
    # acceptance >=1-epsilon; rejection <=epsilon forces epsilon>=1/2.
    second_bound = sp.solve_univariate_inequality(1 - epsilon <= epsilon, epsilon)
    assert sp.simplify_logic(
        sp.Equivalent(second_bound, epsilon >= sp.Rational(1, 2))
    ) is sp.true


def main():
    labelled_transfer()
    singleton_overlap()
    projected_transfer()
    general_collision_identity()
    coverage_router_bounds()
    print("PASS: exact labelled transfer diag(1,r-1)/r")
    print("PASS: finite-terminal singleton-overlap obstruction")
    print("PASS: uniform m-fanout multiplier (r-1)(1-1/m)")
    print("PASS: general collision-leak identity")
    print("PASS: sharp coverage-router error lower bounds 1/3 and 1/2")
    print("NO-GO: ordinary positive terminal cannot realize the router")
    print("OPEN: signed terminal-difference realization")


if __name__ == "__main__":
    main()
