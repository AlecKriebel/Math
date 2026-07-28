#!/usr/bin/env python3
"""Discovery scan for unit-reachable response-2-CNF component returns.

Input is one short graph6 record per line.  For every connected graph with
gamma=alpha=gamma_infinity=3, the script computes the greatest eternal
triple-family.  At each independent reference triple having no empty or full
response list, it reconstructs the three frozen complement projections and
the exact response 2-CNF.  It then looks for a directed implication cycle
reachable from a genuine singleton unit.

The scan is a mechanism probe.  It is not used as a finite exclusion.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import sys


def iter_bits(mask: int):
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit


def decode_graph6(record: str) -> tuple[int, ...]:
    values = [ord(char) - 63 for char in record.strip()]
    if not values or not 0 <= values[0] <= 62:
        raise ValueError("only short graph6 records are supported")
    n = values[0]
    bits = [
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    ]
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        if adjacency[bit.bit_length() - 1] & scan:
            return False
    return True


def dominates(
    adjacency: tuple[int, ...], state: int, all_mask: int
) -> bool:
    covered = state
    for bit in iter_bits(state):
        covered |= adjacency[bit.bit_length() - 1]
    return covered == all_mask


def no_dominating_pair(adjacency: tuple[int, ...]) -> bool:
    n = len(adjacency)
    all_mask = (1 << n) - 1
    closed = tuple(adjacency[v] | (1 << v) for v in range(n))
    if any(mask == all_mask for mask in closed):
        return False
    return all(
        closed[u] | closed[v] != all_mask
        for u in range(n)
        for v in range(u + 1, n)
    )


def independent_triples_if_alpha_three(
    adjacency: tuple[int, ...],
) -> tuple[int, ...]:
    n = len(adjacency)
    triples = tuple(
        sum(1 << v for v in choice)
        for choice in itertools.combinations(range(n), 3)
        if independent(
            adjacency, sum(1 << v for v in choice)
        )
    )
    if not triples:
        return ()
    if any(
        independent(
            adjacency, sum(1 << v for v in choice)
        )
        for choice in itertools.combinations(range(n), 4)
    ):
        return ()
    return triples


def greatest_triple_family(adjacency: tuple[int, ...]) -> set[int]:
    n = len(adjacency)
    all_mask = (1 << n) - 1
    family = {
        sum(1 << v for v in choice)
        for choice in itertools.combinations(range(n), 3)
        if dominates(
            adjacency, sum(1 << v for v in choice), all_mask
        )
    }
    while True:
        removed = set()
        for state in family:
            for target_bit in iter_bits(all_mask ^ state):
                target = target_bit.bit_length() - 1
                movers = state & adjacency[target]
                if not any(
                    ((state ^ guard_bit) | target_bit) in family
                    for guard_bit in iter_bits(movers)
                ):
                    removed.add(state)
                    break
        if not removed:
            return family
        family.difference_update(removed)


def mask_vertices(mask: int) -> tuple[int, ...]:
    return tuple(v for v in range(mask.bit_length()) if mask >> v & 1)


def response_lists(
    adjacency: tuple[int, ...], family: set[int], reference: int
) -> dict[int, frozenset[int]]:
    n = len(adjacency)
    anchors = mask_vertices(reference)
    return {
        x: frozenset(
            a
            for a in anchors
            if adjacency[x] >> a & 1
            and ((reference ^ (1 << a)) | (1 << x)) in family
        )
        for x in range(n)
        if not (reference >> x & 1)
    }


def projection_components(
    adjacency: tuple[int, ...],
    anchors: tuple[int, int, int],
    lists: dict[int, frozenset[int]],
    frozen: int,
) -> tuple[dict[int, tuple[int | None, int]], list[dict[str, object]]]:
    n = len(adjacency)
    allowed = set(anchors) - {frozen}
    allowed.update(x for x, values in lists.items() if frozen not in values)
    component: dict[int, int] = {}
    parity: dict[int, int] = {}
    components: list[list[int]] = []
    all_mask = (1 << n) - 1
    for root in sorted(allowed):
        if root in component:
            continue
        index = len(components)
        component[root] = index
        parity[root] = 0
        queue = [root]
        vertices = []
        while queue:
            left = queue.pop()
            vertices.append(left)
            h_neighbors = (
                all_mask ^ adjacency[left] ^ (1 << left)
            )
            for right in sorted(allowed):
                if not (h_neighbors >> right & 1):
                    continue
                if right not in component:
                    component[right] = index
                    parity[right] = parity[left] ^ 1
                    queue.append(right)
                elif parity[right] == parity[left]:
                    raise AssertionError("frozen projection is not bipartite")
        components.append(sorted(vertices))
    remaining = sorted(set(anchors) - {frozen})
    anchor_index = component[remaining[0]]
    if component[remaining[1]] != anchor_index:
        raise AssertionError("anchor edge split across components")
    if parity[remaining[0]]:
        for vertex in components[anchor_index]:
            parity[vertex] ^= 1
    variables = []
    variable_of_component: dict[int, int | None] = {}
    for index, vertices in enumerate(components):
        if index == anchor_index:
            variable_of_component[index] = None
        else:
            variable_of_component[index] = -1
            variables.append(
                {
                    "frozen": frozen,
                    "vertices": vertices,
                    "component_index": index,
                }
            )
    data = {
        vertex: (variable_of_component[component[vertex]], parity[vertex])
        for vertex in allowed
    }
    return data, variables


def build_formula(
    adjacency: tuple[int, ...], family: set[int], reference: int
) -> dict[str, object] | None:
    anchors = mask_vertices(reference)
    lists = response_lists(adjacency, family, reference)
    if any(len(values) not in (1, 2) for values in lists.values()):
        return None
    projection_data: dict[tuple[int, int], tuple[int | None, int]] = {}
    variables: list[dict[str, object]] = []
    for frozen in anchors:
        data, local_variables = projection_components(
            adjacency, anchors, lists, frozen
        )
        local_to_global = {}
        for item in local_variables:
            global_id = len(variables)
            item["id"] = global_id
            variables.append(item)
            local_to_global[item["component_index"]] = global_id
        for vertex, (placeholder, parity) in data.items():
            if placeholder is None:
                projection_data[(frozen, vertex)] = (None, parity)
            else:
                component_index = next(
                    item["component_index"]
                    for item in local_variables
                    if vertex in item["vertices"]
                )
                projection_data[(frozen, vertex)] = (
                    local_to_global[component_index],
                    parity,
                )

    units = []
    fixed_failure = False
    for vertex, values in lists.items():
        if len(values) != 1:
            continue
        demanded = next(iter(values))
        for frozen in set(anchors) - {demanded}:
            variable, parity = projection_data[(frozen, vertex)]
            remaining = sorted(set(anchors) - {frozen})
            required = parity ^ remaining.index(demanded)
            if variable is None:
                fixed_failure |= bool(required)
            else:
                units.append(
                    {
                        "node": [variable, required],
                        "vertex": vertex,
                        "frozen": frozen,
                        "demanded": demanded,
                    }
                )

    clauses = []
    n = len(adjacency)
    for x, y in itertools.combinations(
        [v for v in range(n) if not (reference >> v & 1)], 2
    ):
        if adjacency[x] >> y & 1:
            continue
        if len(lists[x]) != 2 or len(lists[y]) != 2:
            continue
        omitted_x = next(iter(set(anchors) - set(lists[x])))
        omitted_y = next(iter(set(anchors) - set(lists[y])))
        if omitted_x == omitted_y:
            continue
        shared = next(iter(set(lists[x]) & set(lists[y])))
        variable_x, parity_x = projection_data[(omitted_x, x)]
        variable_y, parity_y = projection_data[(omitted_y, y)]
        remaining_x = sorted(set(anchors) - {omitted_x})
        remaining_y = sorted(set(anchors) - {omitted_y})
        forbidden_x = parity_x ^ remaining_x.index(shared)
        forbidden_y = parity_y ^ remaining_y.index(shared)
        clauses.append(
            {
                "edge": [x, y],
                "shared": shared,
                "left": [variable_x, forbidden_x],
                "right": [variable_y, forbidden_y],
            }
        )

    # Substitute fixed endpoints.  Only genuine free/free clauses create
    # the component-return mechanism inspected here.
    arcs: dict[tuple[int, int], list[tuple[tuple[int, int], int]]] = (
        collections.defaultdict(list)
    )
    derived_units = list(units)
    for index, clause in enumerate(clauses):
        left_variable, left_forbidden = clause["left"]
        right_variable, right_forbidden = clause["right"]
        if left_variable is None and right_variable is None:
            fixed_failure |= left_forbidden == 0 and right_forbidden == 0
        elif left_variable is None:
            if left_forbidden == 0:
                derived_units.append(
                    {
                        "node": [right_variable, 1 - right_forbidden],
                        "vertex": None,
                        "frozen": variables[right_variable]["frozen"],
                        "demanded": None,
                        "source_clause": index,
                    }
                )
        elif right_variable is None:
            if right_forbidden == 0:
                derived_units.append(
                    {
                        "node": [left_variable, 1 - left_forbidden],
                        "vertex": None,
                        "frozen": variables[left_variable]["frozen"],
                        "demanded": None,
                        "source_clause": index,
                    }
                )
        else:
            arcs[(left_variable, left_forbidden)].append(
                ((right_variable, 1 - right_forbidden), index)
            )
            arcs[(right_variable, right_forbidden)].append(
                ((left_variable, 1 - left_forbidden), index)
            )

    return {
        "anchors": list(anchors),
        "lists": {str(k): sorted(v) for k, v in lists.items()},
        "variables": variables,
        "units": units,
        "all_units": derived_units,
        "clauses": clauses,
        "arcs": arcs,
        "fixed_failure": fixed_failure,
    }


def first_reachable_cycle(formula: dict[str, object]):
    arcs = formula["arcs"]
    for unit in formula["units"]:
        start = tuple(unit["node"])
        queue = collections.deque([start])
        parent = {start: None}
        parent_clause = {}
        while queue:
            node = queue.popleft()
            for successor, clause_index in arcs.get(node, ()):
                if successor == start:
                    path = []
                    cursor = node
                    while cursor is not None:
                        path.append(cursor)
                        cursor = parent[cursor]
                    path.reverse()
                    path.append(start)
                    clauses = [
                        parent_clause[path[i]]
                        for i in range(1, len(path) - 1)
                    ] + [clause_index]
                    if len(clauses) >= 2:
                        return {
                            "unit": unit,
                            "literal_cycle": [list(item) for item in path],
                            "clause_indices": clauses,
                        }
                if successor not in parent:
                    parent[successor] = node
                    parent_clause[successor] = clause_index
                    queue.append(successor)
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-graphs", type=int)
    parser.add_argument("--stop-first", action="store_true")
    args = parser.parse_args()
    totals: collections.Counter[str] = collections.Counter()
    first = None
    for raw in sys.stdin:
        record = raw.strip()
        if not record or record.startswith(">"):
            continue
        if args.max_graphs and totals["graphs_read"] >= args.max_graphs:
            break
        totals["graphs_read"] += 1
        adjacency = decode_graph6(record)
        triples = independent_triples_if_alpha_three(adjacency)
        if not triples or not no_dominating_pair(adjacency):
            continue
        totals["static_equality_graphs"] += 1
        family = greatest_triple_family(adjacency)
        if not family:
            continue
        totals["eternal_equality_graphs"] += 1
        for reference in triples:
            totals["references"] += 1
            formula = build_formula(adjacency, family, reference)
            if formula is None:
                continue
            totals["no_full_references"] += 1
            if formula["units"]:
                totals["references_with_free_singleton_units"] += 1
            if formula["clauses"]:
                totals["references_with_cross_clauses"] += 1
            if formula["units"] and formula["clauses"]:
                totals["references_with_units_and_cross_clauses"] += 1
            cycle = first_reachable_cycle(formula)
            if cycle is None:
                continue
            totals["references_with_unit_reachable_cycle"] += 1
            if first is None:
                first = {
                    "graph6": record,
                    "reference": list(mask_vertices(reference)),
                    "family_size": len(family),
                    "formula": {
                        key: value
                        for key, value in formula.items()
                        if key != "arcs"
                    },
                    "cycle": cycle,
                }
                if args.stop_first:
                    break
        if args.stop_first and first is not None:
            break
    for key in (
        "references_with_free_singleton_units",
        "references_with_cross_clauses",
        "references_with_units_and_cross_clauses",
        "references_with_unit_reachable_cycle",
    ):
        totals[key] += 0
    print(
        json.dumps(
            {
                "schema": "fresh-component-chain-cycle-scan-v1",
                "classification": "OBSERVED_DISCOVERY_ONLY",
                "totals": dict(sorted(totals.items())),
                "first_unit_reachable_cycle": first,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
