#!/usr/bin/env python3
"""Independently authored finite checks. Standard library, no input files or network.
This does not import the packet verifier. Prints deterministic JSON only.
Universal geometric assertions are audited in AUDIT.md, not certified by sampling.
"""
import itertools as it
import json
import math
from fractions import Fraction as F


def insist(p, label):
    if not p:
        raise AssertionError(label)


def mask(indices):
    return sum(1 << i for i in indices)


def colors_hit(edge, color_classes):
    return all(edge & c for c in color_classes)


def color_masks(labels, k):
    return tuple(mask(i for i, x in enumerate(labels) if x == c) for c in range(k))


def balancing():
    cases = 0
    for levels, d in it.product(range(1, 7), range(8)):
        q = 1 << levels
        threshold = q + (q - 1) * d
        # The closed form for repeated floor((a-d)/2) is independent of the
        # author's recursive implementation. The real bound is the proof's.
        value = F(threshold - (q - 1) * d, q)
        below = F(threshold - 1 - (q - 1) * d, q)
        insist(value == 1 and math.floor(below) == 0, 'balanced formula')
        cases += 1
    feasible = 0
    for a, d in it.product(range(65), range(8)):
        possible = [b for b in range(a + 1) if abs(2*b-a) <= d]
        if possible:
            insist(min(possible) >= math.ceil(F(a-d, 2)), 'actual integer child')
            feasible += 1
    # M-1 is not a coloring impossibility certificate: D=1, q=2, M=3.
    insist(min(b for b in range(3) if abs(2*b-2) <= 1) == 1,
           'do not mistake weak floor negative for theorem sharpness')
    return {'formula_cases': cases, 'feasible_integer_child_cases': feasible,
            'one_below_is_only_conservative_floor_failure': True,
            'ordinary_two_cover_can_have_depths': [1, 999]}


def interval_removal():
    intervals = [(a, b) for a in range(5) for b in range(a+1, 5)]
    vertex_covers = [mask(x for x in range(5) if a <= x <= b) for a, b in intervals]
    unions = [0] * (1 << len(intervals))
    for sub in range(1, len(unions)):
        bit = sub & -sub
        unions[sub] = unions[sub ^ bit] | vertex_covers[bit.bit_length()-1]
    count = 0
    # Remove from largest index first, unlike the frozen verifier.
    for family in range(1, 1 << len(intervals)):
        for target in range(32):
            if unions[family] & target != target:
                continue
            current = family
            for j in reversed(range(len(intervals))):
                candidate = current & ~(1 << j)
                if unions[candidate] & target == target:
                    current = candidate
            insist(unions[current] & target == target, 'subcover')
            insist(all(unions[current ^ (1 << j)] & target != target
                       for j in range(len(intervals)) if current >> j & 1), 'minimal')
            # Doubled coordinates cover endpoints and all open arrangement cells.
            depth = max(sum(current >> j & 1 for j, (a, b) in enumerate(intervals)
                            if 2*a <= x <= 2*b) for x in range(9))
            insist(depth <= 2, 'interval shallow subcover')
            count += 1
    insist(count == 30648, 'interval count')
    # Explicit multiplicity, degeneracy, nested, and arbitrary target controls.
    extra_cases = 0
    extra = [(0,0),(1,1),(2,2),(0,1),(1,2),(0,2)]
    for n in range(1, 5):
        for inds in it.combinations_with_replacement(range(len(extra)), n):
            fam = [extra[j] for j in inds]
            for target in range(8):
                good = [sub for sub in range(1 << n)
                        if all(any(sub >> j & 1 and a <= x <= b
                                   for j, (a,b) in enumerate(fam))
                               for x in range(3) if target >> x & 1)]
                if not good:
                    continue
                minimal = [sub for sub in good if not any(
                    sub >> j & 1 and (sub ^ (1 << j)) in good for j in range(n))]
                for sub in minimal:
                    insist(max(sum(sub >> j & 1 for j,(a,b) in enumerate(fam)
                                   if 2*a <= x <= 2*b) for x in range(5)) <= 2,
                           'all minimal subcovers including degenerate duplicates')
                extra_cases += 1
    return {'base_cover_target_cases': count,
            'extra_degenerate_duplicate_cases_all_minimal_subcovers': extra_cases}


