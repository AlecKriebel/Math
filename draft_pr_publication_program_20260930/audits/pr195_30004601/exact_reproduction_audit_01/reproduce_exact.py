#!/usr/bin/env python3
"""Independent standard-library exact reproduction for PR195.

No candidate or previous review implementation is imported. Run with Python 3.10+
and no third-party packages. The default emits a deterministic JSON certificate;
--verify PATH recomputes it and requires exact byte equality with PATH.
"""
from fractions import Fraction as F
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path


def add(a, b):
    c = dict(a)
    for e, q in b.items():
        c[e] = c.get(e, 0) + q
        if not c[e]:
            del c[e]
    return c


def scale(a, q):
    return {e: q*v for e, v in a.items() if q*v}


def mul(a, b):
    c = {}
    for e, q in a.items():
        for f, r in b.items():
            g = tuple(x+y for x, y in zip(e, f))
            c[g] = c.get(g, 0) + q*r
            if not c[g]:
                del c[g]
    return c


def linear(coefficients):
    n = len(coefficients)
    return {tuple(int(i == j) for i in range(n)): F(q)
            for j, q in enumerate(coefficients) if q}


def one(n):
    return {(0,)*n: F(1)}


def powpoly(a, k):
    n = len(next(iter(a)))
    v = one(n)
    for _ in range(k):
        v = mul(v, a)
    return v


def derivative(a, j):
    c = {}
    for e, q in a.items():
        if e[j]:
            f = list(e)
            f[j] -= 1
            c[tuple(f)] = q*e[j]
    return c


def substitute(a, forms):
    n = len(next(iter(forms[0])))
    c = {}
    for e, q in a.items():
        v = scale(one(n), q)
        for f, exponent in zip(forms, e):
            v = mul(v, powpoly(f, exponent))
        c = add(c, v)
    return c


def monomials(n, d):
    if n == 1:
        return [(d,)]
    return [(i,)+e for i in range(d, -1, -1)
            for e in monomials(n-1, d-i)]


