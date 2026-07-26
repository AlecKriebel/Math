#!/usr/bin/env python3
"""Exact E7--E5 closure of the two frozen discrete CO companion orbits."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z, weight = sp.symbols("x y z weight")
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


def exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def coefficients(value, degree):
    polynomial = sp.Poly(sp.expand(value), *xyz)
    return [
        polynomial.coeff_monomial(x**i * y**j * z**ell)
        for i, j, ell in exponents(degree)
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


def exact_zero(value):
    return sp.cancel(sp.expand(value)) == 0


def raw_e7_matrix(P, Q, R):
    uu = sp.symbols("u0:10")
    vv = sp.symbols("v0:10")
    ww = sp.symbols("w0:6")
    U = sum(coefficient * monomial for coefficient, monomial in zip(uu, mon3))
    V = sum(coefficient * monomial for coefficient, monomial in zip(vv, mon3))
    W = sum(coefficient * monomial for coefficient, monomial in zip(ww, mon2))
    E7 = sp.expand(jac3(P, Q, W) + jac3(P, V, R) + jac3(U, Q, R))
    matrix, rhs = sp.linear_eq_to_matrix(coefficients(E7, 7), uu + vv + ww)
    assert rhs == sp.zeros(36, 1)
    return matrix


def verify_branch(data):
    label = data["label"]
    h, r = data["h"], data["r"]
    P, Q, R = h**2, h * x**2, x * r
    normals = data["normals"]

    matrix7 = raw_e7_matrix(P, Q, R)
    assert matrix7.shape == (36, 26)
    assert matrix7.rank() == 18
    assert (
        matrix7.extract(data["e7_rows"], data["e7_columns"]).det()
        == data["e7_minor"]
    )

    gauges = [
        coefficient_column((R, 0, 0)),
        coefficient_column((0, R, 0)),
        *[
            coefficient_column(
                tuple(
                    sp.diff(component, variable)
                    for component in (P, Q, R)
                )
            )
            for variable in xyz
        ],
    ]
    basis = sp.Matrix.hstack(
        *(gauges + [coefficient_column(normal) for normal in normals])
    )
    assert matrix7 * basis == sp.zeros(36, 8)
    assert basis.rank() == 8
    assert (
        basis.extract(data["basis_rows"], range(8)).det()
        == data["basis_minor"]
    )

    normal_parameters = sp.symbols(f"{label}_n0:3")
    U = sum(parameter * normal[0] for parameter, normal in zip(normal_parameters, normals))
    V = sum(parameter * normal[1] for parameter, normal in zip(normal_parameters, normals))
    W = sum(parameter * normal[2] for parameter, normal in zip(normal_parameters, normals))

    aa = sp.symbols(f"{label}_a0:6")
    bb = sp.symbols(f"{label}_b0:6")
    ell = sp.symbols(f"{label}_l0:9")
    lower = aa + bb + ell
    H2 = sp.Matrix(
        [
            sum(coefficient * monomial for coefficient, monomial in zip(aa, mon2)),
            sum(coefficient * monomial for coefficient, monomial in zip(bb, mon2)),
            W,
        ]
    )
    L = sp.Matrix(3, 3, ell)
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + weight * H2.jacobian(xyz)
                + weight**2 * sp.Matrix([U, V, R]).jacobian(xyz)
                + weight**3 * sp.Matrix([P, Q, 0]).jacobian(xyz)
            ).det()
        ),
        weight,
    )
    assert all(
        exact_zero(determinant.coeff_monomial(weight**degree))
        for degree in (9, 8, 7)
    )

    E6 = sp.expand(determinant.coeff_monomial(weight**6))
    matrix6, rhs6 = sp.linear_eq_to_matrix(coefficients(E6, 6), lower)
    assert matrix6.shape == (28, 21)
    assert matrix6.rank() == 10
    assert (
        matrix6.extract(data["e6_rows"], data["e6_columns"]).det()
        == data["e6_minor"]
    )
    assert all(
        exact_zero((vector.T * rhs6)[0])
        for vector in matrix6.T.nullspace()
    )
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), lower)))
    substitutions6 = dict(zip(lower, solution6))
    assert all(
        exact_zero(entry)
        for entry in matrix6 * sp.Matrix(solution6) - rhs6
    )

    E5 = sp.expand(
        determinant.coeff_monomial(weight**5).subs(substitutions6)
    )
    remaining5 = tuple(
        unknown for unknown in lower if unknown in E5.free_symbols
    )
    matrix5, rhs5 = sp.linear_eq_to_matrix(
        coefficients(E5, 5), remaining5
    )
    assert matrix5.rank() == data["e5_rank"]
    assert (
        sp.factor(
            matrix5.extract(data["e5_rows"], data["e5_columns"]).det()
        )
        == data["e5_minor"](normal_parameters)
    )
    assert all(
        exact_zero((vector.T * rhs5)[0])
        for vector in matrix5.T.nullspace()
    )
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining5)))
    substitutions5 = dict(zip(remaining5, solution5))
    assert exact_zero(L.det().subs(substitutions6).subs(substitutions5))

    if data.get("boundary_normal") is not None:
        boundary = {normal_parameters[data["boundary_normal"]]: 0}
        E6_boundary = sp.expand(E6.subs(boundary))
        matrix6b, rhs6b = sp.linear_eq_to_matrix(
            coefficients(E6_boundary, 6), lower
        )
        assert matrix6b.rank() == 10
        solution6b = next(iter(sp.linsolve((matrix6b, rhs6b), lower)))
        substitutions6b = dict(zip(lower, solution6b))
        E5b = sp.expand(
            determinant.coeff_monomial(weight**5)
            .subs(boundary)
            .subs(substitutions6b)
        )
        remaining5b = tuple(
            unknown for unknown in lower if unknown in E5b.free_symbols
        )
        matrix5b, rhs5b = sp.linear_eq_to_matrix(
            coefficients(E5b, 5), remaining5b
        )
        assert matrix5b.rank() == 4
        assert all(
            exact_zero((vector.T * rhs5b)[0])
            for vector in matrix5b.T.nullspace()
        )
        solution5b = next(iter(sp.linsolve((matrix5b, rhs5b), remaining5b)))
        substitutions5b = dict(zip(remaining5b, solution5b))
        assert exact_zero(
            L.det()
            .subs(boundary)
            .subs(substitutions6b)
            .subs(substitutions5b)
        )

    print(f"PASS {label}: complete E7 quotient and exhaustive E6/E5 singularity")


BRANCHES = (
    {
        "label": "HR2_CO",
        "h": y * z,
        "r": x**2 + y * z,
        "normals": ((x**3, 0, 0), (0, x**3, 0), (0, 0, x**2)),
        "e7_rows": (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19, 23, 25, 31, 32),
        "e7_columns": (1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 23, 25),
        "e7_minor": -45137758519296,
        "basis_rows": (0, 4, 7, 8, 10, 14, 20, 24),
        "basis_minor": -4,
        "e6_rows": (1, 2, 3, 5, 7, 8, 11, 13, 17, 18),
        "e6_columns": (1, 2, 3, 5, 7, 8, 9, 11, 19, 20),
        "e6_minor": -26873856,
        "e5_rank": 4,
        "e5_rows": (1, 2, 7, 8),
        "e5_columns": (0, 1, 2, 3),
        "e5_minor": lambda _: sp.Integer(324),
    },
    {
        "label": "P3_CO",
        "h": y**2 + x * z,
        "r": x**2 + y**2 + x * z,
        "normals": (
            (x**3, 0, 0),
            (0, x**3, 0),
            (2 * z * (x * z + y**2), x**2 * z, x * z),
        ),
        "e7_rows": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 19),
        "e7_columns": (1, 2, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17, 18, 19, 24, 25),
        "e7_minor": -4814694242058240,
        "basis_rows": (0, 2, 4, 5, 10, 12, 20, 22),
        "basis_minor": -8,
        "e6_rows": (0, 1, 2, 3, 4, 5, 6, 7, 8, 11),
        "e6_columns": (1, 2, 4, 5, 7, 8, 10, 11, 19, 20),
        "e6_minor": 1934917632,
        "e5_rank": 4,
        "e5_rows": (0, 1, 2, 4),
        "e5_columns": (0, 1, 2, 4),
        "e5_minor": lambda parameters: -1296 * parameters[2] ** 2,
        "boundary_normal": 2,
    },
)

for branch in BRANCHES:
    verify_branch(branch)

print("MARKED_DISTINCT_CO_SYMPY_PASS_B74219")