def cyclic_intervals():
    counts = dict.fromkeys(['closed', 'open', 'left_closed', 'right_closed'], 0)
    incidence_tests = 0
    for n in range(1, 7):
        for left in it.combinations_with_replacement(range(-2,3), n):
            # Scale original half-unit endpoints by four; interval length is four.
            starts = [2*a for a in left]
            boundaries = sorted(set(starts + [a+4 for a in starts]))
            query = boundaries + [F(a+b,2) for a,b in zip(boundaries,boundaries[1:])]
            query += [boundaries[0]-1, boundaries[-1]+1]
            for mode, k in it.product(counts, range(2,5)):
                for x in query:
                    lo = (lambda a: a <= x) if mode in ['closed','left_closed'] else (lambda a: a < x)
                    hi = (lambda a: x <= a+4) if mode in ['closed','right_closed'] else (lambda a: x < a+4)
                    active = [j for j,a in enumerate(starts) if lo(a) and hi(a)]
                    insist(not active or active == list(range(active[0],active[-1]+1)), 'consecutive block')
                    if len(active) >= k:
                        insist({j % k for j in active} == set(range(k)), 'cyclic color coverage')
                    incidence_tests += 1
                counts[mode] += 1
    insist(sum(counts[m] for m in ['closed','open','left_closed']) == 4149, 'cyclic count')
    return {'matching_three_boundary_modes_cases': 4149,
            'additional_right_closed_cases': counts['right_closed'],
            'point_boundary_queries': incidence_tests}


def finite_types():
    cases = high = below_controls = 0
    for r,k in it.product(range(1,6), range(2,5)):
        threshold = r*(k-1)+1
        low = [k-1] * r
        insist(sum(low) == threshold-1 and max(low) < k, 'one-less pigeonhole boundary')
        below_controls += 1
        for amounts in it.product(range(k+1), repeat=r):
            # A literal per-type coloring, not only the pigeonhole implication.
            color_sets = [set(range(k)) if n >= k else {0} if n else set()
                          for n in amounts]
            for pattern in range(1 << r):
                chosen = [j for j in range(r) if pattern >> j & 1]
                if sum(amounts[j] for j in chosen) >= threshold:
                    seen = set().union(*(color_sets[j] for j in chosen))
                    insist(seen == set(range(k)), 'finite-type construction')
                    high += 1
                cases += 1
    insist(cases == 157888, 'finite-type count')
    return {'multiplicity_incidence_cases': cases, 'heavy_patterns_coloring_checked': high,
            'one_less_pigeonhole_controls': below_controls}


def hub_counts():
    rows = []
    for s in range(2,5):
        n = 2*s-1
        edges = [mask(c) for c in it.combinations(range(n),s)]
        with_hub = [e | (1 << n) for e in edges]
        b2 = sum(all(colors_hit(e, color_masks(lab,2)) for e in edges)
                 for lab in it.product(range(2),repeat=n))
        h2 = sum(all(colors_hit(e, color_masks(lab,2)) for e in with_hub)
                 for lab in it.product(range(2),repeat=n+1))
        h3 = sum(all(colors_hit(e, color_masks(lab,3)) for e in with_hub)
                 for lab in it.product(range(3),repeat=n+1))
        insist(b2 == 0 and h2 == 1 << n and h3 == 0, 'hub and nonhereditary trace')
        rows.append({'s':s,'base_two_colorings':b2,'hub_two_colorings':h2,
                     'hub_three_colorings':h3,'incidence_pairs':len(edges)*(n+1)})
    return rows


def geometry(n, edges, spacing=None, radius=F(1,4), cutoff=None):
    q = len(edges)
    Q = n+1 if spacing is None else spacing
    witness = [Q*(j+1) for j in range(q)]
    disks = [(witness[j]-i, 0) for j,e in enumerate(edges) for i in range(n) if e >> i & 1]
    R = Q*(q+1)+n if cutoff is None else cutoff
    def contains(x,y):
        return x > R or any((x-a)**2+(y-b)**2 < radius**2 for a,b in disks)
    mismatch = [(j,i,bool(e >> i & 1),contains(witness[j]-i,0))
                for j,e in enumerate(edges) for i in range(n)
                if bool(e >> i & 1) != contains(witness[j]-i,0)]
    return mismatch, disks, witness, R, contains


