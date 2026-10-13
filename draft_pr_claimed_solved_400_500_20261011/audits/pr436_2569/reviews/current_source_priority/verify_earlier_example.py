#!/usr/bin/env python3
"""Independent exact checks of the already published order-12 example.

This is validation of the cited example, not a search for a new example.
Uses only Python's standard library; every failure raises explicitly.
"""
import json
from fractions import Fraction as F
from pathlib import Path


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def matmul(x, y, p=None):
    z = (x[0]*y[0]+x[1]*y[2], x[0]*y[1]+x[1]*y[3],
         x[2]*y[0]+x[3]*y[2], x[2]*y[1]+x[3]*y[3])
    return tuple(v % p for v in z) if p else z


def matpow(x, n, p=None):
    z = (1, 0, 0, 1)
    for _ in range(n):
        z = matmul(z, x, p)
    return z


def basis(vectors):
    pivots = {}
    for x in vectors:
        while x:
            p = x.bit_length()-1
            if p in pivots:
                x ^= pivots[p]
            else:
                pivots[p] = x
                break
    return list(pivots.values())


def span(vectors):
    out = [0]
    for x in basis(vectors):
        out += [y ^ x for y in out]
    return out


elements = [(i, j) for j in range(4) for i in range(3)]
indices = {g: n for n, g in enumerate(elements)}


def groupmul(x, y):
    i, j = x
    k, l = y
    return ((i + (-1)**j*k) % 3, (j+l) % 4)


table = [[indices[groupmul(g, h)] for h in elements] for g in elements]


def ringmul(x, y):
    z = 0
    for i in range(12):
        if x >> i & 1:
            for j in range(12):
                if y >> j & 1:
                    z ^= 1 << table[i][j]
    return z


A, B, I = (0, 1, 1, 1), (1, 1, 0, 1), (1, 0, 0, 1)
AQ, BQ = (0, -1, 1, -1), (1, -1, 0, -1)
for aa, bb, modulus in [(A, B, 2), (AQ, BQ, None)]:
    require(matpow(aa, 3, modulus) == I, 'A order 3')
    require(matpow(bb, 2, modulus) == I, 'B order 2')
    require(matmul(matmul(bb, aa, modulus), bb, modulus)
            == matpow(aa, 2, modulus), 'inversion action')
require(len(basis(sum(v << i for i, v in enumerate(m))
                  for m in [I, A, B, matmul(A, B, 2)])) == 4,
        'matrix algebra span')
require((1+1+1) % 2 == 1 and (0*0+0+1) % 2 == 1,
        'polynomial has no roots over F2')

images = [matmul(matpow(A, i, 2), matpow(B, j, 2), 2) for i, j in elements]


def quotient(x):
    m = (0, 0, 0, 0)
    for i in range(12):
        if x >> i & 1:
            m = tuple(a ^ b for a, b in zip(m, images[i]))
    return (x.bit_count() & 1, m)


def quotient_zero(x):
    return quotient(x) == (0, (0, 0, 0, 0))


for i in range(12):
    for j in range(12):
        require(images[table[i][j]] == matmul(images[i], images[j], 2),
                'group quotient multiplication')

unit = 1 << indices[(0, 0)]
a = 1 << indices[(1, 0)]
a2 = 1 << indices[(2, 0)]
b = 1 << indices[(0, 1)]
z = 1 << indices[(0, 2)]
e, c = unit ^ a ^ a2, a ^ a2
f = ringmul(c, a ^ ringmul(a, b) ^ unit ^ z)
require(ringmul(e, e) == e and ringmul(f, f) == f, 'idempotents')
require(ringmul(e, f) == ringmul(f, e) == 0, 'orthogonality')
require(quotient(f) == (0, (0, 0, 0, 1)), 'f image is E22')

radical = basis(x for x in range(4096) if quotient_zero(x))
radical_dimensions = []
power = radical
while power:
    radical_dimensions.append(len(power))
    power = basis(ringmul(x, y) for x in power for y in radical)
    require(len(radical_dimensions) <= 12, 'nilpotence')
radical_dimensions.append(0)
require(radical_dimensions == [7, 2, 1, 0], 'radical powers')
require(len({quotient(x) for x in range(4096)}) == 32, 'quotient surjectivity')

projectives = []
for label, t in [('e', e), ('f', f)]:
    left = basis(ringmul(1 << i, t) for i in range(12))
    corner = basis(ringmul(ringmul(t, 1 << i), t) for i in range(12))
    corner_rad = basis(ringmul(ringmul(t, x), t) for x in radical)
    require(len(corner)-len(corner_rad) == 1, 'primitive corner quotient')
    projectives.append({'idempotent': label, 'mask': t,
                        'dimension': len(left), 'corner_dimension': len(corner),
                        'corner_radical_dimension': len(corner_rad)})
require([x['dimension'] for x in projectives] == [4, 4], 'PIM dimensions')
require([(x['corner_dimension'], x['corner_radical_dimension'])
         for x in projectives] == [(4, 3), (2, 1)], 'PIM corners')

# Rational quaternion algebra Q(omega) + Q(omega)j.
def emul(x, y):
    a, b = x
    c, d = y
    return (a*c-b*d, a*d+b*c-b*d)


def econj(x):
    return (x[0]-x[1], -x[1])


def add(x, y):
    return tuple(a+b for a, b in zip(x, y))


def qmul(x, y):
    u, v, s, t = x[:2], x[2:], y[:2], y[2:]
    p = emul(u, s)
    q = emul(v, econj(t))
    return tuple(a-b for a, b in zip(p, q)) + add(emul(u, t), emul(v, econj(s)))


def qpow(x, n):
    out = (1, 0, 0, 0)
    for _ in range(n):
        out = qmul(out, x)
    return out


qbasis = [tuple(F(int(i == j)) for i in range(4)) for j in range(4)]
for x in qbasis:
    for y in qbasis:
        for zz in qbasis:
            require(qmul(qmul(x, y), zz) == qmul(x, qmul(y, zz)), 'associativity')
omega, jj, one = qbasis[1], qbasis[2], qbasis[0]
qimages = [qmul(qpow(omega, i), qpow(jj, j)) for i, j in elements]
require(len(set(qimages)) == 12, 'faithful quaternion group')
for i in range(12):
    for j in range(12):
        require(qimages[table[i][j]] == qmul(qimages[i], qimages[j]), 'quaternion group products')
x = add(omega, qmul(omega, jj))
require(add(add(qmul(x, x), x), (2, 0, 0, 0)) == (0, 0, 0, 0),
        'explicit nonlifting residue polynomial')

out = {'verdict': 'PASS_EARLIER_EXACT_EXAMPLE_FINITE_CHECKS',
       'purpose': 'Independent verification of existing source example only',
       'proof_search_turns_added': 0,
       'group_order': 12, 'prime': 2, 'simple_dimensions': [1, 2],
       'all_simple_rational_lifts': ['Q', 'W of dimension 2'],
       'projectives': projectives, 'radical_power_dimensions': radical_dimensions,
       'idempotent_count': sum(ringmul(x, x) == x for x in range(4096)),
       'basis_associativity_checks': 64, 'faithful_group_product_checks': 144,
       'quaternion_norm_formula': 'x^2-xy+y^2+z^2-zt+t^2',
       'universal_division_and_radical_arguments': 'Written proof audit; finite checking is supplementary',
       'actual_nonlift_PIM': 'kGf; O tensor any hypothetical lift would be projective of R-rank 2, while D dimensions over Q are multiples of 4'}
Path(__file__).with_name('earlier_example_checks.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
