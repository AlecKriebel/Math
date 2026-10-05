#!/usr/bin/env python3
"""Finite exact controls for PROOF.md. No external files, network, or packages.
These tests do not certify the unresolved universal geometric statement.
"""
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product
import json


def check(condition, description):
    if not condition:
        raise AssertionError(description)


def edge_colors(edge, coloring):
    return {coloring[v] for v in edge}


def polychromatic(edges, coloring, k):
    wanted = set(range(k))
    return all(edge_colors(e, coloring) == wanted for e in edges)


def balanced_controls():
    rows = []
    for r in range(1, 7):
        q = 2 ** r
        for d in range(8):
            m = q + (q - 1) * d
            a = m
            for _ in range(r):
                a = (a - d) // 2
            check(a == 1, "balanced lower-bound recurrence")
            b = m - 1
            for _ in range(r):
                b = (b - d) // 2
            check(b == 0, "one-below-threshold recurrence negative control")
            rows.append([q, d, m, a, b])
    check(min(1, 999) == 1, "ordinary split may leave depth one")
    return {"recurrence_cases": len(rows), "all_terminal_bounds": 1,
            "one_below_threshold_terminal_bounds": 0,
            "one_vs_many_depths": [1, 999]}


def interval_controls():
    intervals = list(combinations(range(5), 2))
    testpoints = [Fraction(i, 2) for i in range(9)]
    cases = 0
    for family_mask in range(1, 1 << len(intervals)):
        family = [j for j in range(len(intervals)) if family_mask >> j & 1]
        for target_mask in range(1 << 5):
            target = [x for x in range(5) if target_mask >> x & 1]
            def covers(indices):
                return all(any(intervals[j][0] <= x <= intervals[j][1]
                               for j in indices) for x in target)
            if not covers(family):
                continue
            minimal = family[:]
            for j in family:
                reduced = [i for i in minimal if i != j]
                if covers(reduced):
                    minimal = reduced
            check(covers(minimal), "minimal subfamily remains cover")
            check(all(not covers([i for i in minimal if i != j])
                      for j in minimal), "subfamily is inclusion-minimal")
            depth = max(sum(intervals[j][0] <= x <= intervals[j][1]
                            for j in minimal) for x in testpoints)
            check(depth <= 2, "minimal closed interval cover has depth <=2")
            cases += 1
    strip_cases = 0
    centers = [Fraction(i, 2) for i in range(-2, 3)]
    for n in range(1, 7):
        for lefts in combinations_with_replacement(centers, n):
            endpoints = sorted(set(lefts) | {a + 1 for a in lefts})
            queries = sorted(set(endpoints) |
                             {(a+b)/2 for a,b in zip(endpoints,endpoints[1:])} |
                             {endpoints[0]-1, endpoints[-1]+1})
            for mode in ('closed', 'open', 'half_open'):
                for k in range(2, 5):
                    coloring = [i % k for i in range(n)]
                    for x in queries:
                        if mode == 'closed':
                            edge = [i for i,a in enumerate(lefts) if a <= x <= a+1]
                        elif mode == 'open':
                            edge = [i for i,a in enumerate(lefts) if a < x < a+1]
                        else:
                            edge = [i for i,a in enumerate(lefts) if a <= x < a+1]
                        if len(edge) >= k:
                            check(edge_colors(edge, coloring) == set(range(k)),
                                  "cyclic ordered congruent intervals")
                    strip_cases += 1
    check(not polychromatic([{0,1,2}], [0,0,0], 3),
          "all-equal strip coloring is rejected")
    return {"minimal_cover_cases": cases, "cyclic_interval_cases": strip_cases,
            "arithmetic": "exact fractions", "bad_coloring_rejected": True}


