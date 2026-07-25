#!/usr/bin/env python3
"""Exact verifier for the strongest local-hybrid four-degree barrier.

The certificate is a triple pseudodistribution, not a graph or Gram
realization.  All proof-relevant arithmetic in this verifier uses Fraction.
"""

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
        zonal_values,
    )
    from verifiers.verify_one_sided_cap_degree10 import (
        CERTIFICATE_PATH as CAP_CERTIFICATE,
        cap_polynomial,
        load_blocks,
    )
    from verifiers.verify_weighted_residual_barrier import (
        center_count,
        harmonic_matrix,
    )
except ModuleNotFoundError:  # Direct execution from the verifier directory.
    from verify_fixed41_bv_degree5 import determinant
    from verify_local_hybrid_barrier import (
        common_center_bound,
        integer_wedge_minimum,
        load_certificate as load_pair_certificate,
        threshold_test_points,
        zonal_values,
    )
    from verify_one_sided_cap_degree10 import (
        CERTIFICATE_PATH as CAP_CERTIFICATE,
        cap_polynomial,
        load_blocks,
    )
    from verify_weighted_residual_barrier import (
        center_count,
        harmonic_matrix,
    )


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "certificates"
    / "local_hybrid_degree4_rank_color_clique_pseudodistribution.json"
)
N = 41


def load_certificate():
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert data["schema"] == (
        "local-hybrid-degree4-rank-color-clique-pseudodistribution-v1"
    )
    assert data["dimension"] == 5
    assert data["cardinality"] == N
    assert Q(data["maximum_inner_product"]) == Q(1, 2)
    nodes = tuple(Q(value) for value in data["nodes"])
    ordered_counts = tuple(data["ordered_pair_counts"])
    triple_items = tuple(
        (tuple(item["types"]), item["count"])
        for item in data["triple_counts"]
    )
    degree_items = tuple(
        (tuple(item["degrees"]), item["multiplicity"])
        for item in data["joint_degree_vectors"]
    )
    assert triple_items == tuple(sorted(triple_items))
    assert degree_items == tuple(sorted(degree_items))
    assert len({item[0] for item in triple_items}) == len(triple_items)
    assert all(
        tuple(sorted(triple)) == triple and count > 0
        for triple, count in triple_items
    )
    assert all(
        len(degrees) == len(nodes)
        and min(degrees) >= 0
        and multiplicity > 0
        for degrees, multiplicity in degree_items
    )
    return nodes, ordered_counts, dict(triple_items), degree_items


def principal_minors(matrix):
    answer = []
    for size in range(1, len(matrix) + 1):
        for indices in combinations(range(len(matrix)), size):
            minor = [[matrix[i][j] for j in indices] for i in indices]
            answer.append((determinant(minor), indices))
    return answer


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


def evaluate(poly, u, v, t):
    return sum(
        coefficient * u**i * v**j * t**k
        for (i, j, k), coefficient in poly.items()
    )


def kernel_spectral_moments(
    nodes, ordered_counts, triple_counts, harmonic_weights
):
    """Exact tr(K), tr(K^2), tr(K^3) for a zonal-kernel combination."""

    maximum_degree = max(harmonic_weights)

    def kernel(t):
        values = zonal_values(t, maximum_degree)
        return sum(
            coefficient * values[degree]
            for degree, coefficient in harmonic_weights.items()
        )

    diagonal = kernel(Q(1))
    node_values = tuple(kernel(node) for node in nodes)
    pair_square = sum(
        Q(count) * value**2
        for count, value in zip(ordered_counts, node_values)
    )
    trace_one = N * diagonal
    trace_two = N * diagonal**2 + pair_square
    trace_three = N * diagonal**3 + 3 * diagonal * pair_square
    trace_three += 6 * sum(
        Q(count)
        * node_values[i]
        * node_values[j]
        * node_values[k]
        for (i, j, k), count in triple_counts.items()
    )
    return trace_one, trace_two, trace_three


