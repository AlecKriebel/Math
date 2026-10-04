#!/usr/bin/env python3
"""Independent, exact audit controls for the seven scoped rank-663 claims.

Only Python's standard library is used. These finite controls are not a proof
certificate for the analytic arguments or a solution of the original problem.
No author helper is imported, and no input file is modified.
"""
from fractions import Fraction as Q
from collections import Counter
from itertools import product
import json

counts = Counter()

def check(group, condition):
    counts[group] += 1
    if not condition:
        raise AssertionError((group, counts[group]))

def mv(matrix, vector):
    return [sum((a*b for a, b in zip(row, vector)), Q(0)) for row in matrix]

def mul(x, y):
    return [a*b for a, b in zip(x, y)]

def gform(matrix, x, y):
    lxy, lx, ly = mv(matrix, mul(x, y)), mv(matrix, x), mv(matrix, y)
    return [(u-v-w)/2 for u, v, w in zip(lxy, mul(x, ly), mul(y, lx))]

# Reconstruct arbitrary-rate reset generators as matrices; test more than three
# states and non-unit rates, independently of the author's helper functions.
for n in (2, 3, 4, 5):
    weights = [Q(2**i, 2**n-1) for i in range(n)]
    for rate in (Q(1, 3), Q(2), Q(7, 2)):
        matrix = [[rate*(weights[j]-(i == j)) for j in range(n)] for i in range(n)]
        for row in matrix:
            check('generator_row_sums', sum(row) == 0)
        for j in range(n):
            check('invariance', sum(weights[i]*matrix[i][j] for i in range(n)) == 0)
            for i in range(n):
                check('reversibility', weights[i]*matrix[i][j] == weights[j]*matrix[j][i])
        tests = list(product((-1, 0, 2), repeat=n))
        for values in tests:
            f = list(map(Q, values))
            mean = sum(p*v for p, v in zip(weights, f))
            centered = [v-mean for v in f]
            variance = sum(p*v*v for p, v in zip(weights, centered))
            gf = gform(matrix, f, f)
            lg = mv(matrix, gf)
            glf = gform(matrix, f, mv(matrix, f))
            g2 = [a/2-b for a, b in zip(lg, glf)]
            for i in range(n):
                check('general_rate_gamma', gf[i] == rate*(variance+centered[i]**2)/2)
                check('general_rate_gamma2', g2[i] == rate**2*(3*variance+centered[i]**2)/4)
                for dim in (Q(1, 2), Q(1), Q(4), Q(17)):
                    k = rate/2-2*rate/dim
                    remainder = g2[i]-k*gf[i]-mv(matrix, f)[i]**2/dim
                    check('general_rate_BE_profile', remainder == rate**2*(Q(1, 2)+1/dim)*variance)
                    check('general_rate_BE_nonnegative', remainder >= 0)

# A coupling is a nonnegative measure with exactly the stated marginals.
# Work with abstract mixture weights; no exponential approximation is needed.
nu = (Q(1, 11), Q(3, 11), Q(7, 11))
for a in (Q(1, 4), Q(1, 2), Q(1)):
    for b in (Q(0), a/2, a):
        for x in range(3):
            for y in range(3):
                coupling = [[Q(0) for _ in range(3)] for _ in range(3)]
                coupling[x][y] += b
                for z in range(3):
                    coupling[z][z] += (1-a)*nu[z]
                    coupling[x][z] += (a-b)*nu[z]
                for z in range(3):
                    check('coupling_source_marginal', sum(coupling[z]) == a*(z == x)+(1-a)*nu[z])
                    check('coupling_target_marginal', sum(row[z] for row in coupling) == b*(z == y)+(1-b)*nu[z])
                check('coupling_nonnegative', all(c >= 0 for row in coupling for c in row))

def exp_minus_bounds(x):
    """Alternating Taylor enclosure for exp(-x), 0<=x<=1/2."""
    assert 0 <= x <= Q(1, 2)
    total = term = Q(1)
    lower = upper = Q(1)
    for k in range(1, 22):
        term *= -x/k
        total += term
        if k % 2:
            lower = total
        else:
            upper = total
    return lower, upper

