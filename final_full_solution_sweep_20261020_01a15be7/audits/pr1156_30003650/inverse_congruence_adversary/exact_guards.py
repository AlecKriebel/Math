"""Exact rational guards for the authored congruence audit; no CP-rank oracle.

The universal proof is in REPORT.md. These finite checks exercise identities,
strictness bounds, singular ranks, sparse pullbacks and excluded endpoints.
The program writes only to stdout and uses no assertions.
"""

from fractions import Fraction as Q
import json


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def identity(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def perturb(n, t):
    return [[Q(i == j) + t for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(x) for x in zip(*a)]


def product(a, b):
    return [[sum((x * y for x, y in zip(row, col)), Q(0))
             for col in transpose(b)] for row in a]


def gram(a):
    return product(a, transpose(a))


def rank(a):
    rows = [row[:] for row in a]
    nr, nc, pivot = len(rows), len(rows[0]), 0
    for col in range(nc):
        indices = [i for i in range(pivot, nr) if rows[i][col] != 0]
        if not indices:
            continue
        chosen = indices[0]
        rows[pivot], rows[chosen] = rows[chosen], rows[pivot]
        scale = rows[pivot][col]
        rows[pivot] = [x / scale for x in rows[pivot]]
        for i in range(nr):
            if i != pivot:
                scale = rows[i][col]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
        if pivot == nr:
            break
    return pivot


def positive(a):
    return all(x > 0 for row in a for x in row)


cases = []
for n in range(1, 9):
    for r in range(1, n + 1):
        sparse = [[Q((j + 1) if i == j else 0) for j in range(r)]
                  for i in range(n)]
        b = product(perturb(n, Q(1, n + 2)), sparse)
        b = [[x * Q(1, 10 ** i) for x in row] for i, row in enumerate(b)]
        # Nonminimal repeated columns check that the positivity bound does not
        # require a shortest positive factor.
        b = [row + [2 * row[0], 7 * row[-1]] for row in b]
        sums = [sum(col, Q(0)) for col in transpose(b)]
        alpha = min(b[i][j] / sums[j] for i in range(n) for j in range(r + 2))
        t = alpha / 2
        require(Q(0) < t < Q(1, n), 'parameter-domain')
        tmat = perturb(n, -t)
        inv = perturb(n, t / (1 - n * t))
        require(product(tmat, inv) == identity(n), 'right-inverse')
        require(product(inv, tmat) == identity(n), 'left-inverse')
        require(positive(inv), 'inverse-strictly-positive')
        tb = product(tmat, b)
        require(positive(tb), 'forward-factor-strictly-positive')
        require(all(tb[i][j] >= b[i][j] / 2
                    for i in range(n) for j in range(r + 2)), 'half-margin')
        require(product(inv, tb) == b, 'factor-roundtrip')
        a = gram(b)
        c = product(product(tmat, a), transpose(tmat))
        require(c == gram(tb), 'forward-congruence')
        require(product(product(inv, c), transpose(inv)) == a, 'gram-roundtrip')
        require(rank(b) == rank(a) == rank(tb) == rank(c) == r, 'singular-rank')
        pulled = product(inv, sparse)
        require(positive(pulled), 'sparse-nonzero-columns-pullback')
        zero = [[Q(0)] for _ in range(n)]
        require(not positive(product(inv, zero)), 'zero-column-is-excluded')
        require(positive(product(perturb(n, Q(1, 13)), sparse)), 'S-forward-strict')
        cases.append({'n': n, 'ordinary_rank': r, 'factor_columns': r + 2,
                      't': str(t), 'alpha': str(alpha)})

# Endpoint guards show why the proof uses a strict safe interval.
singular_t = perturb(2, -Q(1, 2))
require(rank(singular_t) == 1, 'excluded-inverse-endpoint')
endpoint_b = [[Q(1)], [Q(3)]]
endpoint_tb = product(perturb(2, -Q(1, 4)), endpoint_b)
require(endpoint_tb == [[Q(0)], [Q(2)]], 'alpha-endpoint-loses-strictness')
require(not positive(endpoint_tb), 'alpha-endpoint-not-positive')

print(json.dumps({'status': 'pass', 'arithmetic': 'exact-rational',
                  'rank_stratum_cases': len(cases), 'cases': cases,
                  'excluded_endpoint_guards': 2,
                  'limitation': 'Finite algebra guards; no minimal-factor or CP-rank certification.'},
                 sort_keys=True, indent=2))
