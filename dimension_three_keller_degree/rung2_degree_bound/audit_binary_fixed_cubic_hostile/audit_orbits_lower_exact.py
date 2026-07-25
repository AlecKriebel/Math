#!/usr/bin/env python3
"""Independent hostile reconstruction of the binary fixed-cubic orbit tree.

This audit intentionally does not import the promoted verifier.  It rebuilds
the E7 matrices and the exceptional E6/E5/E4 systems from full 3-by-3
determinants over QQ (and only uses symbolic parameters where needed).
"""

from __future__ import annotations

import itertools
import sys

import sympy as sp

if not __debug__:
    print("FAIL: exact audit refuses optimized Python (-O)", file=sys.stderr)
    raise SystemExit(2)

p, q, r, z = sp.symbols("p q r z")
xyz = (p, q, r)
cub = (p**3, p**2 * q, p * q**2, q**3)
quad = (p**2, p * q, q**2)
allquad = (p**2, p * q, q**2, p * r, q * r, r**2)


def exact_zero(value):
    return sp.cancel(sp.expand(value)) == 0


def coeffs(value, gens=xyz):
    return [
        coefficient
        for _, coefficient in sp.Poly(sp.expand(value), *gens).terms()
    ]


def jac2(f, g):
    return sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p)


def e7_matrix(h, w, level):
    """Coefficient matrix of grad(w) adj(J(ph,qh)) (u,v) - 4h^2 tau."""
    dmat = sp.Matrix([p * h, q * h]).jacobian((p, q))
    row = sp.Matrix([[sp.diff(w, p), sp.diff(w, q)]]) * dmat.adjugate()
    if level == 2:
        unknowns = sp.symbols("c0:2")
        value = (row * sp.Matrix(unknowns))[0]
    elif level == 1:
        unknowns = sp.symbols("l0:5")
        uv = sp.Matrix(
            [
                unknowns[0] * p + unknowns[1] * q,
                unknowns[2] * p + unknowns[3] * q,
            ]
        )
        value = (row * uv)[0] - 4 * h**2 * unknowns[4]
    elif level == 0:
        unknowns = sp.symbols("b0:8")
        uv = sp.Matrix(
            [
                sum(unknowns[j] * quad[j] for j in range(3)),
                sum(unknowns[3 + j] * quad[j] for j in range(3)),
            ]
        )
        value = (row * uv)[0] - 4 * h**2 * (
            unknowns[6] * p + unknowns[7] * q
        )
    else:
        raise ValueError(level)
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(value, (p, q)), unknowns)
    assert rhs == sp.zeros(rhs.rows, 1)
    return unknowns, matrix


def e7_dims(h, w):
    return tuple(
        e7_matrix(h, w, level)[1].cols - e7_matrix(h, w, level)[1].rank()
        for level in (2, 1, 0)
    )


def rho(h, w):
    aa = jac2(q * h, w)
    bb = jac2(p * h, w)
    cc = jac2(p * h, q * h)
    common = sp.gcd(sp.gcd(aa, bb), cc)
    return sp.Poly(common, p, q).total_degree()


def maximal_minor_gcd(matrix, parameters):
    rank = matrix.rank()
    answer = None
    for rows in itertools.combinations(range(matrix.rows), rank):
        for columns in itertools.combinations(range(matrix.cols), rank):
            minor = sp.factor(matrix.extract(rows, columns).det())
            if minor == 0:
                continue
            poly = sp.Poly(minor, *parameters)
            answer = poly if answer is None else sp.gcd(answer, poly)
            if answer.total_degree() == 0:
                return sp.factor(answer.as_expr())
    assert answer is not None
    return sp.factor(answer.as_expr())


def same_parameter_divisor(observed, expected, parameters):
    quotient = sp.cancel(observed / expected)
    return quotient != 0 and not (quotient.free_symbols & set(parameters))


