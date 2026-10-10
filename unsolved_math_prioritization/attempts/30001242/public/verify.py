#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; Python standard library only.

Build each degree of S/(x^N-y^(N-1)z,l1,l2) directly as a relation matrix.
No computer-algebra package, saved certificate, or network input is used.
"""
from fractions import Fraction
from itertools import product
import json
import random


def monomials(m):
    if m < 0:
        return []
    return [(a, b, m-a-b) for a in range(m+1) for b in range(m-a+1)]


def rank(rows, p):
    if not rows:
        return 0
    a = [[x % p for x in r] for r in rows] if p else [list(map(Fraction, r)) for r in rows]
    nr, nc = len(a), len(a[0])
    out = 0
    for col in range(nc):
        pivot = next((i for i in range(out, nr) if a[i][col]), None)
        if pivot is None:
            continue
        a[out], a[pivot] = a[pivot], a[out]
        inv = pow(a[out][col], -1, p) if p else 1/a[out][col]
        a[out] = [(x*inv) % p for x in a[out]] if p else [x*inv for x in a[out]]
        for i in range(out+1, nr):
            if a[i][col]:
                c = a[i][col]
                a[i] = [(x-c*y) % p for x, y in zip(a[i], a[out])] if p else [x-c*y for x, y in zip(a[i], a[out])]
        out += 1
        if out == nr:
            break
    return out


def quotient_dim(N, m, pair, p):
    basis = monomials(m)
    index = {e: i for i, e in enumerate(basis)}
    rows = []
    for coefficients in pair:
        for e in monomials(m-1):
            row = [0]*len(basis)
            for j, coeff in enumerate(coefficients):
                target = tuple(e[i]+(i == j) for i in range(3))
                row[index[target]] += coeff
            rows.append(row)
    for e in monomials(m-N):
        row = [0]*len(basis)
        row[index[(e[0]+N, e[1], e[2])]] += 1
        row[index[(e[0], e[1]+N-1, e[2]+1)]] -= 1
        rows.append(row)
    return len(basis)-rank(rows, p)


def cross(pair):
    (a,b,c), (d,e,f) = pair
    return (b*f-c*e, c*d-a*f, a*e-b*d)


def main():
    assertions = 0
    matrices = 0
    generic_pairs = 0
    exceptional_rank_two = 0
    dependent_pairs = 0
    field_stats = []
    for p in (0,2,3,5,7):
        if p == 2:
            # Every ordered pair of linear forms over F_2.
            pairs = [(row[:3], row[3:]) for row in product(range(2), repeat=6)]
        else:
            pairs = [((0,1,0),(0,0,1)), ((1,0,0),(0,1,0)),
                     ((1,0,0),(2,0,0)), ((0,0,0),(0,0,0)),
                     ((1,2,3),(3,1,4)), ((1,1,0),(0,1,1))]
            rng = random.Random(1242+p)
            for _ in range(6 if p == 0 else 12):
                pairs.append((tuple(rng.randrange(-3,4) for _ in range(3)),
                              tuple(rng.randrange(-3,4) for _ in range(3))))
        degrees = range(2,5) if p == 0 else range(2,7)
        before = matrices
        for N in degrees:
            for pair in pairs:
                r = rank(pair, p)
                v = cross(pair)
                zero = lambda x: (x % p == 0) if p else (x == 0)
                assert all(zero(sum(a*b for a,b in zip(row,v))) for row in pair)
                assertions += 1
                c = v[0]**N-v[1]**(N-1)*v[2]
                good = not zero(c)
                if good:
                    assert r == 2
                    assertions += 1
                    generic_pairs += 1
                elif r == 2:
                    exceptional_rank_two += 1
                else:
                    dependent_pairs += 1
                for m in range(N+2):
                    got = quotient_dim(N,m,pair,p)
                    matrices += 1
                    if m < N:
                        expected = len([e for e in monomials(m) if all(e[i] == 0 for i in range(r))])
                        # S/(l1,l2) is a polynomial ring in 3-r variables.
                        assert got == expected and got > 0
                        assertions += 1
                    if r == 2:
                        expected = int(m < N) if good else 1
                        assert got == expected
                        assertions += 1
                    if r == 0:
                        expected = len(monomials(m))-len(monomials(m-N))
                        assert got == expected
                        assertions += 1
                # The open-set witness is characteristic-independent.
                witness = cross(((0,1,0),(0,0,1)))
                assert witness == (1,0,0)
                assert witness[0]**N-witness[1]**(N-1)*witness[2] == 1
                assertions += 2
        field_stats.append({'characteristic':p, 'pairs_per_degree':len(pairs),
                            'N_values':list(degrees), 'degree_matrices':matrices-before})
    result = {
        'problem_id':30001242, 'result':'PASS',
        'exact_assertions':assertions, 'degree_matrices':matrices,
        'generic_pair_degree_cases':generic_pairs,
        'exceptional_rank_two_pair_degree_cases':exceptional_rank_two,
        'dependent_pair_degree_cases':dependent_pairs,
        'fields':field_stats,
        'scope':'Finite exact controls only. Genericity and all-N nonexistence are proved in PROOF.md.'
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
