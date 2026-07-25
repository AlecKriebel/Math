#!/usr/bin/env python3
"""Fail-closed exact certificate for the binary fixed-cubic line row.

Every calculation is over QQ (or the displayed quadratic extension).  The
script intentionally reconstructs coefficient matrices from the determinant;
it does not load cached ranks or precomputed equations.
"""

from __future__ import annotations

if not __debug__:
    raise RuntimeError("verification requires assertions; do not use -O")

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
variables = (p, q, r)
bc3 = (p**3, p**2 * q, p * q**2, q**3)
bc2 = (p**2, p * q, q**2)
q2 = (p**2, p * q, q**2, p * r, q * r, r**2)


def coefficients(expression, gens=variables):
    return [
        coefficient
        for _, coefficient in sp.Poly(sp.expand(expression), *gens).terms()
    ]


def exact_zero(expression):
    return sp.cancel(sp.expand(expression)) == 0


def tangent(vector, power):
    if power == 1:
        return (
            vector[0] * p + vector[1] * q,
            vector[2] * p + vector[3] * q,
            vector[4],
        )
    if power == 0:
        return (
            sum(vector[j] * bc2[j] for j in range(3)),
            sum(vector[3 + j] * bc2[j] for j in range(3)),
            vector[6] * p + vector[7] * q,
        )
    raise ValueError(power)


def e7_matrix(h, W, power):
    D = sp.Matrix([h * p, h * q]).jacobian((p, q))
    row = sp.Matrix([[sp.diff(W, p), sp.diff(W, q)]]) * D.adjugate()
    if power == 2:
        unknowns = sp.symbols("e2_0:2")
        expression = (row * sp.Matrix(unknowns))[0]
    elif power == 1:
        unknowns = sp.symbols("e1_0:5")
        top = sp.Matrix(
            [
                unknowns[0] * p + unknowns[1] * q,
                unknowns[2] * p + unknowns[3] * q,
            ]
        )
        expression = (row * top)[0] - 4 * h**2 * unknowns[4]
    elif power == 0:
        unknowns = sp.symbols("e0_0:8")
        top = sp.Matrix(
            [
                sum(unknowns[j] * bc2[j] for j in range(3)),
                sum(unknowns[3 + j] * bc2[j] for j in range(3)),
            ]
        )
        normal = unknowns[6] * p + unknowns[7] * q
        expression = (row * top)[0] - 4 * h**2 * normal
    else:
        raise ValueError(power)
    matrix, rhs = sp.linear_eq_to_matrix(
        coefficients(expression, (p, q)), unknowns
    )
    assert rhs == sp.zeros(rhs.rows, 1)
    return unknowns, matrix


def e7_bases(h, W):
    dimensions = []
    bases = {}
    for power in (2, 1, 0):
        _, matrix = e7_matrix(h, W, power)
        kernel = matrix.nullspace()
        dimensions.append(len(kernel))
        if power in (1, 0):
            bases[power] = [tangent(vector, power) for vector in kernel]
    return tuple(dimensions), bases


def make_e6_system(prefix, h, W, ur):
    u = sp.symbols(f"{prefix}u0:8")
    a = sp.symbols(f"{prefix}a0:15")
    ell33 = sp.symbols(f"{prefix}ell33")
    H3 = sp.Matrix(
        [
            sum(u[j] * bc3[j] for j in range(4))
            + sp.integrate(ur[0], r),
            sum(u[4 + j] * bc3[j] for j in range(4))
            + sp.integrate(ur[1], r),
            W,
        ]
    )
    H2 = sp.Matrix(
        [
            sum(a[j] * q2[j] for j in range(6)),
            sum(a[6 + j] * q2[j] for j in range(6)),
            sum(a[12 + j] * bc2[j] for j in range(3))
            + sp.integrate(ur[2], r),
        ]
    )
    D = sp.Matrix([h * p, h * q]).jacobian((p, q))
    B = sp.Matrix(H3[:2, :]).jacobian((p, q))
    top_ur = sp.Matrix([sp.diff(H3[0], r), sp.diff(H3[1], r)])
    wrow = sp.Matrix([[sp.diff(W, p), sp.diff(W, q)]])
    Atop = sp.Matrix(H2[:2, :])
    ar = sp.Matrix([sp.diff(Atop[0], r), sp.diff(Atop[1], r)])
    trow = sp.Matrix([[sp.diff(H2[2], p), sp.diff(H2[2], q)]])
    tau = sp.diff(H2[2], r)
    E6 = sp.expand(
        D.det() * ell33
        + sp.trace(B.adjugate() * D) * tau
        - (wrow * D.adjugate() * ar)[0]
        - (wrow * B.adjugate() * top_ur)[0]
        - (trow * D.adjugate() * top_ur)[0]
    )
    unknowns = u + a + (ell33,)
    matrix, rhs = sp.linear_eq_to_matrix(coefficients(E6), unknowns)
    return {
        "u": u,
        "a": a,
        "ell33": ell33,
        "H3": H3,
        "H2": H2,
        "E6": E6,
        "unknowns": unknowns,
        "matrix": matrix,
        "rhs": rhs,
    }


