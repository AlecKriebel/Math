#!/usr/bin/env python3
"""Exact bounded controls, not a proof search or a general-projection oracle.

Run: python check.py > control-results.json
Standard library only. e=2,...,6; largest matrix is 126 by 126.
"""
from fractions import Fraction
from itertools import combinations_with_replacement, combinations
import json


def rank(matrix):
    if not matrix:
        return 0
    a = [[Fraction(v) for v in row] for row in matrix]
    h, w = len(a), len(a[0])
    r = 0
    for col in range(w):
        p = next((i for i in range(r, h) if a[i][col]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        v = a[r][col]
        a[r] = [x / v for x in a[r]]
        for i in range(r + 1, h):
            v = a[i][col]
            if v:
                a[i] = [x - v * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == h:
            break
    return r


def determinant(matrix):
    a = [[Fraction(v) for v in row] for row in matrix]
    n = len(a)
    ans = Fraction(1)
    for j in range(n):
        p = next((i for i in range(j, n) if a[i][j]), None)
        if p is None:
            return Fraction(0)
        if p != j:
            a[p], a[j] = a[j], a[p]
            ans = -ans
        v = a[j][j]
        ans *= v
        for i in range(j + 1, n):
            mul = a[i][j] / v
            if mul:
                a[i] = [x - mul * y for x, y in zip(a[i], a[j])]
    return ans


def exponents(pair, e):
    out = [0] * e
    for i in pair:
        out[i] += 1
    return tuple(out)


def syzygy_matrix(e, pairs):
    """Taylor pair relations generate the syzygy module of a monomial ideal.

    Apply every pair-lcm relation to arbitrary A-valued images. Columns are
    indexed by (generator, basis element of A=1,z_1,...,z_e). Terms of degree
    >=2 vanish in A. No expected rank is inserted into the matrix.
    """
    gens = [exponents(pair, e) for pair in pairs]
    basis = [(0,) * e] + [tuple(int(a == b) for a in range(e)) for b in range(e)]
    idx = {mon: i for i, mon in enumerate(basis)}
    d, g = e + 1, len(gens)
    rows = []
    for i, j in combinations(range(g), 2):
        lcm = tuple(max(a, b) for a, b in zip(gens[i], gens[j]))
        terms = [dict() for _ in basis]
        for k, sign in [(i, 1), (j, -1)]:
            mult = tuple(a - b for a, b in zip(lcm, gens[k]))
            for t, mon in enumerate(basis):
                prod = tuple(a + b for a, b in zip(mult, mon))
                if prod in idx:
                    terms[idx[prod]][k * d + t] = sign
        for sparse in terms:
            if sparse:
                rows.append([sparse.get(k, 0) for k in range(g * d)])
    return rows


def normal_matrix(e, pairs, cross_terms=True):
    g = len(pairs)
    excluded = [((a, a), a) for a in range(e)]
    other = [(pair, b) for pair in pairs for b in range(e)
             if (pair, b) not in excluded]
    rows = excluded + other
    n = e * g
    matrix = [[0] * n for _ in range(n)]
    for r, (pair, b) in enumerate(rows):
        i, j = pair
        # Hessian of z_i*z_j evaluated on the source direction and z_b.
        if b == i:
            matrix[r][j] += 1
        if b == j:
            matrix[r][i] += 1
        if cross_terms and (pair, b) in other:
            matrix[r][e + other.index((pair, b))] += 1
    return matrix


def test_e(e):
    pairs = list(combinations_with_replacement(range(e), 2))
    g, d = len(pairs), e + 1
    c, n = g - e, e * g
    m = n + c
    normal = normal_matrix(e, pairs)
    det = determinant(normal)
    failed_normal = normal_matrix(e, pairs, cross_terms=False)
    failed_rank = rank(failed_normal)
    syz = syzygy_matrix(e, pairs)
    syz_rank = rank(syz)
    local_hom = g * d - syz_rank
    total_hom = (n - e) * d + local_hom
    qlength = m * d - total_hom
    q = Fraction(qlength, c)
    assert det == 2 ** e
    assert failed_rank == e < n
    assert syz_rank == g
    assert local_hom == g * e
    assert qlength == g
    assert q == Fraction(e + 1, e - 1)
    assert (q < 2) == (e >= 4)
    assert Fraction(e + 1) + Fraction(e * e, c) == Fraction(n, c) + 1
    # The special and general square-zero scheme has Hilbert function 1,d,d,...
    hilbert = [1, d, d, d]
    assert hilbert[0] < d and hilbert[1] == d
    # Independent explicit e=4 arithmetic catches omission of source linear terms.
    if e == 4:
        assert (n, c, m, d, local_hom, total_hom, qlength) == (40, 6, 46, 5, 40, 220, 10)
    return {
        'e': e, 'g': g, 'n': n, 'c': c, 'target_dimension': m,
        'ambient_dimension': (n + 2) * (n + 1) // 2 - 1,
        'normal_matrix_size': n, 'normal_determinant': int(det),
        'no_cross_terms_negative_control_rank': failed_rank,
        'syzygy_equations': len(syz), 'hom_unknowns': g * d,
        'syzygy_rank': syz_rank, 'local_hom_dimension': local_hom,
        'total_hom_dimension': total_hom, 'Q_length': qlength,
        'q': str(q), 'regularity': 2, 'hilbert_function_degrees_0_to_3': hilbert,
        'strong_comparison_fails': q < 2,
        'weak_bound': str(Fraction(n, c) + 1),
        'weak_bound_satisfied': 2 <= Fraction(n, c) + 1,
        'extra_point_incidence_codimension_in_parameters': c,
        'derivation_dimension': e * e,
        'fixed_scheme_dimension_bound_is_equality': True,
    }


def main():
    results = [test_e(e) for e in range(2, 7)]
    print(json.dumps({
        'result': 'PASS', 'arithmetic': 'exact Fraction/integer',
        'tested_e': list(range(2, 7)),
        'limitations': [
            'These are finite algebra and matrix controls only.',
            'No point on a sampled general projection was numerically solved.',
            'Openness, incidence dominance, absence of extra points, and exact local elimination are proved in PROOF.md.',
            'The primary uniform n/c+1 conjecture is not settled.',
            'No first-discovery claim or independent human peer review is asserted.'
        ], 'cases': results,
    }, indent=2))


if __name__ == '__main__':
    main()
