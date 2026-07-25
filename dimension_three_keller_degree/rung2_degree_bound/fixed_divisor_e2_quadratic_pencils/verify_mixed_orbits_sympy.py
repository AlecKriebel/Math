#!/usr/bin/env python3
"""Exact certificates excluding both mixed-companion e=2 pencils."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z, scale = sp.symbols("x y z scale")
variables = (x, y, z)
mon3 = tuple(
    x**i * y**j * z ** (3 - i - j)
    for i in range(3, -1, -1)
    for j in range(3 - i, -1, -1)
)
mon2 = tuple(
    x**i * y**j * z ** (2 - i - j)
    for i in range(2, -1, -1)
    for j in range(2 - i, -1, -1)
)


def exact_zero(value):
    return sp.cancel(sp.expand(value)) == 0


def jac3(f, g, h):
    return sp.Matrix([f, g, h]).jacobian(variables).det()


def homogeneous_exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def homogeneous_coefficients(value, degree):
    polynomial = sp.Poly(sp.expand(value), *variables)
    return [
        polynomial.coeff_monomial(x**i * y**j * z**k)
        for i, j, k in homogeneous_exponents(degree)
    ]


def coefficient(value, monomial):
    return sp.Poly(sp.expand(value), *variables).coeff_monomial(monomial)


def coefficient_column(direction):
    U, V, W = direction
    return sp.Matrix(
        [coefficient(U, monomial) for monomial in mon3]
        + [coefficient(V, monomial) for monomial in mon3]
        + [coefficient(W, monomial) for monomial in mon2]
    )


def nonzero_left_pairs(matrix, rhs):
    return [
        (vector, sp.factor((vector.T * rhs)[0]))
        for vector in matrix.T.nullspace()
        if not exact_zero((vector.T * rhs)[0])
    ]


def polynomial_left_pair(matrix, rhs, vector):
    denominators = [
        sp.together(entry).as_numer_denom()[1]
        for entry in vector
        if not exact_zero(entry)
    ]
    denominator = sp.factor(sp.lcm(denominators)) if denominators else sp.Integer(1)
    polynomial_vector = vector.applyfunc(
        lambda entry: sp.cancel(denominator * entry)
    )
    assert all(
        sp.together(entry).as_numer_denom()[1] in (1, -1)
        for entry in polynomial_vector
    )
    assert all(
        exact_zero(entry) for entry in matrix.T * polynomial_vector
    )
    return polynomial_vector, sp.factor((polynomial_vector.T * rhs)[0])


def associate(value, target):
    if exact_zero(value) or exact_zero(target):
        return exact_zero(value) and exact_zero(target)
    ratio = sp.cancel(value / target)
    return not ratio.free_symbols and ratio != 0


def weighted_determinant(P, Q, R, U, V, W, prefix):
    a = sp.symbols(f"{prefix}a0:6")
    b = sp.symbols(f"{prefix}b0:6")
    ell = sp.symbols(f"{prefix}l0:9")
    H2 = sp.Matrix(
        [
            sum(c * monomial for c, monomial in zip(a, mon2)),
            sum(c * monomial for c, monomial in zip(b, mon2)),
            W,
        ]
    )
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([P, Q, 0])
    L = sp.Matrix(3, 3, ell)
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + scale * H2.jacobian(variables)
                + scale**2 * H3.jacobian(variables)
                + scale**3 * H4.jacobian(variables)
            ).det()
        ),
        scale,
    )
    return weighted, a, b, ell, L


def raw_e7_certificate(label, p, q, normal_directions, expected):
    P = p**2
    Q = p * q
    R = x * q
    u = sp.symbols(f"{label}u0:10")
    v = sp.symbols(f"{label}v0:10")
    w = sp.symbols(f"{label}w0:6")
    U = sum(c * monomial for c, monomial in zip(u, mon3))
    V = sum(c * monomial for c, monomial in zip(v, mon3))
    W = sum(c * monomial for c, monomial in zip(w, mon2))
    E7 = sp.expand(
        jac3(P, Q, W) + jac3(P, V, R) + jac3(U, Q, R)
    )
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E7, 7), u + v + w
    )
    rows, columns, determinant, kernel_rows, kernel_determinant = expected
    assert exact_zero(jac3(P, Q, R))
    assert rhs == sp.zeros(36, 1)
    assert matrix.shape == (36, 26)
    assert matrix.rank() == 14
    assert matrix.extract(rows, columns).det() == determinant
    translations = tuple(
        tuple(sp.diff(component, variable) for component in (P, Q, R))
        for variable in variables
    )
    directions = (
        (R, 0, 0),
        (0, R, 0),
        translations[0],
        translations[1],
        translations[2],
    ) + normal_directions
    kernel = sp.Matrix.hstack(
        *(coefficient_column(direction) for direction in directions)
    )
    assert matrix * kernel == sp.zeros(36, 12)
    assert kernel.rank() == 12
    assert (
        kernel.extract(kernel_rows, range(12)).det()
        == kernel_determinant
    )
    assert matrix.cols - matrix.rank() == kernel.cols
    print(
        f"PASS {label} raw E7: rank 14, complete 12-dimensional "
        "kernel with five legal gauges"
    )


def ranktwo_raw():
    p = x**2
    q = y * z
    normals = (
        (0, x**3, 0),
        (4 * x**2 * y, y**2 * z, 0),
        (4 * x**2 * z, y * z**2, 0),
        (0, 0, x**2),
        (0, x * y**2, y**2),
        (0, 0, y * z),
        (0, x * z**2, z**2),
    )
    expected = (
        (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19),
        (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 19),
        -5308416,
        (0, 1, 2, 4, 10, 11, 12, 13, 14, 15, 20, 24),
        64,
    )
    raw_e7_certificate("ranktwo", p, q, normals, expected)


def rankone_raw():
    p = x**2
    q = y**2 + x * z
    normals = (
        (4 * x**2 * y, y * q, 0),
        (4 * x**2 * z, z * q, 0),
        (0, 0, x**2),
        (0, x**2 * z, x * z),
        (0, -x**2 * z, y**2),
        (0, x * y * z, y * z),
        (0, x * z**2, z**2),
    )
    expected = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15),
        (1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 18, 19),
        -849346560,
        (0, 1, 2, 3, 10, 11, 12, 13, 14, 15, 20, 22),
        -128,
    )
    raw_e7_certificate("rankone", p, q, normals, expected)


def ranktwo_general_e6():
    p = x**2
    q = y * z
    P, Q, R = p**2, p * q, x * q
    A, C, D, w0, w3, w4, w5 = sp.symbols(
        "rtA rtC rtD rtw0 rtw3 rtw4 rtw5"
    )
    U = 4 * C * x**2 * y + 4 * D * x**2 * z
    V = (
        A * x**3
        + C * y**2 * z
        + D * y * z**2
        + w3 * x * y**2
        + w5 * x * z**2
    )
    W = w0 * p + w3 * y**2 + w4 * q + w5 * z**2
    weighted, a, b, ell, _ = weighted_determinant(
        P, Q, R, U, V, W, "rtg"
    )
    assert all(
        exact_zero(weighted.coeff_monomial(scale**degree))
        for degree in (9, 8, 7)
    )
    unknowns = a + b + ell
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(
            weighted.coeff_monomial(scale**6), 6
        ),
        unknowns,
    )
    rows = (1, 2, 3, 5, 7, 8, 11, 13)
    columns = (1, 2, 3, 5, 7, 8, 9, 11)
    assert matrix.rank() == 8
    assert matrix.extract(rows, columns).det() == 4096
    values = [value for _, value in nonzero_left_pairs(matrix, rhs)]
    assert len(values) == 2
    assert any(associate(value, C * w3) for value in values)
    assert any(associate(value, D * w5) for value in values)
    print("PASS rank-two E6: exact compatibility C*w3=D*w5=0")


def ranktwo_nonzero_branch(label, D_value, w5_value):
    p = x**2
    q = y * z
    P, Q, R = p**2, p * q, x * q
    A, C, D, w0, w4, w5 = sp.symbols(
        f"{label}A {label}C {label}D {label}w0 {label}w4 {label}w5"
    )
    U = 4 * C * x**2 * y + 4 * D_value * x**2 * z
    V = (
        A * x**3
        + C * y**2 * z
        + D_value * y * z**2
        + w5_value * x * z**2
    )
    W = w0 * p + w4 * q + w5_value * z**2
    weighted, a, b, ell, _ = weighted_determinant(
        P, Q, R, U, V, W, label
    )
    unknowns = a + b + ell
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(
            weighted.coeff_monomial(scale**6), 6
        ),
        unknowns,
    )
    assert matrix6.rank() == 8
    assert not nonzero_left_pairs(matrix6, rhs6)
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), unknowns)))
    substitutions6 = dict(zip(unknowns, solution6))
    assert exact_zero(
        weighted.coeff_monomial(scale**6).subs(substitutions6)
    )
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    remaining = tuple(
        unknown for unknown in unknowns if unknown in E5.free_symbols
    )
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5, 5), remaining
    )
    pairs = nonzero_left_pairs(matrix5, rhs5)
    found = False
    for vector, _ in pairs:
        _, polynomial = polynomial_left_pair(matrix5, rhs5, vector)
        if associate(polynomial, C**3):
            found = True
            break
    assert found
    print(f"PASS rank-two {label}: polynomial E5 syzygy forces C^3=0")


def ranktwo_zero_branch():
    p = x**2
    q = y * z
    P, Q, R = p**2, p * q, x * q
    A, w0, w3, w4, w5 = sp.symbols(
        "rtzA rtz_w0 rtz_w3 rtz_w4 rtz_w5"
    )
    U = 0
    V = A * x**3 + w3 * x * y**2 + w5 * x * z**2
    W = w0 * p + w3 * y**2 + w4 * q + w5 * z**2
    weighted, a, b, ell, L = weighted_determinant(
        P, Q, R, U, V, W, "rtz"
    )
    unknowns = a + b + ell
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(
            weighted.coeff_monomial(scale**6), 6
        ),
        unknowns,
    )
    assert matrix6.rank() == 8
    assert not nonzero_left_pairs(matrix6, rhs6)
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), unknowns)))
    substitutions6 = dict(zip(unknowns, solution6))
    expected6 = {
        a[1]: 0,
        a[2]: 0,
        a[3]: 0,
        a[5]: 0,
        b[1]: ell[7],
        b[2]: ell[8],
        b[3]: -w3 * w4,
        b[5]: -w4 * w5,
    }
    assert all(
        exact_zero(substitutions6[unknown] - value)
        for unknown, value in expected6.items()
    )
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    assert coefficient(E5, x**4 * y) == 4 * (ell[4] + ell[7] * w4)
    assert coefficient(E5, x**4 * z) == -4 * (ell[5] + ell[8] * w4)
    assert coefficient(E5, x**2 * y**2 * z) == -ell[1]
    assert coefficient(E5, x**2 * y * z**2) == ell[2]
    forced = {
        ell[1]: 0,
        ell[2]: 0,
        ell[4]: -ell[7] * w4,
        ell[5]: -ell[8] * w4,
    }
    assert exact_zero(L.det().subs(forced))
    print(
        "PASS rank-two zero-normal branch: four literal E5 coefficients "
        "force det(L)=0"
    )


def ranktwo_certificate():
    ranktwo_raw()
    ranktwo_general_e6()
    D, w5 = sp.symbols("rtD rt_w5")
    ranktwo_nonzero_branch("rt_c_only", 0, w5)
    ranktwo_nonzero_branch("rt_both", D, 0)
    # The involution y<->z preserves P,Q,R and interchanges C,D and
    # w3,w5, so the D-only branch is the checked C-only branch.
    p, q = x**2, y * z
    swap = {y: z, z: y}
    assert exact_zero(p.xreplace(swap) - p)
    assert exact_zero(q.xreplace(swap) - q)
    assert exact_zero((x * q).xreplace(swap) - x * q)
    ranktwo_zero_branch()
    print("ALL RANK-TWO MIXED-ORBIT CERTIFICATES PASSED")


def rankone_general_e6():
    p = x**2
    q = y**2 + x * z
    P, Q, R = p**2, p * q, x * q
    C, D, w0, w2, w3, w4, w5 = sp.symbols(
        "roC roD ro_w0 ro_w2 ro_w3 ro_w4 ro_w5"
    )
    U = 4 * C * x**2 * y + 4 * D * x**2 * z
    V = (
        C * y * q
        + D * z * q
        + (w2 - w3) * x**2 * z
        + w4 * x * y * z
        + w5 * x * z**2
    )
    W = w0 * p + w2 * x * z + w3 * y**2 + w4 * y * z + w5 * z**2
    weighted, a, b, ell, _ = weighted_determinant(
        P, Q, R, U, V, W, "rog"
    )
    assert all(
        exact_zero(weighted.coeff_monomial(scale**degree))
        for degree in (9, 8, 7)
    )
    unknowns = a + b + ell
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(
            weighted.coeff_monomial(scale**6), 6
        ),
        unknowns,
    )
    rows = (0, 1, 2, 3, 4, 5, 6, 8)
    columns = (1, 2, 4, 5, 7, 8, 10, 11)
    assert matrix.rank() == 8
    assert matrix.extract(rows, columns).det() == 49152
    values = [value for _, value in nonzero_left_pairs(matrix, rhs)]
    E = C * w5 + D * w4
    assert len(values) == 3
    assert sum(associate(value, E) for value in values) == 2
    assert sum(associate(value, D * w5) for value in values) == 1
    print(
        "PASS rank-one E6: exact compatibility "
        "D*w5=C*w5+D*w4=0"
    )


def rankone_branch_data(label, substitutions):
    p = x**2
    q = y**2 + x * z
    P, Q, R = p**2, p * q, x * q
    C, D, w0, w2, w3, w4, w5 = sp.symbols(
        "roC roD ro_w0 ro_w2 ro_w3 ro_w4 ro_w5"
    )
    U = (4 * C * x**2 * y + 4 * D * x**2 * z).subs(substitutions)
    V = (
        C * y * q
        + D * z * q
        + (w2 - w3) * x**2 * z
        + w4 * x * y * z
        + w5 * x * z**2
    ).subs(substitutions)
    W = (
        w0 * p + w2 * x * z + w3 * y**2 + w4 * y * z + w5 * z**2
    ).subs(substitutions)
    weighted, a, b, ell, L = weighted_determinant(
        P, Q, R, U, V, W, label
    )
    unknowns = a + b + ell
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(
            weighted.coeff_monomial(scale**6), 6
        ),
        unknowns,
    )
    assert matrix6.rank() == 8
    assert not nonzero_left_pairs(matrix6, rhs6)
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), unknowns)))
    substitutions6 = dict(zip(unknowns, solution6))
    assert exact_zero(
        weighted.coeff_monomial(scale**6).subs(substitutions6)
    )
    E5 = sp.expand(
        weighted.coeff_monomial(scale**5).subs(substitutions6)
    )
    remaining = tuple(
        unknown for unknown in unknowns if unknown in E5.free_symbols
    )
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E5, 5), remaining
    )
    return (
        weighted,
        a,
        b,
        ell,
        L,
        substitutions6,
        E5,
        remaining,
        matrix5,
        rhs5,
    )


def rankone_nonzero_normals():
    C, D, w4, w5 = sp.symbols("roC roD ro_w4 ro_w5")
    # D != 0 forces w5=w4=0 at E6.  A polynomial left syzygy
    # of the E5 coefficient matrix then has value 24*D^3.
    data = rankone_branch_data(
        "ro_d_nonzero", {w4: 0, w5: 0}
    )
    matrix5, rhs5 = data[-2:]
    found_d = False
    for vector, _ in nonzero_left_pairs(matrix5, rhs5):
        polynomial_vector, polynomial = polynomial_left_pair(
            matrix5, rhs5, vector
        )
        if associate(polynomial, D**3):
            assert all(
                sp.together(entry).as_numer_denom()[1] in (1, -1)
                for entry in polynomial_vector
            )
            found_d = True
            break
    assert found_d

    # If D=0 and C!=0, E6 forces w5=0.  Two cross-multiplied
    # polynomial syzygies yield f(C,w4)=g(C,w4)=0, whose resultant
    # is -250*C^9.
    data = rankone_branch_data(
        "ro_c_nonzero", {D: 0, w5: 0}
    )
    matrix5, rhs5 = data[-2:]
    f = C**3 + 2 * C**2 * w4 - 2 * C * w4**2 + w4**3
    g = (C + 2 * w4) * (-3 * C**2 + w4**2)
    found_f = found_g = False
    for vector, _ in nonzero_left_pairs(matrix5, rhs5):
        _, polynomial = polynomial_left_pair(matrix5, rhs5, vector)
        found_f = found_f or associate(polynomial, C * f)
        found_g = found_g or associate(polynomial, C * g)
    assert found_f and found_g
    assert sp.factor(sp.resultant(f, g, w4)) == -250 * C**9
    print(
        "PASS rank-one nonzero normals: D^3 syzygy and "
        "resultant(f,g)=-250*C^9"
    )


def assert_rankone_open_zero_solution(label, substitutions, parameter, minor):
    data = rankone_branch_data(label, substitutions)
    (
        _,
        a,
        b,
        ell,
        L,
        _,
        E5,
        remaining,
        matrix5,
        rhs5,
    ) = data
    assert matrix5.rank() == 6
    rows, columns, expected_determinant = minor
    assert exact_zero(
        matrix5.extract(rows, columns).det() - expected_determinant
    )
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining)))
    solution = dict(zip(remaining, solution5))
    w3 = sp.symbols("ro_w3")
    expected = {
        a[3]: 0,
        b[3]: -w3**2,
        ell[1]: 0,
        ell[2]: 0,
        ell[4]: -ell[7] * w3,
        ell[5]: -ell[8] * w3,
    }
    assert all(
        unknown not in solution
        or exact_zero(solution[unknown] - value)
        for unknown, value in expected.items()
    )
    assert exact_zero(E5.subs(solution))
    assert exact_zero(L.det().subs(solution))
    assert parameter in expected_determinant.free_symbols


def rankone_zero_normals():
    C, D, w2, w3, w4, w5 = sp.symbols(
        "roC roD ro_w2 ro_w3 ro_w4 ro_w5"
    )
    # Chart w4 != 0.
    assert_rankone_open_zero_solution(
        "ro_zero_w4",
        {C: 0, D: 0},
        w4,
        (
            (0, 1, 2, 3, 4, 5),
            (0, 1, 2, 3, 4, 5),
            768 * w4**2,
        ),
    )
    # Complementary chart w4=0,w5!=0.
    assert_rankone_open_zero_solution(
        "ro_zero_w5",
        {C: 0, D: 0, w4: 0},
        w5,
        (
            (0, 1, 2, 4, 6, 8),
            (0, 1, 2, 3, 4, 5),
            -4096 * w5**2,
        ),
    )

    # Closed stratum w4=w5=0, d=w2-w3=0.
    data = rankone_branch_data(
        "ro_zero_d0",
        {C: 0, D: 0, w4: 0, w5: 0, w2: w3},
    )
    (
        _,
        _,
        _,
        ell,
        L,
        _,
        E5,
        remaining,
        matrix5,
        rhs5,
    ) = data
    assert matrix5.rank() == 4
    assert (
        matrix5.extract((0, 1, 2, 4), (0, 1, 2, 3)).det()
        == 64
    )
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining)))
    solution = dict(zip(remaining, solution5))
    expected = {
        ell[1]: 0,
        ell[2]: 0,
        ell[4]: -ell[7] * w3,
        ell[5]: -ell[8] * w3,
    }
    assert all(
        exact_zero(solution[unknown] - value)
        for unknown, value in expected.items()
    )
    assert exact_zero(E5.subs(solution))
    assert exact_zero(L.det().subs(solution))

    # Remaining stratum d!=0.  E5 has rank four and the displayed
    # minor records the only division.  Two literal E4 coefficients
    # then kill det(L) by product identities.
    data = rankone_branch_data(
        "ro_zero_d",
        {C: 0, D: 0, w4: 0, w5: 0},
    )
    (
        weighted,
        _,
        _,
        ell,
        L,
        substitutions6,
        E5,
        remaining,
        matrix5,
        rhs5,
    ) = data
    d = w2 - w3
    assert matrix5.rank() == 4
    assert exact_zero(
        matrix5.extract((0, 1, 2, 4), (0, 1, 2, 4)).det()
        + 64 * d**2
    )
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining)))
    solution = dict(zip(remaining, solution5))
    assert exact_zero(E5.subs(solution))
    E4 = sp.expand(
        weighted.coeff_monomial(scale**4)
        .subs(substitutions6)
        .subs(solution)
    )
    M = ell[5] + ell[8] * w3
    assert exact_zero(
        coefficient(E4, x**4) + 4 * ell[7] * M / d
    )
    assert exact_zero(
        coefficient(E4, x**3 * z) - ell[2] * ell[7] / d
    )
    determinant = sp.factor(L.det().subs(solution))
    expected_determinant = -ell[7] * (
        ell[0] * M - ell[2] * (ell[3] + ell[6] * w3)
    )
    assert exact_zero(determinant - expected_determinant)
    assert exact_zero(
        determinant
        + ell[0] * (ell[7] * M)
        - (ell[3] + ell[6] * w3) * (ell[2] * ell[7])
    )
    print(
        "PASS rank-one zero normals: two open charts, d=0, and "
        "d!=0 product exit all force det(L)=0"
    )


def rankone_certificate():
    rankone_raw()
    rankone_general_e6()
    rankone_nonzero_normals()
    rankone_zero_normals()
    print("ALL RANK-ONE MIXED-ORBIT CERTIFICATES PASSED")


def main():
    ranktwo_certificate()
    rankone_certificate()
    print("ALL FIXED-DIVISOR e=2 MIXED-ORBIT SYMPY CERTIFICATES PASSED")


if __name__ == "__main__":
    main()