def polynomial_left_pairings(matrix, rhs, branch_parameters):
    """Return denominator-cleared exact compatibility certificates."""
    output = []
    branch_parameters = set(branch_parameters)
    for vector in matrix.T.nullspace():
        denominators = [
            sp.together(entry).as_numer_denom()[1] for entry in vector
        ]
        common = sp.lcm(denominators)
        polynomial_vector = sp.Matrix(
            [sp.cancel(common * entry) for entry in vector]
        )
        assert all(
            exact_zero(item)
            for item in matrix.T * polynomial_vector
        )
        pairing = sp.factor(sp.expand(polynomial_vector.dot(rhs)))
        if pairing:
            output.append(
                (
                    pairing,
                    not (
                        sp.together(common).as_numer_denom()[0].free_symbols
                        & branch_parameters
                    ),
                )
            )
    return output


def has_constant_multiple(pairings, target, parameters):
    parameters = set(parameters)
    for pairing, branch_safe in pairings:
        if not branch_safe:
            continue
        quotient = sp.cancel(pairing / target)
        if quotient != 0 and not (quotient.free_symbols & parameters):
            return True
    return False


def fixed_e7_tangent_constant(name, h, W, N):
    """Solve E6 exactly and return lower-variable-free E5 coefficients."""
    u = sp.symbols(f"{name}u0:8")
    a = sp.symbols(f"{name}a0:15")
    ell = sp.symbols(f"{name}l0:9")
    H3 = sp.Matrix(
        [
            sum(u[j] * bc3[j] for j in range(4)) + r * N[0],
            sum(u[4 + j] * bc3[j] for j in range(4)) + r * N[1],
            W,
        ]
    )
    H2 = sp.Matrix(
        [
            sum(a[j] * q2[j] for j in range(6)),
            sum(a[6 + j] * q2[j] for j in range(6)),
            sum(a[12 + j] * bc2[j] for j in range(3)) + r * N[2],
        ]
    )
    L = sp.Matrix(3, 3, ell)
    H4 = sp.Matrix([h * p, h * q, 0])
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + z * H2.jacobian(variables)
                + z**2 * H3.jacobian(variables)
                + z**3 * H4.jacobian(variables)
            ).det()
        ),
        z,
    )
    assert exact_zero(weighted.coeff_monomial(z**8))
    assert exact_zero(weighted.coeff_monomial(z**7))
    unknowns = u + a + (ell[8],)
    matrix, rhs = sp.linear_eq_to_matrix(
        coefficients(weighted.coeff_monomial(z**6)), unknowns
    )
    assert matrix.rank() == matrix.row_join(rhs).rank()
    solution = next(iter(sp.linsolve((matrix, rhs), unknowns)))
    substitutions = {
        unknowns[index]: solution[index]
        for index in range(len(unknowns))
        if solution[index] != unknowns[index]
    }
    E5coeffs = coefficients(
        weighted.coeff_monomial(z**5).subs(substitutions)
    )
    lower = set(u + a + ell)
    constants = [
        sp.factor(item)
        for item in E5coeffs
        if item != 0 and not (item.free_symbols & lower)
    ]
    print(
        name,
        "fixed E7 tangent: E6",
        matrix.shape,
        "rank",
        matrix.rank(),
        "E5 constants",
        constants,
    )
    return constants


