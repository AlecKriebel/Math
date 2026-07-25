#!/usr/bin/env python3
"""Independent full-determinant audit of every exceptional E6 branch."""

from __future__ import annotations

import itertools
import sys

import sympy as sp

from audit_orbits_lower_exact import (
    allquad,
    coeffs,
    cub,
    e7_matrix,
    exact_zero,
    p,
    q,
    quad,
    r,
    xyz,
    z,
)

if not __debug__:
    print("FAIL: exact audit refuses optimized Python (-O)", file=sys.stderr)
    raise SystemExit(2)


def tangent_bases(h, w):
    output = {}
    for level in (1, 0):
        _, matrix = e7_matrix(h, w, level)
        vectors = matrix.nullspace()
        if level == 1:
            output[level] = [
                (
                    v[0] * p + v[1] * q,
                    v[2] * p + v[3] * q,
                    v[4],
                )
                for v in vectors
            ]
        else:
            output[level] = [
                (
                    sum(v[i] * quad[i] for i in range(3)),
                    sum(v[3 + i] * quad[i] for i in range(3)),
                    v[6] * p + v[7] * q,
                )
                for v in vectors
            ]
    return output


def build_system(prefix, h, w, derivative):
    uu = sp.symbols(f"{prefix}u0:8")
    aa = sp.symbols(f"{prefix}a0:15")
    ll = sp.symbols(f"{prefix}l0:9")
    h3 = sp.Matrix(
        [
            sum(uu[i] * cub[i] for i in range(4))
            + sp.integrate(derivative[0], r),
            sum(uu[4 + i] * cub[i] for i in range(4))
            + sp.integrate(derivative[1], r),
            w,
        ]
    )
    h2 = sp.Matrix(
        [
            sum(aa[i] * allquad[i] for i in range(6)),
            sum(aa[6 + i] * allquad[i] for i in range(6)),
            sum(aa[12 + i] * quad[i] for i in range(3))
            + sp.integrate(derivative[2], r),
        ]
    )
    linear = sp.Matrix(3, 3, ll)
    dmat = sp.Matrix([p * h, q * h]).jacobian((p, q))
    bmat = sp.Matrix(h3[:2, :]).jacobian((p, q))
    top_derivative = sp.Matrix(
        [sp.diff(h3[0], r), sp.diff(h3[1], r)]
    )
    wrow = sp.Matrix([[sp.diff(w, p), sp.diff(w, q)]])
    atop = sp.Matrix(h2[:2, :])
    ar = sp.Matrix([sp.diff(atop[0], r), sp.diff(atop[1], r)])
    trow = sp.Matrix([[sp.diff(h2[2], p), sp.diff(h2[2], q)]])
    tau = sp.diff(h2[2], r)
    e6 = sp.expand(
        dmat.det() * ll[8]
        + sp.trace(bmat.adjugate() * dmat) * tau
        - (wrow * dmat.adjugate() * ar)[0]
        - (wrow * bmat.adjugate() * top_derivative)[0]
        - (trow * dmat.adjugate() * top_derivative)[0]
    )
    unknowns = uu + aa + (ll[8],)
    matrix, rhs = sp.linear_eq_to_matrix(coeffs(e6), unknowns)
    return {
        "h": h,
        "w": w,
        "u": uu,
        "a": aa,
        "l": ll,
        "h3": h3,
        "h2": h2,
        "linear": linear,
        "e6": e6,
        "unknowns": unknowns,
        "matrix": matrix,
        "rhs": rhs,
    }


def full_weighted(system):
    h4 = sp.Matrix([p * system["h"], q * system["h"], 0])
    weighted = sp.Poly(
        sp.expand(
            (
                system["linear"]
                + z * system["h2"].jacobian(xyz)
                + z**2 * system["h3"].jacobian(xyz)
                + z**3 * h4.jacobian(xyz)
            ).det()
        ),
        z,
    )
    assert exact_zero(weighted.coeff_monomial(z**6) - system["e6"])
    return weighted


