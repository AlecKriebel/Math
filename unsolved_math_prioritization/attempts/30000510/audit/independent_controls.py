#!/usr/bin/env python3
"""Independent rational controls for the singular-scope audit; no external inputs.
These controls supplement, and do not prove, the universal topology statements.
"""
from fractions import Fraction as Q
from itertools import permutations, product
from collections import Counter
import json

INF = None
ALPHABET = [INF, Q(-3), Q(-1), Q(0), Q(1, 2), Q(1), Q(4)]
MATRICES = [(1, 0, 0, 1), (1, 1, 0, 1), (0, -1, 1, 0),
            (2, 1, 1, 1), (3, 2, 1, 1), (1, 0, -2, 1)]

def det(m):
    a, b, c, d = m
    return a*d-b*c

def act(m, x):
    a, b, c, d = map(Q, m)
    u, v = (a, c) if x is INF else (a*x+b, c*x+d)
    assert (u, v) != (0, 0)
    return INF if v == 0 else u/v

def inverse(m):
    a, b, c, d = m
    assert det(m) != 0
    return (d, -b, -c, a)

def normalize_pair(x, y):
    assert x != y
    a, c = (Q(1), Q(0)) if x is INF else (x, Q(1))
    b, d = (Q(1), Q(0)) if y is INF else (y, Q(1))
    if a*d-b*c < 0:
        b, d = -b, -d
    g = (a, b, c, d)
    assert det(g) > 0
    h = inverse(g)
    assert act(h, x) is INF and act(h, y) == 0
    return h

def normalize_three(points):
    h = normalize_pair(points[0], points[1])
    xs = [act(h, x) for x in points]
    i = next(i for i in range(2, len(xs)) if xs[i] is not INF and xs[i] != 0)
    r = abs(xs[i])
    return [INF if x is INF else x/r for x in xs]

def cyclic_key(x):
    return (0, 0) if x is INF else (1, -x)

def wind(xs):
    return sum(cyclic_key(xs[(i+1) % len(xs)]) < cyclic_key(xs[i])
               for i in range(len(xs)))

def main():
    triples = orbit_checks = positive_dilation_checks = 0
    for t in permutations(ALPHABET, 3):
        z = normalize_three(t)
        assert z[0] is INF and z[1] == 0 and z[2] in (-1, 1)
        triples += 1
        for h in MATRICES:
            assert det(h) > 0
            ht = [act(h, x) for x in t]
            assert normalize_three(ht) == z
            assert wind(ht) == wind(t)
            orbit_checks += 1
        for r in [Q(1, 9), Q(1, 2), Q(2), Q(13)]:
            rt = [INF if x is INF else r*x for x in t]
            assert normalize_three(rt) == z
            positive_dilation_checks += 1

    # Exhaust all cyclic order words without importing the author's partition code.
    counts = {}
    for n in range(3, 7):
        c = Counter()
        for m in range(3, n+1):
            for tail in product(range(m), repeat=n-1):
                w = (0,) + tail
                if set(w) != set(range(m)):
                    continue
                if any(w[i] == w[(i+1) % n] for i in range(n)):
                    continue
                k = sum(w[(i+1) % n] < w[i] for i in range(n))
                c[k] += 1
        assert set(c) == set(range(1, n))
        counts[str(n)] = {str(k):c[k] for k in sorted(c)}
    assert counts['3'] == {'1': 1, '2': 1}
    assert counts['4'] == {'1': 1, '2': 8, '3': 1}

    # Every binary word, including inadmissible inputs, tests the exact exclusion.
    binary_words = admissible_binary = 0
    for n in range(1, 13):
        for w in product((0, 1), repeat=n):
            adjacent = all(w[i] != w[(i+1) % n] for i in range(n))
            alternating = n % 2 == 0 and all(w[i] == (w[0]+i) % 2 for i in range(n))
            assert adjacent == alternating
            binary_words += 1
            if adjacent:
                assert sum(w[(i+1) % n] < w[i] for i in range(n)) == n//2
                admissible_binary += 1

    radial_checks = 0
    for n in range(4, 42, 2):
        # Multiple zero entries and near-boundary radii test the domain constraints.
        for j in range(1, n-1):
            for radius in [Q(1, 1000000), Q(1, 4), Q(499999, 1000000)]:
                v = [Q(0)]*n
                v[j], v[-1] = radius, -radius
                for t in [Q(0), Q(1, 100), Q(1, 2), Q(99, 100), Q(1)]:
                    w = [((1-t)+t/(4*radius))*a for a in v]
                    assert w[0] == 0 and sum(w) == 0
                    assert 0 < max(map(abs, w)) < Q(1, 2)
                    if t == 1: assert max(map(abs, w)) == Q(1, 4)
                    if radius == Q(1, 4): assert w == v
                    radial_checks += 1

    return {'scope':'Independent exact finite controls only; not a universal proof.',
            'normalized_distinct_triples':triples,
            'projective_orbit_and_winding_checks':orbit_checks,
            'dilation_normalization_checks':positive_dilation_checks,
            'cyclic_types_by_winding':counts,
            'binary_words_examined':binary_words,
            'adjacent_distinct_binary_words':admissible_binary,
            'near_boundary_radial_checks':radial_checks,
            'arithmetic':'fractions.Fraction and integers',
            'all_assertions_passed':True}

if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
