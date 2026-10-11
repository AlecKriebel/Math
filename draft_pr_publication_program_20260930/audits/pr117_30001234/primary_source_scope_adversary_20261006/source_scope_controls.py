#!/usr/bin/env python3
"""Exact, optimization-resistant scope controls; no third-party source is required.

This checks the selected example and distinctions in the written source report.
Finite rational samples supplement, rather than prove, its complete-face argument.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
import sys

checks = 0


def require(condition, message):
    global checks
    checks += 1
    if not condition:
        raise ValueError(message)


if "--force-failure" in sys.argv:
    require(False, "Deliberate false guard for optimization-resistance control")


def image(matrix, z):
    return tuple(sum(Q(a) * b for a, b in zip(row, z)) for row in matrix)


def rank(matrix):
    rows = [list(map(Q, row)) for row in matrix]
    pivot = 0
    for col in range(len(rows[0])):
        p = next((i for i in range(pivot, len(rows)) if rows[i][col]), None)
        if p is None:
            continue
        rows[pivot], rows[p] = rows[p], rows[pivot]
        div = rows[pivot][col]
        rows[pivot] = [x / div for x in rows[pivot]]
        for i in range(len(rows)):
            if i != pivot:
                fac = rows[i][col]
                rows[i] = [x - fac * y for x, y in zip(rows[i], rows[pivot])]
        pivot += 1
    return pivot


# Independently transcribed f1=x1*y2-x2*y1, f2=x2*y3-x3*y2,
# f3=x3*y1-x1*y3, with order x1,x2,x3,y1,y2,y3.
positive = [(1, 0, 0, 0, 1, 0), (0, 1, 0, 0, 0, 1), (0, 0, 1, 1, 0, 0)]
negative = [(0, 1, 0, 1, 0, 0), (0, 0, 1, 0, 1, 0), (1, 0, 0, 0, 0, 1)]
columns = positive + negative
A = [tuple(col[j] for col in columns) for j in range(6)]
A += [tuple(int(j % 3 == i) for j in range(6)) for i in range(3)]
expected = [(1, 0, 0, 0, 0, 1), (0, 1, 0, 1, 0, 0),
            (0, 0, 1, 0, 1, 0), (0, 0, 1, 1, 0, 0),
            (1, 0, 0, 0, 1, 0), (0, 1, 0, 0, 0, 1),
            (1, 0, 0, 1, 0, 0), (0, 1, 0, 0, 1, 0),
            (0, 0, 1, 0, 0, 1)]
require(A == expected, "Matrix does not retain exact augmented source rows")
require(len(A) == 9 and all(len(row) == 6 for row in A), "Wrong dimensions")
require(rank(A) == 5, "Wrong augmented rank")
v = tuple(map(Q, (1, 1, 1, -1, -1, -1)))
require(image(A, v) == (0,) * 9, "Wrong kernel direction")
require(len(columns) == len(set(columns)), "Repeated degree-two monomial")
for col in columns:
    require(sum(col) == 2, "Generator term degree is not two")
    require(all(x in (0, 1) for x in col), "Generator term is not squarefree")
    require(any(col), "Source forbids the zero exponent vector")
for p, n in zip(positive, negative):
    require(all(min(x, y) == 0 for x, y in zip(p, n)), "Unexpected common factor")


def z(t):
    return (t,) * 3 + (1 - t,) * 3


parameters = sorted({Q(i, j) for j in range(1, 17) for i in range(j + 1)})
for t in parameters:
    point = z(t)
    alternate = z(Q(0) if t else Q(1))
    require(all(x >= 0 for x in point), "Wrong nonnegative domain")
    require(image(A, point) == (1,) * 9, "Whole augmented image not constant")
    require(sum(point) == 3, "Wrong source objective")
    require(point != alternate, "No distinct rational alternate optimizer")
    require(image(A, alternate) == image(A, point), "Alternate is not in fiber")
    require(not all(x < 1 for x in image(A, point)), "Strict-LP confusion")
    require(sum(point) == sum(image(A, point)[6:]), "Objective not image determined")
    # LaClair LP(8) includes U={1,2,3}: total weight <= |U|-1=2.
    require(sum(point) > 2, "Modified-LaClair LP confused with original")

# With nu_i=1-mu_i, the three cyclic top rows become mu1<=mu3,
# mu2<=mu1, mu3<=mu2. On this bounded finite grid test the equivalence.
grid = [Q(i, 4) for i in range(5)]
for a in grid:
    for b in grid:
        for c in grid:
            point = (a, b, c, 1 - a, 1 - b, 1 - c)
            feasible = all(x <= 1 for x in image(A, point))
            require(feasible == (a == b == c), "Cyclic inequality direction error")


def singleton_fiber_exists(points, matrix):
    return any(all(p == q or image(matrix, p) != image(matrix, q)
                   for q in points) for p in points)


# Three conditions are different. These are finite logical controls, not claims
# that finite sets are LP faces.
two = [(Q(0), Q(0)), (Q(1), Q(0))]
require(singleton_fiber_exists(two, [(1, 0)]), "Confused point and image uniqueness")
require(len(two) != 1, "Unique-optimizer control broken")
require(len({image([(1, 0)], p) for p in two}) != 1, "Unique-image control broken")
require(not singleton_fiber_exists(two, [(0, 1)]), "Constant-image fiber control broken")
require(len({image([(0, 1)], p) for p in two}) == 1, "Constant image is not unique")
require(singleton_fiber_exists([two[0]], [(0, 1)]), "Singleton face control broken")

# Check the polynomial syzygy x3*f1+x1*f2+x2*f3=0. It makes a
# generator redundant after inverting x2, not in the source polynomial ring.
def monomial_times(exponent, coordinate):
    out = list(exponent)
    out[coordinate] += 1
    return tuple(out)


relation = {}
for p, n, coord in zip(positive, negative, (2, 0, 1)):
    for exponent, coefficient in [(p, 1), (n, -1)]:
        exponent = monomial_times(exponent, coord)
        relation[exponent] = relation.get(exponent, 0) + coefficient
require(all(x == 0 for x in relation.values()), "Wrong localized-redundancy syzygy")
require(not any(col == (0,) * 6 for col in columns), "A generator term is a unit")

# Rational points survive every source-required endpoint and orientation.
for p in [z(Q(0)), z(Q(1))]:
    require(sum(p) == 3 and image(A, p) == (1,) * 9, "Endpoint failure")
require(z(Q(0)) != z(Q(1)), "Rational endpoints coincide")

print(json.dumps({"status": "PASS", "checks": checks,
                  "rational_segment_parameters": len(parameters),
                  "cyclic_grid_controls": len(grid) ** 3,
                  "rank": 5, "optimal_value": "3",
                  "scope": "supplement to written primary-source reasoning",
                  "novelty_clearance": False, "publication_clearance": False},
                 indent=2))
