#!/usr/bin/env python3
"""Exact finite controls for the reconstructed 5000005 candidate.

These controls are supporting evidence, not proofs of the imported Veech facts,
hyperelliptic uniqueness, or the all-n endpoint matching theorem.
"""
from collections import Counter
from fractions import Fraction as F
from math import gcd
import json
from pathlib import Path

counts = Counter()


def check(condition, category, detail=None):
    if not condition:
        raise AssertionError((category, detail))
    counts[category] += 1


def corner(n, s, j):
    """Return (cone number, corner number) for copy s and vertex j."""
    j %= n
    if n % 2:
        t = j if j % 2 == s else j + n
        return 0, t
    return (s + j) % 2, j


def printed_types(n, alpha, beta, copy):
    """Definition2.1, retaining its preceding segment-parity selector."""
    m = n // 2
    answer = []
    for k in range(n - 2):
        if copy == 0:  # odd segment count: sum selector
            eq = alpha + beta == F(2 * (n - k - 1), n)
            if n % 2:
                bounds = ((k <= m - 1 and alpha >= F(n - 2*(k+1), n))
                          or (k >= m and alpha <= F(2*(n-k-2), n)))
            else:
                bounds = ((k <= m - 1 and alpha >= F(m-k-1, m))
                          or (k >= m - 1 and alpha <= F(n-k-2, m)))
        else:  # even segment count: difference selector
            if n % 2:
                bounds = ((k <= m + 1 and alpha <= F(n-2*(k+1), n)
                           and beta-alpha == F(2*(k+1), n))
                          or (k >= m and alpha >= F(2*(n-k-2), n)
                              and beta-alpha == F(2*(k+3-n), n)))
            else:
                bounds = ((k <= m-1 and alpha <= F(m-k-1, m)
                           and beta-alpha == F(k+1, m))
                          or (k >= m-1 and alpha >= F(n-k-2, m)
                              and beta-alpha == F(k+3-n, m)))
            eq = True
        if eq and bounds:
            answer.append(k)
    return answer


