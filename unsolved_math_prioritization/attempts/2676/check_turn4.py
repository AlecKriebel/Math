"""Exact controls for the fourth KP-1.17 partial research turn.

This checks graph enumeration and the stated integral/projective algebra.
It does not implement Floer theory, link recognition, or the topological
classification inputs used in the written proof.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, permutations, product
from math import gcd
import json
import sympy as s
from sympy.matrices.normalforms import smith_normal_form

counts = Counter()


def check(condition, family):
    assert condition, family
    counts[family] += 1


def connected(n, edges):
    reached = {0}
    while True:
        enlarged = reached | {v for u, v in edges if u in reached} | {
            u for u, v in edges if v in reached}
        if enlarged == reached:
            return len(reached) == n
        reached = enlarged


def tree_count(n, edges):
    lap = s.zeros(n)
    for u, v in edges:
        lap[u, u] += 1
        lap[v, v] += 1
        lap[u, v] -= 1
        lap[v, u] -= 1
    return int(lap[:-1, :-1].det())


def canonical(n, edges):
    encodings = []
    for perm in permutations(range(n)):
        multiplicities = Counter(tuple(sorted((perm[u], perm[v]))) for u, v in edges)
        encodings.append(tuple(multiplicities[u, v] for u, v in combinations(range(n), 2)))
    return n, min(encodings)


classes = {}
for n in range(2, 6):
    pairs = list(combinations(range(n), 2))
    for m in range(n, 6):
        for selected in combinations_with_replacement(range(len(pairs)), m):
            edges = [pairs[j] for j in selected]
            if not connected(n, edges):
                continue
            if any(not connected(n, edges[:j] + edges[j+1:]) for j in range(m)):
                continue
            tau = tree_count(n, edges)
            direct = sum(connected(n, [edges[j] for j in chosen])
                         for chosen in combinations(range(m), n-1))
            check(tau == direct, 'matrix_tree_vs_direct_enumeration')
            check(tau >= m, 'edge_count_bound_on_all_enumerated_graphs')
            if tau == 5:
                classes[canonical(n, edges)] = {
                    'vertices': n, 'edges': m,
                    'degrees': sorted(sum(v in edge for edge in edges) for v in range(n)),
                    'tree_count': tau,
                }
check(len(classes) == 3, 'exactly_three_determinant_five_graphs')
check({(v['vertices'], v['edges'], tuple(v['degrees'])) for v in classes.values()} == {
    (2, 5, (5, 5)), (5, 5, (2, 2, 2, 2, 2)), (3, 4, (2, 3, 3))},
    'determinant_five_graph_identification')

for a, b, ell in product(range(1, 15), repeat=3):
    if a + b < 3:
        continue
    tau = a*b + a*ell + b*ell
    check(tau >= a+b-1+(a+b)*ell, 'theta_lower_bound')
    check((tau <= 5) == (ell == 1 and sorted((a, b)) == [1, 2]),
          'unique_first_ear_of_tree_count_at_most_five')

A = s.Matrix([[3, -5], [1, -2]])
check(A.det() == -1, 'orientation_reversing_gluing')
check(A * (-s.eye(2)) == (-s.eye(2)) * A, 'linear_equivariance')
presentation = s.Matrix([[1, -3], [0, 5]])
SNF = smith_normal_form(presentation, domain=s.ZZ)
check(tuple(abs(int(SNF[i, i])) for i in range(2)) == (1, 5),
      'full_homology_smith_form')
check(A * s.Matrix([1, 0]) == s.Matrix([3, 1]), 'meridian_maps_to_interior_slope_three')
check(A * s.Matrix([1, 1]) == s.Matrix([-2, -1]), 'endpoint_one_maps_to_two')
r = s.symbols('r')
check(s.cancel((3*r-5)/(r-2) - (3+1/(r-2))) == 0, 'mobius_identity')

for p in range(-80, 81):
    for q in range(1, 31):
        if gcd(p, q) != 1:
            continue
        P, Q = 3*p-5*q, p-2*q
        check(gcd(P, Q) == 1, 'primitive_slope_preservation')
        if p <= q:
            # Both P,Q are negative. Check 2 <= P/Q < 3 by signed multiplication.
            check(Q < 0 and P <= 2*Q and P > 3*Q,
                  'projective_complement_maps_into_two_to_three')
        if p != 0:
            rank = p + 2*max(0, q-p)
            check((rank == abs(p)) == (p >= q), 'trefoil_rank_formula_lspace_range')
            check(rank >= abs(p) and (rank-abs(p)) % 2 == 0,
                  'trefoil_rank_formula_parity_and_lower_bound')

# Direct finite-grid checks of the actual linear pillowcase commutation.
# These supplement the symbolic equality; they do not assert a finite test
# is a substitute for equivariance on the whole torus.
for modulus in [2, 3, 5, 7, 11]:
    images = set()
    for x, y in product(range(modulus), repeat=2):
        image = ((3*x-5*y) % modulus, (x-2*y) % modulus)
        images.add(image)
        negative_then_image = ((-3*x+5*y) % modulus, (-x+2*y) % modulus)
        image_then_negative = tuple((-v) % modulus for v in image)
        check(negative_then_image == image_then_negative, 'pillowcase_commutation_controls')
    check(len(images) == modulus**2, 'pillowcase_linear_map_bijective')
check(presentation.det() % 2 == 1, 'branched_component_mod_two_homology_control')

print(json.dumps({
    'status': 'PASS',
    'exact_assertions': sum(counts.values()),
    'families': dict(sorted(counts.items())),
    'determinant_five_graphs': sorted(classes.values(), key=lambda v: (v['vertices'], v['edges'])),
    'gluing_matrix_columns_in_meridian_longitude_basis': [[3, -5], [1, -2]],
    'homology_smith_invariants': [1, 5],
    'scope': 'Exact graph and gluing algebra only. Topological and Floer conclusions use the written proof and named primary theorems. This is not a mixed-alternation counterexample; KP-1.17 remains unresolved.'
}, indent=2, sort_keys=True))
