#!/usr/bin/env python3
"""Exact finite controls for the scoped claims; not an infinite proof checker."""
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import sys

COUNTS = {}


def check(group, assertion):
    COUNTS[group] = COUNTS.get(group, 0) + 1
    if not assertion:
        raise AssertionError((group, COUNTS[group]))


def star_distance(x, y):
    arm, height = x
    arm2, height2 = y
    return abs(height-height2) if arm == arm2 else height+height2


def star_checks():
    for arms in range(1, 6):
        points = [(0, 0)] + [(i, j) for i in range(arms) for j in range(1, 4)]
        for perm in itertools.permutations(range(arms)):
            action = lambda x: (perm[x[0]], x[1]) if x[1] else (0, 0)
            for x, y in itertools.product(points, repeat=2):
                check('finite_star_isometries', star_distance(action(x), action(y)) == star_distance(x, y))


INV = {'a': 'A', 'A': 'a', 'b': 'B', 'B': 'b'}


def reduce_word(word):
    stack = []
    for c in word:
        if stack and stack[-1] == INV[c]:
            stack.pop()
        else:
            stack.append(c)
    return ''.join(stack)


def common_prefix(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return min(len(a), len(b))


def tree_distance(a, b):
    return len(a)+len(b)-2*common_prefix(a, b)


def q(x, y):
    a, n = x
    b, m = y
    return n+m-2*min(n, m, common_prefix(a, b))


def D(x, y):
    return q(x, y)+(x != y)


def four_sums(points, metric):
    a, b, c, d = points
    return sorted((metric(a, b)+metric(c, d), metric(a, c)+metric(b, d), metric(a, d)+metric(b, c)))


def word_checks():
    words = sorted(set(reduce_word(''.join(w)) for w in itertools.product('aAbB', repeat=3)))
    words = [w for w in words if w]
    # Long reduced prefixes of explicitly eventually constant infinite words.
    rays = [w+next(c for c in 'aAbB' if c != INV[w[-1]])*30 for w in words[:16]]
    points = [(r, h) for r in rays for h in range(5)]
    for x, y in itertools.product(points, repeat=2):
        check('tree_pullback_identity', q(x, y) == tree_distance(x[0][:x[1]], y[0][:y[1]]))
        check('decorated_tree_metric_comparison', 0 <= D(x, y)-q(x, y) <= 1)
    for i in range(2000):
        x, y, z = (points[(i*mul+offset) % len(points)] for mul, offset in ((7, 1), (13, 2), (19, 3)))
        check('decorated_tree_triangle', D(x, z) <= D(x, y)+D(y, z))
        four = [points[(i*mul+offset) % len(points)] for mul, offset in ((7, 1), (13, 2), (19, 3), (23, 4))]
        sums = four_sums(four, D)
        check('decorated_tree_four_point', sums[-1]-sums[-2] <= 2)
    for g in words:
        for x, y in itertools.product(points[::9], repeat=2):
            gx = (reduce_word(g+x[0]), x[1])
            gy = (reduce_word(g+y[0]), y[1])
            check('fixed_element_rough_isometry', abs(D(gx, gy)-D(x, y)) <= 2*len(g))
    samples = []
    for n in range(1, 129):
        x = ('a'*n+'b'*(n+1), n)
        y = ('a'*n+'B'*(n+1), n)
        gx = (reduce_word('A'*n+x[0]), n)
        gy = (reduce_word('A'*n+y[0]), n)
        check('fixed_height_obstruction', D(x, y) == 1 and D(gx, gy) == 2*n+1)
        if n in (1, 2, 8, 32, 128):
            samples.append({'n': n, 'input_distance': D(x, y), 'output_distance': D(gx, gy)})
    return samples


def mul(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)


def canonical(A):
    return A if next(x for x in A if x) > 0 else tuple(-x for x in A)


def mobius(A, z):
    a, b, c, d = A
    x, y = z
    den = (c*x+d)**2+c*c*y*y
    return (((a*x+b)*(c*x+d)+a*c*y*y)/den, y/den)


def cosh_distance(z, w):
    x, y = z
    u, v = w
    return 1+((x-u)**2+(y-v)**2)/(2*y*v)


def modular_checks():
    S, T, Ti = (0, -1, 1, 0), (1, 1, 0, 1), (1, -1, 0, 1)
    matrices = {(1, 0, 0, 1)}
    for _ in range(5):
        matrices |= {canonical(mul(A, B)) for A in matrices for B in (S, T, Ti)}
    zs = [(F(x, 2), F(y, 3)) for x, y in ((0, 3), (1, 2), (-3, 5), (4, 1))]
    for A in sorted(matrices):
        a, b, c, d = A
        check('modular_determinants', a*d-b*c == 1)
        norm_u2, norm_v2 = a*a+c*c, b*b+d*d
        check('modular_column_angle_identity', F((a*d-b*c)**2, norm_u2*norm_v2) == F(1, norm_u2*norm_v2))
        check('modular_column_angle_bound', F(1, norm_u2*norm_v2) <= F(1, norm_v2))
        for z, w in itertools.product(zs, repeat=2):
            gz, gw = mobius(A, z), mobius(A, w)
            check('upper_half_plane_preserved', gz[1] > 0 and gw[1] > 0)
            check('hyperbolic_plane_isometry', cosh_distance(gz, gw) == cosh_distance(z, w))
    samples = []
    for n in range(2, 129):
        A = (n, n*n-1, 1, n)
        a, b, c, d = A
        Nu, Nv = a*a+c*c, b*b+d*d
        check('rank_one_limit_control', a*d-b*c == 1 and max(abs(a), abs(c)) < max(abs(b), abs(d)))
        check('rank_one_angle_control', F(1, Nu*Nv) <= F(1, Nv) <= F(1, n*n))
        if n in (2, 8, 32, 128):
            samples.append({'n': n, 'column_norm_squares': [Nu, Nv], 'sine_angle_squared': str(F(1, Nu*Nv))})
    return len(matrices), samples


def combinatorial_checks():
    for a, b, p, t in itertools.permutations(range(4)):
        xp = list(itertools.combinations((a, b, p), 2))
        yp = list(itertools.combinations((a, t, p), 2))
        survivors = {(frozenset(i), frozenset(j)) for i, j in itertools.product(xp, yp) if not set(i) & set(j)}
        expected = {(frozenset((a, b)), frozenset((t, p))), (frozenset((b, p)), frozenset((a, t)))}
        check('nine_crossratio_reduction', survivors == expected)
    # The metric-annulus nesting construction uses s_j=4^(-j), r_j=2s_j.
    for j in range(1, 129):
        s, r, delta = F(1, 4**j), F(2, 4**j), F(3, 2*4**j)
        next_r = F(2, 4**(j+1))
        check('all_annuli_nesting_arithmetic', 0 < s < delta < r and next_r < s)


def aggregation_checks():
    rho1 = lambda x, y: abs(x[0]-y[0])
    rho2 = lambda x, y: abs(x[1]-y[1])
    l1 = lambda x, y: rho1(x, y)+rho2(x, y)
    linf = lambda x, y: max(rho1(x, y), rho2(x, y))
    samples = []
    for n in range(1, 129):
        square = ((0, 0), (n, n), (0, n), (n, 0))
        diamond = ((n, 0), (-n, 0), (0, n), (0, -n))
        for points in (square, diamond):
            for rho in (rho1, rho2):
                ss = four_sums(points, rho)
                check('coordinate_zero_hyperbolicity', ss[-1] == ss[-2])
        s1, si = four_sums(square, l1), four_sums(diamond, linf)
        check('sum_nonhyperbolicity_witness', s1 == [2*n, 2*n, 4*n])
        check('max_nonhyperbolicity_witness', si == [2*n, 2*n, 4*n])
        if n in (1, 2, 8, 32, 128):
            samples.append({'n': n, 'sum_metric_four_point_sums': s1, 'max_metric_four_point_sums': si})
    return samples


def main():
    star_checks()
    word_samples = word_checks()
    matrix_count, matrix_samples = modular_checks()
    combinatorial_checks()
    grid_samples = aggregation_checks()
    result = {
        'problem_id': 6200007,
        'status': 'PASS',
        'arithmetic': 'integers_and_exact_rationals_only',
        'assertions': dict(sorted(COUNTS.items())),
        'total_assertions': sum(COUNTS.values()),
        'modular_matrices_tested': matrix_count,
        'fixed_height_samples': word_samples,
        'matrix_angle_samples': matrix_samples,
        'aggregation_samples': grid_samples,
        'limits': [
            'Finite controls do not prove compactness, conicality, or boundary correspondence.',
            'The explicit all-n formulas, not their tested ranges, prove the two unbounded failures.',
            'The original universal realization question remains unresolved.'
        ]
    }
    out = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if '--write' in sys.argv:
        Path(__file__).with_name('CHECKS.json').write_text(out)
    print(out, end='')


if __name__ == '__main__':
    main()
