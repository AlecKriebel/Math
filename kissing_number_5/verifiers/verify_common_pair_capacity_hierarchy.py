#!/usr/bin/env python3
"""Exact verifier for the refuted cumulative-only hierarchy artifact.

Only standard-library arithmetic is used here.  Discovery solver output is
not read or trusted.  Passing this program verifies the stored cumulative
threshold rows; it does not verify all arbitrary-base-subset consequences
of the pointwise projection theorem.  The candidate is refuted by the
stratified audit and must not be cited as a surviving barrier.
"""

from fractions import Fraction as Q
from hashlib import sha256
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
    from verify_weighted_residual_barrier import (
        center_count,
        harmonic_matrix,
    )


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "certificates"
    / "common_pair_capacity_degree4_pseudodistribution.json"
)
N = 41


def capacity_from_p(p):
    """Return the proved capacity, or None below the useful range."""

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


def capacity_for_thresholds(base_threshold, high_threshold):
    assert -1 <= base_threshold <= 0
    assert 0 < high_threshold <= Q(1, 2)
    if base_threshold == -1:
        return None, 0
    p = 2 * high_threshold**2 / (1 + base_threshold)
    return p, capacity_from_p(p)


def qualifying_edge_count(triple, nodes, base_threshold, high_threshold):
    """Number of qualifying base edges in one unordered colored triangle."""

    answer = 0
    for base_position in range(3):
        other_positions = tuple(
            position for position in range(3) if position != base_position
        )
        if (
            nodes[triple[base_position]] <= base_threshold
            and nodes[triple[other_positions[0]]] >= high_threshold
            and nodes[triple[other_positions[1]]] >= high_threshold
        ):
            answer += 1
    return answer


def hierarchy_rows(nodes, ordered_counts, triple_counts):
    """Reconstruct all nontrivial finite-support threshold rows exactly."""

    answer = []
    base_thresholds = tuple(node for node in nodes if node <= 0)
    high_thresholds = tuple(node for node in nodes if node > 0)
    for base_threshold in base_thresholds:
        for high_threshold in high_thresholds:
            p, capacity = capacity_for_thresholds(
                base_threshold, high_threshold
            )
            if capacity is None:
                continue
            left = sum(
                Q(count)
                * qualifying_edge_count(
                    triple, nodes, base_threshold, high_threshold
                )
                for triple, count in triple_counts.items()
            )
            right = Q(capacity) * sum(
                Q(count, 2)
                for node, count in zip(nodes, ordered_counts)
                if node <= base_threshold
            )
            answer.append(
                {
                    "base_threshold": base_threshold,
                    "high_threshold": high_threshold,
                    "p": p,
                    "capacity": capacity,
                    "left": left,
                    "right": right,
                    "slack": right - left,
                }
            )
    return tuple(answer)


def principal_minors(matrix):
    answer = []
    for size in range(1, len(matrix) + 1):
        for indices in combinations(range(len(matrix)), size):
            minor = [[matrix[i][j] for j in indices] for i in indices]
            answer.append((determinant(minor), indices))
    return answer


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load_candidate(path=CERTIFICATE):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == (
        "common-pair-capacity-degree4-pseudodistribution-v1"
    )
    assert data["status"] == "REFUTED"
    assert data["dimension"] == 5
    assert data["cardinality"] == N
    assert Q(data["maximum_inner_product"]) == Q(1, 2)
    nodes = tuple(Q(value) for value in data["nodes"])
    ordered_counts = tuple(data["ordered_pair_counts"])
    triple_items = tuple(
        (tuple(item["types"]), item["count"])
        for item in data["triple_counts"]
    )
    assert triple_items == tuple(sorted(triple_items))
    assert len({triple for triple, _ in triple_items}) == len(triple_items)
    assert all(
        len(triple) == 3
        and tuple(sorted(triple)) == triple
        and count > 0
        for triple, count in triple_items
    )
    return data, nodes, ordered_counts, dict(triple_items)