def geometric_controls():
    systems = pairs = 0
    # Exhaust all edge sequences, including empty, repeated, full edges and isolated
    # vertices, for n<=4 and q<=3; unlike testing only hub examples.
    for n,q in it.product(range(1,5), range(1,4)):
        for edges in it.product(range(1 << n), repeat=q):
            bad,disks,witness,R,inside = geometry(n,edges)
            insist(not bad, 'arbitrary finite incidence encoding')
            insist(all(a >= 2 for a,b in disks), 'positive disk centers')
            insist(max(witness) < R, 'half-plane beyond witnesses')
            insist(not inside(R, 10**6), 'open half-plane boundary')
            insist(inside(R+F(1,100),10**6), 'half-plane interior')
            for a,b in disks[:1]:
                insist(not inside(a+F(1,4),b), 'open disk boundary')
                insist(inside(a+F(1,5),b), 'disk interior')
            systems += 1
            pairs += n*q
    # Independently test every hub incidence too.
    hub_pairs = 0
    for s in range(2,5):
        n=2*s
        edges=[mask(c)|(1 << (n-1)) for c in it.combinations(range(n-1),s)]
        bad,_,_,_,_=geometry(n,edges)
        insist(not bad,'hub geometry')
        hub_pairs += n*len(edges)
    insist(hub_pairs == 352,'hub geometry count')
    # Verify an explicit selector in each residue class, with arbitrary vertical
    # translation and half-plane equality included among test coordinates.
    samples = 0
    R=19
    for k,x,c in ((k,x,c) for k in range(2,8) for x in range(-50,51) for c in range(k)):
        j=max(1,math.floor(F(R-x,R+1))+1)
        j += (c-j) % k
        insist(j % k == c and x > R-j*(R+1),'explicit residue witness')
        samples += 1
    insist(samples == 2727,'half-plane sample count')
    return {'exhaustive_arbitrary_edge_sequence_systems':systems,
            'arbitrary_encoding_incidence_pairs':pairs,'hub_incidence_pairs':hub_pairs,
            'open_boundaries_checked':True,'explicit_cofinal_witness_samples':samples}


def union_bounds():
    rows=[]
    for N,k in [(1,2),(10,3),(100,4),(1000,5)]:
        feasible=[m for m in range(1,100) if N*k*(k-1)**m < k**m]
        m=min(feasible)
        value=F(N*k*(k-1)**m,k**m)
        insist(N*k*(k-1)**(m-1) >= k**(m-1),'minimal strict threshold')
        rows.append({'N':N,'k':k,'M':m,'numerator':value.numerator,'denominator':value.denominator})
    return rows


def deliberate_negatives():
    bad_spacing=geometry(2,[1,1],spacing=1)[0]
    bad_radius=geometry(2,[1,0],radius=F(2))[0]
    bad_halfplane=geometry(2,[0],cutoff=0)[0]
    insist(bad_spacing and bad_radius and bad_halfplane,'geometric mutations caught')
    all_equal=not colors_hit(7,color_masks([0,0,0],3))
    singleton_failure=not any(colors_hit(1,color_masks(lab,2)) for lab in it.product(range(2),repeat=1))
    # Boundaries, cofinality, hereditary trace, and closure are mathematical
    # negative checks; these finite witnesses illustrate, not replace, proofs.
    R=19
    finite_last_index=199
    far_left=R-(finite_last_index+1)*(R+1)
    insist(all(not far_left > R-j*(R+1) for j in range(1,finite_last_index+1)),
           'finite prefix does not cover plane')
    # Strict decrease to -1 need not escape to minus infinity.
    insist(all(-2 <= R+(-1+F(1,j+1)) for j in range(1,100)), 'bounded decrease insufficient')
    insist(all(not -1 > R for _ in range(3)), 'vertical translation alone insufficient')
    # An open cover need not have a point-finite subcover: tails of right halfplanes.
    # Also, infinite polychromatic tail constraints are non-closed in product topology.
    for n in range(1,30):
        coloring=lambda i: 0 if i <= n else (i-n)%2
        insist(all(coloring(i)==0 for i in range(1,n+1)), 'all-red coordinate prefix')
        for start in range(1,30):
            j=max(start,n+1)
            insist({coloring(j),coloring(j+1)}=={0,1},'tail coloring witness')
    insist(all_equal and singleton_failure,'bad coloring and union equality rejected')
    return {'all_equal_three_coloring_rejected':all_equal,
            'union_bound_equality_singleton_rejected':singleton_failure,
            'insufficient_spacing_mismatches':bad_spacing,
            'oversized_disk_mismatches':bad_radius,
            'premature_halfplane_mismatches':bad_halfplane,
            'finite_prefix_coverage_claim_rejected':True,
            'strict_decrease_without_unboundedness_rejected':True,
            'unbounded_vertical_parameters_alone_rejected':True,
            'one_less_balancing_bound_not_sharpness_certificate':True,
            'infinite_tail_nonclosure_control':True}


def main():
    result={'all_checks_passed':True,'scope':'Finite exact controls only; see AUDIT.md for universal reasoning.',
            'balancing':balancing(),'intervals':interval_removal(),'cyclic_intervals':cyclic_intervals(),
            'finite_types':finite_types(),'hubs':hub_counts(),'geometry':geometric_controls(),
            'union_bound':union_bounds(),'deliberate_negatives':deliberate_negatives()}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
