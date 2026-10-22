#!/usr/bin/env python3
"""Independent, standard-library-only diagnostics for Lebedev arXiv:2609.32950v1.

This authored checker does not import, execute, or read the author's companion.
Finite tests support the audit; they do not prove its infinite-parameter results.
"""
from fractions import Fraction as F
from itertools import product, combinations
from collections import Counter
import json


def check(condition, label):
    """Always enforce a diagnostic, including under python -O and -OO."""
    if not condition:
        raise RuntimeError("FAILED: " + label)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def determinant(a):
    a = [[F(v) for v in row] for row in a]
    z = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            z = -z
        v = a[j][j]
        z *= v
        for k in range(j, len(a)):
            a[j][k] /= v
        for i in range(j+1, len(a)):
            v = a[i][j]
            for k in range(j, len(a)):
                a[i][k] -= v*a[j][k]
    return z


def inverse(a):
    n = len(a)
    b = [[F(v) for v in row]+[F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if b[i][j])
        b[j], b[pivot] = b[pivot], b[j]
        v = b[j][j]
        b[j] = [x/v for x in b[j]]
        for i in range(n):
            if i != j:
                v = b[i][j]
                b[i] = [x-v*y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def gram_ok(v):
    d = len(v[0])
    return all(dot(a, b) == (d if i == j else -1)
               for i, a in enumerate(v) for j, b in enumerate(v))


def feasible(v, x, m, n):
    return all(-n <= t <= n for t in x) and all(dot(a, x) >= -m for a in v)


def in_lattice(x, n):
    return all((F(t)-n).denominator == 1 and (F(t)-n).numerator % 2 == 0 for t in x)


def paley():
    squares = {t*t % 11 for t in range(1, 11)}
    v = [[1]*11]+[[-1 if i == j else (1 if (j-i) % 11 in squares else -1)
                    for j in range(11)] for i in range(11)]
    check(gram_ok(v), 'exact_check_001')
    # Independent coefficient computation proves each displayed product as a
    # linear expression in n and a, without finite parameter substitution.
    coeff = [(-1, 0), (-1, 0), (-1, 0), (1, -3), (-1, 1), (-1, 1),
             (1, -1), (-1, 1), (1, 0), (1, -1), (1, 0)]
    products = [(sum(row[j]*coeff[j][0] for j in range(11)),
                 sum(row[j]*coeff[j][1] for j in range(11))) for row in v]
    check(products == [(-1, -2), (-1, -2), (-1, 4), (-1, -2), (-1, 4), (-1, 4),
                        (11, -8), (-1, 4), (-1, 4), (-1, -2), (-1, -2), (-1, -2)], 'exact_check_002')
    rows = [0, 1, 3, 9, 10, 11]
    free = [3, 4, 5, 6, 7, 9]
    minor = [[v[i][j] for j in free] for i in rows]
    check(determinant(minor) == 64, 'exact_check_003')
    x = [a*3+b for a, b in coeff]
    check(feasible(v, x, 5, 3) and not in_lattice(x, 3), 'exact_check_004')
    check(all(dot(v[i], x) == -5 for i in rows), 'exact_check_005')
    check([j for j, z in enumerate(x) if abs(z) < 3] == free, 'exact_check_006')
    chart = [(F(z)+3)/2 for z in x]
    check(sum(z.denominator == 2 for z in chart) == 6, 'exact_check_007')
    cases = 0
    for n in range(1, 22, 2):
        for m in range(n+2, 11*n, 2):
            if 3*m < 7*n and (m-n) % 4 == 2:
                a = (m-n)//2
                y = [u*n+w*a for u, w in coeff]
                check(feasible(v, y, m, n) and not in_lattice(y, n), 'exact_check_008')
                cases += 1
    # Deliberately corrupted inputs must fail the corresponding predicates.
    bad = [row[:] for row in v]
    bad[1][1] *= -1
    check(not gram_ok(bad), 'exact_check_009')
    check(determinant([minor[0]]+minor[:-1]) == 0, 'exact_check_010')
    check(not feasible(v, x, 3, 3), 'exact_check_011')
    check(all(F(t).denominator == 1 for t in x) and not in_lattice(x, 3), 'exact_check_012')
    return {'gram': 'PASS', 'vertex': x, 'chart': list(map(str, chart)),
            'products': [dot(a, x) for a in v], 'active_minor_determinant': 64,
            'parametric_product_coefficients': products, 'sampled_admissible_cases': cases,
            'negative_controls': ['flipped_matrix_entry', 'duplicated_active_row',
                                  'wrong_scale_m', 'wrong_ambient_lattice']}


def sylvester(N):
    return [[1 if (i & j).bit_count() % 2 == 0 else -1 for j in range(1, N)]
            for i in range(N)]


def hole():
    v = sylvester(16)
    check(gram_ok(v), 'exact_check_013')
    h = [0, 0, 0, -2, 2, 2, 2, -2, 2, 2, 2, 2, 2, 2, 2]
    check(in_lattice(h, 2) and feasible(v, h, 10, 2), 'exact_check_014')
    lattice = {x for x in product((-1, 1), repeat=15) if feasible(v, x, 5, 1)}
    check(not any(tuple(hj-xj for hj, xj in zip(h, x)) in lattice for x in lattice), 'exact_check_015')
    face = {x for x in lattice if all(2*x[j] == h[j] for j in range(3, 15))}
    T = {(-1, 1, -1), (1, -1, -1), (-1, -1, 1), (1, 1, 1)}
    check({x[:3] for x in face} == T and len(face) == 4, 'exact_check_016')
    check(all(tuple(-z for z in t) not in T for t in T), 'exact_check_017')
    fixed = [sum(v[i][j]*(h[j]//2) for j in range(3, 15)) for i in range(16)]
    check(fixed == [8, -4, -4, -4, -4, 0, 0, 0, -4, 0, 0, 0, 0, 4, 4, 4], 'exact_check_018')
    changed = h[:]
    changed[0] = 2
    check(feasible(v, changed, 10, 2), 'exact_check_019')
    check(any(tuple(hj-xj for hj, xj in zip(changed, x)) in lattice for x in lattice), 'exact_check_020')
    false_face_point = [1, -1, 1]+[z//2 for z in h[3:]]
    check(not feasible(v, false_face_point, 5, 1), 'exact_check_021')
    return {'degree_two_hole': h, 'all_source_lattice_points_enumerated': 32768,
            'feasible_source_lattice_points': len(lattice), 'face_lattice_points': len(face),
            'decompositions': 0, 'fixed_row_contributions': fixed,
            'integrality_proof': 'Theorem 2.3, independently audited in prose; not inferred from this enumeration',
            'negative_controls': ['nearby_degree_two_point_is_decomposable', 'false_face_point_is_infeasible']}


def small_signs():
    result = {}
    for k in range(1, 5):
        counts = Counter()
        for bits in product((-1, 1), repeat=(k-1)**2):
            a = [[1]*k for _ in range(k)]
            for q, (i, j) in enumerate(product(range(1, k), repeat=2)):
                a[i][j] = bits[q]
            det = abs(determinant(a))
            counts[str(det)] += 1
            if det == 2**(k-1):
                inv = inverse(a)
                check(all((2*z).denominator == 1 for row in inv for z in row), 'exact_check_022')
                check(all(sum(row).denominator == 1 for row in inv), 'exact_check_023')
                if k == 3:
                    check(all(sum(z != 0 for z in row) == 2 and
                               all(z in (0, F(1, 2), F(-1, 2)) for z in row) for row in inv), 'exact_check_024')
            elif det:
                check(k == 4 and det == 16, 'exact_check_025')
                check(all(dot(row, other) == (4 if i == j else 0)
                           for i, row in enumerate(a) for j, other in enumerate(a)), 'exact_check_026')
        result[str(k)] = dict(counts)
    return result


def sharp_examples():
    result = []
    for N in (16, 32, 64):
        v = sylvester(N)
        check(gram_ok(v), 'exact_check_027')
        rho = 3*N//8-1
        for n in (1, 3, 5, 7):
            x = []
            for j in range(1, N):
                w = (j & 7).bit_count()
                s = -1 if w <= 1 else (1 if w == 3 else (-1 if j & 8 else 1))
                x.append(n*s+(1 if j in (1, 2, 4) else (-1 if j == 7 else 0)))
            m = rho*n-2
            check(n < m < (N-1)*n and m % 2 == 1, 'exact_check_028')
            check(feasible(v, x, m, n) and not in_lattice(x, n), 'exact_check_029')
            free = [j for j, z in enumerate(x) if abs(z) < n]
            check(free == [0, 1, 3, 6], 'exact_check_030')
            rows = [0, 1, 2, 4]
            check(all(dot(v[i], x) == -m for i in rows), 'exact_check_031')
            det = determinant([[v[i][j] for j in free] for i in rows])
            check(abs(det) == 16, 'exact_check_032')
            result.append({'N': N, 'n': n, 'm': m, 'active_minor_abs_determinant': int(abs(det)),
                           'minimum_simplex_slack': min(dot(row, x)+m for row in v)})
    return result


def resonance():
    # Uses the same mathematically defined Paley family, reconstructed here.
    squares = {t*t % 11 for t in range(1, 11)}
    v = [[1]*11]+[[-1 if i == j else (1 if (j-i) % 11 in squares else -1)
                    for j in range(11)] for i in range(11)]
    x = [1]+[-1]*10
    check(feasible(v, x, 9, 1), 'exact_check_033')
    tight = [i for i, row in enumerate(v) if dot(row, x) == -9]
    check(tight == [0], 'exact_check_034')
    check(9 > F(3*11-1, 4), 'exact_check_035')
    return {'d': 11, 'm': 9, 'n': 1, 'cube_vertex': x, 'incident_genuine_facets': 12,
            'simplex_row_products': [dot(row, x) for row in v],
            'conclusion': 'Nonsimple resonance, although Santos printed sufficient bound is satisfied'}


if __name__ == '__main__':
    report = {'status': 'PASS', 'arithmetic': 'exact integers and fractions only',
              'external_companion_executed': False, 'paley': paley(), 'hole': hole(),
              'small_sign_matrix_classes': small_signs(), 'sylvester_sharpness_samples': sharp_examples(),
              'smoothness_resonance': resonance()}
    print(json.dumps(report, indent=2))
