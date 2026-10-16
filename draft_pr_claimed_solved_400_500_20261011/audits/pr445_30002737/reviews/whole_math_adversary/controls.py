#!/usr/bin/env python3
"""Independent exact algebra and deterministic geometry controls.

Every essential guard is an explicit exception, including optimized execution.
Finite controls do not prove the credited infinite Rudin-Shapiro theorem.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


C = [(F(0), F(0)), (F(1, 10), F(1, 10)), (F(1, 3), F(0)), (F(0), F(1, 3))]
mean = [F(1), F(1), F(1, 2), F(1, 2)]


def occ_polynomial(slot, i, j):
    if slot < 2:
        return {(): F(1)}
    variable = ('x', i) if slot == 2 else ('y', j)
    return {(): F(1, 2), (variable,): F(1, 2)}


def multiply_expectation(p, q):
    result = F(0)
    for a, av in p.items():
        for b, bv in q.items():
            variables = a + b
            # Each tested factor contains at most two symbols. The exact moment
            # functional uses zero means and delta two-point correlation only.
            factor = F(1)
            for family in ['x', 'y']:
                indices = [i for fam, i in variables if fam == family]
                require(len(indices) <= 2, 'unsupported higher moment')
                if len(indices) == 1 or (len(indices) == 2 and indices[0] != indices[1]):
                    factor = F(0)
            result += av * bv * factor
    return result


def displacement(c, d, m, n):
    return (C[d][0] - C[c][0] + m, C[d][1] - C[c][1] + n)


markers = [(c, d) for c, d in product(range(4), repeat=2)
           if tuple((C[d][j] - C[c][j]) % 1 for j in [0, 1]) == C[1]]
require(markers == [(0, 1)], 'marker collision')
require(len(set(C)) == 4, 'slot collision')
require(all((30 * t).denominator == 1 for c in C for t in c), 'motif off grid')

pair_checks = 0
collision_checked = 0
for m, n in product(range(-3, 4), repeat=2):
    direct = defaultdict(F)
    decomposition = defaultdict(F)
    terms = defaultdict(int)
    for c, d in product(range(4), repeat=2):
        actual = multiply_expectation(occ_polynomial(c, 0, 0), occ_polynomial(d, m, n))
        target = mean[c] * mean[d]
        if c == d == 2 and m == 0:
            target += F(1, 4)
        if c == d == 3 and n == 0:
            target += F(1, 4)
        require(actual == target, f'pair identity fails {c,d,m,n}')
        r = displacement(c, d, m, n)
        direct[r] += actual
        decomposition[r] += target
        terms[r] += 1
        pair_checks += 1
    require(direct == decomposition, 'colliding coefficient mismatch')
    collision_checked += sum(v > 1 for v in terms.values())


def rs(i):
    if i == 0:
        return 1
    if i == -1:
        return -1
    q, r = divmod(i, 4)
    return rs(q) * (1 if r < 2 or (q + r) % 2 == 0 else -1)


rho = {'a': 'ab', 'b': 'ac', 'c': 'db', 'd': 'dc'}
left, right = 'c', 'a'
for _ in range(5):
    for __ in range(2):
        left = ''.join(rho[t] for t in left)
        right = ''.join(rho[t] for t in right)
bilateral = [1 if t in 'ab' else -1 for t in left + right]
require(bilateral == [rs(i) for i in range(-len(left), len(right))], 'source recursion mismatch')
require(all((1 if t in 'ab' else -1) == (-1) ** ((i & (i >> 1)).bit_count())
            for i, t in enumerate(right)), 'positive binary formula mismatch')

# Four-letter primitive incidence implies primitive 16-letter block incidence:
# every coordinate letter occurs in every 3rd iterate, hence each letter pair
# occurs at some independent (row,column) position of each 3rd block iterate.
images = dict(rho)
for _ in range(2):
    images = {c: ''.join(rho[t] for t in w) for c, w in images.items()}
require(all(set(w) == set(rho) for w in images.values()), 'rho third iterate not primitive')
for c, d in product(rho, repeat=2):
    require({(a, b) for a in images[c] for b in images[d]} == set(product(rho, repeat=2)),
            'product block third iterate not primitive')

# Exact physical counts include the trimmed source and target boundaries.
grid = [(int(30 * c[0]), int(30 * c[1])) for c in C]
physical = []
shifts = sorted({(grid[d][0] - grid[c][0] + 30*m,
                  grid[d][1] - grid[c][1] + 30*n)
                 for c, d in product(range(4), repeat=2)
                 for m, n in product(range(-1, 2), repeat=2)})
for N in [32, 64, 128]:
    xs, ys = [rs(i - N//2) for i in range(N)], [rs(i + 71) for i in range(N)]
    points = set()
    for i, j in product(range(N), repeat=2):
        for slot in [0, 1] + ([2] if xs[i] == 1 else []) + ([3] if ys[j] == 1 else []):
            points.add((30*i+grid[slot][0], 30*j+grid[slot][1]))
    worst = F(0)
    for r in shifts:
        direct = sum((p[0]+r[0], p[1]+r[1]) in points for p in points)
        count = 0
        limit = F(0)
        for c, d in product(range(4), repeat=2):
            rem = [r[k] - grid[d][k] + grid[c][k] for k in [0, 1]]
            if any(t % 30 for t in rem):
                continue
            m, n = (t//30 for t in rem)
            limit += multiply_expectation(occ_polynomial(c, 0, 0), occ_polynomial(d, m, n))
            column = sum((c != 2 or xs[i] == 1) and (d != 2 or xs[i+m] == 1)
                         for i in range(max(0, -m), min(N, N-m)))
            row = sum((c != 3 or ys[j] == 1) and (d != 3 or ys[j+n] == 1)
                      for j in range(max(0, -n), min(N, N-n)))
            count += column * row
        require(direct == count, f'finite physical count mismatch {N,r}')
        worst = max(worst, abs(F(direct, N*N) - limit))
    physical.append({'N': N, 'points': len(points), 'displacements': len(shifts),
                     'worst_limit_error': str(worst), 'exact_count_matches': True})


def flow_interval(t):
    # Partition by all symbolic jumps, deriving section integration directly.
    low = math.floor(t)-2
    high = math.ceil(t)+3
    breaks = sorted({F(0), F(1)} | {F(j)-t for j in range(low, high) if 0 < F(j)-t < 1})
    correlation = F(0)
    for a, b in zip(breaks, breaks[1:]):
        if math.floor((a+b)/2+t) == 0:
            correlation += b-a
    return correlation


flow_checks = 0
for denom in [1, 2, 3, 5, 7, 11, 17]:
    for numerator in range(-4*denom, 4*denom+1):
        t = F(numerator, denom)
        require(flow_interval(t) == max(F(0), 1-abs(t)), f'flow mismatch {t}')
        flow_checks += 1
require(flow_interval(F(0)) == 1, 'zero observable norm')
require(flow_interval(F(1)) == flow_interval(F(-1)) == 0, 'bad flow endpoints')
origin = sum(w*w for w in mean) + F(1, 2)
require(origin == sum(mean) == 3 and sum(mean)**2 == 9, 'normalization mismatch')

result = {'status': 'PASS', 'optimized': not __debug__, 'reviewer': '/root/pr445_whole_math_adversary',
          'marker_pairs': markers, 'moment_pair_checks': pair_checks,
          'collision_locations_checked': collision_checked, 'bilateral_sites': len(bilateral),
          'product_primitive_depth': 3, 'physical_counts': physical,
          'flow_checks': flow_checks, 'density': '3', 'origin_autocorrelation': '3',
          'origin_bragg_intensity': '9', 'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'limitations': 'Finite exact algebra/geometry only. Infinite theorem reconstructed separately; no priority certificate.'}
print(json.dumps(result, indent=2))
