#!/usr/bin/env python3
"""Exact verifier for the degree-three BV plus rank-cut barrier.

Only standard-library rational arithmetic is used.  The artifact is a
triple pseudodistribution, not a common graph or Gram matrix.
"""

from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path

try:
    from verifiers.verify_fixed41_bv_degree5 import determinant
    from verifiers.verify_local_hybrid_barrier import (
        common_center_bound,
        integer_wedge_minimum,
        load_certificate as load_pair_certificate,
        threshold_test_points,
    )
    from verifiers.verify_weighted_residual_barrier import (
        center_count,
        harmonic_matrix,
    )
except ModuleNotFoundError:  # Direct execution from the repository root.
    from verify_fixed41_bv_degree5 import determinant
    from verify_local_hybrid_barrier import (
        common_center_bound,
        integer_wedge_minimum,
        load_certificate as load_pair_certificate,
        threshold_test_points,
    )
    from verify_weighted_residual_barrier import (
        center_count,
        harmonic_matrix,
    )


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "certificates"
    / "local_hybrid_degree3_rank_pseudodistribution.json"
)
N = 41


def load_certificate():
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert data["schema"] == (
        "local-hybrid-degree3-rank-pseudodistribution-v1"
    )
    assert data["dimension"] == 5
    assert data["cardinality"] == N
    assert Q(data["maximum_inner_product"]) == Q(1, 2)
    nodes = tuple(Q(value) for value in data["nodes"])
    ordered_counts = tuple(data["ordered_pair_counts"])
    items = tuple(
        (tuple(item["types"]), item["count"])
        for item in data["triple_counts"]
    )
    assert items == tuple(sorted(items))
    assert len({triple for triple, _ in items}) == len(items)
    assert all(
        tuple(sorted(triple)) == triple and count > 0
        for triple, count in items
    )
    return nodes, ordered_counts, dict(items)


def principal_minors(matrix):
    result = []
    for size in range(1, len(matrix) + 1):
        for indices in combinations(range(len(matrix)), size):
            value = determinant(
                [[matrix[i][j] for j in indices] for i in indices]
            )
            result.append((value, indices))
    return result


