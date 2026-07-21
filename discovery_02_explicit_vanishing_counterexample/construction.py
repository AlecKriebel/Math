#!/usr/bin/env python3
"""Exact straight-line construction of the quartic HN counterexample.

The construction starts from the normalized Alpoge map, uses six stable
degree-reduction gadgets (four two-variable and two one-variable gadgets),
then applies the BCW unipotent homogenization and the de Bondt--van den Essen
symmetrization.

The final quartic is intentionally kept as a straight-line expression:

    P(A,B) = i * sum_j h_j(A + i B) B_j,

where h is the 27-dimensional cubic homogeneous map returned by
``cubic_homogeneous_map``.  Expanding P is unnecessary and much less useful
than this exact representation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import sympy as sp


I = sp.I


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
    """Return the announced map, its variables, and its three-point fiber."""
    x, y, z = sp.symbols("x y z")
    u = 1 + x * y
    raw = [
        sp.expand(u**3 * z + y**2 * u * (4 + 3 * x * y)),
        sp.expand(y + 3 * x * u**2 * z + 3 * x * y**2 * (4 + 3 * x * y)),
        sp.expand(2 * x - 3 * x**2 * y - x**3 * z),
    ]
    points = [
        (sp.Rational(0), sp.Rational(0), sp.Rational(-1, 4)),
        (sp.Rational(1), sp.Rational(-3, 2), sp.Rational(13, 2)),
        (sp.Rational(-1), sp.Rational(3, 2), sp.Rational(13, 2)),
    ]
    return (x, y, z), raw, points


def normalized_announced_map():
    """Postcompose the announced map so its linear part is the identity."""
    variables, raw, points = announced_map()
    # J(raw)(0) sends (x,y,z) to (z,y,2x), hence its inverse sends
    # (P,Q,R) to (R/2,Q,P).
    normalized = [sp.expand(raw[2] / 2), raw[1], raw[0]]
    return list(variables), normalized, points


def _evaluate(expressions: Sequence[sp.Expr], variables, point):
    substitutions = dict(zip(variables, point))
    return tuple(sp.expand(f.subs(substitutions)) for f in expressions)


def degree_reduction() -> Reduction:
    """Construct the 13-dimensional degree-at-most-three stable model."""
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
        """Add a+P,b+Q and subtract coefficient*(a+P)*(b+Q)."""
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
        """Add a+P and multiply it by an already encoded output factor."""
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
        """Add b+Q and multiply it by an already encoded output factor."""
        nonlocal variables, mapping
        extend_points(Q)
        b = sp.symbols(f"{name}b")
        variables.append(b)
        mapping.append(sp.expand(b + Q))
        mapping[target] = sp.expand(
            mapping[target] - coefficient * mapping[first_index] * mapping[-1]
        )
        return len(variables) - 1

    # Gadget 1 removes all nonlinear terms of the first coordinate.
    a1, b1 = standard_gadget(
        0, x**2, x * z + 3 * y, -sp.Rational(1, 2), "g1"
    )

    # Gadgets 2--3 reduce the second coordinate.  The high-degree part is
    # 3*x**2*y*(2*z + x*y*z + 3*y**2); its two residual branches share xy.
    a2, b2 = standard_gadget(
        1, 3 * x**2 * y, 2 * z + x * y * z + 3 * y**2, 1, "g2"
    )
    a3, b3 = standard_gadget(
        1, x * y, variables[a2] * z + 3 * x * variables[b2], -1, "g3"
    )

    # Gadgets 4--6 reduce the third coordinate.  The factor xz+3y encoded
    # by gadget 1 and the factor xy encoded by gadget 3 are reused, saving
    # three auxiliary variables.
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
    del a5, b3, b6  # names document the construction; indices are not reused.

    # A final output shear removes the degree-four part of the b4 coordinate
    # using two already encoded factors; it needs no new variable.
    mapping[b4] = sp.expand(mapping[b4] - mapping[a3] * mapping[b1])

    zero = {v: 0 for v in variables}
    linear_part = sp.Matrix(
        [[sp.diff(f, v).subs(zero) for v in variables] for f in mapping]
    )
    normalized = [sp.expand(f) for f in linear_part.inv() * sp.Matrix(mapping)]

    def homogeneous_part(poly, degree):
        P = sp.Poly(poly, *variables)
        return sp.Add(
            *[
                coefficient * sp.prod(v**e for v, e in zip(variables, monomial))
                for monomial, coefficient in P.terms()
                if sum(monomial) == degree
            ]
        )

    quadratic = [homogeneous_part(f, 2) for f in normalized]
    cubic = [homogeneous_part(f, 3) for f in normalized]
    return Reduction(
        variables=variables,
        map_before_linear_normalization=mapping,
        linear_part=linear_part,
        normalized_map=normalized,
        quadratic_part=quadratic,
        cubic_part=cubic,
        collision_points=collision_points,
    )


def cubic_homogeneous_map(reduction: Reduction | None = None):
    """Return BCW's 27-dimensional cubic homogeneous nilpotent map h."""
    if reduction is None:
        reduction = degree_reduction()
    n = len(reduction.variables)
    X = reduction.variables
    Y = list(sp.symbols("Y1:" + str(n + 1)))
    T = sp.Symbol("T")
    variables = X + Y + [T]
    h = [
        sp.expand(Y[j] * T**2 + reduction.quadratic_part[j] * T)
        for j in range(n)
    ]
    h += [sp.expand(-reduction.cubic_part[j]) for j in range(n)]
    h += [sp.Integer(0)]
    return variables, h


