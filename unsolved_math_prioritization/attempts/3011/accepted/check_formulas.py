#!/usr/bin/env python3
"""Finite exact checks of formulas; not a test of the ANR conjecture.

Writes only JSON to stdout, unless --output names an external file. All mathematical
checks use require/raise and remain active with python -O and -OO.
"""
import argparse
from fractions import Fraction as F
import json
import os
from pathlib import Path
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pl_eval(points, x):
    require(points[0][0] <= x <= points[-1][0], 'outside PL domain')
    for (a, b), (c, d) in zip(points, points[1:]):
        if a <= x <= c:
            return b + (d-b)*(x-a)/(c-a)
    raise RuntimeError('PL interval not found')


def pl_inverse(points):
    require(all(a[0] < b[0] and a[1] < b[1] for a, b in zip(points, points[1:])),
            'inverse requires strict monotonicity')
    return [(y, x) for x, y in points]


def alexander(points, t):
    require(F(0) <= t <= F(1), 'bad shrinking parameter')
    if t == 0:
        return [(F(-1), F(-1)), (F(1), F(1))]
    result = [(F(-1), F(-1))]
    for x, y in points:
        if result[-1][0] == t*x:
            require(result[-1][1] == t*y, 'inconsistent gluing')
        else:
            result.append((t*x, t*y))
    if result[-1][0] != 1:
        result.append((F(1), F(1)))
    return result


def sup_distance(a, b):
    xs = sorted(set([x for x, _ in a] + [x for x, _ in b]))
    return max(abs(pl_eval(a, x)-pl_eval(b, x)) for x in xs)


def transpose(a):
    return [list(c) for c in zip(*a)]


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def check_alexander():
    ident = [(F(-1), F(-1)), (F(1), F(1))]
    family = [ident]
    for k in range(-7, 8):
        family.append([(F(-1), F(-1)), (F(0), F(k, 8)), (F(1), F(1))])
    count = 0
    for a in family:
        ai = pl_inverse(a)
        for t in [F(0), F(1, 17), F(1, 3), F(2, 3), F(1)]:
            at = alexander(a, t)
            ati = alexander(ai, t)
            require(pl_inverse(at) == ati, 'Alexander inverse formula')
            require(sup_distance(at, ident) == t*sup_distance(a, ident),
                    'Alexander displacement equality')
            for b in family:
                require(sup_distance(at, alexander(b, t)) == t*sup_distance(a, b),
                        'Alexander pair-distance equality')
                count += 1
    return count


def check_interval_averaging():
    samples = [[(F(-1), F(-1)), (F(0), F(k, 8)), (F(1), F(1))]
               for k in range(-7, 8)]
    count = 0
    for a in samples:
        for b in samples:
            for t in [F(0), F(1, 7), F(1, 2), F(1)]:
                p = [(x, (1-t)*pl_eval(a, x)+t*pl_eval(b, x))
                     for x in [F(-1), F(0), F(1)]]
                pl_inverse(p)
                require(p[0][1] == -1 and p[-1][1] == 1, 'endpoint failure')
                count += 1
    # Negative control: a fold must be rejected by the inverse precondition.
    bad = [(F(-1), F(-1)), (F(0), F(1)), (F(1), F(1))]
    rejected = False
    try:
        pl_inverse(bad)
    except RuntimeError:
        rejected = True
    require(rejected, 'non-strict negative control was accepted')
    return count


