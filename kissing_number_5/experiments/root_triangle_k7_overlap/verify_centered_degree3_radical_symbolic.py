#!/usr/bin/env python3
"""Symbolically verify the centered root-triangle degree-three radical.

For a fixed root triple, each flag coordinate is summed over all unordered
pairs of the other 38 vertices.  The certificate vectors are claimed to
give the zero polynomial on the affine space

    4 + sum_{j != i} q_ij = 0,  i=0,...,40.

This verifier parametrizes that affine space exactly.  Forty-one edge
variables are eliminated using disjoint odd cycles (twelve triangles and
one 5-cycle).  Every remaining polynomial calculation uses integers after
a common denominator of eight is cleared.  Thus an empty reduced sparse
polynomial is an exact ideal-membership check, not an evaluation test.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path
import sys
import time

from experiments.root_triangle_k7_overlap.search_root_triangle_degree3_psd import (
    LOCAL_EDGES,
    invariant_monomial_orbits,
)


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "centered_degree3_radical.json"
CERTIFICATE_SHA256 = (
    "322c9f4399a4059e118875a67568090fc7455434abc708720b2d808b07360280"
)
VERTEX_COUNT = 41
ROOT = (0, 1, 2)
RESIDUAL = tuple(range(3, VERTEX_COUNT))
EDGES = tuple(itertools.combinations(range(VERTEX_COUNT), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pivot_components():
    triangles = [
        (0, 3, 4),
        (1, 5, 6),
        (2, 7, 8),
    ]
    triangles.extend(
        tuple(range(first, first + 3))
        for first in range(9, 36, 3)
    )
    cycle = (36, 37, 38, 39, 40)
    return tuple(triangles) + (cycle,)


def component_edges(component):
    if len(component) == 3:
        return tuple(itertools.combinations(component, 2))
    require(len(component) == 5, "unexpected pivot component")
    return tuple(
        tuple(sorted((component[index], component[(index + 1) % 5])))
        for index in range(5)
    )


def invert(matrix):
    size = len(matrix)
    augmented = [
        [Q(value) for value in row]
        + [Q(int(row_index == column)) for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if augmented[row][column] != 0
            ),
            None,
        )
        require(pivot is not None, "singular pivot incidence matrix")
        augmented[column], augmented[pivot] = (
            augmented[pivot],
            augmented[column],
        )
        pivot_value = augmented[column][column]
        augmented[column] = [
            value / pivot_value for value in augmented[column]
        ]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            if scale == 0:
                continue
            augmented[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    augmented[row], augmented[column]
                )
            ]
    return tuple(
        tuple(row[size + column] for column in range(size))
        for row in augmented
    )


def edge_linear_numerators():
    """Return q_edge as an integer linear numerator divided by two.

    A linear numerator maps ``None`` to its constant and a free edge index
    to its coefficient.
    """
    components = pivot_components()
    covered = tuple(vertex for component in components for vertex in component)
    require(
        tuple(sorted(covered)) == tuple(range(VERTEX_COUNT)),
        "pivot components do not partition the vertices",
    )
    pivot_edges = tuple(
        edge
        for component in components
        for edge in component_edges(component)
    )
    require(len(pivot_edges) == VERTEX_COUNT, "wrong pivot edge count")
    require(len(set(pivot_edges)) == len(pivot_edges), "duplicate pivot edge")
    pivot_set = set(pivot_edges)
    free_edges = tuple(edge for edge in EDGES if edge not in pivot_set)
    require(
        len(free_edges) == len(EDGES) - VERTEX_COUNT,
        "wrong free dimension",
    )
    free_index = {edge: EDGE_INDEX[edge] for edge in free_edges}
    expressions = {
        edge: {free_index[edge]: 2}
        for edge in free_edges
    }

    for component in components:
        pivots = component_edges(component)
        incidence = [
            [
                int(vertex in edge)
                for edge in pivots
            ]
            for vertex in component
        ]
        inverse = invert(incidence)
        for pivot_index, pivot_edge in enumerate(pivots):
            numerator = {}
            for row_index, vertex in enumerate(component):
                twice_coefficient = 2 * inverse[pivot_index][row_index]
                require(
                    twice_coefficient.denominator == 1,
                    "pivot inverse is not half-integral",
                )
                coefficient = int(twice_coefficient)
                numerator[None] = numerator.get(None, 0) - 4 * coefficient
                for neighbor in range(VERTEX_COUNT):
                    if neighbor == vertex:
                        continue
                    edge = tuple(sorted((vertex, neighbor)))
                    if edge in pivot_set:
                        continue
                    variable = free_index[edge]
                    numerator[variable] = (
                        numerator.get(variable, 0) - coefficient
                    )
            expressions[pivot_edge] = {
                variable: coefficient
                for variable, coefficient in numerator.items()
                if coefficient
            }

    require(len(expressions) == len(EDGES), "missing edge expression")
    # Independently check all 41 row sums at the linear-polynomial level.
    for vertex in range(VERTEX_COUNT):
        row = {None: 8}
        for neighbor in range(VERTEX_COUNT):
            if neighbor == vertex:
                continue
            edge = tuple(sorted((vertex, neighbor)))
            for variable, coefficient in expressions[edge].items():
                row[variable] = row.get(variable, 0) + coefficient
        require(
            all(coefficient == 0 for coefficient in row.values()),
            f"parametrization does not center row {vertex}",
        )
    return expressions, pivot_set, free_edges


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = (
                result.get(monomial, 0)
                + left_coefficient * right_coefficient
            )
    return {
        monomial: coefficient
        for monomial, coefficient in result.items()
        if coefficient
    }


def linear_polynomial(numerator):
    return {
        (() if variable is None else (variable,)): coefficient
        for variable, coefficient in numerator.items()
    }


def monomial_reduction(
    actual_edges,
    exponent,
    expressions,
    power_cache,
):
    result = {(): 1}
    for edge, power in zip(actual_edges, exponent):
        if power == 0:
            continue
        key = (edge, power)
        factor = power_cache.get(key)
        if factor is None:
            factor = {(): 1}
            linear = linear_polynomial(expressions[edge])
            for _ in range(power):
                factor = multiply(factor, linear)
            power_cache[key] = factor
        result = multiply(result, factor)
    return result


def local_polynomial(vector, orbits):
    """Return monomial coefficients after clearing the common denominator."""
    result = {}
    for coefficient, orbit in zip(vector, orbits):
        if coefficient == 0:
            continue
        degree = sum(orbit[0])
        scale = coefficient * 2 ** (3 - degree)
        for exponent in orbit:
            result[exponent] = result.get(exponent, 0) + scale
    return {
        exponent: coefficient
        for exponent, coefficient in result.items()
        if coefficient
    }


def verify_vector(vector, orbits, expressions):
    local = local_polynomial(vector, orbits)
    aggregate = {}
    power_cache = {}
    for first, second in itertools.combinations(RESIDUAL, 2):
        vertices = ROOT + (first, second)
        actual_edges = tuple(
            tuple(sorted((vertices[row], vertices[column])))
            for row, column in LOCAL_EDGES
        )
        for exponent, coefficient in local.items():
            reduced = monomial_reduction(
                actual_edges,
                exponent,
                expressions,
                power_cache,
            )
            for monomial, reduced_coefficient in reduced.items():
                aggregate[monomial] = (
                    aggregate.get(monomial, 0)
                    + coefficient * reduced_coefficient
                )
        aggregate = {
            monomial: coefficient
            for monomial, coefficient in aggregate.items()
            if coefficient
        }
    require(not aggregate, "radical vector is not a polynomial identity")
    return len(local), len(power_cache)


def verify(path=CERTIFICATE):
    require(sha256(path) == CERTIFICATE_SHA256, "certificate hash mismatch")
    payload = json.loads(path.read_text())
    require(payload["feature_dimension"] == 48, "wrong feature dimension")
    require(payload["radical_dimension"] == 26, "wrong radical dimension")
    require(
        payload["status"]
        == "EXACT-SAMPLE-CERTIFIED ONLY — UNIVERSALITY CONJECTURAL",
        "input artifact overstates its certification status",
    )
    orbits = invariant_monomial_orbits(3)
    require(len(orbits) == 48, "unexpected invariant basis")
    expressions, pivot_set, free_edges = edge_linear_numerators()
    started = time.time()
    vector_reports = []
    for index, vector in enumerate(payload["radical_vectors"]):
        require(len(vector) == len(orbits), "wrong radical vector width")
        local_terms, cached_powers = verify_vector(
            tuple(map(int, vector)),
            orbits,
            expressions,
        )
        vector_reports.append(
            {
                "index": index,
                "local_monomials": local_terms,
                "cached_edge_powers": cached_powers,
            }
        )
        print(
            f"verified {index + 1}/{len(payload['radical_vectors'])}",
            file=sys.stderr,
            flush=True,
        )
    return {
        "status": "PASS",
        "arithmetic": "exact integers after clearing denominator 8",
        "vertices": VERTEX_COUNT,
        "root": list(ROOT),
        "extension_pairs": len(tuple(itertools.combinations(RESIDUAL, 2))),
        "centering_equations": VERTEX_COUNT,
        "pivot_edges": len(pivot_set),
        "free_variables": len(free_edges),
        "radical_vectors_verified": len(vector_reports),
        "elapsed_seconds": time.time() - started,
        "vectors": vector_reports,
    }


def main():
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else CERTIFICATE
    require(len(sys.argv) <= 2, "usage: verifier [certificate.json]")
    print(json.dumps(verify(path), indent=2))


if __name__ == "__main__":
    main()
