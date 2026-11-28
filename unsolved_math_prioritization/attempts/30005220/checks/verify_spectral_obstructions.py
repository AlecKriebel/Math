#!/usr/bin/env python3
"""Exact finite character-spectrum checks. Standard-library only.

An ordinary character of C_n is stored as a multiset of linear-character
exponents. Equality of characters is equality of exponent multiplicities,
not approximate comparison of complex roots. No irreducibility is inferred.
"""
import collections
import itertools
import json
import math
from pathlib import Path


def units(n):
    return [u for u in range(n) if math.gcd(u, n) == 1] if n > 1 else [0]


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def phi(n):
    return len(units(n))


def ppart(n, p):
    a = 1
    while n % p == 0:
        a *= p
        n //= p
    return a


def stabilizer(n, weights):
    c = collections.Counter(w % n for w in weights)
    return [u for u in units(n) if collections.Counter((u*w) % n for w in weights) == c]


def conductor(n, weights):
    """Conductor divides n. Q_n^H <= Q_d iff Gal(Q_n/Q_d) <= H."""
    h = set(stabilizer(n, weights))
    for d in divisors(n):
        if all(u in h for u in units(n) if (u - 1) % d == 0):
            return d
    raise AssertionError('No conductor divisor found')


def record(n, p, weights):
    pn = ppart(n, p)
    c = conductor(n, weights)
    ca = ppart(c, p)
    h = stabilizer(pn, weights)
    field_degree = phi(pn) // len(h)
    assert phi(ca) % field_degree == 0
    return {'n': n, 'p': p, 'degree': len(weights), 'weights': list(weights),
            'global_conductor': c,
            'restriction_conductor': conductor(pn, weights),
            'restriction_stabilizer': h,
            'restriction_field_degree': field_degree,
            'tested_index': phi(ca) // field_degree}


def nextprime(p):
    q = p + 1
    while any(q % d == 0 for d in range(2, math.isqrt(q) + 1)):
        q += 1
    return q


def main():
    # Reducible characters on C_(p^2) x C_q ~= C_(p^2*q).
    obstruction = []
    for p in (2, 3, 5, 7, 11):
        q = nextprime(p)
        n = p*p*q
        weights = [0] + [(q*(1+p*j)+p*p*j) % n for j in range(p)]
        r = record(n, p, weights)
        assert r['global_conductor'] == n
        assert r['restriction_conductor'] == (1 if p == 2 else p)
        assert r['tested_index'] == p
        assert len(stabilizer(n, weights)) == 1
        assert len(set(weights)) == p+1
        # Norm equals p+1, so these are certainly reducible, not counterexamples.
        r['character_norm'] = sum(m*m for m in collections.Counter(weights).values())
        assert r['character_norm'] == p+1
        obstruction.append(r)

    # At p=2, conductor equality alone does not imply field equality.
    binary = record(8, 2, [0, 1, 7])
    assert binary['global_conductor'] == binary['restriction_conductor'] == 8
    assert binary['tested_index'] == 2
    assert binary['restriction_stabilizer'] == [1, 7]

    # Modest finite sanity tests for the proved degree<p proposition.
    plans = [(2, 8, 1), (2, 24, 1), (3, 9, 2), (3, 18, 2),
             (3, 45, 2), (5, 25, 3), (5, 50, 2), (7, 49, 2)]
    totals = []
    for p, n, maxdegree in plans:
        count = 0
        for d in range(1, maxdegree+1):
            assert d < p
            for w in itertools.combinations_with_replacement(range(n), d):
                r = record(n, p, w)
                assert r['tested_index'] % p != 0, r
                count += 1
        totals.append({'p':p, 'n':n, 'max_degree':maxdegree, 'cases':count})

    # Proper cyclic p-subgroup induction: high-order linear multiplicities are 0 mod p.
    induction_cases = 0
    for p in (2, 3, 5):
        for b in range(1, 5):
            n = p**b
            for h in range(b):
                subgroup_order = p**h
                for t in range(subgroup_order):
                    extensions = [j for j in range(n) if j % subgroup_order == t]
                    for i in range(2, b+1):
                        cnt = sum(n//math.gcd(n, j) == p**i for j in extensions)
                        assert cnt % p == 0, (p,b,h,t,i,cnt)
                        induction_cases += 1

    out = {'status':'PASS',
           'scope':'Exact spectral checks, not a search over irreducible characters of arbitrary groups.',
           'reducible_obstructions':obstruction,
           'binary_conductor_only_obstruction':binary,
           'small_degree_test_plans':totals,
           'small_degree_cases':sum(r['cases'] for r in totals),
           'proper_cyclic_induction_congruences':induction_cases}
    target = Path(__file__).with_name('verification_results.json')
    target.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
