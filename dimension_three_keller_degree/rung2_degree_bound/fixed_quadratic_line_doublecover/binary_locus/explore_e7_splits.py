#!/usr/bin/env python3
"""Small exact search for E7 splitting strata; exploratory, not a verifier."""

import itertools
import sympy as sp

p, q, r = sp.symbols("p q r")
u2, v2 = sp.symbols("u2 v2")
u1p, u1q, v1p, v1q, t1 = sp.symbols("u1p u1q v1p v1q t1")
u0p, u0m, u0q, v0p, v0m, v0q, t0p, t0q = sp.symbols(
    "u0p u0m u0q v0p v0m v0q t0p t0q"
)
Ur = u2 * r**2 + r * (u1p * p + u1q * q) + (
    u0p * p**2 + u0m * p * q + u0q * q**2
)
Vr = v2 * r**2 + r * (v1p * p + v1q * q) + (
    v0p * p**2 + v0m * p * q + v0q * q**2
)
Tr = t1 * r + t0p * p + t0q * q
blocks = (
    (2, (u2, v2)),
    (1, (u1p, u1q, v1p, v1q, t1)),
    (0, (u0p, u0m, u0q, v0p, v0m, v0q, t0p, t0q)),
)


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def ranks(h, R):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    equation = sp.expand(jac(Q, R) * Ur - jac(P, R) * Vr
                         + jac(P, Q) * Tr)
    out = []
    for power, unknowns in blocks:
        value = sp.Poly(equation, r).coeff_monomial(r**power)
        degree = 7 - power
        rows = [
            sp.Poly(value, p, q).coeff_monomial(p**i * q ** (degree - i))
            for i in range(degree, -1, -1)
        ]
        matrix, _ = sp.linear_eq_to_matrix(rows, unknowns)
        out.append(matrix.rank())
    return tuple(out)


def resultant(h, R):
    return sp.factor(sp.resultant(h.subs(q, 1), R.subs(q, 1), p))


h = p**2 + q**2
for coefficients in itertools.product(range(-2, 3), repeat=4):
    if coefficients == (0, 0, 0, 0):
        continue
    R = sum(coefficients[i] * p ** (3 - i) * q**i for i in range(4))
    if resultant(h, R) == 0:
        continue
    split = ranks(h, R)
    if split == (2, 5, 8):
        print("full", coefficients, R, "resultant", resultant(h, R))
        break
else:
    print("no full-rank sample")

for coefficients in (
    (1, 0, 0, 1),
    (1, 1, 0, 1),
    (1, 1, 1, 1),
    (1, 2, 3, 4),
):
    R = sum(coefficients[i] * p ** (3 - i) * q**i for i in range(4))
    print(coefficients, "ranks", ranks(h, R), "res", resultant(h, R))
