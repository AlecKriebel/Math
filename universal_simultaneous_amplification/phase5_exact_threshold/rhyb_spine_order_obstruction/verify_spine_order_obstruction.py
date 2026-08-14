#!/usr/bin/env python3
"""Exact replay of the deterministic two-cycle spine-order obstruction."""

from __future__ import annotations

import sympy as sp


Q = sp.Rational
r, kappa = sp.symbols("r kappa", positive=True)


def weighted_pair(left, right, measure):
    return sp.factor(
        sum(measure[i] * left[i] * right[i] for i in range(2))
    )


def build_family():
    P = sp.Matrix([[0, 1], [1, 0]])
    pi = sp.Matrix([Q(1, 2), Q(1, 2)])
    a = sp.Matrix([2 / (1 + kappa), 2 * kappa / (1 + kappa)])
    p = sp.Matrix([1 / (1 + kappa), kappa / (1 + kappa)])
    Da = sp.diag(*a)
    R = sp.diag(*[1 / value for value in a]) * P * Da
    t = sp.diag(*[1 / value for value in a]) * (P * a)

    q = sp.Matrix(
        [
            (kappa * r + 1) / (r * (kappa + r)),
            (kappa + r) / (r * (kappa * r + 1)),
        ]
    )
    b = sp.ones(2, 1) - q
    s = sp.Matrix([b[1], b[0]])
    h = sp.ones(2, 1) - s

    assert sp.factor(sum(pi[i] * a[i] for i in range(2)) - 1) == 0
    assert all(
        sp.factor(t[i] * b[i] - r * q[i] * (P * b)[i]) == 0
        for i in range(2)
    )
    assert all(
        sp.factor(s[i] - r * h[i] * (R * s)[i]) == 0
        for i in range(2)
    )
    return P, pi, a, p, R, q, s, h


def build_spine(P, pi, a, p, R, q, s, h):
    X = (r - 1) * q
    h1 = sp.Matrix(
        [sp.factor(1 / (1 + r * (R * X)[i])) for i in range(2)]
    )
    v = sp.Matrix([a[i] * s[i] for i in range(2)])
    Vv = sp.Matrix([sp.factor((P * v)[i] / v[i]) for i in range(2)])

    K = sp.zeros(2)
    for i in range(2):
        for j in range(2):
            K[i, j] = sp.factor(P[i, j] * v[j] / (Vv[i] * v[i]))
    assert K == P

    m = sp.Matrix(
        [sp.factor(pi[i] * Vv[i] * v[i] ** 2) for i in range(2)]
    )
    assert sp.factor(m[0] * K[0, 1] - m[1] * K[1, 0]) == 0

    x = sp.Matrix([sp.factor(X[i] / s[i]) for i in range(2)])
    A = sp.Matrix(
        [sp.factor(r * h[i] * h1[i] / (a[i] * s[i])) for i in range(2)]
    )
    first = sp.ones(2, 1) - h1
    gap = weighted_pair(first - s, sp.ones(2, 1), p)
    spine_gap = weighted_pair(A, K * (x - sp.ones(2, 1)), m)
    raw = weighted_pair(A, x - sp.ones(2, 1), m)
    cross = sp.factor(
        Q(1, 2)
        * sum(
            m[i]
            * K[i, j]
            * (A[i] - A[j])
            * (x[i] - x[j])
            for i in range(2)
            for j in range(2)
        )
    )
    assert sp.factor(gap - spine_gap) == 0
    assert sp.factor(gap - raw + cross) == 0
    return x, A, K, gap, cross


