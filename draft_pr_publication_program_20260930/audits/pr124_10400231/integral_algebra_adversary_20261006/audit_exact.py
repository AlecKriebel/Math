"""Exact finite checks. No topology is computationally certified.

All checks are explicit exceptions, so python -O cannot disable them.
Polynomials are sparse Laurent dictionaries over the integers.
"""
import argparse
from itertools import combinations, permutations, product
import json
from math import comb, gcd
import random
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--mutant', choices=['order_one', 'zero_order_zero', 'empty_det_zero', 'primitive_content', 'drop_torsion', 'remove_tminus1', 'valuation_as_nullity', 'rectangular_as_square'])
args = parser.parse_args()
MUTANT = args.mutant
CHECKS = 0
MATRIX_CASES = 0

class AuditFailure(Exception):
    pass

def ck(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AuditFailure(label)

def trim(a):
    return {e: c for e, c in a.items() if c}

def add(a, b):
    c = dict(a)
    for e, v in b.items():
        c[e] = c.get(e, 0) + v
    return trim(c)

def scale(a, c):
    return trim({e: c * v for e, v in a.items()})

def mul(a, b):
    c = {}
    for e, v in a.items():
        for f, w in b.items():
            c[e + f] = c.get(e + f, 0) + v * w
    return trim(c)

def shift(a, k):
    return {e + k: v for e, v in a.items()}

def power(a, n):
    c = {0: 1}
    for _ in range(n):
        c = mul(c, a)
    return c

ONE = {0: 1}
ZERO = {}
X = {0: -1, 1: 1}

def integer_det(a):
    n = len(a)
    out = 0
    for perm in permutations(range(n)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = sign
        for i in range(n):
            term *= a[i][perm[i]]
        out += term
    return out

def determinant(a, torsion_block=False):
    n = len(a)
    if n == 0 and MUTANT == 'empty_det_zero':
        return {}
    if torsion_block and MUTANT == 'drop_torsion':
        a = [[entry for entry in row[:-1]] for row in a[:-1]]
        n -= 1
    out = {}
    for perm in permutations(range(n)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = {0: sign}
        for i in range(n):
            term = mul(term, a[i][perm[i]])
        out = add(out, term)
    if MUTANT == 'primitive_content' and out:
        content = 0
        for c in out.values():
            content = gcd(content, abs(c))
        out = {e: c // content for e, c in out.items()}
    return out

def order_at_one(a, p):
    reduced = trim({e: c % p for e, c in a.items()})
    if not reduced:
        return 0 if MUTANT == 'zero_order_zero' else None
    low, high = min(reduced), max(reduced)
    for k in range(high - low + 1):
        coefficient = sum(v * comb(e - low, k) for e, v in reduced.items() if e - low >= k) % p
        if coefficient:
            if MUTANT == 'order_one' and k > 1:
                return 1
            if MUTANT == 'remove_tminus1' and k > 0:
                return k - 1
            return k
    raise AuditFailure('nonzero polynomial had no Taylor coefficient')

def rank_mod_p(a, p, columns=None):
    b = [list(row) for row in a]
    rows = len(b)
    cols = len(b[0]) if rows else (columns or 0)
    r = 0
    for j in range(cols):
        pivot = next((k for k in range(r, rows) if b[k][j] % p), None)
        if pivot is None:
            continue
        b[r], b[pivot] = b[pivot], b[r]
        inverse = pow(b[r][j] % p, -1, p)
        b[r] = [(v * inverse) % p for v in b[r]]
        for k in range(rows):
            if k != r:
                factor = b[k][j] % p
                b[k] = [(v - factor * w) % p for v, w in zip(b[k], b[r])]
        r += 1
        if r == rows:
            break
    return r

def nullity(a, p):
    n = len(a)
    if MUTANT == 'valuation_as_nullity':
        d = abs(integer_det(a))
        if d:
            v = 0
            while d % p == 0:
                d //= p
                v += 1
            return v
    return n - rank_mod_p(a, p)

def presentation_bound_status(a, p, d):
    """The determinant bound has a square-domain guard, not a gcd-domain guard."""
    n = len(a)
    if any(len(row) != n for row in a) and MUTANT != 'rectangular_as_square':
        return 'OUTSIDE_SQUARE_HYPOTHESIS'
    evaluated = [[sum(entry.values()) for entry in row] for row in a]
    r = n - rank_mod_p(evaluated, p)
    order = order_at_one(d, p)
    return 'VALID_BOUND' if order is None or order >= r else 'BOUND_FAIL'

def smith_finite(a):
    n = len(a)
    previous = 1
    answer = []
    for k in range(1, n + 1):
        divisor = 0
        for rows in combinations(range(n), k):
            for cols in combinations(range(n), k):
                divisor = gcd(divisor, abs(integer_det([[a[i][j] for j in cols] for i in rows])))
        if divisor == 0:
            raise AuditFailure('smith_finite called for a nonfinite cokernel')
        ck(divisor % previous == 0, 'Smith divisor divisibility')
        invariant = divisor // previous
        if invariant > 1:
            answer.append(invariant)
        previous = divisor
    return answer

def square_case(a, p):
    global MATRIX_CASES
    n = len(a)
    ck(all(len(row) == n for row in a), 'genuine square presentation required')
    evaluated = [[sum(entry.values()) for entry in row] for row in a]
    d = determinant(a)
    ck(sum(d.values()) == integer_det(evaluated), 'determinant augmentation agrees')
    order = order_at_one(d, p)
    r = nullity(evaluated, p)
    ck(order is None or order >= r, 'square determinant/nullity bound')
    MATRIX_CASES += 1
    return d, r, order

def main():
    # Edge conventions and derivative-free multiplicity checks.
    ck(determinant([]) == ONE, 'empty determinant must be one')
    ck(order_at_one({}, 2) is None, 'zero reduced polynomial has infinite order')
    square_case([], 2)
    square_case([[ONE, ZERO], [ZERO, ZERO]], 2)
    d, r, o = square_case([[X, ZERO], [ZERO, X]], 2)
    ck((r, o) == (2, 2), 'two uncancelled t-1 factors')
    for p in [2, 3, 5, 7, 11, 13]:
        ck(order_at_one(power(X, p), p) == p, 'Hasse multiplicity in characteristic p')

    candidates = []
    for p in [2, 3, 5, 7, 11, 13]:
        delta = {-1: 1, 0: p**3 - 2, 1: 1}
        ck(sum(delta.values()) == p**3, 'candidate augmentation')
        ck({-e: c for e, c in delta.items()} == delta, 'candidate reciprocity')
        ck(shift(delta, 1) == add(power(X, 2), {1: p**3}), 'candidate exact identity')
        ck(order_at_one(delta, p) == 2, 'candidate order exactly two, including p=2')
        ck(nullity([[p, 0, 0], [0, p, 0], [0, 0, p]], p) == 3, 'elementary torsion p-rank three')
        ck(nullity([[p**3]], p) == 1, 'cyclic p-cubed group p-rank one')
        ck(nullity([[p, 0], [0, p**2]], p) == 2, 'mixed group p-rank two')
        for sign, k, inversion in product([-1, 1], range(-9, 10), [False, True]):
            unit_delta = scale(shift({(-e if inversion else e): c for e, c in delta.items()}, k), sign)
            ck(order_at_one(unit_delta, p) == 2, 'Laurent unit or inversion changes no multiplicity')

        one = [[delta]]
        two = [[{0: p}, X], [scale(shift(X, -1), -1), {0: p**2}]]
        ck(determinant(one) == delta, 'cyclic realization determinant')
        ck(determinant(two) == delta, 'mixed realization determinant')
        ck(smith_finite([[p**3]]) == [p**3], 'cyclic exact specialization')
        ck(smith_finite([[p, 0], [0, p**2]]) == [p, p**2], 'mixed exact specialization')
        square_case(one, p)
        square_case(two, p)
        # Torsion-block columns matter. Lower rows alter the group even at fixed determinant.
        for c, expected in [(0, [p, p**2]), (1, [p**3]), (1 + 3*p, [p**3])]:
            a = [[ONE, ZERO, ZERO], [ZERO, {0: p**2}, ZERO], [ZERO, {0: c}, {0: p}]]
            ck(determinant(a, torsion_block=True) == {0: p**3}, 'retain the torsion relation column')
            ck(smith_finite([[1, 0, 0], [0, p**2, 0], [0, c, p]]) == expected, 'torsion coordinate and legal lift controls')
            square_case(a, p)
        ck(determinant([[{0: p}, ZERO], [ZERO, {0: p}]]) == {0: p**2}, 'integer content is retained')
        # Rectangular module R/(p,t-1): gcd order 1, specialization Z/p.
        ck(rank_mod_p([[p, 0]], p) == 0, 'rectangular specialization p-rank one')
        ck(p % p == 0 and sum(X.values()) % p == 0 and 1 % p == 1, 'rectangular fitting ideal proper under evaluation')
        claimed_rectangular_bound = (order_at_one(ONE, p) >= 1)
        ck(not claimed_rectangular_bound, 'gcd order cannot imply specialization bound')
        ck(presentation_bound_status([[{0: p}, X]], p, ONE) == 'OUTSIDE_SQUARE_HYPOTHESIS', 'rectangular gcd must not be promoted to square presentation')
        candidates.append({'p': p, 'augmentation': p**3, 'target_p_rank': 3, 'mod_p_order': 2, 'singleton_specialization': [p**3], 'two_by_two_specialization': [p, p**2]})

    # Exhaustive independent small-field family with Laurent entries a*t^-1+b*t.
    for entries in product(range(4), repeat=4):
        a = [[{-1: entries[2*i+j] & 1, 1: (entries[2*i+j] >> 1) & 1} for j in range(2)] for i in range(2)]
        square_case(a, 2)
    # Seeded exact integer Laurent cases, plus rank-deficient specializations.
    rng = random.Random(10400231)
    for p in [2, 3, 5, 7]:
        for n in range(1, 5):
            for rep in range(24):
                a = [[trim({e: rng.randrange(-3, 4) for e in [-1, 0, 1]}) for j in range(n)] for i in range(n)]
                if rep % 2 == 0:
                    for i in range(rep % n, n):
                        for j in range(n):
                            entry = a[i][j]
                            entry[0] = -entry.get(-1, 0) - entry.get(1, 0)
                d, r, o = square_case(a, p)
                if n > 1:
                    b = [[dict(entry) for entry in row] for row in a]
                    b[0] = [add(x, scale(y, 2)) for x, y in zip(a[0], a[1])]
                    ck(determinant(b) == d, 'unimodular row-addition determinant')
                b = [[dict(entry) for entry in row] for row in a]
                b[0] = [shift(entry, -3) for entry in b[0]]
                ck(determinant(b) == shift(d, -3), 'Laurent row-unit determinant')

    print(json.dumps({'status': 'PASS', 'explicit_checks': CHECKS, 'matrix_cases': MATRIX_CASES, 'candidate_primes': candidates, 'seed': 10400231, 'scope': 'Exact algebraic controls only; no topological or novelty certification.'}, sort_keys=True))

try:
    main()
except AuditFailure as error:
    print(json.dumps({'status': 'REJECTED', 'mutant': MUTANT, 'check_number': CHECKS, 'reason': str(error)}, sort_keys=True))
    sys.exit(1)
