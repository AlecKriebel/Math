#!/usr/bin/env python3
"""Supported adaptation of /root/pr445_reproduction exact_controls.py.

The finite mathematical logic is preserved; the CLI became a return-value API.
Original source SHA256: 8f10069458d02fe866aaccf5653bd2511f90939a9efc50e1d5286917bbcadb30.
Independent exact controls; explicit exceptions remain active with -O.

Stipulated RS first/second moments are used only in finite polynomial identities.
No finite computation here proves the infinite RS correlation theorem.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def add_polys(*polys):
    out = {}
    for poly in polys:
        for term, coeff in poly.items():
            out[term] = out.get(term, Q(0)) + coeff
    return out


def mul(left, right):
    out = {}
    for a, x in left.items():
        for b, y in right.items():
            term = tuple(sorted(a + b))
            out[term] = out.get(term, Q(0)) + x * y
    return out


def expectation(poly, x_mean=Q(0)):
    total = Q(0)
    for monomial, coeff in poly.items():
        # Binary signs square to one. Coordinate product action factors x/y.
        odd = [symbol for symbol, degree in Counter(monomial).items() if degree % 2]
        value = coeff
        for family in ['x', 'y']:
            terms = [index for sequence, index in odd if sequence == family]
            require(len(terms) <= 2, 'Only first and second moments are stipulated')
            if len(terms) == 1:
                value *= x_mean if family == 'x' else Q(0)
            elif len(terms) == 2:
                value *= Q(int(terms[0] == terms[1]))
        total += value
    return total


def occupancy(slot, i, j):
    if slot < 2:
        return {(): Q(1)}
    symbol = ('x', i) if slot == 2 else ('y', j)
    return {(): Q(1, 2), (symbol,): Q(1, 2)}


def weighted(i, j):
    return {(): Q(4), (('x', i),): Q(1), (('y', j),): Q(2)}


def floor_cell_correlation(p, q, bad_flow=False):
    # For t=p/q all possible jumps occur at the q equally spaced section bins.
    # Their exact rational midpoints avoid every seam, including negative time.
    count = 0
    for j in range(q):
        u = Q(2*j+1, 2*q)
        shift = (u + Q(p, q)).__floor__()
        if bad_flow:
            shift += 1
        count += int(shift == 0)
    return Q(count, q)


def run_checks(mutant=None):
    require(mutant in [None, "marker", "moments", "normalization", "flow", "cocycle"], "Unknown exact-control mutant")
    marker = (Q(1, 6), Q(0)) if mutant == 'marker' else (Q(1, 10), Q(1, 10))
    slots = [(Q(0), Q(0)), marker, (Q(1, 3), Q(0)), (Q(0), Q(1, 3))]
    mean_weights = [Q(1), Q(1), Q(1, 2), Q(1, 2)]
    pairs = [(i, j) for i, a in enumerate(slots) for j, b in enumerate(slots)
             if tuple((b[k]-a[k]) % 1 for k in [0, 1]) == marker]
    require(pairs == [(0, 1)], f'Marker is ambiguous: {pairs}')
    min_distance_squared = min(sum((b[k]-a[k]+offset[k])**2 for k in [0, 1])
                               for a, b in product(slots, repeat=2)
                               for offset in product(range(-1, 2), repeat=2)
                               if any(b[k]-a[k]+offset[k] for k in [0, 1]))
    require(min_distance_squared == Q(1, 50), 'Unexpected slot separation')
    local_geometry_checks = 0
    translation = (Q(-7, 30), Q(11, 30))
    for xs, ys in product(product([-1, 1], repeat=4), repeat=2):
        points = set()
        anchors = set()
        for i, j in product(range(4), repeat=2):
            anchor = (Q(i)+translation[0], Q(j)+translation[1])
            anchors.add(anchor)
            present = [0, 1] + ([2] if xs[i] == 1 else []) + ([3] if ys[j] == 1 else [])
            points.update((anchor[0]+slots[c][0], anchor[1]+slots[c][1]) for c in present)
        decoded = {p for p in points if (p[0]+marker[0], p[1]+marker[1]) in points}
        require(decoded == anchors, 'Physical marker failed after a noninteger translation')
        for i, j in product(range(4), repeat=2):
            anchor = (Q(i)+translation[0], Q(j)+translation[1])
            for slot, expected in [(2, xs[i] == 1), (3, ys[j] == 1)]:
                require(((anchor[0]+slots[slot][0], anchor[1]+slots[slot][1]) in points) == expected,
                        'Decoded sign differs from the original')
        local_geometry_checks += 1
    pair_checks = weighted_checks = product_observable_checks = 0
    x_mean = Q(1, 3) if mutant == 'moments' else Q(0)
    for m, n in product(range(-6, 7), repeat=2):
        for c, d in product(range(4), repeat=2):
            actual = expectation(mul(occupancy(c, 0, 0), occupancy(d, m, n)), x_mean)
            claimed = mean_weights[c]*mean_weights[d]
            claimed += Q(1, 4)*int(c == d == 2 and m == 0)
            claimed += Q(1, 4)*int(c == d == 3 and n == 0)
            require(actual == claimed, f'Occupancy coefficient differs: {(c,d,m,n,actual,claimed)}')
            pair_checks += 1
        require(expectation(mul(weighted(0, 0), weighted(m, n)), x_mean) ==
                Q(16)+int(m == 0)+4*int(n == 0), 'Weighted coefficient differs')
        weighted_checks += 1
        g0 = {(('x', 0), ('y', 0)): Q(1)}
        gmn = {(('x', m), ('y', n)): Q(1)}
        require(expectation(mul(g0, gmn), x_mean) == int(m == n == 0),
                'Product observable coefficient differs')
        product_observable_checks += 1
    density = sum(expectation(occupancy(c, 0, 0)) for c in range(4))
    gamma_zero = sum(expectation(mul(occupancy(c, 0, 0), occupancy(c, 0, 0))) for c in range(4))
    decomposition_zero = sum(w*w for w in mean_weights)+Q(1, 2)
    bragg_zero = sum(mean_weights)**2
    target_density = Q(4) if mutant == 'normalization' else Q(3)
    require(density == gamma_zero == decomposition_zero == target_density,
            'Density/self-pair/decomposition normalization fails')
    require(bragg_zero == 9, 'Origin Bragg normalization fails')
    flow_checks = 0
    for q in range(1, 32):
        for p in range(-3*q, 3*q+1):
            actual = floor_cell_correlation(p, q, mutant == 'flow')
            target = max(Q(0), Q(1)-abs(Q(p, q)))
            require(actual == target, f'Floor-bin triangle fails at {p}/{q}: {actual} != {target}')
            flow_checks += 1
    planar_flow_checks = 0
    for p, r in product(range(-8, 9), repeat=2):
        a = floor_cell_correlation(p, 5)
        b = floor_cell_correlation(r, 7)
        direct_count = sum(int((Q(2*i+1, 10)+Q(p, 5)).__floor__() == 0 and
                               (Q(2*j+1, 14)+Q(r, 7)).__floor__() == 0)
                           for i, j in product(range(5), range(7)))
        require(Q(direct_count, 35) == a*b, 'Planar floor integration fails')
        planar_flow_checks += 1
    cocycle_checks = 0
    for u, s, t in product([Q(i, 9) for i in range(9)],
                           [Q(i, 7) for i in range(-9, 10)],
                           [Q(i, 5) for i in range(-9, 10)]):
        m = (u+s).__floor__()
        phase = u+s-m
        sequential = m+(phase+t).__floor__()
        if mutant == 'cocycle':
            sequential += 1
        require(sequential == (u+s+t).__floor__(), 'Suspension action cocycle fails')
        require(0 <= phase < 1, 'Suspension representative outside section')
        cocycle_checks += 1
    return {'status': 'pass', 'arithmetic': 'exact Fraction and polynomial moment reduction',
          'marker_pairs': pairs, 'minimum_squared_slot_distance': str(min_distance_squared),
          'translated_local_geometry_cases': local_geometry_checks,
          'motif_pair_moment_identities': pair_checks, 'weighted_moment_identities': weighted_checks,
          'product_observable_moment_identities': product_observable_checks,
          'density': str(density), 'autocorrelation_at_zero': str(gamma_zero),
          'bragg_at_zero': str(bragg_zero), 'floor_bin_suspension_checks': flow_checks,
          'planar_section_checks': planar_flow_checks, 'suspension_cocycle_checks': cocycle_checks,
          'scope': 'Finite exact controls conditional on RS first/second moments; not an infinite RS proof'}


if __name__ == '__main__':
    print(json.dumps(run_checks(), indent=2))
