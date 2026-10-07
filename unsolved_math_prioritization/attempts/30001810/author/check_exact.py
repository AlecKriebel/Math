#!/usr/bin/env python3
"""Finite exact-arithmetic checks for the authored partial-results report.

These tests check explicit examples and finite shuffle instances, not the
unresolved general comparison or the infinite-dimensional duality theorem.
No network, external datasets, floating point, or symbolic package is used.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json


def determinant(rows):
    a = [[F(x) for x in row] for row in rows]
    answer = F(1)
    for i in range(len(a)):
        pivot = next((j for j in range(i, len(a)) if a[j][i]), None)
        if pivot is None:
            return F(0)
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            answer = -answer
        v = a[i][i]
        answer *= v
        for j in range(i + 1, len(a)):
            factor = a[j][i] / v
            for k in range(i, len(a)):
                a[j][k] -= factor * a[i][k]
    return answer


def shuffles(a, b):
    p, q = len(a) - 1, len(b) - 1
    for horizontal in combinations(range(p + q), p):
        h = set(horizontal)
        inversions = sum(k - index for index, k in enumerate(horizontal))
        sign = (-1) ** inversions
        i = j = 0
        vertices = [(a[0], b[0])]
        for k in range(p + q):
            if k in h:
                i += 1
            else:
                j += 1
            vertices.append((a[i], b[j]))
        yield sign, tuple(vertices)


def cleaned(c):
    return {k: v for k, v in c.items() if v}


pair_count = simplex_count = 0
for p in range(6):
    for q in range(6):
        a, b = list(range(p + 1)), list(range(q + 1))
        terms = list(shuffles(a, b))
        assert len(terms) == comb(p + q, p)
        left, right = Counter(), Counter()
        for sign, vertices in terms:
            coords = [tuple([int(i == k) for k in range(1, p + 1)] +
                            [int(j == k) for k in range(1, q + 1)])
                      for i, j in vertices]
            rows = [[coords[col + 1][row] - coords[0][row]
                     for col in range(p + q)] for row in range(p + q)]
            assert determinant(rows) == sign
            simplex_count += 1
            if p + q:
                for k in range(len(vertices)):
                    face = vertices[:k] + vertices[k + 1:]
                    left[face] += sign * (-1) ** k
        if p:
            for i in range(p + 1):
                for sign, vertices in shuffles(a[:i] + a[i + 1:], b):
                    right[vertices] += (-1) ** i * sign
        if q:
            for j in range(q + 1):
                for sign, vertices in shuffles(a, b[:j] + b[j + 1:]):
                    right[vertices] += (-1) ** (p + j) * sign
        assert cleaned(left) == cleaned(right)
        pair_count += 1

# Triangle D: -2 <= x <= 1 and (x+2)/3 <= y <= x+2.
def interior(x, y):
    return F(-2) < x < F(1) and (x + 2) / 3 < y < x + 2


def on_boundary(x, y):
    in_closed = F(-2) <= x <= F(1) and (x + 2) / 3 <= y <= x + 2
    return in_closed and not interior(x, y)


vertices = [(-2, 0), (1, 1), (1, 3)]
edge_y_velocities = [vertices[(i + 1) % 3][1] - vertices[i][1] for i in range(3)]
assert all(v != 0 for v in edge_y_velocities)
fold_tests = []
for y, expected in [(F(3, 5), -1), (F(2), 1)]:
    preimages = []
    degree = 0
    for x in [F(-1, 2), F(1, 2)]:
        assert x * x == F(1, 4)
        assert not on_boundary(x, y)
        if interior(x, y):
            jac = 2 * x
            sign = 1 if jac > 0 else -1
            preimages.append({'x': str(x), 'y': str(y), 'jacobian': str(jac)})
            degree += sign
    assert degree == expected and len(preimages) == 1
    fold_tests.append({'target': ['1/4', str(y)], 'preimages': preimages, 'degree': degree})

print(json.dumps({
    'status': 'PASS',
    'arithmetic': 'exact rational arithmetic, Python standard library',
    'shuffle_dimension_pairs': pair_count,
    'shuffle_dimensions': '0 <= p,q <= 5',
    'shuffle_simplices_checked': simplex_count,
    'shuffle_checks': ['binomial term count', 'determinant equals orientation sign',
                       'full signed boundary identity'],
    'fold_edge_y_velocities': edge_y_velocities,
    'fold_degree_checks': fold_tests,
    'not_certified_by_computation': ['general equality', 'general duality proof',
                                    'smooth triangulation existence',
                                    'all dimensions of shuffle identity']
}, indent=2, sort_keys=True))
