#!/usr/bin/env python3
"""Self-contained 13-variable stable reduction used by Discovery 03."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import sympy as sp


@dataclass
class Reduction:
    variables: list[sp.Symbol]
    map_before_linear_normalization: list[sp.Expr]
    linear_part: sp.Matrix
    normalized_map: list[sp.Expr]
    quadratic_part: list[sp.Expr]
    cubic_part: list[sp.Expr]
    collision_points: list[tuple[sp.Rational, ...]]


def announced_map():
    x, y, z = sp.symbols("x y z")
    u = 1 + x * y
    mapping = [
        sp.expand(u**3 * z + y**2 * u * (4 + 3 * x * y)),
        sp.expand(y + 3 * x * u**2 * z + 3 * x * y**2 * (4 + 3 * x * y)),
        sp.expand(2 * x - 3 * x**2 * y - x**3 * z),
    ]
    points = [
        (sp.Rational(0), sp.Rational(0), sp.Rational(-1, 4)),
        (sp.Rational(1), sp.Rational(-3, 2), sp.Rational(13, 2)),
        (sp.Rational(-1), sp.Rational(3, 2), sp.Rational(13, 2)),
    ]
    return (x, y, z), mapping, points


def normalized_announced_map():
    variables, raw, points = announced_map()
    return list(variables), [sp.expand(raw[2] / 2), raw[1], raw[0]], points


def degree_reduction() -> Reduction:
    variables, mapping, collision_points = normalized_announced_map()
    x, y, z = variables

    def extend_points(P, Q=None):
        nonlocal collision_points
        old_variables = variables[:]
        extended = []
        for point in collision_points:
            substitutions = dict(zip(old_variables, point))
            values = list(point)
            values.append(sp.expand(-P.subs(substitutions)))
            if Q is not None:
                values.append(sp.expand(-Q.subs(substitutions)))
            extended.append(tuple(values))
        collision_points = extended

    def standard_gadget(target, P, Q, coefficient, name):
        nonlocal variables, mapping
        extend_points(P, Q)
        a, b = sp.symbols(f"{name}a {name}b")
        variables.extend([a, b])
        mapping.extend([sp.expand(a + P), sp.expand(b + Q)])
        mapping[target] = sp.expand(
            mapping[target] - coefficient * mapping[-2] * mapping[-1]
        )
        return len(variables) - 2, len(variables) - 1

    def reuse_second_factor(target, P, second_index, coefficient, name):
        nonlocal variables, mapping
        extend_points(P)
        a = sp.symbols(f"{name}a")
        variables.append(a)
        mapping.append(sp.expand(a + P))
        mapping[target] = sp.expand(
            mapping[target] - coefficient * mapping[-1] * mapping[second_index]
        )
        return len(variables) - 1

    def reuse_first_factor(target, first_index, Q, coefficient, name):
        nonlocal variables, mapping
        extend_points(Q)
        b = sp.symbols(f"{name}b")
        variables.append(b)
        mapping.append(sp.expand(b + Q))
        mapping[target] = sp.expand(
            mapping[target] - coefficient * mapping[first_index] * mapping[-1]
        )
        return len(variables) - 1

    a1, b1 = standard_gadget(
        0, x**2, x * z + 3 * y, -sp.Rational(1, 2), "g1"
    )
    a2, b2 = standard_gadget(
        1, 3 * x**2 * y, 2 * z + x * y * z + 3 * y**2, 1, "g2"
    )
    a3, b3 = standard_gadget(
        1, x * y, variables[a2] * z + 3 * x * variables[b2], -1, "g3"
    )
    a4, b4 = standard_gadget(
        2,
        x * y**2,
        7 * y + 3 * x * z + 3 * x * y**2 + x**2 * y * z,
        1,
        "g4",
    )
    a5 = reuse_second_factor(2, variables[a4] * x * y, b1, -1, "g5")
    b6 = reuse_first_factor(
        2,
        a3,
        variables[a4] * variables[b1] - y * variables[b4],
        1,
        "g6",
    )
    del a1, a5, b3, b6

    mapping[b4] = sp.expand(mapping[b4] - mapping[a3] * mapping[b1])

    zero = {variable: 0 for variable in variables}
    linear_part = sp.Matrix(
        [[sp.diff(component, variable).subs(zero) for variable in variables]
         for component in mapping]
    )
    normalized = [sp.expand(component) for component in linear_part.inv() * sp.Matrix(mapping)]

    def homogeneous_part(polynomial, degree):
        poly = sp.Poly(polynomial, *variables)
        return sp.Add(
            *[
                coefficient
                * sp.prod(variable**exponent for variable, exponent in zip(variables, monomial))
                for monomial, coefficient in poly.terms()
                if sum(monomial) == degree
            ]
        )

    return Reduction(
        variables=variables,
        map_before_linear_normalization=mapping,
        linear_part=linear_part,
        normalized_map=normalized,
        quadratic_part=[homogeneous_part(component, 2) for component in normalized],
        cubic_part=[homogeneous_part(component, 3) for component in normalized],
        collision_points=collision_points,
    )


def evaluate(expressions: Sequence[sp.Expr], variables, point):
    substitutions = dict(zip(variables, point))
    return tuple(sp.expand(expression.subs(substitutions)) for expression in expressions)
