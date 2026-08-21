#!/usr/bin/env python3
"""Exact contact equations for the unmarked q divisor in fixed-linear delta=1."""

from __future__ import annotations

import sympy as sp


p, q, r = sp.symbols("p q r")
a2, a3 = sp.symbols("a2 a3")
b1, b2, b3 = sp.symbols("b1 b2 b3")
c0, c2, c3 = sp.symbols("c0 c2 c3")

A = a2 * p * q**2 + a3 * q**3
B = p**3 + b1 * p**2 * q + b2 * p * q**2 + b3 * q**3
R = c0 * p**3 + sp.Rational(3, 4) * b1 * c0 * p**2 * q + c2 * p * q**2 + c3 * q**3
P, Q = p * A, p * B


def jac2(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def jac3(f: sp.Expr, g: sp.Expr, h: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix(
            [[sp.diff(value, variable) for variable in (p, q, r)]
             for value in (f, g, h)]
        ).det()
    )


alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
direction = lambda f: sp.diff(f, q) - sp.Rational(1, 4) * b1 * sp.diff(f, p)
N = tuple(sp.cancel(direction(form) / q) for form in (P, Q, R))
assert all(sp.denom(entry) == 1 for entry in N)
assert sp.expand(alpha * N[0] + beta * N[1] + gamma * N[2]) == 0

u, v, t = N
curvature = sp.expand(
    jac3(P, r * v, r * t)
    + jac3(r * u, Q, r * t)
    + jac3(r * u, r * v, R)
)
assert sp.Poly(curvature, r).degree() == 1
K = sp.expand(sp.Poly(curvature, r).coeff_monomial(r))


def contact_equations():
    lam, mu = sp.symbols("lam mu")
    residual = sp.Poly(
        sp.expand(K - lam * alpha - mu * beta), p, q
    )
    return lam, mu, [
        sp.factor(residual.coeff_monomial(p ** (5 - index) * q**index))
        for index in range(6)
    ]


def main() -> None:
    lam, mu, equations = contact_equations()
    print("N =", tuple(sp.factor(entry) for entry in N))
    print("K =", sp.factor(K))
    for index, equation in enumerate(equations):
        print(p ** (5 - index) * q**index, ":", equation)


if __name__ == "__main__":
    main()
