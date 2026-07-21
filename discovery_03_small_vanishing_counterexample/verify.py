#!/usr/bin/env python3
"""Exact proof-side checks for the two Discovery 03 constructions."""

from __future__ import annotations

import argparse

import sympy as sp

from construction import (
    announced_map,
    compressed_collision_points,
    compressed_cubic_map,
    cubic_component_factorization,
    degree_reduction,
    evaluate,
    meng_gradient_map,
    meng_potential,
    normalized_announced_map,
    quartic_potential,
    symmetric_collision_points,
)


def total_degree(polynomial, variables):
    if polynomial == 0:
        return -1
    return sp.Poly(polynomial, *variables).total_degree()


def verify_source():
    variables, mapping, points = announced_map()
    jacobian = sp.Matrix(mapping).jacobian(variables)
    assert sp.factor(jacobian.det()) == -2
    images = [evaluate(mapping, variables, point) for point in points]
    assert len(set(points)) == 3
    assert images == [(sp.Rational(-1, 4), 0, 0)] * 3
    print("[1/6] source: det JF=-2 and the rational three-point fiber checks")


def verify_meng_lift():
    base_variables, source_map, source_points = normalized_announced_map()
    variables, potential, points = meng_potential()
    gradient_variables, gradient, gradient_points = meng_gradient_map()
    assert variables == gradient_variables and points == gradient_points
    assert len(variables) == 6
    polynomial = sp.Poly(potential, *variables)
    assert polynomial.total_degree() == 8
    assert len(polynomial.terms()) == 204

    # Before the coordinate change, lambda.Phi(x) has Hessian blocks
    # [[A, JPhi^T], [JPhi, 0]], hence determinant -(det JPhi)^2=-1.
    # The change (x,lambda)=(a+i*b,(a-i*b)/2) has determinant i, so Hessian
    # congruence multiplies the determinant by i^2=-1.  Thus det Hess(S)=1.
    # We check the congruence and its ingredients entry by entry.
    x1, x2, x3 = base_variables
    l1, l2, l3 = sp.symbols("l1 l2 l3")
    lambdas = [l1, l2, l3]
    base_potential = sp.expand(sum(lambdas[j] * source_map[j] for j in range(3)))
    base_hessian = sp.hessian(base_potential, list(base_variables) + lambdas)
    a_variables = variables[:3]
    b_variables = variables[3:]
    base_substitutions = {
        base_variables[j]: a_variables[j] + sp.I * b_variables[j]
        for j in range(3)
    }
    base_substitutions.update(
        {lambdas[j]: (a_variables[j] - sp.I * b_variables[j]) / 2 for j in range(3)}
    )
    coordinate_matrix = sp.zeros(6)
    for j in range(3):
        coordinate_matrix[j, j] = 1
        coordinate_matrix[j, j + 3] = sp.I
        coordinate_matrix[j + 3, j] = sp.Rational(1, 2)
        coordinate_matrix[j + 3, j + 3] = -sp.I / 2
    hessian = sp.hessian(potential, variables)
    source_jacobian = sp.Matrix(source_map).jacobian(base_variables)
    transformed = coordinate_matrix.T * base_hessian.subs(
        base_substitutions, simultaneous=True
    ) * coordinate_matrix
    assert all(sp.expand(entry) == 0 for entry in hessian - transformed)
    assert coordinate_matrix.det() == sp.I
    assert sp.factor(source_jacobian.det()) == 1
    assert hessian.subs(dict.fromkeys(variables, 0)) == sp.eye(6)

    images = [evaluate(gradient, variables, point) for point in points]
    assert len(set(points)) == 3
    assert images[0] == images[1] == images[2]
    assert images[0] == (0, 0, sp.Rational(-1, 8), 0, 0, sp.I / 8)
    print(
        "[2/6] Meng lift: a 6-variable identity-linear gradient Keller map, "
        "det Hess(S)=1, with a Q(i) three-point fiber"
    )


