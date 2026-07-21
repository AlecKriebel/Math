#!/usr/bin/env python3
"""Exact constructions for Discovery 03.

There are two related outputs.

1.  Meng's gradient lift applied directly to the announced three-dimensional
    Keller map gives a six-variable gradient map with constant determinant
    and an explicit three-point fiber.
2.  A rank-compressed BCW homogenization followed by the
    de Bondt--van den Essen symmetrization gives a homogeneous quartic
    Hessian-nilpotent polynomial in 44 variables with an explicit collision
    under Z -> Z-gradient(P).
"""

from __future__ import annotations

import sympy as sp

from stable_reduction import announced_map, degree_reduction, normalized_announced_map

from compressed_construction import (  # noqa: E402
    compressed_collision_points,
    compressed_cubic_map,
    cubic_component_factorization,
)


I = sp.I


def meng_potential():
    """Return the normalized six-variable Meng potential.

    If Phi has identity linear part and determinant one, put

        X=A+iB,  Lambda=(A-iB)/2,  S=Lambda.Phi(X).

    This is Meng's gradient lift followed by a linear congruence.  Its Hessian
    has determinant one and equals the identity at the origin.
    """
    base_variables, mapping, points = normalized_announced_map()
    a_variables = list(sp.symbols("a1:4"))
    b_variables = list(sp.symbols("b1:4"))
    substitutions = {
        base_variables[index]: a_variables[index] + I * b_variables[index]
        for index in range(3)
    }
    dual = [(a_variables[index] - I * b_variables[index]) / 2 for index in range(3)]
    potential = sp.expand(
        sum(dual[index] * mapping[index].subs(substitutions) for index in range(3))
    )
    lifted_points = [
        tuple(coordinate / 2 for coordinate in point)
        + tuple(-I * coordinate / 2 for coordinate in point)
        for point in points
    ]
    return a_variables + b_variables, potential, lifted_points


def meng_gradient_map():
    variables, potential, points = meng_potential()
    gradient = [sp.expand(sp.diff(potential, variable)) for variable in variables]
    return variables, gradient, points


def quartic_potential(expand=False):
    """Return P=i*sum h_j(A+iB)B_j for the compressed 22D cubic map."""
    h_variables, h, _, _ = compressed_cubic_map()
    dimension = len(h_variables)
    a_variables = list(sp.symbols("A1:" + str(dimension + 1)))
    b_variables = list(sp.symbols("B1:" + str(dimension + 1)))
    substitutions = {
        h_variables[index]: a_variables[index] + I * b_variables[index]
        for index in range(dimension)
    }
    potential = I * sum(
        h[index].subs(substitutions) * b_variables[index]
        for index in range(dimension)
    )
    if expand:
        potential = sp.expand(potential)
    return a_variables + b_variables, potential


def symmetric_collision_points(count=2):
    """Lift compressed cubic collisions to the 44D gradient map.

    Write M(x)=I+Jh(x)^T.  In coordinates (A,B)=(x-i*y,y), the map
    Z-gradient(P) has blocks

        x-i*M(x)y,  M(x)y-i*h(x).

    The base points collide under x -> x+h(x).  Taking y=0 at the anchor
    point and solving M(x)y=-i*h(anchor)+i*h(x) at every other point makes
    both displayed blocks common.
    """
    h_variables, h, _, _ = compressed_cubic_map()
    points = compressed_collision_points()[:count]
    jacobian = sp.Matrix(h).jacobian(h_variables)
    data = []
    for point in points:
        substitutions = dict(zip(h_variables, point))
        h_value = sp.Matrix([component.subs(substitutions) for component in h])
        matrix = sp.eye(len(h_variables)) + jacobian.subs(substitutions).T
        data.append((point, h_value, matrix))

    common_second = -I * data[-1][1]
    lifted = []
    for point, h_value, matrix in data:
        y_value = matrix.inv() * (common_second + I * h_value)
        a_value = sp.Matrix(point) - I * y_value
        lifted.append(tuple(a_value) + tuple(y_value))
    return lifted


def evaluate(expressions, variables, point):
    substitutions = dict(zip(variables, point))
    return tuple(sp.simplify(expression.subs(substitutions)) for expression in expressions)


__all__ = [
    "announced_map",
    "compressed_collision_points",
    "compressed_cubic_map",
    "cubic_component_factorization",
    "degree_reduction",
    "evaluate",
    "meng_gradient_map",
    "meng_potential",
    "normalized_announced_map",
    "quartic_potential",
    "symmetric_collision_points",
]
