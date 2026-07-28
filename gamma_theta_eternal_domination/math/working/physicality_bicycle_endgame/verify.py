#!/usr/bin/env python3
"""Independent verifier for the physical-holonomy boundary controls.

The implementation uses ordinary Python sets and does not import the
campaign evaluators or the SAT discovery script.
"""

from __future__ import annotations

import argparse
from itertools import combinations, permutations, product
import json
from pathlib import Path


ORDER = 12
ANCHORS = (0, 1, 2)
OUTSIDE = tuple(range(3, ORDER))
TYPE = {
    3: 0,
    4: 1,
    5: 2,
    6: 0,
    7: 1,
    8: 2,
    9: 0,
    10: 1,
    11: 2,
}
GATES = ((3, 4, 5), (6, 7, 8), (9, 10, 11))
ODD_RING = ((3, 6), (7, 10), (11, 5))
EXTRA_MATES = ((3, 9), (4, 7), (8, 11))

H_MINUS = {
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 6),
    (0, 9),
    (1, 2),
    (1, 4),
    (1, 7),
    (1, 10),
    (2, 5),
    (2, 8),
    (2, 11),
    (3, 4),
    (3, 5),
    (3, 6),
    (4, 5),
    (5, 11),
    (6, 7),
    (6, 8),
    (7, 8),
    (7, 10),
    (9, 10),
    (9, 11),
    (10, 11),
}
H_PLUS = H_MINUS | set(EXTRA_MATES)

EXPECTED = {
    "minus": {
        "g_graph6": r"KBjB\z[^||Z[",
        "h_graph6": "K{S{aCb_AAcb",
        "parameters": {
            "gamma": 2,
            "i": 2,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 4,
        },
        "dominating_triples": 163,
        "kernel_triples": 163,
        "deletion_rounds": [],
        "dominating_pairs": 9,
        "four_coloring_h": (0, 1, 2, 1, 2, 0, 2, 0, 1, 3, 2, 1),
    },
    "plus": {
        "g_graph6": r"KBjB\j[Z||ZW",
        "h_graph6": "K{S{aSbcAAcf",
        "parameters": {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 4,
            "theta": 4,
        },
        "dominating_triples": 136,
        "kernel_triples": 0,
        "deletion_rounds": [34, 56, 46],
        "dominating_pairs": 0,
        "four_coloring_h": (0, 1, 2, 1, 2, 3, 2, 0, 1, 2, 3, 0),
    },
}


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def complement(edges: set[tuple[int, int]]) -> set[tuple[int, int]]:
    return set(combinations(range(ORDER), 2)) - edges


def adjacent(edges: set[tuple[int, int]], u: int, v: int) -> bool:
    return u != v and pair(u, v) in edges


