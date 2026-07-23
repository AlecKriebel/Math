#!/usr/bin/env python3
"""Exact verifier for the five-node, degree-three BV barrier.

The certificate is a triple pseudodistribution.  This verifier does not
trust the MILP search or floating-point eigenvalues: it uses only standard
library rational arithmetic.
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
    / "local_hybrid_degree3_triple_pseudodistribution.json"
)
N = 41


def load_triple_certificate():
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert data["schema"] == (
        "local-hybrid-degree3-triple-pseudodistribution-v1"
    )
    assert data["dimension"] == 5
    assert data["cardinality"] == N
    assert Q(data["maximum_inner_product"]) == Q(1, 2)
    nodes = tuple(Q(value) for value in data["nodes"])
    ordered_counts = tuple(data["ordered_pair_counts"])
    triples = tuple(
        (tuple(item["types"]), item["count"])
        for item in data["triple_counts"]
    )
    assert triples == tuple(sorted(triples))
    assert len({triple for triple, _ in triples}) == len(triples)
    assert all(
        tuple(sorted(triple)) == triple and count > 0
        for triple, count in triples
    )
    return nodes, ordered_counts, dict(triples)


def all_principal_minors(matrix):
    result = []
    for size in range(1, len(matrix) + 1):
        for indices in combinations(range(len(matrix)), size):
            minor = determinant(
                [[matrix[i][j] for j in indices] for i in indices]
            )
            result.append((minor, indices))
    return result


def mixed_center_count(triple, first_type, second_type):
    return triple.count(first_type) * triple.count(second_type)


def verify():
    nodes, ordered_counts, triple_counts = load_triple_certificate()
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

    gram_determinants = {}
    for triple in triple_counts:
        u, v, t = (nodes[index] for index in triple)
        value = 1 + 2 * u * v * t - u * u - v * v - t * t
        assert value > 0
        gram_determinants[triple] = value
    assert min(
        (value, triple) for triple, value in gram_determinants.items()
    ) == (Q(278991, 3125000), (2, 4, 4))

    # Check every event cell of the universal deep-wedge inequality.
    wedge_slacks = []
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
        wedge_slacks.append((wedges - lower, upper - wedges))

    deep_0_wedges = sum(
        center_count(triple, {0}) * count
        for triple, count in triple_counts.items()
    )
    deep_01_wedges = sum(
        center_count(triple, {0, 1}) * count
        for triple, count in triple_counts.items()
    )
    mixed_01_wedges = sum(
        mixed_center_count(triple, 0, 1) * count
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
    # The type-0 degrees can be 3^5,4^25,5^11.  A three-edge type-1
    # star on four of the degree-five vertices attains both coupling caps.
    assert 5 * 3 + 25 * 4 + 11 * 5 == ordered_counts[0]
    assert 5 * 3 + 25 * 6 + 11 * 10 == deep_0_wedges
    assert mixed_01_wedges == 5 * (3 + 1 + 1 + 1)
    assert type_1_wedges == 3

    # All total-degree-three BV blocks are positive definite.  Every
    # principal minor is checked exactly.
    minimum_minors = {}
    for harmonic_degree in range(4):
        matrix = harmonic_matrix(
            3,
            harmonic_degree,
            nodes,
            ordered_counts,
            triple_counts,
        )
        minors = all_principal_minors(matrix)
        assert all(value > 0 for value, _ in minors)
        minimum_minors[harmonic_degree] = min(minors)
    assert minimum_minors == {
        0: (
            Q(84333109360856935209633, 1050625000000000000000000),
            (1, 3),
        ),
        1: (
            Q(
                3449723259474261817946435877,
                42025000000000000000000000000,
            ),
            (1, 2),
        ),
        2: (
            Q(
                31248817301127972207531453743,
                378225000000000000000000000000,
            ),
            (0, 1),
        ),
        3: (
            Q(106047122208949126237, 20500000000000000000),
            (0,),
        ),
    }

    # C047: every PSD Gram matrix of rank at most five obeys
    # 20 D^2 <= 9 V^3 for its centered first three spectral moments.
    pair_square_moment = sum(
        Q(count, N) * node**2
        for count, node in zip(ordered_counts, nodes)
    )
    triple_cycle_moment = sum(
        Q(6 * count, N) * nodes[i] * nodes[j] * nodes[k]
        for (i, j, k), count in triple_counts.items()
    )
    p1 = Q(N)
    p2 = p1 * (1 + pair_square_moment)
    p3 = p1 * (1 + 3 * pair_square_moment + triple_cycle_moment)
    spectral_variance = p2 - p1**2 / 5
    centered_third = (
        p3 - p1**3 / 25 - 3 * p1 * spectral_variance / 5
    )
    rank_five_violation = (
        20 * centered_third**2 - 9 * spectral_variance**3
    )
    assert pair_square_moment == Q(5933759, 820000)
    assert triple_cycle_moment == Q(942439107537, 20500000000)
    assert spectral_variance == Q(29759, 20000)
    assert centered_third == Q(11249247537, 500000000)
    assert rank_five_violation == Q(
        252349919611050160863, 25000000000000000
    ) > 0

    # Unlike the rank-aware reassignment, this one passes the basic
    # common-colored-graph degree covariance condition.  Triple counts
    # determine the second moments of the five color-degree columns.
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
    color_minors = []
    for size_minor in range(1, len(nodes) + 1):
        for indices in combinations(range(len(nodes)), size_minor):
            color_minors.append(
                (
                    determinant(
                        [
                            [color_covariance[i][j] for j in indices]
                            for i in indices
                        ]
                    ),
                    indices,
                )
            )
    assert all(value >= 0 for value, _ in color_minors)
    assert [
        item for item in color_minors if item[0] == 0
    ] == [(Q(0), (0, 1, 2, 3, 4))]
    assert min(
        item for item in color_minors if item[0] > 0
    ) == (Q(456, 41), (1,))

    # Scope boundary: the next total degree fails.  The k=3 block in the
    # radial direction p(u)=u has a negative diagonal entry.
    degree_4_k3 = harmonic_matrix(
        4, 3, nodes, ordered_counts, triple_counts
    )
    first_degree_4_failure = degree_4_k3[1][1]
    assert first_degree_4_failure == Q(
        -65176795992375100476726763,
        20500000000000000000000000,
    )

    return {
        "triple_type_count": len(triple_counts),
        "minimum_3_by_3_determinant": min(gram_determinants.values()),
        "incidences": incidences,
        "deep_0_wedges": deep_0_wedges,
        "deep_01_wedges": deep_01_wedges,
        "mixed_01_wedges": mixed_01_wedges,
        "type_1_wedges": type_1_wedges,
        "minimum_wedge_slack": min(
            min(lower, upper) for lower, upper in wedge_slacks
        ),
        "degree_3_minimum_principal_minors": minimum_minors,
        "pair_square_moment": pair_square_moment,
        "triple_cycle_moment": triple_cycle_moment,
        "rank_five_spectral_variance": spectral_variance,
        "rank_five_centered_third": centered_third,
        "rank_five_violation": rank_five_violation,
        "color_covariance_minimum_positive_minor": Q(456, 41),
        "first_degree_4_failure": first_degree_4_failure,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
