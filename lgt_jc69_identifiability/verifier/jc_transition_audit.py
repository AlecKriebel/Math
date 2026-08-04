#!/usr/bin/env python3
"""Exact direct JC69 transition-matrix summation on a three-leaf tree."""
from __future__ import annotations

import itertools
import sympy as s

u, v = s.symbols("u v", positive=True)
# u=exp(-mu*g1), v=exp(-mu*(g2-g1)); exp(-mu*g2)=u*v.


def P(z, a, b):
    return (1 + 3 * z) / 4 if a == b else (1 - z) / 4


def pattern_prob(i, j, k):
    # Topology ((1,2),3).  Root state r is uniform; cherry ancestor c.
    total = 0
    for r in range(4):
        for c in range(4):
            total += s.Rational(1, 4) * P(v, r, c) * P(u, c, i) * P(u, c, j) * P(u * v, r, k)
    return s.expand(total)


def main():
    probs = {(i, j, k): pattern_prob(i, j, k) for i, j, k in itertools.product(range(4), repeat=3)}
    assert s.simplify(sum(probs.values()) - 1) == 0

    p0 = sum(p for (i, j, k), p in probs.items() if i == j == k)
    p12 = sum(p for (i, j, k), p in probs.items() if i == j and k != i)
    p13 = sum(p for (i, j, k), p in probs.items() if i == k and j != i)
    p23 = sum(p for (i, j, k), p in probs.items() if j == k and i != j)
    pD = sum(p for (i, j, k), p in probs.items() if len({i, j, k}) == 3)
    assert s.simplify(p0 + p12 + p13 + p23 + pD - 1) == 0
    assert s.simplify(p13 - p23) == 0

    A = s.simplify((4 * (p0 + p12) - 1) / 3)
    B = s.simplify((4 * (p0 + p13) - 1) / 3)
    C = s.simplify((16 * p0 - 1 - 3 * A - 6 * B) / 6)
    assert s.simplify(A - u**2) == 0
    assert s.simplify(B - (u * v)**2) == 0
    assert s.simplify(C - u**3 * v**2) == 0

    print("PASS all 64 JC69 pattern probabilities sum to one")
    print("PASS aggregate site-pattern transform")
    print("PASS cherry pair = exp(-2 mu g1)")
    print("PASS noncherry pair = exp(-2 mu g2)")
    print("PASS three-way coordinate = exp[-mu(g1+2g2)]")
    print("ALL DIRECT TRANSITION-MATRIX AUDITS PASSED")


if __name__ == "__main__":
    main()
