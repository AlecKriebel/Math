#!/usr/bin/env python3
"""Exact finite controls for Turn 5; Python standard library only."""
from fractions import Fraction as Q
import json


def mul_linear(poly, root):
    out = [Q(0)] * (len(poly) + 1)
    for i, c in enumerate(poly):
        out[i] -= c * root
        out[i + 1] += c
    return out


def lagrange(nodes, a):
    out, den = [Q(1)], Q(1)
    for b in nodes:
        if b != a:
            out = mul_linear(out, b)
            den *= a - b
    return [c / den for c in out]


def evaluate(poly, x):
    out = Q(0)
    for c in reversed(poly):
        out = out * x + c
    return out


def main():
    checks = 0

    def check(b):
        nonlocal checks
        assert b
        checks += 1

    for d in range(7):
        nodes = list(range(-d, d + 1))
        L = {a: lagrange(nodes, a) for a in nodes}
        for a in nodes:
            for b in nodes:
                check(evaluate(L[a], b) == int(a == b))
        # Deliberately not necessarily theta-symmetric: the theorem is
        # valid on the whole square and hence on the invariant subspace.
        C = {(a, b): Q((13 * a * a + 7 * a * b - 11 * b + 5) % 19 - 9)
             if abs(a - b) <= d else Q(0)
             for a in nodes for b in nodes}
        M = {(i, j): sum(c * a ** i * b ** j for (a, b), c in C.items())
             for i in range(2 * d + 1) for j in range(2 * d + 1)}
        # Factor the inverse transform into two exact matrix products.
        left = {(a, j): sum(L[a][i] * M[i, j] for i in range(2 * d + 1))
                for a in nodes for j in range(2 * d + 1)}
        rec = {(a, b): sum(left[a, j] * L[b][j] for j in range(2 * d + 1))
               for a in nodes for b in nodes}
        for e, c in C.items():
            check(rec[e] == c)
        N = 2 * d + 1
        residues = {(a % N, b % N): c for (a, b), c in C.items()}
        check(len(residues) == len(C))
        for (a, b), c in C.items():
            check(residues[a % N, b % N] == c)

    print(json.dumps({"status": "PASS", "exact_assertions": checks,
                      "support_bounds_tested": list(range(7)),
                      "scope": "Finite-jet inversion and no aliasing; no topological input construction"},
                     indent=2))


if __name__ == "__main__":
    main()
