#!/usr/bin/env python3
"""Clean-room hostile replay for the dynamic Y_3 candidate.

This file deliberately does not import the candidate checker or any campaign
graph/game implementation.  Graphs are ordinary adjacency dictionaries and
states are frozensets.  The checks cover:

* the 64 graph completions times nine nonempty internal-list subpatterns in
  the seven-vertex rigidity overapproximation;
* all 16 completions of the eight-vertex double-defect local kernel;
* the literal one-guard family and all obligations in the FDzro control; and
* the complete triple-kernel failure of the ten-vertex negative control.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
import hashlib
import itertools
import json


Vertex = Hashable
State = frozenset[Vertex]
Graph = dict[Vertex, frozenset[Vertex]]


def graph(vertices: Iterable[Vertex], edges: Iterable[tuple[Vertex, Vertex]]) -> Graph:
    vertices = tuple(vertices)
    rows: dict[Vertex, set[Vertex]] = {vertex: set() for vertex in vertices}
    for left, right in edges:
        if left == right or left not in rows or right not in rows:
            raise AssertionError(("bad edge", left, right))
        rows[left].add(right)
        rows[right].add(left)
    return {vertex: frozenset(neighbors) for vertex, neighbors in rows.items()}


def edge_set(g: Graph) -> frozenset[frozenset[Vertex]]:
    return frozenset(
        frozenset((left, right))
        for left, neighbors in g.items()
        for right in neighbors
        if repr(left) < repr(right)
    )


def ordinary_graph6_pairs(order: int) -> tuple[tuple[int, int], ...]:
    return tuple((left, right) for right in range(1, order) for left in range(right))


def decode_graph6(record: str) -> Graph:
    """Decode the ordinary n<=62 graph6 form from its published bit order."""

    payload = [ord(character) - 63 for character in record.strip()]
    if not payload or not 0 <= payload[0] <= 62:
        raise AssertionError(("unsupported graph6", record))
    order = payload[0]
    bits = tuple(
        (value >> shift) & 1
        for value in payload[1:]
        for shift in range(5, -1, -1)
    )
    pairs = ordinary_graph6_pairs(order)
    if len(bits) < len(pairs):
        raise AssertionError(("short graph6", record))
    edges = [pair for pair, bit in zip(pairs, bits, strict=False) if bit]
    if any(bits[len(pairs) :]):
        raise AssertionError(("nonzero graph6 padding", record))
    return graph(range(order), edges)


def encode_graph6(g: Graph) -> str:
    vertices = tuple(sorted(g))
    if vertices != tuple(range(len(vertices))) or len(vertices) > 62:
        raise AssertionError("encoder requires vertices 0,...,n-1 with n<=62")
    bits = [
        int(right in g[left])
        for left, right in ordinary_graph6_pairs(len(vertices))
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    chars = [chr(len(vertices) + 63)]
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def complement(g: Graph) -> Graph:
    vertices = tuple(g)
    return graph(
        vertices,
        (
            (left, right)
            for left, right in itertools.combinations(vertices, 2)
            if right not in g[left]
        ),
    )


def states(vertices: Iterable[Vertex], size: int) -> set[State]:
    return {frozenset(choice) for choice in itertools.combinations(tuple(vertices), size)}


def dominates(g: Graph, state: State) -> bool:
    return all(vertex in state or bool(g[vertex] & state) for vertex in g)


def independent(g: Graph, state: State) -> bool:
    return all(right not in g[left] for left, right in itertools.combinations(state, 2))


def restoration_ok(
    reference: State,
    state: State,
    response_lists: dict[Vertex, frozenset[Vertex]],
) -> bool:
    missing = reference - state
    supplied = frozenset().union(
        *(response_lists.get(vertex, frozenset()) for vertex in state - reference)
    )
    return missing <= supplied


def successors(g: Graph, state: State, attacked: Vertex) -> set[State]:
    if attacked in state:
        raise AssertionError(("occupied attack", state, attacked))
    return {
        frozenset((state - {guard}) | {attacked})
        for guard in state
        if attacked in g[guard]
    }


def greatest_kernel(
    g: Graph,
    initial: Iterable[State],
) -> tuple[set[State], list[dict[State, Vertex]]]:
    active = set(initial)
    rounds: list[dict[State, Vertex]] = []
    while True:
        doomed: dict[State, Vertex] = {}
        for state in sorted(active, key=lambda item: tuple(sorted(item, key=repr))):
            for attacked in g:
                if attacked in state:
                    continue
                if not (successors(g, state, attacked) & active):
                    doomed[state] = attacked
                    break
        if not doomed:
            return active, rounds
        rounds.append(doomed)
        active.difference_update(doomed)


def direct_state(reference: State, anchor: Vertex, outside: Vertex) -> State:
    return frozenset((reference - {anchor}) | {outside})


def family_lists(
    g: Graph,
    reference: State,
    family: set[State],
    outside_vertices: Iterable[Vertex],
) -> dict[Vertex, frozenset[Vertex]]:
    result: dict[Vertex, frozenset[Vertex]] = {}
    for outside in outside_vertices:
        result[outside] = frozenset(
            anchor
            for anchor in reference
            if outside in g[anchor]
            and direct_state(reference, anchor, outside) in family
        )
    return result


def static_lists(
    g: Graph,
    reference: State,
    outside_vertices: Iterable[Vertex],
) -> dict[Vertex, frozenset[Vertex]]:
    result: dict[Vertex, frozenset[Vertex]] = {}
    for outside in outside_vertices:
        result[outside] = frozenset(
            anchor
            for anchor in reference
            if outside in g[anchor]
            and dominates(g, direct_state(reference, anchor, outside))
        )
    return result


def rigidity_replay() -> dict[str, object]:
    anchors = ("a", "b", "c")
    path = ("x0", "x1", "x2", "x3")
    vertices = anchors + path
    reference = frozenset(anchors)
    positive = {
        ("a", "x0"),
        ("a", "x1"),
        ("c", "x1"),
        ("b", "x2"),
        ("c", "x2"),
        ("b", "x3"),
    }
    path_g_edges = {("x0", "x2"), ("x0", "x3"), ("x1", "x3")}
    forced_edges = {frozenset(edge) for edge in positive | path_g_edges}
    forced_nonedges = {
        frozenset(edge)
        for edge in itertools.combinations(anchors, 2)
    } | {
        frozenset(edge)
        for edge in (("x0", "x1"), ("x1", "x2"), ("x2", "x3"))
    }
    all_pairs = {
        frozenset(edge) for edge in itertools.combinations(vertices, 2)
    }
    optional = sorted(
        all_pairs - forced_edges - forced_nonedges,
        key=lambda edge: tuple(sorted(edge)),
    )
    expected_optional = {
        frozenset(edge)
        for edge in (
            ("b", "x0"),
            ("c", "x0"),
            ("b", "x1"),
            ("a", "x2"),
            ("a", "x3"),
            ("c", "x3"),
        )
    }
    if set(optional) != expected_optional or len(optional) != 6:
        raise AssertionError(("rigidity coverage", optional))

    internal_left = (
        frozenset({"a"}),
        frozenset({"c"}),
        frozenset({"a", "c"}),
    )
    internal_right = (
        frozenset({"b"}),
        frozenset({"c"}),
        frozenset({"b", "c"}),
    )
    survivors: list[tuple[int, tuple[str, ...], tuple[str, ...], int]] = []
    cases = 0
    for mask in range(1 << len(optional)):
        completion = set(forced_edges)
        completion.update(optional[index] for index in range(6) if mask & (1 << index))
        g = graph(
            vertices,
            (tuple(edge) for edge in completion),
        )
        for left in internal_left:
            for right in internal_right:
                cases += 1
                lists = {
                    "x0": frozenset({"a"}),
                    "x1": left,
                    "x2": right,
                    "x3": frozenset({"b"}),
                }
                initial = {
                    state
                    for state in states(vertices, 3)
                    if dominates(g, state)
                    and restoration_ok(reference, state, lists)
                }
                terminal, _ = greatest_kernel(g, initial)
                required = {
                    direct_state(reference, anchor, outside)
                    for outside, palette in lists.items()
                    for anchor in palette
                }
                if reference in terminal and required <= terminal:
                    survivors.append(
                        (
                            mask,
                            tuple(sorted(left)),
                            tuple(sorted(right)),
                            len(terminal),
                        )
                    )

    if cases != 576 or len(survivors) != 4:
        raise AssertionError(("rigidity census", cases, survivors))
    if any(left != ("a", "c") or right != ("b", "c") for _, left, right, _ in survivors):
        raise AssertionError(("smaller family list survived", survivors))
    return {
        "cases": cases,
        "optional_pairs": [sorted(edge) for edge in optional],
        "survivors": survivors,
    }


def double_defect_replay() -> dict[str, object]:
    vertices = ("a", "b", "c", "x0", "x1", "x2", "x3", "d")
    reference = frozenset(("a", "b", "c"))
    fixed_edges_raw = {
        ("a", "x0"),
        ("a", "x1"),
        ("c", "x1"),
        ("b", "x2"),
        ("c", "x2"),
        ("b", "x3"),
        ("c", "x0"),
        ("c", "x3"),
        ("x0", "x2"),
        ("x0", "x3"),
        ("x1", "x3"),
        ("d", "c"),
        ("d", "x1"),
        ("d", "x2"),
    }
    fixed_nonedges_raw = {
        ("a", "b"),
        ("a", "c"),
        ("b", "c"),
        ("x0", "x1"),
        ("x1", "x2"),
        ("x2", "x3"),
        ("d", "a"),
        ("d", "b"),
        ("d", "x0"),
        ("d", "x3"),
    }
    fixed_edges = {frozenset(edge) for edge in fixed_edges_raw}
    fixed_nonedges = {frozenset(edge) for edge in fixed_nonedges_raw}
    all_pairs = {
        frozenset(edge) for edge in itertools.combinations(vertices, 2)
    }
    optional = sorted(
        all_pairs - fixed_edges - fixed_nonedges,
        key=lambda edge: tuple(sorted(edge)),
    )
    expected_optional = {
        frozenset(edge)
        for edge in (("b", "x0"), ("b", "x1"), ("a", "x2"), ("a", "x3"))
    }
    if fixed_edges & fixed_nonedges or set(optional) != expected_optional:
        raise AssertionError(
            ("double-defect pair coverage", fixed_edges & fixed_nonedges, optional)
        )
    if len(fixed_edges) + len(fixed_nonedges) + len(optional) != 28:
        raise AssertionError("not all eight-vertex pairs covered")

    lists = {
        "x0": frozenset({"a"}),
        "x1": frozenset({"a", "c"}),
        "x2": frozenset({"b", "c"}),
        "x3": frozenset({"b"}),
        "d": frozenset({"c"}),
    }
    required = {
        direct_state(reference, anchor, outside)
        for outside, palette in lists.items()
        for anchor in palette
    }
    rows: list[dict[str, object]] = []
    for mask in range(16):
        completion = set(fixed_edges)
        completion.update(optional[index] for index in range(4) if mask & (1 << index))
        g = graph(vertices, (tuple(edge) for edge in completion))
        initial = {
            state
            for state in states(vertices, 3)
            if dominates(g, state) and restoration_ok(reference, state, lists)
        }
        if not required <= initial:
            raise AssertionError(("missing required direct state", mask))
        terminal, rounds = greatest_kernel(g, initial)
        if reference in terminal:
            raise AssertionError(("double defect survives", mask))
        rank = next(index + 1 for index, row in enumerate(rounds) if reference in row)
        rows.append(
            {
                "mask": mask,
                "initial": len(initial),
                "round_sizes": [len(row) for row in rounds],
                "reference_rank": rank,
                "fatal_attack": rounds[rank - 1][reference],
            }
        )

    table = [
        (
            row["mask"],
            row["initial"],
            row["round_sizes"],
            row["reference_rank"],
            row["fatal_attack"],
        )
        for row in rows
    ]
    table_digest = hashlib.sha256(
        json.dumps(table, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "cases": len(rows),
        "optional_pairs": [sorted(edge) for edge in optional],
        "table": table,
        "table_sha256": table_digest,
    }


def domination_number(g: Graph) -> int:
    for size in range(len(g) + 1):
        if any(dominates(g, state) for state in states(g, size)):
            return size
    raise AssertionError("domination number not found")


def independence_number(g: Graph) -> int:
    for size in range(len(g), -1, -1):
        if any(independent(g, state) for state in states(g, size)):
            return size
    raise AssertionError("independence number not found")


def eternal_kernel(g: Graph, size: int) -> tuple[set[State], list[dict[State, Vertex]]]:
    return greatest_kernel(
        g,
        (state for state in states(g, size) if dominates(g, state)),
    )


def eternal_domination_number(g: Graph) -> int:
    for size in range(1, len(g) + 1):
        terminal, _ = eternal_kernel(g, size)
        if terminal:
            return size
    raise AssertionError("eternal domination number not found")


def k_colorable(g: Graph, color_count: int) -> bool:
    order = tuple(sorted(g, key=lambda vertex: (-len(g[vertex]), vertex)))
    assigned: dict[int, int] = {}

    def extend(index: int, used: int) -> bool:
        if index == len(order):
            return True
        vertex = order[index]
        upper = min(color_count, used + 1)
        for color in range(upper):
            if any(assigned.get(neighbor) == color for neighbor in g[vertex]):
                continue
            assigned[vertex] = color
            if extend(index + 1, max(used, color + 1)):
                return True
            del assigned[vertex]
        return False

    return extend(0, 0)


def chromatic_number(g: Graph) -> int:
    for count in range(1, len(g) + 1):
        if k_colorable(g, count):
            return count
    raise AssertionError("chromatic number not found")


def parameter_tuple(g: Graph) -> tuple[int, int, int, int]:
    return (
        domination_number(g),
        independence_number(g),
        eternal_domination_number(g),
        chromatic_number(complement(g)),
    )


def fdzro_replay() -> dict[str, object]:
    record = "FDzro"
    g = decode_graph6(record)
    if encode_graph6(g) != record:
        raise AssertionError("FDzro graph6 round trip")
    reference = frozenset((0, 1, 2))
    desired = {
        3: frozenset((0,)),
        4: frozenset((0, 2)),
        5: frozenset((1, 2)),
        6: frozenset((1,)),
    }
    forbidden = {
        direct_state(reference, anchor, outside)
        for outside in range(3, 7)
        for anchor in reference - desired[outside]
    }
    initial = {
        state
        for state in states(g, 3)
        if dominates(g, state) and state not in forbidden
    }
    family, rounds = greatest_kernel(g, initial)
    if len(family) != 21 or reference not in family:
        raise AssertionError(("FDzro constrained family", len(family), len(rounds)))
    actual_lists = family_lists(g, reference, family, range(3, 7))
    if actual_lists != desired:
        raise AssertionError(("FDzro family lists", actual_lists))

    obligations: list[tuple[tuple[int, ...], int, tuple[int, ...]]] = []
    for state in sorted(family, key=lambda item: tuple(sorted(item))):
        if not dominates(g, state):
            raise AssertionError(("FDzro nondominating state", state))
        for attacked in sorted(set(g) - state):
            responders = tuple(
                sorted(
                    guard
                    for guard in state
                    if attacked in g[guard]
                    and frozenset((state - {guard}) | {attacked}) in family
                )
            )
            if not responders:
                raise AssertionError(("FDzro failed obligation", state, attacked))
            obligations.append((tuple(sorted(state)), attacked, responders))
    if len(obligations) != 84:
        raise AssertionError(("FDzro obligation count", len(obligations)))

    actual_parameters = parameter_tuple(g)
    if actual_parameters != (2, 3, 3, 3):
        raise AssertionError(("FDzro parameters", actual_parameters))
    expected_static = {
        3: frozenset((0, 2)),
        4: frozenset((0, 1, 2)),
        5: frozenset((0, 1, 2)),
        6: frozenset((1, 2)),
    }
    actual_static = static_lists(g, reference, range(3, 7))
    if actual_static != expected_static:
        raise AssertionError(("FDzro static lists", actual_static))
    obligation_digest = hashlib.sha256(
        json.dumps(obligations, separators=(",", ":")).encode()
    ).hexdigest()
    family_digest = hashlib.sha256(
        json.dumps(
            [tuple(sorted(state)) for state in sorted(family, key=lambda item: tuple(sorted(item)))],
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    return {
        "graph6": record,
        "edges": len(edge_set(g)),
        "parameters": actual_parameters,
        "family_size": len(family),
        "family_sha256": family_digest,
        "obligations": len(obligations),
        "obligation_sha256": obligation_digest,
        "family_lists": {str(key): sorted(value) for key, value in actual_lists.items()},
        "static_lists": {str(key): sorted(value) for key, value in actual_static.items()},
    }


def bipartite(g: Graph, induced_vertices: set[int]) -> bool:
    colors: dict[int, int] = {}
    for start in induced_vertices:
        if start in colors:
            continue
        colors[start] = 0
        frontier = [start]
        while frontier:
            vertex = frontier.pop()
            for neighbor in g[vertex] & induced_vertices:
                if neighbor not in colors:
                    colors[neighbor] = 1 - colors[vertex]
                    frontier.append(neighbor)
                elif colors[neighbor] == colors[vertex]:
                    return False
    return True


def negative_control_replay() -> dict[str, object]:
    g_record = "IzM]XTR`W"
    h_record = "ICp`eik]_"
    g = decode_graph6(g_record)
    h = decode_graph6(h_record)
    if encode_graph6(g) != g_record or encode_graph6(h) != h_record:
        raise AssertionError("negative-control graph6 round trip")
    if edge_set(complement(g)) != edge_set(h):
        raise AssertionError("negative-control complement mismatch")
    actual_parameters = parameter_tuple(g)
    if actual_parameters != (3, 3, 4, 4):
        raise AssertionError(("negative-control parameters", actual_parameters))

    k4_count = sum(
        all(right in h[left] for left, right in itertools.combinations(choice, 2))
        for choice in itertools.combinations(h, 4)
    )
    if k4_count:
        raise AssertionError(("negative-control H K4 count", k4_count))
    if not all(bipartite(h, set(h[vertex])) for vertex in h):
        raise AssertionError("negative-control nonbipartite H link")
    if not all(h[left] & h[right] for left, right in itertools.combinations(h, 2)):
        raise AssertionError("negative-control pair without common H neighbor")

    initial = {state for state in states(g, 3) if dominates(g, state)}
    terminal, rounds = greatest_kernel(g, initial)
    sizes = [len(row) for row in rounds]
    if len(initial) != 77 or terminal or sizes != [10, 20, 40, 7]:
        raise AssertionError(("negative-control triple kernel", len(initial), len(terminal), sizes))
    independent_triples = {state for state in states(g, 3) if independent(g, state)}
    ranks = [
        next(index + 1 for index, row in enumerate(rounds) if state in row)
        for state in independent_triples
    ]
    if len(ranks) != 7 or sorted(ranks) != [3, 3, 4, 4, 4, 4, 4]:
        raise AssertionError(("negative-control independent ranks", ranks))
    four_family, _ = eternal_kernel(g, 4)
    if not four_family:
        raise AssertionError("negative-control missing eternal four-family")
    return {
        "graph6": g_record,
        "complement_graph6": h_record,
        "G_edges": len(edge_set(g)),
        "H_edges": len(edge_set(h)),
        "parameters": actual_parameters,
        "H_K4_count": k4_count,
        "H_all_links_bipartite": True,
        "H_every_pair_common_neighbor": True,
        "dominating_triples": len(initial),
        "round_sizes": sizes,
        "independent_rank_multiset": sorted(ranks),
        "eternal_four_family_size": len(four_family),
    }


def main() -> int:
    # Independent small graph6 convention anchor: Ch is the labeled path
    # 0-1-2-3 in ordinary graph6 ordering.
    path4 = decode_graph6("Ch")
    if edge_set(path4) != {
        frozenset((0, 1)),
        frozenset((1, 2)),
        frozenset((2, 3)),
    }:
        raise AssertionError("graph6 convention anchor failed")

    result = {
        "schema": "dynamic-gluing-y3-hostile-v1",
        "rigidity": rigidity_replay(),
        "double_defect": double_defect_replay(),
        "FDzro": fdzro_replay(),
        "negative_control": negative_control_replay(),
    }
    digest = hashlib.sha256(
        json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("PASS: independent dynamic Y3 hostile replay")
    print(f"result_sha256={digest}")
    print(
        "rigidity_cases="
        f"{result['rigidity']['cases']}; "
        "rigidity_survivors="
        f"{len(result['rigidity']['survivors'])}; "
        "double_defect_cases="
        f"{result['double_defect']['cases']}; "
        "FDzro_obligations="
        f"{result['FDzro']['obligations']}; "
        "negative_rounds="
        f"{result['negative_control']['round_sizes']}"
    )
    print(
        "double_defect_table_sha256="
        f"{result['double_defect']['table_sha256']}; "
        "FDzro_obligation_sha256="
        f"{result['FDzro']['obligation_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