def check_top_and_local_formula():
    aa = sp.symbols("ha0:4")
    bb = sp.symbols("wa0:4")
    h = sum(aa[i] * cub[i] for i in range(4))
    w = sum(bb[i] * cub[i] for i in range(4))
    dmat = sp.Matrix([p * h, q * h]).jacobian((p, q))
    expected = (
        4 * h * sp.eye(2)
        - sp.Matrix([p, q])
        * sp.Matrix([[sp.diff(h, p), sp.diff(h, q)]])
    )
    assert exact_zero(dmat.det() - 4 * h**2)
    assert all(exact_zero(x) for x in dmat.adjugate() - expected)
    for m in range(1, 4):
        for n in range(0, 4):
            hm = p**m * q ** (3 - m)
            wm = p**n * q ** (3 - n)
            common = sp.gcd(
                sp.gcd(jac2(q * hm, wm), jac2(p * hm, wm)),
                jac2(p * hm, q * hm),
            )
            assert sp.Poly(common, p, q).terms()[-1][0][0] == min(
                2 * m, m + n - 1
            )
    print("PASS top adjugate identity and 12 local root-order instances")


def check_universal_low_rho_and_pivots():
    a, b, c, d = sp.symbols("a b c d")
    general_w = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3
    hs = p * q * (p - q)
    hd = p**2 * q
    ht = p**3

    # Squarefree h: these are exactly the three marked-root evaluations.
    m0 = e7_matrix(hs, general_w, 0)[1]
    assert m0.shape == (8, 8)
    assert exact_zero(
        m0.det() + 46656 * a**2 * d**2 * (a + b + c + d) ** 2
    )

    # Double h, rho=1: endpoint nonvanishing is the complete condition.
    md = e7_matrix(hd, general_w, 0)[1]
    assert md.shape == (7, 8)
    gcd_d = maximal_minor_gcd(md, (a, b, c, d))
    assert same_parameter_divisor(gcd_d, a**2 * d**2, (a, b, c, d))

    # Triple h: the unique rho=2 splitting jump is the affine quadratic
    # covariant 3*b*d-c^2; after depression this is the missing-linear chart.
    mt = e7_matrix(ht, general_w, 1)[1]
    assert mt.shape == (5, 5)
    assert exact_zero(mt.det() - 3456 * d**2 * (3 * b * d - c**2))

    A, B, lam = sp.symbols("A B lam")
    families = (
        ("s2a", hs, p**2 * (A * p + q), A, A**2 * (A + 1) ** 2),
        ("s2b", hs, p * q * (A * p + q), A, A**2 * (A + 1) ** 2),
        (
            "d2q",
            hd,
            q * (p**2 + B * p * q + q**2),
            B,
            (B - 2) * (B + 2),
        ),
        (
            "d2p",
            hd,
            p * (p**2 + B * p * q + q**2),
            B,
            (B - 2) * (B + 2),
        ),
        (
            "t2",
            ht,
            q**3 + p**2 * q + lam * p**3,
            lam,
            27 * lam**2 + 4,
        ),
    )
    for name, h, w, parameter, expected in families:
        normal_block = e7_matrix(h, w, 0)[1][:, :6]
        assert normal_block.shape == (6, 6)
        assert same_parameter_divisor(
            sp.factor(normal_block.det()), expected, (parameter,)
        ), name

    # The only finite-family r-multiplier jump is B=0 in d2q.
    r_d2q = e7_matrix(
        hd, q * (p**2 + B * p * q + q**2), 1
    )[1]
    assert same_parameter_divisor(r_d2q.det(), B, (B,))
    assert e7_dims(hd, p * (p**2 + q**2)) == (0, 0, 2)
    assert e7_dims(ht, p**3 + q**3) == (0, 1, 2)
    print("PASS universal rho<=2 ranks, split jumps, and every normal pivot")


