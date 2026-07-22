#!/usr/bin/env python3
"""Exact constructions for Discovery 06.

The main object is a 14-variable polynomial vector ``g`` obtained by placing
the degree 3--7 tails of the normalized three-variable map in three constant
nilpotent state chains of lengths 2, 4, and 5.  The map in the theorem is
``T = identity + g``.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


@dataclass(frozen=True)
class Construction:
    base_variables: tuple[sp.Symbol, ...]
    state_variables: tuple[sp.Symbol, ...]
    variables: tuple[sp.Symbol, ...]
    xi_variables: tuple[sp.Symbol, ...]
    homogeneous_parts: tuple[tuple[sp.Expr, ...], ...]
    phi: tuple[sp.Expr, ...]
    B: sp.Matrix
    N: sp.Matrix
    C: sp.Matrix
    g: tuple[sp.Expr, ...]
    A: sp.Expr
    b: sp.Expr
    source_points: tuple[tuple[sp.Rational, ...], ...]
    collision_points: tuple[tuple[sp.Rational, ...], ...]


def _evaluate(expressions, variables, point):
    substitutions = dict(zip(variables, point))
    return tuple(sp.expand(expression.subs(substitutions)) for expression in expressions)


def build_construction() -> Construction:
    x, y, z = sp.symbols("x y z")
    base_variables = (x, y, z)

    # H[d-2] is the homogeneous degree-d part of Phi-identity.
    homogeneous_parts = (
        (0, 3 * x * z, 4 * y**2),
        (-sp.Rational(3, 2) * x**2 * y, 12 * x * y**2, 3 * x * y * z),
        (-sp.Rational(1, 2) * x**3 * z, 6 * x**2 * y * z, 7 * x * y**3),
        (0, 9 * x**2 * y**3, 3 * x**2 * y**2 * z),
        (0, 3 * x**3 * y**2 * z, 3 * x**2 * y**4),
        (0, 0, x**3 * y**3 * z),
    )
    phi = tuple(
        sp.expand(variable + sum(part[index] for part in homogeneous_parts))
        for index, variable in enumerate(base_variables)
    )

    # State order: the length-2 chain for output 1, the length-4 chain for
    # output 2, then the length-5 chain for output 3.
    state_variables = sp.symbols("u11 u12 u21 u22 u23 u24 u31 u32 u33 u34 u35")
    variables = base_variables + state_variables
    xi_variables = sp.symbols("xi1:15")

    B = sp.zeros(3, 11)
    B[0, 0] = B[1, 2] = B[2, 6] = 1
    N = sp.zeros(11)
    for start, length in ((0, 2), (2, 4), (6, 5)):
        for offset in range(length - 1):
            N[start + offset, start + offset + 1] = 1

    tails = (
        homogeneous_parts[1][0], homogeneous_parts[2][0],
        homogeneous_parts[1][1], homogeneous_parts[2][1],
        homogeneous_parts[3][1], homogeneous_parts[4][1],
        homogeneous_parts[1][2], homogeneous_parts[2][2],
        homogeneous_parts[3][2], homogeneous_parts[4][2],
        homogeneous_parts[5][2],
    )
    C = sp.Matrix(tails)
    U = sp.Matrix(state_variables)
    top = sp.Matrix(homogeneous_parts[0]) + B * U
    bottom = -C - N * U
    g = tuple(sp.expand(entry) for entry in top.col_join(bottom))
    A = sp.expand(-sum(xi * component for xi, component in zip(xi_variables, g)))
    b = x + y + state_variables[0]

    source_points = (
        (sp.Rational(0), sp.Rational(0), sp.Rational(-1, 4)),
        (sp.Rational(1), sp.Rational(-3, 2), sp.Rational(13, 2)),
        (sp.Rational(-1), sp.Rational(3, 2), sp.Rational(13, 2)),
    )

    # On a zero state target, (I-N)U=C.  Thus each state coordinate is the
    # tail sum in its chain and the first three coordinates become Phi(X).
    collision_points = []
    inverse_state = sum((N**power for power in range(11)), sp.zeros(11))
    for point in source_points:
        state = inverse_state * C.subs(dict(zip(base_variables, point)))
        collision_points.append(tuple(point) + tuple(sp.Rational(value) for value in state))

    return Construction(
        base_variables=base_variables,
        state_variables=state_variables,
        variables=variables,
        xi_variables=xi_variables,
        homogeneous_parts=homogeneous_parts,
        phi=phi,
        B=B,
        N=N,
        C=C,
        g=g,
        A=A,
        b=b,
        source_points=source_points,
        collision_points=tuple(collision_points),
    )


def map_T(data: Construction):
    return tuple(sp.expand(variable + component) for variable, component in zip(data.variables, data.g))


def homogeneous_companion(data: Construction):
    """Return the 15-variable degree-seven homogeneous vector (h,0)."""
    w = sp.Symbol("w")
    variables = data.variables + (w,)
    substitutions = {variable: variable / w for variable in data.variables}
    h = tuple(sp.cancel(w**7 * component.subs(substitutions)) for component in data.g) + (sp.S.Zero,)
    return variables, h


def evaluate(expressions, variables, point):
    return _evaluate(expressions, variables, point)


__all__ = [
    "Construction",
    "build_construction",
    "evaluate",
    "homogeneous_companion",
    "map_T",
]
