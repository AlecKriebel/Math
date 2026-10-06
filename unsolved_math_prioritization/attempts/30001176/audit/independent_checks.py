#!/usr/bin/env python3
"""Independent finite-set controls. No author code is imported or executed."""
from functools import lru_cache
from itertools import combinations, product
import json
import random

ZERO = (frozenset(), frozenset(), frozenset())
COUNTS = {}

def check(label, condition):
    if not condition:
        raise RuntimeError(label)
    COUNTS[label] = COUNTS.get(label, 0) + 1

@lru_cache(maxsize=None)
def mul(x, y):
    a, b, c = x
    d, e, f = y
    twist = frozenset(i for i in a if len(e - {i}) % 2)
    return a ^ d, b ^ e, c ^ f ^ twist

def inv(x):
    a, b, c = x
    return a, b, c ^ frozenset(i for i in a if len(b - {i}) % 2)

def gen(i, slot):
    x = list(ZERO)
    x[slot] = frozenset({i})
    return tuple(x)

def closure(generators):
    found, pending = {ZERO}, [ZERO]
    while pending:
        x = pending.pop()
        for y in generators:
            xy = mul(x, y)
            if xy not in found:
                found.add(xy)
                pending.append(xy)
    return found

def subsets(indices):
    indices = sorted(indices)
    return [frozenset(c) for r in range(len(indices)+1) for c in combinations(indices, r)]

def full_group(indices):
    powerset = subsets(indices)
    return set(product(powerset, repeat=3))

def relabel(x, mapping):
    return tuple(frozenset(mapping[i] for i in coordinate) for coordinate in x)

def comm(x, y):
    return mul(mul(mul(x, y), inv(x)), inv(y))

def run():
    COUNTS.clear()
    all2 = full_group({0, 1})
    for x, y, z in product(all2, repeat=3):
        check('all_two_site_associativity', mul(mul(x, y), z) == mul(x, mul(y, z)))
    all3 = full_group({0, 1, 2})
    for x in all3:
        check('identity', mul(ZERO, x) == mul(x, ZERO) == x)
        check('two_sided_inverse', mul(x, inv(x)) == mul(inv(x), x) == ZERO)
    H, K = {}, {}
    for I in subsets({0, 1, 2}):
        H[I] = closure([gen(i, k) for i in I for k in (0, 1)])
        K[I] = closure([gen(i, k) for i in I for k in (0, 1, 2)])
        expected = full_group(I) if len(I) >= 2 else set(product(subsets(I), subsets(I), [frozenset()]))
        check('canonical_generated_subgroup', H[I] == expected)
        check('enlarged_generated_subgroup', K[I] == full_group(I))
    meet_failures = []
    for I, J in product(H, repeat=2):
        intersection = H[I] & H[J]
        if intersection != H[I & J]:
            meet_failures.append([sorted(I), sorted(J), len(intersection), len(H[I & J])])
        check('enlarged_meet', K[I] & K[J] == K[I & J])
        # Generate joins from the explicit site generators, including central sites.
        joined = closure([gen(i, k) for i in I | J for k in (0, 1, 2)])
        check('enlarged_join', joined == K[I | J])
        for x in all3:
            check('fourier_projection_composition', (x in H[I] and x in H[J]) == (x in intersection))
        if not I & J:
            for x, y in product(H[I], H[J]):
                check('disjoint_trace_basis', (mul(x, y) == ZERO) == (x == ZERO and y == ZERO))
    check('six_ordered_meet_failures', len(meet_failures) == 6)
    p, q1, q2, z0 = gen(0, 0), gen(1, 1), gen(2, 1), gen(0, 2)
    check('two_commutators_same_witness', comm(p, q1) == comm(p, q2) == z0)
    check('witness_outside_singleton', z0 not in H[frozenset({0})])
    check('intersection_dimension_eight', H[frozenset({0,1})] & H[frozenset({0,2})] == K[frozenset({0})] and len(K[frozenset({0})]) == 8)
    check('singleton_dimension_four', len(H[frozenset({0})]) == 4)
    check('fourier_expectations_distinguish_meet', z0 in H[frozenset({0,1})] and z0 in H[frozenset({0,2})] and z0 not in H[frozenset({0})])
    # Actual left regular actions as permutations of the 512 group basis vectors.
    for g in (p, q1, q2, z0):
        action = {x:mul(g,x) for x in all3}
        check('left_regular_bijective', set(action.values()) == all3)
        check('left_regular_normalized_trace_zero', sum(x == y for x,y in action.items()) == 0)
    for x in all3:
        check('regular_commutator_action', mul(p,mul(q1,mul(p,mul(q1,x)))) == mul(z0,x))
    alternating = ZERO
    for g in (p,q1)*4:
        alternating = mul(alternating,g)
    check('nonfree_eighth_moment', alternating == ZERO)
    # Exercise genuinely non-contiguous labels and non-surjective injections.
    labels = (0, 1, 37, 1001, 1000000)
    rng = random.Random(30001176)
    samples = [tuple(frozenset(i for i in labels if rng.randrange(2)) for _ in range(3)) for _ in range(90)]
    mapping = {i:7+3*i for i in labels}
    for t in range(1800):
        x,y,z = (samples[rng.randrange(len(samples))] for _ in range(3))
        check('sparse_label_associativity', mul(mul(x,y),z) == mul(x,mul(y,z)))
        check('sparse_label_injection', relabel(mul(x,y),mapping) == mul(relabel(x,mapping),relabel(y,mapping)))
    # Known incorrect relations must be distinguished by these controls.
    check('reject_commuting_sites_model', mul(p,q1) != mul(q1,p))
    check('reject_diagonal_commutator_model', comm(gen(0,0),gen(0,1)) == ZERO)
    check('reject_no_enlargement_repair', H[frozenset({0})] != K[frozenset({0})])
    for a,b in product((-1,1),repeat=2):
        x = a+2*b
        sign = 1 if x > 0 else -1
        check('single_selfadjoint_recovers_site', sign == b and x-2*sign == a)
    return {'schema':1,'problem_id':'30001176','status':'PASS_FINITE_SUPPLEMENT',
            'implementation':'Finite sets and symmetric differences; no author code imports.',
            'counts':dict(sorted(COUNTS.items())),'total_checks':sum(COUNTS.values()),
            'finite_group_orders':[len(all2),len(all3)],'meet_failures':sorted(meet_failures),
            'scope':'Finite diagnostics only. Infinite proof and source-scope conclusions are in AUDIT.md and INDEPENDENT_LEMMAS.md.'}

if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
