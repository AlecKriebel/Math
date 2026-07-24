#!/usr/bin/env python3
"""Exact verifier for the stratified common-pair/BV Farkas dual.

Only the Python standard library and exact ``Fraction`` arithmetic are used.
This file does not import the earlier cumulative-hierarchy verifier.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations_with_replacement, permutations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "certificates"
    / "common_pair_capacity_stratified_dual.json"
)
N = 41


def file_digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def transverse_q(k, u, v, t):
    if k == 0:
        return Q(1)
    w = t - u * v
    if k == 1:
        return w
    a = (1 - u * u) * (1 - v * v)
    q0, q1 = Q(1), w
    for degree in range(1, k):
        q0, q1 = (
            q1,
            (
                2 * (degree + 1) * w * q1
                - degree * a * q0
            )
            / (degree + 2),
        )
    return q1


def z_matrix(k, radial_degree, u, v, t):
    transverse = transverse_q(k, u, v, t)
    return [
        [
            transverse * u**row * v**column
            for column in range(radial_degree + 1)
        ]
        for row in range(radial_degree + 1)
    ]


def zero_matrix(size):
    return [[Q(0) for _ in range(size)] for _ in range(size)]


def add_scaled(target, source, scale=Q(1)):
    for row in range(len(target)):
        for column in range(len(target)):
            target[row][column] += scale * source[row][column]


def harmonic_affine_data(
    total_degree,
    harmonic_degree,
    nodes,
    ordered_counts,
    triples,
):
    """Return M(0) and the coefficient matrix of every triangle mass."""

    radial_degree = total_degree - harmonic_degree
    constant = zero_matrix(radial_degree + 1)
    add_scaled(
        constant,
        z_matrix(
            harmonic_degree,
            radial_degree,
            Q(1),
            Q(1),
            Q(1),
        ),
    )
    for node, count in zip(nodes, ordered_counts):
        weight = Q(count, N)
        for point in (
            (Q(1), node, node),
            (node, Q(1), node),
            (node, node, Q(1)),
        ):
            add_scaled(
                constant,
                z_matrix(
                    harmonic_degree,
                    radial_degree,
                    *point,
                ),
                weight,
            )

    coefficients = []
    for triple in triples:
        values = tuple(nodes[index] for index in triple)
        orbit = tuple(sorted(set(permutations(values))))
        matrix = zero_matrix(radial_degree + 1)
        for point in orbit:
            add_scaled(
                matrix,
                z_matrix(
                    harmonic_degree,
                    radial_degree,
                    *point,
                ),
                Q(6, N * len(orbit)),
            )
        coefficients.append(matrix)
    return constant, tuple(coefficients)


def quadratic_form(matrix, vector):
    return sum(
        vector[row] * matrix[row][column] * vector[column]
        for row in range(len(vector))
        for column in range(len(vector))
    )


def capacity(p):
    if p > 1:
        return 0
    if p > Q(3, 4):
        return 1
    if p > Q(2, 3):
        return 2
    if p > Q(5, 8):
        return 3
    if p > Q(1, 2):
        return 4
    if p == Q(1, 2):
        return 6
    return None


def verify(path=CERTIFICATE):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == (
        "common-pair-capacity-stratified-degree3-dual-v1"
    )
    assert data["dimension"] == 5
    assert data["cardinality"] == N

    source_record = data["source_pair_certificate"]
    source_path = ROOT / source_record["path"]
    assert file_digest(source_path) == source_record["sha256"]
    source = json.loads(source_path.read_text(encoding="utf-8"))
    assert source["dimension"] == 5 and source["size"] == N
    nodes = tuple(
        Q(atom["t_numerator"], atom["t_denominator"])
        for atom in source["atoms"]
    )
    ordered_counts = tuple(
        atom["ordered_count"] for atom in source["atoms"]
    )
    assert nodes == tuple(Q(value) for value in data["support"])
    assert ordered_counts == tuple(data["ordered_pair_counts"])
    assert sum(ordered_counts) == N * (N - 1)
    assert all(count % 2 == 0 for count in ordered_counts)

    triples = tuple(
        triple
        for triple in combinations_with_replacement(
            range(len(nodes)), 3
        )
        if (
            1
            + 2
            * nodes[triple[0]]
            * nodes[triple[1]]
            * nodes[triple[2]]
            - sum(nodes[index] ** 2 for index in triple)
        )
        >= 0
    )
    assert len(triples) == data["exact_diagnostics"][
        "feasible_triangle_type_count"
    ]

    incidence_rows = tuple(
        tuple(Q(triple.count(color)) for triple in triples)
        for color in range(len(nodes))
    )
    incidence_targets = tuple(
        Q((N - 2) * count, 2) for count in ordered_counts
    )

    capacity_rows = []
    capacity_uppers = []
    for stored in data["stratified_capacity_rows"]:
        color = stored["base_color"]
        base = nodes[color]
        high = Q(stored["high_threshold"])
        assert base == Q(stored["base_value"])
        p = 2 * high**2 / (1 + base)
        cap = capacity(p)
        assert p == Q(stored["p"])
        assert cap == stored["capacity"]
        upper = Q(cap * ordered_counts[color], 2)
        assert upper == stored["upper"]
        row = tuple(
            Q(
                sum(
                    triple[position] == color
                    and all(
                        nodes[triple[other]] >= high
                        for other in range(3)
                        if other != position
                    )
                    for position in range(3)
                )
            )
            for triple in triples
        )
        capacity_rows.append(row)
        capacity_uppers.append(upper)

    bv_constants = []
    bv_rows = []
    for stored in data["bv_scalar_directions"]:
        total_degree = stored["total_degree"]
        harmonic_degree = stored["harmonic_degree"]
        vector = tuple(Q(value) for value in stored["direction"])
        assert len(vector) == total_degree - harmonic_degree + 1
        constant_matrix, coefficient_matrices = harmonic_affine_data(
            total_degree,
            harmonic_degree,
            nodes,
            ordered_counts,
            triples,
        )
        scalar_constant = quadratic_form(constant_matrix, vector)
        scalar_row = tuple(
            quadratic_form(matrix, vector)
            for matrix in coefficient_matrices
        )
        assert scalar_constant == Q(stored["constant"])
        bv_constants.append(scalar_constant)
        bv_rows.append(scalar_row)

    multipliers = data["farkas_multipliers"]
    incidence_multipliers = tuple(
        Q(value) for value in multipliers["incidence_equalities"]
    )
    capacity_multipliers = tuple(
        Q(value) for value in multipliers["capacity_upper_rows"]
    )
    bv_multipliers = tuple(
        Q(value) for value in multipliers["bv_nonnegative_rows"]
    )
    assert len(incidence_multipliers) == len(incidence_rows)
    assert len(capacity_multipliers) == len(capacity_rows)
    assert len(bv_multipliers) == len(bv_rows)
    assert all(value >= 0 for value in capacity_multipliers)
    assert all(value >= 0 for value in bv_multipliers)

    combined_coefficients = tuple(
        sum(
            multiplier * row[index]
            for multiplier, row in zip(
                incidence_multipliers, incidence_rows
            )
        )
        - sum(
            multiplier * row[index]
            for multiplier, row in zip(
                capacity_multipliers, capacity_rows
            )
        )
        + sum(
            multiplier * row[index]
            for multiplier, row in zip(bv_multipliers, bv_rows)
        )
        for index in range(len(triples))
    )
    right_hand_side = (
        sum(
            multiplier * target
            for multiplier, target in zip(
                incidence_multipliers, incidence_targets
            )
        )
        - sum(
            multiplier * upper
            for multiplier, upper in zip(
                capacity_multipliers, capacity_uppers
            )
        )
        - sum(
            multiplier * constant
            for multiplier, constant in zip(
                bv_multipliers, bv_constants
            )
        )
    )

    diagnostics = data["exact_diagnostics"]
    assert right_hand_side == Q(
        diagnostics["positive_right_hand_side"]
    )
    assert right_hand_side > 0
    assert max(combined_coefficients) == Q(
        diagnostics["largest_variable_coefficient"]
    )
    assert min(combined_coefficients) == Q(
        diagnostics["smallest_variable_coefficient"]
    )
    assert all(value < 0 for value in combined_coefficients)

    # If x_T >= 0 satisfied the five marginal equations, the two capacity
    # upper bounds, and the three BV scalar inequalities, the displayed
    # combination would give
    #
    #   sum_T combined_coefficients[T] x_T >= right_hand_side > 0.
    #
    # Its left side is <= 0 because every coefficient is strictly negative.
    return {
        "triangle_types": triples,
        "capacity_uppers": tuple(capacity_uppers),
        "bv_constants": tuple(bv_constants),
        "combined_coefficients": combined_coefficients,
        "right_hand_side": right_hand_side,
        "status": "PASS",
    }


if __name__ == "__main__":
    result = verify()
    print("stratified common-pair degree-three dual: PASS")
    print("feasible triangle types:", len(result["triangle_types"]))
    print("largest variable coefficient:", max(
        result["combined_coefficients"]
    ))
    print("positive right-hand side:", result["right_hand_side"])