def fixed_lower_tangent_constant(name, h, W, N):
    """Solve E5 on a zero-normal lower syzygy and return E4 constants."""
    u = sp.symbols(f"{name}u0:8")
    a = sp.symbols(f"{name}a0:9")
    ell = sp.symbols(f"{name}l0:8")
    H3 = sp.Matrix(
        [
            sum(u[j] * bc3[j] for j in range(4)),
            sum(u[4 + j] * bc3[j] for j in range(4)),
            W,
        ]
    )
    H2 = sp.Matrix(
        [
            sum(a[j] * bc2[j] for j in range(3)) + r * N[0],
            sum(a[3 + j] * bc2[j] for j in range(3)) + r * N[1],
            sum(a[6 + j] * bc2[j] for j in range(3)),
        ]
    )
    L = sp.Matrix(
        [
            [ell[0], ell[1], ell[2]],
            [ell[3], ell[4], ell[5]],
            [ell[6], ell[7], 0],
        ]
    )
    H4 = sp.Matrix([h * p, h * q, 0])
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + z * H2.jacobian(variables)
                + z**2 * H3.jacobian(variables)
                + z**3 * H4.jacobian(variables)
            ).det()
        ),
        z,
    )
    for degree in (8, 7, 6):
        assert exact_zero(weighted.coeff_monomial(z**degree))
    unknowns = u + a + (ell[2], ell[5])
    matrix, rhs = sp.linear_eq_to_matrix(
        coefficients(weighted.coeff_monomial(z**5)), unknowns
    )
    assert matrix.rank() == matrix.row_join(rhs).rank()
    solution = next(iter(sp.linsolve((matrix, rhs), unknowns)))
    substitutions = {
        unknowns[index]: solution[index]
        for index in range(len(unknowns))
        if solution[index] != unknowns[index]
    }
    E4coeffs = coefficients(
        weighted.coeff_monomial(z**4).subs(substitutions)
    )
    lower = set(u + a + ell)
    constants = [
        sp.factor(item)
        for item in E4coeffs
        if item != 0 and not (item.free_symbols & lower)
    ]
    print(
        name,
        "lower tangent: E5",
        matrix.shape,
        "rank",
        matrix.rank(),
        "E4 constants",
        constants,
    )
    return constants


