#!/usr/bin/env python3
"""Exact verifier for the C039--C047 convex-mixture separator."""

from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

try:
    from verifiers.verify_fixed41_bv_degree5 import (
        add_scaled,
        unique_permutations,
        zero_matrix,
        z_matrix,
    )
except ModuleNotFoundError:
    from verify_fixed41_bv_degree5 import (
        add_scaled,
        unique_permutations,
        zero_matrix,
        z_matrix,
    )


ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "certificates" / "fixed41_rank_mixture_separator.json"
N = 41


def parse_measure_a(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    grid = tuple(Q(value) for value in data["grid"])
    alpha = tuple(Q(value) for value in data["alpha"])
    triples = tuple(tuple(item) for item in data["triples"])
    nu = tuple(Q(value) for value in data["nu"])
    return hashlib.sha256(raw).hexdigest(), grid, alpha, triples, nu


def parse_measure_b(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    grid = tuple(Q(value) for value in data["nodes"])
    alpha = tuple(Q(count, N) for count in data["ordered_pair_counts"])
    triples = tuple(
        tuple(item["types"]) for item in data["triple_counts"]
    )
    # Each stored count is an unordered vertex-triple count, so 6/N is its
    # mass in the fixed-center ordered triple normalization.
    nu = tuple(
        Q(6 * item["count"], N) for item in data["triple_counts"]
    )
    return hashlib.sha256(raw).hexdigest(), grid, alpha, triples, nu


def harmonic_matrix(total_degree, harmonic_degree, measure):
    _sha, grid, alpha, triples, nu = measure
    radial_degree = total_degree - harmonic_degree
    matrix = zero_matrix(radial_degree + 1)
    add_scaled(
        matrix,
        z_matrix(
            harmonic_degree, radial_degree, Q(1), Q(1), Q(1)
        ),
    )
    for node, weight in zip(grid, alpha):
        add_scaled(
            matrix,
            z_matrix(
                harmonic_degree, radial_degree, Q(1), node, node
            ),
            weight,
        )
        add_scaled(
            matrix,
            z_matrix(
                harmonic_degree, radial_degree, node, Q(1), node
            ),
            weight,
        )
        add_scaled(
            matrix,
            z_matrix(
                harmonic_degree, radial_degree, node, node, Q(1)
            ),
            weight,
        )
    for triple, weight in zip(triples, nu):
        values = tuple(grid[index] for index in triple)
        orbit = unique_permutations(values)
        for u, v, t in orbit:
            add_scaled(
                matrix,
                z_matrix(
                    harmonic_degree, radial_degree, u, v, t
                ),
                weight / len(orbit),
            )
    return matrix


def quadratic(matrix, vector):
    return sum(
        vector[i] * matrix[i][j] * vector[j]
        for i in range(len(vector))
        for j in range(len(vector))
    )


def multiply_polynomials(first, second):
    result = [Q(0)] * (len(first) + len(second) - 1)
    for i, a in enumerate(first):
        for j, b in enumerate(second):
            result[i + j] += a * b
    return result


def moments(measure):
    _sha, grid, alpha, triples, nu = measure
    pair_square = sum(weight * node**2 for node, weight in zip(grid, alpha))
    triple_cycle = sum(
        weight
        * grid[triple[0]]
        * grid[triple[1]]
        * grid[triple[2]]
        for triple, weight in zip(triples, nu)
    )
    delta = pair_square - Q(36, 5)
    excess = triple_cycle - Q(1116, 25) - Q(108, 5) * delta
    return delta, excess


def verify():
    certificate = json.loads(CERT.read_text())
    assert certificate["schema"] == "fixed41-rank-mixture-separator-v1"
    assert certificate["dimension"] == 5
    assert certificate["cardinality"] == N

    source_a = ROOT / "certificates" / certificate["all_harmonic_source"]
    source_b = ROOT / "certificates" / certificate["rank_feasible_source"]
    measure_a = parse_measure_a(source_a)
    measure_b = parse_measure_b(source_b)
    assert measure_a[0] == certificate["all_harmonic_source_sha256"]
    assert measure_b[0] == certificate["rank_feasible_source_sha256"]

    for measure in (measure_a, measure_b):
        _sha, _grid, alpha, triples, nu = measure
        assert sum(alpha) == 40
        assert sum(nu) == 40 * 39
        for index in range(len(alpha)):
            marginal = sum(
                weight * triple.count(index) / 3
                for triple, weight in zip(triples, nu)
            )
            assert marginal == 39 * alpha[index]

    delta_a, excess_a = moments(measure_a)
    delta_b, excess_b = moments(measure_b)
    assert delta_a == Q(7796592200083, 800000000000000)
    assert excess_a == Q(416587466342759, 16000000000000000)
    assert 20 * excess_a**2 - 369 * delta_a**3 > 0
    assert delta_b == Q(29759, 820000)
    assert excess_b == Q(9958803, 1025000000)
    assert 20 * excess_b**2 - 369 * delta_b**3 < 0

    theta = Q(certificate["rank_feasible_example_theta"])
    delta = (1 - theta) * delta_a + theta * delta_b
    excess = (1 - theta) * excess_a + theta * excess_b
    rank_residual = 20 * excess**2 - 369 * delta**3
    expected_rank = certificate["rank_feasible_example"]
    assert delta == Q(expected_rank["delta"])
    assert excess == Q(expected_rank["E"])
    assert rank_residual == Q(expected_rank["rank_residual"]) < 0

    active_a = measure_a[1][1:]
    assert set(active_a).isdisjoint(measure_b[1])
    polynomial = [Q(1)]
    for root in active_a:
        polynomial = multiply_polynomials(polynomial, [-root, Q(1)])
    separator = certificate["separator"]
    stored_polynomial = [
        Q(value)
        for value in separator["radial_polynomial_coefficients_ascending"]
    ]
    assert polynomial == stored_polynomial
    assert all(
        sum(coefficient * root**degree for degree, coefficient
            in enumerate(polynomial)) == 0
        for root in active_a
    )

    assert separator["harmonic_degree"] == 3
    assert separator["radial_degree"] == 6
    assert separator["total_degree"] == 9
    matrix_a = harmonic_matrix(9, 3, measure_a)
    matrix_b = harmonic_matrix(9, 3, measure_b)
    value_a = quadratic(matrix_a, polynomial)
    value_b = quadratic(matrix_b, polynomial)
    assert value_a == Q(separator["all_harmonic_endpoint_value"]) == 0
    assert value_b == Q(separator["rank_feasible_endpoint_value"]) < 0
    assert (1 - theta) * value_a + theta * value_b < 0

    return {
        "status": "PASS",
        "theta_example": str(theta),
        "theta_example_rank_residual": str(rank_residual),
        "separator_block": "harmonic 3, radial 6, total 9",
        "endpoint_A_separator_value": str(value_a),
        "endpoint_B_separator_value": str(value_b),
        "conclusion": "theta=0 fails C047; every theta>0 fails H_(3,9)",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
