#!/usr/bin/env python3
"""Independent exact arithmetic for the KP-4.69 audit; no source files needed.

The geometric theorems are deliberately not represented as machine-certified.
All acceptance conditions use explicit exceptions, including under -O and -OO.
"""
import json
from itertools import product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def times(a, b):
    # Exact ring Z[zeta], zeta^2 = zeta - 1, zeta = exp(pi*i/3).
    u, v = a
    s, t = b
    return (u*s - v*t, u*t + v*s + v*t)


ZERO, ONE = (0, 0), (1, 0)
IDENTITY = (ONE, ZERO, ZERO, ONE)
A = ((0, 1), ZERO, ZERO, (1, -1))
X = (ZERO, ONE, (-1, 0), ZERO)


def matrix_mul(a, b):
    return tuple(add(times(a[2*i], b[j]), times(a[2*i+1], b[2+j]))
                 for i in range(2) for j in range(2))


def power(a, n):
    result = IDENTITY
    for _ in range(n):
        result = matrix_mul(result, a)
    return result


def generated(generators):
    group = {IDENTITY}
    while True:
        enlarged = group | {matrix_mul(g, a) for g in group for a in generators}
        if enlarged == group:
            return group
        require(len(enlarged) <= 1000, 'unexpectedly large generated matrix group')
        group = enlarged


def matrix_group_check():
    group = generated([A, X])
    require(len(group) == 12, 'matrix group must have order twelve')
    normal_forms = {(i, j): matrix_mul(power(A, i), power(X, j))
                    for i in range(6) for j in range(2)}
    require(set(normal_forms.values()) == group, 'normal forms do not cover group')
    require(power(A, 6) == IDENTITY and power(A, 3) != IDENTITY, 'order of A')
    require(power(X, 2) == power(A, 3) and power(X, 4) == IDENTITY, 'order of X')
    inverses = {}
    for a in group:
        possible = [b for b in group if matrix_mul(a, b) == IDENTITY == matrix_mul(b, a)]
        require(len(possible) == 1, 'matrix inverse')
        inverses[a] = possible[0]
    checks = 0
    for (i, j), (k, ell) in product(normal_forms, repeat=2):
        expected = ((i + (-1)**j*k + 3*j*ell) % 6, (j + ell) % 2)
        require(matrix_mul(normal_forms[i, j], normal_forms[k, ell]) ==
                normal_forms[expected], 'candidate normal-form formula disagrees with matrices')
        checks += 1
    commutators = [matrix_mul(matrix_mul(matrix_mul(a, b), inverses[a]), inverses[b])
                   for a, b in product(group, repeat=2)]
    derived = generated(commutators)
    require(derived == {IDENTITY, power(A, 2), power(A, 4)}, 'derived group')
    quotient = {frozenset(matrix_mul(g, d) for d in derived) for g in group}
    x_cosets = {frozenset(matrix_mul(power(X, i), d) for d in derived) for i in range(4)}
    require(quotient == x_cosets and len(quotient) == 4, 'cyclic quotient order four')
    # The incorrect dihedral-style x^2=1 relation is visibly rejected.
    require(power(X, 2) != IDENTITY, 'negative control x^2=1 was accepted')
    return {'representation': '2 by 2 matrices over Z[zeta_6]',
            'matrix_elements': len(group), 'normal_form_products_checked': checks,
            'derived_order': len(derived), 'abelianization': 'Z/4',
            'cyclic_sylow_2_order': len(generated([X])),
            'wrong_dihedral_relation_rejected': True}


def cycle_basis_check(m, n):
    edges = {(i, j) for i in range(m) for j in range(n)}
    tree = {(0, j) for j in range(n)} | {(i, 0) for i in range(m)}
    require(len(tree) == m+n-1, 'spanning-tree edge count')
    cycles = [{(0, 0), (i, 0), (0, j), (i, j)}
              for i in range(1, m) for j in range(1, n)]
    require(len(cycles) == len(edges-tree) == (m-1)*(n-1), 'fundamental-cycle rank')
    # Each cycle contains its own unique non-tree edge, hence these are independent.
    require({next(iter(c-tree)) for c in cycles} == edges-tree,
            'fundamental cycles do not have unique pivots')
    require(all(len(c & edges) % 2 == 0 for c in cycles), 'all-edge class not zero')
    single = {(0, 0)}
    require(any(len(c & single) % 2 for c in cycles), 'single edge should be nonzero')
    # Removing just one all-edge twist destroys the cancellation.
    require(any(len(c & (edges-single)) % 2 for c in cycles),
            'omitted-twist negative control should be nonzero')
    return {'bipartition': [m, n], 'vertices': m+n, 'edges': m*n,
            'spanning_tree_edges': len(tree), 'independent_cycles': len(cycles),
            'all_edge_cycle_pairings_zero': True,
            'single_and_missing_edge_controls_nonzero': True}


def cancellation_controls():
    vectors = set(product(range(2), repeat=2))
    xor = lambda a, b: (a[0]^b[0], a[1]^b[1])
    require(all(xor(a, a) == (0, 0) for a in vectors), 'full cancellation')
    restricted = {(0, 0), (1, 0)}
    require((0, 0) not in {xor((0, 1), h) for h in restricted},
            'one factor alone cannot cancel the other factor')
    swap = lambda a: (a[1], a[0])
    a = (1, 0)
    require(xor(a, swap(a)) != (0, 0), 'nontrivial pullback control')
    return {'full_group_classes': len(vectors), 'full_cancellation': True,
            'proper_subgroup_negative_control': True,
            'nontrivial_pullback_negative_control': True,
            'does_not_verify_geometric_realization': True}


def main():
    # Independent Kunneth accounting: the only rational basis classes have
    # degrees 0, 3 on M, and 0, 1 on the circle.
    degrees = [i+j for i in (0, 3) for j in (0, 1)]
    betti = [degrees.count(i) for i in range(5)]
    require(betti == [1, 1, 0, 1, 1], 'rational homology')
    require(sum((-1)**i*b for i, b in enumerate(betti)) == 0, 'Euler characteristic')
    require(betti[2] == 0, 'rational intersection space')
    result = {'status': 'PASS', 'group': matrix_group_check(),
              'cover': [cycle_basis_check(m, n) for m, n in ((2, 2), (3, 4), (12, 12))],
              'mapping_torus_betti': betti, 'signature_from_zero_rank': 0,
              'cancellation_controls': cancellation_controls(),
              'geometric_proof_is_not_machine_certified': True}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