def kernel_spectral_moments(
    nodes, ordered_counts, triple_counts, harmonic_weights
):
    maximum_degree = max(harmonic_weights)

    def kernel(t):
        values = zonal_values(t, maximum_degree)
        return sum(
            coefficient * values[degree]
            for degree, coefficient in harmonic_weights.items()
        )

    diagonal = kernel(Q(1))
    values = tuple(kernel(node) for node in nodes)
    pair_square = sum(
        Q(count) * value**2
        for count, value in zip(ordered_counts, values)
    )
    trace_one = N * diagonal
    trace_two = N * diagonal**2 + pair_square
    trace_three = N * diagonal**3 + 3 * diagonal * pair_square
    trace_three += 6 * sum(
        Q(count) * values[i] * values[j] * values[k]
        for (i, j, k), count in triple_counts.items()
    )
    return trace_one, trace_two, trace_three


def verify_source_audits(data):
    audit = data["source_audits"]
    local_results = []
    for stored in audit["local_hybrid_witnesses"]:
        path = ROOT / stored["file"]
        assert file_digest(path) == stored["sha256"]
        source = json.loads(path.read_text(encoding="utf-8"))
        nodes = tuple(Q(value) for value in source["nodes"])
        ordered_counts = tuple(source["ordered_pair_counts"])
        triple_counts = {
            tuple(item["types"]): item["count"]
            for item in source["triple_counts"]
        }
        rows = hierarchy_rows(nodes, ordered_counts, triple_counts)
        strong = next(
            row
            for row in rows
            if row["base_threshold"] == Q(-11, 25)
            and row["high_threshold"] == Q(499, 1000)
        )
        assert strong["p"] == Q(249001, 280000)
        assert strong["capacity"] == 1
        assert strong["left"] == stored["strong_cut_left"]
        assert strong["right"] == stored["strong_cut_right"]
        assert strong["slack"] == stored["slack"] < 0
        local_results.append(strong["slack"])

    harmonic_stored = audit["all_harmonic_witness"]
    path = ROOT / harmonic_stored["file"]
    assert file_digest(path) == harmonic_stored["sha256"]
    all_harmonic_certificate = (
        ROOT / harmonic_stored["all_harmonic_certificate"]
    )
    assert file_digest(all_harmonic_certificate) == (
        harmonic_stored["all_harmonic_certificate_sha256"]
    )
    source = json.loads(path.read_text(encoding="utf-8"))
    nodes = tuple(Q(value) for value in source["grid"])
    alpha = tuple(Q(value) for value in source["alpha"])
    triples = tuple(tuple(item) for item in source["triples"])
    nu = tuple(Q(value) for value in source["nu"])
    assert len(triples) == len(nu)

    harmonic_rows = []
    for base_threshold in (node for node in nodes if node <= 0):
        for high_threshold in (node for node in nodes if node > 0):
            p, capacity = capacity_for_thresholds(
                base_threshold, high_threshold
            )
            if capacity is None:
                continue
            # A stored nu weight is the total mass of its permutation orbit.
            # Symmetry therefore assigns one third of the sum over the three
            # possible base-edge positions to a fixed coordinate.
            left = sum(
                weight
                * qualifying_edge_count(
                    triple, nodes, base_threshold, high_threshold
                )
                / 3
                for triple, weight in zip(triples, nu)
            )
            right = Q(capacity) * sum(
                weight
                for node, weight in zip(nodes, alpha)
                if node <= base_threshold
            )
            assert left <= right
            harmonic_rows.append(
                (
                    base_threshold,
                    high_threshold,
                    p,
                    capacity,
                    left,
                    right,
                    right - left,
                )
            )

    positive_slacks = tuple(
        row[-1] for row in harmonic_rows if row[-1] > 0
    )
    zero_slacks = tuple(row[-1] for row in harmonic_rows if row[-1] == 0)
    assert len(harmonic_rows) == harmonic_stored["nontrivial_cut_count"]
    assert len(positive_slacks) == harmonic_stored["positive_slack_count"]
    assert len(zero_slacks) == harmonic_stored["zero_slack_count"]
    assert min(positive_slacks) == Q(
        harmonic_stored["minimum_positive_slack"]
    )
    return tuple(local_results), tuple(harmonic_rows)


