#!/usr/bin/env python3
"""Exact-arithmetic falsification checks for the upstream normalized tensor identity.

These finitely many rational checks are reproducible audit evidence, not a proof
of a universally quantified identity or of the log-Brunn--Minkowski theorem.
The accompanying audit note supplies the algebraic derivation.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from random import Random


def symmetric_tensor(n, rng):
    values = {k: F(rng.randrange(-9, 10), rng.randrange(1, 8))
              for k in combinations_with_replacement(range(n), 3)}
    return {k: values[tuple(sorted(k))] for k in product(range(n), repeat=3)}


def check(n, rng):
    ix = list(product(range(n), repeat=3))
    h = [[F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            h[i][j] = h[j][i] = F(rng.randrange(-9, 10), rng.randrange(1, 8))
    C, S = symmetric_tensor(n, rng), symmetric_tensor(n, rng)
    J = {k: sum(h[k[0]][a] * C[(a, k[1], k[2])] for a in range(n)) for k in ix}
    symJ = {k: (J[k] + J[(k[1], k[0], k[2])] + J[(k[2], k[0], k[1])])/3 for k in ix}
    norm = lambda X: sum(X[k]**2 for k in ix)
    dot = lambda X, Y: sum(X[k] * Y[k] for k in ix)
    J12 = {k: J[(k[1], k[0], k[2])] for k in ix}
    cross = sum(S[(a, l, k)] *
                (sum(C[(a, i, l)] * h[i][k] for i in range(n)) + S[(a, k, l)])
                for a, l, k in ix)
    qder = sum((sum(S[(i, a, d)] * h[a][j] + h[i][a] * S[(a, j, d)]
                    for a in range(n)) +
                sum(h[i][a] * C[(a, b, d)] * h[b][j]
                    for a in range(n) for b in range(n))) * C[(i, j, d)]
               for i, j, d in ix)
    cubic = sum(sum(h[i][a] * h[a][j] for a in range(n)) *
                sum(C[(i, k, l)] * C[(j, l, k)] for k in range(n) for l in range(n))
                for i in range(n) for j in range(n))
    assert cross == norm(S) + dot(S, J)
    assert qder == 2*dot(S, J) + dot(J, J12)
    assert cubic == norm(J)
    assert norm(symJ) == (norm(J) + 2*dot(J, J12))/3
    remainder = 2*cross + qder + cubic
    squares = 2*sum((S[k] + symJ[k])**2 for k in ix) + F(1, 6)*sum((J[k]-J12[k])**2 for k in ix)
    assert remainder == squares
    assert squares >= 0


if __name__ == "__main__":
    rng = Random(20261006)
    count = 0
    for n in range(1, 6):
        for _ in range(40):
            check(n, rng)
            count += 1
    print(f"PASS: {count} exact rational tensor checks; dimensions 1--5; seed 20261006.")