def combined_derivative(h, w, prefix, include_r=True):
    bases = tangent_bases(h, w)
    rpars = sp.symbols(f"{prefix}g0:{len(bases[1])}")
    zpars = sp.symbols(f"{prefix}k0:{len(bases[0])}")
    derivative = []
    for coordinate in range(3):
        value = sum(
            rpars[i] * r * bases[1][i][coordinate]
            for i in range(len(rpars))
        )
        value += sum(
            zpars[i] * bases[0][i][coordinate]
            for i in range(len(zpars))
        )
        derivative.append(sp.expand(value))
    if not include_r:
        derivative = [
            sp.expand(
                sum(
                    zpars[i] * bases[0][i][coordinate]
                    for i in range(len(zpars))
                )
            )
            for coordinate in range(3)
        ]
    return tuple(derivative), rpars, zpars, bases


def left_pairings(matrix, rhs):
    output = []
    for vector in matrix.T.nullspace():
        denominators = [
            sp.together(item).as_numer_denom()[1] for item in vector
        ]
        common = sp.lcm(denominators)
        cleared = sp.Matrix([sp.cancel(common * item) for item in vector])
        assert all(exact_zero(item) for item in matrix.T * cleared)
        pairing = sp.factor(sp.expand(cleared.dot(rhs)))
        if pairing != 0:
            output.append(pairing)
    return output


def has_constant_multiple(values, target, parameters):
    for value in values:
        quotient = sp.cancel(value / target)
        if quotient != 0 and not (quotient.free_symbols & set(parameters)):
            return True
    return False


def check_raw_ranks():
    hs = p * q * (p - q)
    hd = p**2 * q
    ht = p**3
    cases = (
        ("rho1s", hs, p * (p + 2 * q) * (p + 3 * q), (12, 24), 9, None),
        ("rho1d", hd, (p + q) * (p + 2 * q) * (p + 3 * q), (13, 24), 9, None),
        ("s2a", hs, p**2 * (2 * p + q), (13, 24), 9, None),
        ("s2b", hs, p * q * (2 * p + q), (11, 24), 9, None),
        ("d2q", hd, q * (p**2 + p * q + q**2), (12, 24), 9, None),
        ("d2p", hd, p * (p**2 + p * q + q**2), (12, 24), 9, None),
        ("t2g", ht, q**3 + p**2 * q, (13, 24), 9, None),
        ("d2q20", hd, q * (p**2 + q**2), (19, 24), 10, ((12, 24), 9)),
        ("t220", ht, p**3 + q**3, (19, 24), 10, ((13, 24), 9)),
        ("s3a", hs, p**2 * q, (20, 24), 10, ((12, 24), 9)),
        ("s3b", hs, hs, (18, 24), 10, ((11, 24), 9)),
        ("d3q", hd, q**2 * (p + q), (22, 24), 10, ((13, 24), 9)),
        ("d3pq", hd, p * q * (p + q), (18, 24), 10, ((11, 24), 9)),
        ("d3p", hd, p**2 * (p + q), (16, 24), 10, ((10, 24), 8)),
        ("t3s", ht, p * q * (p - q), (20, 24), 10, ((12, 24), 9)),
        ("t3d", ht, p * q**2, (17, 24), 10, ((12, 24), 9)),
        ("d4a", hd, p * q**2, (20, 24), 9, ((12, 24), 9)),
        ("d4b", hd, p**2 * q, (14, 24), 9, ((9, 24), 8)),
        ("t4", ht, p**2 * (p + q), (16, 24), 9, ((10, 24), 8)),
    )
    for name, h, w, shape, rank, r0_expected in cases:
        derivative, _, _, _ = combined_derivative(h, w, "rr" + name)
        system = build_system("rs" + name, h, w, derivative)
        assert system["matrix"].shape == shape, name
        assert system["matrix"].rank() == rank, name
        if r0_expected:
            derivative0, _, _, _ = combined_derivative(
                h, w, "rz" + name, include_r=False
            )
            system0 = build_system("rt" + name, h, w, derivative0)
            assert system0["matrix"].shape == r0_expected[0], name
            assert system0["matrix"].rank() == r0_expected[1], name
    print("PASS every displayed raw E6 shape and rank")


