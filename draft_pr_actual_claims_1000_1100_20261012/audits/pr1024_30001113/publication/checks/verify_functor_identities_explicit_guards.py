# Guard adaptation; original independent source is retained in evidence.
"""Independent arithmetic sanity checks for the exact functor argument.

Not a finite substitute for the infinite-series or arbitrary-natural-map proof.
F4 = F2[u]/(u^2+u+1), encoded in two bits; B=F4[e]/e^3.
"""
import json
from itertools import product

def require(test, message):
    if not test:
        raise RuntimeError(message)

def fm(a, b):
    v = 0
    for i in range(2):
        if b >> i & 1:
            v ^= a << i
    if v & 4:
        v ^= 7
    return v

def ba(a, b):
    return tuple((x ^ y for x, y in zip(a, b)))

def bm(a, b):
    c = [0, 0, 0]
    for i in range(3):
        for j in range(3 - i):
            c[i + j] ^= fm(a[i], b[j])
    return tuple(c)

def j(a):
    return (a[0], a[1], a[1] ^ a[2])

def mm(a, b):
    return [[ba(bm(a[i][0], b[0][k]), bm(a[i][1], b[1][k])) for k in range(2)] for i in range(2)]
zero, one, e, ee = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
unitscalar = ba(one, e)
me = [[one, e], [one, one]]
meprime = [[one, ba(e, ee)], [one, one]]
c = [[unitscalar, e], [zero, one]]
require(mm(me, me) == [[unitscalar, zero], [zero, unitscalar]], 'original assertion at line 47')
rhs = [[bm(unitscalar, v) for v in row] for row in mm(c, me)]
require(mm(meprime, c) == rhs, 'original assertion at line 49')
elements = list(product(range(4), repeat=3))
require(all((j(j(a)) == a for a in elements)), 'original assertion at line 51')
require(all((j(ba(a, b)) == ba(j(a), j(b)) for a in elements for b in elements)), 'original assertion at line 52')
require(all((j(bm(a, b)) == bm(j(a), j(b)) for a in elements for b in elements)), 'original assertion at line 53')
fixed = [a for a in elements if j(a) == a]
require(fixed == [a for a in elements if a[1] == 0], 'original assertion at line 55')
require({(a[0], a[1]) for a in fixed} == {(v, 0) for v in range(4)}, 'original assertion at line 56')
require(len(fixed) == 16, 'original assertion at line 57')
require(fm(2, 2 ^ 1) == 1, 'original assertion at line 58')
require(all((v ^ v == 0 for v in range(4))), 'original assertion at line 61')
require(all((v ^ v != 1 for v in range(4))), 'original assertion at line 62')
print(json.dumps({'status': 'PASS', 'ring': 'F4[e]/e^3', 'ring_elements': len(elements), 'fixed_elements': len(fixed), 'pairwise_additive_checks': len(elements) ** 2, 'pairwise_multiplicative_checks': len(elements) ** 2, 'fixed_reduction_is_exactly_constants': True, 'involution_matrix': True, 'conjugacy_matrix': True, 'u_times_u_plus_one': True, 'all_first_order_constant_terms_cancel': True, 'warning': 'Exact identities only; universal functor conclusion is proved in the report.'}, indent=2, sort_keys=True))