def test_cones_and_types():
    for n in range(3, 31):
        N = n-2
        delta = F(N, n)
        cycles = [[(t % 2, t % n) for t in range(2*n)]] if n % 2 else [
            [((t+c) % 2, t) for t in range(n)] for c in range(2)]
        flattened = [p for cycle in cycles for p in cycle]
        check(len(set(flattened)) == 2*n, 'corner_cycle_partition', n)
        for c, cycle in enumerate(cycles):
            for t, (s, j) in enumerate(cycle):
                check(corner(n, s, j) == (c, t), 'corner_coordinates')
                physical_base = t*delta + (c if n % 2 == 0 else 0)
                check((physical_base - (s-F(2*j, n))) % 2 == 0,
                      'physical_corner_direction')
        for sign in [0, 1]:
            labels = [2*j+sign for j in range(N)] if n % 2 else [
                2*j-c+sign for c in range(2) for j in range(N//2)]
            check(set(x % N for x in labels) == set(range(N)), 'label_bijection')
        # Formal corner/end-angle data, not asserted actual long trajectories.
        for u in range(0, 2*N+1):
            alpha = F(u, 2*n)
            for s in range(2):
                for j in range(n):
                    c, t = corner(n, s, j)
                    lower = t*delta
                    cp = c if n % 2 == 0 else 0
                    for shift in range(-2, 2*n+1):
                        phi = alpha+1-cp+2*shift
                        offset = phi-lower
                        if not 0 <= offset <= delta:
                            continue
                        beta = 1-offset if s == 0 else offset+F(2, n)
                        angle_s = n*(alpha+beta)/2 if s == 0 else n*(beta-alpha)/2
                        check(angle_s.denominator == 1, 'angle_integrality')
                        source_k = (n-1-int(angle_s) if s == 0 else int(angle_s)-1) % N
                        b = phi-alpha
                        check(b.denominator == 1, 'integer_germ_label')
                        check(int(b) % N == source_k, 'source_type_equals_label')
                        # At sides the printed representative may be N rather
                        # than 0. Interior samples compare the printed branches.
                        if 0 < alpha < delta and 0 < offset < delta:
                            check(printed_types(n, alpha, beta, s) == [source_k],
                                  'printed_parity_selected_branches',
                                  (n, alpha, beta, s, source_k))
                        ar, br = delta-alpha, 1+F(2,n)-beta
                        sr = n*(ar+br)/2 if s == 0 else n*(br-ar)/2
                        kr = (n-1-int(sr) if s == 0 else int(sr)-1) % N
                        check(kr == -source_k % N, 'bisector_type_reversal')


def test_model_chords():
    for n in range(3, 51):
        N = n-2
        delta = F(N,n)
        matchings = {h: {} for h in range(2*n)}
        for s in range(2):
            for j in range(n):
                c, t = corner(n,s,j)
                for span in range(1,n):
                    jp = (j+span) % n
                    cp, tp = corner(n,s,jp)
                    h = (n*s-2*j+n-1-span) % (2*n)
                    theta = F(h,n)
                    phi_u = t*delta+F(n-1-span,n)
                    phi_v = tp*delta+F(span-1,n)
                    a, b = phi_u-theta, phi_v-theta
                    check(a.denominator == b.denominator == 1, 'model_integer_labels')
                    a,b = int(a)%N,int(b)%N
                    check((a+b+h)%N == 0, 'model_reflection_sum')
                    check((b-a-(span-1))%N == 0, 'model_chord_type')
                    check(a not in matchings[h] or matchings[h][a] == b,
                          'boundary_germ_consistency')
                    matchings[h][a] = b
        for h,pairs in matchings.items():
            check(set(pairs) == set(range(N)), 'all_model_germs_exhausted')
            check(set(pairs.values()) == set(range(N)), 'model_endpoint_bijection')


def test_common_shift_and_alignment():
    for n in range(3,51):
        N = n-2
        for C in range(N):
            for d in range(N):
                for a in range(N):
                    b = (C-a)%N
                    ap,bp = (a+d)%N,(b+d)%N
                    check((bp-ap)%N == (b-a)%N, 'common_shift_type_invariance')
                    check((ap+bp-C-2*d)%N == 0, 'common_shift_reflection_transport')
        for ell in range(-4*n,4*n+1):
            if n%2 == 0 and ell%2:
                continue
            s = ell%2 if n%2 else 0
            j = ((ell+n*s)//2)%n
            c,t = corner(n,s,j)
            a = F(t*N+ell,n)
            check(a.denominator == 1, 'rotation_alignment_integrality')
            check((2*int(a)-ell)%N == 0, 'rotation_alignment_no_division')
        for h in range(N+1):
            k = (N-h)%N
            for hp in range(N+1):
                for eps in [-1,1]:
                    ell = hp-eps*h
                    if n%2 == 0 and ell%2:
                        continue
                    check((N-hp)%N == (eps*k-ell)%N, 'signed_rule_model_boundaries')


def hex_type_primitive(p,q):
    s=(p+q)%3
    if s == 1:return 0
    if s == 2:return 2
    return 1 if (p%3,q%3) == (1,2) else 3


def hex_type_endpoint(p,q):
    if (p%3,q%3) == (1,2):return 1
    if p%2 == q%2 == 0:return 2
    if (p%3,q%3) == (2,1):return 3
    return 0


def test_elementary():
    for p in range(-30,31):
        for q in range(-30,31):
            if gcd(p,q) != 1:continue
            first = next(t for t in range(1,4) if t*(p+q)%3 != 2)
            check(first == (2 if (p+q)%3 == 2 else 1), 'hex_first_marked_vertex')
            k=hex_type_primitive(p,q)
            check(hex_type_endpoint(first*p,first*q) == k, 'hex_source_type')
            rp,rq=p-q,p
            bp,bq=q,p
            check(gcd(rp,rq) == gcd(bp,bq) == 1, 'hex_primitivity')
            check(rp*rp-rp*rq+rq*rq == p*p-p*q+q*q, 'hex_rotation_norm')
            check(hex_type_primitive(rp,rq) == (k-2)%4, 'hex_rotation_type')
            check(hex_type_primitive(bp,bq) == -k%4, 'hex_bisector_type')
            check((p%2 == q%2 == 1) == (q%2 == p%2 == 1), 'square_type_swap')


if __name__ == '__main__':
    test_cones_and_types()
    test_model_chords()
    test_common_shift_and_alignment()
    test_elementary()
    result = {
        'status':'PASS',
        'assertions':sum(counts.values()),
        'counts':dict(sorted(counts.items())),
        'arithmetic':'Python standard-library integers and Fraction; no floating-point assertions',
        'limitations':['Finite controls only; classical Veech facts are imported',
                       'Formal endpoint-angle data are not certificates of actual long trajectories',
                       'No numerical experiment replaces the all-n proof or separate review'],
    }
    output=Path(__file__).with_name('verification.json')
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
