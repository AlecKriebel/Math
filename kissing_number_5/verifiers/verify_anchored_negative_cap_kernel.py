#!/usr/bin/env python3
"""Verify exact anchored negative-neighborhood cap-kernel evaluations.

The cap polynomial is reconstructed from its rational Gram factors.  This
script checks the aggregate pair/triple formula on two pseudodistributions,
all support-induced threshold cuts, all subsets of nonpositive support
colors, and an exact D5 sanity instance.  A pseudodistribution is never
treated as a simultaneous edge-colored graph.
"""

from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
from itertools import combinations, permutations, product
import json
from pathlib import Path

try:
    from verifiers.verify_one_sided_cap_degree10 import (
        CERTIFICATE_PATH as CAP_CERTIFICATE,
        cap_polynomial,
        factor_payload_digest,
        load_blocks,
    )
except ModuleNotFoundError:
    from verify_one_sided_cap_degree10 import (
        CERTIFICATE_PATH as CAP_CERTIFICATE,
        cap_polynomial,
        factor_payload_digest,
        load_blocks,
    )


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT / "certificates" / "anchored_negative_cap_kernel_evaluations.json"
)
N = 41


def file_sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def polynomial_evaluator(polynomial):
    @lru_cache(maxsize=None)
    def evaluate(u, v, t):
        return sum(
            coefficient * u**i * v**j * t**k
            for (i, j, k), coefficient in polynomial.items()
        )

    return evaluate


def integer_aggregate(evaluate, nodes, ordered_counts, triple_counts, selected):
    """Return diagonal, off-diagonal, total for unnormalized counts."""

    diagonal = sum(
        Q(ordered_counts[index])
        * evaluate(-nodes[index], -nodes[index], Q(1))
        for index in selected
    )
    off_diagonal = Q(0)
    for triple, count in triple_counts.items():
        orbit = tuple(sorted(set(permutations(triple))))
        orbit_sum = sum(
            (
                evaluate(-nodes[u], -nodes[v], nodes[t])
                for u, v, t in orbit
                if u in selected and v in selected
            ),
            Q(0),
        )
        off_diagonal += Q(6 * count, len(orbit)) * orbit_sum
    return diagonal, off_diagonal, diagonal + off_diagonal


def measure_aggregate(evaluate, nodes, alpha, triples, nu, selected):
    """Return the same functional for measures normalized by 1/N."""

    diagonal = sum(
        alpha[index] * evaluate(-nodes[index], -nodes[index], Q(1))
        for index in selected
    )
    off_diagonal = Q(0)
    for triple, weight in zip(triples, nu):
        orbit = tuple(sorted(set(permutations(triple))))
        orbit_sum = sum(
            (
                evaluate(-nodes[u], -nodes[v], nodes[t])
                for u, v, t in orbit
                if u in selected and v in selected
            ),
            Q(0),
        )
        off_diagonal += weight / len(orbit) * orbit_sum
    return diagonal, off_diagonal, diagonal + off_diagonal


def all_subset_values(functional, support_indices):
    values = {}
    for mask in range(1, 1 << len(support_indices)):
        selected = {
            support_indices[index]
            for index in range(len(support_indices))
            if mask & (1 << index)
        }
        values[mask] = functional(selected)[2]
    return values


