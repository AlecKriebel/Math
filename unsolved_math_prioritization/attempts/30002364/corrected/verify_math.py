"""Exact finite certificate only; launch through the pinned external bootstrap."""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit('Use python -I -S and the pinned external bootstrap.')
from fractions import Fraction
import itertools
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def mul(x, y):
    a, b = x
    d, e = y
    return ((a + (-1) ** b * d) % 4, (b + e) % 2)


H = [(a, b) for b in range(2) for a in range(4)]
identity = (0, 0)
s = (0, 1)
require(len(set(H)) == 8, 'group order')
require(all(mul(x, y) in H for x in H for y in H), 'closure')
require(all(mul(mul(x, y), z) == mul(x, mul(y, z))
            for x in H for y in H for z in H), 'associativity')
require(all(mul(identity, x) == x == mul(x, identity) for x in H), 'identity')
inv = {x: next(y for y in H if mul(x, y) == identity) for x in H}
require(all(mul(inv[x], x) == identity for x in H), 'inverses')
r = (1, 0)
require(mul(mul(s, r), s) == inv[r], 'dihedral relation')

f = dict(zip(H, [-1, -1, -1, 1, -1, 1, 1, -1]))
M = [[f[mul(inv[t], h)] for h in H] for t in H]
a = {h: f[h] + f[mul(s, h)] for h in H}
N = [[a[mul(inv[t], h)] for h in H] for t in H]
require(list(a.values()) == [-2, -2, 0, 2, -2, 2, 0, -2], 'average vector')


def determinant(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    require(all(len(row) == len(a) for row in a), 'square matrix')
    d = Fraction(1)
    for j in range(len(a)):
        p = next((i for i in range(j, len(a)) if a[i][j]), None)
        if p is None:
            return Fraction(0)
        if p != j:
            a[j], a[p] = a[p], a[j]
            d = -d
        pivot = a[j][j]
        d *= pivot
        for i in range(j + 1, len(a)):
            c = a[i][j] / pivot
            a[i] = [x - c * y for x, y in zip(a[i], a[j])]
    return d


require(determinant(M) == 256, 'Hodge determinant')
require(N[4:] == N[:4], 'repeated slope rows')
require(determinant([row[:4] for row in N[:4]]) == 80, 'slope minor')
columns = [tuple(row[j] for row in N) for j in range(8)]
signed_columns = columns + [tuple(-x for x in col) for col in columns]
require(len(set(signed_columns)) == 16, 'root-of-unity collision')
require(all(any(col) for col in columns), 'zero column')
e = [0, 1, 0, 1, 0, -1, 0, -1]
require(all(sum(x * y for x, y in zip(row, e)) == 0 for row in N), 'Tate relation')
require([sum(x * y for x, y in zip(row, e)) for row in M]
        == [0, -2, 0, -2, 0, 2, 0, 2], 'relation is not Hodge invariant')
# Test all unordered degree-two wedges in the sixteen distinct eigenlines.
pairs = [(i, j) for i in range(16) for j in range(i + 1, 16)
         if all(x + y == 0 for x, y in zip(signed_columns[i], signed_columns[j]))]
require(pairs == [(j, j + 8) for j in range(8)], 'unexpected divisor eigenline')
quartic_labels = [1, 3, 8 + 5, 8 + 7]
require(len(set(quartic_labels)) == 4, 'distinct wedge labels')
require(not any(i in quartic_labels and j in quartic_labels for i, j in pairs),
        'quartic line contains a conjugate pair')
require(all(sum(signed_columns[j][t] for j in quartic_labels) == 0 for t in range(8)),
        'quartic line is not Tate')
# Full 16-by-16 centered matrix from the CM type and its local average.
G = [(a, b, c) for c in range(2) for b in range(2) for a in range(4)]

def gmul(x, y):
    z = mul(x[:2], y[:2])
    return z + ((x[2] + y[2]) % 2,)


def ffull(x):
    return (-1) ** x[2] * f[x[:2]]


def afull(x):
    return ffull(x) + ffull(gmul((0, 1, 0), x))

D = [(0, 0, 0), (0, 1, 0)]
require(all(afull(gmul(d, g)) == afull(g) for d in D for g in G), 'left invariance')
right_stabilizer = [k for k in G if all(afull(gmul(g, k)) == afull(g) for g in G)]
require(right_stabilizer == [(0, 0, 0)], 'nontrivial right stabilizer')
# Local mod-5 facts: F=(X^2-4)(X^2-2), X^2-2 irreducible, i has roots.
F = [3, 0, -6, 0, 1]
product = [8, 0, -6, 0, 1]
require([x % 5 for x in F] == [x % 5 for x in product], 'mod-5 factorization')
require([x for x in range(5) if sum(c * x**j for j, c in enumerate(F)) % 5 == 0]
        == [2, 3], 'linear roots')
require(all((x*x - 2) % 5 for x in range(5)), 'quadratic irreducibility')
require((2*2 + 1) % 5 == 0, 'i split')
# F_25 = F_5[b]/(b^2-2).
def f25mul(x, y):
    return ((x[0]*y[0] + 2*x[1]*y[1]) % 5,
            (x[0]*y[1] + x[1]*y[0]) % 5)
z = (1, 0)
for _ in range(5):
    z = f25mul(z, (0, 1))
require(z == (0, 4), 'Frobenius negates b')
require(16 * 3 * (36 - 12)**2 == 27648 == 2**10 * 3**3, 'quartic discriminant')
slopes = [Fraction(x + 2, 4) for x in N[0]]
slopes += [1 - x for x in slopes]
require({str(x): slopes.count(x) for x in set(slopes)} == {'0': 6, '1/2': 4, '1': 6},
        'Newton slopes')
print(json.dumps({'result': 'PASS finite certificate', 'hodge_centered_rank': 8,
                  'hodge_determinant': 256, 'tate_centered_rank': 4,
                  'slope_minor_determinant': 80, 'distinct_signed_columns': 16,
                  'divisor_pair_count': len(pairs), 'exotic_candidate_codimension': 2,
                  'newton_slopes': {'0': 6, '1/2': 4, '1': 6},
                  'geometric_theorems_formally_verified': False}, sort_keys=True))
