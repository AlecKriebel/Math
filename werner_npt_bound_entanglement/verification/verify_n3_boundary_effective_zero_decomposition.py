#!/usr/bin/env python3
"""Verify the exact four-component effective-quartic zero decomposition.

The certificate is a finite rational branching proof.  This verifier:

1. reconstructs the 300 quadratic zero equations from the positive
   effective-quartic Gram certificate;
2. checks 278 ambient product factorizations and independently
   enumerates their 64 maximal independent-set branches;
3. checks every rational split in the 486-node branch DAG;
4. checks every leaf annihilates all 300 quadrics and lies in one of
   four stated linear components; and
5. checks every stated component itself annihilates all 300 quadrics.

Only the Python standard library is used.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import json
from pathlib import Path

from verify_n3_boundary_flat_quartic_sos import span_basis, quotient


ROOT = Path(__file__).resolve().parent
GRAM_CERTIFICATE = (
    ROOT / "certificates" / "n3_boundary_effective_quartic_sos.json"
)
DECOMPOSITION_CERTIFICATE = (
    ROOT
    / "certificates"
    / "n3_boundary_effective_zero_decomposition.json"
)


def decode_dense_matrix(data):
    return [
        [Fraction(numerator, denominator) for numerator, denominator in row]
        for row in data
    ]


def decode_row(data, dimension):
    row = [Fraction(0) for _ in range(dimension)]
    for index, (numerator, denominator) in data:
        assert row[index] == 0
        row[index] = Fraction(numerator, denominator)
    return tuple(row)


def reconstruct_zero_equations():
    certificate = json.loads(GRAM_CERTIFICATE.read_text())
    assert certificate["format"] == "n3-flat-kernel-effective-rational-face-v1"
    dimension = certificate["dimension"]
    terms = {}
    for indices, encoded in certificate["quartic_terms"]:
        exponent = tuple(indices.count(index) for index in range(dimension))
        terms[exponent] = Fraction(*encoded)

    parity_basis = span_basis(
        [
            sum(
                1 << index
                for index, power in enumerate(exponent)
                if power & 1
            )
            for exponent in terms
        ]
    )
    active = {
        index
        for index in range(dimension)
        if terms.get(
            tuple(4 if other == index else 0 for other in range(dimension)),
            0,
        )
    }
    monomials = [(index, index) for index in active]
    for first, second in itertools.combinations(range(dimension), 2):
        exponent = tuple(
            2 if index in (first, second) else 0
            for index in range(dimension)
        )
        if terms.get(exponent, 0) or first in active and second in active:
            monomials.append((first, second))
    monomials.sort()

    by_character = defaultdict(list)
    for number, (first, second) in enumerate(monomials):
        parity = 0 if first == second else (1 << first) ^ (1 << second)
        by_character[quotient(parity, parity_basis)].append(number)
    blocks = list(by_character.values())
    bases = [
        decode_dense_matrix(matrix) for matrix in certificate["bases"]
    ]
    assert len(blocks) == len(bases)

    equations = []
    for block, basis in zip(blocks, bases):
        rank = len(basis[0])
        for column in range(rank):
            equation = {
                monomials[global_index]: basis[row][column]
                for row, global_index in enumerate(block)
                if basis[row][column]
            }
            assert equation
            equations.append(equation)
    assert len(equations) == 300
    return dimension, equations


def rref(rows, dimension):
    work = [list(row) for row in rows if any(row)]
    pivot_row = 0
    for column in range(dimension):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    work[row], work[pivot_row]
                )
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    work = [tuple(row) for row in work if any(row)]
    work.sort(key=lambda row: next(index for index, value in enumerate(row) if value))
    return tuple(work)


def nullspace(rows, dimension):
    reduced = rref(rows, dimension)
    pivot_columns = [
        next(index for index, value in enumerate(row) if value)
        for row in reduced
    ]
    pivot_set = set(pivot_columns)
    basis = []
    for free in range(dimension):
        if free in pivot_set:
            continue
        vector = [Fraction(0) for _ in range(dimension)]
        vector[free] = 1
        for row, pivot in zip(reduced, pivot_columns):
            vector[pivot] = -row[free]
        basis.append(tuple(vector))
    return basis


def restrict_quadratic(equation, basis):
    row_support = [
        [
            (column, basis[column][row])
            for column in range(len(basis))
            if basis[column][row]
        ]
        for row in range(len(basis[0]))
    ] if basis else []
    output = defaultdict(Fraction)
    for (first, second), coefficient in equation.items():
        for first_column, first_value in row_support[first]:
            for second_column, second_value in row_support[second]:
                monomial = tuple(sorted((first_column, second_column)))
                output[monomial] += (
                    coefficient * first_value * second_value
                )
    return {
        monomial: coefficient
        for monomial, coefficient in output.items()
        if coefficient
    }


def restricted_linear(row, basis):
    return [
        sum(x * y for x, y in zip(row, vector))
        for vector in basis
    ]


def product_polynomial(first, second):
    output = defaultdict(Fraction)
    for first_index, first_value in enumerate(first):
        if not first_value:
            continue
        for second_index, second_value in enumerate(second):
            if not second_value:
                continue
            output[tuple(sorted((first_index, second_index)))] += (
                first_value * second_value
            )
    return {
        monomial: coefficient
        for monomial, coefficient in output.items()
        if coefficient
    }


def proportional(first, second):
    assert first and second
    assert set(first) == set(second)
    monomial = next(iter(first))
    scale = first[monomial] / second[monomial]
    assert scale
    assert all(first[key] == scale * second[key] for key in first)


def normalize(row):
    pivot = next(value for value in row if value)
    return tuple(value / pivot for value in row)


def maximal_independent_sets(forms, edges):
    dimension = len(forms)
    adjacency = [0 for _ in range(dimension)]
    allowed = (1 << dimension) - 1
    for first, second in edges:
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

    def search(clique, candidates, excluded):
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
            search(
                clique | vertex_bit,
                candidates & complement[vertex],
                excluded & complement[vertex],
            )
            candidates &= ~vertex_bit
            excluded |= vertex_bit
            choices &= ~vertex_bit

    search(0, allowed, 0)
    return output


def main():
    dimension, equations = reconstruct_zero_equations()
    certificate = json.loads(DECOMPOSITION_CERTIFICATE.read_text())
    assert certificate["format"] == "n3-boundary-effective-zero-decomposition-v1"
    assert certificate["dimension"] == dimension == 55

    # Verify every advertised ambient factorization directly.
    forms = set()
    edges_as_rows = []
    factored_equations = set()
    for equation_index, first_data, second_data in certificate[
        "ambient_factorizations"
    ]:
        assert equation_index not in factored_equations
        factored_equations.add(equation_index)
        first = decode_row(first_data, dimension)
        second = decode_row(second_data, dimension)
        product = product_polynomial(first, second)
        proportional(equations[equation_index], product)
        first = normalize(first)
        second = normalize(second)
        forms.add(first)
        forms.add(second)
        edges_as_rows.append((first, second))
    assert len(factored_equations) == 278
    forms = sorted(forms)
    assert len(forms) == 36
    form_index = {row: index for index, row in enumerate(forms)}
    edges = [
        (form_index[first], form_index[second])
        for first, second in edges_as_rows
    ]
    independent_sets = maximal_independent_sets(forms, edges)
    assert len(independent_sets) == 64

    nodes = certificate["nodes"]
    decoded_nodes = []
    row_to_node = {}
    for number, node in enumerate(nodes):
        rows = tuple(
            decode_row(row, dimension) for row in node["rows"]
        )
        assert rref(rows, dimension) == rows
        assert rows not in row_to_node
        row_to_node[rows] = number
        decoded_nodes.append((rows, node))

    expected_initial_rows = {
        rref(
            [
                form
                for index, form in enumerate(forms)
                if not ((branch >> index) & 1)
            ],
            dimension,
        )
        for branch in independent_sets
    }
    initial_nodes = set(certificate["initial_nodes"])
    assert {
        decoded_nodes[number][0] for number in initial_nodes
    } == expected_initial_rows

    components = [
        tuple(decode_row(row, dimension) for row in component)
        for component in certificate["components"]
    ]
    assert sorted(dimension - len(component) for component in components) == [
        27,
        27,
        37,
        37,
    ]
    for component in components:
        assert rref(component, dimension) == component
        basis = nullspace(component, dimension)
        assert all(
            not restrict_quadratic(equation, basis)
            for equation in equations
        )

    reachable = set()
    stack = list(initial_nodes)
    leaf_count = 0
    while stack:
        number = stack.pop()
        if number in reachable:
            continue
        reachable.add(number)
        rows, node = decoded_nodes[number]
        basis = nullspace(rows, dimension)
        if node["kind"] == "split":
            equation = equations[node["equation"]]
            restricted = restrict_quadratic(equation, basis)
            factors = [
                decode_row(row, dimension) for row in node["factors"]
            ]
            assert len(factors) == 2
            product = product_polynomial(
                restricted_linear(factors[0], basis),
                restricted_linear(factors[1], basis),
            )
            proportional(restricted, product)
            children = node["children"]
            assert len(children) == 2
            for child, factor in zip(children, factors):
                expected = rref(rows + (factor,), dimension)
                assert decoded_nodes[child][0] == expected
                stack.append(child)
        else:
            assert node["kind"] == "leaf"
            leaf_count += 1
            assert all(
                not restrict_quadratic(equation, basis)
                for equation in equations
            )
            assert any(
                rref(component + rows, dimension) == rows
                for component in components
            )
    assert reachable == set(range(len(nodes)))
    assert leaf_count == 148
    assert len(nodes) == 486
    print(
        "verified exact effective-quartic zero decomposition:",
        len(equations),
        "quadrics,",
        len(factored_equations),
        "ambient factorizations,",
        len(independent_sets),
        "initial branches,",
        len(nodes),
        "branch nodes,",
        leaf_count,
        "linear leaves, and component dimensions",
        sorted(dimension - len(component) for component in components),
    )


if __name__ == "__main__":
    main()
