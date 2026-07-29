#!/usr/bin/env python3
"""Analyze the exact common-zero equations of the effective quartic SOS.

Because every reduced Gram block in the certificate is positive definite,
the effective quartic vanishes precisely when all columns of every range
basis annihilate the corresponding quadratic-monomial vector.  This
script reconstructs those exact quadratic equations, factors them, and
finds maximum coordinate subspaces contained in their common zero set.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import importlib.util
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "verification"
    / "certificates"
    / "n3_boundary_effective_quartic_sos.json"
)
VERIFIER = (
    ROOT / "verification" / "verify_n3_boundary_flat_quartic_sos.py"
)
SPEC = importlib.util.spec_from_file_location("sos_verifier", VERIFIER)
sos_verifier = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(sos_verifier)

EFFECTIVE = ROOT / "discovery" / "build_n3_boundary_effective_quartic.py"
EFFECTIVE_SPEC = importlib.util.spec_from_file_location(
    "effective_quartic", EFFECTIVE
)
effective = importlib.util.module_from_spec(EFFECTIVE_SPEC)
assert EFFECTIVE_SPEC.loader is not None
EFFECTIVE_SPEC.loader.exec_module(effective)


def decode_matrix(data):
    return [
        [Fraction(numerator, denominator) for numerator, denominator in row]
        for row in data
    ]


def reconstruct():
    certificate = json.loads(CERTIFICATE.read_text())
    dimension = certificate["dimension"]
    terms = {}
    for indices, encoded in certificate["quartic_terms"]:
        exponent = tuple(indices.count(index) for index in range(dimension))
        terms[exponent] = Fraction(*encoded)

    parity_basis = sos_verifier.span_basis(
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
        by_character[
            sos_verifier.quotient(parity, parity_basis)
        ].append(number)
    blocks = list(by_character.values())
    bases = [
        decode_matrix(matrix) for matrix in certificate["bases"]
    ]
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
    return dimension, terms, monomials, equations


def factored_linear_forms(equations, dimension=55):
    """Return exact linear-factor pairs, or ``None``, for each equation."""

    variables = sp.symbols(f"x0:{dimension}", real=True)
    output = []
    for equation in equations:
        polynomial = sum(
            sp.Rational(coefficient.numerator, coefficient.denominator)
            * variables[first]
            * variables[second]
            for (first, second), coefficient in equation.items()
        )
        _, factors = sp.factor_list(polynomial)
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
            rows = []
            for factor in expanded:
                poly = sp.Poly(factor, variables)
                assert poly.coeff_monomial(1) == 0
                rows.append(
                    tuple(
                        Fraction(poly.coeff_monomial(variable))
                        for variable in variables
                    )
                )
            output.append(tuple(rows))
        else:
            output.append(None)
    return output


def maximum_coordinate_subspace(dimension, equations):
    """Maximum independent set in the graph of forbidden monomial pairs."""

    forbidden = [0 for _ in range(dimension)]
    excluded = 0
    for equation in equations:
        for first, second in equation:
            if first == second:
                excluded |= 1 << first
            else:
                forbidden[first] |= 1 << second
                forbidden[second] |= 1 << first
    allowed = ((1 << dimension) - 1) & ~excluded

    # Maximum independent set is maximum clique in the complement graph.
    complement = [0 for _ in range(dimension)]
    for vertex in range(dimension):
        complement[vertex] = allowed & ~(1 << vertex) & ~forbidden[vertex]

    best = 0
    population = lambda value: bin(value).count("1")

    def expand(clique, candidates):
        nonlocal best
        if population(clique) + population(candidates) <= population(best):
            return
        if not candidates:
            if population(clique) > population(best):
                best = clique
            return

        # Greedy coloring gives an upper bound for clique extension.
        order = []
        bounds = []
        remaining = candidates
        color = 0
        while remaining:
            color += 1
            available = remaining
            while available:
                vertex_bit = available & -available
                vertex = vertex_bit.bit_length() - 1
                order.append(vertex)
                bounds.append(color)
                remaining &= ~vertex_bit
                available &= ~vertex_bit & ~complement[vertex]

        for position in range(len(order) - 1, -1, -1):
            if population(clique) + bounds[position] <= population(best):
                return
            vertex = order[position]
            vertex_bit = 1 << vertex
            if candidates & vertex_bit:
                expand(
                    clique | vertex_bit,
                    candidates & complement[vertex],
                )
                candidates &= ~vertex_bit

    expand(0, allowed)
    return [
        index for index in range(dimension) if (best >> index) & 1
    ]


def evaluate_quadratic(equation, vector):
    return sum(
        coefficient * vector.get(first, 0) * vector.get(second, 0)
        for (first, second), coefficient in equation.items()
    )


def factorized_zero_tangent():
    """The 37-dimensional tangent to |a><b| tensor P_W at the base point."""

    boundary = effective.boundary
    kernel, _, _, _ = effective.build()
    label_to_coordinate = {
        label: index for index, label in enumerate(boundary.LABELS)
    }
    original_directions = []

    # a varies in the orthogonal complement of |00> on the first two sites.
    for first_two in itertools.product(range(3), repeat=2):
        if first_two == (0, 0):
            continue
        for phase in ("real", "imag"):
            original_directions.append(
                {
                    label_to_coordinate[
                        ("U", first_two + (logical,), logical, phase)
                    ]: Fraction(1)
                    for logical in range(2)
                }
            )

    # b varies in the orthogonal complement of |11>.
    for first_two in itertools.product(range(3), repeat=2):
        if first_two == (1, 1):
            continue
        for phase in ("real", "imag"):
            original_directions.append(
                {
                    label_to_coordinate[
                        ("V", first_two + (logical,), logical, phase)
                    ]: Fraction(1)
                    for logical in range(2)
                }
            )

    # The common two-plane W moves inside the third qutrit.
    for logical in range(2):
        for phase in ("real", "imag"):
            original_directions.append(
                {
                    label_to_coordinate[
                        ("U", (0, 0, 2), logical, phase)
                    ]: Fraction(1),
                    label_to_coordinate[
                        ("V", (1, 1, 2), logical, phase)
                    ]: Fraction(1),
                }
            )

    # The relative phase of |a><b|.
    original_directions.append(
        {
            label_to_coordinate[("logical", 0)]: Fraction(1),
            label_to_coordinate[("logical", 1)]: Fraction(1),
        }
    )
    assert len(original_directions) == 37

    hessian = boundary.hessian()
    components = boundary.connected_components(hessian)
    nonpivots = []
    for component in components:
        pivot = max(component, key=lambda index: hessian[index][index])
        nonpivots.extend(index for index in component if index != pivot)
    assert len(nonpivots) == len(kernel)

    kernel_directions = []
    for original in original_directions:
        coordinates = {
            variable: original.get(nonpivot, 0)
            for variable, nonpivot in enumerate(nonpivots)
            if original.get(nonpivot, 0)
        }
        reconstructed = defaultdict(Fraction)
        for variable, value in coordinates.items():
            for coordinate, coefficient in kernel[variable].items():
                reconstructed[coordinate] += value * coefficient
        assert {
            coordinate: value
            for coordinate, value in reconstructed.items()
            if value
        } == original
        kernel_directions.append(coordinates)
    return kernel_directions


def effective_zero_component_rows():
    """Exact RREF equations for the four maximal linear zero components."""

    def rows(data):
        return [
            {
                index: Fraction(coefficient)
                for index, coefficient in equation
            }
            for equation in data
        ]

    return [
        rows(
            [
                [(4, 1), (5, -1)],
                [(7, 1), (8, -1)],
                [(10, 1)], [(11, 1)], [(12, 1)], [(13, 1)],
                [(16, 1), (17, -1)],
                [(19, 1), (20, -1)],
                [(22, 1)], [(23, 1)], [(24, 1)], [(25, 1)],
                [(26, 1), (27, -1)],
                [(29, 1), (30, -1)],
                [(32, 1)], [(33, 1)], [(34, 1)], [(35, 1)],
            ]
        ),
        rows(
            [
                [(5, 1), (6, 1)],
                [(8, 1), (9, -1)],
                [(17, 1), (18, 1)],
                [(20, 1), (21, -1)],
                [(27, 1), (28, -1)],
                [(30, 1), (31, 1)],
                [(36, 1)], [(37, 1)], [(40, 1)], [(41, 1)],
                [(42, 1)], [(43, 1)], [(44, 1)], [(45, 1)],
                [(48, 1)], [(49, 1)], [(52, 1)], [(53, 1)],
            ]
        ),
        rows(
            [
                [(5, 1), (6, 1)],
                [(8, 1), (9, -1)],
                [(16, 1), (17, -1)],
                [(19, 1), (20, -1)],
                [(22, 1)], [(23, 1)], [(24, 1)], [(25, 1)],
                [(26, 1), (28, -1)],
                [(27, 1), (28, -1)],
                [(29, 1), (31, 1)],
                [(30, 1), (31, 1)],
                [(32, 1)], [(33, 1)], [(34, 1)], [(35, 1)],
                [(36, 1)], [(37, 1)], [(40, 1)], [(41, 1)],
                [(42, 1)], [(43, 1)], [(44, 1)], [(45, 1)],
                [(48, 1)], [(49, 1)], [(52, 1)], [(53, 1)],
            ]
        ),
        rows(
            [
                [(4, 1), (5, -1)],
                [(7, 1), (8, -1)],
                [(10, 1)], [(11, 1)], [(12, 1)], [(13, 1)],
                [(17, 1), (18, 1)],
                [(20, 1), (21, -1)],
                [(26, 1), (28, -1)],
                [(27, 1), (28, -1)],
                [(29, 1), (31, 1)],
                [(30, 1), (31, 1)],
                [(32, 1)], [(33, 1)], [(34, 1)], [(35, 1)],
                [(36, 1)], [(37, 1)], [(40, 1)], [(41, 1)],
                [(42, 1)], [(43, 1)], [(44, 1)], [(45, 1)],
                [(48, 1)], [(49, 1)], [(52, 1)], [(53, 1)],
            ]
        ),
    ]


def nullspace_directions(rows, dimension=55):
    matrix = sp.Matrix(
        [
            [row.get(index, 0) for index in range(dimension)]
            for row in rows
        ]
    )
    return [
        {
            index: Fraction(value)
            for index, value in enumerate(vector)
            if value
        }
        for vector in matrix.nullspace()
    ]


def verify_linear_zero_subspace(equations, directions):
    """Check a linear space lies in every homogeneous quadratic equation."""

    assert sp.Matrix(
        [
            [direction.get(index, 0) for direction in directions]
            for index in range(55)
        ]
    ).rank() == len(directions)
    for equation in equations:
        assert all(
            evaluate_quadratic(equation, direction) == 0
            for direction in directions
        )
        for first, second in itertools.combinations(directions, 2):
            total = defaultdict(Fraction)
            for index, value in first.items():
                total[index] += value
            for index, value in second.items():
                total[index] += value
            assert evaluate_quadratic(equation, total) == 0


def jacobian_rank(equations, point, dimension=55):
    rows = []
    for equation in equations:
        row = [Fraction(0) for _ in range(dimension)]
        for (first, second), coefficient in equation.items():
            if first == second:
                row[first] += 2 * coefficient * point.get(first, 0)
            else:
                row[first] += coefficient * point.get(second, 0)
                row[second] += coefficient * point.get(first, 0)
        rows.append(row)
    return sp.Matrix(rows).rank()


def main() -> None:
    dimension, _, monomials, equations = reconstruct()
    variables = sp.symbols(f"x0:{dimension}", real=True)
    factorizations = defaultdict(int)
    irreducible = []
    for equation in equations:
        polynomial = sum(
            sp.Rational(coefficient.numerator, coefficient.denominator)
            * variables[first]
            * variables[second]
            for (first, second), coefficient in equation.items()
        )
        factor = sp.factor(polynomial)
        if isinstance(factor, sp.Mul) and sum(
            sp.Poly(term, variables).total_degree()
            for term in factor.args
            if not term.is_number
        ) == 2:
            nonconstant = [
                term for term in factor.args if not term.is_number
            ]
            if (
                len(nonconstant) == 2
                and all(
                    sp.Poly(term, variables).total_degree() == 1
                    for term in nonconstant
                )
            ):
                factorizations["linear_times_linear"] += 1
                continue
        factorizations["irreducible_or_square"] += 1
        irreducible.append(factor)

    maximum = maximum_coordinate_subspace(dimension, equations)
    factorized = factorized_zero_tangent()
    verify_linear_zero_subspace(equations, factorized)
    generic_factorized_point = defaultdict(Fraction)
    for number, direction in enumerate(factorized):
        for index, value in direction.items():
            generic_factorized_point[index] += (number + 1) * value
    factorized_jacobian_rank = jacobian_rank(
        equations, generic_factorized_point, dimension
    )
    components = []
    for rows in effective_zero_component_rows():
        directions = nullspace_directions(rows, dimension)
        verify_linear_zero_subspace(equations, directions)
        generic_point = defaultdict(Fraction)
        for number, direction in enumerate(directions):
            for index, value in direction.items():
                generic_point[index] += (number + 1) * value
        components.append(
            (len(directions), jacobian_rank(equations, generic_point))
        )
    print("dimension", dimension)
    print("quadratic monomials", len(monomials))
    print("zero equations", len(equations))
    print("factor profile", dict(factorizations))
    print("maximum coordinate zero-subspace dimension", len(maximum))
    print("maximum coordinate zero-subspace", maximum)
    print(
        "verified factorized zero-manifold tangent dimension",
        len(factorized),
    )
    print(
        "Jacobian rank at deterministic factorized point",
        factorized_jacobian_rank,
        "(local variety dimension at most",
        dimension - factorized_jacobian_rank,
        ")",
    )
    print("verified maximal linear zero components (dimension, Jacobian rank)", components)
    print("first irreducible equations")
    for polynomial in irreducible[:20]:
        print(" ", polynomial)


if __name__ == "__main__":
    main()
