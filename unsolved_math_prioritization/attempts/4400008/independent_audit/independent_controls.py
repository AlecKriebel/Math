#!/usr/bin/env python3
"""Independent exact finite controls; imports no authored verification code.
These do not prove the infinite topological or classification assertions.
"""
from itertools import product
from math import gcd
import json

CHECKS = 0

def require(p, why):
    global CHECKS
    CHECKS += 1
    if not p:
        raise AssertionError(why)

def rotate(word, k):
    k %= len(word)
    return word[k:] + word[:k]

def hits(bit, n):
    """Read the two cylinders directly as coordinate constraints."""
    u = all(bit(j) == (j == n) for j in range(-3*n, 3*n+1))
    v = all(bit(j) == (j == -n) for j in range(-5*n, n+1))
    return u, v

def periodic_h(word):
    if not any(word):
        return word
    p = len(word)
    n = min(min(j, p-j) for j, b in enumerate(word) if b)
    if n == 0:
        return word
    u, v = hits(lambda j: word[j % p], n)
    require(not (u and v), 'U_n and V_n disjoint')
    return rotate(word, 2*n if u else -2*n if v else 0)

def least_period(word):
    return next(k for k in range(1, len(word)+1) if rotate(word, k) == word)

def finite_h(support):
    if not support or 0 in support:
        return support, 0
    n = min(map(abs, support))
    u, v = hits(lambda j: j in support, n)
    jump = 2*n if u else -2*n if v else 0
    return tuple(sorted(j-jump for j in support)), jump

def even_language(word):
    possible = {0, 1}
    for bit in word:
        possible = ({0} if 0 in possible else set()) if bit else {1-s for s in possible}
    return bool(possible)

def main():
    periodic_cases = 0
    zero_neighborhood_checks = 0
    for p in range(1, 15):
        for w in product((0, 1), repeat=p):
            hw = periodic_h(w)
            require(periodic_h(hw) == w, 'periodic involution')
            require(hw in {rotate(w, j) for j in range(p)}, 'orbit membership')
            require(least_period(hw) == least_period(w), 'least-period preservation')
            for r in range((p+1)//2):
                if all(w[j % p] == 0 for j in range(-r, r+1)):
                    require(all(hw[j % p] == 0 for j in range(-r, r+1)),
                            'central zero neighborhood invariant')
                    zero_neighborhood_checks += 1
            periodic_cases += 1

    boundary_cases = 0
    max_jump = 0
    for n in range(1, 258):
        p = (n+1, 3*n+2)
        hp, before = finite_h(p)
        shifted = tuple(j-1 for j in p)
        hshift, after = finite_h(shifted)
        require(before == 0 and hp == p, 'aperiodic witness unchanged')
        require(after == 2*n, 'shifted witness uses prescribed exchange')
        require(hshift == tuple(j-(2*n+1) for j in p), 'exact jump 2n+1')
        require(finite_h(hshift)[0] == shifted, 'inverse on witness')
        # Both cylinder endpoints and just-outside coordinates are audited.
        for other, expected in ((3*n,False),(3*n+1,True),(-3*n,False),(-3*n-1,True)):
            u, v = hits(lambda j, a=other: j in (n,a), n)
            require(u == expected and not v, 'U boundary constraint')
            boundary_cases += 1
        for other, expected in ((-5*n,False),(-5*n-1,True),(n,False),(n+1,True)):
            u, v = hits(lambda j, a=other: j in (-n,a), n)
            require(v == expected and not u, 'V boundary constraint')
            boundary_cases += 1
        max_jump = 2*n+1

    # Independent graph-automaton test, rather than merely counting ones.
    even_windows = 0
    for m in range(1, 97):
        w = (1,) + (0,)*(2*m+1)
        for k in range(len(w)):
            block = tuple(w[(k+j)%len(w)] for j in range(2*m+1))
            require(even_language(block), 'every tested block accepted by even-shift automaton')
            even_windows += 1
        require(not even_language((1,)+(0,)*(2*m+1)+(1,)), 'odd gap rejected')

    # Count cyclic allowed words directly, with no matrix-power implementation.
    allowed = {(0,0),(0,1),(1,2),(2,0),(2,1)}
    expansion = []
    for p in range(1, 11):
        expansion.append(sum(all((w[j],w[(j+1)%p]) in allowed for j in range(p))
                             for w in product(range(3), repeat=p)))
    require(expansion[:2] == [1,3], 'expansion loses one fixed point')
    lucas = [1,3]
    for _ in range(8):
        lucas.append(lucas[-1]+lucas[-2])
    require(expansion == lucas, 'cyclic word count equals Lucas recurrence')
    require(expansion[0] != 2, 'flow equivalence does not imply TOE')

    # Losing onto-orbit, or replacing an infinite line by a finite cycle, matters.
    require({(2*j)%3 for j in range(3)} == set(range(3)), 'finite cycle positive step2 works')
    require(all(2*j != 1 for j in range(-1024,1025)), 'step2 on Z misses odd indices')
    require(gcd(2,3) == 1 and gcd(2,4) == 2, 'finite generator depends on period')
    # A 2-cycle is irreducible and periodic but has no odd fixed points.
    cycle2_counts = [2 if n%2 == 0 else 0 for n in range(1,21)]
    require(all(cycle2_counts[n-1] == 0 for n in range(1,21,2)), 'irreducible need not mixing')
    # Dense full orbit alone does not imply forward transitivity: single-marker shift.
    require(all(-n != 1 for n in range(1025)), 'forward orbit of marker0 never reaches marker1')

    print(json.dumps({
      'target_id':'4400008','result':'PASS','arithmetic':'exact integers, tuples, finite automata',
      'assertions':CHECKS,'periodic_full_shift_words':periodic_cases,
      'periodic_word_lengths':[1,14],'zero_neighborhood_checks':zero_neighborhood_checks,
      'aperiodic_witness_n':[1,257],'largest_checked_unique_jump':max_jump,
      'cylinder_boundary_checks':boundary_cases,'even_shift_m':[1,96],
      'even_shift_windows_checked':even_windows,
      'expansion_fixed_counts_direct_enumeration_n1_to10':expansion,
      'negative_inferences_rejected':[
       'expansivity bounds every orbit-equivalence cocycle',
       'finitely checked language windows establish finite type',
       'positive S squared has the same complete infinite orbits',
       'a finite-cycle speedup validates an infinite-orbit construction',
       'flow equivalence preserves orbit cardinalities',
       'irreducibility alone implies mixing',
       'dense full orbit alone implies forward transitivity'],
      'scope':'Finite controls and countermodels only. Infinite claims require audit.md and the retained proofs.'
    },indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
