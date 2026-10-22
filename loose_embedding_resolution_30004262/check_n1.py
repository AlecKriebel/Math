# AST-derived explicit checks: active under python -O. Finite sanity checks only.
from fractions import Fraction as Q
from itertools import combinations

def d(i, j):
    if i == j:
        return Q(0)
    if i > j:
        i, j = (j, i)
    if i == 0:
        return Q(1, 2 ** j)
    return Q(1, 2 ** i) if j == i + 1 else Q(1, 2 ** i) + Q(1, 2 ** (j + 1))

def f(i):
    return 0 if i == 0 else 2 ** (i - 1)
K = 35
P = list(range(K + 1))
pairs = list(combinations(P, 2))
for a, b, c in combinations(P, 3):
    ds = [d(a, b), d(a, c), d(b, c)]
    if not 2 * max(ds) <= sum(ds):
        raise AssertionError('Exact finite sanity check failed')
forward = {}
backward = {}
for a, b in pairs:
    x, y = (d(a, b), abs(f(a) - f(b)))
    if not (x > 0 and y > 0):
        raise AssertionError('Exact finite sanity check failed')
    if not (x not in forward or forward[x] == y):
        raise AssertionError('Exact finite sanity check failed')
    if not (y not in backward or backward[y] == x):
        raise AssertionError('Exact finite sanity check failed')
    forward[x] = y
    backward[y] = x
print(f'PASS: all {len(list(combinations(P, 3)))} triangles and {len(pairs)} pair classes on Y_{K}; exact rational arithmetic.')
print('This finite test is a sanity check, not the proof for all finite subsets.')
