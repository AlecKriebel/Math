#!/usr/bin/env python3
"""Generate exact all-harmonic tail data for the repaired witness.

The resulting JSON is checked independently by
``verifiers/verify_fixed41_bv_all_harmonics.py``.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

from verifiers import verify_fixed41_bv_all_harmonics as base


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source", type=Path, default=here / "candidate_exact.json"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=here / "all_harmonics_certificate.json",
    )
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    source = json.loads(source_bytes)
    grid = [Q(value) for value in source["grid"]]
    alpha = [Q(value) for value in source["alpha"]]
    triples = [tuple(item) for item in source["triples"]]
    nu = [Q(value) for value in source["nu"]]
    active_grid = grid[1:]
    active_index = {value: index for index, value in enumerate(active_grid)}

    coefficient_matrices: dict[
        tuple[Q, Q], list[list[Q]]
    ] = {}
    ordered_terms = []
    for triple, weight in zip(triples, nu, strict=True):
        values = tuple(grid[index] for index in triple)
        orbit = sorted(set(itertools.permutations(values)))
        coefficient = weight / len(orbit)
        for u, v, t in orbit:
            if u not in active_index or v not in active_index:
                continue
            i, j = active_index[u], active_index[v]
            area = (1 - u * u) * (1 - v * v)
            displacement = t - u * v
            delta = area - displacement * displacement
            key = (area, displacement)
            matrix = coefficient_matrices.setdefault(
                key, base.zero_matrix(6)
            )
            matrix[i][j] += coefficient
            ordered_terms.append(
                (i, j, coefficient, area, displacement, delta)
            )

    limits = [base.zero_matrix(6), base.zero_matrix(6)]
    tail_bounds = [base.zero_matrix(6), base.zero_matrix(6)]
    for i, q in enumerate(active_grid):
        radial_factor = 1 - q * q
        limits[0][i][i] += alpha[i + 1]
        limits[1][i][i] += alpha[i + 1] * radial_factor
    for i, j, coefficient, area, displacement, delta in ordered_terms:
        if delta == 0:
            limits[0][i][j] += coefficient
            limits[1][i][j] += coefficient * displacement
        else:
            tail_bounds[0][i][j] += (
                coefficient * base.ceil_sqrt_fraction(area / delta)
            )
            tail_bounds[1][i][j] += (
                coefficient
                * base.ceil_sqrt_fraction(area * area / delta)
            )

    limit_pivots = {}
    inverse_norms = {}
    eigenvalue_bounds = {}
    tail_rows = {}
    tail_constants = {}
    for parity, name in enumerate(("even", "odd")):
        pivots = base.ldl_pivots(limits[parity])
        if not all(value > 0 for value in pivots):
            raise ValueError(f"{name} limit is not positive definite")
        inverse = base.inverse(limits[parity])
        inverse_norm = max(sum(abs(value) for value in row) for row in inverse)
        row_sums = [sum(row) for row in tail_bounds[parity]]
        tail_constant = max(
            sum(abs(inverse[i][h]) * row_sums[h] for h in range(6))
            for i in range(6)
        )
        limit_pivots[name] = [str(value) for value in pivots]
        inverse_norms[name] = str(inverse_norm)
        eigenvalue_bounds[name] = str(1 / inverse_norm)
        tail_rows[name] = [str(value) for value in row_sums]
        tail_constants[name] = str(tail_constant)

    finite_through = 599
    analytic_tail_from = finite_through + 1
    if Q(tail_constants["even"]) >= analytic_tail_from:
        raise ValueError("even analytic tail threshold is insufficient")
    if Q(tail_constants["odd"]) >= analytic_tail_from:
        raise ValueError(
            "odd analytic tail threshold is insufficient: "
            + tail_constants["odd"]
        )
    sequences = {
        key: base.normalized_transverse_sequences(
            *key, finite_through // 2
        )
        for key in coefficient_matrices
    }
    minimum_pivot = None
    for degree in range(1, finite_through + 1):
        parity = degree % 2
        matrix = base.zero_matrix(6)
        for i, q in enumerate(active_grid):
            matrix[i][i] = alpha[i + 1]
            if parity:
                matrix[i][i] *= 1 - q * q
        for key, coefficient_matrix in coefficient_matrices.items():
            kernel = sequences[key][parity][degree // 2]
            for i in range(6):
                for j in range(6):
                    matrix[i][j] += coefficient_matrix[i][j] * kernel
        for index, pivot in enumerate(base.ldl_pivots(matrix)):
            if pivot <= 0:
                raise ValueError(f"nonpositive pivot at degree {degree}")
            candidate = (pivot, degree, index)
            if minimum_pivot is None or candidate[0] < minimum_pivot[0]:
                minimum_pivot = candidate
    assert minimum_pivot is not None

    pair_through = 129
    pair_sequences = [
        base.gegenbauer_5_sequence(q, pair_through) for q in grid
    ]
    pair_values = []
    for degree in range(1, pair_through + 1):
        pair_values.append(
            (
                1
                + sum(
                    alpha[index] * pair_sequences[index][degree]
                    for index in range(len(grid))
                ),
                degree,
            )
        )
    minimum_pair = min(pair_values)
    if minimum_pair[0] <= 0:
        raise ValueError("nonpositive finite pair moment")

    old_tail = json.loads(
        (
            Path(__file__).resolve().parents[2]
            / "certificates"
            / "fixed41_bv_all_harmonics_certificate.json"
        ).read_text()
    )
    inverse_bounds = [
        Q(value)
        for value in old_tail["pair_interior_inverse_three_halves_bounds"]
    ]
    weighted_pair_bound = sum(
        alpha[i + 1] * inverse_bounds[i] for i in range(len(active_grid))
    )
    endpoint_margin = 1 - alpha[0]
    if endpoint_margin <= 0:
        raise ValueError("nonpositive antipodal endpoint margin")
    normalized_pair_tail = Q(31, 5) * weighted_pair_bound / endpoint_margin
    pair_tail_from = pair_through + 1
    if normalized_pair_tail**2 >= pair_tail_from**3:
        raise ValueError(
            "pair analytic tail threshold is insufficient: "
            + str(normalized_pair_tail)
        )

    certificate = {
        "schema": "fixed41-bv-all-harmonics-v1",
        "source_certificate": args.source.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "finite_check_through": finite_through,
        "analytic_tail_from": analytic_tail_from,
        "limit_ldl_pivots": limit_pivots,
        "limit_inverse_infinity_norm": inverse_norms,
        "limit_eigenvalue_lower_bound": eigenvalue_bounds,
        "interior_tail_row_sums": tail_rows,
        "tail_constants": tail_constants,
        "minimum_finite_ldl_pivot": {
            "value": str(minimum_pivot[0]),
            "harmonic_degree": minimum_pivot[1],
            "pivot_index": minimum_pivot[2],
        },
        "pair_moment_finite_check_through": pair_through,
        "minimum_finite_pair_moment": {
            "value": str(minimum_pair[0]),
            "degree": minimum_pair[1],
        },
        "pair_interior_inverse_three_halves_bounds": [
            str(value) for value in inverse_bounds
        ],
        "pair_weighted_tail_bound": str(weighted_pair_bound),
        "pair_endpoint_margin": str(endpoint_margin),
        "normalized_pair_tail_constant": str(normalized_pair_tail),
        "pair_analytic_tail_from": pair_tail_from,
    }
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")


if __name__ == "__main__":
    main()