def check_r_multiplier_squares():
    hs = p * q * (p - q)
    hd = p**2 * q
    ht = p**3
    cases = (
        ("d2q20", hd, q * (p**2 + q**2)),
        ("t220", ht, p**3 + q**3),
        ("s3a", hs, p**2 * q),
        ("s3b", hs, hs),
        ("d3q", hd, q**2 * (p + q)),
        ("d3pq", hd, p * q * (p + q)),
        ("d3p", hd, p**2 * (p + q)),
        ("t3s", ht, p * q * (p - q)),
        ("t3d", ht, p * q**2),
    )
    gamma = sp.symbols("gamma")
    for name, h, w in cases:
        basis = tangent_bases(h, w)[1]
        assert len(basis) == 1
        derivative = tuple(gamma * r * item for item in basis[0])
        system = build_system("sq" + name, h, w, derivative)
        high = sp.Poly(system["e6"], r).coeff_monomial(r**3)
        lower = set(system["unknowns"])
        constants = [
            sp.cancel(item / gamma**2)
            for item in coeffs(high, (p, q))
            if item != 0
            and not (sp.cancel(item / gamma**2).free_symbols & lower)
        ]
        assert any(item != 0 for item in constants), name
    print("PASS all nine rho=2/3 r-multipliers die by literal E6 squares")


def check_pivots_and_zero_normal_kernels():
    hd = p**2 * q
    ht = p**3
    root = sp.sqrt(3) * sp.I
    pivots = (
        (
            "d2q+",
            hd,
            q * (p + q) ** 2,
            (p**2 / 6 + 3 * p * q / 2, -p * q / 3 + q**2, 0),
        ),
        (
            "d2q-",
            hd,
            q * (p - q) ** 2,
            (-p**2 / 6 + 3 * p * q / 2, p * q / 3 + q**2, 0),
        ),
        (
            "d2p+",
            hd,
            p * (p + q) ** 2,
            (-3 * p**2 / 2 + 5 * p * q / 2, -3 * p * q + q**2, 0),
        ),
        (
            "d2p-",
            hd,
            p * (p - q) ** 2,
            (3 * p**2 / 2 + 5 * p * q / 2, 3 * p * q + q**2, 0),
        ),
        (
            "t2+",
            ht,
            q**3 + p**2 * q + 2 * root * p**3 / 9,
            (
                -4 * root * p**2 / 9 + 4 * p * q / 3,
                -2 * p**2 / 9 - root * p * q / 3 + q**2,
                0,
            ),
        ),
        (
            "t2-",
            ht,
            q**3 + p**2 * q - 2 * root * p**3 / 9,
            (
                4 * root * p**2 / 9 + 4 * p * q / 3,
                -2 * p**2 / 9 + root * p * q / 3 + q**2,
                0,
            ),
        ),
    )
    for name, h, w, normal in pivots:
        system = build_system("pv" + name, h, w, normal)
        assert system["matrix"].rank() < system["matrix"].row_join(
            system["rhs"]
        ).rank(), name

    hs = p * q * (p - q)
    unique = (
        ("s3a", hs, p**2 * q),
        ("s3b", hs, hs),
        ("d3q", hd, q**2 * (p + q)),
        ("d3pq", hd, p * q * (p + q)),
        ("d3p", hd, p**2 * (p + q)),
        ("t3s", ht, p * q * (p - q)),
    )
    for name, h, w in unique:
        matrix = e7_matrix(h, w, 0)[1][:, :6]
        kernel = matrix.nullspace()
        assert len(kernel) == 1
        vector = kernel[0]
        normal = (
            sum(vector[i] * quad[i] for i in range(3)),
            sum(vector[3 + i] * quad[i] for i in range(3)),
            0,
        )
        system = build_system("uq" + name, h, w, normal)
        assert system["matrix"].rank() < system["matrix"].row_join(
            system["rhs"]
        ).rank(), name

    higher = (
        ("t3d", ht, p * q**2),
        ("d4a", hd, p * q**2),
        ("d4b", hd, p**2 * q),
        ("t4", ht, p**2 * (p + q)),
    )
    for name, h, w in higher:
        matrix = e7_matrix(h, w, 0)[1][:, :6]
        kernel = matrix.nullspace()
        assert len(kernel) == 2
        x, y = sp.symbols(f"{name}x {name}y")
        vector = x * kernel[0] + y * kernel[1]
        normal = (
            sum(vector[i] * quad[i] for i in range(3)),
            sum(vector[3 + i] * quad[i] for i in range(3)),
            0,
        )
        system = build_system("hq" + name, h, w, normal)
        pairings = left_pairings(system["matrix"], system["rhs"])
        assert has_constant_multiple(pairings, y**2, (x, y)), name
    print("PASS both signs of every pivot and every zero-normal E6 kernel")


