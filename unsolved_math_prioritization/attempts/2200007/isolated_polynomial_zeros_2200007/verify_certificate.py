#!/usr/bin/env python3
"""Exact corroborating checks of the credited, fixed quartic certificate.

No external code or data is imported. This checks one known example; it is not
a new search, a general extremal computation, or a formal proof of real analysis.
"""
import itertools
import json
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ValueError(message)


def radicands(t):
    return [t * (8 - t)] + [(t - i + 1) * (t - i) for i in range(1, 9)]


def calculate():
    # Coordinates are t, x_0, ..., x_8. Expand the nine squares over Z.
    n = 10
    def monomial(index, degree):
        e = [0] * n
        e[index] = degree
        return tuple(e)
    zero = (0,) * n
    qs = [{monomial(1, 2): 1, monomial(0, 2): 1, monomial(0, 1): -8}]
    for i in range(1, 9):
        q = {monomial(i + 1, 2): 1, monomial(0, 2): -1,
             monomial(0, 1): 2 * i - 1}
        if i > 1:
            q[zero] = -i * (i - 1)
        qs.append(q)
    p = {}
    for q in qs:
        require(max(map(sum, q)) == 2, 'summand degree')
        for a, ca in q.items():
            for b, cb in q.items():
                e = tuple(x + y for x, y in zip(a, b))
                p[e] = p.get(e, 0) + ca * cb
    p = {e: c for e, c in p.items() if c}
    require(max(map(sum, p)) == 4, 'SOS degree')
    require(p.get(monomial(1, 4)) == 1, 'leading coefficient')

    # The complete root list of all factored radicands is {0,...,8}.
    # On each complementary open cell every radicand has constant sign,
    # since a continuous polynomial changes sign only through a root.
    roots = set([0, 8])
    for i in range(1, 9):
        roots.update([i - 1, i])
    require(sorted(roots) == list(range(9)), 'root partition')
    representatives = [Fraction(-1)] + [Fraction(2*j + 1, 2) for j in range(8)] + [Fraction(9)]
    cells = []
    for t in representatives:
        r = radicands(t)
        negative = [i for i, v in enumerate(r) if v < 0]
        require(bool(negative), 'unexcluded open sign cell')
        require(all(v != 0 for v in r), 'representative on root')
        cells.append({'representative': str(t), 'negative_radicands': negative})

    slices, points = [], set()
    for t in range(9):
        r = radicands(t)
        require(all(v >= 0 for v in r), 'infeasible integer')
        vanishing = [i for i, v in enumerate(r) if v == 0]
        expected = [0, 1] if t == 0 else ([0, 8] if t == 8 else [t, t + 1])
        require(vanishing == expected, 'vanishing indices')
        positive = [i for i, v in enumerate(r) if v > 0]
        require(len(positive) == 7, 'positive radicand count')
        before = len(points)
        for signs in itertools.product([-1, 1], repeat=7):
            sign_map = dict(zip(positive, signs))
            # Exact coordinate encoding: (sign, radicand) represents
            # sign*sqrt(radicand), with the unique encoding (0,0) for zero.
            point = (t,) + tuple((sign_map.get(i, 0), r[i]) for i in range(9))
            require(point not in points, 'duplicate point')
            points.add(point)
        count = len(points) - before
        require(count == 128, 'slice count')
        slices.append({'t': t, 'radicands': r, 'zero_indices': vanishing, 'points': count})
    require(len(points) == 1152 and len(points) > 2**10, 'strict counterexample')
    return {'problem_id': 2200007, 'prior_creator': 'DannyExperiments',
            'purpose': 'Verification of a fixed prior certificate; no new research approach',
            'k': 2, 'l': 10, 'summands': 9, 'summand_degree': 2,
            'SOS_degree': 4, 'x_0_fourth_power_coefficient': 1,
            'open_sign_cells_excluded': cells, 'slices': slices,
            'distinct_real_zeros': len(points), 'conjectured_maximum': 2**10,
            'strict_excess': len(points)-2**10,
            'finite_real_zero_set': True, 'new_discovery_claim': False}


if __name__ == '__main__':
    print(json.dumps(calculate(), indent=2, sort_keys=True))