def reduce_quadratic(expression, generator, relation):
    numerator, denominator = sp.together(expression).as_numer_denom()
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
    pivot_row = 0
    for column in range(matrix.cols):
        pivot = next(
            (
                row
                for row in range(pivot_row, matrix.rows)
                if rows[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [
            reduce_quadratic(item / value, generator, relation)
            for item in rows[pivot_row]
        ]
        for row in range(matrix.rows):
            if row == pivot_row or rows[row][column] == 0:
                continue
            multiplier = rows[row][column]
            rows[row] = [
                reduce_quadratic(
                    rows[row][j] - multiplier * rows[pivot_row][j],
                    generator,
                    relation,
                )
                for j in range(matrix.cols)
            ]
        pivot_row += 1
        if pivot_row == matrix.rows:
            break
    return pivot_row


def check_d4b_gamma_branch():
    alpha, beta, gamma = sp.symbols("ga gb gamma")
    relation = 3 * gamma**2 - 8 * gamma + 8
    R1 = (-p / 2, q, 0)
    R2 = (2 * p, 0, 1)
    kappa = 1 - 3 * gamma / 8
    ur = tuple(
        sp.expand(
            r * (gamma * R1[j] + R2[j])
            + (alpha * p + beta * q) * (R1[j] + kappa * R2[j])
        )
        for j in range(3)
    )
    system = make_e6_system("g", p**2 * q, p**2 * q, ur)
    u, a, ell33 = system["u"], system["a"], system["ell33"]
    substitutions = {
        u[0]: (
            6 * a[11] * gamma
            - 4 * a[11]
            + 16 * a[12]
            - 3 * u[5] * gamma
            + 2 * u[5]
        )
        / 12,
        u[1]: (
            4 * a[13] * gamma
            + 8 * a[5]
            - 3 * u[6] * gamma
            + 2 * u[6]
        )
        / 4,
        u[2]: (8 * a[14] - 3 * u[7]) * (gamma + 2) / 12,
        u[3]: 0,
        u[4]: 0,
        a[3]: -(
            6 * alpha * a[5] * gamma
            - 16 * alpha * a[5]
            + 3 * beta * a[11] * gamma
            - 8 * beta * a[11]
            + 4 * a[10]
            - 16 * ell33
        )
        / 8,
        a[4]: -beta * a[5] * (3 * gamma - 8) / 4,
        a[9]: -alpha * a[11] * (3 * gamma - 8) / 4,
    }
    assert quotient_rank(
        system["matrix"].applyfunc(
            lambda item: reduce_quadratic(item, gamma, relation)
        ),
        gamma,
        relation,
    ) == 8
    assert all(
        reduce_quadratic(item.subs(substitutions), gamma, relation) == 0
        for item in coefficients(system["E6"])
    )
    ell = sp.symbols("gl0:8") + (ell33,)
    L = sp.Matrix(3, 3, ell)
    D = sp.Matrix([p**3 * q, p**2 * q**2]).jacobian((p, q))
    Bmat = sp.Matrix(system["H3"][:2, :]).jacobian((p, q))
    A = sp.Matrix(system["H2"][:2, :]).jacobian((p, q))
    top_ur = sp.Matrix(
        [sp.diff(system["H3"][0], r), sp.diff(system["H3"][1], r)]
    )
    wrow = sp.Matrix([[sp.diff(p**2 * q, p), sp.diff(p**2 * q, q)]])
    ar = sp.Matrix(
        [sp.diff(system["H2"][0], r), sp.diff(system["H2"][1], r)]
    )
    trow = sp.Matrix(
        [[sp.diff(system["H2"][2], p), sp.diff(system["H2"][2], q)]]
    )
    tau = sp.diff(system["H2"][2], r)
    d5 = sp.trace(Bmat.adjugate() * D)
    d4 = sp.trace(A.adjugate() * D) + Bmat.det()
    E5 = sp.expand(
        d5 * ell[8]
        + d4 * tau
        - (wrow * D.adjugate() * sp.Matrix([ell[2], ell[5]]))[0]
        - (wrow * Bmat.adjugate() * ar)[0]
        - (wrow * A.adjugate() * top_ur)[0]
        - (trow * D.adjugate() * ar)[0]
        - (trow * Bmat.adjugate() * top_ur)[0]
        - (
            sp.Matrix([[ell[6], ell[7]]])
            * D.adjugate()
            * top_ur
        )[0]
    )
    reduced = [
        sp.factor(
            reduce_quadratic(item.subs(substitutions), gamma, relation)
        )
        for item in coefficients(E5)
    ]
    print("d4b algebraic gamma branch-only E5 terms", [
        item
        for item in reduced
        if not (
            item.free_symbols
            & (set(u) | set(a) | set(ell))
        )
    ])
    assert any(
        exact_zero(item + 5 * alpha * (gamma - 4) / 8)
        for item in reduced
    )
    assert any(
        exact_zero(item + 5 * beta * (gamma - 4) / 8)
        for item in reduced
    )
    assert any(
        exact_zero(item - (gamma + 2) / 6) for item in reduced
    )
    assert reduce_quadratic(gamma + 2, gamma, relation) != 0
    print(
        "d4b algebraic gamma: E6 rank 8; E5 contains",
        (gamma + 2) / 6,
    )


def check_t4_gamma_branch():
    alpha, beta = sp.symbols("ta tb")
    R2 = (0, p, 1)
    N1 = (4 * p**2, -p * (3 * p - q), 0)
    N3 = (0, p**2, p)
    N4 = (-4 * p**2, 3 * p**2, q)
    ur = tuple(
        sp.expand(
            r * R2[j] + alpha * N1[j] + beta * N3[j] + alpha * N4[j]
        )
        for j in range(3)
    )
    system = make_e6_system("t", p**3, p**2 * (p + q), ur)
    u, a, ell33 = system["u"], system["a"], system["ell33"]
    sub6 = {
        u[1]: 2 * (-4 * a[14] + a[5] + 4 * u[6] + 18 * u[7]),
        u[2]: 6 * u[7],
        u[3]: 0,
        u[5]: 2 * a[11] + a[13] + 6 * a[14] - 6 * u[6] - 27 * u[7],
        a[3]: -2 * (4 * alpha * a[11] - beta * a[5] - 2 * a[10]),
        a[4]: 2 * alpha * a[5],
        a[9]: 6 * alpha * a[11] + 2 * beta * a[11] - 3 * a[10] + ell33,
    }
    assert system["matrix"].rank() == 7
    assert all(
        exact_zero(item.subs(sub6)) for item in coefficients(system["E6"])
    )
    ell = sp.symbols("tl0:8") + (ell33,)
    L = sp.Matrix(3, 3, ell)
    H4 = sp.Matrix([p**4, p**3 * q, 0])
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + z * system["H2"].jacobian(variables)
                + z**2 * system["H3"].jacobian(variables)
                + z**3 * H4.jacobian(variables)
            ).det()
        ),
        z,
    )
    sub5 = {
        u[7]: 0,
        a[14]: u[6],
        a[10]: 2 * alpha * a[11],
        a[2]: 2 * a[5] * u[6],
        ell[5]: 2 * a[11] * ell[8],
        ell[2]: 2 * a[5] * ell[8],
    }
    sub5[a[1]] = (
        -16 * a[11] * u[6] + 2 * a[13] * a[5] + 8 * a[8]
    )
    sub5[a[7]] = (
        ell[7]
        - sp.Rational(3, 4) * sub5[a[1]]
        + 2 * a[11] * a[13]
        + sp.Rational(3, 2) * a[13] * a[5]
    )
    E5 = sp.expand(weighted.coeff_monomial(z**5).subs(sub6).subs(sub5))
    assert E5 == 0
    E4 = sp.expand(weighted.coeff_monomial(z**4).subs(sub6).subs(sub5))
    K = a[8] - 2 * a[11] * u[6]
    assert exact_zero(
        sp.Poly(E4, p, q, r).coeff_monomial(p * r**3) + 4 * K
    )
    sub4 = {a[8]: 2 * a[11] * u[6]}
    E4a = sp.expand(E4.subs(sub4))
    assert exact_zero(
        sp.Poly(E4a, p, q, r).coeff_monomial(p**2 * q * r)
        - (2 * a[5] * ell[7] - ell[1])
    )
    sub4[ell[1]] = 2 * a[5] * ell[7]
    E4b = sp.expand(E4.subs(sub4))
    assert exact_zero(
        sp.Poly(E4b, p, q, r).coeff_monomial(p**3 * r)
        - 4 * (ell[4] - 2 * a[11] * ell[7])
    )
    sub4[ell[4]] = 2 * a[11] * ell[7]
    assert exact_zero(E4.subs(sub4))
    all_subs = {}
    all_subs.update(sub6)
    all_subs.update(sub5)
    all_subs.update(sub4)
    assert exact_zero(L.det().subs(all_subs))
    print(
        "t4 algebraic r-leaf: E6 rank 7; E4 makes L columns 2,3 proportional"
    )