def integrate_abs_affine(slope, intercept, left, right):
    if slope and left < -intercept/slope < right:
        root = -intercept/slope
        return (integrate_abs_affine(slope, intercept, left, root)
                + integrate_abs_affine(slope, intercept, root, right))
    signed = slope*(right*right-left*left)/2+intercept*(right-left)
    return abs(signed)

def interval_w1(a, b, x, y):
    """Exact integral of the absolute CDF difference for uniform-reset laws."""
    nodes = sorted(set((Q(0), x, y, Q(1))))
    answer = Q(0)
    for left, right in zip(nodes, nodes[1:]):
        mid = (left+right)/2
        answer += integrate_abs_affine(b-a, a*(x <= mid)-b*(y <= mid), left, right)
    return answer

# Unlike the author suite, check the actual W1 on a continuum example, not just
# its coupling upper bound. Exponentials are enclosed by exact rational series.
positions = [Q(i, 6) for i in range(7)]
root_times = [Q(i, 12) for i in range(7)]
for u, v in product(root_times, repeat=2):
    if not u < v:
        continue
    s, t, q = u*u, v*v, v-u
    alo, ahi = exp_minus_bounds(2*s)
    blo, bhi = exp_minus_bounds(2*t)
    elo, ehi = exp_minus_bounds(s)
    a, b = (alo+ahi)/2, (blo+bhi)/2
    # W1 changes by at most |delta a|+|delta b| on this diameter-one space.
    error = (ahi-alo+bhi-blo)/2
    for x, y in product(positions, repeat=2):
        if x == y:
            continue
        r = abs(x-y)
        w = interval_w1(a, b, x, y)
        check('actual_interval_W1_enclosure', w+error <= elo*r+8*q*q/r)
        check('interval_coupling_upper', w <= b*r+(a-b))
        if x < y:
            check('interval_CDF_formula', w == a*(y-x)+(a-b)*(x*x-y+Q(1, 2)))

# Exact witnesses refute tempting stronger statements; PASS means the forbidden
# stronger statement was rejected, rather than the forbidden statement passed.
for dim in range(1, 101):
    p = Q(1, dim+2)
    g, variance = 1-p, p*(1-p)
    check('reject_finite_BE_at_curvature_one', 2*variance-4*g*g/dim < 0)
    for k in (Q(-1), Q(0), Q(1, 2), Q(9, 10)):
        finite_dim = 4/(1-k)
        check('reject_no_finite_BE_at_any_curvature', (3-k)*variance+(1-k-4/finite_dim)*g*g >= 0)

for p in (Q(1, 100), Q(1, 4), Q(1, 2)):
    # For delta_0 and (1-p)delta_0+p delta_1, W1=p and W2^2=p.
    check('reject_W1_to_W2_reversal', p*p < p)

for r in (Q(1, 20), Q(1, 4), Q(2, 5)):
    a = Q(2, 3)
    # Uniform interval, x=0, y=r: the right unequal-time derivative is
    # 2*a*(1/2-r)>0, whereas at optimal equal-time kappa=2 the penalty
    # is quadratic in the time increment. Thus no finite C repairs kappa=2.
    check('reject_optimal_reset_curvature_upgrade', 2*a*(Q(1, 2)-r) > 0)

for u, v in product(root_times, repeat=2):
    if u > v:
        continue
    tau = Q(2, 3)*(u*u+u*v+v*v)
    check('heat_time_gap_factor', tau-2*u*u == Q(2, 3)*(v-u)*(v+2*u))
    check('heat_time_gap_sign', tau >= 2*u*u)

for n in range(1, 101):
    partial = sum((Q(1, 4**j) for j in range(1, n+1)), Q(0))
    check('hilbert_cube_diameter_tail', 3*partial == 1-Q(1, 4**n))

print(json.dumps({
    'status': 'PASS',
    'target': 'rank 663 / 4000018 / AMR-039-0018',
    'total_assertions': sum(counts.values()),
    'assertions_by_group': dict(sorted(counts.items())),
    'arithmetic': 'Python fractions.Fraction; exact rational arithmetic including certified exponential enclosures',
    'limits': 'Finite controls only. Universal analytic arguments and source theorem applicability require the written audit.',
}, indent=2, sort_keys=True))
