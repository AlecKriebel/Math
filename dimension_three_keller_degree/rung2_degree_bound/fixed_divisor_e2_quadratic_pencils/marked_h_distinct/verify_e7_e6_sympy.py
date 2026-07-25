#!/usr/bin/env python3
"""Exact E7/E6 certificate for all six marked-h-distinct branches."""

from __future__ import annotations

import sys

if not __debug__:
    print("FAIL: verification requires assertions; do not use -O", file=sys.stderr)
    raise SystemExit(2)

import sympy as sp

x, y, z, tau = sp.symbols("x y z tau")
xyz = (x, y, z)
A, B, C, D, T, E, F, S = sp.symbols("A B C D T E F S")

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


def homogeneous_exponents(degree):
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def homogeneous_coefficients(value, degree):
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


def exact_zero(value):
    return sp.cancel(sp.expand(value)) == 0


def associate(value, target):
    if exact_zero(value) or exact_zero(target):
        return exact_zero(value) and exact_zero(target)
    ratio = sp.cancel(value / target)
    return not ratio.free_symbols and ratio != 0


def polynomial_left_values(matrix, rhs):
    output = []
    for vector in matrix.T.nullspace():
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if not exact_zero(entry)
        ]
        denominator = sp.factor(sp.lcm(denominators)) if denominators else 1
        polynomial_vector = vector.applyfunc(
            lambda entry: sp.cancel(denominator * entry)
        )
        assert all(
            sp.together(entry).as_numer_denom()[1] in (1, -1)
            for entry in polynomial_vector
        )
        assert all(exact_zero(entry) for entry in matrix.T * polynomial_vector)
        value = sp.factor((polynomial_vector.T * rhs)[0])
        if not exact_zero(value):
            output.append(value)
    return output


def check_generators(actual, expected):
    assert actual
    assert all(any(associate(value, target) for target in expected) for value in actual)
    assert all(any(associate(value, target) for value in actual) for target in expected)


