#!/usr/bin/env python3
"""Exact finite controls for the explicitly scoped proofs of KOU-21.39.

Standard-library only. These controls do not enumerate infinite groups and do
not resolve the original existence question. Run with Python 3.10 or newer.
"""
from collections import Counter, deque
from itertools import permutations, product, combinations
import json
from math import gcd, lcm
from pathlib import Path

CHECKS = Counter()

def check(condition, category):
    CHECKS[category] += 1
    if not condition:
        raise AssertionError(category)


def perm_mul(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def perm_inv(a):
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def perm_order(a):
    n, x, identity = 1, a, tuple(range(len(a)))
    while x != identity:
        n += 1
        x = perm_mul(x, a)
    return n


def subgroup_closure(generators, identity, mul, inv):
    generators = set(generators)
    generators |= {inv(g) for g in tuple(generators)}
    found, queue = {identity}, deque([identity])
    while queue:
        x = queue.popleft()
        for g in generators:
            y = mul(x, g)
            if y not in found:
                found.add(y)
                queue.append(y)
    return found


def a5_checks():
    s5 = list(permutations(range(5)))
    a5 = [g for g in s5 if sum(g[i] > g[j] for i in range(5)
                               for j in range(i + 1, 5)) % 2 == 0]
    identity = tuple(range(5))
    aset = set(a5)
    check(len(aset) == 60, 'a5_order')
    for a, b in product(a5, repeat=2):
        check(perm_mul(a, b) in aset, 'a5_multiplication_closure')
    classes = []
    unseen = set(a5)
    while unseen:
        g = min(unseen)
        cls = {perm_mul(perm_mul(h, g), perm_inv(h)) for h in s5}
        classes.append(cls)
        unseen -= cls
    check(sorted(map(len, classes)) == [1, 15, 20, 24], 'a5_s5_orbits')
    orders = {g: perm_order(g) for g in a5}
    check(Counter(orders.values()) == {1: 1, 2: 15, 3: 20, 5: 24},
          'a5_element_orders')
    for cls in classes:
        check(len({orders[g] for g in cls}) == 1, 'a5_order_homogeneity')
    # All nontrivial normal closures are the whole group. This is an exhaustive
    # finite certificate of simplicity, not merely a comparison of orders.
    for g in a5:
        if g == identity:
            continue
        conj = {perm_mul(perm_mul(h, g), perm_inv(h)) for h in a5}
        normal_closure = subgroup_closure(conj, identity, perm_mul, perm_inv)
        check(normal_closure == aset, 'a5_nontrivial_normal_closures')
    reps = {n: next(g for g in a5 if orders[g] == n) for n in (1, 2, 3, 5)}
    types = []
    for mask in range(8):
        selected = [q for bit, q in enumerate((2, 3, 5)) if mask & (1 << bit)]
        coordinates = [identity] + [reps[q] if q in selected else identity
                                    for q in (2, 3, 5)]
        order = lcm(*(orders[g] for g in coordinates))
        types.append({'nonidentity_types': selected, 'order': order})
    check(sorted(t['order'] for t in types) == [1, 2, 3, 5, 6, 10, 15, 30],
          'boolean_eight_distinct_order_types')
    involution = reps[2]
    centralizer_size = sum(perm_mul(h, involution) == perm_mul(involution, h)
                          for h in a5)
    check(centralizer_size == 4, 'a5_involution_centralizer')
    atomic_indices = [15 ** m for m in range(1, 9)]
    check(len(set(atomic_indices)) == 8, 'atomic_sum_distinct_centralizer_indices')
    # Negative control: equal element order does NOT entail equal orbit invariant.
    check(perm_order(involution) == 2 and 15 != 15 ** 2,
          'negative_equal_order_does_not_determine_orbit')
    return {'group_order': 60, 's5_orbit_sizes': sorted(map(len, classes)),
            'element_order_counts': dict(sorted(Counter(orders.values()).items())),
            'nontrivial_normal_closures_checked': 59,
            'boolean_patterns': types,
            'atomic_support_1_through_8_centralizer_indices': atomic_indices}


def identity_matrix(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def matrix_mul(a, b, p):
    n = len(a)
    # All matrices here are upper triangular, including their inverses.
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(i, j + 1)) % p
                       if i <= j else 0 for j in range(n)) for i in range(n))


def matrix_power(a, e, p):
    out = identity_matrix(len(a))
    while e:
        if e & 1:
            out = matrix_mul(out, a, p)
        a = matrix_mul(a, a, p)
        e //= 2
    return out


