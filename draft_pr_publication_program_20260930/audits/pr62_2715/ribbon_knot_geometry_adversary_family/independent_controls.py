#!/usr/bin/env python3
"""Exact logical/geometric-count diagnostics, not computations for actual knots."""
import json
import os
from collections import Counter
from itertools import combinations, permutations, product

if not __debug__:
    raise SystemExit("Refusing optimized Python: independent controls require active checks.")

checks = Counter()
def check(condition, family):
    if not condition:
        raise RuntimeError("Control failed: " + family)
    checks[family] += 1

# A ribbon annulus has Euler characteristic 0: b-s=0. Reversal exchanges
# index 0 and 2. This count does not encode a particular embedded annulus.
for births in range(21):
    original = (births, births, 0)
    reverse = tuple(reversed(original))
    check(original[0]-original[1]+original[2] == 0, "annular_morse_counts")
    check(reverse[0]-reverse[1]+reverse[2] == 0, "annular_morse_counts")
    check((reverse[2] == 0) == (births == 0), "annular_morse_counts")

# Finiteness, antisymmetry, and a constant split invariant can coexist with
# distinct comparable objects. These are abstract models, not knot examples.
objects = range(3)
relation = {(i,j) for i in objects for j in objects if i <= j}
check(all((i,i) in relation for i in objects), "finite_poset_countermodel")
check(all(i==j for i,j in relation if (j,i) in relation), "finite_poset_countermodel")
check(all((i,k) in relation for i,j in relation for j2,k in relation if j==j2), "finite_poset_countermodel")
check((0,1) in relation and (1,0) not in relation, "finite_poset_countermodel")
check(len({i for i in objects if (i,2) in relation}) == 3, "finite_poset_countermodel")
# Constant functor to F2 with every morphism sent to identity respects composition.
check(all(1*1 == 1 for i,j in relation for j2,k in relation if j==j2), "finite_poset_countermodel")

# Exhaust all nonzero small finite H profiles, with shifts in both directions
# and collisions with the fixed summand B. Common B cancels grade by grade.
sites = ((-1,-2),(0,0),(1,2),(2,0))
B = Counter({(-1,-2):2,(0,0):1,(3,6):2})
def shifted(H,n):
    return Counter({(h+2*n,q+4*n):rank for (h,q),rank in H.items()})
profile_count = 0
for ranks in product(range(3), repeat=len(sites)):
    H = Counter({site:rank for site,rank in zip(sites,ranks) if rank})
    if not H:
        continue
    profile_count += 1
    family = {n:B+shifted(H,n) for n in range(-2,3)}
    for n,m in combinations(family,2):
        X,Y = family[n],family[m]
        check(sum(X.values()) == sum(Y.values()), "graded_shift_obstruction")
        check(X != Y, "graded_shift_obstruction")
        check(any(X[k] > Y[k] for k in X), "graded_shift_obstruction")
        check(any(Y[k] > X[k] for k in Y), "graded_shift_obstruction")
# Nonzero H is essential; a trivial-band formula H=0 has no obstruction.
check(B+shifted(Counter(),0) == B+shifted(Counter(),1), "zero_H_boundary")

# A5 is a concrete finite (hence residually finite), perfect group. It supplies
# a group-theoretic control, not a group claimed to occur as a knot group.
def compose(p,q):
    return tuple(p[q[i]] for i in range(5))
def inv(p):
    q = [0]*5
    for i,j in enumerate(p):
        q[j] = i
    return tuple(q)
def parity(p):
    return sum(p[i]>p[j] for i in range(5) for j in range(i+1,5)) % 2
A5 = {p for p in permutations(range(5)) if parity(p)==0}
commutators = {compose(compose(compose(p,q),inv(p)),inv(q)) for p in A5 for q in A5}
check(len(A5)==60, "residual_finiteness_is_not_nilpotence")
check(commutators==A5, "residual_finiteness_is_not_nilpotence")
check(len(commutators)>1, "residual_finiteness_is_not_nilpotence")

print(json.dumps({
    "status":"PASS_SCOPED_CONTROLS",
    "pid":os.getpid(),
    "checks_by_family":dict(checks),
    "total_checks":sum(checks.values()),
    "nonzero_H_profiles":profile_count,
    "scope":"Finite exact logical, grading and Morse-count controls only; no actual knot computations and no proof or refutation of KP1.56."
},indent=2,sort_keys=True))
