#!/usr/bin/env python3
"""Exact finite checks only; no global polygon-connectivity certification."""
from fractions import Fraction as F
import json
import sys


class CheckFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise CheckFailure(message)


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def mul(a, s):
    return tuple(x*s for x in a)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


ZERO = (F(0), F(0), F(0))


def intersection(p, q, r, s):
    """Return None, ('point', coordinate), or ('overlap',) for exact segments."""
    u, v, w = sub(q, p), sub(s, r), sub(r, p)
    require(dot(u, u) > 0 and dot(v, v) > 0, 'zero-length segment')
    for i, j in ((0, 1), (0, 2), (1, 2)):
        d = u[j]*v[i]-u[i]*v[j]
        if d:
            a = (w[j]*v[i]-w[i]*v[j])/d
            b = (u[i]*w[j]-u[j]*w[i])/d
            x, y = add(p, mul(u, a)), add(r, mul(v, b))
            if 0 <= a <= 1 and 0 <= b <= 1 and x == y:
                return ('point', x)
            return None
    if cross(w, u) != ZERO:
        return None
    k = next(i for i in range(3) if u[i])
    a, b = w[k]/u[k], (s[k]-p[k])/u[k]
    low, high = max(F(0), min(a, b)), min(F(1), max(a, b))
    if low > high:
        return None
    if low == high:
        return ('point', add(p, mul(u, low)))
    return ('overlap',)


def simple(vertices):
    n = len(vertices)
    require(n >= 3, 'not a closed polygon')
    require(all(dot(sub(vertices[(i+1) % n], vertices[i]),
                    sub(vertices[(i+1) % n], vertices[i])) > 0
                for i in range(n)), 'zero edge')
    for i in range(n):
        for j in range(i+1, n):
            got = intersection(vertices[i], vertices[(i+1) % n],
                               vertices[j], vertices[(j+1) % n])
            expected = (('point', vertices[j]) if j == i+1 else
                        ('point', vertices[0]) if (i, j) == (0, n-1) else None)
            require(got == expected, f'illegal edge intersection {i},{j}: {got}')


def length_squares(vertices):
    return [dot(sub(vertices[(i+1) % len(vertices)], vertices[i]),
                sub(vertices[(i+1) % len(vertices)], vertices[i]))
            for i in range(len(vertices))]


def rationalize(vertices):
    return [tuple(F(x) for x in v) for v in vertices]


def unit_polygon(vertices):
    simple(vertices)
    require(all(q == 1 for q in length_squares(vertices)), 'not unit-edge')


def flatten(vertices, a):
    return [(x, y, a*z) for x, y, z in vertices]


def check_examples():
    subdivision = []
    for r in map(F, ('0', '1/10', '1/4', '1/2')):
        c, s = (1-r*r)/(1+r*r), 2*r/(1+r*r)
        require(c*c+s*s == 1 and c >= F(3, 5), 'circle identity or bound')
        p = rationalize([(0, 0, 0), (c, 0, s), (2*c, 0, 0),
                         (2*c, 1, 0), (c, 1, -s), (0, 1, 0)])
        unit_polygon(p)
        require(dot(sub(p[2], p[0]), sub(p[2], p[0])) == 4*c*c,
                'coarse chord formula')
        subdivision.append({'r': str(r), 'coarse_chord_length': str(2*c)})
    require(subdivision[-1]['coarse_chord_length'] == '6/5', 'endpoint chord')

    square = rationalize([(0, 0, 0), (F(3, 5), 0, F(4, 5)),
                          (F(3, 5), F(3, 5), 0), (0, F(3, 5), F(4, 5))])
    unit_polygon(square)
    flattening = []
    for a in map(F, ('0', '1/4', '1/2', '3/4', '1')):
        p = flatten(square, a)
        simple(p)
        expected = F(9, 25)+F(16, 25)*a*a
        require(expected > 0 and all(q == expected for q in length_squares(p)),
                'constant-height length identity')
        flattening.append({'vertical_scale': str(a), 'common_length_squared': str(expected)})

    rows = rationalize([(F(2, 3), F(2, 3), F(1, 3)),
                        (F(-2, 3), F(1, 3), F(2, 3)),
                        (F(1, 3), F(-2, 3), F(2, 3))])
    require(all(dot(rows[i], rows[j]) == (1 if i == j else 0)
                for i in range(3) for j in range(3)), 'matrix not orthogonal')
    require(cross(rows[0], rows[1]) == rows[2], 'matrix orientation')
    cube = rationalize([(0, 0, 0), (1, 0, 0), (1, 1, 0),
                        (1, 1, 1), (0, 1, 1), (0, 0, 1)])
    p = [tuple(dot(row, v) for row in rows) for v in cube]
    unit_polygon(p)
    proj = flatten(p, F(0))
    simple(proj)
    left_tests = 0
    for i in range(6):
        e = sub(proj[(i+1) % 6], proj[i])
        for j in range(6):
            if j not in (i, (i+1) % 6):
                require(cross(e, sub(proj[j], proj[i]))[2] > 0,
                        'projection not strictly convex')
                left_tests += 1
    hs = [sub(p[(i+1) % 6], p[i])[2] for i in range(6)]
    require(hs == list(map(F, ('1/3', '-2/3', '2/3', '-1/3', '2/3', '-2/3'))),
            'unexpected vertical increments')
    lens = length_squares(flatten(p, F(1, 2)))
    require(set(lens) == {F(11, 12), F(2, 3)}, 'flattening obstruction lost')

    bad_unit = list(square)
    bad_unit[1] = add(bad_unit[1], (F(1), F(0), F(0)))
    bad_cross = rationalize([(0, 0, 0), (1, 1, 0), (0, 1, 0), (1, 0, 0)])
    bad_backtrack = rationalize([(0, 0, 0), (1, 0, 0), (F(1, 2), 0, 0), (0, 1, 0)])
    rejected = 0
    for fn, v in [(unit_polygon, bad_unit), (simple, bad_cross), (simple, bad_backtrack)]:
        try:
            fn(v)
        except CheckFailure:
            rejected += 1
        else:
            raise CheckFailure('deliberately invalid fixture accepted')

    return {'result': 'PASS', 'scope': 'finite rational example checks only',
            'global_conjecture_solved': False, 'component_decomposition_executed': False,
            'subdivision_samples': subdivision, 'uniform_flattening_samples': flattening,
            'mixed_height_flattened_length_squares': [str(x) for x in lens],
            'strict_convex_projection_halfplane_checks': left_tests,
            'invalid_fixtures_rejected': rejected}


def main():
    try:
        require(len(sys.argv) == 1, 'this checker accepts no arguments')
        result = check_examples()
    except Exception as exc:
        print(json.dumps({'result': 'FAIL', 'error': str(exc)}, sort_keys=True), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