def check_top_and_root_formula():
    h0, h1, h2, h3 = sp.symbols("h0:4")
    w0, w1, w2, w3 = sp.symbols("w0:4")
    h = h0 * p**3 + h1 * p**2 * q + h2 * p * q**2 + h3 * q**3
    W = w0 * p**3 + w1 * p**2 * q + w2 * p * q**2 + w3 * q**3
    D = sp.Matrix([p * h, q * h]).jacobian((p, q))
    assert exact_zero(D.det() - 4 * h**2)
    adj_expected = 4 * h * sp.eye(2) - sp.Matrix([p, q]) * sp.Matrix(
        [[sp.diff(h, p), sp.diff(h, q)]]
    )
    assert all(
        exact_zero(item)
        for item in (D.adjugate() - adj_expected)
    )
    row = sp.Matrix([[sp.diff(W, p), sp.diff(W, q)]]) * D.adjugate()
    J = lambda f, g: sp.diff(f, p) * sp.diff(g, q) - sp.diff(
        f, q
    ) * sp.diff(g, p)
    assert exact_zero(row[0] + J(q * h, W))
    assert exact_zero(row[1] - J(p * h, W))
    for multiplicity in range(1, 4):
        for order in range(0, 4):
            hm = p**multiplicity * q ** (3 - multiplicity)
            Wm = p**order * q ** (3 - order)
            P, Q = p * hm, q * hm
            triple = (J(Q, Wm), J(P, Wm), J(P, Q))
            gcd = sp.gcd(sp.gcd(triple[0], triple[1]), triple[2])
            observed = sp.Poly(gcd, p, q).terms()[-1][0][0]
            expected = min(
                2 * multiplicity, multiplicity + order - 1
            )
            assert observed == expected
    print("top identities and all 12 local root-order checks passed")