def verify_candidate(data, nodes, ordered_counts, triple_counts):
    size, pair_nodes, pair_counts, _, _ = load_pair_certificate()
    assert size == N
    assert nodes == pair_nodes
    assert ordered_counts == pair_counts
    assert sum(ordered_counts) == N * (N - 1)
    assert all(count % 2 == 0 for count in ordered_counts)

    assert sum(triple_counts.values()) == comb(N, 3)
    incidences = tuple(
        sum(
            count * triple.count(color)
            for triple, count in triple_counts.items()
        )
        for color in range(len(nodes))
    )
    assert incidences == tuple(
        (N - 2) * count // 2 for count in ordered_counts
    )
    assert incidences == (3315, 117, 5109, 12714, 10725)

    # Every occupied triangle is in the full closed Gram-PSD domain.
    determinants = {}
    for triple in triple_counts:
        u, v, t = (nodes[index] for index in triple)
        value = 1 + 2 * u * v * t - u * u - v * v - t * t
        assert value >= 0
        determinants[triple] = value

    hierarchy = hierarchy_rows(nodes, ordered_counts, triple_counts)
    assert all(row["slack"] >= 0 for row in hierarchy)
    diagnostics = data["exact_diagnostics"]
    for key in ("common_pair_strong_cut", "common_pair_all_negative_cut"):
        stored = diagnostics[key]
        row = next(
            item
            for item in hierarchy
            if item["base_threshold"] == Q(stored["base_threshold"])
            and item["high_threshold"] == Q(stored["high_threshold"])
        )
        assert row["p"] == Q(stored["p"])
        assert row["capacity"] == stored["capacity"]
        assert row["left"] == stored["left"]
        assert row["right"] == stored["right"]
        assert row["slack"] == stored["slack"]

    # The previously used exact local wedge inequalities.
    threshold_rows = []
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
        deep_degree = sum(ordered_counts[index] for index in deep_types)
        high_edges = sum(
            ordered_counts[index] // 2 for index in high_types
        )
        wedges = sum(
            center_count(triple, deep_types) * count
            for triple, count in triple_counts.items()
        )
        lower = integer_wedge_minimum(deep_degree, N)
        upper = common_center_bound(q) * high_edges
        assert lower <= wedges <= upper
        threshold_rows.append((q, lower, wedges, upper))

    # Forced color-{0,1} neighborhood clique moment inequalities.
    color_wedges = [[0 for _ in nodes] for _ in nodes]
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
    for first in (0, 1):
        for second in (0, 1):
            feasible_closers = []
            for closer in range(len(nodes)):
                u, v, t = nodes[first], nodes[second], nodes[closer]
                gram_det = 1 + 2 * u * v * t - u * u - v * v - t * t
                if gram_det >= 0:
                    feasible_closers.append(closer)
            assert feasible_closers == [4]
    assert 1 - nodes[4] > 0
    assert 1 + 5 * nodes[4] > 0
    assert color_wedges[0][1] + 2 * color_wedges[1][1] == 24
    assert color_wedges[1][1] == 3

    # All degree-four Bachoc--Vallentin blocks are positive definite.
    minimum_minors = []
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
        minimum_minors.append(min(minors))
    stored_minors = diagnostics["minimum_BV_principal_minors"]
    assert len(stored_minors) == len(minimum_minors)
    for harmonic_degree, ((value, indices), stored) in enumerate(
        zip(minimum_minors, stored_minors)
    ):
        assert stored["harmonic_degree"] == harmonic_degree
        assert tuple(stored["indices"]) == indices
        assert Q(stored["value"]) == value

    # Exact fixed-rank C047 consequence.
    pair_square = sum(
        Q(count, N) * node**2
        for count, node in zip(ordered_counts, nodes)
    )
    triple_cycle = sum(
        Q(6 * count, N) * nodes[i] * nodes[j] * nodes[k]
        for (i, j, k), count in triple_counts.items()
    )
    delta = pair_square - Q(36, 5)
    center = Q(1116, 25) + Q(108, 5) * delta
    residual = triple_cycle - center
    polynomial_residual = 20 * residual**2 - 369 * delta**3
    # This is exactly the rank-five spectral inequality
    #
    #   20 D^2 - 9 V^3 <= 0,
    #
    # with D=N*residual and V=N*delta.  Dividing it by N^2 gives
    # 20*residual^2 - 9*N*delta^3, hence the coefficient 369=9*41.
    spectral_polynomial_residual = (
        20 * (N * residual) ** 2 - 9 * (N * delta) ** 3
    )
    assert spectral_polynomial_residual == N**2 * polynomial_residual
    stored_rank = diagnostics["rank_five_C047"]
    assert delta == Q(stored_rank["delta"])
    assert residual == Q(stored_rank["centered_residual"])
    assert polynomial_residual == Q(
        stored_rank["normalized_polynomial_residual"]
    ) < 0
    assert spectral_polynomial_residual == Q(
        stored_rank["spectral_polynomial_residual"]
    ) < 0

    # Two complete-kernel centered-skew inequalities.
    skew_results = {}
    for label, weights, rank in (
        (
            "H0_over_6_plus_5H1_over_6",
            {0: Q(1, 6), 1: Q(5, 6)},
            6,
        ),
        ("H2", {2: Q(1)}, 14),
    ):
        trace_one, trace_two, trace_three = kernel_spectral_moments(
            nodes, ordered_counts, triple_counts, weights
        )
        variance = trace_two - trace_one**2 / rank
        centered_third = (
            trace_three
            - 3 * trace_one * trace_two / rank
            + 2 * trace_one**3 / rank**2
        )
        skew_residual = (
            rank * (rank - 1) * centered_third**2
            - (rank - 2) ** 2 * variance**3
        )
        assert skew_residual <= 0
        assert skew_residual == Q(diagnostics["centered_skew"][label])
        skew_results[label] = skew_residual

    # Full centered covariance of the five colored degree columns.
    second_moment = [
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
    covariance = [
        [
            second_moment[first][second]
            - Q(
                ordered_counts[first] * ordered_counts[second],
                N,
            )
            for second in range(len(nodes))
        ]
        for first in range(len(nodes))
    ]
    covariance_minors = principal_minors(covariance)
    assert all(value >= 0 for value, _ in covariance_minors)
    assert [
        item for item in covariance_minors if item[0] == 0
    ] == [(Q(0), (0, 1, 2, 3, 4))]

    return {
        "hierarchy_rows": hierarchy,
        "triangle_determinants": determinants,
        "threshold_rows": tuple(threshold_rows),
        "minimum_BV_minors": tuple(minimum_minors),
        "C047_residual": polynomial_residual,
        "skew_residuals": skew_results,
        "color_wedges": color_wedges,
    }


def verify(path=CERTIFICATE):
    data, nodes, ordered_counts, triple_counts = load_candidate(path)
    local_audit, harmonic_audit = verify_source_audits(data)
    candidate = verify_candidate(
        data, nodes, ordered_counts, triple_counts
    )
    return {
        "local_witness_slacks": local_audit,
        "all_harmonic_rows": harmonic_audit,
        "candidate": candidate,
    }


if __name__ == "__main__":
    result = verify()
    candidate = result["candidate"]
    print("cumulative-only common-pair checks: PASS")
    print("candidate status: REFUTED by exact base-color strata")
    print("local witness slacks:", result["local_witness_slacks"])
    print(
        "all-harmonic minimum positive slack:",
        min(
            row[-1]
            for row in result["all_harmonic_rows"]
            if row[-1] > 0
        ),
    )
    print(
        "reoptimized strong-cut slack:",
        next(
            row["slack"]
            for row in candidate["hierarchy_rows"]
            if row["base_threshold"] == Q(-11, 25)
        ),
    )
    print("C047 residual:", candidate["C047_residual"])
