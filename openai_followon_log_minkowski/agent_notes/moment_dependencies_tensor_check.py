#!/usr/bin/env python3
"""Exact rational checks of the normalized tensor contractions.

These are reproducible algebra regression checks, not a proof of all-dimensional
identities or of the upstream inequality. The general proof is in the audit note.
Only Python's standard library is needed.
"""

from fractions import Fraction as F
from itertools import product
import json
import random


def symmetric(rng, n, rank):
    values = {}
    result = {}
    for indices in product(range(n), repeat=rank):
        key = tuple(sorted(indices))
        values.setdefault(key, rng.randint(-3, 3))
        result[indices] = F(values[key])
    return result


def check(n, rng):
    h, C, S = [symmetric(rng, n, rank) for rank in (2, 3, 3)]
    triples = list(product(range(n), repeat=3))
    J = {(i, j, k): sum(h[i, a] * C[a, j, k] for a in range(n))
         for i, j, k in triples}
    normS = sum(value * value for value in S.values())
    normJ = sum(value * value for value in J.values())
    SJ = sum(S[i, j, k] * J[i, j, k] for i, j, k in triples)
    Jswap = sum(J[i, j, k] * J[j, i, k] for i, j, k in triples)
    cross = 2 * sum(
        S[a, l, k] * (sum(C[a, i, l] * h[i, k] for i in range(n))
                      + S[a, k, l])
        for a, l, k in triples
    )
    derivative = sum(
        (sum(S[i, a, d] * h[a, j] + h[i, a] * S[a, j, d]
             for a in range(n))
         + sum(h[i, a] * C[a, b, d] * h[b, j]
               for a, b in product(range(n), repeat=2))) * C[i, j, d]
        for i, j, d in triples
    )
    cubic = sum(
        sum(h[i, a] * h[a, j] for a in range(n))
        * sum(C[i, k, l] * C[j, l, k]
              for k, l in product(range(n), repeat=2))
        for i, j in product(range(n), repeat=2)
    )
    assert cross == 2 * normS + 2 * SJ
    assert derivative == 2 * SJ + Jswap
    assert cubic == normJ
    symJ = {(i, j, k): (J[i, j, k] + J[j, i, k] + J[k, i, j]) / 3
            for i, j, k in triples}
    assert sum(v * v for v in symJ.values()) == (normJ + 2 * Jswap) / 3
    squares = 2 * sum((S[t] + symJ[t]) ** 2 for t in triples)
    squares += F(1, 6) * sum((J[i, j, k] - J[j, i, k]) ** 2
                            for i, j, k in triples)
    assert cross + derivative + cubic == squares
    assert squares >= 0


if __name__ == "__main__":
    rng = random.Random(20261006)
    repetitions = 50
    for dimension in range(1, 6):
        for _ in range(repetitions):
            check(dimension, rng)
    print(json.dumps({"status": "pass", "arithmetic": "fractions.Fraction",
                      "seed": 20261006, "dimensions": [1, 2, 3, 4, 5],
                      "cases_per_dimension": repetitions,
                      "total_cases": 5 * repetitions,
                      "claims_per_case": 6}, indent=2))