def check_delta4_compatibility_tree():
    hd = p**2 * q
    ht = p**3
    cases = (
        ("d4a", hd, p * q**2),
        ("d4b", hd, p**2 * q),
        ("t4", ht, p**2 * (p + q)),
    )
    for name, h, w in cases:
        derivative, rpars, zpars, _ = combined_derivative(
            h, w, "dt" + name
        )
        system = build_system("ds" + name, h, w, derivative)
        values = left_pairings(system["matrix"], system["rhs"])
        parameters = rpars + zpars
        g0, g1 = rpars
        if name == "d4a":
            assert has_constant_multiple(values, g0**2, parameters)
            assert has_constant_multiple(values, g1**2, parameters)
        elif name == "d4b":
            assert has_constant_multiple(
                values, 3 * g0**2 - 8 * g0 * g1 + 8 * g1**2, parameters
            )
            assert has_constant_multiple(
                values,
                (3 * g0 - 4 * g1) * zpars[0]
                + (-4 * g0 + 8 * g1) * zpars[2],
                parameters,
            )
            assert has_constant_multiple(
                values,
                (3 * g0 - 4 * g1) * zpars[1]
                + (-4 * g0 + 8 * g1) * zpars[3],
                parameters,
            )
        else:
            assert has_constant_multiple(values, g0**2, parameters)
            specialized = tuple(item.subs(g0, 0) for item in derivative)
            system0 = build_system("tz", h, w, specialized)
            values0 = left_pairings(system0["matrix"], system0["rhs"])
            params0 = (g1,) + zpars
            assert has_constant_multiple(values0, g1 * zpars[1], params0)
            assert has_constant_multiple(
                values0, g1 * (-zpars[0] - 3 * zpars[1] + zpars[3]), params0
            )
    print("PASS complete division-free delta=4 compatibility tree")


def reduce_quadratic(value, generator, relation):
    numerator, denominator = sp.together(value).as_numer_denom()
    numerator = sp.rem(numerator, relation, generator)
    denominator = sp.rem(denominator, relation, generator)
    inverse = sp.invert(denominator, relation, generator)
    return sp.cancel(sp.rem(numerator * inverse, relation, generator))


def quotient_rank(matrix, generator, relation):
    rows = [
        [
            reduce_quadratic(matrix[i, j], generator, relation)
            for j in range(matrix.cols)
        ]
        for i in range(matrix.rows)
    ]
    pivot = 0
    for column in range(matrix.cols):
        selected = next(
            (row for row in range(pivot, matrix.rows) if rows[row][column] != 0),
            None,
        )
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        scale = rows[pivot][column]
        rows[pivot] = [
            reduce_quadratic(item / scale, generator, relation)
            for item in rows[pivot]
        ]
        for row in range(matrix.rows):
            if row == pivot or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                reduce_quadratic(
                    rows[row][j] - scale * rows[pivot][j], generator, relation
                )
                for j in range(matrix.cols)
            ]
        pivot += 1
        if pivot == matrix.rows:
            break
    return pivot


