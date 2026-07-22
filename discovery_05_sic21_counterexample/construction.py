#!/usr/bin/env python3
"""Exact construction underlying Discovery 05.

The input is the certified 13-variable stable model from Discovery 03,

    Psi(X) = X + H2(X) + B K(X),

where H2 is quadratic and K has eight cubic components.  On Z=(X,U) put

    g(X,U) = (H2(X) + B U, -K(X)).

Then det(I+s Jg)=1.  The polynomial used for the Special Image Conjecture is

    A(xi,Z) = -sum_j xi_j g_j(Z).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
D3 = ROOT / "discovery_03_small_vanishing_counterexample"
if str(D3) not in sys.path:
    sys.path.insert(0, str(D3))

from compressed_construction import cubic_component_factorization  # noqa: E402
from stable_reduction import degree_reduction  # noqa: E402


@dataclass
class SICConstruction:
    x_variables: list[sp.Symbol]
    u_variables: list[sp.Symbol]
    z_variables: list[sp.Symbol]
    xi_variables: list[sp.Symbol]
    h2: list[sp.Expr]
    injection: sp.Matrix
    cubic_basis: list[sp.Expr]
    psi: list[sp.Expr]
    g: list[sp.Expr]
    A: sp.Expr
    b: sp.Expr
    collision_points: list[tuple[sp.Expr, ...]]


def build_construction() -> SICConstruction:
    reduction = degree_reduction()
    injection, cubic_basis, _ = cubic_component_factorization(reduction)
    x_variables = list(reduction.variables)
    u_variables = list(sp.symbols("U1:9"))
    z_variables = x_variables + u_variables
    xi_variables = list(sp.symbols("xi1:22"))

    first_block = list(
        sp.Matrix(reduction.quadratic_part) + injection * sp.Matrix(u_variables)
    )
    g = [sp.expand(component) for component in first_block]
    g.extend(sp.expand(-component) for component in cubic_basis)
    A = sp.expand(-sum(xi * component for xi, component in zip(xi_variables, g)))

    collision_points = []
    for point in reduction.collision_points:
        substitutions = dict(zip(x_variables, point))
        u_value = tuple(sp.expand(k.subs(substitutions)) for k in cubic_basis)
        collision_points.append(tuple(point) + u_value)

    return SICConstruction(
        x_variables=x_variables,
        u_variables=u_variables,
        z_variables=z_variables,
        xi_variables=xi_variables,
        h2=[sp.expand(component) for component in reduction.quadratic_part],
        injection=injection,
        cubic_basis=[sp.expand(component) for component in cubic_basis],
        psi=[sp.expand(component) for component in reduction.normalized_map],
        g=g,
        A=A,
        b=x_variables[0],
        collision_points=collision_points,
    )


def evaluate(expressions, variables, point):
    substitutions = dict(zip(variables, point))
    return tuple(sp.expand(expression.subs(substitutions)) for expression in expressions)


def image_map(construction: SICConstruction):
    return [
        sp.expand(variable + component)
        for variable, component in zip(construction.z_variables, construction.g)
    ]


def image_operator(expression, xi_variables, z_variables):
    """Apply E(xi^alpha p(Z))=partial_Z^alpha p(Z) exactly."""
    polynomial = sp.Poly(sp.expand(expression), *xi_variables)
    answer = sp.Integer(0)
    for alpha, coefficient in polynomial.terms():
        term = coefficient
        for variable, order in zip(z_variables, alpha):
            if order:
                term = sp.diff(term, variable, order)
        answer += term
    return sp.expand(answer)


__all__ = [
    "SICConstruction",
    "build_construction",
    "evaluate",
    "image_map",
    "image_operator",
]
