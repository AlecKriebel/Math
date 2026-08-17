#!/usr/bin/env python3
"""Independent construction of the codimension-one all-spectrum family
with a semipositive conservation law.

Species order: X1,...,Xm,Z.
Reaction order:
  R0,
  Ri (i=2,...,m-2),
  Ra, Rb, Rplus, Rminus.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple
import sympy as sp


@dataclass(frozen=True)
class Reaction:
    name: str
    source: Tuple[int, ...]
    target: Tuple[int, ...]


def family_reactions(m: int) -> List[Reaction]:
    if m < 3:
        raise ValueError("m must be at least 3")
    n = m + 1
    def vec(**kw: int) -> Tuple[int, ...]:
        out = [0] * n
        for key, val in kw.items():
            if key == "Z":
                idx = m
            else:
                idx = int(key[1:]) - 1
            out[idx] = val
        return tuple(out)

    rxns: List[Reaction] = [Reaction("R0", vec(), vec(X1=1))]
    for i in range(2, m - 1):
        src = {"X1": 1, f"X{i}": 1}
        tgt = {"X1": 1, f"X{i+1}": 1}
        rxns.append(Reaction(f"R{i}", vec(**src), vec(**tgt)))
    rxns.extend([
        Reaction("Ra", vec(X1=1, **{f"X{m-1}": 1}), vec(**{f"X{m}": 2})),
        Reaction("Rb", vec(**{f"X{m}": 2}), vec(X2=1)),
        Reaction("Rplus", vec(Z=2), vec(X1=1, **{f"X{m}": 1})),
        Reaction("Rminus", vec(X1=1, **{f"X{m}": 1}), vec(Z=2)),
    ])
    assert len(rxns) == m + 2
    return rxns


def matrices(m: int) -> tuple[sp.Matrix, sp.Matrix]:
    rxns = family_reactions(m)
    Y = sp.Matrix.hstack(*(sp.Matrix(r.source) for r in rxns))
    Yp = sp.Matrix.hstack(*(sp.Matrix(r.target) for r in rxns))
    Gamma = Yp - Y
    return Gamma, Y


def conservation_vector(m: int) -> sp.Matrix:
    return sp.Matrix([0] + [4] * (m - 2) + [2, 1])


def flux_vector(m: int, a=sp.Symbol("a", positive=True), b=sp.Symbol("b", positive=True)) -> sp.Matrix:
    return sp.Matrix([a] * m + [b, b])


def jacobian_factor(m: int, a=sp.Symbol("a", positive=True), b=sp.Symbol("b", positive=True)) -> sp.Matrix:
    Gamma, Y = matrices(m)
    v = flux_vector(m, a, b)
    return sp.simplify(Gamma * sp.diag(*list(v)) * Y.T)


def vector_field(m: int, a=sp.Symbol("a", positive=True), b=sp.Symbol("b", positive=True)):
    Gamma, Y = matrices(m)
    x = sp.symbols(f"x1:{m+1}") + (sp.Symbol("z"),)
    rates = []
    v = flux_vector(m, a, b)
    for j in range(Y.cols):
        mon = sp.Integer(1)
        for i in range(Y.rows):
            mon *= x[i] ** int(Y[i, j])
        rates.append(v[j] * mon)
    f = sp.simplify(Gamma * sp.Matrix(rates))
    return x, f


def hessian_bilinear_from_reactions(m: int, u: sp.Matrix, w: sp.Matrix,
                                    a=sp.Integer(1), b=sp.Integer(1)) -> sp.Matrix:
    """B(u,w)=D^2 f(1)[u,w], built directly reaction-by-reaction."""
    Gamma, Y = matrices(m)
    v = flux_vector(m, a, b)
    n = m + 1
    out = sp.zeros(n, 1)
    for r in range(Y.cols):
        y = [int(Y[i, r]) for i in range(n)]
        # At x=1: D2 x^y[u,w] = sum_{i != j} y_i y_j u_i w_j
        # + sum_i y_i(y_i-1)u_i w_i.
        d2 = sp.Integer(0)
        for i in range(n):
            d2 += y[i] * (y[i] - 1) * u[i] * w[i]
            for j in range(n):
                if i != j:
                    d2 += y[i] * y[j] * u[i] * w[j]
        out += v[r] * d2 * Gamma[:, r]
    return sp.simplify(out)


def check_small(m: int) -> None:
    Gamma, Y = matrices(m)
    c = conservation_vector(m)
    a, b = sp.symbols("a b", positive=True)
    A = jacobian_factor(m, a, b)
    assert c.T * Gamma == sp.zeros(1, Gamma.cols)
    assert Gamma.rank() == m
    assert len(Gamma.nullspace()) == 2
    assert Gamma * flux_vector(m, a, b) == sp.zeros(m + 1, 1)
    x, f = vector_field(m, a, b)
    Jdirect = sp.Matrix(f).jacobian(x).subs({xx: 1 for xx in x})
    assert sp.simplify(Jdirect - A) == sp.zeros(m + 1)
    print(f"m={m}: reactions={len(family_reactions(m))}, rank={Gamma.rank()}, all checks pass")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("m", type=int)
    args = parser.parse_args()
    check_small(args.m)
