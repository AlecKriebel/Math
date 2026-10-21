from fractions import Fraction as Q
from collections import defaultdict
from itertools import combinations
from math import gcd
import json
from pathlib import Path

def check(D, M):
    groups = defaultdict(list)
    for m in range(1, M + 1):
        for mu in range(m):
            if (mu * mu - D) % m == 0:
                x = Q(mu, m)
                p, q = (x.numerator, x.denominator)
                k = m // q
                if not (mu == k * p and m == k * q and (D % k == 0)):
                    raise AssertionError('exact check failed')
                if not gcd(q, D) == 1:
                    raise AssertionError('exact check failed')
                if not (k * k * p * p - D) % q == 0:
                    raise AssertionError('exact check failed')
                groups[x].append((m, mu, k))
    collisions = []
    for x, labels in groups.items():
        if len(labels) > 1:
            for (m, mu, k), (mm, mumu, kk) in combinations(labels, 2):
                if not (k != kk and (k * k - kk * kk) % x.denominator == 0):
                    raise AssertionError('exact check failed')
                if not (m <= D * (D * D - 1) and mm <= D * (D * D - 1)):
                    raise AssertionError('exact check failed')
            collisions.append({'position': str(x), 'labels': labels})
    for alpha, beta in [(Q(1), Q(2)), (Q(3, 2), Q(7, 3)), (Q(2), Q(3))]:
        for m in range(1, M + 1):
            if not (alpha <= Q(M, m) < beta) == (Q(M) / beta < m <= Q(M) / alpha):
                raise AssertionError('exact check failed')
    points = sorted((x for x, labels in groups.items() for _ in labels))
    N = len(points)
    gaps = [points[(i + 1) % N] - points[i] + (i == N - 1) for i in range(N)]
    if not (sum(gaps) == 1 and sum((N * g for g in gaps)) == N):
        raise AssertionError('exact check failed')
    if not sum((g == 0 for g in gaps)) == N - len(groups):
        raise AssertionError('exact check failed')
    return {'D': D, 'M': M, 'labels': N, 'positions': len(groups), 'zero_gaps': N - len(groups), 'collisions': collisions}
import sympy as s
v, E, z, t = s.symbols('v E z t', positive=True)
a = lambda w: s.diag(s.sqrt(w), 1 / s.sqrt(w))
k = s.Matrix([[1, 1], [-1, 1]]) / s.sqrt(2)
if not s.simplify(a(z) * k * a(1 / v) * a(E) - a(z) * k * a(E / v)) == s.zeros(2):
    raise AssertionError('exact check failed')
y, u = s.symbols('y u', positive=True)
n = lambda w: s.Matrix([[1, w], [0, 1]])
if not s.simplify(a(y) * n(u) - n(y * u) * a(y)) == s.zeros(2):
    raise AssertionError('exact check failed')
h = lambda x: -1 / x
if not h(Q(1)) - h(Q(-1)) == -2:
    raise AssertionError('exact check failed')
results = [check(D, 500) for D in [2, 3, 6, 7, 10, 11, 14, 15, 30]]
Path('exact_audit_results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps([{k: v for k, v in r.items() if k != 'collisions'} for r in results], indent=2))
