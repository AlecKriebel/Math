#!/usr/bin/env python3
"""Exact frozen-bridge checks for Q2-E0-A2-B2-D1-N2.

This is a post-freeze checker written from the blinded derivation.  It does
not import any legacy verifier.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


x, y, z, lam, mu = sp.symbols("x y z lam mu")
xyz = (x, y, z)


def monomials(degree: int) -> list[sp.Expr]:
    return [
        x**i * y**j * z**(degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    ]


def coefficient_vector(poly: sp.Expr, degree: int) -> sp.Matrix:
    P = sp.Poly(sp.expand(poly), *xyz)
    return sp.Matrix([P.coeff_monomial(m) for m in monomials(degree)])


def derivation_matrix(p: sp.Expr, q: sp.Expr, degree: int) -> sp.Matrix:
    cross = sp.Matrix([sp.diff(p, v) for v in xyz]).cross(
        sp.Matrix([sp.diff(q, v) for v in xyz])
    )
    columns = []
    for m in monomials(degree):
        dm = sum(cross[i] * sp.diff(m, xyz[i]) for i in range(3))
        columns.append(coefficient_vector(dm, degree + 1))
    return sp.Matrix.hstack(*columns)


def quadratic_matrix(f: sp.Expr) -> sp.Matrix:
    hessian = sp.hessian(f, xyz)
    return hessian / 2


charts = {
    "P111": (x**2 + z**2, y**2 + z**2, "1+1+1"),
    "P11_1": (x**2 + y**2, z**2, "2+1-semisimple"),
    "P2_1": (y**2 + z**2, 2*x*y + z**2, "2+1-Jordan"),
    "P21": (y**2, 2*x*y + z**2, "3-partition-2+1"),
    "P3": (2*y*z, 2*x*z + y**2, "3-partition-3"),
}

expected_determinants = {
    "P111": lam * mu * (lam + mu),
    "P11_1": lam**2 * mu,
    "P2_1": -mu**2 * (lam + mu),
    "P21": -mu**3,
    "P3": -mu**3,
}

expected_cubic_kernels = {
    "P111": [],
    "P11_1": [z**3, z*(x**2 + y**2)],
    "P2_1": [],
    "P21": [y**3, y*(2*x*y + z**2)],
    "P3": [],
}


def normalized_basis(vectors: list[sp.Matrix], degree: int) -> list[str]:
    result = []
    mons = monomials(degree)
    for vector in vectors:
        poly = sp.expand(sum(vector[i] * mons[i] for i in range(len(mons))))
        result.append(str(poly))
    return result


def check_chart(name: str, p: sp.Expr, q: sp.Expr, root_type: str) -> dict:
    pencil_matrix = lam * quadratic_matrix(p) + mu * quadratic_matrix(q)
    determinant = sp.factor(pencil_matrix.det())
    assert sp.expand(determinant - expected_determinants[name]) == 0

    M2 = derivation_matrix(p, q, 2)
    M3 = derivation_matrix(p, q, 3)
    assert M2.shape == (10, 6)
    assert M3.shape == (15, 10)
    assert M2.rank() == 4
    assert M3.rank() == (8 if expected_cubic_kernels[name] else 10)

    k2 = M2.nullspace()
    k3 = M3.nullspace()
    ck2 = M2.T.nullspace()
    ck3 = M3.T.nullspace()
    assert len(k2) == 2
    assert len(ck2) == 6
    assert len(ck3) == 15 - M3.rank()

    expected2 = sp.Matrix.hstack(
        coefficient_vector(p, 2), coefficient_vector(q, 2)
    )
    actual2 = sp.Matrix.hstack(*k2)
    assert expected2.rank() == 2
    assert expected2.row_join(actual2).rank() == 2

    if expected_cubic_kernels[name]:
        expected3 = sp.Matrix.hstack(
            *(coefficient_vector(f, 3) for f in expected_cubic_kernels[name])
        )
        actual3 = sp.Matrix.hstack(*k3)
        assert expected3.rank() == 2
        assert expected3.row_join(actual3).rank() == 2
    else:
        assert k3 == []

    return {
        "chart": name,
        "p": str(p),
        "q": str(q),
        "determinant": str(determinant),
        "root_type": root_type,
        "D2": {
            "shape": list(M2.shape),
            "rank": M2.rank(),
            "kernel_dimension": len(k2),
            "kernel": [str(p), str(q)],
            "cokernel_dimension": len(ck2),
            "dual_cokernel_basis": normalized_basis(ck2, 3),
        },
        "D3": {
            "shape": list(M3.shape),
            "rank": M3.rank(),
            "kernel_dimension": len(k3),
            "kernel": [str(f) for f in expected_cubic_kernels[name]],
            "cokernel_dimension": len(ck3),
            "dual_cokernel_basis": normalized_basis(ck3, 4),
        },
    }


def check_coefficient_map() -> dict:
    aa = sp.symbols("a0:6")
    bb = sp.symbols("b0:6")
    p = aa[0]*x**2 + aa[1]*x*y + aa[2]*x*z + aa[3]*y**2 + aa[4]*y*z + aa[5]*z**2
    q = bb[0]*x**2 + bb[1]*x*y + bb[2]*x*z + bb[3]*y**2 + bb[4]*y*z + bb[5]*z**2
    frozen = [
        x**4, x**3*y, x**3*z, x**2*y**2, x**2*y*z,
        x**2*z**2, x*y**3, x*y**2*z, x*y*z**2, x*z**3,
        y**4, y**3*z, y**2*z**2, y*z**3, z**4,
    ]
    expanded = []
    for f in (p**2, p*q, q**2):
        P = sp.Poly(sp.expand(f), *xyz)
        expanded.append([P.coeff_monomial(m) for m in frozen])
    assert len(expanded) == 3 and all(len(row) == 15 for row in expanded)

    r0, r1, r2, s0, s1, s2 = sp.symbols("r0 r1 r2 s0 s1 s2")
    u = sp.symbols("u1:4")
    v = sp.symbols("v1:4")
    rho = [
        r0*expanded[0][i] + r1*expanded[1][i] + r2*expanded[2][i]
        for i in range(15)
    ]
    sigma = [
        s0*expanded[0][i] + s1*expanded[1][i] + s2*expanded[2][i]
        for i in range(15)
    ]
    coefficients = [
        sp.expand(u[k]*rho[i] + v[k]*sigma[i])
        for k in range(3)
        for i in range(15)
    ]
    assert len(coefficients) == 45

    R = r0*p**2 + r1*p*q + r2*q**2
    S = s0*p**2 + s1*p*q + s2*q**2
    for k in range(3):
        direct = sp.Poly(sp.expand(u[k]*R + v[k]*S), *xyz)
        for i, monomial in enumerate(frozen):
            assert sp.expand(
                coefficients[15*k+i] - direct.coeff_monomial(monomial)
            ) == 0
    return {
        "input_parameters": 6 + 6 + 3 + 3 + 3 + 3,
        "output_coefficients": len(coefficients),
        "map_kind": "polynomial convolution; no divisions",
        "pivot_rule": "Ci is c0=...=c(i-1)=0 and ci!=0",
    }


def main() -> None:
    results = [
        check_chart(name, p, q, root_type)
        for name, (p, q, root_type) in charts.items()
    ]
    composite_p, composite_q = x**2, y**2
    composite_det = sp.expand(
        (lam*quadratic_matrix(composite_p) + mu*quadratic_matrix(composite_q)).det()
    )
    assert composite_det == 0

    certificate = {
        "method": "SymPy exact rational matrices and symbolic convolution",
        "charts": results,
        "composite_boundary": {
            "p": str(composite_p),
            "q": str(composite_q),
            "determinant": "0",
            "field_drop": "C((x/y)^2) is properly contained in C(x/y)",
            "route": "Q2-E0-A1-B4-D1-N4",
        },
        "coefficient_map": check_coefficient_map(),
    }
    output = Path(__file__).with_name("bridge_exact_data_sympy.json")
    output.write_text(json.dumps(certificate, indent=2) + "\n")
    print("PASS: five conic-pencil charts and composite boundary")
    for row in results:
        print(
            f"  {row['chart']}: "
            f"D2 rank/kernel/cokernel={row['D2']['rank']}/"
            f"{row['D2']['kernel_dimension']}/{row['D2']['cokernel_dimension']}; "
            f"D3={row['D3']['rank']}/"
            f"{row['D3']['kernel_dimension']}/{row['D3']['cokernel_dimension']}"
        )
    print("PASS: polynomial 45-coefficient frozen-pivot map")


if __name__ == "__main__":
    main()
