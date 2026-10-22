def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

"""Exact standard-library audit of LOW_RANK.md rational examples."""
from fractions import Fraction as F
from itertools import combinations


def gram(rows):
    return [[sum(a*b for a, b in zip(x, y)) for y in rows] for x in rows]


def full_spark_2(rows):
    return all(a[0]*b[1] != a[1]*b[0] for a, b in combinations(rows, 2))


X = [[0, 1], [2, -1], [2, 1], [1, 1]]
vs = [[1, 0], [1, 2], [1, -2]]
cs = [F(3, 4), F(1, 8), F(1, 8)]
us = [[sum(a*b for a, b in zip(row, v)) for row in X] for v in vs]
Q = gram(X)
require(full_spark_2(X), 'Certificate validation failed at original line 19')
require(Q == [[1, -1, 1, 1], [-1, 5, 3, 1], [1, 3, 5, 3], [1, 1, 3, 2]], 'Certificate validation failed at original line 20')
require(all(sum(c*v[i]*v[j] for c, v in zip(cs, vs)) == int(i == j)
           for i in range(2) for j in range(2)), 'Certificate validation failed at original line 21')
require(all(Q[i][j] == sum(c*w[i]*w[j] for c, w in zip(cs, us))
           for i in range(4) for j in range(4)), 'Certificate validation failed at original line 23')
require(all(sum(x != 0 for x in w) == 3 for w in us), 'Certificate validation failed at original line 25')
all_rays = [[-y, x] for x, y in X]
require(all(sum(x*y for x, y in zip(a, b)) != 0
           for a, b in combinations(all_rays, 2)), 'Certificate validation failed at original line 27')
print('PASS: positive matrix has width 3 and minimum width-3 rank 3.')

ts = [F(1, 2), F(-1, 2), F(3, 4), F(-3, 4)]
B = [[F(1), t] for t in ts]
require(full_spark_2(B), 'Certificate validation failed at original line 33')
require(all(q > 0 for row in gram(B) for q in row), 'Certificate validation failed at original line 34')
require(-1 + F(3, 4) < 0, 'Certificate validation failed at original line 35')
require(all(F(3, 4) - t*t > 0 for t in ts), 'Certificate validation failed at original line 36')
require(sum(t/(1+t*t) for t in ts) == 0, 'Certificate validation failed at original line 37')
require(sum(1/(1+t*t) for t in ts) == F(72, 25) < 3, 'Certificate validation failed at original line 38')
require(sum(t*t/(1+t*t) for t in ts) == F(28, 25), 'Certificate validation failed at original line 39')
print('PASS: negative matrix has width 4 despite normalized absolute spectral radius 72/25 < 3.')