def verify():
    nodes, ordered_counts, triple_counts = load_certificate()
    size, pair_nodes, pair_counts, _, _ = load_pair_certificate()
    assert size == N
    assert nodes == pair_nodes
    assert ordered_counts == pair_counts
    unordered_counts = tuple(count // 2 for count in ordered_counts)

    assert sum(triple_counts.values()) == N * (N - 1) * (N - 2) // 6
    incidences = tuple(
        sum(
            count * triple.count(edge_type)
            for triple, count in triple_counts.items()
        )
        for edge_type in range(len(nodes))
    )
    assert incidences == (3315, 117, 5109, 12714, 10725)
    assert incidences == tuple(
        (N - 2) * count for count in unordered_counts
    )

    determinants = {}
    for triple in triple_counts:
        u, v, t = (nodes[index] for index in triple)
        value = 1 + 2 * u * v * t - u * u - v * v - t * t
        assert value > 0
        determinants[triple] = value
    assert min(
        (value, triple) for triple, value in determinants.items()
    ) == (Q(278991, 3125000), (2, 4, 4))

    # All continuous deep-threshold event cells.
    event_slacks = []
    for q in threshold_test_points(nodes):
        deep_types = {
            index
            for index, node in enumerate(nodes)
            if node < 0 and node * node >= q
        }
        high_types = {
            index
            for index, node in enumerate(nodes)
            if node >= 2 * q - 1
        }
        deep_degree = sum(
            ordered_counts[index] for index in deep_types
        )
        high_edges = sum(
            unordered_counts[index] for index in high_types
        )
        wedges = sum(
            center_count(triple, deep_types) * count
            for triple, count in triple_counts.items()
        )
        lower = integer_wedge_minimum(deep_degree, N)
        upper = common_center_bound(q) * high_edges
        assert lower <= wedges <= upper
        event_slacks.append((wedges - lower, upper - wedges))

    deep_0_wedges = sum(
        center_count(triple, {0}) * count
        for triple, count in triple_counts.items()
    )
    deep_01_wedges = sum(
        center_count(triple, {0, 1}) * count
        for triple, count in triple_counts.items()
    )
    mixed_01_wedges = sum(
        triple.count(0) * triple.count(1) * count
        for triple, count in triple_counts.items()
    )
    type_1_wedges = sum(
        center_count(triple, {1}) * count
        for triple, count in triple_counts.items()
    )
    assert (
        deep_0_wedges,
        deep_01_wedges,
        mixed_01_wedges,
        type_1_wedges,
    ) == (275, 308, 30, 3)
    assert mixed_01_wedges <= 5 * ordered_counts[1]
    assert type_1_wedges <= 3
    assert 5 * 3 + 25 * 4 + 11 * 5 == ordered_counts[0]
    assert 5 * 3 + 25 * 6 + 11 * 10 == deep_0_wedges

    minimum_minors = {}
    for harmonic_degree in range(4):
        matrix = harmonic_matrix(
            3,
            harmonic_degree,
            nodes,
            ordered_counts,
            triple_counts,
        )
        minors = principal_minors(matrix)
        assert all(value > 0 for value, _ in minors)
        minimum_minors[harmonic_degree] = min(minors)
    assert minimum_minors == {
        0: (
            Q(
                258743294447584132869903,
                4202500000000000000000000,
            ),
            (1, 3),
        ),
        1: (
            Q(
                43298054454337461453155341,
                2101250000000000000000000000,
            ),
            (1, 2),
        ),
        2: (
            Q(
                2044735394554621266331271839,
                18911250000000000000000000000,
            ),
            (0, 1),
        ),
        3: (
            Q(44961384503977585143, 10250000000000000000),
            (0,),
        ),
    }

    # Exact C047 rank-five spectral-moment audit.
    pair_square_moment = sum(
        Q(count, N) * node**2
        for count, node in zip(ordered_counts, nodes)
    )
    triple_cycle_moment = sum(
        Q(6 * count, N) * nodes[i] * nodes[j] * nodes[k]
        for (i, j, k), count in triple_counts.items()
    )
    delta = pair_square_moment - Q(36, 5)
    rank_center = Q(1116, 25) + Q(108, 5) * delta
    fixed_rank_residual = triple_cycle_moment - rank_center
    p1 = Q(N)
    spectral_variance = p1 * delta
    centered_third = p1 * fixed_rank_residual
    rank_five_residual = (
        20 * centered_third**2 - 9 * spectral_variance**3
    )
    assert pair_square_moment == Q(5933759, 820000)
    assert triple_cycle_moment == Q(46569451803, 1025000000)
    assert delta == Q(29759, 820000)
    assert fixed_rank_residual == Q(9958803, 1025000000)
    assert abs(fixed_rank_residual) < Q(1, 100)
    assert spectral_variance == Q(29759, 20000)
    assert centered_third == Q(9958803, 25000000)
    assert rank_five_residual == Q(
        -26475139223868987, 1000000000000000
    ) < 0

    # Basic common-edge-colored-graph consistency fails.  If d_q(v) are
    # the five color degrees, the triple counts determine their second
    # moment matrix.  Its centered version must be PSD for any common graph.
    color_wedges = [
        [Q(0) for _ in range(len(nodes))] for _ in range(len(nodes))
    ]
    for triple, count in triple_counts.items():
        for first in range(len(nodes)):
            multiplicity = triple.count(first)
            color_wedges[first][first] += (
                Q(multiplicity * (multiplicity - 1), 2) * count
            )
            for second in range(first + 1, len(nodes)):
                value = (
                    multiplicity * triple.count(second) * count
                )
                color_wedges[first][second] += value
                color_wedges[second][first] += value
    color_second_moment = [
        [
            (
                Q(ordered_counts[first])
                + 2 * color_wedges[first][first]
                if first == second
                else color_wedges[first][second]
            )
            for second in range(len(nodes))
        ]
        for first in range(len(nodes))
    ]
    color_covariance = [
        [
            color_second_moment[first][second]
            - Q(
                ordered_counts[first] * ordered_counts[second], N
            )
            for second in range(len(nodes))
        ]
        for first in range(len(nodes))
    ]
    color_direction = (Q(2), Q(-1), Q(0), Q(0), Q(1))
    color_variance_violation = sum(
        color_direction[i]
        * color_covariance[i][j]
        * color_direction[j]
        for i in range(len(nodes))
        for j in range(len(nodes))
    )
    assert color_variance_violation == Q(-570, 41)
    color_minors = principal_minors(color_covariance)
    assert min(color_minors) == (Q(-19857375, 41), (0, 1, 2, 3))

    # A simple exact next-degree separator.
    degree_4_k3 = harmonic_matrix(
        4, 3, nodes, ordered_counts, triple_counts
    )
    degree_4_failure = degree_4_k3[1][1]
    assert degree_4_failure == Q(
        -34232597256626759823593857,
        10250000000000000000000000,
    )

    return {
        "triple_type_count": len(triple_counts),
        "minimum_3_by_3_determinant": min(determinants.values()),
        "incidences": incidences,
        "deep_0_wedges": deep_0_wedges,
        "deep_01_wedges": deep_01_wedges,
        "mixed_01_wedges": mixed_01_wedges,
        "type_1_wedges": type_1_wedges,
        "minimum_event_slack": min(
            min(lower, upper) for lower, upper in event_slacks
        ),
        "degree_3_minimum_principal_minors": minimum_minors,
        "pair_square_moment": pair_square_moment,
        "triple_cycle_moment": triple_cycle_moment,
        "fixed_rank_residual": fixed_rank_residual,
        "rank_five_residual": rank_five_residual,
        "color_variance_violation": color_variance_violation,
        "degree_4_failure": degree_4_failure,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
