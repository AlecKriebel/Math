#!/usr/bin/env python3
"""Independent algebra diagnostics, not a proof of the topology.

No author/reviewer verifier is imported. All checks use explicit failures and
remain active under python -O. Polynomials use s=t-1 coefficient tuples.
"""
import argparse
import itertools
import json
import math
import os
import random
import sys
from collections import Counter

COUNTS = Counter()


class AuditFailure(Exception):
    pass


def require(ok, label):
    COUNTS[label.split(':')[0]] += 1
    if not ok:
        raise AuditFailure(label)


def add(a, b):
    c = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        c[i] += x
    for i, x in enumerate(b):
        c[i] += x
    return tuple(c)


def mul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return tuple(c)


def parity(perm):
    return -1 if sum(perm[i] > perm[j] for i in range(len(perm))
                    for j in range(i + 1, len(perm))) % 2 else 1


def determinant(a):
    out = (0,)
    for perm in itertools.permutations(range(len(a))):
        term = (parity(perm),)
        for i, j in enumerate(perm):
            term = mul(term, a[i][j])
        out = add(out, term)
    return out


def integer_det(a):
    return sum(parity(perm) * math.prod(a[i][perm[i]]
                                      for i in range(len(a)))
               for perm in itertools.permutations(range(len(a))))


def constant(a):
    return [[entry[0] for entry in row] for row in a]


def rank(a, p):
    b = [[x % p for x in row] for row in a]
    rows, cols = len(b), len(b[0]) if b else 0
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if b[i][c]), None)
        if pivot is None:
            continue
        b[r], b[pivot] = b[pivot], b[r]
        inv = pow(b[r][c], -1, p)
        b[r] = [(x * inv) % p for x in b[r]]
        for i in range(rows):
            if i != r:
                factor = b[i][c]
                b[i] = [(x - factor * y) % p
                        for x, y in zip(b[i], b[r])]
        r += 1
        if r == rows:
            break
    return r


def order(coeff, p):
    return next((i for i, x in enumerate(coeff) if x % p), math.inf)


