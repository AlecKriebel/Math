#!/usr/bin/env python3
"""Exact branch decomposition of the effective-quartic zero ideal.

The 300 SOS-zero quadrics consist of 278 products of rational linear
forms and 22 quadrics which are irreducible in the ambient coordinates.
The product equations first reduce the real zero set to 64 coordinate
branches.  On each branch this script recursively factors any surviving
quadratic equation and splits on its two linear factors.

If every leaf is linear, the output is an exact finite union of rational
linear subspaces.  Otherwise it prints a strictly smaller residual
quadratic ideal for each nonlinear leaf.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import importlib.util
import json
import os
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "analyze_n3_boundary_effective_zero_variety.py"
SPEC = importlib.util.spec_from_file_location("zero_analysis", SOURCE)
zero_analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(zero_analysis)

OUTPUT = os.environ.get("N3_ZERO_DECOMPOSITION_OUTPUT")


def normalize(row):
    pivot = next(value for value in row if value)
    row = tuple(value / pivot for value in row)
    return row


def canonical_rows(rows, dimension=55):
    if not rows:
        return ()
    reduced, _ = sp.Matrix(rows).rref()
    return tuple(
        tuple(Fraction(value) for value in row)
        for row in reduced.tolist()
        if any(row)
    )


def maximal_independent_sets(factor_pairs):
    forms = sorted(
        {
            normalize(row)
            for pair in factor_pairs
            if pair is not None
            for row in pair
        }
    )
    form_index = {row: index for index, row in enumerate(forms)}
    dimension = len(forms)
    adjacency = [0 for _ in range(dimension)]
    allowed = (1 << dimension) - 1
    for pair in factor_pairs:
        if pair is None:
            continue
        first, second = (
            form_index[normalize(row)] for row in pair
        )
        if first == second:
            allowed &= ~(1 << first)
        else:
            adjacency[first] |= 1 << second
            adjacency[second] |= 1 << first
    complement = [
        allowed & ~(1 << index) & ~adjacency[index]
        for index in range(dimension)
    ]
    population = lambda value: bin(value).count("1")
    output = []

    def bron_kerbosch(clique, candidates, excluded):
        if not candidates and not excluded:
            output.append(clique)
            return
        union = candidates | excluded
        if union:
            pivot = max(
                (
                    index
                    for index in range(dimension)
                    if (union >> index) & 1
                ),
                key=lambda index: population(
                    candidates & complement[index]
                ),
            )
            choices = candidates & ~complement[pivot]
        else:
            choices = candidates
        while choices:
            vertex_bit = choices & -choices
            vertex = vertex_bit.bit_length() - 1
            bron_kerbosch(
                clique | vertex_bit,
                candidates & complement[vertex],
                excluded & complement[vertex],
            )
            candidates &= ~vertex_bit
            excluded |= vertex_bit
            choices &= ~vertex_bit

    bron_kerbosch(0, allowed, 0)
    return forms, output


def nullspace(rows, dimension=55):
    matrix = (
        sp.Matrix(rows)
        if rows
        else sp.zeros(0, dimension)
    )
    return matrix.nullspace()


def basis_row_support(basis):
    return [
        [
            (column, Fraction(basis[column][row]))
            for column in range(len(basis))
            if basis[column][row]
        ]
        for row in range(55)
    ]


def restrict_equation(equation, row_support):
    output = {}
    for (first, second), coefficient in equation.items():
        for first_column, first_value in row_support[first]:
            for second_column, second_value in row_support[second]:
                monomial = tuple(sorted((first_column, second_column)))
                output[monomial] = (
                    output.get(monomial, Fraction(0))
                    + coefficient * first_value * second_value
                )
                if not output[monomial]:
                    del output[monomial]
    return output


def polynomial_expression(polynomial, variables):
    return sum(
        sp.Rational(coefficient.numerator, coefficient.denominator)
        * variables[first]
        * variables[second]
        for (first, second), coefficient in polynomial.items()
    )


def factor_pair(polynomial, variables):
    expression = polynomial_expression(polynomial, variables)
    _, factors = sp.factor_list(expression)
    expanded = [
        factor
        for factor, exponent in factors
        for _ in range(exponent)
    ]
    if (
        len(expanded) == 2
        and all(
            sp.Poly(factor, variables).total_degree() == 1
            for factor in expanded
        )
    ):
        return tuple(expanded)
    return None


def lift_linear_form(factor, variables, basis):
    polynomial = sp.Poly(factor, variables)
    logical = sp.Matrix(
        [
            polynomial.coeff_monomial(variable)
            for variable in variables
        ]
    )
    frame = sp.Matrix.hstack(*basis)
    lifted = frame * ((frame.T * frame).inv() * logical)
    assert (lifted.T * frame).T == logical
    return tuple(Fraction(value) for value in lifted)


def main():
    dimension, _, _, equations = zero_analysis.reconstruct()
    assert dimension == 55
    factor_pairs = zero_analysis.factored_linear_forms(
        equations, dimension
    )
    forms, independent_sets = maximal_independent_sets(factor_pairs)
    print(
        "ambient linear factors",
        len(forms),
        "maximal product branches",
        len(independent_sets),
        "branch sizes",
        dict(Counter(bin(branch).count("1") for branch in independent_sets)),
    )

    initial_states = []
    for branch in independent_sets:
        rows = [
            form
            for index, form in enumerate(forms)
            if not ((branch >> index) & 1)
        ]
        initial_states.append(canonical_rows(rows, dimension))

    memo = set()
    stack = list(dict.fromkeys(initial_states))
    linear_leaves = set()
    residual_leaves = {}
    node_data = {}
    visited_profile = Counter()
    while stack:
        rows = stack.pop()
        if rows in memo:
            continue
        memo.add(rows)
        basis = nullspace(rows, dimension)
        local_dimension = len(basis)
        variables = sp.symbols(f"y0:{local_dimension}", real=True)
        row_support = basis_row_support(basis)
        residual = []
        splitting_pair = None
        splitting_equation = None
        for number, equation in enumerate(equations):
            polynomial = restrict_equation(equation, row_support)
            if not polynomial:
                continue
            residual.append((number, polynomial))
            pair = factor_pair(polynomial, variables)
            if pair is not None and splitting_pair is None:
                splitting_pair = pair
                splitting_equation = number
        visited_profile[(local_dimension, len(residual))] += 1

        if not residual:
            linear_leaves.add(rows)
            node_data[rows] = {"kind": "leaf"}
            continue
        if splitting_pair is None:
            residual_leaves[rows] = residual
            node_data[rows] = {"kind": "residual"}
            continue

        children = []
        lifted_factors = []
        for factor in splitting_pair:
            lifted = lift_linear_form(factor, variables, basis)
            lifted_factors.append(lifted)
            children.append(canonical_rows(rows + (lifted,), dimension))
        node_data[rows] = {
            "kind": "split",
            "equation": splitting_equation,
            "factors": tuple(lifted_factors),
            "children": tuple(children),
        }
        stack.extend(set(children))

    # Remove linear leaves strictly contained in a larger linear leaf.
    maximal_linear = []
    for rows in sorted(linear_leaves, key=len):
        rowspace = sp.Matrix(rows)
        contained = False
        for larger in maximal_linear:
            larger_matrix = sp.Matrix(larger)
            if sp.Matrix.vstack(larger_matrix, rowspace).rank() == len(rows):
                # The current rowspace contains the larger rowspace, hence
                # its nullspace is contained in the larger leaf.
                contained = True
                break
        if not contained:
            maximal_linear.append(rows)

    print("visited states", len(memo), "profile", dict(visited_profile))
    print(
        "linear leaves",
        len(linear_leaves),
        "maximal linear leaves",
        len(maximal_linear),
        "dimensions",
        dict(Counter(dimension - len(rows) for rows in maximal_linear)),
    )
    print(
        "nonlinear residual leaves",
        len(residual_leaves),
        "profile",
        dict(
            Counter(
                (dimension - len(rows), len(residual))
                for rows, residual in residual_leaves.items()
            )
        ),
    )
    for number, rows in enumerate(maximal_linear):
        print(
            "LINEAR_COMPONENT",
            number,
            "dimension",
            dimension - len(rows),
        )
        for row in rows:
            print(
                " ",
                [
                    (index, str(value))
                    for index, value in enumerate(row)
                    if value
                ],
            )
    for number, (rows, residual) in enumerate(residual_leaves.items()):
        print(
            "RESIDUAL_COMPONENT",
            number,
            "ambient dimension",
            dimension - len(rows),
            "quadrics",
            len(residual),
        )
        print(
            " constraint rank",
            len(rows),
            "residual equation indices",
            [index for index, _ in residual],
        )

    if OUTPUT:
        assert not residual_leaves
        ordered_nodes = sorted(node_data)
        node_index = {
            rows: number for number, rows in enumerate(ordered_nodes)
        }

        def encode_fraction(value):
            value = Fraction(value)
            return [value.numerator, value.denominator]

        def encode_row(row):
            return [
                [index, encode_fraction(value)]
                for index, value in enumerate(row)
                if value
            ]

        ambient_factorizations = []
        for equation, pair in enumerate(factor_pairs):
            if pair is None:
                continue
            ambient_factorizations.append(
                [
                    equation,
                    encode_row(pair[0]),
                    encode_row(pair[1]),
                ]
            )
        certificate = {
            "format": "n3-boundary-effective-zero-decomposition-v1",
            "dimension": dimension,
            "ambient_factorizations": ambient_factorizations,
            "initial_nodes": sorted(
                node_index[rows] for rows in set(initial_states)
            ),
            "components": [
                [encode_row(row) for row in rows]
                for rows in maximal_linear
            ],
            "nodes": [],
        }
        for rows in ordered_nodes:
            data = node_data[rows]
            encoded = {
                "rows": [encode_row(row) for row in rows],
                "kind": data["kind"],
            }
            if data["kind"] == "split":
                encoded.update(
                    {
                        "equation": data["equation"],
                        "factors": [
                            encode_row(row) for row in data["factors"]
                        ],
                        "children": [
                            node_index[child] for child in data["children"]
                        ],
                    }
                )
            certificate["nodes"].append(encoded)
        Path(OUTPUT).write_text(
            json.dumps(certificate, separators=(",", ":"))
        )
        print(
            "certificate",
            OUTPUT,
            "bytes",
            Path(OUTPUT).stat().st_size,
        )


if __name__ == "__main__":
    main()