BRANCHES = (
    {
        "label": "RT-reducible/H",
        "h": y * z,
        "R": x * y * z,
        "U": A * x**3 - 2 * C * y**2 * z - 2 * D * y * z**2,
        "V": (
            B * x**3
            + C * x**2 * y
            + D * x**2 * z
            + 2 * E * x * y**2
            + 2 * F * x * z**2
        ),
        "W": T * x**2 + E * y**2 + F * z**2,
        "parameters": (A, B, C, D, T, E, F),
        "compatibility": (A * C, A * D, A * E, A * F, C * E, D * F, E**2, F**2),
        "e7_rank": 14,
        "e7_rows": (7, 8, 11, 13, 16, 17, 18, 19, 23, 25, 30, 31, 32, 33),
        "e7_columns": (1, 2, 3, 5, 6, 7, 8, 9, 13, 15, 16, 17, 18, 19),
        "e7_det": -82944,
        "basis_rows": (0, 4, 7, 8, 10, 11, 12, 13, 14, 15, 20, 24),
        "basis_det": 64,
        "e6_rank": 8,
        "e6_rows": (7, 8, 11, 13, 17, 18, 23, 25),
        "e6_columns": (1, 2, 3, 5, 7, 8, 9, 11),
        "e6_det": 256,
        "witness_e5": -y**2 * z * (x**2 - 2 * z**2),
    },
    {
        "label": "RT-reducible/S",
        "h": y * z,
        "R": x**3,
        "U": A * x * y * z,
        "V": B * x * y * z + sp.Rational(2, 3) * C * y**2 * z
        + sp.Rational(2, 3) * D * y * z**2,
        "W": C * x * y + D * x * z + T * y * z,
        "parameters": (A, B, C, D, T),
        "compatibility": (C**2, D**2),
        "e7_rank": 16,
        "e7_rows": (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19, 23, 25),
        "e7_columns": (1, 2, 3, 5, 6, 7, 8, 9, 13, 15, 16, 17, 18, 19, 23, 25),
        "e7_det": 25389989167104,
        "basis_rows": (0, 4, 7, 8, 10, 14, 17, 18, 20, 24),
        "basis_det": sp.Rational(16, 3),
        "e6_rank": 10,
        "e6_rows": (1, 2, 3, 5, 7, 8, 11, 13, 17, 18),
        "e6_columns": (1, 2, 3, 5, 7, 8, 9, 11, 19, 20),
        "e6_det": -26873856,
        "witness_e5": 3 * x**2 * y * (x**2 + 2 * z**2),
    },
    {
        "label": "RT-smooth/H",
        "h": x**2 + y * z,
        "R": x * (x**2 + y * z),
        "U": A * x**3 - 2 * C * y * (x**2 + y * z)
        - 2 * D * z * (x**2 + y * z),
        "V": (
            B * x**3
            + C * x**2 * y
            + D * x**2 * z
            + 2 * E * x * y**2
            + 2 * F * x * z**2
        ),
        "W": T * x**2 + E * y**2 + F * z**2,
        "parameters": (A, B, C, D, T, E, F),
        "compatibility": (A * C, A * D, A * E, A * F, C * E, D * F, E**2, F**2),
        "e7_rank": 14,
        "e7_rows": (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19),
        "e7_columns": (1, 2, 3, 5, 6, 7, 8, 9, 13, 15, 16, 17, 18, 19),
        "e7_det": -82944,
        "basis_rows": (0, 1, 2, 4, 10, 11, 12, 13, 14, 15, 20, 24),
        "basis_det": 64,
        "e6_rank": 8,
        "e6_rows": (1, 2, 3, 5, 7, 8, 11, 13),
        "e6_columns": (1, 2, 3, 5, 7, 8, 9, 11),
        "e6_det": 256,
        "witness_e5": -(x**2 + y * z) * (x**2 * y - 2 * x**2 * z - 2 * y * z**2),
    },
    {
        "label": "RT-smooth/S",
        "h": x**2 + y * z,
        "R": x**3,
        "U": A * x * y * z
        - sp.Rational(4, 3) * C * y * (x**2 + y * z)
        - sp.Rational(4, 3) * D * z * (x**2 + y * z),
        "V": B * x * y * z + sp.Rational(2, 3) * C * y**2 * z
        + sp.Rational(2, 3) * D * y * z**2,
        "W": C * x * y + D * x * z + T * y * z,
        "parameters": (A, B, C, D, T),
        "compatibility": (C**2, D**2),
        "e7_rank": 16,
        "e7_rows": (1, 2, 3, 5, 6, 7, 8, 9, 11, 13, 16, 17, 18, 19, 23, 25),
        "e7_columns": (1, 2, 3, 5, 6, 7, 8, 9, 13, 15, 16, 17, 18, 19, 23, 25),
        "e7_det": 25389989167104,
        "basis_rows": (0, 1, 2, 4, 10, 11, 12, 14, 20, 24),
        "basis_det": sp.Rational(16, 3),
        "e6_rank": 10,
        "e6_rows": (1, 2, 3, 5, 7, 8, 11, 13, 17, 18),
        "e6_columns": (1, 2, 3, 5, 7, 8, 9, 11, 19, 20),
        "e6_det": -26873856,
        "witness_e5": 3 * x**2 * (x**2 * y + 2 * x**2 * z + 2 * y * z**2),
    },
    {
        "label": "RO-smooth/H",
        "h": y**2 + x * z,
        "R": x * (y**2 + x * z),
        "U": A * x**3 - 2 * C * y * (y**2 + x * z)
        - 2 * D * z * (y**2 + x * z)
        + 2 * T * z * (y**2 + x * z),
        "V": (
            B * x**3
            + C * x**2 * y
            + (D + T) * x**2 * z
            + 2 * E * x * y * z
            + 2 * F * x * z**2
        ),
        "W": T * x * z + E * y * z + F * z**2,
        "parameters": (A, B, C, D, T, E, F),
        "compatibility": (
            A * C,
            A * D,
            A * E,
            A * F,
            C * F + D * E,
            E * F,
            2 * D * F - E**2,
            F**2,
        ),
        "e7_rank": 14,
        "e7_rows": (2, 4, 5, 7, 8, 9, 11, 12, 13, 14, 16, 17, 19, 22),
        "e7_columns": (1, 2, 4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19),
        "e7_det": -13271040,
        "basis_rows": (0, 2, 4, 5, 10, 11, 12, 13, 14, 15, 20, 22),
        "basis_det": -128,
        "e6_rank": 8,
        "e6_rows": (2, 4, 5, 7, 8, 9, 11, 13),
        "e6_columns": (1, 2, 4, 5, 7, 8, 10, 11),
        "e6_det": 3072,
        "witness_e5": -(x * z + y**2) * (x**3 - 4 * x * y * z - 4 * y**3),
    },
    {
        "label": "RO-smooth/S",
        "h": y**2 + x * z,
        "R": x**3,
        "U": 2 * A * z * (y**2 + x * z),
        "V": (
            A * x**2 * z
            + B * x * (y**2 + x * z)
            + sp.Rational(2, 3) * C * y * (y**2 + x * z)
            + sp.Rational(2, 3) * D * z * (y**2 + x * z)
        ),
        "W": C * x * y + S * (y**2 + x * z) + D * x * z,
        "parameters": (A, B, C, D, S),
        "compatibility": (C * D, D**2),
        "e7_rank": 16,
        "e7_rows": (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 17),
        "e7_columns": (1, 2, 4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 24, 25),
        "e7_det": 12187194800209920,
        "basis_rows": (0, 2, 4, 5, 10, 12, 14, 15, 20, 22),
        "basis_det": sp.Rational(64, 3),
        "e6_rank": 10,
        "e6_rows": (0, 1, 2, 3, 4, 5, 6, 7, 8, 11),
        "e6_columns": (1, 2, 4, 5, 7, 8, 10, 11, 19, 20),
        "e6_det": 1934917632,
        "witness_e5": 3 * x**2 * (x**3 + 4 * x * y * z + 4 * y**3),
    },
)


