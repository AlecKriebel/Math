#!/usr/bin/env python3
"""Exact integer sanity checks for the frozen competitors; no proof search.

This finite computation checks concrete formulas. The infinite and topological
claims are justified deductively in CHECKS.md and REPORT.md.
"""
import json
from math import gcd, isqrt

MAX_N = 4096
competitors = []
for n in range(1, MAX_N + 1):
    m = isqrt(2 * n * n) + 1
    # Exactly certifies floor(n sqrt(2)) and 0 < t_n < 1/n.
    assert (m - 1) ** 2 < 2 * n * n < m ** 2
    g = gcd(m, n)
    p, q = m // g, n // g
    assert gcd(p, q) == 1
    assert m * q == p * n
    assert (q * m) % n == 0
    # A shorter return would require q to divide its period.
    for k in range(1, q):
        assert (k * m) % n != 0
    assert p * p - 2 * q * q >= 1
    if n <= 10:
        competitors.append({"n": n, "m_n": m, "least_period": q,
                            "pell_numerator": p * p - 2 * q * q})

# Independent enumeration of reduced rational angles in (sqrt(2),sqrt(2)+1).
MAX_Q = 64
bounded_angles = 0
for q in range(1, MAX_Q + 1):
    for p in range(q + 1, 3 * q + 1):
        if gcd(p, q) != 1:
            continue
        if p * p <= 2 * q * q:
            continue
        # p/q < sqrt(2)+1 iff p/q-1 < sqrt(2), since p>q.
        if (p - q) ** 2 >= 2 * q * q:
            continue
        bounded_angles += 1
        assert p * p - 2 * q * q >= 1

print(json.dumps({
    "status": "pass",
    "arithmetic": "exact unbounded Python integers; no floating point",
    "max_competitor_n": MAX_N,
    "competitors_checked": MAX_N,
    "max_enumerated_least_period": MAX_Q,
    "reduced_angles_checked": bounded_angles,
    "sample_competitors": competitors,
    "limits": "Finite sanity checks do not establish infinite-period exclusion, topology, or source admissibility. See CHECKS.md for deductive verification."
}, indent=2))