def verify_factorizations(x, A, K, gap, cross):
    x0_minus_one = sp.factor(x[0] - 1)
    x1_minus_one = sp.factor(x[1] - 1)
    dx = sp.factor(x[0] - x[1])
    dA = sp.factor(A[0] - A[1])

    claimed_x0 = (
        (kappa - 1)
        * (kappa * (r**2 - r - 1) - 1)
        / (kappa * (kappa + r) * (r + 1))
    )
    claimed_x1 = -(
        (kappa - 1)
        * (-kappa + r**2 - r - 1)
        / ((r + 1) * (kappa * r + 1))
    )
    claimed_dx = (
        (kappa - 1)
        * (kappa + 1)
        * (-kappa**2 + kappa * r**3 - 3 * kappa * r - 1)
        / (kappa * (kappa + r) * (r + 1) * (kappa * r + 1))
    )
    claimed_dA = -(
        r
        * (kappa - 1)
        * (kappa + 1)
        * (kappa + r)
        * (kappa * r + 1)
        * (kappa**2 + kappa * r + 2 * kappa + 1)
        / (
            2
            * kappa
            * (r + 1)
            * (kappa**2 + kappa * r**2 + r - 1)
            * (kappa**2 * (r - 1) + kappa * r**2 + 1)
        )
    )
    assert sp.factor(x0_minus_one - claimed_x0) == 0
    assert sp.factor(x1_minus_one - claimed_x1) == 0
    assert sp.factor(dx - claimed_dx) == 0
    assert sp.factor(dA - claimed_dA) == 0

    # K swaps the labels, so its smoothing reverses the A-order exactly.
    assert sp.factor((K * A)[0] - (K * A)[1] + dA) == 0

    # The cross-Dirichlet term has the sign of dA*dx because its edge
    # conductance is positive.
    edge_conductance = sp.factor(cross / (dA * dx))
    assert edge_conductance == (
        2
        * kappa**2
        * (r - 1) ** 2
        * (r + 1) ** 2
        / (r**2 * (kappa + 1) ** 2 * (kappa + r) * (kappa * r + 1))
    )

    C2 = r**4 - 2 * r**3 + r + 1
    C1 = r**5 - r**4 - 3 * r**2 + 3 * r + 2
    claimed_gap = (
        kappa
        * (kappa - 1) ** 2
        * (r - 1)
        * (C2 * (kappa**2 + 1) + C1 * kappa)
        / (
            r
            * (kappa + r)
            * (kappa * r + 1)
            * (kappa**2 + kappa * r**2 + r - 1)
            * (kappa**2 * (r - 1) + kappa * r**2 + 1)
        )
    )
    assert sp.factor(gap - claimed_gap) == 0
    return C2, C1


def verify_interval_signs(C2, C1):
    u = sp.symbols("u", nonnegative=True)
    shifted_C2 = sp.expand(C2.subs(r, Q(3, 2) + u))
    shifted_C1 = sp.expand(C1.subs(r, Q(3, 2) + u))
    assert shifted_C2 == (
        Q(13, 16) + u + Q(9, 2) * u**2 + 4 * u**3 + u**4
    )
    assert shifted_C1 == (
        Q(73, 32)
        + Q(93, 16) * u
        + Q(69, 4) * u**2
        + Q(33, 2) * u**3
        + Q(13, 2) * u**4
        + u**5
    )

    right = Q(151, 100)
    # Both functions controlling the one-crossing/order signs are increasing
    # on this short interval, and remain strictly negative at its right end.
    assert (r**2 - r - 1).subs(r, right) == -Q(2299, 10000)
    assert (r**3 - 3 * r).subs(r, right) == -Q(1087049, 1000000)
    assert sp.diff(r**2 - r - 1, r).subs(r, Q(3, 2)) > 0
    assert sp.diff(r**3 - 3 * r, r).subs(r, Q(3, 2)) > 0
    assert sp.diff(r**2 - r - 1, r, 2) > 0
    assert sp.diff(r**3 - 3 * r, r, 2).subs(r, Q(3, 2)) > 0


def main():
    data = build_family()
    x, A, K, gap, cross = build_spine(*data)
    C2, C1 = verify_factorizations(x, A, K, gap, cross)
    verify_interval_signs(C2, C1)
    print("PASS: exact two-cycle endpoint and linked Doob spine")
    print("PASS: strict x one-crossing with positive cross-Dirichlet term")
    print("PASS: KA reverses the A-order while the endpoint gap stays positive")
    print("SCOPE: obstruction to qualitative spine-order proofs only")


if __name__ == "__main__":
    main()
