#!/usr/bin/env python3
"""Exact finite controls for the known parity-shift construction; no dependencies."""
from fractions import Fraction
from itertools import product
from math import prod
import json

checks = 0

def check(condition):
    global checks
    checks += 1
    assert condition

def rank(rows):
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length()-1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return len(pivots)

def parity_rows(shape):
    points = list(product(*(range(q) for q in shape)))
    index = {p: i for i, p in enumerate(points)}
    rows = []
    for n, q in enumerate(shape):
        for other in product(*(range(shape[j]) for j in range(len(shape)) if j != n)):
            row = 0
            for b in range(q):
                p = list(other)
                p.insert(n, b)
                row |= 1 << index[tuple(p)]
            rows.append(row)
    return points, rows

cases = []
for shape in [(2,), (4,), (2, 2), (4, 4), (4, 8), (2, 4, 8), (4, 8, 16)]:
    points, rows = parity_rows(shape)
    index = {p: i for i, p in enumerate(points)}
    free = list(product(*(range(q-1) for q in shape)))
    # Interpolation basis: one free site and every distinguished-coordinate replacement.
    basis = []
    for f in free:
        v = 0
        for p in product(*[(f[n], shape[n]-1) for n in range(len(shape))]):
            v |= 1 << index[p]
        basis.append(v)
        for row in rows:
            check((row & v).bit_count() % 2 == 0)
        check([int(bool(v & (1 << index[p]))) for p in free] == [int(p == f) for p in free])
    kernel_dimension = len(points)-rank(rows)
    check(kernel_dimension == prod(q-1 for q in shape))
    check(rank(basis) == kernel_dimension)
    # Every translation by bitwise XOR preserves a nontrivial sample codeword.
    v = 0
    for i, b in enumerate(basis):
        if i % 3 != 1:
            v ^= b
    for shift in points:
        translated = 0
        for p in points:
            if v & (1 << index[p]):
                translated |= 1 << index[tuple(p[j]^shift[j] for j in range(len(shape)))]
        for row in rows:
            check((row & translated).bit_count() % 2 == 0)
    # A fresh tail coordinate forces every variable supported in the old window to zero.
    extended_points, extended_rows = parity_rows(shape+(4,))
    old_columns = {j: index[p[:-1]] for j, p in enumerate(extended_points) if p[-1] == 0}
    restricted_rows = []
    for row in extended_rows:
        restricted = sum(1 << col for j, col in old_columns.items() if row & (1 << j))
        restricted_rows.append(restricted)
    check(rank(restricted_rows) == len(points))
    cases.append({'shape': list(shape), 'coordinates': len(points),
                  'parity_rank': rank(rows), 'kernel_dimension': kernel_dimension,
                  'fresh_tail_support_kernel_dimension': len(points)-rank(restricted_rows)})

p = Fraction(1)
product_bounds = []
for n in range(1, 41):
    p *= 1-Fraction(1, 2**(n+1))
    union_bound = Fraction(1,2)+Fraction(1,2**(n+1))
    check(p >= union_bound)
    tail_lower_bound = p * (1-Fraction(1,2**(n+1)))
    check(tail_lower_bound >= Fraction(1,2))
    if n in [1, 2, 3, 10, 40]:
        product_bounds.append({'n': n, 'partial_product': str(p),
                               'infinite_product_lower_bound': str(tail_lower_bound)})
# Adversarial boundary: constant size two has positive finite ratios but zero limit.
for n in range(1,41):
    check(Fraction(prod(2-1 for _ in range(n)), 2**n) == Fraction(1,2**n))

print(json.dumps({'all_passed': True, 'assertions': checks, 'finite_cases': cases,
                  'positive_product_bounds': product_bounds,
                  'boundary_control': 'q_n=2 has entropy ratios 2^(-N), tending to zero',
                  'scope': 'Finite exact controls; the infinite proof is in verification.md'},
                 indent=2, sort_keys=True))