def graph6(edges: set[tuple[int, int]]) -> str:
    bits = [
        int((u, v) in edges)
        for v in range(1, ORDER)
        for u in range(v)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(ORDER + 63) + "".join(payload)


def dominates(
    state: tuple[int, ...],
    edges: set[tuple[int, int]],
) -> bool:
    occupied = set(state)
    return all(
        vertex in occupied
        or any(adjacent(edges, vertex, guard) for guard in state)
        for vertex in range(ORDER)
    )


def independent(
    state: tuple[int, ...],
    edges: set[tuple[int, int]],
) -> bool:
    return not any(adjacent(edges, u, v) for u, v in combinations(state, 2))


def domination_number(edges: set[tuple[int, int]]) -> int:
    for size in range(1, ORDER + 1):
        if any(dominates(state, edges) for state in combinations(range(ORDER), size)):
            return size
    raise AssertionError("no dominating set")


def independence_number(edges: set[tuple[int, int]]) -> int:
    return max(
        size
        for size in range(1, ORDER + 1)
        if any(
            independent(state, edges)
            for state in combinations(range(ORDER), size)
        )
    )


def independent_domination_number(edges: set[tuple[int, int]]) -> int:
    for size in range(1, ORDER + 1):
        if any(
            independent(state, edges) and dominates(state, edges)
            for state in combinations(range(ORDER), size)
        ):
            return size
    raise AssertionError("no independent dominating set")


def colorable(
    edges: set[tuple[int, int]],
    color_count: int,
) -> tuple[int, ...] | None:
    order = sorted(
        range(ORDER),
        key=lambda vertex: -sum(
            adjacent(edges, vertex, other) for other in range(ORDER)
        ),
    )
    colors = [-1] * ORDER

    def search(index: int) -> bool:
        if index == ORDER:
            return True
        vertex = order[index]
        forbidden = {
            colors[other]
            for other in range(ORDER)
            if colors[other] >= 0 and adjacent(edges, vertex, other)
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(index + 1):
                return True
            colors[vertex] = -1
        return False

    return tuple(colors) if search(0) else None


def greatest_kernel(
    edges: set[tuple[int, int]],
    guard_count: int,
) -> tuple[set[tuple[int, ...]], list[int], int]:
    active = {
        state
        for state in combinations(range(ORDER), guard_count)
        if dominates(state, edges)
    }
    initial = len(active)
    rounds: list[int] = []
    while True:
        deleted = {
            state
            for state in active
            if any(
                not any(
                    adjacent(edges, guard, attacked)
                    and tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    in active
                    for guard in state
                )
                for attacked in range(ORDER)
                if attacked not in state
            )
        }
        if not deleted:
            return active, rounds, initial
        rounds.append(len(deleted))
        active -= deleted


def eternal_number(edges: set[tuple[int, int]]) -> int:
    for size in range(1, ORDER + 1):
        kernel, _, _ = greatest_kernel(edges, size)
        if kernel:
            return size
    raise AssertionError("no eternal family")


def family_lists(
    family: set[tuple[int, ...]],
) -> dict[int, tuple[int, ...]]:
    anchor = set(ANCHORS)
    return {
        vertex: tuple(
            omitted
            for omitted in ANCHORS
            if tuple(sorted((anchor - {omitted}) | {vertex})) in family
        )
        for vertex in OUTSIDE
    }


def expected_lists() -> dict[int, tuple[int, ...]]:
    return {
        vertex: tuple(anchor for anchor in ANCHORS if anchor != TYPE[vertex])
        for vertex in OUTSIDE
    }


def check_physical_types(
    h_edges: set[tuple[int, int]],
) -> None:
    for vertex in OUTSIDE:
        anchor_neighbors = {
            anchor
            for anchor in ANCHORS
            if adjacent(h_edges, anchor, vertex)
        }
        if anchor_neighbors != {TYPE[vertex]}:
            raise AssertionError(("wrong physical type", vertex, anchor_neighbors))


def bipartitions(
    h_edges: set[tuple[int, int]],
) -> dict[int, list[tuple[set[int], set[int]]]]:
    result: dict[int, list[tuple[set[int], set[int]]]] = {}
    for omitted in ANCHORS:
        vertices = {vertex for vertex in OUTSIDE if TYPE[vertex] == omitted}
        unseen = set(vertices)
        components = []
        while unseen:
            root = min(unseen)
            sides = ({root}, set())
            color = {root: 0}
            stack = [root]
            unseen.remove(root)
            while stack:
                vertex = stack.pop()
                for other in vertices:
                    if not adjacent(h_edges, vertex, other):
                        continue
                    wanted = 1 - color[vertex]
                    if other in color and color[other] != wanted:
                        raise AssertionError("type component is not bipartite")
                    if other not in color:
                        color[other] = wanted
                        sides[wanted].add(other)
                        unseen.remove(other)
                        stack.append(other)
            components.append(sides)
        result[omitted] = components
    return result


def check_side_purity(
    h_edges: set[tuple[int, int]],
    parts: dict[int, list[tuple[set[int], set[int]]]],
) -> None:
    for vertex in OUTSIDE:
        for components in parts.values():
            for left, right in components:
                sees_left = any(adjacent(h_edges, vertex, x) for x in left)
                sees_right = any(adjacent(h_edges, vertex, x) for x in right)
                if sees_left and sees_right:
                    raise AssertionError(("side-purity failure", vertex, left, right))


def check_cross_triangles(h_edges: set[tuple[int, int]]) -> None:
    for x, y in combinations(OUTSIDE, 2):
        if TYPE[x] == TYPE[y] or not adjacent(h_edges, x, y):
            continue
        third = ({0, 1, 2} - {TYPE[x], TYPE[y]}).pop()
        witnesses = [
            z
            for z in OUTSIDE
            if TYPE[z] == third
            and adjacent(h_edges, x, z)
            and adjacent(h_edges, y, z)
        ]
        if not witnesses:
            raise AssertionError(("cross edge has no transversal triangle", x, y))


def common_neighbor_failures(
    h_edges: set[tuple[int, int]],
) -> list[tuple[int, int]]:
    return [
        (u, v)
        for u, v in combinations(range(ORDER), 2)
        if not any(
            adjacent(h_edges, u, witness)
            and adjacent(h_edges, v, witness)
            for witness in range(ORDER)
            if witness not in (u, v)
        )
    ]


def c079_fans(
    h_edges: set[tuple[int, int]],
) -> list[tuple[int, int, int, tuple[int, ...]]]:
    fans = []
    for omitted in ANCHORS:
        component_vertices = [
            vertex for vertex in OUTSIDE if TYPE[vertex] == omitted
        ]
        for length_vertices in range(2, len(component_vertices) + 1):
            for path in permutations(component_vertices, length_vertices):
                if path[0] > path[-1] or (length_vertices - 1) % 2 == 0:
                    continue
                if not all(
                    adjacent(h_edges, path[i], path[i + 1])
                    for i in range(length_vertices - 1)
                ):
                    continue
                for hub in OUTSIDE:
                    if hub in path:
                        continue
                    if not (
                        adjacent(h_edges, hub, path[0])
                        and adjacent(h_edges, hub, path[-1])
                    ):
                        continue
                    for positive in OUTSIDE:
                        if (
                            positive == hub
                            or positive in path
                            or TYPE[positive] == omitted
                        ):
                            continue
                        if adjacent(h_edges, positive, hub):
                            fans.append((omitted, positive, hub, path))
    return fans


def shortest_unbalanced_cycle(
    h_edges: set[tuple[int, int]],
) -> tuple[int, ...]:
    for length in range(3, len(OUTSIDE) + 1):
        for cycle in permutations(OUTSIDE, length):
            if cycle[0] != min(cycle) or cycle[1] > cycle[-1]:
                continue
            if not all(
                adjacent(h_edges, cycle[i], cycle[(i + 1) % length])
                for i in range(length)
            ):
                continue
            parity = sum(
                TYPE[cycle[i]] == TYPE[cycle[(i + 1) % length]
                ]
                for i in range(length)
            ) % 2
            if parity:
                return cycle
    raise AssertionError("no unbalanced signed cycle")


def word_classification() -> dict[str, list[tuple[int, ...]]]:
    classes: dict[str, list[tuple[int, ...]]] = {}
    for length in (3, 4, 5):
        canonical = set()
        for word in product(range(3), repeat=length):
            if sum(
                word[i] == word[(i + 1) % length] for i in range(length)
            ) % 2 == 0:
                continue
            representatives = []
            for reverse in (False, True):
                base = word if not reverse else tuple(reversed(word))
                for shift in range(length):
                    rotated = base[shift:] + base[:shift]
                    names: dict[int, int] = {}
                    relabeled = []
                    for value in rotated:
                        names.setdefault(value, len(names))
                        relabeled.append(names[value])
                    representatives.append(tuple(relabeled))
            canonical.add(min(representatives))
        classes[str(length)] = sorted(canonical)
    return classes


def verify_control(
    name: str,
    h_edges: set[tuple[int, int]],
) -> dict[str, object]:
    expected = EXPECTED[name]
    g_edges = complement(h_edges)
    if graph6(g_edges) != expected["g_graph6"]:
        raise AssertionError("G graph6 mismatch")
    if graph6(h_edges) != expected["h_graph6"]:
        raise AssertionError("H graph6 mismatch")

    kernel3, deletion_rounds, initial3 = greatest_kernel(g_edges, 3)
    parameters = {
        "gamma": domination_number(g_edges),
        "i": independent_domination_number(g_edges),
        "alpha": independence_number(g_edges),
        "gamma_infinity": eternal_number(g_edges),
        "theta": next(
            count
            for count in range(1, ORDER + 1)
            if colorable(h_edges, count) is not None
        ),
    }
    if parameters != expected["parameters"]:
        raise AssertionError((name, parameters))
    if initial3 != expected["dominating_triples"]:
        raise AssertionError("wrong dominating-triple count")
    if len(kernel3) != expected["kernel_triples"]:
        raise AssertionError("wrong triple-kernel size")
    if deletion_rounds != expected["deletion_rounds"]:
        raise AssertionError(("wrong deletion rounds", deletion_rounds))

    dominating_pairs = sum(
        dominates(state, g_edges)
        for state in combinations(range(ORDER), 2)
    )
    if dominating_pairs != expected["dominating_pairs"]:
        raise AssertionError("wrong dominating-pair count")

    if colorable(h_edges, 3) is not None:
        raise AssertionError("H unexpectedly three-colorable")
    coloring4 = expected["four_coloring_h"]
    if any(
        coloring4[u] == coloring4[v] for u, v in h_edges
    ):
        raise AssertionError("stored H four-coloring is invalid")

    check_physical_types(h_edges)
    parts = bipartitions(h_edges)
    check_side_purity(h_edges, parts)
    check_cross_triangles(h_edges)

    if any(
        all(adjacent(h_edges, u, v) for u, v in combinations(four, 2))
        for four in combinations(range(ORDER), 4)
    ):
        raise AssertionError("H contains K4")

    for gate in GATES:
        if not all(
            adjacent(h_edges, u, v) for u, v in combinations(gate, 2)
        ):
            raise AssertionError(("missing gate", gate))
    for u, v in ODD_RING:
        if not adjacent(h_edges, u, v) or TYPE[u] != TYPE[v]:
            raise AssertionError(("missing odd-ring connector", u, v))

    anchor = tuple(sorted(ANCHORS))
    direct_dominating_lists = {
        vertex: tuple(
            omitted
            for omitted in ANCHORS
            if tuple(
                sorted((set(anchor) - {omitted}) | {vertex})
            )
            in {
                state
                for state in combinations(range(ORDER), 3)
                if dominates(state, g_edges)
            }
        )
        for vertex in OUTSIDE
    }
    if direct_dominating_lists != expected_lists():
        raise AssertionError("static direct-swap lists are not exact physical types")

    response_lists = None
    obligations = None
    if name == "minus":
        if family_lists(kernel3) != expected_lists():
            raise AssertionError("eternal-family response lists differ")
        obligations = 0
        for state in kernel3:
            for attacked in range(ORDER):
                if attacked in state:
                    continue
                obligations += 1
                if not any(
                    adjacent(g_edges, guard, attacked)
                    and tuple(
                        sorted((set(state) - {guard}) | {attacked})
                    )
                    in kernel3
                    for guard in state
                ):
                    raise AssertionError(("failed obligation", state, attacked))
        response_lists = {
            str(vertex): list(values)
            for vertex, values in family_lists(kernel3).items()
        }

    failures = common_neighbor_failures(h_edges)
    if name == "plus" and failures:
        raise AssertionError(("plus should have gamma-three witnesses", failures))
    if name == "minus" and not failures:
        raise AssertionError("minus unexpectedly has gamma at least three")

    return {
        "g_graph6": graph6(g_edges),
        "h_graph6": graph6(h_edges),
        "g_size": len(g_edges),
        "h_size": len(h_edges),
        "parameters": parameters,
        "dominating_triples": initial3,
        "kernel_triples": len(kernel3),
        "deletion_rounds": deletion_rounds,
        "dominating_pairs": dominating_pairs,
        "attack_obligations": obligations,
        "response_lists": response_lists,
        "direct_dominating_lists": {
            str(vertex): list(values)
            for vertex, values in direct_dominating_lists.items()
        },
        "common_neighbor_failures": [list(uv) for uv in failures],
        "c079_fans": [
            [omitted, positive, hub, list(path)]
            for omitted, positive, hub, path in c079_fans(h_edges)
        ],
        "shortest_unbalanced_cycle": list(
            shortest_unbalanced_cycle(h_edges)
        ),
        "four_coloring_h": list(coloring4),
        "side_purity": True,
        "every_cross_edge_in_transversal_triangle": True,
    }


def check_control_file(
    path: Path,
    result: dict[str, object],
) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "physicality-bicycle-endgame-controls-v1":
        raise AssertionError("wrong control schema")
    if data.get("order") != ORDER or data.get("anchor_state") != list(ANCHORS):
        raise AssertionError("wrong control order or anchor")
    if {
        int(vertex): int(omitted)
        for vertex, omitted in data.get("types", {}).items()
    } != TYPE:
        raise AssertionError("control type map differs")
    if {
        tuple(int(vertex) for vertex in gate)
        for gate in data.get("gates", [])
    } != set(GATES):
        raise AssertionError("control gate set differs")
    if {
        pair(int(u), int(v))
        for u, v in data.get("odd_ring_edges", [])
    } != {pair(u, v) for u, v in ODD_RING}:
        raise AssertionError("control odd ring differs")

    stored_minus = {
        pair(int(u), int(v))
        for u, v in data["minus"]["h_edges"]
    }
    if stored_minus != H_MINUS:
        raise AssertionError("stored H-minus edges differ")
    stored_added = {
        pair(int(u), int(v))
        for u, v in data["plus"]["added_h_edges"]
    }
    if stored_minus | stored_added != H_PLUS:
        raise AssertionError("stored H-plus edges differ")

    for name in ("minus", "plus"):
        stored = data[name]
        checked = result[name]
        for field in ("g_graph6", "h_graph6", "parameters", "dominating_pairs"):
            if stored[field] != checked[field]:
                raise AssertionError((name, field, stored[field], checked[field]))
        if stored["dominating_triples"] != checked["dominating_triples"]:
            raise AssertionError((name, "dominating_triples"))
        if stored["greatest_triple_family"] != checked["kernel_triples"]:
            raise AssertionError((name, "greatest_triple_family"))
        if stored["shortest_unbalanced_cycle"] != checked[
            "shortest_unbalanced_cycle"
        ]:
            raise AssertionError((name, "shortest_unbalanced_cycle"))
    if data["minus"]["attack_obligations"] != result["minus"][
        "attack_obligations"
    ]:
        raise AssertionError("stored attack-obligation count differs")
    if data["plus"]["deletion_rounds"] != result["plus"]["deletion_rounds"]:
        raise AssertionError("stored deletion rounds differ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = {
        "schema": "physicality-bicycle-endgame-controls-v1",
        "minus": verify_control("minus", H_MINUS),
        "plus": verify_control("plus", H_PLUS),
        "unbalanced_type_word_classes": word_classification(),
    }
    if args.check is not None:
        check_control_file(args.check, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
