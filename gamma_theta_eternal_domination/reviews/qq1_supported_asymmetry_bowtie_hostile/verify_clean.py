#!/usr/bin/env python3
"""Clean-room audit for the supported asymmetric-edge bow-tie theorem.

Only the Python standard library is used.  Graphs are immutable neighbor
sets and guard configurations are frozensets, unlike the candidate's bit-mask
transition implementation.
"""

from __future__ import annotations

import hashlib
import itertools
import json


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def graph_from_code(order: int, code: int) -> tuple[frozenset[int], ...]:
    rows = [set() for _ in range(order)]
    for index, (left, right) in enumerate(itertools.combinations(range(order), 2)):
        if code >> index & 1:
            rows[left].add(right)
            rows[right].add(left)
    return tuple(frozenset(row) for row in rows)


def decode_graph6(record: str) -> tuple[frozenset[int], ...]:
    words = [ord(character) - 63 for character in record]
    demand(words and 0 <= words[0] <= 62, "small graph6 header required")
    order = words[0]
    stream = [
        (word >> shift) & 1
        for word in words[1:]
        for shift in range(5, -1, -1)
    ]
    required = order * (order - 1) // 2
    demand(len(stream) >= required, "truncated graph6")
    demand(all(bit == 0 for bit in stream[required:]), "nonzero graph6 padding")
    rows = [set() for _ in range(order)]
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if stream[cursor]:
                rows[left].add(right)
                rows[right].add(left)
            cursor += 1
    return tuple(frozenset(row) for row in rows)