def probabilistic_controls():
    rows = []
    for n,k in [(1,2),(10,3),(100,4),(1000,5)]:
        m = 1
        while n*k*Fraction(k-1,k)**m >= 1:
            m += 1
        p = n*k*Fraction(k-1,k)**m
        prev = n*k*Fraction(k-1,k)**(m-1)
        check(p < 1 <= prev, "strict union-bound threshold")
        rows.append({"N":n,"k":k,"M":m,
                     "bound_numerator":p.numerator,"bound_denominator":p.denominator})
    check(Fraction(1*2,1)*Fraction(1,2)**1 == 1,
          "union bound at equality is inconclusive")
    check(not any(polychromatic([{0}], c, 2) for c in product(range(2), repeat=1)),
          "singleton rejects missing strictness")
    return {"thresholds":rows,"equality_negative_control_rejected":True}


def realization(edges, n, q_multiplier=None):
    q = len(edges)
    Q = n + 1 if q_multiplier is None else q_multiplier
    points = [Q*(e+1) for e in range(q)]
    centers = {points[e]-i for e,edge in enumerate(edges) for i in edge}
    R = Q*(q+1)+n
    mismatches = []
    for e, x in enumerate(points):
        for i in range(n):
            z = x-i
            # Radius 1/4; all data are integers, so this is exact squared distance.
            actual = any(16*(z-c)**2 < 1 for c in centers) or z > R
            expected = i in edges[e]
            if actual != expected:
                mismatches.append([e,i,expected,actual])
    return {"pair_count":q*n,"mismatches":mismatches,
            "Q":Q,"R":R,"minimum_center":min(centers) if centers else None}


def obstruction_controls():
    rows=[]
    for s in range(2,5):
        n0=2*s-1
        base=[set(e) for e in combinations(range(n0),s)]
        hub=[e|{n0} for e in base]
        b2=sum(polychromatic(base,c,2) for c in product(range(2),repeat=n0))
        h2=sum(polychromatic(hub,c,2) for c in product(range(2),repeat=n0+1))
        h3=sum(polychromatic(hub,c,3) for c in product(range(3),repeat=n0+1))
        check(b2==0 and h2>0 and h3==0,"hub obstruction and trace")
        geometry=realization(hub,n0+1)
        check(not geometry['mismatches'],"geometric incidences agree exactly")
        check(geometry['minimum_center']>=2,"shape contained in positive halfplane")
        rows.append({"s":s,"base_vertices":n0,"edge_count":len(base),
                     "base_2colorings":b2,"hub_2colorings":h2,
                     "hub_polychromatic_3colorings":h3,
                     "incidence_pairs":geometry['pair_count']})
    malformed=realization([{0},{0}],2,q_multiplier=1)
    check(len(malformed['mismatches'])>0,"collision bug negative control detected")
    # Minimal ordered sequence for the half-plane extraction: a_j=-j*(R+1).
    # For every bounded test x and every color, sufficiently large j covers x.
    R=19
    for k in range(2,8):
        for x in range(-50,51):
            for color in range(k):
                js=[j for j in range(1,200) if j%k==color]
                check(any(x>R-j*(R+1) for j in js),"cofinal halfplane subsequence")
    return {"hub_cases":rows,"malformed_spacing_mismatches":malformed['mismatches'],
            "halfplane_sample_checks":sum(k*101 for k in range(2,8)),
            "warning":"Finite checks do not prove a fixed-shape global obstruction."}


def type_controls():
    checked=0
    tight=0
    for r in range(1,6):
        for k in range(2,5):
            threshold=r*(k-1)+1
            for counts in product(range(k+1), repeat=r):
                for pattern in range(1<<r):
                    present=[j for j in range(r) if pattern>>j&1]
                    depth=sum(counts[j] for j in present)
                    if depth>=threshold:
                        check(any(counts[j]>=k for j in present),
                              "finite-type pigeonhole")
                    checked+=1
            counts=[k-1]*r
            check(sum(counts)==threshold-1 and all(c<k for c in counts),
                  "type proof one-below-threshold control")
            tight+=1
    return {"count_pattern_cases":checked,"one_below_threshold_controls":tight,
            "warning":"Sharpness of the pigeonhole step is not optimality of m_k."}


def main():
    report={"all_checks_passed":True,"scope":"finite exact controls only",
            "balanced":balanced_controls(),"intervals":interval_controls(),
            "random":probabilistic_controls(),"obstructions":obstruction_controls(),
            "types":type_controls()}
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
