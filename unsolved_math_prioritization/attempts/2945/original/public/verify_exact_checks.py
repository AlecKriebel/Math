#!/usr/bin/env python3
"""Exact finite checks accompanying KP-4.69 partial results.

Standard library only. No source/corpus files, downloads, or floating-point
arithmetic are used. This is not a smooth pseudo-isotopy decision procedure.
"""
import json
import math
from itertools import product


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def mul(p, q):
    # a^i x^j, with a^6=1, x^2=a^3, x a x^-1=a^-1.
    i, j = p
    k, ell = q
    return ((i + (-1 if j else 1) * k + 3*j*ell) % 6,
            (j + ell) % 2)


def gf2_rank(rows):
    pivots = {}
    for row in rows:
        while row:
            p = row.bit_length() - 1
            if p in pivots:
                row ^= pivots[p]
            else:
                pivots[p] = row
                break
    return len(pivots)


def group_checks():
    group = list(product(range(6), range(2)))
    universe = set(group)
    identity = (0, 0)
    check(len(universe) == 12, 'Incorrect group cardinality')
    for p, q in product(group, repeat=2):
        check(mul(p, q) in universe, 'Closure failed')
    for p, q, r in product(group, repeat=3):
        check(mul(mul(p, q), r) == mul(p, mul(q, r)),
              'Associativity failed')
    inv = {}
    for p in group:
        check(mul(identity, p) == p == mul(p, identity), 'Identity failed')
        candidates = [q for q in group
                      if mul(p, q) == identity == mul(q, p)]
        check(len(candidates) == 1, 'Inverse failed')
        inv[p] = candidates[0]
    a, x = (1, 0), (0, 1)
    check(mul(x, x) == (3, 0), 'x^2=a^3 failed')
    check(mul(mul(x, a), inv[x]) == inv[a], 'Conjugation failed')
    powers = [identity]
    for _ in range(3):
        powers.append(mul(powers[-1], x))
    check(len(set(powers)) == 4 and mul(powers[-1], x) == identity,
          'Cyclic Sylow 2 subgroup failed')
    commutators = {mul(mul(mul(p, q), inv[p]), inv[q])
                   for p, q in product(group, repeat=2)}
    derived = {identity}
    while True:
        nxt = derived | {mul(p, q) for p in derived for q in commutators}
        if nxt == derived:
            break
        derived = nxt
    check(derived == {(0, 0), (2, 0), (4, 0)}, 'Derived subgroup mismatch')
    cosets = {frozenset(mul(p, q) for q in derived) for p in group}
    x_cosets = [frozenset(mul(p, q) for q in derived) for p in powers]
    check(len(cosets) == 4 and len(set(x_cosets)) == 4,
          'Abelianization is not cyclic of order four')
    # Integer determinantal divisors for the presentation's abelian relation matrix.
    relation_rows = [(6, 0), (-3, 2), (2, 0)]
    delta1 = math.gcd(*(abs(t) for row in relation_rows for t in row))
    minors = [abs(p[0]*q[1] - p[1]*q[0])
              for p, q in product(relation_rows, repeat=2)]
    delta2 = math.gcd(*minors)
    check((delta1, delta2) == (1, 4), 'Smith invariants mismatch')
    return {
        'group': 'Dic_3', 'order': 12,
        'associativity_triples_checked': 12**3,
        'cyclic_sylow_2_order': 4,
        'derived_subgroup_order': 3,
        'abelianization_invariant_factors_nontrivial': [4],
        'relation_matrix_smith_nonzero': [1, 4]
    }


def graph_check(m, n):
    # m left vertices, n right vertices; edge (i,j) has bit index i*n+j.
    vertex_rows = []
    for i in range(m):
        vertex_rows.append(sum(1 << (i*n+j) for j in range(n)))
    for j in range(n):
        vertex_rows.append(sum(1 << (i*n+j) for i in range(m)))
    rank = gf2_rank(vertex_rows)
    all_edges = (1 << (m*n)) - 1
    boundary_of_left = 0
    for row in vertex_rows[:m]:
        boundary_of_left ^= row
    check(boundary_of_left == all_edges, 'All-edge cut identity failed')
    check(rank == m+n-1, 'Connected graph incidence rank failed')
    check(gf2_rank(vertex_rows + [all_edges]) == rank,
          'All edges did not cancel in cohomology')
    check(gf2_rank(vertex_rows + [1]) == rank+1,
          'Single-edge negative control unexpectedly cancelled')
    cycle_rank = m*n-rank
    check(cycle_rank == (m-1)*(n-1), 'Cover free rank mismatch')
    return {'left_vertices': m, 'right_vertices': n,
            'degree_edges': m*n, 'incidence_rank_F2': rank,
            'free_rank': cycle_rank,
            'all_edge_cochain_is_coboundary': True,
            'single_edge_negative_control_is_not_coboundary': True}


def cancellation_check():
    # The local-realization proof, not this calculation, establishes that these
    # two coordinates can be realized by relative homeomorphisms.
    vectors = list(product(range(2), repeat=2))
    for a in vectors:
        translates = {(a[0]^h[0], a[1]^h[1]) for h in vectors}
        check(translates == set(vectors), 'Coset mismatch')
        check((a[0]^a[0], a[1]^a[1]) == (0, 0), 'Cancellation failed')
    return {'obstruction_group': '(Z/2)^2',
            'classes_checked': 4,
            'each_class_can_be_cancelled_if_full_realization_holds': True,
            'geometric_realization_is_an_external_theorem': True}


def main():
    group = group_checks()
    graphs = [graph_check(m, n) for m, n in [(2,2), (3,4), (12,12)]]
    base_betti = [1, 0, 0, 1]
    circle_betti = [1, 1]
    product_betti = [sum(base_betti[i]*circle_betti[k-i]
                         for i in range(4) if 0 <= k-i < 2)
                     for k in range(5)]
    check(product_betti == [1,1,0,1,1], 'Kunneth ranks failed')
    euler = sum((-1)**i*b for i,b in enumerate(product_betti))
    check(euler == 0, 'Euler characteristic mismatch')
    result = {
        'problem_id': 2945,
        'all_checks_passed': True,
        'method': 'exact finite integer and F2 arithmetic; no numerical tests',
        'group': group,
        'cover_graph_checks': graphs,
        'mapping_torus_rational_betti': product_betti,
        'mapping_torus_euler_characteristic': euler,
        'casson_sullivan_cancellation_model': cancellation_check(),
        'limitations': [
            'Does not decide smooth or topological pseudo-isotopy.',
            'Does not certify external theorems or their geometric hypotheses.',
            'Does not supply a diffeomorphism of the unstabilized cylinder.'
        ]
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
