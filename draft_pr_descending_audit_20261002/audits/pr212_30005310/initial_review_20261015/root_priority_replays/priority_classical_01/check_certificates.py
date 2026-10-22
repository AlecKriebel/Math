#!/usr/bin/env python3
"""Small exact checks for the classical K4,4 specialization; standard library only.

No random sampling, numerical ranks, network, or writes. Run from any directory.
The JSON output is a finite certificate; the report supplies the analytic arguments.
"""
from fractions import Fraction as Q
from itertools import combinations
import json


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[sum(x * y for x, y in zip(r, c)) for c in transpose(b)] for r in a]


def determinant(a):
    a = [[Q(x) for x in r] for r in a]
    answer = Q(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            a[pivot], a[j] = a[j], a[pivot]
            answer = -answer
        value = a[j][j]
        answer *= value
        a[j] = [x / value for x in a[j]]
        for i in range(j + 1, len(a)):
            value = a[i][j]
            a[i] = [x - value * y for x, y in zip(a[i], a[j])]
    return answer


def pivot_columns(a):
    a = [[Q(x) for x in r] for r in a]
    row, answer = 0, []
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot], a[row] = a[row], a[pivot]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(len(a)):
            if i != row:
                value = a[i][col]
                a[i] = [x - value * y for x, y in zip(a[i], a[row])]
        answer.append(col)
        row += 1
        if row == len(a):
            break
    return answer


def identity(n):
    return [[Q(int(i == j)) for j in range(n)] for i in range(n)]


def gram(a):
    return multiply(a, transpose(a))


def observed(s):
    return [s[i][i] for i in range(8)] + [s[i][j] for i in range(4) for j in range(4, 8)]


def jacobian(x):
    r, result = len(x[0]), []
    for i in range(8):
        row = [Q(0)] * (8 * r)
        for k in range(r):
            row[i * r + k] = 2 * x[i][k]
        result.append(row)
    for i in range(4):
        for j in range(4, 8):
            row = [Q(0)] * (8 * r)
            for k in range(r):
                row[i * r + k] = x[j][k]
                row[j * r + k] = x[i][k]
            result.append(row)
    return result


# Dominance of the rank-four Gram-statistic map.
u = identity(4)
a = [[Q(int(k in {i, (i + 1) % 4})) for k in range(4)] for i in range(4)]
x4 = u + a
j4 = jacobian(x4)
cols4 = pivot_columns(j4)
minor4 = determinant([[row[c] for c in cols4] for row in j4])
assert len(cols4) == 24 and minor4 != 0

# Genuine vertex-color equality K11=K22 sums the first two diagonal outputs.
j4_tied = [[a + b for a, b in zip(j4[0], j4[1])]] + j4[2:]
cols4_tied = pivot_columns(j4_tied)
minor4_tied = determinant([[row[c] for c in cols4_tied] for row in j4_tied])
assert len(cols4_tied) == 23 and minor4_tied != 0

# Weak threshold witness and exact rank-three intersection witness.
x2 = [[Q(1), Q(0)]] * 4 + [[Q(0), Q(1)]] * 4
x3_intersection = [[Q(1), Q(0), Q(0)]] * 2 + [[Q(0), Q(0), Q(1)]] * 2 + [[Q(0), Q(1), Q(0)]] * 4
assert observed(gram(x2)) == observed(identity(8)) == observed(gram(x3_intersection))
assert len(pivot_columns(x2)) == 2 and len(pivot_columns(x3_intersection)) == 3

# A concrete version of the BS lower-bound mechanism for three observations.
# V is 4-by-3 and W=HV, H a rational Householder orthogonal matrix.
v = identity(3) + [[Q(1), Q(1), Q(1)]]
hvector = list(map(Q, [1, 2, 3, 4]))
h = [[Q(int(i == j)) - 2 * hvector[i] * hvector[j] / 30 for j in range(4)] for i in range(4)]
assert gram(h) == identity(4)
w = multiply(h, v)
assert multiply(transpose(v), v) == multiply(transpose(w), w)
pairs3 = list((i, j) for i in range(3) for j in range(i, 3))
c = [[p[i] * p[j] for p in v] + [-p[i] * p[j] for p in w] for i, j in pairs3]
assert all(sum(row) == 0 for row in c)
cols3 = tuple(range(6))
minor3 = determinant([[row[j] for j in cols3] for row in c])
assert minor3 == Q(1148, 3375)
assert len(pivot_columns(v)) == 3

# The explicit rank-four sparse positive semidefinite obstruction is
# M = [[I,-H^t],[-H,I]] = [I;-H][I,-H^t].
m = [identity(4)[i] + [-h[j][i] for j in range(4)] for i in range(4)]
m += [[-h[i][j] for j in range(4)] + identity(4)[i] for i in range(4)]
assert multiply(m, v + w) == [[Q(0)] * 3 for _ in range(8)]
assert len(pivot_columns(m)) == 4

epsilon = Q(1, 100)
diagonal_lower = (1 - epsilon) ** 2
cross_upper = 2 * epsilon * (1 + epsilon)
margin = diagonal_lower - 4 * cross_upper
assert margin == Q(8993, 10000) and margin > 0

def strings(a):
    return [[str(x) for x in r] for r in a]


result = {
    "arithmetic": "fractions.Fraction; deterministic exact rational elimination",
    "rank4_dominance": {"jacobian_shape": [24, 32], "minor_columns_zero_based": cols4, "minor_determinant": str(minor4)},
    "rank4_tied_dominance": {"jacobian_shape": [23, 32], "minor_columns_zero_based": cols4_tied, "minor_determinant": str(minor4_tied)},
    "weak_witness": {"rank": 2, "statistics_equal_identity": True, "open_box_epsilon": str(epsilon), "diagonal_dominance_margin": str(margin)},
    "exact_rank3_intersection_witness": {"rank": 3, "statistics_equal_identity": True},
    "mlt_rank3_open_failure": {"V": strings(v), "W": strings(w), "C_shape": [6, 8], "C_times_ones": ["0"] * 6, "minor_columns_zero_based": list(cols3), "minor_determinant": str(minor3), "stress_rank": 4, "stress_times_data_zero": True},
    "classical_numeric_specializations": {"K4,4": {"gcr": 4, "wmlt": 2, "mlt": min(next(k for k in range(1, 9) if k*(k+1)//2 >= 8), 5)}, "K3,4": {"gcr": 4, "wmlt": 2, "mlt": min(next(k for k in range(1, 8) if k*(k+1)//2 >= 7), 4)}}
}
print(json.dumps(result, indent=2, sort_keys=True))