def quartic_potential(reduction: Reduction | None = None, expand=False):
    """Return variables and P=i*sum h_j(A+iB)B_j in 54 variables."""
    if reduction is None:
        reduction = degree_reduction()
    h_variables, h = cubic_homogeneous_map(reduction)
    r = len(h_variables)
    A = list(sp.symbols("A1:" + str(r + 1)))
    B = list(sp.symbols("B1:" + str(r + 1)))
    substitutions = {
        h_variables[j]: A[j] + I * B[j]
        for j in range(r)
    }
    potential = I * sum(h[j].subs(substitutions) * B[j] for j in range(r))
    if expand:
        potential = sp.expand(potential)
    return A + B, potential


def cubic_collision_points(reduction: Reduction | None = None):
    """Return three explicit collision points for W -> W+h(W)."""
    if reduction is None:
        reduction = degree_reduction()
    points = []
    X = reduction.variables
    for point in reduction.collision_points:
        substitutions = dict(zip(X, point))
        H3 = tuple(sp.expand(f.subs(substitutions)) for f in reduction.cubic_part)
        points.append(tuple(point) + H3 + (sp.Integer(1),))
    return points


def symmetric_collision_points(reduction: Reduction | None = None, count=2):
    """Lift cubic collisions to the 54-dimensional gradient map.

    If B(X)=X+h(X), the conjugated gradient map has second block
    (I+Jh(X)^T)y-i*h(X).  We take y=0 over the last base point and
    solve for the other y's so that all second blocks agree.  This gives
    substantially smaller rational coordinates than forcing that block to 0.
    """
    if reduction is None:
        reduction = degree_reduction()
    h_variables, h = cubic_homogeneous_map(reduction)
    points = cubic_collision_points(reduction)[:count]
    Jh = sp.Matrix(h).jacobian(h_variables)
    point_data = []
    for point in points:
        substitutions = dict(zip(h_variables, point))
        h_value = sp.Matrix([f.subs(substitutions) for f in h])
        matrix = sp.eye(len(h_variables)) + Jh.subs(substitutions).T
        point_data.append((point, h_value, matrix))

    # At the anchor point y=0, so the common second-block value is -i*h.
    common_second_block = -I * point_data[-1][1]
    lifted = []
    for point, h_value, matrix in point_data:
        y = matrix.inv() * (common_second_block + I * h_value)
        # The original coordinates of the symmetric map are S(x,y)=(x-iy,y).
        a = sp.Matrix(point) - I * y
        lifted.append(tuple(a) + tuple(y))
    return lifted


def evaluate_map(mapping, variables, point):
    return _evaluate(mapping, variables, point)