def matrix_inverse(a, p):
    n = len(a)
    b = [[int(i == j) for j in range(n)] for i in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            b[i][j] = -sum(a[i][k] * b[k][j] for k in range(i + 1, j + 1)) % p
    return tuple(map(tuple, b))


def matrix_comm(a, b, p):
    return matrix_mul(matrix_mul(matrix_mul(matrix_inverse(a, p),
                                            matrix_inverse(b, p), p), a, p), b, p)


def transvection(n, i, j, a, p):
    out = [list(row) for row in identity_matrix(n)]
    out[i][j] = a % p
    return tuple(map(tuple, out))


def triangular_checks():
    groups = []
    for p, interior in ((2, 3), (3, 3), (5, 3), (2, 4), (3, 4)):
        n = interior + 2
        positions = list(combinations(range(1, interior + 1), 2))
        cases, entries = 0, 0
        for values in product(range(p), repeat=len(positions)):
            a = [list(row) for row in identity_matrix(n)]
            for (i, j), value in zip(positions, values):
                a[i][j] = value
            g = tuple(map(tuple, a))
            check(matrix_mul(g, matrix_inverse(g, p), p) == identity_matrix(n),
                  'unitriangular_inverse')
            cases += 1
            for (i, j), value in zip(positions, values):
                if not value:
                    continue
                lhs = matrix_comm(matrix_comm(transvection(n, 0, i, 1, p), g, p),
                                  transvection(n, j, n - 1, 1, p), p)
                rhs = transvection(n, 0, n - 1, value, p)
                check(lhs == rhs, 'mclain_double_commutator_extraction')
                entries += 1
        groups.append({'prime': p, 'interior_dimension': interior,
                       'all_matrices_checked': cases, 'nonzero_entries_checked': entries})
    # The elementary commutator formula, with all coefficient pairs.
    for p in (2, 3, 5, 7):
        for a, b in product(range(p), repeat=2):
            check(matrix_comm(transvection(3, 0, 1, a, p),
                              transvection(3, 1, 2, b, p), p)
                  == transvection(3, 0, 2, a * b, p),
                  'mclain_elementary_commutator')
    jordan = []
    for p in (2, 3, 5, 7):
        for n in range(2, 19):
            a = [list(row) for row in identity_matrix(n)]
            for i in range(n - 1):
                a[i][i + 1] = 1
            u = tuple(map(tuple, a))
            exponent = p
            while exponent < n:
                exponent *= p
            check(matrix_power(u, exponent, p) == identity_matrix(n),
                  'jordan_power_upper')
            check(matrix_power(u, exponent // p, p) != identity_matrix(n),
                  'jordan_power_lower')
            jordan.append({'prime': p, 'dimension': n, 'exact_order': exponent})
    for p in (2, 3, 5, 7):
        record = next(x for x in jordan if x['prime'] == p and x['dimension'] == p + 1)
        check(record['exact_order'] == p * p, 'negative_dense_chain_breaks_exponent_p')
    return {'extraction_cases': groups, 'jordan_order_certificates': jordan}


def beta(v, w, p):
    n = len(v) // 2
    return sum(v[i] * w[n + i] - v[n + i] * w[i] for i in range(n)) % p


def e_mul(x, y, p):
    v, a = x
    w, b = y
    return (tuple((s + t) % p for s, t in zip(v, w)),
            (a + b + pow(2, -1, p) * beta(v, w, p)) % p)


def e_inv(x, p):
    return (tuple(-a % p for a in x[0]), -x[1] % p)


def e_comm(x, y, p):
    return e_mul(e_mul(e_mul(e_inv(x, p), e_inv(y, p), p), x, p), y, p)


def e_power(x, m, p):
    ans = (tuple(0 for _ in x[0]), 0)
    for _ in range(m):
        ans = e_mul(ans, x, p)
    return ans


def extraspecial_checks():
    results = []
    for p, rank in ((3, 1), (5, 1), (3, 2)):
        dim = 2 * rank
        vs = list(product(range(p), repeat=dim))
        zero = (0,) * dim
        elements = [(v, a) for v in vs for a in range(p)]
        identity = (zero, 0)
        center = set()
        derived_values = set()
        for x, y in product(elements, repeat=2):
            comm = e_comm(x, y, p)
            check(comm == (zero, beta(x[0], y[0], p)), 'extraspecial_commutator_formula')
            derived_values.add(comm)
        for x in elements:
            check(e_mul(x, e_inv(x, p), p) == identity, 'extraspecial_inverse')
            check(e_power(x, p, p) == identity, 'extraspecial_exponent')
            if all(beta(x[0], v, p) == 0 for v in vs):
                center.add(x)
        check(center == {(zero, a) for a in range(p)} == derived_values,
              'extraspecial_center_equals_derived')
        # Exhaustive associativity in the smallest test group, not in all test groups.
        if p == 3 and rank == 1:
            for x, y, z in product(elements, repeat=3):
                check(e_mul(e_mul(x, y, p), z, p) == e_mul(x, e_mul(y, z, p), p),
                      'extraspecial_associativity_exhaustive_E3')
        basis = [tuple(int(i == j) for i in range(dim)) for j in range(dim)]
        generators = []
        # Symplectic transvections T_u(v)=v+beta(v,u)u, all u.
        for u in vs:
            if u == zero:
                continue
            def trans(x, u=u):
                v, a = x
                c = beta(v, u, p)
                return tuple((s + c * t) % p for s, t in zip(v, u)), a
            for v, w in product(basis, repeat=2):
                check(beta(trans((v, 0))[0], trans((w, 0))[0], p) == beta(v, w, p),
                      'symplectic_generators_preserve_form_on_basis')
            generators.append(trans)
        # All nonzero multipliers; no primitive-root assumption is needed.
        for lam in range(1, p):
            def multiplier(x, lam=lam):
                v, a = x
                return tuple((lam * t if i < rank else t) % p
                             for i, t in enumerate(v)), lam * a % p
            generators.append(multiplier)
        for j in range(dim):
            def shear(x, j=j):
                return x[0], (x[1] + x[0][j]) % p
            generators.append(shear)
        eset = set(elements)
        for f in generators:
            check({f(x) for x in elements} == eset, 'extraspecial_generators_bijective')
            if p == 3 and rank == 1:
                for x, y in product(elements, repeat=2):
                    check(f(e_mul(x, y, p)) == e_mul(f(x), f(y), p),
                          'extraspecial_generators_homomorphisms_E3')
        unseen = set(elements)
        orbit_sizes = []
        while unseen:
            seed = min(unseen)
            seen, q = {seed}, deque([seed])
            while q:
                x = q.popleft()
                for f in generators:
                    y = f(x)
                    if y not in seen:
                        seen.add(y)
                        q.append(y)
            orbit_sizes.append(len(seen))
            unseen -= seen
        check(sorted(orbit_sizes) == sorted([1, p - 1, len(elements) - p]),
              'extraspecial_exact_three_orbits')
        for v in vs:
            if v != zero:
                check({beta(v, w, p) for w in vs} == set(range(p)),
                      'extraspecial_noncentral_commutators_cover_center')
        check(1 < len(center) < len(elements), 'negative_extraspecial_characteristic_center')
        results.append({'prime': p, 'hyperbolic_rank': rank, 'order': len(elements),
                        'center_order': len(center), 'derived_order': len(derived_values),
                        'certified_orbit_sizes': sorted(orbit_sizes),
                        'associativity_exhaustive': p == 3 and rank == 1})
    return results


def h_mul(x, y, p):
    # Unitriangular coordinates (a,b,c) with entry c at (1,3).
    a, b, c = x
    d, e, f = y
    return ((a + d) % p, (b + e) % p, (c + f + a * e) % p)


def h_inv(x, p):
    a, b, c = x
    return (-a % p, -b % p, (a * b - c) % p)


def h_comm(x, y, p):
    return h_mul(h_mul(h_mul(h_inv(x, p), h_inv(y, p), p), x, p), y, p)


def amalgamation_checks():
    out = []
    for p in (3, 5):
        cgroup = list(product(range(p), repeat=2))
        # C=<c,d>; in A=H x Cp, c=z and d is the extra factor.
        emb_a = lambda x: ((0, 0, x[0]), x[1])
        # In B=H, c=u and d=w.
        emb_b = lambda x: (x[0], 0, x[1])
        a_mul = lambda x, y: (h_mul(x[0], y[0], p), (x[1] + y[1]) % p)
        check(len({emb_a(x) for x in cgroup}) == p ** 2, 'amalgam_A_embedding_injective')
        check(len({emb_b(x) for x in cgroup}) == p ** 2, 'amalgam_B_embedding_injective')
        for x, y in product(cgroup, repeat=2):
            xy = tuple((a + b) % p for a, b in zip(x, y))
            check(a_mul(emb_a(x), emb_a(y)) == emb_a(xy), 'amalgam_A_embedding_hom')
            check(h_mul(emb_b(x), emb_b(y), p) == emb_b(xy), 'amalgam_B_embedding_hom')
        x, y, z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
        check(h_comm(x, y, p) == z, 'amalgam_c_is_commutator_in_A')
        check(h_comm(emb_b((1, 0)), y, p) == emb_b((0, 1)) != (0, 0, 0),
              'negative_class_two_amalgam_contradiction')
        for h in product(range(p), repeat=3):
            check(h_comm(z, h, p) == (0, 0, 0), 'amalgam_A_centrality')
            power = (0, 0, 0)
            for _ in range(p):
                power = h_mul(power, h, p)
            check(power == (0, 0, 0), 'amalgam_exponent_p')
        out.append({'prime': p, 'A_order': p ** 4, 'B_order': p ** 3,
                    'C_order': p ** 2, 'both_embeddings_verified': True,
                    'class_two_commutator_contradiction_verified': True})
    return out


def main():
    result = {
        'schema': 'kourovka-2548-exact-controls-v1',
        'scope': 'Finite controls for proved boundary examples; original problem unresolved.',
        'a5_and_boolean': a5_checks(),
        'mclain': triangular_checks(),
        'extraspecial': extraspecial_checks(),
        'class_two_amalgam': amalgamation_checks(),
    }
    result['assertion_counts'] = dict(sorted(CHECKS.items()))
    result['total_assertions'] = sum(CHECKS.values())
    result['status'] = 'pass'
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
