#!/usr/bin/env python3
"""Exact finite diagnostics for PROOF.md; not a proof assistant or PDE solver."""
from fractions import Fraction as F
from itertools import product
import json

counts = {}

def check(group, assertion):
    assert assertion, group
    counts[group] = counts.get(group, 0) + 1

def zeros(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]

def diagonal(xs):
    m = zeros(len(xs))
    for i, x in enumerate(xs):
        m[i][i] = F(x)
    return m

def tr(m):
    return list(map(list, zip(*m)))

def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]

def conj(u, a):
    return mul(mul(u, a), tr(u))

def frob2(a, b):
    return sum((x-y)**2 for ra, rb in zip(a, b) for x, y in zip(ra, rb))

# Infinite tail identities are verified through the exact finite geometric
# identity plus its explicit remainder, for many finite endpoints.
for n in range(1, 129):
    eps = F(1, 2**(n+2))
    check('error_budget', eps < 1)
    for m in range(n+1, n+10):
        finite = sum(F(1, 2**(j+2)) for j in range(n, m))
        remainder = F(1, 2**(m+1))
        check('geometric_tail', finite + remainder == F(1, 2**(n+1)))
    check('density_error', F(1, 2**n) + F(1, 2**(n+1)) == F(3, 2**(n+1)))

# Every pair (cube,basis-index) enters at its maximum coordinate and stays.
for j in range(1, 33):
    for ell in range(1, 33):
        n = max(j, ell)
        check('dense_schedule', j <= n and ell <= n)
        check('dense_schedule_minimality', not (j <= n-1 and ell <= n-1))

# Sample nonresonance choices. Eigenvalues divided by pi^2 are rational.
# The multi-index bound is exhaustive for these bounded candidate intervals.
nonresonant = []
protected = {F(1, 2), F(5, 4), F(3), F(11, 7)}
for d in (2, 3, 4):
    lower, upper = F(2), F(3)
    m_bound = 11  # 4*upper^2*max(protected)=108, so every m_i<=10.
    sums = {sum(m*m for m in tup) for tup in product(range(1, m_bound), repeat=d)}
    check('multiindex_bound', F(m_bound*m_bound) > 4*upper*upper*max(protected))
    candidates = [lower + F(k, 31) for k in range(1, 31)]
    good = next(a for a in candidates if all(F(s, 4)/(a*a) not in protected for s in sums))
    check('cube_choice_interval', lower < good < upper)
    for s in sums:
        check('cube_nonresonance', F(s, 4)/(good*good) not in protected)
    nonresonant.append({'dimension': d, 'half_width': str(good), 'normalized_protected': sorted(map(str, protected))})

# Exact finite-dimensional model: nested spectral projections undergo small
# orthogonal rotations. This tests algebra in the fixed-rank argument, not
# the analytic window-convergence lemma or an actual Dirichlet domain.
N = 6
identity = diagonal([1]*N)
u = identity
previous = {}
for n in range(1, N+1):
    if n > 1:
        step = n-1
        t = F(1, 2**(step+6))
        c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
        v = diagonal([1]*N)
        v[0][0] = v[n-1][n-1] = c
        v[0][n-1], v[n-1][0] = -s, s
        check('rotation_identity', c*c+s*s == 1)
        u = mul(u, v)
    check('orthogonal_matrix', mul(u, tr(u)) == identity)
    r = conj(u, diagonal([F(1, j+2) if j < n else 0 for j in range(N)]))
    current = {}
    for k in range(1, n+1):
        p = conj(u, diagonal([1 if j < k else 0 for j in range(N)]))
        current[k] = p
        check('projection_selfadjoint', tr(p) == p)
        check('projection_idempotent', mul(p, p) == p)
        check('projection_rank', sum(p[j][j] for j in range(N)) == k)
        check('projection_commutes', mul(p, r) == mul(r, p))
        if k > 1:
            check('projection_nested', mul(current[k-1], p) == current[k-1])
        if k < n:
            check('projection_step_bound', frob2(p, previous[k]) < F(1, 2**((n-1)+2))**2)
    # The largest projection contains all of the currently introduced
    # coordinate test vectors, exactly in this model.
    check('model_birth_cutoff', current[n] == diagonal([1 if j < n else 0 for j in range(N)]))
    previous = current

# A degenerate eigenspace can be stable while its individual eigenvectors
# are not perturbatively close to a previously chosen basis. The block
# [[1,t],[t,1]] splits at every t>0 with fixed +/- eigenvector directions.
for power in range(1, 33):
    t = F(1, 2**power)
    block = [[F(1), t], [t, F(1)]]
    for eig, vec in ((1+t, [F(1), F(1)]), (1-t, [F(1), F(-1)])):
        check('degenerate_split', [sum(row[j]*vec[j] for j in range(2)) for row in block] == [eig*x for x in vec])
    check('whole_degenerate_space', mul(diagonal([1, 1]), block) == block)

print(json.dumps({
    'status': 'PASS',
    'assertions': sum(counts.values()),
    'groups': counts,
    'nonresonant_examples': nonresonant,
    'arithmetic': 'exact Python Fraction arithmetic',
    'scope': 'finite algebraic diagnostics and summability/scheduling identities only',
    'not_verified_by_code': [
        'infinite-dimensional theorem',
        'finite-window Mosco or norm-resolvent convergence',
        'numerical admissible window sizes',
        'historical novelty or literature completeness'
    ]
}, indent=2, sort_keys=True))