def verify():
    nodes, ordered_counts, triple_counts, degree_items = load_certificate()
    size, pair_nodes, pair_counts, _, _ = load_pair_certificate()
    assert size == N
    assert nodes == pair_nodes
    assert ordered_counts == pair_counts
    unordered_counts = tuple(count // 2 for count in ordered_counts)

    assert sum(triple_counts.values()) == comb(N, 3)
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

    color_wedges = [
        [0 for _ in nodes] for _ in nodes
    ]
    for triple, count in triple_counts.items():
        for first in range(len(nodes)):
            first_count = triple.count(first)
            color_wedges[first][first] += (
                first_count * (first_count - 1) // 2 * count
            )
            for second in range(first + 1, len(nodes)):
                value = first_count * triple.count(second) * count
                color_wedges[first][second] += value
                color_wedges[second][first] += value
    assert color_wedges == [
        [275, 17, 1091, 2733, 2239],
        [17, 3, 30, 99, 82],
        [1091, 30, 714, 4147, 3522],
        [2733, 99, 4147, 4925, 8599],
        [2239, 82, 3522, 8599, 3504],
    ]

    # Every universal threshold wedge inequality used in the search.
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

    # On this support, two incident color-{0,1} edges can close only in
    # color 4.  Six color-4 equidistant vectors would have the positive
    # definite Gram eigenvalues 1-s (multiplicity 5) and 1+5s, and hence
    # rank 6.  Thus each color-{0,1} row degree is at most five.
    for first in (0, 1):
        for second in (0, 1):
            feasible_closers = []
            for closer in range(len(nodes)):
                u, v, t = nodes[first], nodes[second], nodes[closer]
                gram_det = 1 + 2 * u * v * t - u * u - v * v - t * t
                if gram_det >= 0:
                    feasible_closers.append(closer)
            assert feasible_closers == [4]
    equidistant_value = nodes[4]
    assert 1 - equidistant_value > 0
    assert 1 + 5 * equidistant_value > 0
    assert (
        color_wedges[0][1] + 2 * color_wedges[1][1]
        <= 4 * ordered_counts[1]
    )
    assert color_wedges[0][1] + 2 * color_wedges[1][1] == 23

    # All total-degree-four Bachoc--Vallentin blocks are positive definite.
    minimum_minors = {}
    for harmonic_degree in range(5):
        matrix = harmonic_matrix(
            4,
            harmonic_degree,
            nodes,
            ordered_counts,
            triple_counts,
        )
        minors = principal_minors(matrix)
        assert all(value > 0 for value, _ in minors)
        minimum_minors[harmonic_degree] = min(minors)

    # The fixed-rank C047 consequence holds strictly.
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
    assert triple_cycle_moment == Q(116433421869, 2562500000)
    assert fixed_rank_residual == Q(34689369, 2562500000)
    assert rank_five_residual == Q(
        -587191589183847267, 25000000000000000
    ) < 0

    # Full centered covariance of the five color-degree columns.
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
    covariance_minors = principal_minors(color_covariance)
    assert all(value >= 0 for value, _ in covariance_minors)
    assert [
        item for item in covariance_minors if item[0] == 0
    ] == [(Q(0), (0, 1, 2, 3, 4))]
    assert min(
        item for item in covariance_minors if item[0] > 0
    ) == (Q(456, 41), (1,))

    # Rank-sensitive centered-skew cuts for complete zonal kernel matrices.
    # If a real symmetric matrix K has rank at most r, then, with
    # V=tr(K^2)-tr(K)^2/r and
    # D=tr(K^3)-3 tr(K)tr(K^2)/r+2 tr(K)^3/r^2,
    #
    #   r(r-1)D^2 <= (r-2)^2 V^3.
    #
    # Harmonic degree k has rank at most h_k on S^4.  These two rational
    # choices give exact violations by the degree-four pseudo-measure.
    mixed_traces = kernel_spectral_moments(
        nodes,
        ordered_counts,
        triple_counts,
        {0: Q(1, 6), 1: Q(5, 6)},
    )
    mixed_trace_one, mixed_trace_two, mixed_trace_three = mixed_traces
    mixed_variance = (
        mixed_trace_two - mixed_trace_one**2 / 6
    )
    mixed_third = (
        mixed_trace_three
        - Q(3, 6) * mixed_trace_one * mixed_trace_two
        + Q(2, 36) * mixed_trace_one**3
    )
    mixed_rank_residual = (
        8 * mixed_variance**3 - 15 * mixed_third**2
    )
    assert mixed_traces == (
        Q(41),
        Q(8149679, 28800),
        Q(71571557473, 36000000),
    )
    assert mixed_variance == Q(80879, 28800)
    assert mixed_third == Q(289016549, 18000000)
    assert mixed_rank_residual == Q(
        -34431882734317334357,
        9331200000000000,
    ) < 0

    degree_two_traces = kernel_spectral_moments(
        nodes,
        ordered_counts,
        triple_counts,
        {2: Q(1)},
    )
    h2_trace_one, h2_trace_two, h2_trace_three = degree_two_traces
    h2_variance = h2_trace_two - h2_trace_one**2 / 14
    h2_third = (
        h2_trace_three
        - Q(3, 14) * h2_trace_one * h2_trace_two
        + Q(2, 196) * h2_trace_one**3
    )
    h2_rank_residual = 72 * h2_variance**3 - 91 * h2_third**2
    assert degree_two_traces == (
        Q(41),
        Q(1566584056811, 12800000000),
        Q(48029489854860834589, 128000000000000000),
    )
    assert h2_variance == Q(
        207688397677, 89600000000
    )
    assert h2_third == Q(
        20244638316825894861,
        6272000000000000000,
    )
    assert h2_rank_residual == Q(
        -5894231556035691703147357630514100177,
        114688000000000000000000000000000000,
    ) < 0

    # The rational intervals used by the discovery MILP are necessary
    # outer approximations to the exact square-root bounds.
    assert (
        15 * Q(7, 2) ** 2 - 8 * mixed_variance**3
        == Q(19611647008561, 2985984000000)
        > 0
    )
    assert (
        91 * Q(157, 50) ** 2 - 72 * h2_variance**3
        == Q(
            47450085131380413914603963850403,
            89915392000000000000000000000000,
        )
        > 0
    )

    # Exact joint row-degree decomposition.  This is stronger than separate
    # marginal graphicality but still does not construct one colored graph.
    degree_rows = []
    for degrees, multiplicity in degree_items:
        degree_rows.extend([degrees] * multiplicity)
    assert len(degree_rows) == N
    assert all(sum(row) == N - 1 for row in degree_rows)
    assert all(row[0] + row[1] <= 5 for row in degree_rows)
    assert min(sum(row[:4]) for row in degree_rows) == 22 >= 7
    assert sum(sum(row[:4]) for row in degree_rows) == 1090
    for first in range(len(nodes)):
        assert sum(row[first] for row in degree_rows) == ordered_counts[first]
        assert sum(
            row[first] * (row[first] - 1) // 2
            for row in degree_rows
        ) == color_wedges[first][first]
        for second in range(first + 1, len(nodes)):
            assert sum(
                row[first] * row[second] for row in degree_rows
            ) == color_wedges[first][second]

    union_degree_sequences = {}
    union_motif_counts = {}
    for mask in range(1, 1 << len(nodes)):
        subset = {
            index for index in range(len(nodes)) if mask & (1 << index)
        }
        degrees = tuple(
            sorted(
                sum(row[index] for index in subset)
                for row in degree_rows
            )
        )
        assert erdos_gallai(degrees)
        union_degree_sequences[mask] = degrees

        edges = sum(unordered_counts[index] for index in subset)
        wedges = 0
        triangles = 0
        for triple, count in triple_counts.items():
            selected = sum(index in subset for index in triple)
            wedges += selected * (selected - 1) // 2 * count
            if selected == 3:
                triangles += count
        two_edges = wedges - 3 * triangles
        one_edge = (
            edges * (N - 2) - 2 * two_edges - 3 * triangles
        )
        zero_edges = comb(N, 3) - one_edge - two_edges - triangles
        motif = zero_edges, one_edge, two_edges, triangles
        assert min(motif) >= 0
        union_motif_counts[mask] = motif
    assert [union_motif_counts[1 << color] for color in range(5)] == [
        (7620, 2765, 275, 0),
        (10546, 111, 3, 0),
        (6240, 3756, 639, 25),
        (2220, 4817, 2972, 651),
        (2813, 5595, 1626, 626),
    ]

    # The exact cap-SDP kernel, anchored at each row and summed over its
    # positive neighbors, is valid but does not separate this witness.
    cap_poly = cap_polynomial(load_blocks(str(CAP_CERTIFICATE)))
    positive_node = nodes[4]
    anchored_cap_sum = (
        Q(ordered_counts[4])
        * evaluate(cap_poly, positive_node, positive_node, Q(1))
    )
    for closer in range(4):
        anchored_cap_sum += (
            2
            * triple_counts.get((closer, 4, 4), 0)
            * evaluate(
                cap_poly, positive_node, positive_node, nodes[closer]
            )
        )
    anchored_cap_sum += (
        6
        * triple_counts[(4, 4, 4)]
        * evaluate(cap_poly, positive_node, positive_node, positive_node)
    )
    assert anchored_cap_sum == Q(
        10900679016442230075787594834809436525730644961751705316478717975134361189524810533654029,
        1059717120000000000000000000000000000000000000000000000000000000000000000000000000000,
    ) > 0

    # The next total degree fails, so this is a sharp scoped barrier.
    degree_five_failure = harmonic_matrix(
        5, 4, nodes, ordered_counts, triple_counts
    )[1][1]
    assert degree_five_failure == Q(
        -894220395027688277353640397221,
        20500000000000000000000000000000,
    ) < 0

    return {
        "triple_type_count": len(triple_counts),
        "minimum_3_by_3_determinant": min(gram_determinants.values()),
        "color_wedges": color_wedges,
        "degree_4_minimum_principal_minors": minimum_minors,
        "fixed_rank_residual": fixed_rank_residual,
        "rank_five_residual": rank_five_residual,
        "mixed_harmonic_rank_residual": mixed_rank_residual,
        "degree_two_harmonic_rank_residual": h2_rank_residual,
        "color_covariance_minimum_positive_minor": Q(456, 41),
        "joint_degree_vector_type_count": len(degree_items),
        "negative_union_minimum_degree": min(
            sum(row[:4]) for row in degree_rows
        ),
        "all_nontrivial_color_unions_graphical": True,
        "anchored_cap_kernel_sum": anchored_cap_sum,
        "degree_5_failure": degree_five_failure,
        "status": "PASS",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
