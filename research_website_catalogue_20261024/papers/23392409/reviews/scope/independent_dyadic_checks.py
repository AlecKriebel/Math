"""Own paper-first dyadic/isqrt interval controls; no supplied code imported.

The written proof supplies continuity, uniqueness and IVT existence. These
integer/rational enclosures certify the particular strict hypotheses and boxes.
No files, network, external modules, native programme or numerical floats.
"""
from fractions import Fraction as F
from math import isqrt
from itertools import combinations
import json

D = 2 ** 160
checks = 0
root_checks = 0


def need(ok, label):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(label)


def I(x):
    return x if isinstance(x, tuple) else (F(x), F(x))


def add(a, b):
    a, b = I(a), I(b)
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    a = I(a)
    return -a[1], -a[0]


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    a, b = I(a), I(b)
    v = [x * y for x in a for y in b]
    return min(v), max(v)


def div(a, b):
    b = I(b)
    need(not (b[0] <= 0 <= b[1]), 'nonzero interval denominator')
    return mul(a, (1 / b[1], 1 / b[0]))


def square(a):
    a = I(a)
    return (F(0) if a[0] <= 0 <= a[1] else min(a[0] ** 2, a[1] ** 2),
            max(a[0] ** 2, a[1] ** 2))


def eighth(a):
    a = I(a)
    need(a[0] >= 0, 'positive eighth power input')
    return a[0] ** 8, a[1] ** 8


def root_point(q):
    global root_checks
    need(q >= 0, 'nonnegative radical argument')
    # Nested integer square roots give floor(N**(1/8)), exactly.
    n = (q.numerator * D ** 8) // q.denominator
    k = isqrt(isqrt(isqrt(n)))
    need(k ** 8 * q.denominator <= q.numerator * D ** 8 <
         (k + 1) ** 8 * q.denominator, 'certified dyadic eighth root')
    root_checks += 1
    if k ** 8 * q.denominator == q.numerator * D ** 8:
        return F(k, D), F(k, D)
    return F(k, D), F(k + 1, D)


def root(a):
    a = I(a)
    return root_point(a[0])[0], root_point(a[1])[1]


def vsub(a, b):
    return sub(a[0], b[0]), sub(a[1], b[1])


def norm2(a):
    return add(square(a[0]), square(a[1]))


def dist16(a, b):
    return eighth(norm2(vsub(a, b)))


def det(a, b):
    return sub(mul(a[0], b[1]), mul(a[1], b[0]))


def orient(a, b, c):
    return det(vsub(b, a), vsub(c, a))


def sign(a):
    a = I(a)
    if a[0] > 0:
        return 1
    if a[1] < 0:
        return -1
    raise ArithmeticError('enclosure does not decide sign')


def inside(a, lo, hi, label):
    a = I(a)
    need(F(lo) < a[0] <= a[1] < F(hi), label)


def serial(a):
    return [str(x) for x in I(a)]


b, c, d, lam = F(2073, 10000), F(4719, 10000), F(64, 10000), F(27, 1250)
A, B, C = (I(0), I(0)), (I(b), I(0)), (I(c), I(d))


def G(s):
    u, v, w = root(s), root(add(s, lam)), root(add(s, 1))
    x = div(sub(add(b * b, u), v), 2 * b)
    y = div(sub(sub(add(c * c + d * d, u), w), mul(2 * c, x)), 2 * d)
    return sub(norm2((x, y)), u), (x, y)


cuts = [F(9, 10000), F(11, 10000), F(13, 10000), F(1, 2), F(1), F(10 ** 16)]
bounds = [('0.38', '0.39'), ('-0.28', '-0.27'), ('0.51', '0.52'),
          ('-0.91', '-0.90'), ('9', '10'), ('-4.766', '-4.765')]
g_rows = []
for s, (lo, hi) in zip(cuts, bounds):
    val, xy = G(s)
    inside(val, lo, hi, 'independent G endpoint strict bound')
    g_rows.append({'s': str(s), 'G': serial(val), 'sign': sign(val)})
need([x['sign'] for x in g_rows] == [1, -1, 1, -1, 1, -1], 'all five sign changes')


def polynomial(t, q, h, ell):
    q2 = q[0] ** 2 + q[1] ** 2
    return q2 ** 8 * (((t - 1) ** 2 + h * h) ** 8 - (t * t + h * h) ** 8) - ell


def boundary_root(q, h, ell):
    lo, hi = F(-8), F(8)
    need(polynomial(lo, q, h, ell) > 0 > polynomial(hi, q, h, ell), 'monotone root bracket')
    for _ in range(140):
        mid = (lo + hi) / 2
        value = polynomial(mid, q, h, ell)
        if value == 0:
            return I(mid)
        if value > 0:
            lo = mid
        else:
            hi = mid
    need(polynomial(lo, q, h, ell) > 0 > polynomial(hi, q, h, ell), 'strict isolated boundary root')
    return lo, hi


