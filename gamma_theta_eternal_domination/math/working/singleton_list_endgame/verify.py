#!/usr/bin/env python3
"""Independent verifier for the singleton-list endgame controls.

The verifier imports no campaign evaluator or search code.  It decodes the
two graph6 records, checks exact graph parameters, reconstructs the relevant
eternal families, checks every one-guard obligation, recomputes response
lists, and audits the claimed sealed caps and unpinned dynamic ports.
"""

from __future__ import annotations

import argparse
from collections import deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


Edge = tuple[int, int]
State = tuple[int, int, int]


def pair(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def decode_graph6(record: str) -> tuple[tuple[int, ...], set[Edge]]:
    raw = record.encode("ascii")
    if not raw or not 63 <= raw[0] <= 125:
        raise ValueError("only ordinary short graph6 is supported")
    order = raw[0] - 63
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(bits) < required:
        raise ValueError("truncated graph6")
    edges: set[Edge] = set()
    position = 0
    for high in range(1, order):
        for low in range(high):
            if bits[position]:
                edges.add((low, high))
            position += 1
    return tuple(range(order)), edges


def complement_edges(vertices: tuple[int, ...], edges: set[Edge]) -> set[Edge]:
    return {
        pair(u, v)
        for u, v in combinations(vertices, 2)
        if pair(u, v) not in edges
    }


def dominates(
    state: tuple[int, ...],
    vertices: tuple[int, ...],
    edges: set[Edge],
) -> bool:
    occupied = set(state)
    return all(
        vertex in occupied
        or any(pair(vertex, guard) in edges for guard in state)
        for vertex in vertices
    )


def independent(state: tuple[int, ...], edges: set[Edge]) -> bool:
    return all(pair(u, v) not in edges for u, v in combinations(state, 2))


def domination_number(vertices: tuple[int, ...], edges: set[Edge]) -> int:
    for size in range(1, len(vertices) + 1):
        if any(
            dominates(state, vertices, edges)
            for state in combinations(vertices, size)
        ):
            return size
    raise AssertionError("finite graph has no dominating set")


def independence_number(vertices: tuple[int, ...], edges: set[Edge]) -> int:
    for size in range(len(vertices), 0, -1):
        if any(
            independent(state, edges)
            for state in combinations(vertices, size)
        ):
            return size
    raise AssertionError("empty maximum independent set")


def independent_domination_number(
    vertices: tuple[int, ...],
    edges: set[Edge],
) -> int:
    for size in range(1, len(vertices) + 1):
        if any(
            independent(state, edges)
            and dominates(state, vertices, edges)
            for state in combinations(vertices, size)
        ):
            return size
    raise AssertionError("finite graph has no maximal independent set")


def chromatic_number(
    vertices: tuple[int, ...],
    h_edges: set[Edge],
) -> tuple[int, tuple[int, ...]]:
    neighbors = {
        vertex: {
            other
            for other in vertices
            if other != vertex and pair(vertex, other) in h_edges
        }
        for vertex in vertices
    }
    order = sorted(vertices, key=lambda x: (-len(neighbors[x]), x))
    for color_count in range(1, len(vertices) + 1):
        assignment: dict[int, int] = {}

        def visit(position: int) -> bool:
            if position == len(order):
                return True
            vertex = order[position]
            forbidden = {
                assignment[other]
                for other in neighbors[vertex]
                if other in assignment
            }
            for color in range(color_count):
                if color in forbidden:
                    continue
                assignment[vertex] = color
                if visit(position + 1):
                    return True
                del assignment[vertex]
            return False

        if visit(0):
            return color_count, tuple(assignment[x] for x in vertices)
    raise AssertionError("unreachable")


def greatest_triple_family(
    vertices: tuple[int, ...],
    edges: set[Edge],
) -> set[State]:
    family = {
        tuple(state)
        for state in combinations(vertices, 3)
        if dominates(state, vertices, edges)
    }
    while True:
        remove: set[State] = set()
        for state in family:
            occupied = set(state)
            for attacked in vertices:
                if attacked in occupied:
                    continue
                if not any(
                    pair(guard, attacked) in edges
                    and tuple(
                        sorted((occupied - {guard}) | {attacked})
                    )
                    in family
                    for guard in state
                ):
                    remove.add(state)
                    break
        if not remove:
            return family
        family -= remove


def verify_family(
    vertices: tuple[int, ...],
    edges: set[Edge],
    family: set[State],
) -> int:
    obligations = 0
    for state in family:
        if not dominates(state, vertices, edges):
            raise AssertionError(f"nondominating selected state {state}")
        occupied = set(state)
        for attacked in vertices:
            if attacked in occupied:
                continue
            obligations += 1
            if not any(
                pair(guard, attacked) in edges
                and tuple(sorted((occupied - {guard}) | {attacked}))
                in family
                for guard in state
            ):
                raise AssertionError(
                    f"failed one-guard obligation {state}, {attacked}"
                )
    return obligations


def response_lists(
    reference: tuple[int, int, int],
    vertices: tuple[int, ...],
    family: set[State],
) -> dict[int, tuple[int, ...]]:
    anchor = set(reference)
    return {
        vertex: tuple(
            responder
            for responder in reference
            if tuple(
                sorted((anchor - {responder}) | {vertex})
            )
            in family
        )
        for vertex in vertices
        if vertex not in anchor
    }


def list_colorings(
    reference: tuple[int, int, int],
    vertices: tuple[int, ...],
    h_edges: set[Edge],
    lists: dict[int, tuple[int, ...]],
) -> list[tuple[int, ...]]:
    outside = sorted(set(vertices) - set(reference), key=lambda x: (len(lists[x]), x))
    assignment: dict[int, int] = {}
    colorings: list[tuple[int, ...]] = []

    def visit(position: int) -> None:
        if position == len(outside):
            colorings.append(tuple(assignment[x] for x in outside))
            return
        vertex = outside[position]
        forbidden = {
            assignment[other]
            for other in assignment
            if pair(vertex, other) in h_edges
        }
        for color in lists[vertex]:
            if color in forbidden:
                continue
            assignment[vertex] = color
            visit(position + 1)
            del assignment[vertex]

    visit(0)
    return colorings


def components(
    subset: set[int],
    h_edges: set[Edge],
) -> list[tuple[int, ...]]:
    neighbors = {vertex: set() for vertex in subset}
    for u, v in h_edges:
        if u in subset and v in subset:
            neighbors[u].add(v)
            neighbors[v].add(u)
    seen: set[int] = set()
    output: list[tuple[int, ...]] = []
    for root in sorted(subset):
        if root in seen:
            continue
        seen.add(root)
        queue = deque([root])
        component: list[int] = []
        parity = {root: 0}
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for other in sorted(neighbors[vertex]):
                if other not in parity:
                    parity[other] = parity[vertex] ^ 1
                    seen.add(other)
                    queue.append(other)
                elif parity[other] == parity[vertex]:
                    raise AssertionError("frozen projection is not bipartite")
        output.append(tuple(sorted(component)))
    return output


def parameters(
    vertices: tuple[int, ...],
    edges: set[Edge],
    family: set[State],
) -> tuple[dict[str, int], tuple[int, ...]]:
    h_edges = complement_edges(vertices, edges)
    theta, coloring = chromatic_number(vertices, h_edges)
    alpha = independence_number(vertices, edges)
    if not family:
        raise AssertionError("missing eternal triple family")
    # alpha <= gamma_infinity and this explicit eternal triple family gives
    # gamma_infinity <= 3.
    if alpha != 3:
        raise AssertionError("control does not force gamma_infinity=3")
    return {
        "gamma": domination_number(vertices, edges),
        "i": independent_domination_number(vertices, edges),
        "alpha": alpha,
        "gamma_infinity": 3,
        "theta": theta,
    }, coloring


def expected_lists(raw: dict[str, list[int]]) -> dict[int, tuple[int, ...]]:
    return {
        int(vertex): tuple(values)
        for vertex, values in raw.items()
    }


def audit_sealed_buffer(data: dict[str, object]) -> dict[str, object]:
    record = str(data["graph6"])
    vertices, edges = decode_graph6(record)
    h_edges = complement_edges(vertices, edges)
    reference = tuple(int(x) for x in data["reference"])
    family = {
        tuple(int(x) for x in state)
        for state in data["selected_family"]
    }
    obligations = verify_family(vertices, edges, family)
    lists = response_lists(reference, vertices, family)
    if lists != expected_lists(data["expected_lists"]):
        raise AssertionError(f"sealed-control list mismatch: {lists}")
    result_parameters, coloring = parameters(vertices, edges, family)
    expected_parameters = {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if result_parameters != expected_parameters:
        raise AssertionError(f"sealed-control parameters: {result_parameters}")
    sealed_color = int(data["sealed_color"])
    positive = {
        vertex for vertex, response in lists.items()
        if sealed_color in response
    }
    sealed = {
        vertex
        for vertex in positive
        if not any(
            pair(vertex, other) in h_edges
            for other in positive - {vertex}
        )
    }
    expected_sealed = {
        int(x) for x in data["sealed_exact_two_vertices"]
    }
    if sealed != expected_sealed:
        raise AssertionError(f"sealed set mismatch: {sealed}")
    buffer_vertex = int(data["forced_singleton_buffer"])
    if lists[buffer_vertex] != (1,):
        raise AssertionError("buffer is not the expected singleton")
    for vertex in expected_sealed:
        if pair(vertex, buffer_vertex) not in h_edges:
            raise AssertionError("buffer misses a sealed exact-two vertex")
        if pair(2, buffer_vertex) not in h_edges:
            raise AssertionError("buffer misses the third anchor")
    list_solutions = list_colorings(reference, vertices, h_edges, lists)
    if len(list_solutions) != 1:
        raise AssertionError("unexpected sealed-control list-coloring count")
    return {
        "graph6": record,
        "order": len(vertices),
        "size": len(edges),
        "parameters": result_parameters,
        "family_size": len(family),
        "attack_obligations": obligations,
        "lists": {str(k): list(v) for k, v in lists.items()},
        "sealed_exact_two_vertices": sorted(sealed),
        "singleton_buffer": buffer_vertex,
        "list_coloring_count": len(list_solutions),
        "h_coloring": list(coloring),
    }


def audit_dynamic_free(data: dict[str, object]) -> dict[str, object]:
    record = str(data["graph6"])
    vertices, edges = decode_graph6(record)
    h_edges = complement_edges(vertices, edges)
    reference = tuple(int(x) for x in data["reference"])
    family = greatest_triple_family(vertices, edges)
    obligations = verify_family(vertices, edges, family)
    lists = response_lists(reference, vertices, family)
    if lists != expected_lists(data["expected_lists"]):
        raise AssertionError(f"dynamic-control list mismatch: {lists}")
    result_parameters, coloring = parameters(vertices, edges, family)
    expected_parameters = {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }
    if result_parameters != expected_parameters:
        raise AssertionError(f"dynamic-control parameters: {result_parameters}")

    dynamic_expected = {
        int(vertex): int(omitted)
        for vertex, omitted in data["dynamic_exact_two_ports"].items()
    }
    dynamic_found: dict[int, int] = {}
    anchor = set(reference)
    for vertex, response in lists.items():
        if len(response) != 2:
            continue
        omitted = next(iter(anchor - set(response)))
        if pair(vertex, omitted) in edges:
            dynamic_found[vertex] = omitted
    if dynamic_found != dynamic_expected:
        raise AssertionError(f"dynamic ports differ: {dynamic_found}")

    component_rows = {}
    expected_components = {
        int(vertex): tuple(int(x) for x in component)
        for vertex, component in data["unpinned_type_components"].items()
    }
    singleton_vertices = {
        vertex for vertex, response in lists.items()
        if len(response) == 1
    }
    for vertex, omitted in dynamic_found.items():
        projected = (
            set(reference) - {omitted}
        ) | {
            outside
            for outside, response in lists.items()
            if omitted not in response
        }
        all_components = components(projected, h_edges)
        component = next(item for item in all_components if vertex in item)
        if component != expected_components[vertex]:
            raise AssertionError(
                f"wrong component at dynamic port {vertex}: {component}"
            )
        markers = sorted(set(component) & singleton_vertices)
        if markers:
            raise AssertionError(
                f"dynamic port {vertex} is not in an unpinned component"
            )
        component_rows[str(vertex)] = {
            "omitted_type": omitted,
            "component": list(component),
            "singleton_markers": markers,
        }

    sealed_caps = {
        int(vertex): int(cap)
        for vertex, cap in data["sealed_singleton_caps"].items()
    }
    physicalization_paths = {
        int(vertex): tuple(int(x) for x in path)
        for vertex, path in data["physicalization_paths"].items()
    }
    cap_rows = {}
    for vertex, cap in sealed_caps.items():
        omitted = dynamic_found[vertex]
        path = physicalization_paths[vertex]
        if path[0] != vertex or len(path) != 3:
            raise AssertionError("malformed physicalization path")
        if any(
            pair(path[index], path[index + 1]) not in h_edges
            for index in range(2)
        ):
            raise AssertionError("physicalization path is not in H")
        if pair(path[0], path[2]) in h_edges:
            raise AssertionError("physicalization endpoints should meet in G")
        if pair(omitted, path[2]) not in h_edges:
            raise AssertionError("representative is not physically omitted")
        if lists[path[2]] != lists[vertex]:
            raise AssertionError("representative has the wrong exact list")
        if lists[cap] != (omitted,):
            raise AssertionError("cap is not the omitted-color singleton")
        positive = {
            outside
            for outside, response in lists.items()
            if omitted in response
        }
        if any(
            pair(cap, other) in h_edges
            for other in positive - {cap}
        ):
            raise AssertionError("claimed singleton cap is not sealed")
        if pair(vertex, cap) not in h_edges:
            raise AssertionError("sealed singleton does not cap its port")
        if pair(path[1], cap) not in h_edges:
            raise AssertionError("singleton is not a cap of the first path edge")
        cap_rows[str(vertex)] = {
            "cap": cap,
            "cap_list": list(lists[cap]),
            "sealed_positive_color": omitted,
            "physicalization_path": list(path),
        }

    list_solutions = list_colorings(reference, vertices, h_edges, lists)
    if len(list_solutions) != 2:
        raise AssertionError("unexpected dynamic-control coloring count")
    return {
        "graph6": record,
        "order": len(vertices),
        "size": len(edges),
        "parameters": result_parameters,
        "greatest_triple_family_size": len(family),
        "attack_obligations": obligations,
        "lists": {str(k): list(v) for k, v in lists.items()},
        "dynamic_free_components": component_rows,
        "sealed_singleton_caps": cap_rows,
        "list_coloring_count": len(list_solutions),
        "h_coloring": list(coloring),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    raw = args.check.read_bytes()
    data = json.loads(raw)
    result = {
        "schema": "singleton-list-endgame-verification-v1",
        "status": "PASS",
        "controls_sha256": sha256(raw).hexdigest(),
        "sealed_exact_two_buffer": audit_sealed_buffer(
            data["sealed_exact_two_buffer"]
        ),
        "dynamic_free_component": audit_dynamic_free(
            data["dynamic_free_component"]
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