def check_e7_taxonomy():
    hs = p * q * (p - q)
    hd = p**2 * q
    ht = p**3
    A, B, Lam = sp.symbols("orbitA orbitB orbitLam")
    rs = sp.sqrt(3) * sp.I
    cases = (
        ("rho0-split", hs, (p + 2 * q) * (p + 3 * q) * (p + 5 * q), (0, 0, 0)),
        (
            "rho1-split",
            hs,
            p * (p + 2 * q) * (p + 3 * q),
            (0, 0, 1),
        ),
        ("rho1-double", hd, (p + q) * (p + 2 * q) * (p + 3 * q), (0, 0, 1)),
        ("s2a", hs, p**2 * (A * p + q), (0, 0, 2)),
        ("s2b", hs, p * q * (A * p + q), (0, 0, 2)),
        ("d2q", hd, q * (p**2 + B * p * q + q**2), (0, 0, 2)),
        ("d2p", hd, p * (p**2 + B * p * q + q**2), (0, 0, 2)),
        ("t2g", ht, q**3 + p**2 * q + Lam * p**3, (0, 0, 2)),
        ("d2q-pivot+", hd, q * (p + q) ** 2, (0, 0, 2)),
        ("d2q-pivot-", hd, q * (p - q) ** 2, (0, 0, 2)),
        ("d2p-pivot+", hd, p * (p + q) ** 2, (0, 0, 2)),
        ("d2p-pivot-", hd, p * (p - q) ** 2, (0, 0, 2)),
        (
            "t2-pivot+",
            ht,
            q**3 + p**2 * q + 2 * rs * p**3 / 9,
            (0, 0, 2),
        ),
        (
            "t2-pivot-",
            ht,
            q**3 + p**2 * q - 2 * rs * p**3 / 9,
            (0, 0, 2),
        ),
        ("d2q-k20", hd, q * (p**2 + q**2), (0, 1, 2)),
        ("t2-k20", ht, p**3 + q**3, (0, 1, 2)),
        ("s3a", hs, p**2 * q, (0, 1, 3)),
        ("s3b", hs, hs, (0, 1, 3)),
        ("d3q", hd, q**2 * (p + q), (0, 1, 3)),
        ("d3pq", hd, p * q * (p + q), (0, 1, 3)),
        ("d3p", hd, p**2 * (p + q), (0, 1, 3)),
        ("t3s", ht, p * q * (p - q), (0, 1, 3)),
        ("t3d", ht, p * q**2, (0, 1, 3)),
        ("d4a", hd, p * q**2, (0, 2, 4)),
        ("d4b", hd, p**2 * q, (0, 2, 4)),
        ("t4", ht, p**2 * (p + q), (0, 2, 4)),
    )
    saved = {}
    for name, h, W, expected in cases:
        dimensions, bases = e7_bases(h, W)
        assert dimensions == expected
        saved[name] = bases
        print(name, "E7 dimensions", dimensions)
        if expected[1] or expected[2]:
            print(" r-basis", [tuple(map(sp.factor, x)) for x in bases[1]])
            print(" 0-basis", [tuple(map(sp.factor, x)) for x in bases[0]])
    return saved


def check_r_multiplier_squares(saved):
    gamma = sp.symbols("rm")
    for name in (
        "d2q-k20",
        "t2-k20",
        "s3a",
        "s3b",
        "d3q",
        "d3pq",
        "d3p",
        "t3s",
        "t3d",
    ):
        hW = {
            "d2q-k20": (p**2 * q, q * (p**2 + q**2)),
            "t2-k20": (p**3, p**3 + q**3),
            "s3a": (p * q * (p - q), p**2 * q),
            "s3b": (p * q * (p - q), p * q * (p - q)),
            "d3q": (p**2 * q, q**2 * (p + q)),
            "d3pq": (p**2 * q, p * q * (p + q)),
            "d3p": (p**2 * q, p**2 * (p + q)),
            "t3s": (p**3, p * q * (p - q)),
            "t3d": (p**3, p * q**2),
        }[name]
        R = saved[name][1][0]
        ur = tuple(gamma * r * item for item in R)
        system = make_e6_system(f"rm{name}", hW[0], hW[1], ur)
        highest = sp.Poly(system["E6"], r).coeff_monomial(r**3)
        high_coefficients = coefficients(highest, (p, q))
        pure = [
            sp.cancel(item / gamma**2)
            for item in high_coefficients
            if item != 0
            and not (
                sp.cancel(item / gamma**2).free_symbols
                & set(system["unknowns"])
            )
        ]
        assert any(value != 0 for value in pure)
        print(name, "r-multiplier killed by E6[r^3]/gamma^2", pure)