def encode_graph6(graph: tuple[frozenset[int], ...]) -> str:
    order = len(graph)
    demand(order <= 62, "small graph6 only")
    stream = [
        int(right in graph[left])
        for right in range(1, order)
        for left in range(right)
    ]
    stream.extend([0] * (-len(stream) % 6))
    payload = []
    for offset in range(0, len(stream), 6):
        value = 0
        for bit in stream[offset : offset + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def states(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield frozenset(choice)


def independent(graph, state: frozenset[int]) -> bool:
    return all(not (graph[vertex] & state) for vertex in state)


def dominates(graph, state: frozenset[int]) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def successors(graph, state: frozenset[int], attack: int):
    demand(attack not in state, f"occupied attack {attack} from {sorted(state)}")
    for guard in sorted(state):
        if attack in graph[guard]:
            yield guard, state.difference({guard}).union({attack})


def eternal(graph, family: set[frozenset[int]]) -> bool:
    if not family or not all(dominates(graph, state) for state in family):
        return False
    return all(
        any(endpoint in family for _, endpoint in successors(graph, state, attack))
        for state in family
        for attack in range(len(graph))
        if attack not in state
    )


def greatest_family(graph, size: int) -> set[frozenset[int]]:
    alive = {
        state for state in states(len(graph), size) if dominates(graph, state)
    }
    while True:
        deleted = {
            state
            for state in alive
            if any(
                not any(
                    endpoint in alive
                    for _, endpoint in successors(graph, state, attack)
                )
                for attack in range(len(graph))
                if attack not in state
            )
        }
        if not deleted:
            return alive
        alive.difference_update(deleted)


def missed_by_pair(graph, left: int, right: int) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex not in (left, right)
        and vertex not in graph[left]
        and vertex not in graph[right]
    )


def clique(graph, members) -> bool:
    return all(
        right in graph[left]
        for left, right in itertools.combinations(tuple(members), 2)
    )


def active(graph, family, source: int, target: int) -> bool:
    if target not in graph[source]:
        return False
    return any(
        source in state
        and target not in state
        and independent(graph, state)
        and state.difference({source}).union({target}) in family
        for state in family
    )


def supported(family, left: int, right: int) -> bool:
    return any(left in state and right in state for state in family)


def specific_activity(graph, family, state, mover: int, target: int, endpoint) -> None:
    demand(independent(graph, state), "activity source is not independent")
    demand(state in family, "activity source is not retained")
    demand(mover in state and target not in state, "activity occupancy failure")
    demand(target in graph[mover], "activity mover edge absent")
    demand(state.difference({mover}).union({target}) == endpoint, "wrong activity endpoint")
    demand(endpoint in family, "activity endpoint is not retained")


def retained_fan(graph, family, left: int, right: int) -> bool:
    witnesses = missed_by_pair(graph, left, right)
    return bool(witnesses) and all(
        frozenset((left, right, witness)) in family for witness in witnesses
    )


def audit_bowtie(graph, family, u: int, x: int) -> dict[str, int]:
    demand(x in graph[u], "ux is not an edge")
    demand(supported(family, u, x), "ux is not family-supported")
    demand(active(graph, family, u, x), "u-to-x activity absent")
    demand(not active(graph, family, x, u), "x-to-u activity present")
    counts = {"orientations": 1, "ux_witnesses": 0, "mixed_cells": 0}
    Z = missed_by_pair(graph, u, x)
    demand(Z and clique(graph, Z), "bad nonempty Z clique")
    for z in Z:
        R = frozenset((u, x, z))
        demand(R in family, "supported ux central state omitted")
        P = missed_by_pair(graph, u, z)
        Q = missed_by_pair(graph, x, z)
        demand(P and Q, "empty bow-tie side")
        demand(set(P).isdisjoint(Q), "bow-tie sides overlap")
        demand(clique(graph, P) and clique(graph, Q), "side is not a clique")
        demand(clique(graph, tuple(P) + tuple(Q)), "bow-tie union is not a clique")
        counts["ux_witnesses"] += 1
        for g in P:
            S = frozenset((u, z, g))
            X = frozenset((x, z, g))
            demand(independent(graph, S) and S in family, "bad P source")
            demand(X in family, "transported X state omitted")
            demand(g in graph[x], "xg edge absent")
            demand(active(graph, family, x, g), "x-to-g activity absent")
            demand(active(graph, family, g, x), "g-to-x activity absent")
            demand(retained_fan(graph, family, x, g), "xg fan not retained")
            for h in Q:
                T = frozenset((x, z, h))
                O = frozenset((u, z, h))
                M = frozenset((z, g, h))
                demand(g != h and h not in S, "mixed-state collision")
                demand(independent(graph, T) and T in family, "bad Q source")
                demand(O not in family, "opposite central state retained")
                demand(h in graph[u] and h in graph[g], "spoke/cross edge absent")
                eligible = [(guard, endpoint) for guard, endpoint in successors(graph, S, h)]
                demand(
                    [guard for guard, _ in eligible] == sorted((u, g)),
                    "wrong physical responders at the mixed-state attack",
                )
                endpoint_by_guard = {guard: endpoint for guard, endpoint in eligible}
                demand(endpoint_by_guard[g] == O, "wrong g-to-h endpoint")
                demand(endpoint_by_guard[u] == M, "wrong u-to-h endpoint")
                demand(M in family, "mixed state omitted")
                specific_activity(graph, family, S, u, h, M)
                specific_activity(graph, family, T, h, u, R)
                specific_activity(graph, family, T, x, g, M)
                specific_activity(graph, family, S, g, x, R)
                demand(active(graph, family, u, h), "u-to-h activity absent")
                demand(active(graph, family, h, u), "h-to-u activity absent")
                demand(
                    all(
                        frozenset((u, h, e)) not in family
                        for e in missed_by_pair(graph, u, h)
                    ),
                    "uh fan not uniformly omitted",
                )
                demand(retained_fan(graph, family, g, h), "gh fan not retained")
                counts["mixed_cells"] += 1
    return counts


def static_equality_three(graph) -> bool:
    order = len(graph)
    gamma_three = (
        not any(dominates(graph, state) for state in states(order, 2))
        and any(dominates(graph, state) for state in states(order, 3))
    )
    alpha_three = (
        any(independent(graph, state) for state in states(order, 3))
        and not any(independent(graph, state) for state in states(order, 4))
    )
    return gamma_three and alpha_three


def arbitrary_family_census() -> dict:
    examined = 0
    applicable_graphs = set()
    applicable_families = 0
    totals = {"orientations": 0, "ux_witnesses": 0, "mixed_cells": 0}
    for order in range(3, 6):
        edge_count = order * (order - 1) // 2
        for code in range(1 << edge_count):
            examined += 1
            graph = graph_from_code(order, code)
            if not static_equality_three(graph):
                continue
            dominating_triples = tuple(
                state for state in states(order, 3) if dominates(graph, state)
            )
            for selector in range(1, 1 << len(dominating_triples)):
                family = {
                    state
                    for index, state in enumerate(dominating_triples)
                    if selector >> index & 1
                }
                if not eternal(graph, family):
                    continue
                applicable_families += 1
                applicable_graphs.add((order, code))
                for u in range(order):
                    for x in graph[u]:
                        if (
                            supported(family, u, x)
                            and active(graph, family, u, x)
                            and not active(graph, family, x, u)
                        ):
                            result = audit_bowtie(graph, family, u, x)
                            for key, value in result.items():
                                totals[key] += value
    demand(examined == 1096, "wrong labeled graph coverage")
    demand(len(applicable_graphs) == 107, "wrong applicable graph count")
    demand(applicable_families == 197, "wrong arbitrary-family count")
    demand(totals == {"orientations": 120, "ux_witnesses": 120, "mixed_cells": 120}, "census mismatch")
    return {
        "orders": [3, 4, 5],
        "labeled_graphs": examined,
        "applicable_graphs": len(applicable_graphs),
        "applicable_eternal_families": applicable_families,
        "theorem_obligations": totals,
    }


def minimum_size(graph, predicate) -> int:
    for size in range(1, len(graph) + 1):
        if any(predicate(state) for state in states(len(graph), size)):
            return size
    raise AssertionError("minimum not found")


def maximum_independent_size(graph) -> int:
    for size in range(len(graph), -1, -1):
        if any(independent(graph, state) for state in states(len(graph), size)):
            return size
    raise AssertionError("alpha not found")


def clique_cover_number(graph) -> tuple[int, list[list[int]]]:
    order = len(graph)
    for count in range(1, order + 1):
        parts: list[list[int]] = [[] for _ in range(count)]

        def extend(vertex: int, used: int) -> bool:
            if vertex == order:
                return True
            for part in range(min(count, used + 1)):
                if all(member in graph[vertex] for member in parts[part]):
                    parts[part].append(vertex)
                    if extend(vertex + 1, max(used, part + 1)):
                        return True
                    parts[part].pop()
            return False

        if extend(0, 0):
            return count, [part[:] for part in parts if part]
    raise AssertionError("theta not found")


def parameter_vector(graph) -> tuple[tuple[int, int, int, int, int], list[list[int]]]:
    gamma = minimum_size(graph, lambda state: dominates(graph, state))
    ind_dom = minimum_size(
        graph, lambda state: independent(graph, state) and dominates(graph, state)
    )
    alpha = maximum_independent_size(graph)
    eternal_number = next(
        size for size in range(1, len(graph) + 1) if greatest_family(graph, size)
    )
    theta, partition = clique_cover_number(graph)
    return (gamma, ind_dom, alpha, eternal_number, theta), partition


def equality_control() -> dict:
    record = "D]?"
    graph = decode_graph6(record)
    demand(encode_graph6(graph) == record, "D]? round trip")
    family = {
        frozenset(state)
        for state in ((0, 1, 4), (0, 2, 4), (0, 3, 4), (1, 2, 4), (2, 3, 4))
    }
    demand(eternal(graph, family), "D]? specified family is not eternal")
    parameters, partition = parameter_vector(graph)
    demand(parameters == (3, 3, 3, 3, 3), "D]? parameter mismatch")
    counts = audit_bowtie(graph, family, 1, 2)
    demand(missed_by_pair(graph, 1, 2) == (4,), "D]? wrong Z")
    demand(missed_by_pair(graph, 1, 4) == (0,), "D]? wrong P")
    demand(missed_by_pair(graph, 2, 4) == (3,), "D]? wrong Q")
    return {
        "graph6": record,
        "parameters": list(parameters),
        "clique_partition": partition,
        "family": [sorted(state) for state in sorted(family, key=lambda row: tuple(sorted(row)))],
        "orientation": [1, 2],
        "Z": [4],
        "P": [0],
        "Q": [3],
        "audit_counts": counts,
    }


def gamma_two_boundary() -> dict:
    record = r"QslallyN\~Y^v^|^z~~V|ve~^}G"
    graph = decode_graph6(record)
    demand(encode_graph6(graph) == record, "order-18 graph6 round trip")
    demand(len(graph) == 18, "boundary order")
    size = sum(len(row) for row in graph) // 2
    demand(size == 114, "boundary edge count")
    parameters, partition = parameter_vector(graph)
    demand(parameters == (2, 3, 3, 3, 3), "boundary parameters")
    family = greatest_family(graph, 3)
    demand(len(family) == 473, "boundary greatest-family size")
    u, x, r, d, w, z = 0, 1, 4, 7, 8, 9
    demand(missed_by_pair(graph, x, r) == (d,), "boundary C_xr")
    demand(missed_by_pair(graph, u, x) == (z,), "boundary W_ux")
    demand(missed_by_pair(graph, u, d) == (w,), "boundary W_ud")
    demand(frozenset((u, x, d)) in family, "boundary support state")
    demand(frozenset((u, w, z)) in family, "boundary C-167 bridge")
    demand(w in graph[x] and z in graph[w], "boundary hot edges")
    demand(missed_by_pair(graph, w, z) == (u,), "boundary W_wz")
    counts = audit_bowtie(graph, family, u, x)
    dominating_pairs = [
        sorted(state) for state in states(len(graph), 2) if dominates(graph, state)
    ]
    demand(len(dominating_pairs) == 30, "boundary dominating-pair count")
    return {
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "order": len(graph),
        "size": size,
        "parameters": list(parameters),
        "clique_partition": partition,
        "greatest_triple_family_size": len(family),
        "orientation": [u, x],
        "C_xr": [d],
        "Z": [z],
        "P": list(missed_by_pair(graph, u, z)),
        "Q": list(missed_by_pair(graph, x, z)),
        "W_ud": [w],
        "W_wz": [u],
        "dominating_pair_count": len(dominating_pairs),
        "audit_counts": counts,
    }


def main() -> None:
    result = {
        "verdict": "PASS",
        "arbitrary_family_census": arbitrary_family_census(),
        "equality_control": equality_control(),
        "gamma_two_boundary": gamma_two_boundary(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
