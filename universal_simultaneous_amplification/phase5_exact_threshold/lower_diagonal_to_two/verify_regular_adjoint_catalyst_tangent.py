#!/usr/bin/env python3
"""Exact verifier for the regular adjoint-kernel catalyst obstruction."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    # The global Bd identity is the p-average of the exact first-event
    # residual.  Use a fully symbolic two-type stochastic kernel and start
    # law; no reversibility is imposed for this algebraic check.
    p, a, c = sp.symbols("p a c", positive=True)
    pvec = sp.Matrix([p, 1 - p])
    kernel = sp.Matrix([[a, 1 - a], [c, 1 - c]])
    adjoint = sp.diag(1 / p, 1 / (1 - p)) * kernel.T * sp.diag(p, 1 - p)
    temperature = adjoint * sp.ones(2, 1)
    b1, b2 = sp.symbols("b1 b2", positive=True)
    b = sp.Matrix([b1, b2])
    z = b - sp.ones(2, 1) / 2
    bd_residual = sp.diag(*list(temperature)) * b - 2 * sp.diag(
        *list(sp.ones(2, 1) - b)
    ) * (kernel * b)
    average_bd_residual = (pvec.T * bd_residual)[0]
    bd_identity = (pvec.T * z)[0] + 2 * (
        z.T * sp.diag(p, 1 - p) * kernel * z
    )[0]
    assert sp.factor(average_bd_residual - bd_identity) == 0

    # The global dB identity follows after dividing its residual by 1-s.
    s1, s2 = sp.symbols("s1 s2", positive=True)
    s = sp.Matrix([s1, s2])
    v = s - sp.ones(2, 1) / 2
    odds_residual = sp.Matrix(
        [s[i] / (1 - s[i]) - 2 * (adjoint * s)[i] for i in range(2)]
    )
    average_odds_residual = (pvec.T * odds_residual)[0] / 2
    db_identity = (pvec.T * v)[0] + 4 * sum(
        pvec[i] * v[i] ** 2 / (1 - 2 * v[i]) for i in range(2)
    )
    assert sp.factor(average_odds_residual - db_identity) == 0

    # Sharp rational period-two tangent.  Q is p-reversible for uniform p,
    # and the one-sided stochastic perturbation has h=(1,-1).
    epsilon = sp.symbols("epsilon", nonnegative=True)
    Q = sp.Matrix([[0, 1], [1, 0]])
    A = sp.Matrix([[1, -1], [0, 0]])
    P = Q + epsilon * A
    t = P.T * sp.ones(2, 1)
    h = sp.diff(t, epsilon).subs(epsilon, 0)
    u = -sp.Rational(1, 2) * (2 * sp.eye(2) - Q).inv() * h
    assert u == sp.Matrix([-sp.Rational(1, 6), sp.Rational(1, 6)])

    inner = lambda left, right: (left.T * right)[0] / 2
    gain_two = sp.factor(-2 * inner(u, Q * u))
    loss_two = sp.factor(4 * inner(u, u))
    assert gain_two == sp.Rational(1, 18)
    assert loss_two == sp.Rational(1, 9)
    assert loss_two == 2 * gain_two

    # Independently insert second-order unknowns into the exact nonlinear
    # equations and recover the same averaged coefficients.
    B1, B2, S1, S2 = sp.symbols("B1 B2 S1 S2")
    b_series = sp.ones(2, 1) / 2 + epsilon * u + epsilon**2 * sp.Matrix([B1, B2])
    s_series = sp.ones(2, 1) / 2 - epsilon * u + epsilon**2 * sp.Matrix([S1, S2])
    bd_equations = sp.diag(*list(t)) * b_series - 2 * sp.diag(
        *list(sp.ones(2, 1) - b_series)
    ) * (P * b_series)
    db_equations = s_series - 2 * sp.diag(
        *list(sp.ones(2, 1) - s_series)
    ) * (P.T * s_series)
    coefficient_equations = [
        sp.expand(value).coeff(epsilon, 2)
        for value in list(bd_equations) + list(db_equations)
    ]
    solution = sp.solve(coefficient_equations, [B1, B2, S1, S2], dict=True)
    assert len(solution) == 1
    solution = solution[0]
    assert sp.factor((solution[B1] + solution[B2]) / 2 - gain_two) == 0
    assert sp.factor((solution[S1] + solution[S2]) / 2 + loss_two) == 0

    print("PASS exact regular adjoint-kernel quadratic catalyst obstruction")


if __name__ == "__main__":
    main()
