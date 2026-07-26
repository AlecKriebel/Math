#!/usr/bin/env python3
"""Clean-room probes for the order-12, parameter-four structural split.

This script intentionally imports no campaign implementation.  It checks:

* the exact P3/complement-connected conclusion exhaustively for every graph
  consisting of an induced C5 and r=0,1,2,3 outside vertices;
* disconnected boundary examples showing why connectedness cannot simply be
  omitted; and
* one-guard eternal-domination values using a direct greatest-fixed-point
  implementation of the definition.

The finite C5 enumeration is only a mutation/sign check; the review's general
acceptance rests on the written proof.
"""

from __future__ import annotations

from itertools import combinations


def cycle_graph(order: int) -> tuple[int, ...]:
    adj = [0] * order
    for vertex in range(order):
        neighbor = (vertex + 1) % order
        adj[vertex] |= 1 << neighbor
        adj[neighbor] |= 1 << vertex
    return tuple(adj)


def complement(adj: tuple[int, ...]) -> tuple[int, ...]:
    order = len(adj)
    full = (1 << order) - 1
    return tuple((full ^ (1 << vertex) ^ adj[vertex]) for vertex in range(order))


def has_p3(adj: tuple[int, ...]) -> bool:
    order = len(adj)
    for triple in combinations(range(order), 3):
        triple_mask = sum(1 << vertex for vertex in triple)
        if not any(
            vertex not in triple and (adj[vertex] & triple_mask) == triple_mask
            for vertex in range(order)
        ):
            return False
    return True


def connected(adj: tuple[int, ...]) -> bool:
    order = len(adj)
    seen = 1
    frontier = 1
    while frontier:
        vertex_bit = frontier & -frontier
        frontier ^= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        new = adj[vertex] & ~seen
        seen |= new
        frontier |= new
    return seen == (1 << order) - 1


def graph_with_fixed_rim(
    rim_order: int, outside_order: int, variable_edge_bits: int
) -> tuple[int, ...]:
    order = rim_order + outside_order
    adj = list(cycle_graph(rim_order)) + [0] * outside_order
    variable_edges = [
        (left, right)
        for left in range(order)
        for right in range(left + 1, order)
        if left >= rim_order or right >= rim_order
    ]
    for index, (left, right) in enumerate(variable_edges):
        if (variable_edge_bits >> index) & 1:
            adj[left] |= 1 << right
            adj[right] |= 1 << left
    return tuple(adj)


def exhaustive_c5_boundary() -> list[tuple[int, int, int, int, int, int]]:
    rows = []
    rim_order = 5
    for outside_order in range(4):
        variable_count = rim_order * outside_order + outside_order * (
            outside_order - 1
        ) // 2
        total = 1 << variable_count
        p3_count = 0
        p3_connected_complement_count = 0
        p3_with_hub_count = 0
        for bits in range(total):
            adj_h = graph_with_fixed_rim(rim_order, outside_order, bits)
            if not has_p3(adj_h):
                continue
            p3_count += 1
            rim_mask = (1 << rim_order) - 1
            if any(
                (adj_h[vertex] & rim_mask) == rim_mask
                for vertex in range(rim_order, rim_order + outside_order)
            ):
                p3_with_hub_count += 1
            if connected(complement(adj_h)):
                p3_connected_complement_count += 1
        rows.append(
            (
                outside_order,
                variable_count,
                total,
                p3_count,
                p3_with_hub_count,
                p3_connected_complement_count,
            )
        )
        assert p3_count == p3_with_hub_count
        assert p3_connected_complement_count == 0
    return rows


def complete_join_cycle(rim_order: int, outside_order: int) -> tuple[int, ...]:
    order = rim_order + outside_order
    adj = list(cycle_graph(rim_order)) + [0] * outside_order
    for outside in range(rim_order, order):
        for other in range(order):
            if other == outside:
                continue
            adj[outside] |= 1 << other
            adj[other] |= 1 << outside
    return tuple(adj)


def dominates(adj: tuple[int, ...], configuration: int) -> bool:
    dominated = configuration
    guards = configuration
    while guards:
        guard_bit = guards & -guards
        guards ^= guard_bit
        guard = guard_bit.bit_length() - 1
        dominated |= adj[guard]
    return dominated == (1 << len(adj)) - 1


def has_eternal_family(adj: tuple[int, ...], guard_count: int) -> bool:
    order = len(adj)
    live = {
        sum(1 << vertex for vertex in configuration)
        for configuration in combinations(range(order), guard_count)
        if dominates(adj, sum(1 << vertex for vertex in configuration))
    }
    changed = True
    while changed and live:
        changed = False
        rejected = set()
        for configuration in live:
            for attacked in range(order):
                attacked_bit = 1 << attacked
                if configuration & attacked_bit:
                    continue
                responders = configuration & adj[attacked]
                legal = False
                while responders:
                    guard_bit = responders & -responders
                    responders ^= guard_bit
                    successor = (configuration ^ guard_bit) | attacked_bit
                    if successor in live:
                        legal = True
                        break
                if not legal:
                    rejected.add(configuration)
                    break
        if rejected:
            live.difference_update(rejected)
            changed = True
    return bool(live)


def eternal_number(adj: tuple[int, ...]) -> int:
    for guard_count in range(1, len(adj) + 1):
        if has_eternal_family(adj, guard_count):
            return guard_count
    raise AssertionError("the all-vertices configuration must be eternal")


def disjoint_union(*graphs: tuple[int, ...]) -> tuple[int, ...]:
    total_order = sum(len(graph) for graph in graphs)
    adj = [0] * total_order
    offset = 0
    for graph in graphs:
        for vertex, neighbors in enumerate(graph):
            adj[offset + vertex] = neighbors << offset
        offset += len(graph)
    return tuple(adj)


def main() -> None:
    print("EXHAUSTIVE_FIXED_INDUCED_C5")
    print("r variable_edges graphs p3 p3_with_hub p3_and_connected_complement")
    for row in exhaustive_c5_boundary():
        print(*row)

    print("CONNECTEDNESS_BOUNDARY")
    for outside_order in (2, 3):
        adj_h = complete_join_cycle(5, outside_order)
        p3 = has_p3(adj_h)
        complement_connected = connected(complement(adj_h))
        print(
            f"K{outside_order}_join_C5 p3={str(p3).lower()} "
            f"complement_connected={str(complement_connected).lower()}"
        )
        assert p3
        assert not complement_connected

    print("ONE_GUARD_VALUES")
    for order in (5, 7, 9, 11):
        cycle = cycle_graph(order)
        anti_cycle = complement(cycle)
        cycle_value = eternal_number(cycle)
        anti_cycle_value = eternal_number(anti_cycle)
        print(
            f"order={order} cycle={cycle_value} "
            f"complement_cycle={anti_cycle_value}"
        )
        assert cycle_value == (order + 1) // 2
        assert anti_cycle_value == 3

    audited_subgraph = disjoint_union(
        (0,),
        (0,),
        complement(cycle_graph(9)),
    )
    audited_value = eternal_number(audited_subgraph)
    print(f"two_isolates_union_complement_C9={audited_value}")
    assert audited_value == 5
    print("VERDICT PASS")


if __name__ == "__main__":
    main()
