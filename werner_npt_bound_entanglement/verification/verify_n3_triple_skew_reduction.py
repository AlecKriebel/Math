#!/usr/bin/env python3
"""Exact checks for agent_n3_triple_skew_reduction.md.

Only Python's standard library and rational arithmetic are used.  Square
roots are cleared throughout by using E_p=sqrt(2) A_p.
"""

from fractions import Fraction as F
from itertools import product


def zero(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zero(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def matvec(a, x):
    return [
        sum((a[i][j] * x[j] for j in range(len(x))), F(0))
        for i in range(len(a))
    ]


def kron(a, b):
    return [
        [
            a[i // len(b)][j // len(b[0])]
            * b[i % len(b)][j % len(b[0])]
            for j in range(len(a[0]) * len(b[0]))
        ]
        for i in range(len(a) * len(b))
    ]


def add(a, b, scale=F(1)):
    return [
        [a[i][j] + scale * b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def scale(c, a):
    return [[c * value for value in row] for row in a]


def hs2(a):
    return sum((value * value for row in a for value in row), F(0))


# Integer skew basis E_p=sqrt(2) A_p.
E = [
    [[0, 0, 0], [0, 0, 1], [0, -1, 0]],
    [[0, 0, -1], [0, 0, 0], [1, 0, 0]],
    [[0, 1, 0], [-1, 0, 0], [0, 0, 0]],
]
E = [[[F(x) for x in row] for row in matrix] for matrix in E]
I3 = eye(3)


# Check 2 A_p^dagger A_s = delta_ps I-|s><p| after clearing roots:
# E_p^T E_s = delta_ps I-|s><p|.
for p, s in product(range(3), repeat=2):
    lhs = matmul(transpose(E[p]), E[s])
    rhs = scale(F(int(p == s)), I3)
    rhs[s][p] -= 1
    assert lhs == rhs


# Check sum A_p tensor A_p=(3P_Phi-F)/2.  After multiplying by two,
# the left side is sum E_p tensor E_p.
pairs = list(product(range(3), repeat=2))
K2 = zero(9, 9)
for p in range(3):
    K2 = add(K2, kron(E[p], E[p]))

rhs = zero(9, 9)
for row, (a, b) in enumerate(pairs):
    for col, (c, d) in enumerate(pairs):
        # 3P_Phi has entry one exactly at |aa><cc|.
        rhs[row][col] += F(int(a == b and c == d))
        # Flip has |a,b><b,a|.
        rhs[row][col] -= F(int(a == d and b == c))
assert K2 == rhs


# Exact eigen-decomposition of K=sum A_p tensor A_p=K2/2:
# eigenvalue 1 on Phi, -1/2 on symmetric Phi-perp, +1/2 on skew.
phi = [F(int(a == b)) for a, b in pairs]
skew01 = [F(int((a, b) == (0, 1)) - int((a, b) == (1, 0)))
          for a, b in pairs]
sym01 = [F(int((a, b) == (0, 1)) + int((a, b) == (1, 0)))
         for a, b in pairs]
assert matvec(K2, phi) == [2 * x for x in phi]
assert matvec(K2, skew01) == skew01
assert matvec(K2, sym01) == [-x for x in sym01]
assert hs2(K2) == F(12)  # ||K||_2^2=12/4=3.


# Equality tensor D=(1/sqrt(3)) K tensor A_0.
# Its Hilbert--Schmidt norm squared is (1/3)*3*1=1.
# Its operator norm squared is (1/3)*1*(1/2)=1/6.
assert F(1, 3) * F(3) * F(1) == F(1)
assert F(1, 3) * F(1) * F(1, 2) == F(1, 6)


# Cross-marginal equality for
# t=Phi_AB tensor |0>, x=Phi_AB tensor |2>.
a = [F(1, 3), F(1, 3), F(0)]
b = [F(1), F(0), F(0)]
c = F(0)
assert sum(b, F(0)) == F(1, 3) + sum(a, F(0)) + c


# The double-skew normalized equality matrix B=K/sqrt(3) has squared
# singular values 1/3 and 1/12 eight times.
squares = [F(1, 3)] + [F(1, 12)] * 8
assert sum(squares, F(0)) == F(1)
assert sum(squares[:2], F(0)) == F(5, 12)
assert F(1, 3) - F(5, 12) == F(-1, 12)


# Arithmetic of the surviving concurrence implication.
assert F(8, 9) * 2 * F(1, 6) == F(8, 27)
assert F(8, 27) > F(2, 9)

print("triple-skew reduction checks: exact")
