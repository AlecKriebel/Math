#!/usr/bin/python3
"""Exact regressions for WORKING_RANK_ONE_PRIMITIVE_EXIT.md."""

from __future__ import annotations

import sympy as sp

x, y, z = sp.symbols("x y z")
mu, nu = sp.symbols("mu nu")
variables = (x, y, z)


def generic_form(prefix: str, degree: int) -> sp.Expr:
    coefficients = []
    monomials = []
    index = 0
    for i in range(degree, -1, -1):
        for j in range(degree - i, -1, -1):
            k = degree - i - j
            coefficients.append(sp.symbols(f"{prefix}{index}"))
            monomials.append(x**i * y**j * z**k)
            index += 1
    return sum(c * m for c, m in zip(coefficients, monomials))


Q = generic_form("q", 3)
S = generic_form("s", 2)
T = generic_form("t", 2)
U = generic_form("u", 2)
R = generic_form("r", 3)
linear = generic_form("l", 1)
P = x**3
h = mu * x**4 + nu * x * Q


def grad(f: sp.Expr) -> sp.Matrix:
    return sp.Matrix([sp.diff(f, v) for v in variables])


def jac(f: sp.Expr, g: sp.Expr, k: sp.Expr) -> sp.Expr:
    return sp.expand(sp.Matrix.hstack(grad(f), grad(g), grad(k)).det())


D = lambda f: jac(P, Q, f)
E6 = sp.expand(D(R) + jac(P, T, h) + jac(S, Q, h))
K = 3 * x**2 * R - 3 * nu * x**3 * T - 4 * mu * x**3 * S - nu * Q * S
assert sp.expand(D(K) - 3 * x**2 * E6) == 0

R_pure = sp.Rational(4, 3) * mu * x * S
E5 = sp.expand(
    jac(linear, Q, mu * x**4)
    + jac(S, T, mu * x**4)
    + jac(P, Q, U)
    + jac(P, T, R_pure)
    + jac(S, Q, R_pure)
)
W = 9 * x**2 * U - 2 * mu * S**2 - 12 * mu * x**3 * linear
assert sp.expand(D(W) - 9 * x**2 * E5) == 0

alpha, beta = sp.symbols("alpha beta")
f = x**3 + x * y + alpha * x + beta * y
critical_substitution = {x: -beta, y: -3 * beta**2 - alpha}
assert all(
    sp.expand(sp.diff(f, v).subs(critical_substitution)) == 0
    for v in variables
)

print("rank-one primitive-exit SymPy checks passed")