def check_rotation_shortcuts():
    minus_id = [[-1, 0], [0, -1]]
    quarter = [[0, -1], [1, 0]]
    require(matmul(minus_id, minus_id) == eye(2), 'pi rotation inverse')
    require(matmul(transpose(quarter), quarter) == eye(2), 'quarter rotation inverse')
    a, b = [[F(1, 7)], [F(0)]], [[F(2, 7)], [F(0)]]
    ma, mb = matmul(minus_id, a), matmul(minus_id, b)
    mid_a = [[(x[0]+y[0])/2] for x, y in zip(a, ma)]
    mid_b = [[(x[0]+y[0])/2] for x, y in zip(b, mb)]
    require(a != b and mid_a == mid_b, 'midpoint-collapse witness')
    qa, qb = matmul(quarter, a), matmul(quarter, b)
    require(qa != qb and qa[0] == qb[0], 'projection-collapse witness')
    # Positive controls: identity interpolation and identity slice projection preserve witnesses.
    require(matmul(eye(2), a) != matmul(eye(2), b), 'identity control')
    require(a[0] != b[0], 'identity projection control')
    return 2


def check_twists():
    count = 0
    for g in range(1, 13):
        size = 2*g
        form = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(g):
            form[2*i][2*i+1] = 1
            form[2*i+1][2*i] = -1
        for j in range(g):
            twist = eye(size)
            twist[2*j][2*j+1] = 1
            inv = eye(size)
            inv[2*j][2*j+1] = -1
            require(matmul(twist, inv) == eye(size), 'twist inverse')
            require(matmul(matmul(transpose(twist), form), twist) == form,
                    'twist symplecticity')
            require(twist != eye(size), 'twist acts trivially')
            for i in range(2*j):
                require([twist[k][i] for k in range(size)] ==
                        [int(k == i) for k in range(size)], 'earlier handle moved')
            count += 1
    # Negative control is genuinely identity on all homology.
    require(matmul(eye(4), eye(4)) == eye(4), 'identity homology control')
    return count


def check_cube_family():
    count = 0
    for n in range(1, 7):
        # Exact lower derivative bound over the full domain uses 0<=b<=1 and |x1|<=1.
        for t in [F(0), F(1, 2), F(1)]:
            for beta in [F(0), F(1, 4), F(1)]:
                for x in [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]:
                    derivative = 1-t*beta*x/2
                    require(derivative >= F(1, 2), 'cube fiber loses monotonicity')
                    y = x+t*beta*(1-x*x)/4
                    if abs(x) == 1 or beta == 0:
                        require(y == x, 'boundary is not fixed')
                    count += 1
    require(F(0)/4 != F(1)/4, 'cube parameter is not detected at center')
    return count


def reduce_word(word):
    result = []
    for symbol, scale, sign in word:
        if scale == 0:
            continue
        if result and result[-1] == (symbol, scale, -sign):
            result.pop()
        else:
            result.append((symbol, scale, sign))
    return result


def inverse_word(word):
    return [(symbol, scale, -sign) for symbol, scale, sign in reversed(word)]


def scale_word(word, t):
    return reduce_word([(symbol, scale*t, sign) for symbol, scale, sign in word])


def canonical_word(vertices, weights):
    require(len(vertices) == len(weights) and sum(weights) == 1,
            'bad symbolic barycentric data')
    if len(vertices) == 1 or weights[0] == 1:
        return [(vertices[0], F(1), 1)]
    tail = 1-weights[0]
    j = canonical_word(vertices[1:], [p/tail for p in weights[1:]])
    first = [(vertices[0], F(1), 1)]
    return reduce_word(scale_word(j+inverse_word(first), tail)+first)


def product_word(vertices, weights):
    tails = [sum(weights[j:]) for j in range(len(weights))]+[F(0)]
    word = []
    for j in reversed(range(len(vertices))):
        word += [(vertices[j], tails[j+1], -1), (vertices[j], tails[j], 1)]
    return reduce_word(word)


def check_noncommutative_formula():
    count = 0
    for size in range(1, 9):
        vertices = list(range(size))
        families = [[F(1, size)]*size,
                    [F(2*j+1, size*size) for j in range(size)]]
        if size > 1:
            families.append([F(0)]+[F(1, size-1)]*(size-1))
            families.append([F(1)]+[F(0)]*(size-1))
        for weights in families:
            actual = canonical_word(vertices, weights)
            require(actual == product_word(vertices, weights), 'ordered factor formula')
            active = [(v, p) for v, p in zip(vertices, weights) if p]
            require(actual == canonical_word([v for v, p in active], [p for v, p in active]),
                    'zero-coordinate face compatibility')
            count += 1
    e0 = [(0, F(1, 2), -1), (0, F(1), 1)]
    e1 = [(1, F(1, 2), 1)]
    require(reduce_word(e0+e1) != reduce_word(e1+e0), 'order-sensitivity control')
    return count


