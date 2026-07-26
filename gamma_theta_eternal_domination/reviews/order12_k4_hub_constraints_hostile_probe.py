#!/usr/bin/env python3
"""Independent finite probes for the order-12 k=4 hub lemmas.

The eternal-domination evaluator below is implemented directly from the
one-guard definition and imports no campaign evaluator.
"""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[1]
NOTE = CAMPAIGN / "math/lemmas/order12_k4_hub_constraints.md"
FROZEN_NOTE_SHA256 = (
    "aab7cc335fddc367375258b655cdf6a637e371adf1aeb731accf9186531ea00c"
)


def graph_from_edge_mask(n: int, edge_mask: int) -> tuple[int, ...]:
    adjacency = [0] * n
    for index, (u, v) in enumerate(combinations(range(n), 2)):
        if edge_mask >> index & 1:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return tuple(adjacency)


def cycle(n: int) -> tuple[int, ...]:
    adjacency = [0] * n
    for vertex in range(n):
        neighbor = (vertex + 1) % n
        adjacency[vertex] |= 1 << neighbor
        adjacency[neighbor] |= 1 << vertex
    return tuple(adjacency)


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    full = (1 << len(adjacency)) - 1
    return tuple(
        (full ^ (1 << vertex)) & ~neighbors
        for vertex, neighbors in enumerate(adjacency)
    )


def induced(
    adjacency: tuple[int, ...],
    vertices: tuple[int, ...],
) -> tuple[int, ...]:
    old_to_new = {old: new for new, old in enumerate(vertices)}
    result = [0] * len(vertices)
    for new_u, old_u in enumerate(vertices):
        for old_v, new_v in old_to_new.items():
            if adjacency[old_u] >> old_v & 1:
                result[new_u] |= 1 << new_v
    return tuple(result)


def disjoint_union(
    first: tuple[int, ...],
    second: tuple[int, ...],
) -> tuple[int, ...]:
    shift = len(first)
    return tuple(first) + tuple(neighbors << shift for neighbors in second)


def dominates(adjacency: tuple[int, ...], configuration: int) -> bool:
    covered = configuration
    remaining = configuration
    while remaining:
        least = remaining & -remaining
        vertex = least.bit_length() - 1
        covered |= adjacency[vertex]
        remaining ^= least
    return covered == (1 << len(adjacency)) - 1


def eternal_at_most(adjacency: tuple[int, ...], k: int) -> bool:
    n = len(adjacency)
    live = {
        sum(1 << vertex for vertex in vertices)
        for vertices in combinations(range(n), k)
        if dominates(
            adjacency,
            sum(1 << vertex for vertex in vertices),
        )
    }
    changed = True
    while changed:
        changed = False
        remove: set[int] = set()
        for configuration in live:
            for attacked in range(n):
                attacked_bit = 1 << attacked
                if configuration & attacked_bit:
                    continue
                legal = False
                guards = configuration & adjacency[attacked]
                while guards:
                    guard_bit = guards & -guards
                    successor = (
                        configuration ^ guard_bit
                    ) | attacked_bit
                    if successor in live:
                        legal = True
                        break
                    guards ^= guard_bit
                if not legal:
                    remove.add(configuration)
                    break
        if remove:
            live.difference_update(remove)
            changed = True
    return bool(live)


@lru_cache(maxsize=None)
def gamma_infinity(adjacency: tuple[int, ...]) -> int:
    for k in range(1, len(adjacency) + 1):
        if eternal_at_most(adjacency, k):
            return k
    raise AssertionError("all-occupied configuration must be eternal")


def domination_number(adjacency: tuple[int, ...]) -> int:
    n = len(adjacency)
    for k in range(n + 1):
        for vertices in combinations(range(n), k):
            configuration = sum(1 << vertex for vertex in vertices)
            if dominates(adjacency, configuration):
                return k
    raise AssertionError("vertex set must dominate")


def p3(adjacency_h: tuple[int, ...]) -> bool:
    n = len(adjacency_h)
    for triple in combinations(range(n), 3):
        triple_mask = sum(1 << vertex for vertex in triple)
        if not any(
            not (triple_mask >> witness & 1)
            and all(adjacency_h[witness] >> vertex & 1 for vertex in triple)
            for witness in range(n)
        ):
            return False
    return True


