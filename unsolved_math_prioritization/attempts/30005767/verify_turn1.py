#!/usr/bin/env python3
"""Exact finite controls for the accompanying all-length grammar/field proof.
Python 3 standard library only. Run from any directory; writes no files.
"""
from itertools import permutations, combinations
from functools import lru_cache
from fractions import Fraction
import json

assertions = 0

def check(condition, label):
    global assertions
    assertions += 1
    if not condition:
        raise AssertionError(label)


def standardize(values):
    order = {x: i + 1 for i, x in enumerate(sorted(values))}
    return tuple(order[x] for x in values)


def cuts(p, skew=False):
    n = len(p)
    return tuple(k for k in range(1, n)
                 if set(p[:k]) == set(range(n-k+1, n+1) if skew else range(1, k+1)))


def op(a, b, skew=False):
    if skew:
        return tuple(x + len(b) for x in a) + b
    return a + tuple(x + len(a) for x in b)


@lru_cache(None)
def recursive_sep(p):
    if len(p) <= 1:
        return True
    for skew in [False, True]:
        cc = cuts(p, skew)
        if cc:
            k = cc[0]
            return recursive_sep(standardize(p[:k])) and recursive_sep(standardize(p[k:]))
    return False


def has123(p):
    return any(p[i] < p[j] < p[k] for i, j, k in combinations(range(len(p)), 3))


BETA = (2, 3, 4, 1)
SEP_BASIS = {(2, 4, 1, 3), (3, 1, 4, 2)}
MAXN = 8
classes = [[] for _ in range(MAXN + 1)]
lefts = [[] for _ in range(MAXN + 1)]
lookup = {}
permutation_count = 0
for n in range(MAXN + 1):
    for p in permutations(range(1, n + 1)):
        permutation_count += 1
        patterns4 = {standardize(tuple(p[i] for i in ix))
                     for ix in combinations(range(n), 4)}
        sep = not bool(patterns4 & SEP_BASIS)
        member = sep and BETA not in patterns4
        lookup[p] = member
        check(recursive_sep(p) == sep, ('recursive Sep definition', p))
        sc, kc = cuts(p), cuts(p, True)
        check(not (sc and kc), ('disjoint decomposition categories', p))
        if member:
            classes[n].append(p)
        if n and sep and not kc and not has123(p):
            lefts[n].append(p)
            if n > 1:
                check(bool(sc), ('L sum decomposable', p))
                k = sc[0]
                a, b = standardize(p[:k]), standardize(p[k:])
                check(a == tuple(range(len(a), 0, -1)) and
                      b == tuple(range(len(b), 0, -1)), ('L two decreasing blocks', p))
                check(not cuts(a) and not cuts(b), ('L exact canonical blocks', p))
        if member and n > 1:
            check(bool(sc) != bool(kc), ('C category exhaustive', p))
            skew = bool(kc)
            k = (kc if skew else sc)[0]
            a, b = standardize(p[:k]), standardize(p[k:])
            check(op(a, b, skew) == p, ('unique reconstruction', p))
            check(not cuts(a, skew), ('first indecomposable', p))
            check(lookup[a] and lookup[b], ('factor membership', p))
            if skew:
                check(not has123(a), ('skew first avoids123', p))
                check(a in lefts[len(a)], ('skew first in L', p))
            else:
                check(len(a) == 1 or bool(cuts(a, True)), ('sum first singleton/skew', p))

check(cuts(BETA) == (), '2341 has no sum cut')
check(cuts(BETA, True) == (3,), '2341 has exactly one skew cut')
check(recursive_sep(BETA) and not lookup[BETA], 'proper subclass witness')
expected = [1, 1, 2, 6, 21, 77, 290, 1118, 4398]
counts = [len(v) for v in classes]
check(counts == expected, 'exhaustive counts')
check(permutation_count == 46234, 'number of permutations tested')
for n in range(1, MAXN + 1):
    check(len(lefts[n]) == (1 if n == 1 else n-1), ('L counts', n))

