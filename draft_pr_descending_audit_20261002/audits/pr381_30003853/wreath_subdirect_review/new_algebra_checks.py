#!/usr/bin/env python3
"""Independent exact controls, written before candidate proof/check inspection.

No candidate imports. Stdlib only. Finite checks supplement, not replace,
the universal proofs in INDEPENDENT_RECONSTRUCTION.md.
"""
from fractions import Fraction
from itertools import permutations, combinations, product
from math import gcd
from functools import reduce
import hashlib
import json
import random
from pathlib import Path


def clean(p):
    return {i: v for i, v in p.items() if v}


def add(p, q):
    z = p.copy()
    for i, v in q.items():
        z[i] = z.get(i, 0) + v
    return clean(z)


def scale(p, k):
    return clean({i: k*v for i, v in p.items()})


def shift(p, k):
    return {i+k: v for i, v in p.items()}


def delta(p):
    return add(shift(p, 1), scale(p, -1))


def ev(p):
    return sum(p.values())


def deriv(p):
    return sum(i*v for i, v in p.items())


def divide_delta(p):
    assert ev(p) == 0
    if not p:
        return {}
    q = {}
    last = 0
    for i in range(min(p), max(p)):
        last -= p.get(i, 0)
        q[i] = last
    q = clean(q)
    assert delta(q) == p
    return q


def wmul(a, b):
    p, k = a
    q, ell = b
    return add(p, shift(q, -k)), k+ell


def winv(a):
    p, k = a
    return scale(shift(p, k), -1), -k


def comm(a, b):
    return wmul(wmul(wmul(winv(a), winv(b)), a), b)


def character(g, m):
    p, k = g
    assert ev(p) % m == 0
    return k, ev(p)//m, deriv(p) % m