def check_d4b_algebraic_branch():
    alpha, beta, gamma = sp.symbols("alpha beta gamma")
    relation = 3 * gamma**2 - 8 * gamma + 8
    r1 = (-p / 2, q, 0)
    r2 = (2 * p, 0, 1)
    kappa = 1 - 3 * gamma / 8
    derivative = tuple(
        sp.expand(
            r * (gamma * r1[j] + r2[j])
            + (alpha * p + beta * q) * (r1[j] + kappa * r2[j])
        )
        for j in range(3)
    )
    system = build_system("ga", p**2 * q, p**2 * q, derivative)
    weighted = full_weighted(system)
    uu, aa, ll = system["u"], system["a"], system["l"]
    substitution = {
        uu[0]: (
            6 * aa[11] * gamma
            - 4 * aa[11]
            + 16 * aa[12]
            - 3 * uu[5] * gamma
            + 2 * uu[5]
        )
        / 12,
        uu[1]: (
            4 * aa[13] * gamma
            + 8 * aa[5]
            - 3 * uu[6] * gamma
            + 2 * uu[6]
        )
        / 4,
        uu[2]: (8 * aa[14] - 3 * uu[7]) * (gamma + 2) / 12,
        uu[3]: 0,
        uu[4]: 0,
        aa[3]: -(
            6 * alpha * aa[5] * gamma
            - 16 * alpha * aa[5]
            + 3 * beta * aa[11] * gamma
            - 8 * beta * aa[11]
            + 4 * aa[10]
            - 16 * ll[8]
        )
        / 8,
        aa[4]: -beta * aa[5] * (3 * gamma - 8) / 4,
        aa[9]: -alpha * aa[11] * (3 * gamma - 8) / 4,
    }
    assert quotient_rank(system["matrix"], gamma, relation) == 8
    assert all(
        reduce_quadratic(item.subs(substitution), gamma, relation) == 0
        for item in coeffs(system["e6"])
    )
    residual = [
        reduce_quadratic(item.subs(substitution), gamma, relation)
        for item in coeffs(weighted.coeff_monomial(z**5))
    ]
    assert any(
        exact_zero(item - (gamma + 2) / 6) for item in residual
    )
    assert reduce_quadratic(gamma + 2, gamma, relation) != 0
    print("PASS both conjugate d4b r-branches: E5 contains (gamma+2)/6")


def contains_numeric_multiple(values, target):
    return any(
        (lambda quotient: quotient != 0 and not quotient.free_symbols)(
            sp.cancel(value / target)
        )
        for value in values
        if value != 0
    )


