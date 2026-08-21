#!/usr/bin/env python3
"""Exploratory E5 solves for the six marked-distinct endpoint slices."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as sp

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "endpoint_data", here / "verify_e7_e6_sympy.py"
)
endpoint_data = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(endpoint_data)

x, y, z, scale = endpoint_data.x, endpoint_data.y, endpoint_data.z, endpoint_data.tau
xyz = endpoint_data.xyz
mon2 = endpoint_data.mon2


def coefficients(value, degree):
    return endpoint_data.homogeneous_coefficients(value, degree)


def left_values(matrix, rhs):
    output = []
    for vector in matrix.T.nullspace():
        value = sp.factor((vector.T * rhs)[0])
        if value != 0:
            output.append(value)
    return output


def calculate(branch, suffix, parameter_substitutions):
    label = branch["label"] + "/" + suffix
    h, R = branch["h"], branch["R"]
    P, Q = sp.expand(h**2), sp.expand(h * x**2)
    U = sp.expand(branch["U"].subs(parameter_substitutions))
    V = sp.expand(branch["V"].subs(parameter_substitutions))
    W = sp.expand(branch["W"].subs(parameter_substitutions))
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
    print("\n", label)
    print(" E6 shape/rank/compat:", matrix6.shape, matrix6.rank(), compatibility6)
    if compatibility6:
        return
    solution6 = next(iter(sp.linsolve((matrix6, rhs6), unknowns)))
    substitutions6 = dict(zip(unknowns, solution6))
    rows6 = matrix6.T.rref()[1]
    columns6 = matrix6.rref()[1]
    print(
        " E6 pivot:",
        rows6,
        columns6,
        sp.factor(matrix6.extract(rows6, columns6).det()),
    )
    E5 = sp.expand(weighted.coeff_monomial(scale**5).subs(substitutions6))
    remaining = tuple(v for v in unknowns if v in E5.free_symbols)
    try:
        matrix5, rhs5 = sp.linear_eq_to_matrix(coefficients(E5, 5), remaining)
    except sp.NonlinearError:
        print(" E5 nonlinear; rows:")
        for exponent, value in zip(endpoint_data.homogeneous_exponents(5), coefficients(E5, 5)):
            if value != 0:
                print("  ", exponent, sp.factor(value))
        return
    compatibility5 = left_values(matrix5, rhs5)
    print(
        " E5 remaining/shape/rank:",
        remaining,
        matrix5.shape,
        matrix5.rank(),
    )
    rows5 = matrix5.T.rref()[1]
    columns5 = matrix5.rref()[1]
    print(
        " E5 pivot:",
        rows5,
        columns5,
        sp.factor(matrix5.extract(rows5, columns5).det()),
    )
    print(" E5 compat:", compatibility5)
    if compatibility5:
        return
    solution5 = next(iter(sp.linsolve((matrix5, rhs5), remaining)))
    substitutions5 = dict(zip(remaining, solution5))
    determinant = sp.factor(
        L.det().subs(substitutions6).subs(substitutions5)
    )
    print(" detL through E5:", determinant)
    print(" E5 changed:")
    for variable, value in zip(remaining, solution5):
        if sp.expand(variable - value) != 0:
            print("  ", variable, "=", sp.factor(value))


branches = {entry["label"]: entry for entry in endpoint_data.BRANCHES}

# H companion: E6 radical is E=F=0 and A(C,D)=0.
for branch_label in ("RT-reducible/H", "RT-smooth/H", "RO-smooth/H"):
    calculate(
        branches[branch_label],
        "A-open",
        {endpoint_data.E: 0, endpoint_data.F: 0, endpoint_data.C: 0, endpoint_data.D: 0},
    )
    calculate(
        branches[branch_label],
        "A-zero",
        {endpoint_data.E: 0, endpoint_data.F: 0, endpoint_data.A: 0},
    )

for branch_label in ("RT-reducible/H", "RT-smooth/H"):
    calculate(
        branches[branch_label],
        "all-normal-zero",
        {
            endpoint_data.A: 0,
            endpoint_data.C: 0,
            endpoint_data.D: 0,
            endpoint_data.E: 0,
            endpoint_data.F: 0,
        },
    )

calculate(
    branches["RO-smooth/H"],
    "T-zero",
    {
        endpoint_data.C: 0,
        endpoint_data.D: 0,
        endpoint_data.E: 0,
        endpoint_data.F: 0,
        endpoint_data.T: 0,
    },
)
calculate(
    branches["RO-smooth/H"],
    "A-zero-final",
    {
        endpoint_data.A: 0,
        endpoint_data.C: 0,
        endpoint_data.D: 0,
        endpoint_data.E: 0,
        endpoint_data.F: 0,
    },
)
calculate(
    branches["RO-smooth/H"],
    "AT-zero-final",
    {
        endpoint_data.A: 0,
        endpoint_data.C: 0,
        endpoint_data.D: 0,
        endpoint_data.E: 0,
        endpoint_data.F: 0,
        endpoint_data.T: 0,
    },
)

# S companion: the exact radicals in the released E6 package.
for branch_label in ("RT-reducible/S", "RT-smooth/S"):
    calculate(
        branches[branch_label],
        "CD-zero",
        {endpoint_data.C: 0, endpoint_data.D: 0},
    )
calculate(
    branches["RO-smooth/S"],
    "D-zero",
    {endpoint_data.D: 0},
)
calculate(
    branches["RO-smooth/S"],
    "CD-zero",
    {endpoint_data.C: 0, endpoint_data.D: 0},
)
calculate(
    branches["RO-smooth/S"],
    "ACD-zero",
    {endpoint_data.A: 0, endpoint_data.C: 0, endpoint_data.D: 0},
)
