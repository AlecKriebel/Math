#!/usr/bin/env python3
"""Exact arithmetic/model controls. Infinite theorems are proved in PROOF.md.

No assertion below certifies general Borel smoothness, non-smoothness, perfectness,
or fusion. The tests check finite arithmetic and exact eventually-periodic models.
"""
from fractions import Fraction as F
from itertools import product
from math import lcm
import json


def main():
    checks = {}
    def check(group, condition):
        if not condition:
            raise AssertionError(group)
        checks[group] = checks.get(group, 0) + 1

    # Compact finite action analog: x -> -x. Closed-class distance fingerprints.
    xs = [F(k, 2) for k in range(-8, 9)]
    probes = xs
    def orbit(x): return frozenset((x, -x))
    def fingerprint(x):
        return tuple(min(abs(a-z) for z in orbit(x)) for a in probes)
    for x, y in product(xs, repeat=2):
        check('closed_class_fingerprints', (fingerprint(x) == fingerprint(y)) == (abs(x) == abs(y)))

    # Repeated-bit code has infinitely many occurrences of each input bit.
    # The proof of the infinite claim is the repetition formula, not a cutoff.
    for length in range(1, 7):
        words = list(product((0, 1), repeat=length))
        for a, b in product(words, repeat=2):
            differing = [i for i in range(length) if a[i] != b[i]]
            for block in (0, 1, 17):
                mismatch = [block*length+i for i in range(length)
                            if a[(block*length+i) % length] != b[(block*length+i) % length]]
                check('periodic_repeat_code', mismatch == [block*length+i for i in differing])
            check('periodic_repeat_code', bool(differing) == (a != b))

    # A closed-class one-orbit box for weight 2^n, delta=2^(-2(n+1)).
    # Infinite bound is evaluated as an exact geometric series.
    budgets = {}
    for p in (1, 2, 3, 4):
        ratio = F(2) ** (1-2*p)
        total = (F(2) ** (-2*p)) / (1-ratio)
        budgets[str(p)] = str(total)
        for dim in range(1, 7):
            deltas = [F(1, 2**(2*(n+1))) for n in range(dim)]
            vertices = [tuple(bit*d for bit,d in zip(bits,deltas))
                        for bits in product((0,1), repeat=dim)]
            maximum = F(0)
            for x,y in product(vertices, repeat=2):
                cost = sum((F(2**n)*abs(x[n]-y[n])**p for n in range(dim)), F(0))
                check('weighted_box_vertices', cost <= total)
                maximum = max(maximum, cost)
            exact_partial = total*(1-ratio**dim)
            check('weighted_box_geometric_sum', maximum == exact_partial)
            check('weighted_box_geometric_sum', total-exact_partial == total*ratio**dim)

    # Exactly represented infinite eventually-periodic bit sequences.
    # E0 depends only on aligned periodic tails, not a sampled prefix.
    sequences = []
    for prefix_len in range(3):
        for prefix in product((0,1), repeat=prefix_len):
            for period_len in (1,2):
                for period in product((0,1), repeat=period_len):
                    sequences.append((prefix,period))
    def bit(s,n):
        prefix,period=s
        return prefix[n] if n < len(prefix) else period[(n-len(prefix)) % len(period)]
    def eventual_equal(a,b):
        start=max(len(a[0]),len(b[0]))
        period=lcm(len(a[1]),len(b[1]))
        return all(bit(a,n)==bit(b,n) for n in range(start,start+period))
    for a,b in product(sequences, repeat=2):
        start=max(len(a[0]),len(b[0]))
        period=lcm(len(a[1]),len(b[1]))
        # Coordinate injection n -> 2n + b(n), matching Proposition 4.
        mapped=all(2*n+bit(a,n)==2*n+bit(b,n) for n in range(start,start+period))
        check('eventual_periodic_E0_to_E1', mapped == eventual_equal(a,b))
        check('eventual_periodic_E0_to_E1', eventual_equal(a,b) == eventual_equal(b,a))
    zero=((),(0,))
    one=((),(1,))
    check('tail_negative_controls', not eventual_equal(zero,one))
    for n in range(1,33):
        finite_ones=((1,)*n,(0,))
        delayed_periodic=((0,)*n,(0,1))
        check('tail_negative_controls', eventual_equal(zero,finite_ones))
        check('tail_negative_controls', not eventual_equal(zero,delayed_periodic))
        check('tail_negative_controls', all(bit(finite_ones,k)==bit(one,k) for k in range(n)))
        check('tail_negative_controls', all(bit(delayed_periodic,k)==bit(zero,k) for k in range(n)))

    # Nondegenerate finite rectangles already fail containment in a diagonal.
    sets=[{0,1},{1,2},{0,2},{0,1,2}]
    for A,B in product(sets, repeat=2):
        check('diagonal_rectangle_negative_control', any(a != b for a,b in product(A,B)))
    for x in product(range(3),repeat=3):
        image=(x[0],x[0],x[1],x[2])
        check('duplication_pullback_negative_control', not(image[0] in {0} and image[1] in {1}))

    # Naked nested cylinders can converge to a singleton if splitting is not preserved.
    # These tests check the exact finite-prefix obstruction; the limit is in the proof.
    for n in range(1,13):
        candidates=list(product((0,1), repeat=n))
        survivors=[s for s in candidates if all(v==0 for v in s)]
        check('unprotected_fusion_negative_control', survivors == [(0,)*n])

    return {
        'result':'PASS_EXPLICIT_CONTROLS_ONLY',
        'total_assertions':sum(checks.values()),
        'groups':checks,
        'weighted_box_infinite_bounds':budgets,
        'limitations':[
            'Finite and eventually-periodic controls do not prove the infinite Baire/fusion arguments.',
            'No general solution, qualifying counterexample, formal proof certificate, or literature-priority check is produced.',
            'E1 is a proof-method negative control excluded by the source orbit-reducibility hypothesis.'
        ]
    }

if __name__ == '__main__':
    print(json.dumps(main(),indent=2,sort_keys=True))
