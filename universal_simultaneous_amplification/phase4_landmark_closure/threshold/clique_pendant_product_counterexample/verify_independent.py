#!/usr/bin/env python3
"""Independent exact solve from microscopic events using SymPy DomainMatrix.

This deliberately does not use ``model.moves`` or FLINT's ``fmpq_mat.solve``.
It builds every matrix row by enumerating labelled replacement events, solves
over the exact rational domain through a separate solver interface, and compares
the result with the committed certificate.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

from microscopic import microscopic_moves


def all_states(c: int, m: int):
    return [
        (h, i, j)
        for h in (0, 1)
        for i in range(c + 1)
        for j in range(m + 1)
    ]


def pair(x: Fraction):
    return x.numerator, x.denominator


def solve(rule: str, c: int, m: int, r: Fraction) -> Fraction:
    extinct, fixed = (0, 0, 0), (1, c, m)
    transient = [s for s in all_states(c, m) if s not in (extinct, fixed)]
    index = {s: k for k, s in enumerate(transient)}
    size = len(transient)
    rows = [[Fraction() for _ in range(size)] for _ in range(size)]
    rhs = [[Fraction()] for _ in range(size)]
    for row, state in enumerate(transient):
        outgoing = microscopic_moves(rule, state, c, m, r)
        rows[row][row] = sum(outgoing.values(), Fraction())
        for target, probability in outgoing.items():
            if target == fixed:
                rhs[row][0] += probability
            elif target != extinct:
                rows[row][index[target]] -= probability

    a = DomainMatrix.from_list([[pair(x) for x in row] for row in rows], QQ)
    b = DomainMatrix.from_list([[pair(x) for x in row] for row in rhs], QQ)
    solution = a.lu_solve(b).to_list_flat()
    h = [Fraction(int(x.numerator), int(x.denominator)) for x in solution]
    n = c + m + 1
    return (
        h[index[(1, 0, 0)]]
        + c * h[index[(0, 1, 0)]]
        + m * h[index[(0, 0, 1)]]
    ) / n


def main() -> None:
    here = Path(__file__).resolve().parent
    certificate = json.loads((here / "certificate.json").read_text())
    c, m, n = 31, 4, 36
    r = Fraction(3, 2)
    rho = {rule: solve(rule, c, m, r) for rule in ("Bd", "dB")}
    for rule in ("Bd", "dB"):
        assert str(rho[rule]) == certificate["rules"][rule]["rho"]

    bd0 = (1 - 1 / r) / (1 - r ** (-n))
    db0 = Fraction(n - 1, n) * (1 - 1 / r) / (1 - r ** (-(n - 1)))
    x, y = rho["Bd"] / bd0, rho["dB"] / db0
    assert x * y > 1
    assert (x + y) / 2 > 1
    assert str((1 - y) / (x - y)) == certificate["arithmetic_crossing_lambda"]
    print("PASS: independent microscopic SymPy-QQ solve matches certificate")


if __name__ == "__main__":
    main()
