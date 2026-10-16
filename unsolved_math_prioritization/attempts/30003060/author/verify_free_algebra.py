#!/usr/bin/env python3
"""Exact finite controls for the authored free-algebra calculation.

Standard library only. Importing this file does not run tests or access files.
The proof covers all primes; this finite program is a diagnostic cross-check.
"""
from fractions import Fraction
from itertools import product
import json
import sys


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def rref(rows, prime):
    a = [[x % prime if prime else Fraction(x) for x in row] for row in rows]
    if not a:
        return a, []
    m, n, row, pivots = len(a), len(a[0]), 0, []
    for col in range(n):
        pivot = next((i for i in range(row, m) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        inv = pow(int(a[row][col]), -1, prime) if prime else 1 / a[row][col]
        a[row] = [(x * inv) % prime if prime else x * inv for x in a[row]]
        for i in range(m):
            if i != row and a[i][col]:
                mul = a[i][col]
                a[i] = [(x - mul * y) % prime if prime else x - mul * y
                        for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == m:
            break
    return a, pivots


def matrix_dimensions(alphabet_size, length, prime):
    words = list(product(range(alphabet_size), repeat=length))
    index = {w: i for i, w in enumerate(words)}
    d = len(words)
    # Basis e_w = prefix(w) tensor last(w).  b(e_w)=w-last(w)prefix(w).
    b = [[0] * d for _ in words]
    for j, w in enumerate(words):
        b[j][j] += 1
        b[index[(w[-1],) + w[:-1]]][j] -= 1
    reduced, pivots = rref(b, prime)
    free = [j for j in range(d) if j not in pivots]
    cycles = []
    for j in free:
        v = [0] * d
        v[j] = 1
        for i, col in enumerate(pivots):
            v[col] = -reduced[i][j]
        cycles.append(v)
    for v in cycles:
        need(all((sum(x * y for x, y in zip(row, v)) % prime == 0) if prime
                 else sum(x * y for x, y in zip(row, v)) == 0 for row in b),
             'nullspace basis is not a cycle')
    # Under concatenation, delta on cycles is the identity into coker(b).
    combined = [row + [v[i] for v in cycles] for i, row in enumerate(b)]
    rank_combined = len(rref(combined, prime)[1])
    delta_rank = rank_combined - len(pivots)
    return {'hk0': d - len(pivots), 'hk1': len(cycles),
            'delta_rank': delta_rank, 'hi0': d - rank_combined,
            'hi1': len(cycles) - delta_rank}


def orbit_dimensions(alphabet_size, length, prime):
    # Separately implemented: no matrix or nullspace routines are used.
    remaining = set(product(range(alphabet_size), repeat=length))
    sizes = []
    while remaining:
        w = min(remaining)
        orbit = {w[i:] + w[:i] for i in range(length)}
        need(orbit <= remaining, 'orbits overlap incorrectly')
        remaining.difference_update(orbit)
        sizes.append(len(orbit))
    bad = sum(prime != 0 and d % prime == 0 for d in sizes)
    return {'hk0': len(sizes), 'hk1': len(sizes),
            'delta_rank': len(sizes) - bad, 'hi0': bad, 'hi1': bad}


def explicit_witness(prime):
    # Direct noncommutative polynomial telescoping and quotient certificate.
    w = (0,) * (prime - 1) + (1,)
    orbit = [w[-i:] + w[:-i] if i else w for i in range(prime)]
    need(len(set(orbit)) == prime, 'witness orbit is not primitive')
    b = {}
    delta = {}
    certificate = {}
    for word in orbit:
        rotated = (word[-1],) + word[:-1]
        b[word] = (b.get(word, 0) + 1) % prime
        b[rotated] = (b.get(rotated, 0) - 1) % prime
        delta[word] = (delta.get(word, 0) + 1) % prime
    need(all(c == 0 for c in b.values()), 'witness is not a b-cycle')
    # Sum_{i=1}^{p-1}(w_i-w_0) is explicitly a sum of commutators:
    # w_i = uv, w_0 = vu, with u the final i letters of w_0.
    for i in range(1, prime):
        u, v = w[-i:], w[:-i]
        need(u + v == orbit[i] and v + u == w, 'commutator factorization')
        certificate[u + v] = (certificate.get(u + v, 0) + 1) % prime
        certificate[v + u] = (certificate.get(v + u, 0) - 1) % prime
    need(delta == {word: certificate.get(word, 0) for word in delta},
         'delta is not the certified commutator sum')
    return {'characteristic': prime, 'total_weight': prime,
            'distinct_chain_terms': prime, 'cycle_verified': True,
            'commutator_certificate_verified': True,
            'no_incoming_higher_boundary': 'W2=0 for the free algebra'}


def main():
    need(sys.flags.isolated == 1, 'run with python -I')
    need(sys.flags.optimize == 0, 'optimized Python is unsupported')
    fields = [0, 2, 3, 5, 7, 11]
    cases = []
    for alphabet, max_length in [(1, 8), (2, 7), (3, 4)]:
        for n in range(1, max_length + 1):
            for characteristic in fields:
                a = matrix_dimensions(alphabet, n, characteristic)
                b = orbit_dimensions(alphabet, n, characteristic)
                need(a == b, 'matrix/orbit mismatch')
                cases.append({'generators': alphabet, 'total_weight': n,
                              'characteristic': characteristic, **a})
    witnesses = [explicit_witness(p) for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]]
    need(next(c for c in cases if (c['generators'], c['total_weight'], c['characteristic'])
              == (2, 2, 2))['hi1'] == 1, 'minimal F2 witness lost')
    need(all(c['hi1'] == 0 for c in cases if c['characteristic'] == 0),
         'characteristic-zero control failed')
    need(all(c['hi1'] == 0 for c in cases if c['generators'] == 1),
         'single-generator control failed')
    result = {'status': 'PASS', 'scope': 'finite controls, not the universal proof or independent review',
              'dimension_cross_checks': len(cases),
              'witness_checks': len(witnesses),
              'all_degree_argument': 'PROOF.md supplies W_j=0 for j>=2 and all-prime proof',
              'cases': cases, 'witnesses': witnesses}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
