#!/usr/bin/env python3
"""Explore the six marked-h-distinct E7/E6 branches over QQ.

This is an exploratory generator, not yet a release certificate.  It keeps
the first two quadratic components and the full linear part arbitrary.  The
only quotiented directions are the two target shears by the fixed cubic
normal component and the source-translation directions that are actually
independent for the displayed branch.
"""

from __future__ import annotations

import sympy as sp

x, y, z, tau = sp.symbols("x y z tau")
xyz = (x, y, z)

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


def homogeneous_exponents(degree: int):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def homogeneous_coefficients(value, degree: int):
    polynomial = sp.Poly(sp.expand(value), *xyz)
    return [
        polynomial.coeff_monomial(x**i * y**j * z**k)
        for i, j, k in homogeneous_exponents(degree)
    ]


def jac3(f, g, h):
    return sp.Matrix([f, g, h]).jacobian(xyz).det()


def coefficient_column(direction):
    U, V, W = direction
    return sp.Matrix(
        [sp.Poly(U, *xyz).coeff_monomial(m) for m in mon3]
        + [sp.Poly(V, *xyz).coeff_monomial(m) for m in mon3]
        + [sp.Poly(W, *xyz).coeff_monomial(m) for m in mon2]
    )


def column_direction(column):
    return (
        sum(column[i] * mon3[i] for i in range(10)),
        sum(column[10 + i] * mon3[i] for i in range(10)),
        sum(column[20 + i] * mon2[i] for i in range(6)),
    )


def independent_extension(initial, candidates):
    columns = list(initial)
    rank = sp.Matrix.hstack(*columns).rank() if columns else 0
    chosen = []
    for candidate in candidates:
        trial = sp.Matrix.hstack(*(columns + [candidate]))
        trial_rank = trial.rank()
        if trial_rank > rank:
            columns.append(candidate)
            chosen.append(candidate)
            rank = trial_rank
    return columns, chosen


def first_full_minor(matrix):
    rows = matrix.T.rref()[1]
    return tuple(rows), sp.factor(matrix.extract(rows, range(matrix.cols)).det())


def polynomial_left_compatibilities(matrix, rhs):
    output = []
    for vector in matrix.T.nullspace():
        value = sp.factor((vector.T * rhs)[0])
        if value == 0:
            continue
        denominators = [
            sp.factor(sp.together(entry).as_numer_denom()[1])
            for entry in vector
            if entry != 0
        ]
        denominator = sp.factor(sp.lcm(denominators)) if denominators else 1
        pvector = vector.applyfunc(lambda entry: sp.cancel(denominator * entry))
        pvalue = sp.factor((pvector.T * rhs)[0])
        output.append((pvalue, denominator, pvector))
    return output


