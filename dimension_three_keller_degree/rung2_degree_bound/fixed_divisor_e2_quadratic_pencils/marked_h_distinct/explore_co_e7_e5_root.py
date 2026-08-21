#!/usr/bin/env python3
"""Explore the two frozen open companion orbits through E7/E6/E5."""

from __future__ import annotations

import itertools

import sympy as sp

x, y, z, scale = sp.symbols("x y z scale")
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


def column(direction):
    U, V, W = direction
    return sp.Matrix(
        [sp.Poly(U, *xyz).coeff_monomial(m) for m in mon3]
        + [sp.Poly(V, *xyz).coeff_monomial(m) for m in mon3]
        + [sp.Poly(W, *xyz).coeff_monomial(m) for m in mon2]
    )


def forms(vector):
    return (
        sp.factor(sum(vector[i] * mon3[i] for i in range(10))),
        sp.factor(sum(vector[10 + i] * mon3[i] for i in range(10))),
        sp.factor(sum(vector[20 + i] * mon2[i] for i in range(6))),
    )


def left_values(matrix, rhs):
    output = []
    for vector in matrix.T.nullspace():
        denominators = [
            sp.together(entry).as_numer_denom()[1]
            for entry in vector
            if entry != 0
        ]
        denominator = sp.factor(sp.lcm(denominators)) if denominators else 1
        vector = vector.applyfunc(lambda entry: sp.cancel(denominator * entry))
        value = sp.factor((vector.T * rhs)[0])
        if value != 0:
            output.append(value)
    return output