def check_zero_normal_e6(saved):
    hs = p * q * (p - q)
    hd = p**2 * q
    ht = p**3
    # The only degree-one stratum whose normal may vanish.
    aa = sp.symbols("aa0:4")
    W = sum(aa[j] * bc3[j] for j in range(4))
    N = (
        -aa[2] * p**2 + 9 * aa[3] * p * q,
        -2 * aa[2] * p * q + 6 * aa[3] * q**2,
        (9 * aa[0] * aa[3] - aa[1] * aa[2]) * p
        + 2 * (3 * aa[1] * aa[3] - aa[2] ** 2) * q,
    )
    sys = make_e6_system("d1", hd, W, N)
    pairs = polynomial_left_pairings(sys["matrix"], sys["rhs"], aa)
    assert has_constant_multiple(pairs, aa[3] ** 3, aa)
    print("rho1 double E6 contains a nonzero multiple of a3^3")

    # Discriminant charts where the generic rho=2 normal basis degenerates.
    special = (
        (
            "d2q-disc",
            hd,
            q * (p + q) ** 2,
            (
                p**2 / 6 + 3 * p * q / 2,
                -p * q / 3 + q**2,
                0,
            ),
        ),
        (
            "d2p-disc",
            hd,
            p * (p + q) ** 2,
            (
                -3 * p**2 / 2 + 5 * p * q / 2,
                -3 * p * q + q**2,
                0,
            ),
        ),
        (
            "t2-disc",
            ht,
            q**3 + p**2 * q + 2 * sp.sqrt(3) * sp.I * p**3 / 9,
            (
                -4 * sp.sqrt(3) * sp.I * p**2 / 9 + 4 * p * q / 3,
                -2 * p**2 / 9
                - sp.sqrt(3) * sp.I * p * q / 3
                + q**2,
                0,
            ),
        ),
    )
    for name, h, W, N in special:
        system = make_e6_system(name, h, W, N)
        assert system["matrix"].rank() < system["matrix"].row_join(
            system["rhs"]
        ).rank()
        print(name, "zero-normal tangent incompatible at E6")

    one_dimensional = (
        ("s3a", hs, p**2 * q, saved["s3a"][0][0]),
        ("s3b", hs, hs, saved["s3b"][0][0]),
        ("d3q", hd, q**2 * (p + q), saved["d3q"][0][0]),
        ("d3pq", hd, p * q * (p + q), saved["d3pq"][0][0]),
        ("d3p", hd, p**2 * (p + q), saved["d3p"][0][0]),
        ("t3s", ht, p * q * (p - q), saved["t3s"][0][0]),
    )
    for name, h, W, N in one_dimensional:
        assert N[2] == 0
        system = make_e6_system("zn" + name, h, W, N)
        assert system["matrix"].rank() < system["matrix"].row_join(
            system["rhs"]
        ).rank()
        print(name, "unique zero-normal tangent incompatible at E6")

    # In these higher-dimensional kernels E6 kills the second direction.
    for name, h, W in (
        ("t3d", ht, p * q**2),
        ("d4a", hd, p * q**2),
        ("d4b", hd, p**2 * q),
        ("t4", ht, p**2 * (p + q)),
    ):
        kernel = [item for item in saved[name][0] if item[2] == 0]
        assert len(kernel) == 2
        x, y = sp.symbols(f"{name}x {name}y")
        N = tuple(x * kernel[0][j] + y * kernel[1][j] for j in range(3))
        system = make_e6_system("zk" + name, h, W, N)
        pairs = polynomial_left_pairings(
            system["matrix"], system["rhs"], (x, y)
        )
        assert has_constant_multiple(pairs, y**2, (x, y))
        print(name, "zero-normal E6 contains a branch-safe multiple of y^2")


