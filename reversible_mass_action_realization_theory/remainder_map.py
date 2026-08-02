#!/usr/bin/env python3
"""Exact fixed-support realization primitives.

The central object is the rational matrix obtained by reducing every unit-rate
reaction contribution modulo a prescribed ideal.  Its kernel is *exactly* the
space of rate vectors whose mass-action field vanishes on that ideal.

This module deliberately contains no numerical optimizer.  Discovery code may
propose supports or positive vectors, but the objects returned here use exact
SymPy arithmetic and are suitable for independent certificates.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import Iterable, Sequence

import sympy as sp


Complex = tuple[int, ...]
Pair = tuple[int, int]
DirectedEdge = tuple[int, int]
Monomial = tuple[int, ...]


@dataclass(frozen=True)
class RemainderMap:
    """Canonical sparse-coordinate representation of the remainder map."""

    matrix: sp.Matrix
    row_keys: tuple[tuple[int, Monomial], ...]
    directed_edges: tuple[DirectedEdge, ...]

    def annihilates(self, rates: Sequence[sp.Expr]) -> bool:
        if len(rates) != self.matrix.cols:
            raise ValueError("one rate is required for every directed edge")
        return self.matrix * sp.Matrix(tuple(map(sp.sympify, rates))) == sp.zeros(
            self.matrix.rows, 1
        )


def validate_support(
    complexes: Sequence[Sequence[int]], pairs: Sequence[Sequence[int]]
) -> tuple[tuple[Complex, ...], tuple[Pair, ...]]:
    """Validate and freeze a finite reversible support."""

    frozen_complexes = tuple(tuple(c) for c in complexes)
    if not frozen_complexes:
        raise ValueError("the support needs at least one complex")
    species = len(frozen_complexes[0])
    if species == 0:
        raise ValueError("complexes must have at least one coordinate")
    if any(len(c) != species for c in frozen_complexes):
        raise ValueError("all complexes must have the same dimension")
    if any(not isinstance(a, int) or isinstance(a, bool) or a < 0
           for c in frozen_complexes for a in c):
        raise ValueError("complex coordinates must be nonnegative integers")
    if len(set(frozen_complexes)) != len(frozen_complexes):
        raise ValueError("complexes must be distinct")

    frozen_pairs = tuple(tuple(edge) for edge in pairs)
    canonical = []
    for edge in frozen_pairs:
        if len(edge) != 2:
            raise ValueError("each reversible pair needs two endpoints")
        i, j = edge
        if not isinstance(i, int) or not isinstance(j, int):
            raise ValueError("complex indices must be integers")
        if not (0 <= i < len(frozen_complexes) and
                0 <= j < len(frozen_complexes)):
            raise ValueError("complex index outside the complex list")
        if i == j:
            raise ValueError("self-reactions are excluded")
        canonical.append(tuple(sorted((i, j))))
    if len(set(canonical)) != len(canonical):
        raise ValueError("a reversible pair was duplicated")
    return frozen_complexes, tuple((int(i), int(j)) for i, j in frozen_pairs)


def directed_edges(pairs: Sequence[Pair]) -> tuple[DirectedEdge, ...]:
    """Expand each stored pair as forward then reverse, fixing rate order."""

    return tuple(edge for i, j in pairs for edge in ((i, j), (j, i)))


def monomial(variables: Sequence[sp.Symbol], complex_: Complex) -> sp.Expr:
    return sp.prod(variable**exponent
                   for variable, exponent in zip(variables, complex_))


def mass_action_field(
    variables: Sequence[sp.Symbol],
    complexes: Sequence[Complex],
    pairs: Sequence[Pair],
    rates: Sequence[sp.Expr],
) -> tuple[sp.Expr, ...]:
    """Construct the mass-action vector field in the fixed directed order."""

    frozen_complexes, frozen_pairs = validate_support(complexes, pairs)
    variables = tuple(variables)
    if len(variables) != len(frozen_complexes[0]):
        raise ValueError("species variables and complex coordinates disagree")
    edges = directed_edges(frozen_pairs)
    if len(rates) != len(edges):
        raise ValueError("one rate is required for every directed edge")
    field = [sp.S.Zero] * len(variables)
    for rate, (source, target) in zip(map(sp.sympify, rates), edges):
        source_monomial = monomial(variables, frozen_complexes[source])
        displacement = tuple(
            frozen_complexes[target][i] - frozen_complexes[source][i]
            for i in range(len(variables))
        )
        for i, delta in enumerate(displacement):
            field[i] += rate * source_monomial * delta
    return tuple(sp.expand(coordinate) for coordinate in field)


def stoichiometric_matrix(
    complexes: Sequence[Complex], pairs: Sequence[Pair]
) -> sp.Matrix:
    """Return one displacement column per undirected pair."""

    frozen_complexes, frozen_pairs = validate_support(complexes, pairs)
    columns = [
        sp.Matrix(tuple(frozen_complexes[j][a] - frozen_complexes[i][a]
                        for a in range(len(frozen_complexes[0]))))
        for i, j in frozen_pairs
    ]
    return sp.Matrix.hstack(*columns) if columns else sp.zeros(
        len(frozen_complexes[0]), 0
    )


def is_connected(complexes: Sequence[Complex], pairs: Sequence[Pair]) -> bool:
    """Check that the undirected complex graph has one linkage class."""

    frozen_complexes, frozen_pairs = validate_support(complexes, pairs)
    adjacency = [set() for _ in frozen_complexes]
    for i, j in frozen_pairs:
        adjacency[i].add(j)
        adjacency[j].add(i)
    seen = {0}
    frontier = [0]
    while frontier:
        i = frontier.pop()
        for j in adjacency[i] - seen:
            seen.add(j)
            frontier.append(j)
    return len(seen) == len(frozen_complexes)


def _coefficient(
    expression: sp.Expr, variables: tuple[sp.Symbol, ...], exponent: Monomial
) -> sp.Expr:
    return sp.Poly(expression, *variables, domain=sp.QQ).coeff_monomial(exponent)


def build_remainder_map(
    variables: Sequence[sp.Symbol],
    complexes: Sequence[Complex],
    pairs: Sequence[Pair],
    ideal_generators: Iterable[sp.Expr],
    *,
    groebner_variables: Sequence[sp.Symbol] | None = None,
    order: str = "lex",
) -> RemainderMap:
    """Build the exact linear conic-preservation matrix.

    Rows are indexed deterministically by ``(field coordinate, monomial)``.
    A zero row is omitted.  If ``M`` is the returned matrix, linearity of
    normal-form reduction gives

        M k = 0  iff  every coordinate of F(k) lies in the ideal.
    """

    variables = tuple(variables)
    frozen_complexes, frozen_pairs = validate_support(complexes, pairs)
    if len(variables) != len(frozen_complexes[0]):
        raise ValueError("species variables and complex coordinates disagree")
    gb_variables = tuple(groebner_variables or variables)
    if set(gb_variables) != set(variables) or len(gb_variables) != len(variables):
        raise ValueError("Groebner variables must permute the species variables")
    basis = sp.groebner(
        tuple(map(sp.sympify, ideal_generators)), *gb_variables,
        order=order, domain=sp.QQ
    )
    edges = directed_edges(frozen_pairs)
    contributions: list[tuple[sp.Expr, ...]] = []
    for column in range(len(edges)):
        unit = [0] * len(edges)
        unit[column] = 1
        field = mass_action_field(
            variables, frozen_complexes, frozen_pairs, unit
        )
        contributions.append(tuple(
            sp.expand(basis.reduce(coordinate)[1]) for coordinate in field
        ))

    monomials: set[Monomial] = set()
    for contribution in contributions:
        for coordinate in contribution:
            monomials.update(sp.Poly(
                coordinate, *variables, domain=sp.QQ
            ).monoms())
    ordered_monomials = tuple(sorted(
        monomials, key=lambda exponent: (sum(exponent), exponent)
    ))

    row_keys: list[tuple[int, Monomial]] = []
    rows: list[list[sp.Expr]] = []
    for coordinate in range(len(variables)):
        for exponent in ordered_monomials:
            row = [
                _coefficient(column[coordinate], variables, exponent)
                for column in contributions
            ]
            if any(entry != 0 for entry in row):
                row_keys.append((coordinate, exponent))
                rows.append(row)
    matrix = sp.Matrix(rows) if rows else sp.zeros(0, len(edges))
    return RemainderMap(matrix, tuple(row_keys), edges)


def verify_positive_kernel_point(
    remainder_map: RemainderMap, rates: Sequence[sp.Expr]
) -> None:
    """Raise unless ``rates`` is an exact strict-positive kernel witness."""

    rational_rates = tuple(sp.Rational(rate) for rate in rates)
    if not all(rate > 0 for rate in rational_rates):
        raise AssertionError("the proposed rate vector is not strictly positive")
    if not remainder_map.annihilates(rational_rates):
        raise AssertionError("the proposed rate vector is not in the kernel")


def coordinate_gcd(
    field: Sequence[sp.Expr], variables: Sequence[sp.Symbol]
) -> sp.Poly:
    """Return the monic gcd of nonzero coordinate polynomials over QQ."""

    polynomials = [sp.Poly(f, *variables, domain=sp.QQ) for f in field if f != 0]
    if not polynomials:
        raise ValueError("the zero vector field has no normalized gcd here")
    return reduce(sp.gcd, polynomials).monic()


__all__ = (
    "RemainderMap", "build_remainder_map", "coordinate_gcd",
    "directed_edges", "is_connected", "mass_action_field", "monomial",
    "stoichiometric_matrix", "validate_support",
    "verify_positive_kernel_point",
)