def branch(label, h, r):
    s = x**2
    P, Q, R = h**2, h * s, x * r
    u = sp.symbols(f"{label}_u0:10")
    v = sp.symbols(f"{label}_v0:10")
    w = sp.symbols(f"{label}_w0:6")
    raw = u + v + w
    U0 = sum(c * m for c, m in zip(u, mon3))
    V0 = sum(c * m for c, m in zip(v, mon3))
    W0 = sum(c * m for c, m in zip(w, mon2))
    E7 = sp.expand(
        jac3(P, Q, W0) + jac3(P, V0, R) + jac3(U0, Q, R)
    )
    matrix7, rhs7 = sp.linear_eq_to_matrix(coefficients(E7, 7), raw)
    assert rhs7 == sp.zeros(36, 1)
    kernel = matrix7.nullspace()
    gauges = [
        column((R, 0, 0)),
        column((0, R, 0)),
        *[
            column(tuple(sp.diff(component, variable) for component in (P, Q, R)))
            for variable in xyz
        ],
    ]
    basis = sp.Matrix.hstack(*gauges)
    normals = []
    for candidate in kernel:
        trial = sp.Matrix.hstack(basis, candidate)
        if trial.rank() > basis.rank():
            normals.append(candidate)
            basis = trial
        if basis.cols == len(kernel):
            break
    assert matrix7 * basis == sp.zeros(36, basis.cols)
    assert basis.rank() == len(kernel)
    print("\n", label, "E7 shape/rank/nullity/normals:", matrix7.shape, matrix7.rank(), len(kernel), len(normals))
    rows7 = matrix7.T.rref()[1]
    columns7 = matrix7.rref()[1]
    print(
        " E7 pivot:",
        rows7,
        columns7,
        sp.factor(matrix7.extract(rows7, columns7).det()),
    )
    basis_rows = basis.T.rref()[1]
    print(
        " basis pivot:",
        basis_rows,
        sp.factor(basis.extract(basis_rows, range(basis.cols)).det()),
    )
    for index, normal in enumerate(normals):
        print(" normal", index, forms(normal))

    parameters = sp.symbols(f"{label}_N0:{len(normals)}")
    U, V, W = (0, 0, 0)
    for parameter, normal in zip(parameters, normals):
        direction = forms(normal)
        U += parameter * direction[0]
        V += parameter * direction[1]
        W += parameter * direction[2]
    U, V, W = map(sp.expand, (U, V, W))
    print(" normal form:", sp.factor(U), sp.factor(V), sp.factor(W))

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
    L = sp.Matrix(3, 3, ell)
    weighted = sp.Poly(
        sp.expand(
            (
                L
                + scale * H2.jacobian(xyz)
                + scale**2 * sp.Matrix([U, V, R]).jacobian(xyz)
                + scale**3 * sp.Matrix([P, Q, 0]).jacobian(xyz)
            ).det()
        ),
        scale,
    )
    unknowns = a + b + ell
    E6 = sp.expand(weighted.coeff_monomial(scale**6))
    matrix6, rhs6 = sp.linear_eq_to_matrix(coefficients(E6, 6), unknowns)
    compatibility6 = left_values(matrix6, rhs6)
    print(" E6 shape/rank/compat:", matrix6.shape, matrix6.rank(), compatibility6)
    if compatibility6:
        return
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), unknowns)))
    substitutions6 = dict(zip(unknowns, solution6))
    rows6 = matrix6.T.rref()[1]
    columns6 = matrix6.rref()[1]
    print(" E6 pivot:", rows6, columns6, sp.factor(matrix6.extract(rows6, columns6).det()))
    print(" E6 changed:")
    for variable, value in zip(unknowns, solution6):
        if sp.expand(variable - value) != 0:
            print("  ", variable, "=", sp.factor(value))
    E5 = sp.expand(weighted.coeff_monomial(scale**5).subs(substitutions6))
    remaining = tuple(variable for variable in unknowns if variable in E5.free_symbols)
    try:
        matrix5, rhs5 = sp.linear_eq_to_matrix(coefficients(E5, 5), remaining)
    except sp.NonlinearError:
        print(" E5 is nonlinear:")
        for exponent, value in zip(exponents(5), coefficients(E5, 5)):
            if value != 0:
                print("  ", exponent, sp.factor(value))
        return
    compatibility5 = left_values(matrix5, rhs5)
    print(" E5 remaining/shape/rank:", remaining, matrix5.shape, matrix5.rank())
    rows5 = matrix5.T.rref()[1]
    columns5 = matrix5.rref()[1]
    print(" E5 pivot:", rows5, columns5, sp.factor(matrix5.extract(rows5, columns5).det()))
    print(" E5 compat:", compatibility5)
    if compatibility5:
        return
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining)))
    substitutions5 = dict(zip(remaining, solution5))
    print(" E5 changed:")
    for variable, value in zip(remaining, solution5):
        if sp.expand(variable - value) != 0:
            print("  ", variable, "=", sp.factor(value))
    print(
        " detL through E5:",
        sp.factor(L.det().subs(substitutions6).subs(substitutions5)),
    )

    if label == "P3_CO":
        special = {parameters[2]: 0}
        E6_zero = sp.expand(weighted.coeff_monomial(scale**6).subs(special))
        matrix6_zero, rhs6_zero = sp.linear_eq_to_matrix(
            coefficients(E6_zero, 6), unknowns
        )
        print(
            " P3 normal-2=0 E6 shape/rank/compat:",
            matrix6_zero.shape,
            matrix6_zero.rank(),
            left_values(matrix6_zero, rhs6_zero),
        )
        solution6_zero = next(
            iter(sp.linsolve((matrix6_zero, rhs6_zero), unknowns))
        )
        substitutions6_zero = dict(zip(unknowns, solution6_zero))
        E5_zero = sp.expand(
            weighted.coeff_monomial(scale**5)
            .subs(special)
            .subs(substitutions6_zero)
        )
        remaining_zero = tuple(
            variable for variable in unknowns if variable in E5_zero.free_symbols
        )
        matrix5_zero, rhs5_zero = sp.linear_eq_to_matrix(
            coefficients(E5_zero, 5), remaining_zero
        )
        print(
            " P3 normal-2=0 E5 remaining/shape/rank:",
            remaining_zero,
            matrix5_zero.shape,
            matrix5_zero.rank(),
        )
        print(
            " P3 normal-2=0 E5 compat:",
            left_values(matrix5_zero, rhs5_zero),
        )
        solution5_zero = next(
            iter(sp.linsolve((matrix5_zero, rhs5_zero), remaining_zero))
        )
        substitutions5_zero = dict(zip(remaining_zero, solution5_zero))
        print(
            " P3 normal-2=0 detL:",
            sp.factor(
                L.det()
                .subs(special)
                .subs(substitutions6_zero)
                .subs(substitutions5_zero)
            ),
        )


branch("HR2_CO", y * z, x**2 + y * z)
branch("P3_CO", y**2 + x * z, x**2 + y**2 + x * z)