def branch_data(label, h, qprime, R):
    P, Q = sp.expand(h**2), sp.expand(h * qprime)
    u = sp.symbols(f"{label}_u0:10")
    v = sp.symbols(f"{label}_v0:10")
    w = sp.symbols(f"{label}_w0:6")
    U0 = sum(c * m for c, m in zip(u, mon3))
    V0 = sum(c * m for c, m in zip(v, mon3))
    W0 = sum(c * m for c, m in zip(w, mon2))
    E7 = sp.expand(
        jac3(P, Q, W0) + jac3(P, V0, R) + jac3(U0, Q, R)
    )
    matrix7, rhs7 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E7, 7), u + v + w
    )
    assert rhs7 == sp.zeros(36, 1)
    rows7 = matrix7.T.rref()[1]
    columns7 = matrix7.rref()[1]
    pivot7 = sp.factor(matrix7.extract(rows7, columns7).det())
    kernel = matrix7.nullspace()

    gauge_directions = [
        (R, 0, 0),
        (0, R, 0),
        *[
            tuple(sp.diff(component, variable) for component in (P, Q, R))
            for variable in xyz
        ],
    ]
    gauge_candidates = [coefficient_column(d) for d in gauge_directions]
    _, gauges = independent_extension([], gauge_candidates)
    combined, complement = independent_extension(gauges, kernel)
    assert len(combined) == len(kernel)
    basis_matrix = sp.Matrix.hstack(*combined)
    assert matrix7 * basis_matrix == sp.zeros(36, len(combined))
    basis_rows, basis_det = first_full_minor(basis_matrix)

    parameters = sp.symbols(f"{label}_n0:{len(complement)}")
    normal_column = sum(
        (parameter * column for parameter, column in zip(parameters, complement)),
        sp.zeros(26, 1),
    )
    U, V, W = tuple(sp.factor(value) for value in column_direction(normal_column))

    a = sp.symbols(f"{label}_a0:6")
    b = sp.symbols(f"{label}_b0:6")
    ell = sp.symbols(f"{label}_l0:9")
    H2 = sp.Matrix(
        [
            sum(c * m for c, m in zip(a, mon2)),
            sum(c * m for c, m in zip(b, mon2)),
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
                + tau * H2.jacobian(xyz)
                + tau**2 * H3.jacobian(xyz)
                + tau**3 * H4.jacobian(xyz)
            ).det()
        ),
        tau,
    )
    assert all(
        sp.expand(weighted.coeff_monomial(tau**degree)) == 0
        for degree in (9, 8, 7)
    )
    E6 = sp.expand(weighted.coeff_monomial(tau**6))
    unknowns6 = a + b + ell
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), unknowns6
    )
    rank6 = matrix6.rank()
    rows6 = matrix6.T.rref()[1]
    columns6 = matrix6.rref()[1]
    pivot6 = sp.factor(matrix6.extract(rows6, columns6).det())
    compat6 = polynomial_left_compatibilities(matrix6, rhs6)

    print(f"\n=== {label} ===")
    print("P =", P)
    print("Q =", Q)
    print("R =", R)
    print(
        "E7 shape/rank/nullity/gauge/complement =",
        matrix7.shape,
        matrix7.rank(),
        len(kernel),
        len(gauges),
        len(complement),
    )
    print("E7 pivot rows/columns/determinant =", rows7, columns7, pivot7)
    print("E7 basis rows/determinant =", basis_rows, basis_det)
    print("U =", U)
    print("V =", V)
    print("W =", W)
    print(
        "E6 shape/rank/pivot rows/columns/determinant =",
        matrix6.shape,
        rank6,
        rows6,
        columns6,
        pivot6,
    )
    print("E6 polynomial compatibilities:")
    for value, denominator, _ in compat6:
        print(" ", value, "[clearing divisor:", denominator, "]")

    return {
        "label": label,
        "P": P,
        "Q": Q,
        "R": R,
        "matrix7": matrix7,
        "gauges": gauges,
        "complement": complement,
        "basis_rows": basis_rows,
        "basis_det": basis_det,
        "parameters": parameters,
        "U": U,
        "V": V,
        "W": W,
        "matrix6": matrix6,
        "rhs6": rhs6,
        "rank6": rank6,
        "rows6": rows6,
        "columns6": columns6,
        "pivot6": pivot6,
        "compat6": compat6,
        "unknowns6": unknowns6,
        "weighted": weighted,
        "L": L,
    }


def main():
    branches = (
        ("rt_reducible_h", y * z, x**2, x * y * z),
        ("rt_reducible_s", y * z, x**2, x**3),
        ("rt_smooth_h", x**2 + y * z, x**2, x * (x**2 + y * z)),
        ("rt_smooth_s", x**2 + y * z, x**2, x**3),
        ("ro_smooth_h", y**2 + x * z, x**2, x * (y**2 + x * z)),
        ("ro_smooth_s", y**2 + x * z, x**2, x**3),
    )
    for branch in branches:
        branch_data(*branch)


if __name__ == "__main__":
    main()