def verify_compression():
    reduction = degree_reduction()
    injection, basis, indices = cubic_component_factorization(reduction)
    assert len(reduction.variables) == 13
    assert injection.shape == (13, 8)
    assert injection.rank() == 8
    assert len(basis) == 8
    assert indices == (0, 1, 2, 5, 6, 9, 10, 11)
    assert injection * sp.Matrix(basis) == sp.Matrix(reduction.cubic_part)
    print(
        "[3/6] compression: the 13 cubic components span an 8-dimensional "
        "space, with H3=B*K exactly"
    )
    return reduction, injection, basis


def verify_compressed_cubic(reduction, injection, basis):
    variables, h, returned_injection, returned_basis = compressed_cubic_map(reduction)
    assert returned_injection == injection
    assert returned_basis == basis
    assert len(variables) == 22
    assert all(total_degree(component, variables) in (-1, 3) for component in h)

    points = compressed_collision_points(reduction)
    base_map = [sp.expand(variable + component) for variable, component in zip(variables, h)]
    images = [evaluate(base_map, variables, point) for point in points]
    assert len(set(points)) == 3
    assert images[0] == images[1] == images[2]

    # For a scalar s, the determinant of I+s*Jh reduces by a Schur
    # complement to
    #   det(I+s*T*JH2+s^2*T^2*B*JK)
    # = det J(Phi)(s*T*X) = 1.
    # Here we check the polynomial matrix identity that carries all the
    # nontrivial algebra; det J(Phi)=1 follows from the certified stable
    # equivalence used in Discovery 02.
    x_variables = reduction.variables
    t = variables[-1]
    s = sp.Symbol("s")
    jh2 = sp.Matrix(reduction.quadratic_part).jacobian(x_variables)
    jk = sp.Matrix(basis).jacobian(x_variables)
    schur = sp.eye(13) + s * t * jh2 + s**2 * t**2 * injection * jk
    scaled = {variable: s * t * variable for variable in x_variables}
    jphi = sp.Matrix(reduction.normalized_map).jacobian(x_variables)
    target = jphi.subs(scaled, simultaneous=True)
    assert all(sp.expand(entry) == 0 for entry in schur - target)

    # Exact pointwise powers are redundant with the identity above, but make
    # useful implementation guards at two nontrivial rational points.
    jacobian_h = sp.Matrix(h).jacobian(variables)
    for point in points[:2]:
        matrix = jacobian_h.subs(dict(zip(variables, point)))
        assert matrix**22 == sp.zeros(22)
    print(
        "[4/6] compressed BCW map: 22D cubic homogeneous h, Jh nilpotent, "
        "with an exact three-point fiber"
    )
    return variables, h


def verify_quartic(direct_gradient_check=True):
    variables, potential = quartic_potential(expand=True)
    polynomial = sp.Poly(potential, *variables, extension=sp.I)
    assert len(variables) == 44
    assert polynomial.total_degree() == 4
    assert len(polynomial.terms()) == 538

    # The de Bondt--van den Essen symmetrization lemma says that for
    # P=i*sum h_j(A+iB)B_j, Hess(P) is nilpotent iff Jh is nilpotent.
    # Step [4/6] supplies the exact hypothesis.
    print("[5/6] symmetrization: a 44-variable homogeneous quartic HNP (538 terms)")

    if direct_gradient_check:
        points = symmetric_collision_points(2)
        gradient = [sp.diff(potential, variable) for variable in variables]
        images = [
            tuple(
                sp.simplify(point[index] - gradient[index].subs(dict(zip(variables, point))))
                for index in range(44)
            )
            for point in points
        ]
        assert points[0] != points[1]
        assert images[0] == images[1]
        print(
            "[6/6] finite certificate: two exact Q(i)-points collide under "
            "Z-gradient(P)"
        )
    else:
        print("[6/6] direct 44-variable gradient collision check skipped")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-gradient", action="store_true")
    arguments = parser.parse_args()

    verify_source()
    verify_meng_lift()
    reduction, injection, basis = verify_compression()
    verify_compressed_cubic(reduction, injection, basis)
    verify_quartic(direct_gradient_check=not arguments.skip_gradient)
    print("All exact checks passed.")


if __name__ == "__main__":
    main()
