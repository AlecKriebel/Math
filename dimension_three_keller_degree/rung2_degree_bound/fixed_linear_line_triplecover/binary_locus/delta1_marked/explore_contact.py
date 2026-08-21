#!/usr/bin/env python3
"""Exact contact equations on the marked p divisor in fixed-linear delta=1."""

from __future__ import annotations

from functools import reduce
from itertools import combinations

import sympy as sp


p, q, r = sp.symbols("p q r")
a0, a1, a2 = sp.symbols("a0 a1 a2")
b0, b1, b2 = sp.symbols("b0 b1 b2")
s0, s1 = sp.symbols("s0 s1")

A = a0 * p**3 + a1 * p**2 * q + a2 * p * q**2
B = b0 * p**3 + b1 * p**2 * q + b2 * p * q**2 + q**3
S = s0 * p**2 + s1 * p * q + q**2
P, Q, R = p * A, p * B, p * S


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


def coeff_vector(f: sp.Expr, degree: int) -> sp.Matrix:
    poly = sp.Poly(sp.expand(f), p, q)
    return sp.Matrix(
        [poly.coeff_monomial(p ** (degree - index) * q**index)
         for index in range(degree + 1)]
    )


alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
assert sp.rem(alpha, p, p) == 0
assert sp.rem(beta, p, p) == 0
assert sp.rem(gamma, p**2, p) == 0

N = (sp.diff(A, q), sp.diff(B, q), sp.diff(S, q))
u, v, t = N
assert sp.expand(alpha * u + beta * v + gamma * t) == 0

curvature = sp.expand(
    jac3(P, r * v, r * t)
    + jac3(r * u, Q, r * t)
    + jac3(r * u, r * v, R)
)
assert sp.Poly(curvature, r).degree() == 1
K = sp.expand(sp.Poly(curvature, r).coeff_monomial(r))

def main() -> None:
    columns = [coeff_vector(form, 5) for form in (alpha, beta, K)]
    matrix = sp.Matrix.hstack(*columns)
    minors = [
        sp.factor(matrix.extract(rows, range(3)).det())
        for rows in combinations(range(6), 3)
    ]
    nonzero = [minor for minor in minors if minor != 0]
    print("N =", tuple(sp.factor(entry) for entry in N))
    print("K =", sp.factor(K))
    print("nonzero contact minors =", len(nonzero))
    print("contact-minor gcd =", sp.factor(reduce(sp.gcd, nonzero)))
    for index, minor in enumerate(minors):
        if minor != 0:
            print(index, sp.factor(minor))


if __name__ == "__main__":
    main()
