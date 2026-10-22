#!/usr/bin/env python3
"""Exact algebraic controls for the P^2 normal-bundle calculation.

Python standard library only. These are checks of matrix identities and boundary
examples, not a computation of global smoothness, ampleness or a Picard group.
Run: python3 check.py
"""
from fractions import Fraction
from itertools import product
import json
import platform


def matrix(rows):
    return tuple(tuple(x for x in row) for row in rows)


def mul(a, b):
    return matrix([[sum(a[i][k] * b[k][j] for k in range(3))
                    for j in range(3)] for i in range(3)])


def sub(a, b):
    return matrix([[a[i][j] - b[i][j] for j in range(3)]
                   for i in range(3)])


def bracket(a, b):
    return sub(mul(a, b), mul(b, a))


def flatten(a):
    return [v for row in a for v in row]


def unit(i, j):
    return matrix([[int((r, c) == (i, j)) for c in range(3)]
                   for r in range(3)])


def rank(cols):
    rows = [[Fraction(x) for x in row] for row in zip(*cols)]
    r = 0
    for c in range(len(cols)):
        p = next((p for p in range(r, len(rows)) if rows[p][c]), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        a = rows[r][c]
        rows[r] = [x/a for x in rows[r]]
        for j in range(len(rows)):
            if j != r:
                a = rows[j][c]
                rows[j] = [x-a*y for x, y in zip(rows[j], rows[r])]
        r += 1
    return r


def B(x, y, z):
    return matrix([[0, 0, 0], [0, x, y], [0, z, -x]])


def wedge(a, b):
    a, b = flatten(a), flatten(b)
    return [a[i]*b[j]-a[j]*b[i] for i in range(9) for j in range(i+1, 9)]


A = matrix([[2, 0, 0], [0, -1, 0], [0, 0, -1]])
zero = matrix([[0]*3 for _ in range(3)])
U = [unit(0, 1), unit(0, 2), unit(1, 0), unit(2, 0)]
W = [B(1, 0, 0), B(0, 1, 0), B(0, 0, 1)]
eigenvalues = [-3, -3, 3, 3]
for D, ev in zip(U, eigenvalues):
    assert bracket(D, A) == matrix([[ev*x for x in row] for row in D])
assert rank([flatten(D) for D in U]) == 4
assert rank([flatten(M) for M in [A]+W+U]) == 8
assert all(bracket(A, b) == zero for b in W)
assert rank([wedge(A, b) for b in W]) == 3

checked = nilpotent = semisimple = 0
for xyz in product(range(-3, 4), repeat=3):
    if xyz == (0, 0, 0):
        continue
    b = B(*xyz)
    assert bracket(A, b) == zero
    assert rank([flatten(A), flatten(b)]) == 2
    # The four infinitesimal-action directions have independent evaluations
    # at A modulo the plane L=<A,B>; this is the proof's key normal test.
    assert rank([flatten(A), flatten(b)] +
                [flatten(bracket(D, A)) for D in U]) == 6
    checked += 1
    if xyz[0]**2 + xyz[1]*xyz[2] == 0:
        nilpotent += 1
        assert mul(b, b) == zero
    else:
        semisimple += 1

# The four symbolic columns of D -> [D,A] are the constant matrix below.
determinant = 1
for v in eigenvalues:
    determinant *= v
assert determinant == 81

# Negative controls: arbitrary conjugation fields cannot all be called normal,
# and this particular proof is not valid in characteristic three.
assert bracket(unit(1, 2), A) == zero
assert all(all(x % 3 == 0 for x in flatten(bracket(D, A))) for D in U)

print(json.dumps({
    "status": "PASS",
    "python": platform.python_version(),
    "arithmetic": "exact integers and fractions; no floating point",
    "ad_A_eigenvalues_on_off_block_space": eigenvalues,
    "ad_A_determinant": determinant,
    "plucker_linear_map_rank": 3,
    "block_direct_sum_dimension": 8,
    "integer_projective_representatives_checked": checked,
    "nilpotent_representatives_checked": nilpotent,
    "semisimple_representatives_checked": semisimple,
    "negative_controls": ["block field has zero A-evaluation",
                          "off-block A-evaluation degenerates in characteristic 3"],
    "limits": ["finite representatives supplement the written all-points proof",
               "does not prove the published smoothness/Fano/Picard results",
               "does not certify source completeness or priority"]
}, indent=2))
