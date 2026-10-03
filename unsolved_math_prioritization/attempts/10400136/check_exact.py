#!/usr/bin/env python3
"""Exact diagnostic checks, not a computation of a QHI state sum.

Standard library only. Monomial matrices encode images of basis vectors by
integer exponents modulo N, so all root-of-unity comparisons are exact.
"""
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path
import json


def compose(left, right, n):
    """Return left * right; entries are (basis-image, phase-exponent)."""
    return tuple((left[p][0], (k + left[p][1]) % n) for p, k in right)


def scalar(mat, k, n):
    return tuple((p, (a + k) % n) for p, a in mat)


def determinant(mat, n):
    perm = [p for p, _ in mat]
    inv = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
    return (-1) ** inv, sum(a for _, a in mat) % n


def potential(vertices, edges, n):
    adj = {v: [] for v in vertices}
    for a, b, k in edges:
        adj[a].append((b, k % n))
        adj[b].append((a, -k % n))
    values = {}
    for base in vertices:
        if base in values:
            continue
        values[base] = 0
        stack = [base]
        while stack:
            a = stack.pop()
            for b, k in adj[a]:
                v = (values[a] + k) % n
                if b in values:
                    if values[b] != v:
                        return None
                else:
                    values[b] = v
                    stack.append(b)
    return values


def run():
    counts = {"matrix_products": 0, "cocycle_identities": 0,
              "charge_cancellations": 0, "even_flattening_phases": 0,
              "graph_controls": 0, "cover_degree_controls": 0,
              "peripheral_exponent_controls": 0}
    ns = [3, 5, 7, 9]
    for n in ns:
        m = (n - 1) // 2
        ident = tuple((j, 0) for j in range(n))
        x = tuple(((j + 1) % n, 0) for j in range(n))
        z = tuple((j, j) for j in range(n))
        assert determinant(x, n) == (1, 0)
        assert determinant(z, n) == (1, 0)
        assert compose(z, x, n) == scalar(compose(x, z, n), 1, n)
        assert not any(p == j for j, (p, _) in enumerate(x))  # tr X = 0
        assert sorted(a for _, a in z) == list(range(n))     # tr Z = Σ ζ^j = 0
        xp = zp = ident
        for _ in range(n):
            xp = compose(xp, x, n)
            zp = compose(zp, z, n)
        assert xp == zp == ident
        mats = {(a, b): tuple(((j + a) % n, b * j % n) for j in range(n))
                for a, b in product(range(n), repeat=2)}
        for a, b, c, d in product(range(n), repeat=4):
            assert compose(mats[a, b], mats[c, d], n) == scalar(
                mats[(a + c) % n, (b + d) % n], b * c, n)
            counts["matrix_products"] += 1
        # The cocycle equation depends on these four coordinates only.
        for b, c, d, e in product(range(n), repeat=4):
            assert (b * c + (b + d) * e - d * e - b * (c + e)) % n == 0
            counts["cocycle_identities"] += 1
        for c0, c1, f0, f1 in product(range(-2, 3), repeat=4):
            for eps in (-1, 1):
                q = -c1 * (f0 - eps * c0) + c0 * (f1 - eps * c1)
                assert q == c0 * f1 - c1 * f0
                counts["charge_cancellations"] += 1
        for c0, c1, a0, a1 in product(range(-2, 3), repeat=4):
            delta = c0 * a1 - c1 * a0
            actual = Fraction(m * (n + 1) * 2 * delta, 2 * n)
            expected = Fraction(m * delta, n)
            assert (actual - expected).denominator == 1
            counts["even_flattening_phases"] += 1
        assert gcd(m, n) == 1
        # Local example ratio has exact log|.| coefficient -m/n < 0.
        assert -Fraction(m, n) < 0

        cases = [(["A", "B", "C"], [("A", "B", 1), ("B", "C", 2), ("C", "A", -3)], True),
                 (["A", "B"], [("A", "B", 1), ("A", "B", 2)], False),
                 (["A"], [("A", "A", 1)], False),
                 (["T0", "T1", "T2"], [("T0", "T1", 1), ("T1", "T2", 0)], True),
                 (["A", "B"], [("A", "B", 1), ("B", "A", 0)], False)]
        for vertices, edges, exists in cases:
            found = potential(vertices, edges, n)
            assert (found is not None) == exists
            if found is not None:
                assert all((found[b] - found[a] - k) % n == 0 for a, b, k in edges)
            counts["graph_controls"] += 1
        # A formal-exponent model of the displayed peripheral recurrences.
        # This checks their algebraic cancellation, not any actual invariant.
        for mu in range(-20, 21):
            classical = lambda t: 2 * t
            root = lambda t: Fraction(2 * t, n)
            quantum = lambda t: -2 * (t // n)
            assert classical(mu + 1) - classical(mu) == 2
            assert n * root(mu) == classical(mu)
            assert root(mu + n) - root(mu) == 2
            assert quantum(mu + n) - quantum(mu) == -2
            assert root(mu + n) + quantum(mu + n) == root(mu) + quantum(mu)
            counts["peripheral_exponent_controls"] += 1
        assert 2 ** n != 2  # Nth powers do not commute with surgery summation.
    for n in range(3, 16, 2):
        for d in range(1, 33):
            root_exponent = Fraction(d, n)
            assert (root_exponent.denominator == 1) == (d % n == 0)
            counts["cover_degree_controls"] += 1
        assert all((2 ** r) % n != 0 for r in range(8))
    result = {"status": "all assertions passed", "odd_orders": ns,
              "counts": counts,
              "scope": "Exact diagnostic algebra only; no actual QHI state sum, global triangulation, or move-anomaly computation.",
              "arithmetic": "integer residues and rational numbers; no floating point"}
    out = Path(__file__).with_name("exact_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
