#!/usr/bin/env python3
"""Derive a candidate centered radical for the degree-three flag basis.

Exact row-centered symmetric arrays are sampled over the rationals.  The
resulting nullspace is used for discovery; the output explicitly remains
conjectural until a symbolic identity verifier is supplied.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
import math
from pathlib import Path
import random

from experiments.root_triangle_k7_overlap.search_root_triangle_degree3_psd import (
    LOCAL_EDGES,
    feature_vector,
    invariant_monomial_orbits,
)


def exact_rank_and_nullspace(rows):
    matrix = [[Q(value) for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_columns = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [
            value / pivot_value for value in matrix[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row]
                )
            ]
        pivot_columns.append(column)
        pivot_row += 1
    free_columns = [
        column
        for column in range(column_count)
        if column not in pivot_columns
    ]
    basis = []
    for free in free_columns:
        vector = [Q(0)] * column_count
        vector[free] = Q(1)
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -matrix[row][free]
        denominator = math.lcm(
            *(value.denominator for value in vector)
        )
        integers = [int(value * denominator) for value in vector]
        divisor = math.gcd(*integers)
        basis.append(tuple(value // divisor for value in integers))
    return len(pivot_columns), tuple(pivot_columns), tuple(basis)


def centered_array(seed, perturbations=500):
    random_generator = random.Random(seed)
    # H is ten times the scaled Gram off-diagonal: H=10*(4g).
    # The constant array H_ij=-1 has every off-diagonal row sum -40.
    matrix = [
        [-1 if row != column else 0 for column in range(41)]
        for row in range(41)
    ]
    for _ in range(perturbations):
        first, second, third, fourth = random_generator.sample(range(41), 4)
        value = random_generator.randint(-5, 5)
        updates = (
            (first, second, value),
            (third, fourth, value),
            (first, third, -value),
            (second, fourth, -value),
        )
        for row, column, increment in updates:
            matrix[row][column] += increment
            matrix[column][row] += increment
    if any(
        sum(matrix[row][column] for column in range(41) if column != row)
        != -40
        for row in range(41)
    ):
        raise RuntimeError("constructed array is not centered")
    return matrix, random_generator


def root_sum(matrix, root, orbits):
    residual = [vertex for vertex in range(41) if vertex not in root]
    result = [0] * len(orbits)
    for first, second in itertools.combinations(residual, 2):
        vertices = root + (first, second)
        values = tuple(
            matrix[vertices[row]][vertices[column]]
            for row, column in LOCAL_EDGES
        )
        local = feature_vector(values, orbits)
        result = [
            accumulated + value
            for accumulated, value in zip(result, local)
        ]
    return tuple(result)


def sample_rows(seeds, roots_per_array, orbits):
    rows = []
    for seed in seeds:
        matrix, random_generator = centered_array(seed)
        roots = [
            tuple(sorted(random_generator.sample(range(41), 3)))
            for _ in range(roots_per_array)
        ]
        rows.extend(root_sum(matrix, root, orbits) for root in roots)
    return tuple(rows)


def normalize_current_basis(raw_basis, degrees):
    result = []
    for vector in raw_basis:
        # The sampled variables are H=10*(4g).  A degree-d orbit is
        # therefore 10^d times the orbit in the quarter-grid basis.
        current = [
            value * 10**degree
            for value, degree in zip(vector, degrees)
        ]
        divisor = math.gcd(*current)
        result.append(tuple(value // divisor for value in current))
    return tuple(result)


def evaluate_current_kernel_on_h_row(vector, row, degrees):
    """Evaluate a quarter-grid kernel on an H=10q feature row exactly."""
    return sum(
        (
            Q(coefficient * entry, 10**degree)
            for coefficient, entry, degree in zip(vector, row, degrees)
        ),
        Q(0),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    orbits = invariant_monomial_orbits(3)
    degrees = tuple(sum(orbit[0]) for orbit in orbits)
    training_rows = sample_rows(
        tuple(20260724 + index for index in range(5)),
        15,
        orbits,
    )
    rank, complement, raw_basis = exact_rank_and_nullspace(training_rows)
    if rank != 22 or len(raw_basis) != 26:
        raise RuntimeError("unexpected centered radical dimension")
    basis = normalize_current_basis(raw_basis, degrees)

    holdout_rows = sample_rows((9102471, 9102472, 9102473), 10, orbits)
    # Convert the current-basis vectors back to the H-scaled basis for the
    # exact holdout evaluation.
    for vector in basis:
        for row in holdout_rows:
            value = evaluate_current_kernel_on_h_row(
                vector, row, degrees
            )
            if value != 0:
                raise RuntimeError("candidate radical failed exact holdout")

    payload = {
        "schema": "kissing5.centered_root_triangle_degree3_radical.v1",
        "status": (
            "EXACT-SAMPLE-CERTIFIED ONLY — UNIVERSALITY CONJECTURAL"
        ),
        "scope_warning": (
            "Exact rational sampling proves these vectors on the named "
            "arrays but does not by itself prove a universal polynomial "
            "identity. A symbolic verifier is still required."
        ),
        "target_cardinality": 41,
        "feature_dimension": 48,
        "radical_dimension": 26,
        "quotient_dimension": 22,
        "feature_degrees": list(degrees),
        "radical_vectors": [list(vector) for vector in basis],
        "quotient_coordinate_indices": list(complement),
        "training": {
            "seeds": [20260724 + index for index in range(5)],
            "roots_per_array": 15,
            "exact_rows": len(training_rows),
        },
        "holdout": {
            "seeds": [9102471, 9102472, 9102473],
            "roots_per_array": 10,
            "exact_rows": len(holdout_rows),
            "arithmetic": "fractions.Fraction; no binary-float division",
            "status": "PASS",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")
    print(args.output)
    print(hashlib.sha256(args.output.read_bytes()).hexdigest())
    print("rank", rank, "radical", len(basis))


if __name__ == "__main__":
    main()
