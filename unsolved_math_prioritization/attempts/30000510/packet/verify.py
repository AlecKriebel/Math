#!/usr/bin/env python3
"""Deterministic exact finite controls; not a universal topology proof.

No network, third-party imports, downloaded code or filesystem writes.
"""
from fractions import Fraction as F
from itertools import permutations
from collections import Counter
import json


def partitions(n):
    """Restricted-growth encodings of all set partitions, fixing label of 0."""
    def rec(w, largest):
        if len(w) == n:
            yield tuple(w)
        else:
            for j in range(largest + 2):
                yield from rec(w + [j], max(largest, j))
    yield from rec([0], 0)


def cyclic_types(n):
    """All surjective cyclic order types, with value at vertex 0 labelled 0."""
    for w in partitions(n):
        m = max(w) + 1
        if m < 3 or any(w[i] == w[(i+1) % n] for i in range(n)):
            continue
        for p in permutations(range(1, m)):
            rename = (0,) + p
            yield tuple(rename[j] for j in w)


def key(x):
    # Positive order in omega([cos(pi*t):sin(pi*t)]): infinity, decreasing reals.
    return (0, F(0)) if x is None else (1, -x)


def winding(points):
    assert all(points[i] != points[(i+1) % len(points)] for i in range(len(points)))
    return sum(key(points[(i+1) % len(points)]) < key(points[i])
               for i in range(len(points)))


def mobius(point, matrix):
    a, b, c, d = map(F, matrix)
    assert a*d-b*c == 1
    num, den = (a, c) if point is None else (a*point+b, c*point+d)
    return None if den == 0 else num/den


def angle_points(increments):
    p = [F(0)]
    for a in increments[:-1]:
        p.append((p[-1]+a) % 1)
    assert sum(increments).denominator == 1
    assert all(0 < a < 1 for a in increments)
    return p


def main():
    matrices = [(1,0,0,1), (1,1,0,1), (0,-1,1,0),
                (2,1,1,1), (1,0,1,1), (1,-2,0,1)]
    type_counts = {}
    matrix_tests = reflection_tests = 0
    for n in range(3, 7):
        counts = Counter()
        seen = set()
        for w in cyclic_types(n):
            assert w not in seen
            seen.add(w)
            m = max(w)+1
            # All m values occur in positive cyclic order.
            alphabet = [None] + [F(m-1-j) for j in range(1, m)]
            pts = [alphabet[j] for j in w]
            k = winding(pts)
            assert 1 <= k <= n-1
            counts[k] += 1
            for matrix in matrices:
                transformed = [mobius(x, matrix) for x in pts]
                assert winding(transformed) == k
                assert len(set(transformed)) == m
                matrix_tests += 1
            reflected = [None if x is None else -x for x in pts]
            assert winding(reflected) == n-k
            reflection_tests += 1
        assert set(counts) == set(range(1, n))
        type_counts[str(n)] = {str(k): counts[k] for k in sorted(counts)}

    # Construct one admissible exact angular slice point for every claimed level.
    slice_tests = 0
    for n in range(3, 21):
        for k in range(1, n):
            a = [F(1,2)] + [F(2*k-1, 2*(n-1))]*(n-1)
            if 2*k == n:
                a[1] += F(1,8)
                a[2] -= F(1,8)
            pts = angle_points(a)
            assert len(set(pts)) >= 3
            assert sum(pts[(i+1)%n] < pts[i] for i in range(n)) == k
            assert a[0] == F(1,2) and sum(a) == k
            slice_tests += 1

    # The two-value locus is precisely alternating, with middle winding.
    alternating_tests = 0
    for n in range(4, 22, 2):
        for t in [F(1,7), F(1,3), F(1,2), F(4,5)]:
            a = [t, 1-t]*(n//2)
            assert len(set(angle_points(a))) == 2
            assert sum(a) == n//2
            assert (a[0] == F(1,2)) == (len(set(a)) == 1)
            alternating_tests += 1

    # Exact rational evaluations of the uniform sup-norm deformation.
    radial_tests = stationary_tests = 0
    times = [F(0), F(1,7), F(1,2), F(6,7), F(1)]
    for n in range(4, 32, 2):
        for seed in range(1, 11):
            raw = [F(0)] + [F(((j+3)*seed+j*j) % 17 - 8) for j in range(1, n-1)]
            raw.append(-sum(raw))
            raw_norm = max(map(abs, raw))
            assert raw_norm > 0 and len(raw) == n and sum(raw) == 0
            for radius in [F(1,8), F(1,4), F(3,8), F(15,32)]:
                v = [x*radius/raw_norm for x in raw]
                M = max(map(abs, v))
                for t in times:
                    w = [((1-t)+t/(4*M))*x for x in v]
                    a = [F(1,2)+x for x in w]
                    assert a[0] == F(1,2) and sum(a) == n//2
                    assert all(0 < x < 1 for x in a)
                    assert max(map(abs, w)) > 0
                    assert len(set(angle_points(a))) >= 3
                    if t == 1:
                        assert max(map(abs, w)) == F(1,4)
                    if M == F(1,4):
                        assert w == v
                        stationary_tests += 1
                    radial_tests += 1

    # A common quotient sequence with distinct admissible limits.
    # Convergence for all m is proved by the formulas in PROOF.md, not inferred here.
    separation_tests = 0
    for n in range(4, 16, 2):
        a = [F(0), F(1)] + [F(0)]*(n//2-2)
        b = [None, F(1)] + [None]*(n//2-2)
        for m in [2,3,5,11]:
            f = sum(([None if x is None else m*m*x, y] for x,y in zip(b,a)), [])
            g = (F(1,m),0,0,F(m))
            transformed = [mobius(x,g) for x in f]
            expected = sum(([x, y/F(m*m)] for x,y in zip(b,a)), [])
            assert transformed == expected and len(set(f)) >= 3
            assert winding(f) == winding(transformed) == n//2
            separation_tests += 1

    # Universal conclusions are recorded for convenient reading, not certified here.
    return {
        "scope": "Exact finite controls only; universal proofs are in PROOF.md.",
        "cyclic_types_by_winding": type_counts,
        "matrix_invariance_tests": matrix_tests,
        "orientation_reversal_tests": reflection_tests,
        "slice_existence_controls": slice_tests,
        "alternating_locus_controls": alternating_tests,
        "radial_deformation_controls": radial_tests,
        "stationary_sphere_controls": stationary_tests,
        "nonhausdorff_sequence_controls": separation_tests,
        "arithmetic": "fractions.Fraction and integer arithmetic only",
        "all_assertions_passed": True,
    }


if __name__ == '__main__':
    print(json.dumps(main(), indent=2, sort_keys=True))
