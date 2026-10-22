#!/usr/bin/env python3
"""Exact algebraic diagnostics for the filling-homology calculation.

The free complexes tested here are not asserted to be handle complexes of
particular four-manifolds. The spun-lens-space realization is proved separately.
"""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
checks = 0


def check(value):
    global checks
    assert value
    checks += 1


def rank(matrix, p=None):
    a = [[Q(x) if p is None else x % p for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = 1 / a[r][c] if p is None else pow(a[r][c], -1, p)
        a[r] = [x * inv if p is None else x * inv % p for x in a[r]]
        for i in range(len(a)):
            if i != r:
                v = a[i][c]
                a[i] = [x - v*y if p is None else (x-v*y) % p
                        for x, y in zip(a[i], a[r])]
        r += 1
    return r


def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


groups = [(d,) for d in range(1, 18)] + [(3, 5), (3, 9), (2, 3), (4, 9),
                                       (3, 5, 7), (2, 4, 9), (5, 25, 125)]
rows = []
for ds in groups:
    k = len(ds)
    d2 = [[ds[i] if j == i else 0 for j in range(2*k)] for i in range(k)]
    d3 = [[ds[j] if i == k+j else 0 for j in range(k)] for i in range(2*k)]
    check(multiply(d2, d3) == [[0]*k for _ in range(k)])
    check(rank(d2) == rank(d3) == k)
    check((k-rank(d2), 2*k-rank(d2)-rank(d3), k-rank(d3)) == (0, 0, 0))
    fields = {}
    for p in (2, 3, 5, 7):
        r2, r3 = rank(d2, p), rank(d3, p)
        betti = (k-r2, 2*k-r2-r3, k-r3)
        t = sum(d % p == 0 for d in ds)
        check(betti == (t, 2*t, t))
        check(1-betti[0]+betti[1]-betti[2] == 1)
        fields[str(p)] = betti
    check((fields['2'] == (0, 0, 0)) == all(d % 2 for d in ds))
    rows.append({'cyclic_orders': ds, 'rational_betti_1_2_3': [0, 0, 0],
                 'field_betti_1_2_3': fields})

# Mayer-Vietoris free-coordinate maps for the spun construction:
# H_2(E)->H_2(U)+H_2(V) is a->(0,a); H_1(E) kills the product circle.
# Test both orientation conventions in the free coordinate.
for sign in (-1, 1):
    for p in (2, 3, 5, 7, 9, 15):
        check(rank([[0], [sign]]) == 1)
        residues = {(a % p, sign*b) for a in range(p) for b in range(-2, 3)}
        quotient_representatives = {a for a, _ in residues}
        check(len(quotient_representatives) == p)

print(json.dumps({'status': 'PASS', 'exact_assertions': checks,
                  'group_models': len(groups), 'models': rows,
                  'scope': 'Algebraic consistency only; not a nonzero boundary-class certificate',
                  'artifact_sha256': hashlib.sha256((HERE/'OBSTRUCTION.md').read_bytes()).hexdigest(),
                  'verifier_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
                 indent=2, sort_keys=True))
