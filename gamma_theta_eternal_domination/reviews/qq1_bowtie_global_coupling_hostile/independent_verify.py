#!/usr/bin/env python3
"""Clean-room audit of the QQ1 global-coupling candidate.

The implementation deliberately uses frozenset states and immutable neighbor
sets.  It shares neither bitsets nor transition code with the candidate.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter


def demand(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def graph_from_integer(order: int, code: int) -> tuple[frozenset[int], ...]:
    neighbors = [set() for _ in range(order)]
    bit = 0
    for left in range(order):
        for right in range(left + 1, order):
            if code & (1 << bit):
                neighbors[left].add(right)
                neighbors[right].add(left)
            bit += 1
    return tuple(frozenset(row) for row in neighbors)


def graph6(record: str) -> tuple[frozenset[int], ...]:
    raw = [ord(character) - 63 for character in record]
    demand(raw and 0 <= raw[0] < 63, "only short graph6 is supported")
    order = raw[0]
    stream = "".join(f"{value:06b}" for value in raw[1:])
    neighbors = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if stream[cursor] == "1":
                neighbors[low].add(high)
                neighbors[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in neighbors)


def states(order: int, size: int) -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(choice)
        for choice in itertools.combinations(range(order), size)
    )


def is_independent(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    return all(graph[vertex].isdisjoint(state) for vertex in state)


def dominates(
    graph: tuple[frozenset[int], ...], state: frozenset[int]
) -> bool:
    covered = set(state)
    for vertex in state:
        covered.update(graph[vertex])
    return len(covered) == len(graph)


def successors(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    source: frozenset[int],
    attack: int,
) -> tuple[tuple[int, frozenset[int]], ...]:
    return tuple(
        (guard, (source - {guard}) | {attack})
        for guard in sorted(source)
        if attack in graph[guard]
        and (source - {guard}) | {attack} in family
    )


def greatest_family(
    graph: tuple[frozenset[int], ...], size: int
) -> set[frozenset[int]]:
    family = {
        state
        for state in states(len(graph), size)
        if dominates(graph, state)
    }
    while True:
        survivors = {
            source
            for source in family
            if all(
                successors(graph, family, source, attack)
                for attack in range(len(graph))
                if attack not in source
            )
        }
        if survivors == family:
            return survivors
        family = survivors


def eternal(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
) -> bool:
    return bool(family) and all(
        dominates(graph, source)
        and all(
            successors(graph, family, source, attack)
            for attack in range(len(graph))
            if attack not in source
        )
        for source in family
    )


def missed_pair(
    graph: tuple[frozenset[int], ...], left: int, right: int
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (left, right)
        and vertex not in graph[left]
        and vertex not in graph[right]
    )


def is_clique(
    graph: tuple[frozenset[int], ...], vertices
) -> bool:
    vertex_tuple = tuple(vertices)
    return all(
        right in graph[left]
        for left, right in itertools.combinations(vertex_tuple, 2)
    )


def active(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    mover: int,
    target: int,
) -> bool:
    if target not in graph[mover]:
        return False
    return any(
        mover in source
        and target not in source
        and is_independent(graph, source)
        and (source - {mover}) | {target} in family
        for source in family
    )


def exact_static_three(graph: tuple[frozenset[int], ...]) -> bool:
    order = len(graph)
    pairs = states(order, 2)
    triples = states(order, 3)
    return (
        not any(dominates(graph, pair) for pair in pairs)
        and any(dominates(graph, triple) for triple in triples)
        and any(is_independent(graph, triple) for triple in triples)
        and not any(
            is_independent(graph, four)
            for four in states(order, 4)
        )
    )


def minimum_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(state) for state in states(order, size)):
            return size
    raise AssertionError("minimum does not exist")


def parameter_vector(
    graph: tuple[frozenset[int], ...]
) -> tuple[int, int, int, int, int]:
    order = len(graph)
    gamma = minimum_size(order, lambda state: dominates(graph, state))
    independent_domination = minimum_size(
        order,
        lambda state: is_independent(graph, state)
        and dominates(graph, state),
    )
    alpha = max(
        size
        for size in range(1, order + 1)
        if any(
            is_independent(graph, state)
            for state in states(order, size)
        )
    )
    eternal_number = next(
        size
        for size in range(1, order + 1)
        if greatest_family(graph, size)
    )
    parts: list[list[int]] = []

    def colorable(vertex: int, limit: int) -> bool:
        if vertex == order:
            return True
        for index in range(min(len(parts) + 1, limit)):
            if index == len(parts):
                parts.append([])
            if all(other in graph[vertex] for other in parts[index]):
                parts[index].append(vertex)
                if colorable(vertex + 1, limit):
                    return True
                parts[index].pop()
            if not parts[index]:
                parts.pop()
                break
        return False

    theta = next(limit for limit in range(1, order + 1) if colorable(0, limit))
    return gamma, independent_domination, alpha, eternal_number, theta


def check_supported_fan(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    left: int,
    right: int,
) -> int:
    witnesses = missed_pair(graph, left, right)
    demand(is_clique(graph, witnesses), ("fan not clique", left, right))
    for witness in witnesses:
        demand(
            frozenset((left, right, witness)) in family,
            ("fan state omitted", left, right, witness),
        )
    return len(witnesses)


def audit_transport(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    u: int,
    x: int,
    r: int,
    completion: tuple[int, ...],
    fibers: dict[int, tuple[int, ...]],
) -> Counter:
    out = Counter()
    hot = frozenset(
        witness
        for fiber in fibers.values()
        for witness in fiber
    )
    demand(hot, "empty hot union")
    demand(hot.isdisjoint(completion), "hot/completion collision")

    for left, right in itertools.combinations(completion, 2):
        demand(right in graph[left], "completion not a clique")
        demand(
            x in missed_pair(graph, left, right)
            and r in missed_pair(graph, left, right),
            "blocker pair missing",
        )
        demand(r not in graph[x], "blockers are adjacent")
        demand(
            not any({left, right} <= source for source in family),
            ("retained completion pair", left, right),
        )
        out["forbidden_completion_pairs"] += 1

    for d in completion:
        for witness in hot:
            source = frozenset((u, d, witness))
            demand(len(source) == 3, "product state collision")
            demand(source in family, ("missing product", d, witness))
            out["product_incidences"] += 1
            for target in completion:
                if target == d:
                    continue
                retained = successors(graph, family, source, target)
                demand(
                    retained
                    == ((d, frozenset((u, target, witness))),),
                    ("transport is not uniquely retained", source, target),
                )
                out["unique_transport_attacks"] += 1

    demand(is_clique(graph, hot), "global hot union is not a clique")
    out["instances"] += 1
    out["multi_C"] += len(completion) >= 2
    out["multi_H"] += len(hot) >= 2
    return out


def audit_polarized_cell(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    u: int,
    x: int,
    z: int,
    w: int,
) -> Counter:
    out = Counter()
    demand(w not in graph[z], "polarized cell is an edge")
    p_side = missed_pair(graph, u, z)
    q_side = missed_pair(graph, x, z)
    demand(w in p_side, "hot vertex absent from P_z")
    demand(p_side and q_side, "empty bow-tie side")
    demand(set(p_side).isdisjoint(q_side), "bow-tie sides overlap")
    demand(is_clique(graph, p_side), "P_z not clique")
    demand(is_clique(graph, q_side), "Q_z not clique")
    demand(
        is_clique(graph, set(p_side) | set(q_side)),
        "P_z and Q_z not completely joined",
    )
    demand(active(graph, family, x, w), "x-to-w activity absent")
    demand(active(graph, family, w, x), "w-to-x activity absent")
    demand(
        frozenset((u, z, w)) in family
        and frozenset((x, z, w)) in family,
        "base bow-tie states absent",
    )
    for h in q_side:
        retained = frozenset((z, w, h))
        omitted = frozenset((u, z, h))
        demand(retained in family, ("mixed state absent", h))
        demand(omitted not in family, ("omitted fan state retained", h))
        demand(frozenset((x, z, h)) in family, "independent Q state absent")
        demand(active(graph, family, u, h), "u-to-h activity absent")
        demand(active(graph, family, h, u), "h-to-u activity absent")
        for e in missed_pair(graph, u, h):
            demand(
                frozenset((u, h, e)) not in family,
                ("omitted uh fan has retained member", u, h, e),
            )
        check_supported_fan(graph, family, x, w)
        check_supported_fan(graph, family, w, h)
        out["polarized_mixed_obligations"] += 1
    out["polarized_cells"] += 1
    return out


def audit_matrix_when_applicable(
    graph: tuple[frozenset[int], ...],
    family: set[frozenset[int]],
    u: int,
    x: int,
    r: int,
    completion: tuple[int, ...],
    fibers: dict[int, tuple[int, ...]],
) -> Counter:
    out = Counter()
    hot = frozenset(
        witness
        for fiber in fibers.values()
        for witness in fiber
    )
    central = missed_pair(graph, u, x)
    if not (
        central
        and active(graph, family, u, x)
        and not active(graph, family, x, u)
        and all(frozenset((u, x, d)) in family for d in completion)
        and all(
            frozenset((u, w, z)) in family
            for w in hot
            for z in central
        )
    ):
        return out

    demand(
        is_clique(graph, set(completion) | set(central)),
        "C union Z is not a clique",
    )
    demand(hot.isdisjoint(set(completion) | set(central)), "H overlap")
    demand(
        all(w not in graph[u] for w in hot)
        and all(z not in graph[u] for z in central),
        "u hits H or Z",
    )
    demand(
        all(w in graph[x] and w in graph[r] for w in hot),
        "x or r misses H",
    )
    demand(
        all(d not in graph[x] for d in completion)
        and all(z not in graph[x] for z in central),
        "x hits C or Z",
    )

    out["canonical_matrix_applications"] += 1
    for w in hot:
        for z in central:
            out["canonical_HZ_cells"] += 1
            if z in graph[w]:
                demand(frozenset((u, w, z)) in family, "bridge absent")
                demand(u in missed_pair(graph, w, z), "u absent from fan")
                check_supported_fan(graph, family, w, z)
                out["canonical_HZ_edges"] += 1
            else:
                out.update(audit_polarized_cell(graph, family, u, x, z, w))
                out["canonical_HZ_nonedges"] += 1
    return out


def exhaustive_census() -> dict[str, object]:
    totals = Counter()
    by_order: dict[str, dict[str, int]] = {}
    for order in range(3, 7):
        count = Counter()
        for code in range(1 << (order * (order - 1) // 2)):
            count["labeled_graphs"] += 1
            graph = graph_from_integer(order, code)
            if not exact_static_three(graph):
                continue
            family = greatest_family(graph, 3)
            if not family:
                continue
            count["equality_graphs"] += 1
            for x in range(order):
                for r in range(order):
                    if x == r or r in graph[x]:
                        continue
                    completion = missed_pair(graph, x, r)
                    if not completion or not is_clique(graph, completion):
                        continue
                    for u in range(order):
                        if (
                            u in (x, r)
                            or x not in graph[u]
                            or r not in graph[u]
                        ):
                            continue
                        fibers = {
                            d: missed_pair(graph, u, d)
                            for d in completion
                        }
                        if not all(fibers.values()):
                            continue
                        if not all(
                            frozenset((u, d, w)) in family
                            for d in completion
                            for w in fibers[d]
                        ):
                            continue
                        count.update(
                            audit_transport(
                                graph,
                                family,
                                u,
                                x,
                                r,
                                completion,
                                fibers,
                            )
                        )
                        count.update(
                            audit_matrix_when_applicable(
                                graph,
                                family,
                                u,
                                x,
                                r,
                                completion,
                                fibers,
                            )
                        )
        by_order[str(order)] = dict(sorted(count.items()))
        totals.update(count)
    return {
        "by_order": by_order,
        "totals": dict(sorted(totals.items())),
    }


def transport_control() -> dict[str, object]:
    graph = graph6("FCQe_")
    family = greatest_family(graph, 3)
    demand(parameter_vector(graph) == (3, 3, 3, 3, 3), "control params")
    demand(len(family) == 12, "control family size")
    u, x, r = 5, 0, 2
    completion = missed_pair(graph, x, r)
    fibers = {d: missed_pair(graph, u, d) for d in completion}
    demand(completion == (1, 4), "control completion")
    demand(fibers == {1: (3,), 4: (3, 6)}, "control fibers")
    audit = audit_transport(
        graph, family, u, x, r, completion, fibers
    )
    demand(frozenset((5, 1, 6)) in family, "transported state absent")
    hot = sorted({w for fiber in fibers.values() for w in fiber})
    central = missed_pair(graph, u, x)
    edge_cells = 0
    nonedge_cells = 0
    for w in hot:
        for z in central:
            demand(frozenset((u, w, z)) in family, "control bridge absent")
            if z in graph[w]:
                check_supported_fan(graph, family, w, z)
                edge_cells += 1
            else:
                nonedge_cells += 1
    demand(
        not active(graph, family, u, x)
        and not active(graph, family, x, u),
        "control unexpectedly polarized",
    )
    return {
        "graph6": "FCQe_",
        "parameters": [3, 3, 3, 3, 3],
        "greatest_family_size": len(family),
        "u_x_r": [u, x, r],
        "C": list(completion),
        "H": hot,
        "Z": list(central),
        "fibers": {str(d): list(fibers[d]) for d in completion},
        "transported_nonseed_state": [5, 1, 6],
        "transport_audit": dict(sorted(audit.items())),
        "matrix_cells": {
            "edges_supported": edge_cells,
            "nonedges_not_polarized_without_asymmetry": nonedge_cells,
        },
        "activity_u_x": False,
        "activity_x_u": False,
    }


def polarized_control() -> dict[str, object]:
    graph = graph6("D]?")
    family = {
        frozenset(state)
        for state in (
            (0, 1, 4),
            (0, 2, 4),
            (0, 3, 4),
            (1, 2, 4),
            (2, 3, 4),
        )
    }
    demand(eternal(graph, family), "polarized family is not eternal")
    demand(parameter_vector(graph) == (3, 3, 3, 3, 3), "polarized params")
    demand(active(graph, family, 1, 2), "forward activity absent")
    demand(not active(graph, family, 2, 1), "reverse activity present")
    audit = audit_polarized_cell(graph, family, 1, 2, 4, 0)
    return {
        "graph6": "D]?",
        "parameters": [3, 3, 3, 3, 3],
        "family_size": len(family),
        "orientation": [1, 2],
        "Z": list(missed_pair(graph, 1, 2)),
        "P": list(missed_pair(graph, 1, 4)),
        "Q": list(missed_pair(graph, 2, 4)),
        "audit": dict(sorted(audit.items())),
    }


def main() -> None:
    print(
        json.dumps(
            {
                "schema": "qq1-global-coupling-hostile-clean-v1",
                "verdict": "THEOREMS_PASS_AUDIT_SCOPE_DEFECT",
                "model": (
                    "one adjacent guard moves to an unoccupied attack; "
                    "the endpoint stays in the same family"
                ),
                "census": exhaustive_census(),
                "transport_control": transport_control(),
                "polarized_control": polarized_control(),
                "scope_defect": (
                    "The candidate census counts nonedge H-by-Z cells "
                    "without requiring u->x asymmetry and without checking "
                    "any C-177 bow-tie conclusion."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
