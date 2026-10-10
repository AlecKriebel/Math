#!/usr/bin/env python3
"""Exact finite sanity controls; not a proof or numerical reduced-length solver."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json


def mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def length(a):
    return sum(map(abs, a), F(0))


def linear_product(roots, scale=F(1)):
    a, m = [scale], abs(scale)
    for r in roots:
        a = mul(a, [-r, F(1)])
        m *= max(F(1), abs(r))
    return a, m


def run():
    # Every Mahler measure here comes from an explicitly specified root family.
    roots = [F(-2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(2)]
    ps = []
    for degree in range(3):
        for rs in combinations_with_replacement(roots, degree):
            for scale in [F(-3, 2), F(1, 3), F(2)]:
                ps.append(linear_product(rs, scale))
    # Nonreal conjugate pairs of radius r: discriminant < 0, M=max(1,r)^2.
    for r in [F(1, 2), F(1), F(2)]:
        for b in [F(0), r]:
            assert b*b < 4*r*r
            for scale in [F(-3, 2), F(1, 3), F(2)]:
                ps.append(([scale*r*r, scale*b, scale], abs(scale)*max(F(1), r)**2))
    qs = [linear_product(rs) for rs in [(), (F(0),), (F(1, 2),), (F(-1, 2),), (F(1),), (F(-1),), (F(2),), (F(-2),), (F(1, 2), F(2)), (F(-2), F(2))]]
    ts = [F(k, 4) for k in range(-8, 9)]
    count = 0
    for t in ts:
        at = [F(1), t, F(1)]
        assert 4-t*t >= 0
        for p, mp in ps:
            for q, mq in qs:
                assert q[-1] == 1 and mq >= 1
                value = length(mul(mul(at, p), q))
                assert value >= 2*mp*mq >= 2*mp
                count += 1
    # Sharp cases t=0, P=c*x^m, Q=1; plus zero-polynomial convention.
    sharp = 0
    for c in [F(-3, 2), F(1, 3), F(2)]:
        for degree in range(9):
            p = [F(0)]*degree+[c]
            assert length(mul([F(1), F(0), F(1)], p)) == 2*abs(c)
            sharp += 1
    assert length(mul([F(1), F(2), F(1)], [F(0)])) == 0
    # Negative control: drop monicity of Q, using Q=1/10, t=0, P=1.
    assert length([F(1, 10), F(0), F(1, 10)]) < 2
    # Negative control: omit the unit-circle root condition from theorem D.
    # x^2+x+5 has conjugate roots of modulus sqrt(5), hence M=5.
    assert 1-4*5 < 0 and length([F(5), F(1), F(1)]) < 2*5
    return {
        'arithmetic': 'fractions.Fraction exact rational arithmetic',
        'parameter_count': len(ts),
        'P_count': len(ps),
        'Q_count': len(qs),
        'product_inequality_checks': count,
        'sharpness_checks': sharp,
        'zero_polynomial_checks': 1,
        'negative_controls': 2,
        'all_checks_passed': True,
        'scope_limit': 'Finite diagnostic checks only; not exhaustive in t, P, or Q; no infimum calculation; published theorem D remains the proof input.'
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
