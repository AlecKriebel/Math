#!/usr/bin/env python3
"""Exact verifier for the degree-3 BV + C047 + color-moment barrier."""

from fractions import Fraction as Q
from itertools import combinations
import json
from math import comb
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
    / "local_hybrid_degree3_rank_color_pseudodistribution.json"
)
N = 41


def load_certificate():
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert data["schema"] == (
        "local-hybrid-degree3-rank-color-pseudodistribution-v1"
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


def erdos_gallai(degrees):
    degrees = sorted(degrees, reverse=True)
    if sum(degrees) % 2:
        return False
    for size in range(1, len(degrees) + 1):
        left = sum(degrees[:size])
        right = size * (size - 1) + sum(
            min(degree, size) for degree in degrees[size:]
        )
        if left > right:
            return False
    return True


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

    gram_determinants = {}
    for triple in triple_counts:
        u, v, t = (nodes[index] for index in triple)
        value = 1 + 2 * u * v * t - u * u - v * v - t * t
        assert value > 0
        gram_determinants[triple] = value
    assert min(
        (value, triple) for triple, value in gram_determinants.items()
    ) == (Q(278991, 3125000), (2, 4, 4))

    # Build every same-color and mixed-color centered-wedge moment.
    color_wedges = [
        [0 for _ in range(len(nodes))] for _ in range(len(nodes))
    ]
    for triple, count in triple_counts.items():
        for first in range(len(nodes)):
            multiplicity = triple.count(first)
            color_wedges[first][first] += (
                multiplicity * (multiplicity - 1) // 2 * count
            )
            for second in range(first + 1, len(nodes)):
                value = multiplicity * triple.count(second) * count
                color_wedges[first][second] += value
                color_wedges[second][first] += value
    assert color_wedges == [
        [275, 30, 1011, 2782, 2257],
        [30, 3, 12, 108, 78],
        [1011, 12, 937, 3755, 3566],
        [2782, 108, 3755, 5087, 8609],
        [2257, 78, 3566, 8609, 3470],
    ]

    # All deep-threshold event cells and the sharper two-small-class caps.
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
        assert integer_wedge_minimum(deep_degree, N) <= wedges
        assert wedges <= common_center_bound(q) * high_edges
    assert color_wedges[0][0] == 275
    assert (
        color_wedges[0][0]
        + color_wedges[0][1]
        + color_wedges[1][1]
    ) == 308
    assert color_wedges[0][1] == 30 <= 5 * ordered_counts[1]
    assert color_wedges[1][1] == 3

    # All total-degree-three BV blocks.
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
                221539235618740811524443,
                2101250000000000000000000,
            ),
            (1, 3),
        ),
        1: (
            Q(
                621858663885311425191787767,
                21012500000000000000000000000,
            ),
            (1, 2),
        ),
        2: (
            Q(4214023039816497247, 12300000000000000000),
            (1,),
        ),
        3: (
            Q(19116262265659420051, 4100000000000000000),
            (0,),
        ),
    }

    # C047 holds strictly.
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
    spectral_variance = N * delta
    centered_third = N * fixed_rank_residual
    rank_five_residual = (
        20 * centered_third**2 - 9 * spectral_variance**3
    )
    assert pair_square_moment == Q(5933759, 820000)
    assert triple_cycle_moment == Q(931389435561, 20500000000)
    assert fixed_rank_residual == Q(199575561, 20500000000)
    assert rank_five_residual == Q(
        -661559877254042433, 25000000000000000
    ) < 0

    # The full centered color-degree covariance is PSD.
    color_second_moment = [
        [
            (
                Q(ordered_counts[first])
                + 2 * color_wedges[first][first]
                if first == second
                else Q(color_wedges[first][second])
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
    color_minors = principal_minors(color_covariance)
    assert all(value >= 0 for value, _ in color_minors)
    assert [
        item for item in color_minors if item[0] == 0
    ] == [(Q(0), (0, 1, 2, 3, 4))]
    assert min(
        item for item in color_minors if item[0] > 0
    ) == (Q(456, 41), (1,))

    # Basic individual-color degree and motif consistency.  Each listed
    # degree multiset is graphical by the exact Erdos--Gallai criterion and
    # reproduces the stored first two degree moments.
    degree_multiplicities = (
        {2: 1, 3: 2, 4: 28, 5: 10},
        {0: 37, 1: 3, 3: 1},
        {0: 8, 1: 1, 7: 1, 8: 25, 9: 6},
        {0: 1, 3: 1, 14: 1, 15: 1, 16: 9, 17: 28},
        {4: 1, 10: 1, 13: 10, 14: 29},
    )
    degree_sequences = []
    motif_counts = []
    for color, multiplicities in enumerate(degree_multiplicities):
        degrees = [
            degree
            for degree, multiplicity in multiplicities.items()
            for _ in range(multiplicity)
        ]
        assert len(degrees) == N
        assert sum(degrees) == ordered_counts[color]
        assert sum(
            degree * (degree - 1) // 2 for degree in degrees
        ) == color_wedges[color][color]
        assert erdos_gallai(degrees)
        degree_sequences.append(tuple(sorted(degrees)))

        triangles = triple_counts.get((color, color, color), 0)
        two_edges = color_wedges[color][color] - 3 * triangles
        one_edge = (
            unordered_counts[color] * (N - 2)
            - 2 * two_edges
            - 3 * triangles
        )
        zero_edges = comb(N, 3) - one_edge - two_edges - triangles
        assert min(zero_edges, one_edge, two_edges, triangles) >= 0
        motif_counts.append(
            (zero_edges, one_edge, two_edges, triangles)
        )
    assert motif_counts == [
        (7620, 2765, 275, 0),
        (10546, 111, 3, 0),
        (6445, 3364, 808, 43),
        (2185, 5084, 2543, 848),
        (2782, 5654, 1601, 623),
    ]

    # Exact next-degree failure: the total-degree-four k=4 scalar.
    degree_4_failure = harmonic_matrix(
        4, 4, nodes, ordered_counts, triple_counts
    )[0][0]
    assert degree_4_failure == Q(
        -1924383662903127930296851,
        4100000000000000000000000,
    )

    return {
        "triple_type_count": len(triple_counts),
        "minimum_3_by_3_determinant": min(gram_determinants.values()),
        "incidences": incidences,
        "color_wedges": color_wedges,
        "degree_3_minimum_principal_minors": minimum_minors,
        "fixed_rank_residual": fixed_rank_residual,
        "rank_five_residual": rank_five_residual,
        "color_covariance_minimum_positive_minor": Q(456, 41),
        "individual_color_degree_sequences": degree_sequences,
        "individual_color_motif_counts": motif_counts,
        "degree_4_failure": degree_4_failure,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