def verify_branch(branch):
    label = branch["label"]
    h, R = branch["h"], branch["R"]
    P, Q = sp.expand(h**2), sp.expand(h * x**2)
    U, V, W = branch["U"], branch["V"], branch["W"]
    parameters = branch["parameters"]

    u = sp.symbols(f"{label.replace('-', '_').replace('/', '_')}_u0:10")
    v = sp.symbols(f"{label.replace('-', '_').replace('/', '_')}_v0:10")
    w = sp.symbols(f"{label.replace('-', '_').replace('/', '_')}_w0:6")
    U0 = sum(c * m for c, m in zip(u, mon3))
    V0 = sum(c * m for c, m in zip(v, mon3))
    W0 = sum(c * m for c, m in zip(w, mon2))
    raw_e7 = sp.expand(
        jac3(P, Q, W0) + jac3(P, V0, R) + jac3(U0, Q, R)
    )
    matrix7, rhs7 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(raw_e7, 7), u + v + w
    )
    assert rhs7 == sp.zeros(36, 1)
    assert matrix7.shape == (36, 26)
    assert matrix7.rank() == branch["e7_rank"]
    assert (
        matrix7.extract(branch["e7_rows"], branch["e7_columns"]).det()
        == branch["e7_det"]
    )

    gauges = [
        coefficient_column((R, 0, 0)),
        coefficient_column((0, R, 0)),
        *[
            coefficient_column(
                tuple(sp.diff(component, variable) for component in (P, Q, R))
            )
            for variable in xyz
        ],
    ]
    normals = [
        coefficient_column(
            (sp.diff(U, parameter), sp.diff(V, parameter), sp.diff(W, parameter))
        )
        for parameter in parameters
    ]
    basis = sp.Matrix.hstack(*(gauges + normals))
    assert basis.cols == 26 - branch["e7_rank"]
    assert matrix7 * basis == sp.zeros(36, basis.cols)
    assert basis.rank() == basis.cols
    assert (
        basis.extract(branch["basis_rows"], range(basis.cols)).det()
        == branch["basis_det"]
    )

    prefix = label.replace("-", "_").replace("/", "_")
    a = sp.symbols(f"{prefix}_a0:6")
    b = sp.symbols(f"{prefix}_b0:6")
    ell = sp.symbols(f"{prefix}_l0:9")
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
        exact_zero(weighted.coeff_monomial(tau**degree))
        for degree in (9, 8, 7)
    )
    E6 = sp.expand(weighted.coeff_monomial(tau**6))
    lower_unknowns = a + b + ell
    matrix6, rhs6 = sp.linear_eq_to_matrix(
        homogeneous_coefficients(E6, 6), lower_unknowns
    )
    assert matrix6.shape == (28, 21)
    assert matrix6.rank() == branch["e6_rank"]
    assert (
        matrix6.extract(branch["e6_rows"], branch["e6_columns"]).det()
        == branch["e6_det"]
    )
    actual = polynomial_left_values(matrix6, rhs6)
    check_generators(actual, branch["compatibility"])

    # A sharp through-E6 witness.  The third row of L is dx, so
    # Jac(P,Q,x)=0 because P,Q are functions of h and x^2.
    witness = {parameter: 0 for parameter in parameters}
    witness.update({unknown: 0 for unknown in lower_unknowns})
    witness[ell[1]] = 1
    witness[ell[5]] = 1
    witness[ell[6]] = 1
    assert L.subs(witness) == sp.Matrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    assert L.det().subs(witness) == 1
    assert all(
        exact_zero(weighted.coeff_monomial(tau**degree).subs(witness))
        for degree in (9, 8, 7, 6)
    )
    witness_e5 = sp.expand(weighted.coeff_monomial(tau**5).subs(witness))
    assert exact_zero(witness_e5 - branch["witness_e5"])
    assert not exact_zero(witness_e5)

    print(
        f"PASS {label}: E7 rank {branch['e7_rank']}, "
        f"legal normal dimension {len(parameters)}, E6 rank "
        f"{branch['e6_rank']}, exact compatibility and sharp witness"
    )


def main():
    for branch in BRANCHES:
        verify_branch(branch)
    print("PASS all six marked-h-distinct E7/E6 branches")


if __name__ == "__main__":
    main()