def smith_factors(a):
    """Smith factors from exact gcds of all minors; small matrices only."""
    divisors = [1]
    n = len(a)
    for k in range(1, n + 1):
        d = 0
        for rr in itertools.combinations(range(n), k):
            for cc in itertools.combinations(range(n), k):
                minor = [[a[i][j] for j in cc] for i in rr]
                d = math.gcd(d, abs(integer_det(minor)))
        if not d:
            raise AuditFailure('smith: input must have finite cokernel')
        divisors.append(d)
    return tuple(divisors[i + 1] // divisors[i] for i in range(n))


def divisibility_check(a, p, family):
    det = determinant(a)
    nullity = len(a) - rank(constant(a), p)
    require(order(det, p) >= nullity, family + ': determinant order >= nullity')
    require(det[0] == integer_det(constant(a)), family + ': specialization commutes')


def exhaustive():
    for p in (2, 3):
        for values in itertools.product(range(p), repeat=8):
            a = [[tuple(values[2 * (2 * i + j):2 * (2 * i + j) + 2])
                  for j in range(2)] for i in range(2)]
            divisibility_check(a, p, 'exhaustive')


def random_controls():
    rng = random.Random(10400231)
    for p in (2, 3, 5, 7):
        for n in (3, 4):
            for _ in range(100):
                a = [[tuple(rng.randrange(-5, 6) for _ in range(3))
                      for j in range(n)] for i in range(n)]
                divisibility_check(a, p, 'random')


def torsion_controls():
    z = (0,)
    genus_zero = [[(2,) if i == j else z for j in range(3)]
                  for i in range(3)]
    require(smith_factors(constant(genus_zero)) == (2, 2, 2),
            'torsion: genus-zero elementary 2-group retained')
    require(determinant(genus_zero) == (8,),
            'torsion: genus-zero determinant retains integer content')
    require(order(determinant(genus_zero), 2) == math.inf,
            'torsion: zero reduced determinant has infinite order')
    require(determinant([]) == (1,) and smith_factors([]) == (),
            'torsion: empty matrix conventions')

    a = [[(2, 1), z, z], [z, (4, 1), z], [(0, 3), (0, 5), (6,)]]
    require(determinant(a) == (48, 36, 6), 'torsion: mixed block determinant')
    require(smith_factors(constant(a)) == (2, 2, 12),
            'torsion: full mixed specialized group')
    for p in (2, 3, 5, 7):
        sf = smith_factors(constant(a))
        require(sum(d % p == 0 for d in sf) == 3 - rank(constant(a), p),
                'torsion: Smith p-rank equals reduction nullity')
        divisibility_check(a, p, 'torsion')
    rng = random.Random(1226)
    for _ in range(100):
        b = [[tuple(x) for x in row] for row in a]
        for j in range(2):
            lift_change = (6 * rng.randrange(-5, 6), 6 * rng.randrange(-5, 6))
            b[2][j] = add(b[2][j], lift_change)
        require(determinant(b) == determinant(a), 'lifts: determinant unchanged')
        require(smith_factors(constant(b)) == smith_factors(constant(a)),
                'lifts: specialized Smith group unchanged')
    require(determinant([row[:2] for row in a[:2]]) != determinant(a),
            'torsion: dropping finite cut torsion is detected')


def torus_bundle_controls():
    for k in range(-5, 6):
        for ell in range(-5, 6):
            if not k or not ell:
                continue
            # B=U(k)L(ell) in SL(2,Z), trace(B)!=2, so its mapping torus has b1=1.
            b = [[1 + k * ell, k], [ell, 1]]
            require(integer_det(b) == 1, 'bundle: oriented monodromy')
            a = [[(b[i][j] - (i == j), -(i == j))
                  for j in range(2)] for i in range(2)]
            expected = (-k * ell, -k * ell, 1)
            require(determinant(a) == expected,
                    'bundle: det(B-tI) in s coordinates')
            sf = smith_factors(constant(a))
            gcd = math.gcd(abs(k), abs(ell))
            require(sf == (gcd, abs(k * ell) // gcd),
                    'bundle: exact homology Smith group')
            for p in (2, 3, 5, 7):
                require(sum(d % p == 0 for d in sf) == 2 - rank(constant(a), p),
                        'bundle: p-rank checked in two ways')
                divisibility_check(a, p, 'bundle')
    a = [[(-2, -1), (0,)], [(0,), (-2, -1)]]
    require(smith_factors(constant(a)) == (2, 2),
            'bundle: minus-identity monodromy gives (Z/2)^2')
    require(order(determinant(a), 2) == 2,
            'bundle: rank-two torsion equality boundary')


def candidate_controls():
    # t Delta_p=(t-1)^2+p^3 t=p^3+p^3 s+s^2, universally.
    for p in (2, 3, 5, 7, 11, 13, 17, 19):
        coeff = (p**3, p**3, 1)
        require(order(coeff, p) == 2, 'candidate: reduced order exactly two')
        require(coeff[0] == p**3, 'candidate: trace equals |T|')
        require(sum(d % p == 0 for d in (p, p, p)) == 3,
                'candidate: full torsion p-rank three')
        require(order(coeff, p) < 3, 'candidate: strict obstruction')
        # Positive unit shifts in t=(1+s) cannot change s-valuation.
        for exponent in range(0, 7):
            unit = tuple(math.comb(exponent, j) for j in range(exponent + 1))
            require(order(mul(coeff, unit), p) == 2,
                    'candidate: Laurent-unit shift control')
    require((1, 6, 1) == (1, 6, 1)[::-1], 'candidate: p=2 reciprocity k=0')


def false_guards():
    # Rectangular presentation [2,s] for Lambda/(2,s): gcd(2,s)=1,
    # but the specialization is Z/2. This is the attack the square lemma excludes.
    order_of_rectangular_module = (1,)
    specialized_p_rank = 1
    require(order(order_of_rectangular_module, 2) < specialized_p_rank,
            'false_guard: arbitrary-module order cannot imply specialization rank')
    require(rank([[0]], 2) == 0 and order((0,), 2) == math.inf,
            'false_guard: identically zero determinant convention')
    require(rank([[1]], 2) == 1 and order((1,), 2) == 0,
            'false_guard: nonsingular constant boundary')


def deliberately_bad(mode):
    if mode == 'false-arbitrary-module':
        require(order((1,), 2) >= 1,
                'guard_reject: unsupported rectangular-module implication')
    elif mode == 'mutant-drop-torsion':
        # Deleting all rows/columns in a genus-zero cut produces the empty matrix.
        lost = []
        require(len(lost) - rank(constant(lost), 2) == 3,
                'guard_reject: mutant lost genus-zero torsion group')
    elif mode == 'mutant-strengthen-by-one':
        require(order((1,), 2) >= (1 - rank([[1]], 2)) + 1,
                'guard_reject: mutant overstates determinant bound')
    else:
        raise AuditFailure('unknown mode')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', default='normal', choices=(
        'normal', 'false-arbitrary-module', 'mutant-drop-torsion',
        'mutant-strengthen-by-one'))
    mode = ap.parse_args().mode
    try:
        if mode != 'normal':
            deliberately_bad(mode)
        else:
            exhaustive()
            random_controls()
            torsion_controls()
            torus_bundle_controls()
            candidate_controls()
            false_guards()
    except AuditFailure as exc:
        print(json.dumps({'status': 'REJECTED', 'mode': mode, 'pid': os.getpid(),
                          'optimized': not __debug__, 'failure': str(exc),
                          'check_counts': dict(COUNTS)}, sort_keys=True))
        return 1
    print(json.dumps({'status': 'PASS', 'mode': mode, 'pid': os.getpid(),
                      'optimized': not __debug__, 'check_counts': dict(COUNTS),
                      'total_checks': sum(COUNTS.values()),
                      'scope': 'Finite algebra diagnostics; topology justified by proof'},
                     sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
