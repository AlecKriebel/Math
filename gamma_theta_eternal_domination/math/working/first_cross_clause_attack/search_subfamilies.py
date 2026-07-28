#!/usr/bin/env python3
"""Capped discovery scan for one-clause unit cores in exact subfamilies.

For a fixed small graph and an independent reference triple, enumerate all
nonempty proper exact response-list assignments.  For each assignment take
the greatest one-guard-closed family among the dominating triples that obey
the prescribed negative direct swaps.  If all prescribed positive swaps
survive, this realizes the exact lists in an arbitrary eternal subfamily.

The scan then detects a two-singleton/one-cross-clause obstruction using the
actual frozen-projection components and their bipartition parities.  This is
discovery code, not a finite certificate.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product


def decode_graph6(record: str) -> tuple[int, list[int]]:
    data = record.strip().encode("ascii")
    if not data or data[0] >= 126:
        raise ValueError("only short graph6 is supported")
    n = data[0] - 63
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * n
    index = 0
    for high in range(1, n):
        for low in range(high):
            if bits[index]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            index += 1
    return n, adjacency


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(mask.bit_length()) if mask >> index & 1)


def dominates(state: int, adjacency: list[int], full: int) -> bool:
    covered = state
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        covered |= adjacency[bit.bit_length() - 1]
    return covered == full


def independent(state: int, adjacency: list[int]) -> bool:
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & scan:
            return False
    return True


def constrained_kernel(
    n: int,
    adjacency: list[int],
    forbidden: set[int],
) -> set[int]:
    full = (1 << n) - 1
    family = {
        sum(1 << vertex for vertex in triple)
        for triple in combinations(range(n), 3)
        if (state := sum(1 << vertex for vertex in triple)) not in forbidden
        and dominates(state, adjacency, full)
    }
    while True:
        bad = set()
        for state in family:
            for attacked in range(n):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                guards = state & adjacency[attacked]
                if not any(
                    ((state ^ bit) | attacked_bit) in family
                    for bit in (
                        1 << guard
                        for guard in range(n)
                        if guards >> guard & 1
                    )
                ):
                    bad.add(state)
                    break
        if not bad:
            return family
        family -= bad


def projection_data(
    n: int,
    adjacency: list[int],
    anchors: tuple[int, int, int],
    lists: dict[int, frozenset[int]],
    frozen: int,
) -> tuple[dict[int, int], dict[int, int], int]:
    retained = set(anchors) - {frozen}
    retained.update(vertex for vertex, values in lists.items() if frozen not in values)
    component: dict[int, int] = {}
    side: dict[int, int] = {}
    component_index = 0
    for root in sorted(retained):
        if root in component:
            continue
        component[root] = component_index
        side[root] = 0
        queue = [root]
        while queue:
            left = queue.pop()
            for right in retained:
                if right in component:
                    continue
                if adjacency[left] >> right & 1:
                    continue
                component[right] = component_index
                side[right] = side[left] ^ 1
                queue.append(right)
        component_index += 1
    anchor_component = component[next(vertex for vertex in anchors if vertex != frozen)]
    return component, side, anchor_component


def one_clause_cores(
    n: int,
    adjacency: list[int],
    anchors: tuple[int, int, int],
    lists: dict[int, frozenset[int]],
) -> list[dict[str, object]]:
    outside = [vertex for vertex in range(n) if vertex not in anchors]
    projections = {
        frozen: projection_data(n, adjacency, anchors, lists, frozen)
        for frozen in anchors
    }
    result = []
    for x, y in combinations(outside, 2):
        if adjacency[x] >> y & 1:
            continue
        if len(lists[x]) != 2 or len(lists[y]) != 2:
            continue
        omitted_x = next(iter(set(anchors) - set(lists[x])))
        omitted_y = next(iter(set(anchors) - set(lists[y])))
        if omitted_x == omitted_y:
            continue
        shared = set(lists[x]) & set(lists[y])
        if len(shared) != 1:
            continue
        color = next(iter(shared))
        comp_x, side_x, fixed_x = projections[omitted_x]
        comp_y, side_y, fixed_y = projections[omitted_y]
        if comp_x[x] == fixed_x or comp_y[y] == fixed_y:
            continue
        for pin_x in outside:
            if len(lists[pin_x]) != 1 or omitted_x in lists[pin_x]:
                continue
            if comp_x.get(pin_x) != comp_x[x]:
                continue
            forced_x = next(iter(lists[pin_x]))
            x_color = (
                forced_x
                if side_x[pin_x] == side_x[x]
                else next(iter(set(anchors) - {omitted_x, forced_x}))
            )
            if x_color != color:
                continue
            for pin_y in outside:
                if len(lists[pin_y]) != 1 or omitted_y in lists[pin_y]:
                    continue
                if comp_y.get(pin_y) != comp_y[y]:
                    continue
                forced_y = next(iter(lists[pin_y]))
                y_color = (
                    forced_y
                    if side_y[pin_y] == side_y[y]
                    else next(iter(set(anchors) - {omitted_y, forced_y}))
                )
                if y_color != color:
                    continue
                result.append(
                    {
                        "ports": [x, y],
                        "types": [omitted_x, omitted_y],
                        "shared_color": color,
                        "pins": [pin_x, pin_y],
                        "same_pin": pin_x == pin_y,
                        "pin_colors": [forced_x, forced_y],
                        "port_parities": [
                            side_x[pin_x] ^ side_x[x],
                            side_y[pin_y] ^ side_y[y],
                        ],
                    }
                )
    return result


def scan(record: str) -> None:
    n, adjacency = decode_graph6(record)
    full = (1 << n) - 1
    independent_triples = [
        triple
        for triple in combinations(range(n), 3)
        if independent(sum(1 << vertex for vertex in triple), adjacency)
        and dominates(
            sum(1 << vertex for vertex in triple), adjacency, full
        )
    ]
    assignments = 0
    realizations = 0
    for anchors in independent_triples:
        reference = sum(1 << vertex for vertex in anchors)
        outside = [vertex for vertex in range(n) if vertex not in anchors]
        choices = []
        for vertex in outside:
            graph_responses = [
                anchor for anchor in anchors if adjacency[vertex] >> anchor & 1
            ]
            values = [
                frozenset(subset)
                for size in (1, 2)
                for subset in combinations(graph_responses, size)
            ]
            choices.append(values)
        if any(not values for values in choices):
            continue
        for selected in product(*choices):
            assignments += 1
            lists = dict(zip(outside, selected, strict=True))
            forbidden = set()
            required = {reference}
            for vertex in outside:
                for anchor in anchors:
                    successor = (reference ^ (1 << anchor)) | (1 << vertex)
                    if anchor in lists[vertex]:
                        required.add(successor)
                    else:
                        forbidden.add(successor)
            family = constrained_kernel(n, adjacency, forbidden)
            if not required <= family:
                continue
            cores = one_clause_cores(n, adjacency, anchors, lists)
            if cores:
                realizations += 1
                print(
                    {
                        "graph6": record,
                        "reference": anchors,
                        "lists": {key: sorted(value) for key, value in lists.items()},
                        "family_size": len(family),
                        "cores": cores,
                    }
                )
                return
    print(
        {
            "graph6": record,
            "independent_references": len(independent_triples),
            "assignments": assignments,
            "realizations": realizations,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph6", nargs="+")
    args = parser.parse_args()
    for record in args.graph6:
        scan(record)


if __name__ == "__main__":
    main()