def check_orbit_representatives_and_lower_leaves():
    hs = p * q * (p - q)
    hd = p**2 * q
    ht = p**3
    cases = (
        ("s0", hs, (p + 2 * q) * (p + 3 * q) * (p + 5 * q), 0, (0, 0, 0)),
        ("s1", hs, p * (p + 2 * q) * (p + 3 * q), 1, (0, 0, 1)),
        ("d1", hd, (p + q) * (p + 2 * q) * (p + 3 * q), 1, (0, 0, 1)),
        ("s2a", hs, p**2 * (2 * p + q), 2, (0, 0, 2)),
        ("s2b", hs, p * q * (2 * p + q), 2, (0, 0, 2)),
        ("d2q", hd, q * (p**2 + p * q + q**2), 2, (0, 0, 2)),
        ("d2p", hd, p * (p**2 + p * q + q**2), 2, (0, 0, 2)),
        ("t2g", ht, q**3 + p**2 * q, 2, (0, 0, 2)),
        ("d2q20", hd, q * (p**2 + q**2), 2, (0, 1, 2)),
        ("t220", ht, p**3 + q**3, 2, (0, 1, 2)),
        ("s3a", hs, p**2 * q, 3, (0, 1, 3)),
        ("s3b", hs, hs, 3, (0, 1, 3)),
        ("d3q", hd, q**2 * (p + q), 3, (0, 1, 3)),
        ("d3pq", hd, p * q * (p + q), 3, (0, 1, 3)),
        ("d3p", hd, p**2 * (p + q), 3, (0, 1, 3)),
        ("t3s", ht, p * q * (p - q), 3, (0, 1, 3)),
        ("t3d", ht, p * q**2, 3, (0, 1, 3)),
        ("d4a", hd, p * q**2, 4, (0, 2, 4)),
        ("d4b", hd, p**2 * q, 4, (0, 2, 4)),
        ("t4", ht, p**2 * (p + q), 4, (0, 2, 4)),
    )
    expected_lower = {
        "t3d": (sp.Rational(8, 5) * p, q, 0),
        "d4a": (sp.Rational(5, 2) * p, q, 0),
        "d4b": (-sp.Rational(1, 2) * p, q, 0),
        "t4": (4 * p, -3 * p + q, 0),
    }
    found = {}
    for name, h, w, expected_rho, expected_dims in cases:
        assert rho(h, w) == expected_rho, name
        assert e7_dims(h, w) == expected_dims, name
        _, lower_matrix = e7_matrix(h, w, 1)
        zero_normal_dimension = 4 - lower_matrix[:, :4].rank()
        assert zero_normal_dimension == (1 if name in expected_lower else 0)
        if name in expected_lower:
            nvec = expected_lower[name]
            dmat = sp.Matrix([p * h, q * h]).jacobian((p, q))
            row = (
                sp.Matrix([[sp.diff(w, p), sp.diff(w, q)]])
                * dmat.adjugate()
            )
            assert exact_zero(
                (row * sp.Matrix(nvec[:2]))[0] - 4 * h**2 * nvec[2]
            )
            found[name] = nvec
    assert set(found) == set(expected_lower)
    print("PASS all discrete orbit representatives and exactly four lower leaves")
    return {
        name: (next(h for n, h, _, _, _ in cases if n == name),
               next(w for n, _, w, _, _ in cases if n == name),
               vector)
        for name, vector in found.items()
    }


def weighted_determinant(h, w, h3_top, h2, linear):
    h3 = sp.Matrix([h3_top[0], h3_top[1], w])
    h4 = sp.Matrix([p * h, q * h, 0])
    return sp.Poly(
        sp.expand(
            (
                linear
                + z * h2.jacobian(xyz)
                + z**2 * h3.jacobian(xyz)
                + z**3 * h4.jacobian(xyz)
            ).det()
        ),
        z,
    )


def solve_linear_coefficient_system(value, unknowns):
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(value), unknowns)
    assert matrix.rank() == matrix.row_join(rhs).rank()
    solution = next(iter(sp.linsolve((matrix, rhs), unknowns)))
    substitutions = {
        unknowns[i]: solution[i]
        for i in range(len(unknowns))
        if solution[i] != unknowns[i]
    }
    return matrix, substitutions


