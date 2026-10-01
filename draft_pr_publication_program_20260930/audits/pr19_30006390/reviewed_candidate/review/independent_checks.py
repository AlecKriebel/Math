#!/usr/bin/env python3
"""Independent exact checks; no imports from the submitted diagnostic script."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json

checks = 0

def verify(condition):
    global checks
    checks += 1
    assert condition


def affine_completion(q):
    # Affine points, one infinite point for each finite slope, and vertical infinity.
    pts = [('a', x, y) for x in range(q) for y in range(q)]
    pts += [('i', slope) for slope in range(q)] + [('v',)]
    index = {point: i for i, point in enumerate(pts)}
    sets = []
    for slope in range(q):
        for intercept in range(q):
            sets.append({('a', x, (slope*x+intercept) % q) for x in range(q)} | {('i', slope)})
    for x in range(q):
        sets.append({('a', x, y) for y in range(q)} | {('v',)})
    sets.append(set(pts[q*q:]))
    return pts, [sum(1 << index[x] for x in line) for line in sets]

results = []
for q in (2, 3):
    pts, lines = affine_completion(q)
    n = len(pts)
    total = 1 << n
    full = total - 1
    verify(n == q*q+q+1 and len(lines) == n)
    verify(len(set(lines)) == n)
    for line in lines:
        verify(line.bit_count() == q+1)
    for i, j in combinations(range(n), 2):
        verify(sum(bool(line & (1 << i)) and bool(line & (1 << j)) for line in lines) == 1)
    for line, other in combinations(lines, 2):
        verify((line & other).bit_count() == 1)
    ordinary = [all(mask & line for line in lines) for mask in range(total)]
    minimal = [mask for mask in range(total) if ordinary[mask] and all(
        not ordinary[mask ^ (1 << i)] for i in range(n) if mask & (1 << i))]
    count_minimal = Counter(mask.bit_count() for mask in minimal)
    tau = []
    nontrivial_blockers = 0
    alteration_cases = 0
    for retained in range(total):
        relevant = [line for line in lines if retained & line]
        # Directly enumerate submasks, instead of the submitted subset DP.
        best = retained.bit_count()
        candidate = retained
        while True:
            if candidate.bit_count() < best and all(candidate & line for line in relevant):
                best = candidate.bit_count()
            if candidate == 0:
                break
            candidate = (candidate - 1) & retained
        tau.append(best)
        contained_minimal = [mask for mask in minimal if mask & retained == mask]
        if ordinary[retained]:
            verify(contained_minimal != [])
            verify(best == min(mask.bit_count() for mask in contained_minimal))
            if not any(retained & line == line for line in lines):
                nontrivial_blockers += 1
                k = retained.bit_count()
                a = k-q-1
                verify(a >= 0 and a*a >= q)
                rs = [(retained & line).bit_count() for line in lines]
                verify(max(rs) <= a+1)
                verify(sum(r*(r-1) for r in rs) == k*(k-1))
                verify(sum(r-1 for r in rs) == k*(q+1)-n)
                verify((a+1)*(k*(q+1)-n)-k*(k-1) == q*(a*a-q))
            # A probability different from the submitted script's 1/2.
            rho = Fraction(1, 3)
            expectation = rho*retained.bit_count()+sum((1-rho)**((retained & line).bit_count()) for line in lines)
            verify(best <= expectation)
            alteration_cases += 1
        else:
            verify(not contained_minimal)
        # Exact complement-of-blocker characterization of full-line independence.
        verify(ordinary[retained] == (not any((full ^ retained) & line == line for line in lines)))
    bad = sum(not value for value in ordinary)
    verify(bad == sum(any(mask & line == line for line in lines) for mask in range(total)))
    verify(Fraction(bad, total) <= n*Fraction(1, 2**(q+1)))
    for k in range(n+1):
        first_moment = sum(Fraction(1, 2**mask.bit_count()) for mask in minimal if mask.bit_count() <= k)
        exact_good_event = Fraction(sum(ordinary[r] and tau[r] <= k for r in range(total)), total)
        exact_all_event = Fraction(sum(value <= k for value in tau), total)
        verify(exact_good_event <= first_moment)
        verify(exact_all_event <= Fraction(bad, total)+first_moment)
        # Independent double count of the expectation of the number of witnesses.
        witnesses = sum(sum(mask & r == mask for mask in minimal if mask.bit_count() <= k) for r in range(total))
        verify(Fraction(witnesses, total) == first_moment)
    line, other = lines[:2]
    joint = Fraction(sum(not (r & line) and not (r & other) for r in range(total)), total)
    marginal = Fraction(1, 2**(q+1))
    verify(joint == Fraction(1, 2**(2*q+1)))
    verify(joint == 2*marginal*marginal)
    sigma_norm_squared = n*Fraction(q+1, (q+1)*len(lines))**2
    verify(sigma_norm_squared == Fraction(1, n))
    verify(n < (q+1)**2)
    verify(n < 10**9*(q+1)**7)
    verify(n < 150000*(q+1)**4)
    results.append({'q':q,'all_point_subsets':total,'minimal_blockers_by_size':dict(sorted(count_minimal.items())),
                    'ordinary_blockers':sum(ordinary),'nontrivial_ordinary_blockers':nontrivial_blockers,
                    'alteration_expectations_checked_at_rho_1_over_3':alteration_cases,
                    'weighted_bounds_checked_for_k':list(range(n+1)),
                    'joint_empty_probability':str(joint),'product_of_marginals':str(marginal*marginal)})

report = {'description':'Independent affine-coordinate exact diagnostics, not asymptotic evidence',
          'all_assertions_passed':True,'assertions':checks,'planes':results}
Path(__file__).with_name('independent_checks.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