def determinant(a):
    a = [[Fraction(x) for x in row] for row in a]
    n = len(a)
    d = Fraction(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            d = -d
        v = a[j][j]
        d *= v
        for i in range(j+1, n):
            t = a[i][j]/v
            for k in range(j, n):
                a[i][k] -= t*a[j][k]
    assert d.denominator == 1
    return int(d)


def rank(a):
    a = [[Fraction(x) for x in row] for row in a]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][j]
        a[r] = [x/v for x in a[r]]
        for i in range(len(a)):
            if i != r:
                t = a[i][j]
                a[i] = [x-t*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def cyclic_matrix(m, n):
    # Basis m*e0, e1-e0, ..., e_(n-1)-e0 for the integral index-m lattice.
    basis = [[m] + [0]*(n-1)]
    for i in range(1, n):
        v = [0]*n
        v[0], v[i] = -1, 1
        basis.append(v)
    cols = []
    for v in basis:
        t = v[-1:] + v[:-1]
        d = [x-y for x, y in zip(t, v)]
        assert sum(d) == 0
        cols.append([sum(d)//m] + d[1:])
    return [list(row) for row in zip(*cols)]


def perm_mul(a, b):
    return tuple(a[b[i]] for i in range(5))


def perm_inv(a):
    return tuple(a.index(i) for i in range(5))


ident = tuple(range(5))
A5 = [p for p in permutations(range(5))
      if sum(p[i] > p[j] for i in range(5) for j in range(i+1, 5)) % 2 == 0]


def tupmul(a, b):
    return tuple(perm_mul(x, y) for x, y in zip(a, b))


def tupinv(a):
    return tuple(perm_inv(x) for x in a)


def closure(gens):
    e = tuple(ident for _ in gens[0])
    seen = {e}
    todo = [e]
    steps = list(gens) + [tupinv(g) for g in gens]
    while todo:
        a = todo.pop()
        for b in steps:
            c = tupmul(a, b)
            if c not in seen:
                seen.add(c)
                todo.append(c)
    return seen


def hmul(a, b, p):
    x, y, z = a
    xx, yy, zz = b
    return x+xx, y+yy, (z+zz+x*yy) % p


def hinv(a, p):
    x, y, z = a
    return -x, -y, (-z+x*y) % p


def hcomm(a, b, p):
    return hmul(hmul(hmul(hinv(a, p), hinv(b, p), p), a, p), b, p)


def run():
    rng = random.Random(38130003853)
    controls = []
    for m in range(1, 13):
        r, s, t = ({0: -1, 1: 1}, 0), ({0: m}, 0), ({}, 1)
        assert comm(r, t) == ({0: 1, 1: -2, 2: 1}, 0)
        assert comm(s, t) == ({0: -m, 1: m}, 0)
        assert comm(r, s) == ({}, 0)
        assert character(r, m) == (0, 0, 1 % m)
        assert character(s, m) == (0, 1, 0)
        for k in range(1, m+1):
            q = divide_delta(scale(r[0], k))
            assert (ev(q) % m == 0) == (k % m == 0)
        for _ in range(100):
            q = clean({i: rng.randrange(-7, 8) for i in range(-12, 13)})
            u = clean({i: rng.randrange(-7, 8) for i in range(-12, 13)})
            a = add(scale(q, m), delta(u))
            assert ev(a) % m == 0
            # Exact kernel test, with Laurent support and negative exponents.
            if ev(a) == 0:
                b = divide_delta(a)
                assert (deriv(a) % m == 0) == (ev(b) % m == 0)
            # Random pairs in the actual infinite restricted group.
            b = add(scale(u, m), delta(q))
            g, h = (a, rng.randrange(-9, 10)), (b, rng.randrange(-9, 10))
            c = character(wmul(g, h), m)
            cg, ch = character(g, m), character(h, m)
            assert c == (cg[0]+ch[0], cg[1]+ch[1], (cg[2]+ch[2]) % m)
            cp, ck = comm(g, h)
            assert ck == 0 and ev(cp) == 0
            assert ev(divide_delta(cp)) % m == 0
        controls.append({'m': m, 'infinite_coinvariant_free_rank': 1,
                         'infinite_torsion_order': m, 'H_ab_free_rank': 2,
                         'actual_group_random_pair_checks': 100})

    cyclic = []
    for m in range(1, 13):
        for n in range(2, 9):
            a = cyclic_matrix(m, n)
            assert rank(a) == n-1
            minors = [abs(determinant([[a[i][j] for j in cols]
                                      for i in range(1, n)]))
                      for cols in combinations(range(n), n-1)]
            tors = reduce(gcd, minors)
            assert tors == gcd(m, n)
            cyclic.append({'m': m, 'n': n, 'rational_rank': n-1,
                           'maximal_minor_gcd': tors})

    x = (1, 2, 0, 3, 4)  # 3-cycle
    y = (1, 0, 3, 2, 4)  # double transposition
    # This pair generates A5 (verified, never assumed).
    if len(closure([(x,), (y,)])) != 60:
        y = (1, 2, 3, 4, 0)  # 5-cycle
    assert len(closure([(x,), (y,)])) == 60
    all_comm = [(perm_mul(perm_mul(perm_mul(perm_inv(a), perm_inv(b)), a), b),)
                for a in A5 for b in A5]
    assert len(closure(all_comm)) == 60
    odd = (1, 0, 2, 3, 4)
    def twist(a):
        return perm_mul(perm_mul(odd, a), perm_inv(odd))
    tests = {
        'diagonal': [(x, x), (y, y)],
        'outer_twisted_diagonal': [(x, twist(x)), (y, twist(y))],
        'full_product': [(x, ident), (y, ident), (ident, x), (ident, y)],
    }
    subdirect = []
    for name, gens in tests.items():
        s = closure(gens)
        assert all({g[i] for g in s} == set(A5) for i in range(2))
        normalizer = set()
        for q in product(A5, repeat=2):
            qi = tupinv(q)
            if all(tupmul(tupmul(q, g), qi) in s for g in gens):
                normalizer.add(q)
        assert normalizer == s
        subdirect.append({'case': name, 'subgroup_order': len(s),
                          'normalizer_order': len(normalizer),
                          'both_projection_orders': [60, 60]})

    central_boundaries = []
    for p in [2, 3, 5, 7]:
        a, b = (1, 0, 0), (0, 1, 0)
        assert hcomm(a, b, p) == (0, 0, 1)
        for aa, bb, cc, dd in product(range(-2, 3), repeat=4):
            c = hcomm((aa, bb, 0), (cc, dd, 0), p)
            assert c == (0, 0, (aa*dd-cc*bb) % p)
            # Paired elements with matching abelian coordinates have paired
            # commutators equal even when their central coordinates differ.
            assert c == hcomm((aa, bb, 1), (cc, dd, 2), p)
        central_boundaries.append({'p': p, 'G_ab_free_rank': 2,
                                   'fiber_H_ab_free_rank': 2,
                                   'fiber_H_ab_torsion_order': p,
                                   'hypothesis_violated': 'derived simple group is abelian'})

    return {'all_passed': True, 'seed': 38130003853,
            'infinite_restricted_wreath_controls': controls,
            'finite_cyclic_integral_controls': cyclic,
            'A5_simple_subdirect_controls': subdirect,
            'central_simple_derived_negative_controls': central_boundaries,
            'limits': 'Finite controls verify instances; universal statements rest on the sealed proofs.'}


if __name__ == '__main__':
    result = run()
    print(json.dumps(result, indent=2))