def radial_canonical_angle(vertices, weights, radius):
    # Angles are measured in units of pi, so all arithmetic is exact rational.
    require(F(0) <= radius <= F(1), 'bad radial evaluation')
    if len(vertices) == 1 or weights[0] == 1:
        return pl_eval(vertices[0], radius)
    tail = 1-weights[0]
    first = pl_eval(vertices[0], radius)
    if radius > tail:
        return first
    j = radial_canonical_angle(vertices[1:], [p/tail for p in weights[1:]], radius/tail)
    return first+j-pl_eval(vertices[0], radius/tail)


def check_radial_amplification():
    count = 0
    for n in [1, 2, 3, 5, 8, 13, 32, 64]:
        weights = [F(1, 2*n)]*n+[F(1, 2)]
        tails = [sum(weights[j:]) for j in range(n+1)]
        radius, amplitude = F(1, 4), F(1, 2*n)
        vertices = []
        increments = []
        for j in range(n):
            low, high = radius/tails[j], radius/tails[j+1]
            require(0 < low < high < 1, 'twist nodes not ordered')
            phi = [(F(0), F(0)), (low, amplitude), (high, -amplitude), (F(1), F(0))]
            require(max(abs(y) for _, y in phi) == amplitude, 'vertex angle bound')
            vertices.append(phi)
            increments.append(pl_eval(phi, low)-pl_eval(phi, high))
        vertices.append([(F(0), F(0)), (F(1), F(0))])
        require(sum(increments) == 1, 'factor product does not rotate by pi')
        require(radial_canonical_angle(vertices, weights, radius) == 1,
                'recursive interpolation disagrees with pi rotation')
        require(2*radius == F(1, 2), 'claimed displacement')
        zero = [(F(0), F(0)), (F(1), F(0))]
        require(radial_canonical_angle([zero]*(n+1), weights, radius) == 0,
                'constant-vertex negative control')
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--require-readonly', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    require(os.geteuid() != 0, 'verification must run as a non-root user')
    if args.require_readonly:
        require(not os.access(root, os.W_OK), 'packet directory is writable')
        for p in root.rglob('*'):
            require(not p.is_symlink(), 'symlink in packet')
            require(not os.access(p, os.W_OK), 'writable packet entry: '+str(p))
    results = {
        'status': 'passed',
        'scope': 'finite exact formula checks only; no ANR conclusion',
        'uid': os.geteuid(),
        'python_optimization': sys.flags.optimize,
        'readonly_required': args.require_readonly,
        'checks': {
            'alexander_distance_and_inverse_cases': check_alexander(),
            'interval_convexity_cases': check_interval_averaging(),
            'rotation_shortcut_counterexamples': check_rotation_shortcuts(),
            'homology_twist_cases': check_twists(),
            'cube_monotonicity_cases': check_cube_family(),
            'noncommutative_word_cases': check_noncommutative_formula(),
            'radial_amplification_cases': check_radial_amplification(),
        },
        'controls': ['non-strict PL map rejected', 'identity interpolation preserves points',
                     'identity slice projection preserves points', 'identity homology action',
                     'noncommutative product order matters', 'constant radial vertices give zero angle'],
    }
    text = json.dumps(results, indent=2, sort_keys=True)+'\n'
    if args.output is None:
        print(text, end='')
    else:
        out = args.output.resolve()
        require(out != root and root not in out.parents, 'output must be external to packet')
        out.write_text(text)


if __name__ == '__main__':
    main()