def rref(rows):
    if not rows:
        return [], []
    a = [[F(x) for x in row] for row in rows]
    r = 0
    pivots = []
    for j in range(len(a[0])):
        k = next((k for k in range(r, len(a)) if a[k][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        q = a[r][j]
        a[r] = [x/q for x in a[r]]
        for k in range(len(a)):
            if k != r and a[k][j]:
                q = a[k][j]
                a[k] = [x-q*y for x, y in zip(a[k], a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    return a, pivots


def transpose(a):
    return [list(v) for v in zip(*a)]


def nullspace(a):
    rr, pivots = rref(a)
    if not a:
        return []
    basis = []
    for j in range(len(a[0])):
        if j in pivots:
            continue
        v = [F(0)]*len(a[0])
        v[j] = F(1)
        for k, p in enumerate(pivots):
            v[p] = -rr[k][j]
        assert all(sum(q*x for q, x in zip(row, v)) == 0 for row in a)
        basis.append(v)
    return basis


def determinant(a):
    a = [[F(x) for x in row] for row in a]
    det = F(1)
    for j in range(len(a)):
        k = next((k for k in range(j, len(a)) if a[k][j]), None)
        if k is None:
            return F(0)
        if k != j:
            a[j], a[k] = a[k], a[j]
            det *= -1
        p = a[j][j]
        det *= p
        for k in range(j+1, len(a)):
            q = a[k][j]/p
            for i in range(j+1, len(a)):
                a[k][i] -= q*a[j][i]
            a[k][j] = F(0)
    return det


def qstr(q):
    q = F(q)
    return str(q.numerator) if q.denominator == 1 else str(q)


def polyrecord(a):
    return [{"exponents": list(e), "coefficient": qstr(a[e])}
            for e in sorted(a, reverse=True)]


def vec_to_syzygy(v, n, d):
    mons = monomials(n, d)
    return [{e: q for e, q in zip(mons, v[j*len(mons):(j+1)*len(mons)]) if q}
            for j in range(4)]


def syzygy_to_vec(s, n, d):
    return [F(a.get(e, 0)) for a in s for e in monomials(n, d)]


def syz_mul(s, a):
    return [mul(x, a) for x in s]


def relation(fs, s):
    a = {}
    for f, q in zip(fs, s):
        a = add(a, mul(f, q))
    return a


def macaulay(fs, n, degree):
    mons = monomials(n, degree)
    source = [(j, m) for j in range(4) for m in monomials(n, degree-6)]
    rows = []
    for j, m in source:
        v = mul(fs[j], {m: F(1)})
        rows.append([v.get(e, F(0)) for e in mons])
    _, independent_rows = rref(transpose(rows))
    _, pivots = rref(rows)
    minor = [[rows[i][j] for j in pivots] for i in independent_rows]
    det = determinant(minor)
    assert len(independent_rows) == len(pivots) and det
    kernel = nullspace(transpose(rows))
    assert len(kernel) + len(pivots) == len(rows)
    for v in kernel:
        assert not relation(fs, vec_to_syzygy(v, n, degree-6))
    rec = {
        "variables": n, "degree": degree,
        "rows": len(rows), "columns": len(mons), "rank": len(pivots),
        "quotient_dimension": len(mons)-len(pivots),
        "monomial_order": [list(m) for m in mons],
        "source_order": [{"generator": j, "monomial": list(m)} for j, m in source],
        "matrix": [[qstr(q) for q in row] for row in rows],
        "rank_minor_rows": independent_rows, "rank_minor_columns": pivots,
        "rank_minor_determinant": qstr(det),
        "left_kernel_basis": [[qstr(q) for q in v] for v in kernel],
    }
    return rec, kernel


def polynomial_determinant(a):
    if len(a) == 1:
        return dict(a[0][0])
    result = {}
    for j in range(len(a)):
        minor = [[r[k] for k in range(len(a)) if k != j] for r in a[1:]]
        result = add(result, scale(mul(a[0][j], polynomial_determinant(minor)), (-1)**j))
    return result


def build_hilbert_burch(binary, matrices):
    chosen = []
    for d in (1, 2, 3):
        span = []
        for degree, s in chosen:
            for m in monomials(2, d-degree):
                span.append(syzygy_to_vec(syz_mul(s, {m: F(1)}), 2, d))
        oldrank = len(rref(span)[1]) if span else 0
        candidates = matrices[d][1]
        added = []
        for v in candidates:
            newrank = len(rref(span+[v])[1])
            if newrank > oldrank:
                s = vec_to_syzygy(v, 2, d)
                assert not relation(binary, s)
                added.append((d, s))
                span.append(v)
                oldrank = newrank
        assert len(added) == 1
        chosen.extend(added)
        assert oldrank == len(candidates)
    matrix = [[chosen[j][1][i] for j in range(3)] for i in range(4)]
    signed_minors = []
    common_factor = None
    for i in range(4):
        minor = [row for j, row in enumerate(matrix) if j != i]
        v = scale(polynomial_determinant(minor), (-1)**i)
        assert v and binary[i]
        exponent = next(iter(binary[i]))
        q = v.get(exponent, 0)/binary[i][exponent]
        assert v == scale(binary[i], q) and q
        if common_factor is None:
            common_factor = q
        assert q == common_factor
        signed_minors.append(v)
    return {
        "column_degrees": [d for d, _ in chosen],
        "matrix": [[polyrecord(v) for v in row] for row in matrix],
        "signed_maximal_minors": [polyrecord(v) for v in signed_minors],
        "signed_maximal_minors_equal_polars_times": qstr(common_factor),
        "all_columns_exact_syzygies": True,
    }, chosen


def coefficient_syzygy_dimension(forms):
    """Directly solve factor divisibility plus sum of seven scalars.

    Unknowns are 4*r coefficients of ambient polar multipliers followed by
    seven factor scalars. This derives the open-flag scalar description by a
    separate linear system, without using a polynomial Macaulay matrix.
    """
    n = len(next(iter(forms[0])))
    original_factors = [(1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),
                        (0,0,1,0),(0,0,0,1),(1,0,1,1)]
    restricted = [substitute(linear(v), forms) for v in original_factors]
    rows = []
    basis = monomials(n, 1)
    for i, (ambient, restricted_factor) in enumerate(zip(original_factors, restricted)):
        for k, e in enumerate(basis):
            row = [F(0)]*(4*n+7)
            for j in range(4):
                row[j*n+k] = F(ambient[j])
            row[4*n+i] = -restricted_factor.get(e, F(0))
            rows.append(row)
    rows.append([F(0)]*(4*n)+[F(1)]*7)
    kernel = nullspace(rows)
    return {"unknowns": 4*n+7, "equations": len(rows), "rank": len(rref(rows)[1]),
            "nullity": len(kernel), "basis": [[qstr(q) for q in v] for v in kernel]}


def certificate():
    factors = [(1,0,0,0),(0,1,0,0),(1,-1,0,0),(1,-2,0,0),
               (0,0,1,0),(0,0,0,1),(1,0,1,1)]
    Q = one(4)
    for coefficients in factors:
        Q = mul(Q, linear(coefficients))
    polars = [derivative(Q, j) for j in range(4)]
    coordinates = [linear(tuple(int(i == j) for i in range(4))) for j in range(4)]
    assert relation(polars, coordinates) == scale(Q, 7)
    ternary_flag = [linear(v) for v in [(1,0,0),(0,1,0),(0,0,1),(1,2,3)]]
    binary_flag = [linear(v) for v in [(1,0),(0,1),(2,3),(7,11)]]
    ternary = [substitute(f, ternary_flag) for f in polars]
    binary = [substitute(f, binary_flag) for f in polars]
    from_ternary = [substitute(f, [linear((1,0)),linear((0,1)),linear((2,3))])
                    for f in ternary]
    assert from_ternary == binary
    ternary_matrices = [macaulay(ternary, 3, d)[0] for d in (6, 7)]
    binary_matrices = {d: macaulay(binary, 2, 6+d) for d in range(4)}
    assert [m['rank'] for m in ternary_matrices] == [4, 12]
    assert [binary_matrices[d][0]['rank'] for d in range(3)] == [4, 7, 9]
    hb, chosen = build_hilbert_burch(binary, binary_matrices)
    prescribed = [linear((11,0)),linear((0,11)),linear((-146,-219)),linear((175,275))]
    assert not relation(binary, prescribed)
    rational_ratio = None
    for a, b in zip(chosen[0][1], prescribed):
        for exponent in set(a)|set(b):
            if b.get(exponent, 0):
                q = a.get(exponent, 0)/b[exponent]
                rational_ratio = q if rational_ratio is None else rational_ratio
                assert q == rational_ratio
            else:
                assert not a.get(exponent, 0)
    assert rational_ratio
    # A basis for the three-factor relation is (1,-11,3).
    assert not add(add(binary_flag[0], scale(binary_flag[2], -11)), scale(binary_flag[3], 3))
    scalar_ternary = coefficient_syzygy_dimension(ternary_flag)
    scalar_binary = coefficient_syzygy_dimension(binary_flag)
    assert scalar_ternary['nullity'] == 0 and scalar_binary['nullity'] == 1
    return {
        "schema": "PR195_independent_standard_library_exact_certificate_v1",
        "field": "Q", "ambient_polynomial": polyrecord(Q),
        "ambient_polars": [polyrecord(f) for f in polars],
        "ternary_polars": [polyrecord(f) for f in ternary],
        "binary_polars": [polyrecord(f) for f in binary],
        "Euler_identity_sum_variables_times_polars_equals_7Q": True,
        "ternary_then_binary_restriction_equals_direct_binary": True,
        "ternary_Macaulay": ternary_matrices,
        "binary_Macaulay": [binary_matrices[d][0] for d in range(4)],
        "binary_primitive_syzygy_degrees": [1,2,3],
        "binary_Hilbert_Burch": hb,
        "candidate_displayed_syzygy_verified": [polyrecord(a) for a in prescribed],
        "independent_linear_kernel_to_displayed_syzygy_ratio": qstr(rational_ratio),
        "factor_scalar_system_ternary": scalar_ternary,
        "factor_scalar_system_binary": scalar_binary,
        "claim_scope": "Exact flags corroborate algebraic generic-open proof; sampling is not a proof of genericity.",
    }


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True)+"\n").encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', type=Path)
    args = parser.parse_args()
    result = encoded(certificate())
    if args.verify:
        assert args.verify.read_bytes() == result, "certificate mismatch"
        print(json.dumps({"verified": True, "certificate_bytes": len(result),
                          "certificate_sha256": hashlib.sha256(result).hexdigest()}))
    else:
        print(result.decode(), end='')


if __name__ == '__main__':
    main()
