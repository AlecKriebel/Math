#!/usr/bin/env python3
"""Clean-room replay of the three deletion-dichotomy controls.

The checker uses ordinary Python sets and direct coloring enumeration.  It
imports no campaign evaluator, response-formula builder, or target code.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
TARGET = CAMPAIGN / "math" / "working" / "full_list_deletion_dichotomy" / "NOTE.md"
LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"

Graph = tuple[frozenset[int], ...]
State = frozenset[int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> Graph:
    text = record.strip()
    order = ord(text[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("only short graph6 is supported")
    bits: list[int] = []
    for char in text[1:]:
        value = ord(char) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    if len(bits) != ((needed + 5) // 6) * 6 or any(bits[needed:]):
        raise ValueError("invalid graph6 padding")
    rows = [set() for _ in range(order)]
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                rows[low].add(high)
                rows[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in rows)


def subsets(vertices: tuple[int, ...], size: int):
    yield from (frozenset(group) for group in itertools.combinations(vertices, size))


def dominates(graph: Graph, state: State, vertices: tuple[int, ...]) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard] & set(vertices))
    return set(vertices) <= covered


def independent(graph: Graph, state: State) -> bool:
    return all(graph[v].isdisjoint(state - {v}) for v in state)


def exact_gamma(graph: Graph, vertices: tuple[int, ...]) -> int:
    for size in range(1, len(vertices) + 1):
        if any(dominates(graph, state, vertices) for state in subsets(vertices, size)):
            return size
    raise AssertionError("finite graph has no dominating set")


def exact_alpha(graph: Graph, vertices: tuple[int, ...]) -> int:
    for size in range(len(vertices), 0, -1):
        if any(independent(graph, state) for state in subsets(vertices, size)):
            return size
    return 0


def proper_h_coloring_exists(
    graph: Graph,
    vertices: tuple[int, ...],
    color_count: int,
) -> bool:
    colors: dict[int, int] = {}
    h_degree = {
        v: sum(w != v and w not in graph[v] for w in vertices)
        for v in vertices
    }

    def search() -> bool:
        if len(colors) == len(vertices):
            return True
        uncolored = [v for v in vertices if v not in colors]
        vertex = max(
            uncolored,
            key=lambda v: (
                len(
                    {
                        colors[w]
                        for w in colors
                        if w != v and w not in graph[v]
                    }
                ),
                h_degree[v],
                -v,
            ),
        )
        for color in range(color_count):
            if any(
                other != vertex
                and other not in graph[vertex]
                and other in colors
                and colors[other] == color
                for other in vertices
            ):
                continue
            colors[vertex] = color
            if search():
                return True
            del colors[vertex]
        return False

    return search()


def exact_theta(graph: Graph, vertices: tuple[int, ...]) -> int:
    for count in range(1, len(vertices) + 1):
        if proper_h_coloring_exists(graph, vertices, count):
            return count
    raise AssertionError("finite complement is not colorable")


def greatest_family(graph: Graph, size: int) -> frozenset[State]:
    vertices = tuple(range(len(graph)))
    active = {
        state
        for state in subsets(vertices, size)
        if dominates(graph, state, vertices)
    }
    while True:
        rejected: set[State] = set()
        for state in active:
            for attack in vertices:
                if attack in state:
                    continue
                if not any(
                    attack in graph[guard]
                    and (state - {guard}) | {attack} in active
                    for guard in state
                ):
                    rejected.add(state)
                    break
        if not rejected:
            return frozenset(active)
        active.difference_update(rejected)


def audit_family(graph: Graph, family: frozenset[State]) -> dict[str, int | bool]:
    obligations = 0
    vertices = tuple(range(len(graph)))
    if not family:
        raise AssertionError("family is empty")
    for state in family:
        if not dominates(graph, state, vertices):
            raise AssertionError("nondominating state")
        for attack in vertices:
            if attack in state:
                continue
            obligations += 1
            if not any(
                attack in graph[guard]
                and (state - {guard}) | {attack} in family
                for guard in state
            ):
                raise AssertionError("missing one-guard response")
    return {"valid": True, "states": len(family), "obligations": obligations}


def response_lists(
    graph: Graph,
    family: frozenset[State],
    reference: State,
) -> dict[int, State]:
    return {
        target: frozenset(
            guard
            for guard in reference
            if target in graph[guard]
            and (reference - {guard}) | {target} in family
        )
        for target in range(len(graph))
        if target not in reference
    }


def anchored_list_colorings(
    graph: Graph,
    reference: State,
    lists: dict[int, State],
    *,
    deleted: frozenset[int] = frozenset(),
) -> tuple[dict[int, int], ...]:
    vertices = tuple(v for v in range(len(graph)) if v not in deleted)
    coloring = {anchor: anchor for anchor in reference}
    targets = [v for v in vertices if v not in reference]
    targets.sort(
        key=lambda v: (
            len(lists[v]),
            -sum(w != v and w not in graph[v] for w in vertices),
            v,
        )
    )
    answers: list[dict[int, int]] = []

    def search(index: int) -> None:
        if index == len(targets):
            answers.append(dict(sorted(coloring.items())))
            return
        vertex = targets[index]
        for color in sorted(lists[vertex]):
            if any(
                other != vertex
                and other not in graph[vertex]
                and other in coloring
                and coloring[other] == color
                for other in vertices
            ):
                continue
            coloring[vertex] = color
            search(index + 1)
            del coloring[vertex]

    if all(lists[v] for v in targets):
        search(0)
    return tuple(answers)


def target_link(graph: Graph, target: int) -> State:
    return frozenset(
        v for v in range(len(graph)) if v != target and v not in graph[target]
    )


def extension_histogram(
    base_colorings: tuple[dict[int, int], ...],
    link: State,
    reference: State,
) -> dict[str, int]:
    return {
        str(color): sum(
            all(coloring[vertex] != color for vertex in link)
            for coloring in base_colorings
        )
        for color in sorted(reference)
    }


def dominating_pairs_with_unique_missing_target(
    graph: Graph,
    target: int,
) -> tuple[tuple[int, int], ...]:
    remaining = tuple(v for v in range(len(graph)) if v != target)
    answers: list[tuple[int, int]] = []
    for p, q in itertools.combinations(remaining, 2):
        pair = frozenset({p, q})
        if not dominates(graph, pair, remaining):
            continue
        common_h = {
            vertex
            for vertex in range(len(graph))
            if vertex not in graph[p]
            and vertex != p
            and vertex not in graph[q]
            and vertex != q
        }
        if common_h == {target}:
            answers.append((p, q))
    return tuple(answers)


def path_core_report(
    graph: Graph,
    lists: dict[int, State],
    target: int,
    color: int,
    path: tuple[int, int, int, int],
) -> dict[str, object]:
    link = target_link(graph, target)
    consecutive_h_edges = all(
        path[i + 1] not in graph[path[i]] for i in range(3)
    )
    nonconsecutive_h_edges = [
        [path[i], path[j]]
        for i in range(4)
        for j in range(i + 2, 4)
        if path[j] not in graph[path[i]]
    ]
    left_terminal, left_port, right_port, right_terminal = path
    structural = (
        left_terminal in link
        and right_terminal in link
        and len(lists[left_terminal]) == 2
        and len(lists[right_terminal]) == 2
        and color in lists[left_terminal]
        and color in lists[right_terminal]
        and lists[left_terminal] == lists[left_port]
        and lists[right_port] == lists[right_terminal]
        and lists[left_port] != lists[right_port]
        and lists[left_port] & lists[right_port] == {color}
    )
    left_forced_terminal = next(iter(lists[left_terminal] - {color}))
    right_forced_terminal = next(iter(lists[right_terminal] - {color}))
    left_forced_port = next(iter(lists[left_port] - {left_forced_terminal}))
    right_forced_port = next(iter(lists[right_port] - {right_forced_terminal}))
    contradiction = (
        left_forced_port == right_forced_port == color
        and right_port not in graph[left_port]
    )
    return {
        "path": list(path),
        "consecutive_complement_edges": consecutive_h_edges,
        "nonconsecutive_complement_edges": nonconsecutive_h_edges,
        "lists": {str(v): sorted(lists[v]) for v in path},
        "endpoints_in_target_link": (
            left_terminal in link and right_terminal in link
        ),
        "structural_two_unit_one_collision_core": structural,
        "forced_colors": {
            str(left_terminal): left_forced_terminal,
            str(left_port): left_forced_port,
            str(right_port): right_forced_port,
            str(right_terminal): right_forced_terminal,
        },
        "middle_collision": contradiction,
    }


def enumerate_shortest_path_cores(
    graph: Graph,
    lists: dict[int, State],
    target: int,
    color: int,
) -> tuple[tuple[int, int, int, int], ...]:
    link = target_link(graph, target)
    answers: set[tuple[int, int, int, int]] = set()
    for path in itertools.permutations(
        [v for v in lists if v != target],
        4,
    ):
        a, b, c, d = path
        if a not in link or d not in link:
            continue
        if not all(path[i + 1] not in graph[path[i]] for i in range(3)):
            continue
        if not (
            len(lists[a]) == len(lists[b]) == len(lists[c]) == len(lists[d]) == 2
            and color in lists[a]
            and color in lists[d]
            and lists[a] == lists[b]
            and lists[c] == lists[d]
            and lists[b] != lists[c]
            and lists[b] & lists[c] == {color}
        ):
            continue
        canonical = min(path, tuple(reversed(path)))
        answers.add(canonical)
    return tuple(sorted(answers))


def parse_family(text: str) -> frozenset[State]:
    return frozenset(
        frozenset(int(char) for char in token)
        for token in text.split()
    )


FDZRO_FAMILY = parse_family(
    """
    012 014 024 026 046 123 124 125 134 145 234 236 245 246 256 346 456
    """
)


def replay_control(
    name: str,
    graph6: str,
    reference: State,
    target: int,
    *,
    family: frozenset[State] | None = None,
) -> dict[str, object]:
    graph = decode_graph6(graph6)
    selected_family = greatest_family(graph, 3) if family is None else family
    lists = response_lists(graph, selected_family, reference)
    base = anchored_list_colorings(
        graph,
        reference,
        lists,
        deleted=frozenset({target}),
    )
    remaining = tuple(v for v in range(len(graph)) if v != target)
    return {
        "name": name,
        "graph6": graph6,
        "order": len(graph),
        "graph_parameters": {
            "gamma": exact_gamma(graph, tuple(range(len(graph)))),
            "alpha": exact_alpha(graph, tuple(range(len(graph)))),
            "theta": exact_theta(graph, tuple(range(len(graph)))),
        },
        "deleted_parameters": {
            "gamma": exact_gamma(graph, remaining),
            "alpha": exact_alpha(graph, remaining),
            "theta": exact_theta(graph, remaining),
        },
        "family_audit": audit_family(graph, selected_family),
        "family_is_greatest": family is None,
        "family_response_lists": {
            str(v): sorted(values) for v, values in lists.items()
        },
        "target_list": sorted(lists[target]),
        "target_link": sorted(target_link(graph, target)),
        "base_compatible_anchored_coloring_count": len(base),
        "base_compatible_anchored_colorings": [
            {str(v): color for v, color in coloring.items()}
            for coloring in base
        ],
        "extension_histogram_by_target_color": extension_histogram(
            base,
            target_link(graph, target),
            reference,
        ),
        "dominating_pairs_with_unique_missing_target": [
            list(pair)
            for pair in dominating_pairs_with_unique_missing_target(graph, target)
        ],
    }


def main() -> int:
    k = replay_control(
        "order-12 equality full-list control",
        "Ksv`f\\knJVis",
        frozenset({1, 2, 3}),
        0,
    )
    graph_k = decode_graph6(k["graph6"])
    lists_k = {
        int(v): frozenset(values)
        for v, values in k["family_response_lists"].items()
    }
    canonical = subprocess.run(
        (str(LABELG), "-q"),
        input=k["graph6"] + "\n",
        text=True,
        capture_output=True,
        check=True,
    )
    if canonical.stderr:
        raise AssertionError(f"labelg stderr: {canonical.stderr!r}")
    k["canonical_graph6"] = canonical.stdout.strip()
    k["failed_augmentation_cores"] = {
        "1": path_core_report(graph_k, lists_k, 0, 1, (10, 5, 4, 11)),
        "2": path_core_report(graph_k, lists_k, 0, 2, (6, 9, 7, 8)),
    }
    k["enumerated_shortest_core_paths"] = {
        str(color): [list(path) for path in enumerate_shortest_path_cores(
            graph_k,
            lists_k,
            0,
            color,
        )]
        for color in (1, 2, 3)
    }

    hcq = replay_control(
        "static-only HCQ control",
        "HCQebjw",
        frozenset({0, 1, 2}),
        8,
    )
    fdzro = replay_control(
        "proper-family gamma-two control",
        "FDzro",
        frozenset({0, 1, 2}),
        4,
        family=FDZRO_FAMILY,
    )
    fdzro_link = set(fdzro["target_link"])
    fdzro_lists = {
        int(v): frozenset(values)
        for v, values in fdzro["family_response_lists"].items()
    }
    fdzro["false_constant_vertices_by_color"] = {
        str(color): sorted(
            vertex
            for vertex in fdzro_link
            if fdzro_lists[vertex] == {color}
        )
        for color in sorted({0, 1, 2})
    }

    result = {
        "schema": "full-list-deletion-dichotomy-control-replay-v1",
        "status": "COMPLETE",
        "target": {
            "path": str(TARGET.relative_to(CAMPAIGN)),
            "sha256": sha256(TARGET),
        },
        "controls": {
            "K": k,
            "HCQebjw": hcq,
            "FDzro": fdzro,
        },
        "implementation": {
            "ordinary_set_graph": True,
            "direct_list_coloring_enumeration": True,
            "campaign_core_imported": False,
            "labelg_sha256": sha256(LABELG),
        },
    }
    source = Path(__file__).resolve()
    result["implementation"]["source_sha256_before_result_write"] = sha256(source)
    output = source.with_name("control_result.json")
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output),
                "output_sha256": sha256(output),
                "K": {
                    "base": k["base_compatible_anchored_coloring_count"],
                    "extensions": k["extension_histogram_by_target_color"],
                    "pairs": k["dominating_pairs_with_unique_missing_target"],
                    "core_paths": k["enumerated_shortest_core_paths"],
                },
                "HCQebjw": {
                    "base": hcq["base_compatible_anchored_coloring_count"],
                    "extensions": hcq["extension_histogram_by_target_color"],
                },
                "FDzro": {
                    "base": fdzro["base_compatible_anchored_coloring_count"],
                    "extensions": fdzro["extension_histogram_by_target_color"],
                    "false_constants": fdzro["false_constant_vertices_by_color"],
                },
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
