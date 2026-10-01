#!/usr/bin/env python3
"""Independent round-2 adversarial checks; Python standard library only."""
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
from decimal import Decimal, localcontext
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[2]


def rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    n = len(a[0]) if a else 0
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [x / q for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def solve(matrix, rhs):
    a = [[F(x) for x in row] + [F(y)] for row, y in zip(matrix, rhs)]
    n = len(rhs)
    assert len(a) == len(a[0]) - 1 == n
    for c in range(n):
        pivot = next(i for i in range(c, n) if a[i][c])
        a[c], a[pivot] = a[pivot], a[c]
        q = a[c][c]
        a[c] = [x / q for x in a[c]]
        for i in range(n):
            if i != c and a[i][c]:
                q = a[i][c]
                a[i] = [x - q * y for x, y in zip(a[i], a[c])]
    answer = [row[-1] for row in a]
    assert all(sum(F(x) * y for x, y in zip(row, answer)) == b
               for row, b in zip(matrix, rhs))
    return answer


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def P(x, y, z):
    return (x*x+y*y+z*z-5)**2 - 4*(4-y*y)*(1-z*z)


# Nonorthogonal rank-two ellipses with proportional radicals and a common
# 3-dimensional ambient kernel: D = AB^2 + 2AB^2 = 3AB^2 in R^5.
A = [[F(2), F(1)], [F(0), F(3)], [F(0), F(0)],
     [F(0), F(0)], [F(0), F(0)]]
assert rank(A) == 2
ellipse_cases = 0
for t in [F(-7), F(-1), F(-1, 3), F(0), F(2, 5), F(1), F(9)]:
    v = [(1-t*t)/(1+t*t), 2*t/(1+t*t)]
    assert dot(v, v) == 1
    u = [v[0]/2, (v[1]-v[0]/2)/3, F(17), F(-9), F(4)]
    assert [sum(A[k][j]*u[k] for k in range(5)) for j in range(2)] == v
    p = [3*dot(row, v) for row in A]
    x, y = p[:2]
    assert (3*x-y)**2 + 4*y*y == 324
    assert p[2:] == [0, 0, 0]
    ellipse_cases += 1

# GP witness in R^6: blocks of two distinct Vandermonde columns.
columns = [[F(t**k) for k in range(6)] for t in range(1, 7)]
subsets_checked = 0
for size in range(1, 7):
    for ids in combinations(range(6), size):
        matrix = [[columns[j][i] for j in ids] for i in range(6)]
        assert rank(matrix) == size
        subsets_checked += 1
assert subsets_checked == 63
v1, v2 = [F(3, 5), F(4, 5)], [F(5, 13), F(12, 13)]
assert dot(v1, v1) == dot(v2, v2) == 1
u_targets = [F(0), F(0), F(0), F(0), F(3), F(4)]
w_targets = v1 + v2 + [F(1, 7), F(-2, 7)]
u = solve(columns, u_targets)
w = solve(columns, w_targets)
# J={1,2}. Check the exact collapsed projections for several epsilons.
for eps in [F(1), F(1, 10), F(1, 1000), F(1, 10**6)]:
    ue = [a+eps*b for a, b in zip(u, w)]
    projected = [dot(col, ue) for col in columns]
    assert projected[:4] == [eps*x for x in v1+v2]
    assert projected[4:] == [3+eps/7, 4-2*eps/7]
    for j in range(3):
        assert dot(projected[2*j:2*j+2], projected[2*j:2*j+2]) > 0

# Quantified continuity evidence independent of floating point: for q=(3,4),
# r=(1/7,-2/7), the normalization inequality
# ||(q+eps*r)/||q+eps*r|| - q/||q|||| <= 2 eps ||r||/||q||
# follows from the triangle and reverse triangle inequalities.
# For eps<=1, ||q+eps*r|| >=5-sqrt(5)/7 >4, so no zero is approached.
# The operator norm of [column5,column6] is bounded by its Frobenius norm.
frobenius_squared = sum(x*x for col in columns[4:] for x in col)
error_bound_squared_at_eps_1 = 4 * F(5, 49) * frobenius_squared / 25

# Nongeneric separator checked on independent exact Pythagorean normals.
separator_checks = []
for a, b, c in [(3,4,0), (0,3,4), (12,5,9), (20,21,15)]:
    r2, s2 = a*a+b*b, a*a+c*c
    r, s = isqrt(r2), isqrt(s2)
    assert r*r == r2 and s*s == s2 and r and s
    x, y, z = F(2*a, r)+F(a, s), F(2*b, r), F(c, s)
    assert P(x, y, z) == 0
    separator_checks.append({'normal':[a,b,c], 'point':[str(x),str(y),str(z)]})
assert P(F(0), F(0), F(1)) == 16

# Rank-one stadium branches. Branch points satisfy their translated circle
# and fail the other circle for generic horizontal components.
for a in [F(1,3), F(1), F(9)]:
    for vx, vy in [(F(3,5),F(4,5)), (F(-3,5),F(4,5))]:
        center = a if vx > 0 else -a
        x, y = center+vx, vy
        assert (x-center)**2+y*y == 1
        assert (x+center)**2+y*y != 1

result = {
    'paper_sha256': hashlib.sha256((BASE/'paper.tex').read_bytes()).hexdigest(),
    'proportional_ellipse_cases': ellipse_cases,
    'vandermonde_column_subsets_checked': subsets_checked,
    'u': list(map(str,u)), 'w': list(map(str,w)),
    'gp_exact_epsilon_cases': 4,
    'gp_limit_error_bound_squared_for_epsilon_1': str(error_bound_squared_at_eps_1),
    'separator_checks': separator_checks,
    'separator_value_at_e3': 16,
    'rank_one_stadium_branch_cases': 6,
    'verdict': 'All exact checks passed; these checks do not certify the universal proofs.'
}
print(json.dumps(result, indent=2))
