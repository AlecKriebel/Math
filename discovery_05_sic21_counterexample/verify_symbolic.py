#!/usr/bin/env python3
"""Primary exact SymPy verifier for the SIC(21) certificate."""

from __future__ import annotations

import sympy as sp

from construction import build_construction, evaluate, image_map, image_operator


def main():
    data = build_construction()
    assert len(data.z_variables) == len(data.xi_variables) == len(data.g) == 21
    assert data.injection.shape == (13, 8)
    assert data.injection.rank() == 8

    polynomial = sp.Poly(data.A, *(data.xi_variables + data.z_variables))
    assert polynomial.total_degree() == 4
    assert len(polynomial.terms()) == 72
    print("[1/5] dimensions and sparsity: 21 pairs, degree(A)=4, 72 terms")

    # Exact Schur-complement identity.  Since H2 is quadratic and K is cubic,
    # its right side is J Psi(sX), where Psi=X+H2+BK.
    s = sp.Symbol("s")
    jh2 = sp.Matrix(data.h2).jacobian(data.x_variables)
    jk = sp.Matrix(data.cubic_basis).jacobian(data.x_variables)
    schur = sp.eye(13) + s * jh2 + s**2 * data.injection * jk
    psi = sp.Matrix(data.x_variables) + sp.Matrix(data.h2) + data.injection * sp.Matrix(
        data.cubic_basis
    )
    assert all(sp.expand(left - right) == 0 for left, right in zip(psi, data.psi))
    scaled = {variable: s * variable for variable in data.x_variables}
    target = psi.jacobian(data.x_variables).subs(scaled, simultaneous=True)
    assert all(sp.expand(entry) == 0 for entry in schur - target)
    print("[2/5] exact pencil reduction: det(I+s Jg)=det JPsi(sX)=1")

    mapping = image_map(data)
    images = [evaluate(mapping, data.z_variables, point) for point in data.collision_points]
    assert len(set(data.collision_points)) == 3
    assert images[0] == images[1] == images[2]
    assert tuple(point[0] for point in data.collision_points) == (0, 1, -1)
    expected = (0, 0, sp.Rational(-1, 4), 0, 0, 0, sp.Rational(1, 2)) + (0,) * 14
    assert images[0] == expected
    print("[3/5] exact three-point collision with first coordinates 0, 1, -1")

    assert image_operator(data.A, data.xi_variables, data.z_variables) == 0
    assert image_operator(data.A**2, data.xi_variables, data.z_variables) == 0
    print("[4/5] direct low-order checks: E(A)=E(A^2)=0")

    eb1 = image_operator(data.b * data.A, data.xi_variables, data.z_variables)
    eb2 = image_operator(data.b * data.A**2, data.xi_variables, data.z_variables)
    assert eb1 != 0 and eb2 != 0
    assert sp.expand(eb2 - 3 * data.x_variables[0] ** 2 * data.x_variables[1]) == 0
    print("[5/5] direct obstruction checks: E(bA) != 0 and E(bA^2)=3*x^2*y")
    print("All exact symbolic checks passed.")


if __name__ == "__main__":
    main()
