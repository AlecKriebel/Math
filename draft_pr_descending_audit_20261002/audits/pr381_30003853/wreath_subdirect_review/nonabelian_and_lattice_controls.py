#!/usr/bin/env python3
"""Additional exact controls after source/candidate comparison.

Imports this audit's independent permutation and rational arithmetic only;
never imports candidate code. Tests actual multiplication, not asserted counts.
"""
from itertools import product, combinations
import json
import random
from new_algebra_checks import perm_mul, perm_inv, ident, determinant, rank


def clean(a):
    return {i: v for i, v in a.items() if v != ident}


def shift(a, k):
    return {i+k: v for i, v in a.items()}


def bmul(a, b):
    return clean({i: perm_mul(a.get(i, ident), b.get(i, ident))
                  for i in a.keys() | b.keys()})


def binv(a):
    return {i: perm_inv(v) for i, v in a.items()}


def mul(a, b):
    p, k = a
    q, ell = b
    return bmul(p, shift(q, -k)), k+ell


def inv(a):
    p, k = a
    return shift(binv(p), k), -k


def run():
    rng = random.Random(38130003854)
    x, y = (1, 2, 0, 3, 4), (1, 2, 3, 4, 0)
    assert perm_mul(x, y) != perm_mul(y, x)
    choices = [ident, x, y, perm_inv(x)]
    lamps = [clean(dict(zip((-7, 0, 5), values)))
             for values in product(choices, repeat=3)]
    conjugates = 0
    for a, b, k in product(lamps, lamps, (-11, -3, -1, 1, 4, 17)):
        s = b, k
        assert mul(s, inv(s)) == ({}, 0)
        assert mul(inv(s), s) == ({}, 0)
        c = mul(mul(inv(s), (a, 0)), s)
        expected = shift(bmul(bmul(binv(b), a), b), k)
        assert c == (expected, 0)
        assert set(c[0]) == {i+k for i in a}
        conjugates += 1
    for _ in range(1000):
        a, b, c = [(rng.choice(lamps), rng.randrange(-10, 11)) for _ in range(3)]
        assert mul(mul(a, b), c) == mul(a, mul(b, c))
    supports = 0
    for n in range(1, 7):
        for s in combinations(range(-4, 5), n):
            for k in (-17, -2, -1, 1, 3, 11):
                assert not {i+k for i in s}.issubset(s)
                supports += 1

    lattice_cases = []
    for m in range(1, 13):
        # Columns are basis vectors for left_f=left_g modulo m.
        basis = [[m, 0, 1, 0], [0, 1, 0, 0],
                 [0, 0, 1, 0], [0, 0, 0, 1]]
        assert determinant(basis) == m
        assert rank(basis) == 4
        tests = 0
        for a, b, c, d in product(range(-4, 5), repeat=4):
            if (a-c) % m:
                continue
            coeff = ((a-c)//m, b, c, d)
            decoded = tuple(sum(basis[i][j]*coeff[j] for j in range(4))
                            for i in range(4))
            assert decoded == (a, b, c, d)
            tests += 1
        # Ambient quotient has m distinct cosets; the lattice itself has
        # an injective integral parametrization by Z^4, so no intrinsic torsion.
        assert len({(a-c) % m for a in range(m) for c in range(m)}) == m
        lattice_cases.append({'m': m, 'determinant': m,
                              'ambient_quotient_order': m,
                              'intrinsic_free_rank': 4,
                              'integral_coordinate_checks': tests})
    return {'all_passed': True, 'A5_wreath_noncommuting_lamps': True,
            'exact_conjugation_checks': conjugates,
            'associativity_checks': 1000,
            'nonempty_finite_support_shift_checks': supports,
            'F_factor_congruence_lattice_controls': lattice_cases,
            'limits': 'Does not implement FP2 recognition or Bleak classification; those are source-theorem inputs.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