def check_t4_branch_with_converse_pivots():
    alpha, beta = sp.symbols("alpha beta")
    r2 = (0, p, 1)
    n1 = (4 * p**2, -p * (3 * p - q), 0)
    n3 = (0, p**2, p)
    n4 = (-4 * p**2, 3 * p**2, q)
    derivative = tuple(
        sp.expand(r * r2[j] + alpha * n1[j] + beta * n3[j] + alpha * n4[j])
        for j in range(3)
    )
    system = build_system("ta", p**3, p**2 * (p + q), derivative)
    weighted = full_weighted(system)
    uu, aa, ll = system["u"], system["a"], system["l"]
    sub6 = {
        uu[1]: 2 * (-4 * aa[14] + aa[5] + 4 * uu[6] + 18 * uu[7]),
        uu[2]: 6 * uu[7],
        uu[3]: 0,
        uu[5]: 2 * aa[11] + aa[13] + 6 * aa[14] - 6 * uu[6] - 27 * uu[7],
        aa[3]: -2 * (4 * alpha * aa[11] - beta * aa[5] - 2 * aa[10]),
        aa[4]: 2 * alpha * aa[5],
        aa[9]: 6 * alpha * aa[11] + 2 * beta * aa[11] - 3 * aa[10] + ll[8],
    }
    assert system["matrix"].rank() == 7
    pivot_variables = [uu[1], uu[2], uu[3], uu[5], aa[3], aa[4], aa[9]]
    pivot_columns = [system["unknowns"].index(item) for item in pivot_variables]
    pivot_block = system["matrix"][:, pivot_columns]
    constant_minor = False
    for rows in itertools.combinations(range(pivot_block.rows), 7):
        determinant = sp.factor(
            pivot_block.extract(rows, range(7)).det()
        )
        if determinant != 0 and not (determinant.free_symbols & {alpha, beta}):
            constant_minor = True
            break
    assert constant_minor
    assert all(
        exact_zero(item.subs(sub6))
        for item in coeffs(system["e6"])
    )

    e5 = sp.expand(weighted.coeff_monomial(z**5).subs(sub6))
    forced = {}

    def require(relation):
        values = [
            sp.factor(item.subs(forced))
            for item in coeffs(e5)
            if sp.factor(item.subs(forced)) != 0
        ]
        assert contains_numeric_multiple(values, relation)

    require(uu[7])
    forced[uu[7]] = 0
    require(aa[14] - uu[6])
    forced[aa[14]] = uu[6]
    require(aa[10] - 2 * alpha * aa[11])
    forced[aa[10]] = 2 * alpha * aa[11]
    require(aa[2] - 2 * aa[5] * uu[6])
    forced[aa[2]] = 2 * aa[5] * uu[6]
    relation_a1 = aa[1] + 16 * aa[11] * uu[6] - 2 * aa[13] * aa[5] - 8 * aa[8]
    require(relation_a1)
    forced[aa[1]] = -16 * aa[11] * uu[6] + 2 * aa[13] * aa[5] + 8 * aa[8]
    value_a7 = (
        ll[7]
        - sp.Rational(3, 4) * forced[aa[1]]
        + 2 * aa[11] * aa[13]
        + sp.Rational(3, 2) * aa[13] * aa[5]
    )
    require(aa[7] - value_a7)
    forced[aa[7]] = value_a7
    require(ll[2] - 2 * aa[5] * ll[8])
    forced[ll[2]] = 2 * aa[5] * ll[8]
    require(ll[5] - 2 * aa[11] * ll[8])
    forced[ll[5]] = 2 * aa[11] * ll[8]
    assert exact_zero(e5.subs(forced))

    e4 = sp.expand(
        weighted.coeff_monomial(z**4).subs(sub6).subs(forced)
    )
    kappa = aa[8] - 2 * aa[11] * uu[6]
    assert exact_zero(
        sp.Poly(e4, p, q, r).coeff_monomial(p * r**3) + 4 * kappa
    )
    sub4 = {aa[8]: 2 * aa[11] * uu[6]}
    e4a = sp.expand(e4.subs(sub4))
    assert exact_zero(
        sp.Poly(e4a, p, q, r).coeff_monomial(p**2 * q * r)
        - (2 * aa[5] * ll[7] - ll[1])
    )
    sub4[ll[1]] = 2 * aa[5] * ll[7]
    e4b = sp.expand(e4.subs(sub4))
    assert exact_zero(
        sp.Poly(e4b, p, q, r).coeff_monomial(p**3 * r)
        - 4 * (ll[4] - 2 * aa[11] * ll[7])
    )
    sub4[ll[4]] = 2 * aa[11] * ll[7]
    assert exact_zero(e4.subs(sub4))
    all_subs = {}
    all_subs.update(sub6)
    all_subs.update(forced)
    all_subs.update(sub4)
    assert exact_zero(system["linear"].det().subs(all_subs))
    print("PASS t4 E6/E5 converse and three necessary E4 pivots force det L=0")


def main():
    check_raw_ranks()
    check_r_multiplier_squares()
    check_pivots_and_zero_normal_kernels()
    check_delta4_compatibility_tree()
    check_d4b_algebraic_branch()
    check_t4_branch_with_converse_pivots()
    print("ALL INDEPENDENT EXCEPTIONAL-BRANCH CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
