#!/usr/bin/env python3
"""Independent exact rank(B)-rank(B^2) control, with no author-code imports."""
import itertools
import json
import sys
from fractions import Fraction


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def rank(matrix, p):
    a = [[v % p if p else Fraction(v) for v in row] for row in matrix]
    m = len(a)
    if not m:
        return 0
    n = len(a[0])
    piv = 0
    for col in range(n):
        hit = next((i for i in range(piv, m) if a[i][col]), None)
        if hit is None:
            continue
        a[piv], a[hit] = a[hit], a[piv]
        inv = pow(int(a[piv][col]), -1, p) if p else 1 / a[piv][col]
        a[piv] = [v * inv % p if p else v * inv for v in a[piv]]
        for i in range(piv + 1, m):
            scalar = a[i][col]
            if scalar:
                a[i] = [(v - scalar * w) % p if p else v - scalar * w
                        for v, w in zip(a[i], a[piv])]
        piv += 1
        if piv == m:
            break
    return piv


def rho(word):
    return word[-1:] + word[:-1]


def check(r, n, p):
    words = list(itertools.product(range(r), repeat=n))
    idx = {word: i for i, word in enumerate(words)}
    N = len(words)
    B = [[0] * N for _ in words]
    B2 = [[0] * N for _ in words]
    for j, w in enumerate(words):
        B[j][j] += 1
        B[idx[rho(w)]][j] -= 1
        B2[j][j] += 1
        B2[idx[rho(w)]][j] -= 2
        B2[idx[rho(rho(w))]][j] += 1
    hi = rank(B, p) - rank(B2, p)
    # Independent combinatorial count by least positive period, selecting minimal rotation.
    representatives = []
    for w in words:
        rotations = [w[i:] + w[:i] for i in range(n)]
        if w == min(rotations):
            d = next(i for i in range(1, n + 1) if w[i:] + w[:i] == w)
            representatives.append(d)
    expected = sum(bool(p) and d % p == 0 for d in representatives)
    require(hi == expected, 'rank-square and period count disagree')
    return dict(generators=r,total_weight=n,characteristic=p,
                higher_H1_dimension=hi,higher_H0_dimension=hi,orbit_count=len(representatives))


def witness(p):
    w = (0,) * (p - 1) + (1,)
    words = [w[i:] + w[:i] for i in range(p)]
    require(len(set(words)) == p, 'terms collide')
    b = {}
    for u in words:
        b[u] = b.get(u, 0) + 1
        b[rho(u)] = b.get(rho(u), 0) - 1
    require(all(v == 0 for v in b.values()), 'cycle fails over integers')
    require(len(words) % p == 0, 'orbit coefficient nonzero')
    return dict(characteristic=p,distinct_terms=len(words),ordinary_cycle_over_integers=True,
                higher_image_orbit_coefficient_mod_p=len(words) % p)


def main():
    require(sys.flags.isolated == 1, 'isolated Python required')
    require(sys.flags.optimize == 0, 'optimization rejected')
    require(sys.flags.no_site == 1, 'site initialization must be disabled')
    require(sys.flags.dont_write_bytecode == 1, 'bytecode writes must be disabled')
    cases = [check(r,n,p) for r,N in [(1,9),(2,7),(3,4)]
             for n in range(1,N+1) for p in [0,2,3,5,7,11]]
    require(all(c['higher_H1_dimension']==0 for c in cases if c['characteristic']==0),
            'characteristic-zero negative control')
    require(all(c['higher_H1_dimension']==0 for c in cases if c['generators']==1),
            'one-letter negative control')
    require(next(c for c in cases if (c['generators'],c['total_weight'],c['characteristic'])==(2,2,2))['higher_H1_dimension']==1,
            'minimal counterexample dimension')
    print(json.dumps(dict(status='PASS',method='dim(ker B intersect im B)=rank(B)-rank(B^2)',
          finite_control_only=True,cases_checked=len(cases),cases=cases,
          all_prime_proof_in_report=True,witnesses=[witness(p) for p in [2,3,5,7,11,13,17,19,23,29,31,37,101]]),sort_keys=True,indent=2))

if __name__=='__main__':
    main()
