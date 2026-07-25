#!/usr/bin/python3
"""Exact regressions for WORKING_RANK_ONE_COMPOSITE_EXIT.md."""

from __future__ import annotations

import sympy as sp

x, y, z = sp.symbols("x y z")
variables = (x, y, z)


def form(prefix: str, degree: int, binary: bool = False) -> sp.Expr:
    terms = []
    index = 0
    for i in range(degree, -1, -1):
        for j in range(degree - i, -1, -1):
            k = degree - i - j
            if binary and k:
                continue
            terms.append(sp.symbols(f"{prefix}{index}") * x**i * y**j * z**k)
            index += 1
    return sum(terms)


P = form("p", 3, True)
Q = form("q", 3, True)
h = form("h", 4, True)
S = form("s", 2)
T = form("t", 2)
U = form("u", 2)
R = form("r", 3)
linear1 = form("l", 1)
linear2 = form("m", 1)


def jac(f: sp.Expr, g: sp.Expr, k: sp.Expr) -> sp.Expr:
    return sp.expand(
        sp.Matrix([[sp.diff(f, v) for v in variables] for f in (f, g, k)]).det()
    )


a = sp.diff(Q, x) * sp.diff(h, y) - sp.diff(Q, y) * sp.diff(h, x)
b = sp.diff(P, x) * sp.diff(h, y) - sp.diff(P, y) * sp.diff(h, x)
c = sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x)

E6 = sp.expand(jac(P, Q, R) + jac(P, T, h) + jac(S, Q, h))
assert sp.expand(E6 - (a * sp.diff(S, z) - b * sp.diff(T, z) + c * sp.diff(R, z))) == 0

S0 = S.subs(z, 0)
T0 = T.subs(z, 0)
R0 = R.subs(z, 0)
E5 = sp.expand(
    jac(linear1, Q, h)
    + jac(P, linear2, h)
    + jac(S0, T0, h)
    + jac(P, Q, U)
    + jac(P, T0, R0)
    + jac(S0, Q, R0)
)
expected_E5 = (
    a * sp.diff(linear1, z)
    - b * sp.diff(linear2, z)
    + c * sp.diff(U, z)
)
assert sp.expand(E5 - expected_E5) == 0

print("rank-one composite-exit SymPy checks passed")
