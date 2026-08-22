#!/usr/bin/env python3
"""Independent exact reconstruction for the all-spectrum stable family.

This verifier layer intentionally does not import anything from ``computation``.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
import sympy as sp


@dataclass(frozen=True)
class Reaction:
    label: str
    y: tuple[int, ...]
    yp: tuple[int, ...]


def reactions(m: int) -> list[Reaction]:
    if m < 3:
        raise ValueError("m >= 3 required")
    n = m + 1

    def v(items: dict[int, int] | None = None) -> tuple[int, ...]:
        out = [0] * n
        if items:
            for i, value in items.items():
                out[i] = value
        return tuple(out)

    out = [Reaction("R0", v(), v({0: 1}))]
    for i in range(2, m - 1):
        out.append(Reaction(f"R{i}", v({0: 1, i - 1: 1}), v({0: 1, i: 1})))
    out += [
        Reaction("Ra", v({0: 1, m - 2: 1}), v({m - 1: 2})),
        Reaction("Rb", v({m - 1: 2}), v({1: 1})),
        Reaction("R+", v({m: 2}), v({0: 1, m - 1: 1})),
        Reaction("R-", v({0: 1, m - 1: 1}), v({m: 2})),
    ]
    if len(out) != m + 2:
        raise AssertionError("wrong reaction count")
    return out


def gamma_y(m: int) -> tuple[sp.Matrix, sp.Matrix]:
    rs = reactions(m)
    Y = sp.Matrix.hstack(*(sp.Matrix(r.y) for r in rs))
    Yp = sp.Matrix.hstack(*(sp.Matrix(r.yp) for r in rs))
    return Yp - Y, Y


def conservation(m: int) -> sp.Matrix:
    return sp.Matrix([0] + [4] * (m - 2) + [2, 1])


def flux(m: int, a: sp.Expr, b: sp.Expr) -> sp.Matrix:
    return sp.Matrix([a] * m + [b, b])


def A_matrix(m: int, a: sp.Expr = sp.Integer(1), b: sp.Expr = sp.Integer(1)) -> sp.Matrix:
    G, Y = gamma_y(m)
    return sp.simplify(G * sp.diag(*list(flux(m, a, b))) * Y.T)


def B_map(m: int, u: sp.Matrix, w: sp.Matrix) -> sp.Matrix:
    G, Y = gamma_y(m)
    weights = flux(m, sp.Integer(1), sp.Integer(1))
    ans = sp.zeros(m + 1, 1)
    for r in range(Y.cols):
        val = sp.Integer(0)
        for i in range(m + 1):
            yi = int(Y[i, r])
            val += yi * (yi - 1) * u[i] * w[i]
            for j in range(i + 1, m + 1):
                yj = int(Y[j, r])
                val += yi * yj * (u[i] * w[j] + u[j] * w[i])
        ans += weights[r] * val * G[:, r]
    return sp.simplify(ans)


def hurwitz_determinants(coeffs: Iterable[sp.Expr]) -> list[sp.Expr]:
    """Hurwitz determinants for a monic polynomial coefficients [1,a1,...,an]."""
    cs = list(coeffs)
    n = len(cs) - 1
    a = [sp.Integer(1)] + cs[1:]
    out = []
    for k in range(1, n + 1):
        H = sp.zeros(k)
        for i in range(k):
            for j in range(k):
                idx = 2 * (i + 1) - (j + 1)
                H[i, j] = a[idx] if 0 <= idx <= n else 0
        out.append(sp.factor(H.det()))
    return out