t1 = boundary_root((c, d), F(10), F(1))
t3 = boundary_root((b, F(0)), F(1), lam)
t5 = boundary_root((c - b, d), F(-10), 1 - lam)
A1 = (sub(mul(t1, c), 10 * d), add(mul(t1, d), 10 * c))
A3 = (mul(t3, b), I(b))
A5 = (add(add(b, mul(t5, c - b)), 10 * d), sub(mul(t5, d), 10 * (c - b)))
points = [A1, A, A3, B, A5, C]
for q, boxes in [(A1, [('0.17194', '0.17196'), ('4.72219', '4.72221')]),
                 (A3, [('-0.55229', '-0.55227')]),
                 (A5, [('0.40359', '0.40361'), ('-2.64281', '-2.64279')])]:
    for coordinate, (lo, hi) in zip(q, boxes):
        inside(coordinate, lo, hi, 'strict algebraic boundary coordinate')
for p, q, r in combinations(points, 3):
    need(sign(orient(p, q, r)) in [-1, 1], 'all20 boundary triples noncollinear')
need(orient(A, B, C) == I(F('0.00132672')), 'exact even determinant')
inside(orient(A1, A3, A5), '6.37', '6.39', 'odd determinant')
cross = [sign(orient(A1, A, A3)), sign(orient(A1, A, B)),
         sign(orient(A3, B, A1)), sign(orient(A3, B, A))]
need(cross == [-1, 1, 1, -1], 'strict crossed boundary')
inside(sub(sub(dist16(A3, C), dist16(A3, A)), 1), '.98', '.99', 'A3 not outgoing solution')
need(b ** 16 != lam and A1[0][0] > b / 2 and A5[0][0] > b / 2,
     'global boundary exclusion reductions')

aa, ff, gg = dist16(A1, A), dist16(A3, A), dist16(A5, B)
L, M = sub(sub(gg, ff), lam), sub(aa, ff)
need(L[0] > 0 and M[0] > 0, 'fixed algebraic L M positive')
bp, cp = vsub(A5, A3), vsub(A1, A3)
determinant = det(bp, cp)
need(determinant[0] > 0, 'fixed incoming linear system invertible')


def H(s):
    u, v, w = root(s), root(add(s, L)), root(add(s, M))
    # Affine regrouping keeps the shared u coefficient together.
    nx = add(add(sub(mul(norm2(bp), cp[1]), mul(norm2(cp), bp[1])),
                 mul(u, sub(cp[1], bp[1]))), sub(mul(w, bp[1]), mul(v, cp[1])))
    ny = add(add(sub(mul(norm2(cp), bp[0]), mul(norm2(bp), cp[0])),
                 mul(u, sub(bp[0], cp[0]))), sub(mul(v, cp[0]), mul(w, bp[0])))
    Y = div(nx, mul(2, determinant)), div(ny, mul(2, determinant))
    return sub(norm2(Y), u), (add(A3[0], Y[0]), add(A3[1], Y[1]))


h0, _ = H(F(1, 100))
h1, _ = H(F(11, 1000))
inside(h0, '.00037', '.00038', 'fixed H left sign')
inside(h1, '-.00081', '-.00080', 'fixed H right sign')
_, Z = H((F(1, 100), F(11, 1000)))
inside(Z[0], '.1677', '.1717', 'whole incoming x box')
inside(Z[1], '-.0036', '-.0026', 'whole incoming y box')
for p, q in combinations(points, 2):
    need(sign(orient(p, q, Z)) in [-1, 1], 'whole incoming box avoids boundary pair line')

outgoing = []
for left, right in zip(cuts, cuts[1:]):
    original_left, original_right = left, right
    leftsign = sign(G(left)[0])
    for _ in range(120):
        mid = (left + right) / 2
        if sign(G(mid)[0]) == leftsign:
            left = mid
        else:
            right = mid
    need(original_left <= left < right <= original_right, 'retained disjoint root bracket')
    need(sign(G(left)[0]) * sign(G(right)[0]) == -1, 'strict opposite retained signs')
    _, X = G((left, right))
    for p, q in combinations(points, 2):
        need(sign(orient(p, q, X)) in [-1, 1], 'outgoing box avoids every boundary pair line')
    outgoing.append({'s_bracket': [str(left), str(right)], 'x_box': serial(X[0]), 'y_box': serial(X[1])})

x0, y0 = b / 2, (c * c + d * d - b * c) / (2 * d)
need(y0 == F(1249057, 128000), 'exact asymptotic coordinate')
need(x0 * x0 + y0 * y0 == F(39007985196121, 409600000000), 'exact asymptotic square')
need(x0 * x0 + y0 * y0 < F('95.235'), 'large-s negative margin')
print(json.dumps({'own_checks': checks, 'certified_dyadic_radical_endpoints': root_checks,
                  'dyadic_denominator': str(D), 'G_endpoint_bounds': g_rows,
                  'boundary_t_boxes': [serial(t1), serial(t3), serial(t5)],
                  'all20_boundary_triples_noncollinear': True, 'strict_crossing_signs': cross,
                  'H_bounds': [serial(h0), serial(h1)], 'whole_incoming_box': [serial(Z[0]), serial(Z[1])],
                  'five_disjoint_outgoing_root_boxes': outgoing,
                  'all_selected_center_boxes_avoid_all15_boundary_pair_lines': True,
                  'written_IVT_monotonicity_and_face_telescope_required': True,
                  'native_code_or_results_read': False, 'project_imports': 0,
                  'network': 0, 'file_writes': 0}, indent=2))