def all_graphs(n: int):
    for edge_mask in range(1 << (n * (n - 1) // 2)):
        yield graph_from_edge_mask(n, edge_mask)


def verify_small_graph_facts() -> dict[str, object]:
    graph_count = 0
    induced_pair_count = 0
    p3_count = 0
    for n in range(1, 6):
        complete_edges = (1 << (n * (n - 1) // 2)) - 1
        for edge_mask, graph in enumerate(all_graphs(n)):
            graph_count += 1
            value = gamma_infinity(graph)
            if (value == 1) != (edge_mask == complete_edges):
                raise AssertionError("gamma-infinity-one characterization failed")
            for subset_mask in range(1, 1 << n):
                vertices = tuple(
                    vertex
                    for vertex in range(n)
                    if subset_mask >> vertex & 1
                )
                if gamma_infinity(induced(graph, vertices)) > value:
                    raise AssertionError("induced-subgraph direction failed")
                induced_pair_count += 1
            if n >= 3:
                p3_count += 1
                if (domination_number(graph) > 3) != p3(complement(graph)):
                    raise AssertionError("P3/domination equivalence failed")

    component_pair_count = 0
    for first_n in range(1, 4):
        for second_n in range(1, 4):
            for first in all_graphs(first_n):
                for second in all_graphs(second_n):
                    if gamma_infinity(disjoint_union(first, second)) != (
                        gamma_infinity(first) + gamma_infinity(second)
                    ):
                        raise AssertionError("component additivity failed")
                    component_pair_count += 1
    return {
        "labeled_graphs_n_le_5": graph_count,
        "induced_graph_pairs": induced_pair_count,
        "component_pairs_total_order_le_6": component_pair_count,
        "p3_equivalence_graphs": p3_count,
    }


def extension_from_mask(r: int, variable_mask: int) -> tuple[int, ...]:
    rim = cycle(5)
    n = 5 + r
    adjacency = list(rim) + [0] * r
    index = 0
    for outside in range(5, n):
        for rim_vertex in range(5):
            if variable_mask >> index & 1:
                adjacency[outside] |= 1 << rim_vertex
                adjacency[rim_vertex] |= 1 << outside
            index += 1
    for first, second in combinations(range(5, n), 2):
        if variable_mask >> index & 1:
            adjacency[first] |= 1 << second
            adjacency[second] |= 1 << first
        index += 1
    return tuple(adjacency)


def verify_theorem4_small_edges() -> dict[str, object]:
    results: dict[str, object] = {}
    for r in (2, 3):
        variable_count = 5 * r + r * (r - 1) // 2
        checked = 0
        qualifying = 0
        for mask in range(1 << variable_count):
            graph_h = extension_from_mask(r, mask)
            checked += 1
            hubs = [
                outside
                for outside in range(5, 5 + r)
                if all(
                    graph_h[outside] >> rim_vertex & 1
                    for rim_vertex in range(5)
                )
            ]
            hubs_independent = all(
                not (graph_h[first] >> second & 1)
                for first, second in combinations(hubs, 2)
            )
            if p3(graph_h) and hubs_independent:
                qualifying += 1
                if len(hubs) > r - 2:
                    raise AssertionError("Theorem 4 edge case failed")
        results[f"r_{r}"] = {
            "extensions_checked": checked,
            "p3_and_hub_independent": qualifying,
            "maximum_permitted_hubs": r - 2,
        }
    return results


def main() -> int:
    note_hash = sha256(NOTE.read_bytes()).hexdigest()
    if note_hash != FROZEN_NOTE_SHA256:
        raise AssertionError("hub note changed during hostile review")
    values = {
        "gamma_infinity_C7": gamma_infinity(cycle(7)),
        "gamma_infinity_complement_C5": gamma_infinity(
            complement(cycle(5))
        ),
        "gamma_infinity_complement_C7": gamma_infinity(
            complement(cycle(7))
        ),
        "gamma_infinity_complement_C9": gamma_infinity(
            complement(cycle(9))
        ),
    }
    if values != {
        "gamma_infinity_C7": 4,
        "gamma_infinity_complement_C5": 3,
        "gamma_infinity_complement_C7": 3,
        "gamma_infinity_complement_C9": 3,
    }:
        raise AssertionError("accepted cycle or antihole value differs")
    report = {
        "schema": "order12-k4-hub-constraints-hostile-probe-v1",
        "frozen_note_sha256": note_hash,
        "small_graph_facts": verify_small_graph_facts(),
        "accepted_values": values,
        "theorem4_edge_cases": verify_theorem4_small_edges(),
        "verdict_signal": "ACCEPT_WITHOUT_SCOPE_INFLATION",
    }
    print(json.dumps(report, allow_nan=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