def check_delta4_r_branching(saved):
    cases = {
        "d4a": (p**2 * q, p * q**2),
        "d4b": (p**2 * q, p**2 * q),
        "t4": (p**3, p**2 * (p + q)),
    }
    for name, (h, W) in cases.items():
        g0, g1 = sp.symbols(f"{name}g0 {name}g1")
        zpars = sp.symbols(f"{name}z0:4")
        rbasis = saved[name][1]
        zbasis = saved[name][0]
        ur = tuple(
            sp.expand(
                r * (g0 * rbasis[0][j] + g1 * rbasis[1][j])
                + sum(zpars[i] * zbasis[i][j] for i in range(4))
            )
            for j in range(3)
        )
        system = make_e6_system("br" + name, h, W, ur)
        parameters = (g0, g1) + zpars
        pairings = polynomial_left_pairings(
            system["matrix"], system["rhs"], parameters
        )
        if name == "d4a":
            assert has_constant_multiple(pairings, g0**2, parameters)
            assert has_constant_multiple(pairings, g1**2, parameters)
            print("d4a E6 forces both r-multipliers to zero")
        elif name == "d4b":
            quadratic = 3 * g0**2 - 8 * g0 * g1 + 8 * g1**2
            relation0 = (
                (3 * g0 - 4 * g1) * zpars[0]
                + (-4 * g0 + 8 * g1) * zpars[2]
            )
            relation1 = (
                (3 * g0 - 4 * g1) * zpars[1]
                + (-4 * g0 + 8 * g1) * zpars[3]
            )
            assert has_constant_multiple(pairings, quadratic, parameters)
            assert has_constant_multiple(pairings, relation0, parameters)
            assert has_constant_multiple(pairings, relation1, parameters)
            print(
                "d4b E6 converse branch:",
                quadratic,
                relation0,
                relation1,
            )
        else:
            assert has_constant_multiple(pairings, g0**2, parameters)
            # Reconstruct the g0=0 chart without dividing by g1.
            specialized = tuple(item.subs(g0, 0) for item in ur)
            system0 = make_e6_system("brt4z", h, W, specialized)
            parameters0 = (g1,) + zpars
            pairings0 = polynomial_left_pairings(
                system0["matrix"], system0["rhs"], parameters0
            )
            assert has_constant_multiple(
                pairings0, g1 * zpars[1], parameters0
            )
            assert has_constant_multiple(
                pairings0,
                g1 * (-zpars[0] - 3 * zpars[1] + zpars[3]),
                parameters0,
            )
            print(
                "t4 E6: g0=0; on g1!=0, z1=0 and z3=z0"
            )


def check_deep_constants():
    hs = p * q * (p - q)
    del hs
    e7_cases = (
        (
            "t3d-E7",
            p**3,
            p * q**2,
            (8 * p**2 / 5, p * q, 0),
            sp.Rational(24, 25),
        ),
        (
            "d4a-E7",
            p**2 * q,
            p * q**2,
            (5 * p**2 / 2, p * q, 0),
            sp.Integer(15),
        ),
        (
            "d4b-E7",
            p**2 * q,
            p**2 * q,
            (-p**2 / 2, p * q, 0),
            sp.Rational(3, 2),
        ),
        (
            "t4-E7",
            p**3,
            p**2 * (p + q),
            (4 * p**2, -p * (3 * p - q), 0),
            sp.Integer(-12),
        ),
    )
    for name, h, W, N, expected in e7_cases:
        constants = fixed_e7_tangent_constant(name, h, W, N)
        assert expected in constants

    lower_cases = (
        (
            "t3d-lower",
            p**3,
            p * q**2,
            (8 * p / 5, q),
            sp.Rational(-24, 5),
        ),
        (
            "d4a-lower",
            p**2 * q,
            p * q**2,
            (5 * p / 2, q),
            sp.Rational(-15, 2),
        ),
        (
            "d4b-lower",
            p**2 * q,
            p**2 * q,
            (-p / 2, q),
            sp.Rational(3, 2),
        ),
        (
            "t4-lower",
            p**3,
            p**2 * (p + q),
            (4 * p, -3 * p + q),
            sp.Integer(-12),
        ),
    )
    for name, h, W, N, expected in lower_cases:
        constants = fixed_lower_tangent_constant(name, h, W, N)
        assert expected in constants


def main():
    check_top_and_root_formula()
    saved = check_e7_taxonomy()
    check_r_multiplier_squares(saved)
    check_delta4_r_branching(saved)
    check_zero_normal_e6(saved)
    check_deep_constants()
    check_d4b_gamma_branch()
    check_t4_gamma_branch()
    print("ALL BINARY FIXED-CUBIC CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
