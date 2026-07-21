#!/usr/bin/env python3
"""Rank-compressed BCW homogenization of the certified 13-variable model."""

from __future__ import annotations

import sympy as sp

from stable_reduction import degree_reduction


def cubic_component_factorization(reduction=None):
    """Return H3=B*K with K a minimal independent list of components."""
    if reduction is None:
        reduction = degree_reduction()
    variables = reduction.variables
    cubic = reduction.cubic_part
    monomials = sorted(
        set().union(*[set(sp.Poly(component, *variables).monoms()) for component in cubic])
    )
    coefficient_matrix = sp.Matrix(
        [
            [sp.Poly(component, *variables).coeff_monomial(monomial) for monomial in monomials]
            for component in cubic
        ]
    )
    independent_indices = tuple(coefficient_matrix.T.rref()[1])
    basis_matrix = coefficient_matrix[list(independent_indices), :]
    basis_components = [cubic[index] for index in independent_indices]

    injection_rows = []
    for row in coefficient_matrix.tolist():
        # Solve coefficients*cubic_basis = component, transposed as a column system.
        coefficients = basis_matrix.T.gauss_jordan_solve(sp.Matrix(row))[0]
        injection_rows.append(list(coefficients))
    injection = sp.Matrix(injection_rows)
    assert injection * sp.Matrix(basis_components) == sp.Matrix(cubic)
    return injection, basis_components, independent_indices


def compressed_cubic_map(reduction=None):
    """Return a 22-variable cubic homogeneous map h with nilpotent Jacobian."""
    if reduction is None:
        reduction = degree_reduction()
    injection, cubic_basis, _ = cubic_component_factorization(reduction)
    x_variables = reduction.variables
    rank = len(cubic_basis)
    y_variables = list(sp.symbols("U1:" + str(rank + 1)))
    t = sp.Symbol("T")
    variables = x_variables + y_variables + [t]
    y_vector = sp.Matrix(y_variables)
    first_block = [
        sp.expand(t * reduction.quadratic_part[index] + t**2 * (injection * y_vector)[index])
        for index in range(len(x_variables))
    ]
    second_block = [sp.expand(-component) for component in cubic_basis]
    mapping = first_block + second_block + [sp.Integer(0)]
    return variables, mapping, injection, cubic_basis


def lift_stable_point(point):
    """Lift a source point of the announced map through the six stable gadgets."""
    x, y, z = map(sp.Rational, point)
    g1a = -x**2
    g1b = -(x * z + 3 * y)
    g2a = -3 * x**2 * y
    g2b = -(2 * z + x * y * z + 3 * y**2)
    g3a = -x * y
    g3b = -(g2a * z + 3 * x * g2b)
    g4a = -x * y**2
    g4b = -(7 * y + 3 * x * z + 3 * x * y**2 + x**2 * y * z)
    g5a = -(g4a * x * y)
    g6b = -(g4a * g1b - y * g4b)
    return (
        x, y, z, g1a, g1b, g2a, g2b, g3a, g3b,
        g4a, g4b, g5a, g6b,
    )


def compressed_collision_points(reduction=None):
    if reduction is None:
        reduction = degree_reduction()
    _, cubic_basis, _ = cubic_component_factorization(reduction)
    result = []
    for point in reduction.collision_points:
        substitutions = dict(zip(reduction.variables, point))
        y_value = tuple(sp.factor(component.subs(substitutions)) for component in cubic_basis)
        result.append(tuple(point) + y_value + (sp.Integer(1),))
    return result


if __name__ == "__main__":
    reduction = degree_reduction()
    variables, mapping, injection, cubic_basis = compressed_cubic_map(reduction)
    print("variables:", len(variables))
    print("cubic rank:", len(cubic_basis))
    print("basis component indices:", cubic_component_factorization(reduction)[2])
    print("injection rank:", injection.rank())
    print("degrees:", sorted(set(sp.Poly(f, *variables).total_degree() for f in mapping if f)))