def direct_lower_constant(name, h, w, normal, expected):
    uu = sp.symbols(f"{name}u0:8")
    aa = sp.symbols(f"{name}a0:9")
    ll = sp.symbols(f"{name}l0:8")
    h3_top = (
        sum(uu[i] * cub[i] for i in range(4)),
        sum(uu[4 + i] * cub[i] for i in range(4)),
    )
    h2 = sp.Matrix(
        [
            sum(aa[i] * quad[i] for i in range(3)) + r * normal[0],
            sum(aa[3 + i] * quad[i] for i in range(3)) + r * normal[1],
            sum(aa[6 + i] * quad[i] for i in range(3)),
        ]
    )
    linear = sp.Matrix(
        [[ll[0], ll[1], ll[2]], [ll[3], ll[4], ll[5]], [ll[6], ll[7], 0]]
    )
    weighted = weighted_determinant(h, w, h3_top, h2, linear)
    for degree in (8, 7, 6):
        assert exact_zero(weighted.coeff_monomial(z**degree))
    unknowns = uu + aa + (ll[2], ll[5])
    matrix, substitutions = solve_linear_coefficient_system(
        weighted.coeff_monomial(z**5), unknowns
    )
    residual = coeffs(
        weighted.coeff_monomial(z**4).subs(substitutions)
    )
    all_symbols = set(uu + aa + ll)
    constants = [
        sp.factor(item)
        for item in residual
        if item != 0 and not (item.free_symbols & all_symbols)
    ]
    assert expected in constants
    return matrix.shape, matrix.rank(), constants


def direct_fixed_e7_constant(name, h, w, normal, expected):
    uu = sp.symbols(f"{name}u0:8")
    aa = sp.symbols(f"{name}a0:15")
    ll = sp.symbols(f"{name}l0:9")
    h3_top = (
        sum(uu[i] * cub[i] for i in range(4)) + r * normal[0],
        sum(uu[4 + i] * cub[i] for i in range(4)) + r * normal[1],
    )
    h2 = sp.Matrix(
        [
            sum(aa[i] * allquad[i] for i in range(6)),
            sum(aa[6 + i] * allquad[i] for i in range(6)),
            sum(aa[12 + i] * quad[i] for i in range(3)),
        ]
    )
    linear = sp.Matrix(3, 3, ll)
    weighted = weighted_determinant(h, w, h3_top, h2, linear)
    assert exact_zero(weighted.coeff_monomial(z**8))
    assert exact_zero(weighted.coeff_monomial(z**7))
    unknowns = uu + aa + (ll[8],)
    matrix, substitutions = solve_linear_coefficient_system(
        weighted.coeff_monomial(z**6), unknowns
    )
    residual = coeffs(
        weighted.coeff_monomial(z**5).subs(substitutions)
    )
    all_symbols = set(uu + aa + ll)
    constants = [
        sp.factor(item)
        for item in residual
        if item != 0 and not (item.free_symbols & all_symbols)
    ]
    assert expected in constants
    return matrix.shape, matrix.rank(), constants


def check_all_e7_and_lower_constants(leaves):
    expected_e7 = {
        "t3d": (sp.Rational(8, 5) * p**2, p * q, 0, sp.Rational(24, 25)),
        "d4a": (sp.Rational(5, 2) * p**2, p * q, 0, sp.Integer(15)),
        "d4b": (-sp.Rational(1, 2) * p**2, p * q, 0, sp.Rational(3, 2)),
        "t4": (4 * p**2, -p * (3 * p - q), 0, sp.Integer(-12)),
    }
    expected_lower = {
        "t3d": sp.Rational(-24, 5),
        "d4a": sp.Rational(-15, 2),
        "d4b": sp.Rational(3, 2),
        "t4": sp.Integer(-12),
    }
    for name, (h, w, lower) in leaves.items():
        e7_data = expected_e7[name]
        e7_result = direct_fixed_e7_constant(
            name + "E7", h, w, e7_data[:3], e7_data[3]
        )
        lower_result = direct_lower_constant(
            name + "low", h, w, lower, expected_lower[name]
        )
        print(
            f"PASS {name}: E7 {e7_result[0]}/{e7_result[1]} "
            f"contains {e7_data[3]}; lower {lower_result[0]}/"
            f"{lower_result[1]} contains {expected_lower[name]}"
        )


def main():
    check_top_and_local_formula()
    check_universal_low_rho_and_pivots()
    leaves = check_orbit_representatives_and_lower_leaves()
    check_all_e7_and_lower_constants(leaves)
    print("ALL INDEPENDENT ORBIT/LOWER CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