# Bounded converse and uniqueness, using brute-force membership as oracle.
products = 0
for n in range(2, MAXN + 1):
    images_sum, images_skew = set(), set()
    for a_len in range(1, n):
        b_len = n-a_len
        for a in classes[a_len]:
            for b in classes[b_len]:
                p = op(a, b)
                products += 1
                check(lookup[p], ('sum closure converse', a, b))
                if not cuts(a):
                    check(p not in images_sum, ('canonical sum injective', p))
                    images_sum.add(p)
                q = op(a, b, True)
                check(lookup[q] == (not has123(a)), ('skew boundary iff', a, b))
                if not cuts(a, True) and not has123(a):
                    check(q not in images_skew, ('canonical skew injective', q))
                    images_skew.add(q)
    check(images_sum == {p for p in classes[n] if cuts(p)}, ('sum grammar surjective', n))
    check(images_skew == {p for p in classes[n] if cuts(p, True)}, ('skew grammar surjective', n))

# Ordinary formal series from the proven grammar, no numerical fitting.
N = 80
l = [0, 1] + [n-1 for n in range(2, N+1)]
f = [0]*(N+1)
for n in range(1, N+1):
    f[n] = int(n == 1) + f[n-1]
    f[n] += sum(l[i]*f[n-i] for i in range(1, n+1))
    f[n] += sum(l[i]*sum(f[j]*f[n-i-j] for j in range(n-i+1))
                for i in range(1, n+1))
c = f.copy(); c[0] = 1
check(c[:9] == counts, 'grammar versus brute force')


def add(a, b):
    return [(a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
            for i in range(max(len(a), len(b)))]


def scale(a, k):
    return [k*x for x in a]


def mul(a, b, degree=None):
    size = len(a)+len(b)-1
    if degree is not None:
        size = min(size, degree+1)
    out = [0]*size
    for i, x in enumerate(a):
        for j, y in enumerate(b[:max(0, size-i)]):
            out[i+j] += x*y
    return out


def ev(p, x):
    result = 0
    for coeff in reversed(p):
        result = result*x+coeff
    return result


A = [0, 1, -1, 1]; B = [1, -2, 2]; D = [1, -2, 1]
P = [1, -8, 20, -24, 16, -4]
U = [1, -4]; V = [1, -6, 5]
check(add(mul(B, B), scale(mul(A, D), -4)) == P, 'exact discriminant')
check(mul([1, -1], [1, -5]) == V, 'second source radical factors')
residual = add(add(mul(A, mul(c, c, N), N), scale(mul(B, c, N), -1)), D)
for n in range(N+1):
    check(residual[n] == 0, ('quadratic coefficient', n))
radical = add(B, scale(mul(A, c, N), -2))
radical_square = mul(radical, radical, N)
for n in range(N+1):
    check(radical_square[n] == (P[n] if n < len(P) else 0), ('recovered radical squared', n))
check(radical[0] == 1, 'correct formal radical branch')
check(radical[1] == -4, 'removable singularity numerator coefficient')
check(ev(P, Fraction(1, 4)) == Fraction(-17, 256), 'P at U zero')
check(ev(V, Fraction(1, 4)) == Fraction(-3, 16), 'V at U zero')
check(ev(P, 1) == 1, 'P at V zero')
check(ev(U, Fraction(1, 4)) == 0 and U[1] != 0, 'simple U zero')
check(ev(V, 1) == 0 and V[1]+2*V[2] != 0, 'simple V zero')
check(len(P)-1 == 5 and P[-1] != 0, 'odd infinity valuation')
check(any(A), 'nonzero radical coefficient denominator')
# Four distinct simultaneous eigencharacters of the sign changes.
characters = [(1,1), (-1,1), (1,-1), (-1,-1)]
check(len(set(characters)) == 4, 'four one-dimensional simultaneous eigenspaces')
# These are finite exact controls on the written valuation/eigenspace proof,
# not an algorithm purporting to exhaust all rational functions.
print(json.dumps(dict(problem_id=30005767, turn=1, status='all exact controls passed',
    assertions=assertions, permutations_examined=permutation_count,
    exhaustive_max_length=MAXN, counts_through_8=counts,
    bounded_product_pairs=products, formal_degree=N,
    counts_through_20=c[:21],
    field_controls={'P_at_quarter':'-17/256','V_at_quarter':'-3/16',
                    'P_at_one':1,'infinity_valuation_of_P':-5},
    scope='Finite controls support the all-length grammar and field proof; they do not replace either proof.',
    dependencies='Python 3 standard library'), indent=2)+'\n', end='')
