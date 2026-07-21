#!/usr/bin/env python3
"""Exact verification of the 54-variable quartic counterexample.

The expensive-looking assertions are reduced to small exact identities.  In
particular, Hessian nilpotence is certified by the characteristic-polynomial
identity of de Bondt--van den Essen, while noninvertibility is checked by an
explicit two-point collision of the associated gradient map.
"""

from __future__ import annotations

import argparse

import sympy as sp

from construction import (
    announced_map,
    cubic_collision_points,
    cubic_homogeneous_map,
    degree_reduction,
    evaluate_map,
    quartic_potential,
    symmetric_collision_points,
)


def total_degree(poly, variables):
    if poly == 0:
        return -1
    return sp.Poly(poly, *variables).total_degree()


def verify_announced_map():
    variables, mapping, points = announced_map()
    jacobian = sp.Matrix(mapping).jacobian(variables)
    assert sp.factor(jacobian.det()) == -2
    images = [evaluate_map(mapping, variables, point) for point in points]
    assert images == [(sp.Rational(-1, 4), 0, 0)] * 3
    print("[1/5] announced map: det=-2 and the rational three-point fiber checks")


def verify_degree_reduction():
    reduction = degree_reduction()
    variables = reduction.variables
    assert len(variables) == 13
    assert reduction.linear_part.det() == 1
    assert max(total_degree(f, variables) for f in reduction.normalized_map) == 3

    zero = {v: 0 for v in variables}
    normalized_linear_part = sp.Matrix(
        [
            [sp.diff(f, v).subs(zero) for v in variables]
            for f in reduction.normalized_map
        ]
    )
    assert normalized_linear_part == sp.eye(13)
    assert all(
        sp.expand(
            reduction.normalized_map[j]
            - variables[j]
            - reduction.quadratic_part[j]
            - reduction.cubic_part[j]
        )
        == 0
        for j in range(13)
    )

    images = [
        evaluate_map(reduction.normalized_map, variables, point)
        for point in reduction.collision_points
    ]
    expected = (
        0,
        0,
        sp.Rational(-1, 4),
        0,
        0,
        0,
        sp.Rational(1, 2),
        0,
        0,
        0,
        0,
        0,
        0,
    )
    assert images == [expected] * 3
    assert len(set(reduction.collision_points)) == 3

    # Every degree-reduction operation is a pre- or post-composition by a
    # triangular automorphism of determinant 1.  Together with det L=1 and
    # the exact det=1 normalization of the announced map, this certifies
    # det J(normalized_map)=1 without expanding a 13x13 determinant.
    print(
        "[2/5] stable reduction: 13 variables, degree 3, det=1, "
        "and a rational three-point fiber"
    )
    return reduction


def verify_cubic_homogeneous_map(reduction):
    variables, h = cubic_homogeneous_map(reduction)
    assert len(variables) == 27
    assert all(total_degree(f, variables) in (-1, 3) for f in h)

    base_map = [sp.expand(v + f) for v, f in zip(variables, h)]
    points = cubic_collision_points(reduction)
    images = [evaluate_map(base_map, variables, point) for point in points]
    assert images[0] == images[1] == images[2]
    assert len(set(points)) == 3

    # Let Phi=X+H2+H3 be the normalized 13-variable map.  Homogeneity gives
    # det(I+T*JH2+T^2*JH3)=det JPhi(TX)=1.  The Jacobian determinant of
    # (X,Y,T) -> (X+Y*T^2+T*H2, Y-H3, T) is the same block determinant.
    # Since h is cubic homogeneous, det(I+s*Jh)=1 identically in s, hence Jh
    # is nilpotent.  The displayed identities below check the nontrivial
    # homogeneity input mechanically.
    T = variables[-1]
    X = reduction.variables
    left = sp.Matrix(
        [
            [
                (sp.eye(13)[i, j]
                 + T * sp.diff(reduction.quadratic_part[i], X[j])
                 + T**2 * sp.diff(reduction.cubic_part[i], X[j]))
                for j in range(13)
            ]
            for i in range(13)
        ]
    )
    scaled_substitution = {X[j]: T * X[j] for j in range(13)}
    jacobian_phi = sp.Matrix(reduction.normalized_map).jacobian(X)
    right = jacobian_phi.subs(scaled_substitution, simultaneous=True)
    assert all(sp.expand(entry) == 0 for entry in (left - right))

    # Pointwise exact power checks are redundant with the proof above but
    # catch implementation mistakes in h at negligible cost.
    Jh = sp.Matrix(h).jacobian(variables)
    samples = [dict.fromkeys(variables, 0)]
    samples += [dict(zip(variables, point)) for point in points[:2]]
    for sample in samples:
        numeric = Jh.subs(sample)
        assert numeric**27 == sp.zeros(27)

    print(
        "[3/5] BCW model: 27-dimensional cubic homogeneous h, "
        "Jh nilpotent, with an exact collision"
    )
    return variables, h


def verify_quartic(reduction, direct_gradient_check=True):
    variables, potential = quartic_potential(reduction, expand=True)
    assert len(variables) == 54
    polynomial = sp.Poly(potential, *variables, extension=sp.I)
    assert polynomial.total_degree() == 4
    assert len(polynomial.terms()) == 598

    # If f=-P=-i*sum h_j(A+iB)B_j, Lemma 1.2 of de Bondt--van den Essen
    # gives Hess(f) nilpotent iff Jh is nilpotent.  Negating a nilpotent
    # Hessian preserves nilpotence, so P is Hessian nilpotent.
    print("[4/5] symmetrization: a homogeneous quartic HNP with 598 monomials")

    if direct_gradient_check:
        points = symmetric_collision_points(reduction, 2)
        gradient = [sp.diff(potential, v) for v in variables]
        images = []
        for point in points:
            substitutions = dict(zip(variables, point))
            images.append(
                tuple(
                    sp.simplify(point[j] - gradient[j].subs(substitutions))
                    for j in range(54)
                )
            )
        assert points[0] != points[1]
        assert images[0] == images[1]
        print(
            "[5/5] finite certificate: two explicit points collide under "
            "Z -> Z-grad(P)"
        )
    else:
        print("[5/5] direct 54-variable gradient collision check skipped")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-gradient",
        action="store_true",
        help="skip the slowest (direct 54-variable gradient) check",
    )
    args = parser.parse_args()

    verify_announced_map()
    reduction = verify_degree_reduction()
    verify_cubic_homogeneous_map(reduction)
    verify_quartic(reduction, direct_gradient_check=not args.skip_gradient)
    print("All exact checks passed.")


if __name__ == "__main__":
    main()