def load_local(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == (
        "local-hybrid-degree4-rank-color-clique-pseudodistribution-v1"
    )
    assert data["dimension"] == 5 and data["cardinality"] == N
    nodes = tuple(Q(value) for value in data["nodes"])
    ordered_counts = tuple(data["ordered_pair_counts"])
    triple_counts = {
        tuple(item["types"]): item["count"]
        for item in data["triple_counts"]
    }
    assert sum(ordered_counts) == N * (N - 1)
    assert sum(triple_counts.values()) == N * (N - 1) * (N - 2) // 6
    for edge_type, count in enumerate(ordered_counts):
        assert sum(
            triple.count(edge_type) * multiplicity
            for triple, multiplicity in triple_counts.items()
        ) == (N - 2) * (count // 2)
    return nodes, ordered_counts, triple_counts


def load_all_harmonic(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assert data["schema"] == (
        "fixed41-bv-fullradial-k16-pseudodistribution-v1"
    )
    assert data["dimension"] == 5 and data["cardinality"] == N
    nodes = tuple(Q(value) for value in data["grid"])
    triples = tuple(tuple(item) for item in data["triples"])
    alpha = tuple(Q(value) for value in data["alpha"])
    nu = tuple(Q(value) for value in data["nu"])
    assert len(triples) == len(nu)
    assert sum(alpha) == N - 1
    assert sum(nu) == (N - 1) * (N - 2)
    return nodes, alpha, triples, nu


def d5_sanity(evaluate):
    roots = []
    for first, second in combinations(range(5), 2):
        for first_sign, second_sign in product((-1, 1), repeat=2):
            vector = [0] * 5
            vector[first] = first_sign
            vector[second] = second_sign
            roots.append(vector)
    gram = [
        [
            Q(sum(a * b for a, b in zip(left, right)), 2)
            for right in roots
        ]
        for left in roots
    ]
    direct = Q(0)
    neighborhood_sizes = []
    for anchor in range(len(roots)):
        neighborhood = [
            point
            for point in range(len(roots))
            if point != anchor and gram[anchor][point] <= 0
        ]
        neighborhood_sizes.append(len(neighborhood))
        direct += sum(
            (
                evaluate(
                    -gram[anchor][first],
                    -gram[anchor][second],
                    gram[first][second],
                )
                for first in neighborhood
                for second in neighborhood
            ),
            Q(0),
        )

    nodes = tuple(sorted({
        gram[first][second]
        for first in range(len(roots))
        for second in range(first)
    }))
    node_index = {node: index for index, node in enumerate(nodes)}
    ordered_counts = [0] * len(nodes)
    for first in range(len(roots)):
        for second in range(len(roots)):
            if first != second:
                ordered_counts[node_index[gram[first][second]]] += 1
    triple_counts = Counter()
    for first, second, third in combinations(range(len(roots)), 3):
        triple = tuple(sorted((
            node_index[gram[first][second]],
            node_index[gram[first][third]],
            node_index[gram[second][third]],
        )))
        triple_counts[triple] += 1
    selected = {
        index for index, node in enumerate(nodes) if node <= 0
    }
    aggregate = integer_aggregate(
        evaluate, nodes, ordered_counts, triple_counts, selected
    )[2]
    assert direct == aggregate > 0
    assert set(neighborhood_sizes) == {27}
    return direct


def verify():
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert certificate["schema"] == (
        "anchored-negative-cap-kernel-evaluations-v1"
    )
    cap_data = json.loads(CAP_CERTIFICATE.read_text(encoding="utf-8"))
    assert factor_payload_digest(cap_data) == certificate[
        "cap_factor_payload_sha256"
    ]
    polynomial = cap_polynomial(load_blocks(str(CAP_CERTIFICATE)))
    evaluate = polynomial_evaluator(polynomial)

    local_source = ROOT / certificate["sources"]["local_degree4"]["path"]
    harmonic_source = ROOT / certificate["sources"]["all_harmonic"]["path"]
    assert file_sha256(local_source) == certificate["sources"][
        "local_degree4"
    ]["sha256"]
    assert file_sha256(harmonic_source) == certificate["sources"][
        "all_harmonic"
    ]["sha256"]

    nodes, ordered_counts, triple_counts = load_local(local_source)
    local_nonpositive = tuple(
        index for index, node in enumerate(nodes) if node <= 0
    )
    assert local_nonpositive == (0, 1, 2, 3)
    local_functional = lambda selected: integer_aggregate(
        evaluate, nodes, ordered_counts, triple_counts, selected
    )
    local_full = local_functional(set(local_nonpositive))
    local_expected = certificate["local_degree4"]
    assert local_full == (
        Q(local_expected["full_negative_diagonal"]),
        Q(local_expected["full_negative_off_diagonal"]),
        Q(local_expected["full_negative_total"]),
    )
    local_nested = tuple(
        local_functional(set(local_nonpositive[:end]))[2]
        for end in range(1, len(local_nonpositive) + 1)
    )
    assert local_nested == tuple(
        Q(value)
        for value in local_expected["nested_height_threshold_totals"]
    )
    local_subsets = all_subset_values(
        local_functional, local_nonpositive
    )
    assert len(local_subsets) == local_expected[
        "all_nonempty_support_subsets_checked"
    ]
    assert min(local_subsets.items(), key=lambda item: item[1]) == (
        local_expected["minimum_subset_mask"],
        Q(local_expected["minimum_subset_total"]),
    )
    assert min(local_subsets.values()) > 0

    harmonic_nodes, alpha, triples, nu = load_all_harmonic(
        harmonic_source
    )
    harmonic_nonpositive = tuple(
        index for index, node in enumerate(harmonic_nodes) if node <= 0
    )
    assert harmonic_nonpositive == (0, 1, 2, 3, 4)
    harmonic_functional = lambda selected: measure_aggregate(
        evaluate, harmonic_nodes, alpha, triples, nu, selected
    )
    harmonic_full = harmonic_functional(set(harmonic_nonpositive))
    harmonic_expected = certificate["all_harmonic"]
    assert harmonic_full == (
        Q(harmonic_expected["full_nonpositive_diagonal"]),
        Q(harmonic_expected["full_nonpositive_off_diagonal"]),
        Q(harmonic_expected["full_nonpositive_total"]),
    )
    harmonic_nested = tuple(
        harmonic_functional(set(harmonic_nonpositive[:end]))[2]
        for end in range(1, len(harmonic_nonpositive) + 1)
    )
    assert harmonic_nested == tuple(
        Q(value)
        for value in harmonic_expected["nested_height_threshold_totals"]
    )
    harmonic_subsets = all_subset_values(
        harmonic_functional, harmonic_nonpositive
    )
    assert len(harmonic_subsets) == harmonic_expected[
        "all_nonempty_support_subsets_checked"
    ]
    assert min(harmonic_subsets.items(), key=lambda item: item[1]) == (
        harmonic_expected["minimum_subset_mask"],
        Q(harmonic_expected["minimum_subset_total"]),
    )
    assert min(harmonic_subsets.values()) > 0

    d5_value = d5_sanity(evaluate)
    assert d5_value == Q(
        certificate["d5_sanity"]["direct_and_aggregate_total"]
    )
    assert certificate["d5_sanity"]["negative_neighborhood_size"] == 27

    return {
        "status": "PASS",
        "local_full_negative_total": local_full[2],
        "local_minimum_subset_total": min(local_subsets.values()),
        "historical_full_nonpositive_total_normalized": harmonic_full[2],
        "historical_minimum_subset_total_normalized": min(
            harmonic_subsets.values()
        ),
        "d5_direct_and_aggregate_total": d5_value,
        "conclusion": "strict positive slack; neither witness separated",
    }


if __name__ == "__main__":
    for key, value in verify().items():
        print(f"{key}: {value}")
