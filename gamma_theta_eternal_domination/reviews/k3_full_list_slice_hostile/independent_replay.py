#!/usr/bin/env python3
"""Clean-room replay for the k=3 full-family-list slice.

This file imports no campaign evaluator and no target-lane code.  Graphs are
represented by ordinary ``frozenset`` neighborhoods.  Eternal closure is
computed as an explicit colored configuration digraph: each state/attack
pair stores its successor states, and dead configurations are deleted to a
greatest fixed point.

The bounded scan covers connected unlabeled graphs emitted by pinned
``geng`` through order nine.  The separate controls replay the order-12
full-list graph, the proper-family and static-list countercontrols, and the
two abstract falsifiers.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"
TARGET_NOTE = CAMPAIGN / "math" / "working" / "k3_full_list_slice" / "NOTE.md"
TARGET_PROBE = CAMPAIGN / "math" / "working" / "k3_full_list_slice" / "probe.py"
TARGET_RESULT = (
    CAMPAIGN / "math" / "working" / "k3_full_list_slice" / "probe_result.json"
)

VertexSet = frozenset[int]
Graph = tuple[VertexSet, ...]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> Graph:
    text = record.strip()
    if not text or text.startswith("~"):
        raise ValueError("only short ordinary graph6 records are supported")
    n = ord(text[0]) - 63
    if not 0 <= n <= 62:
        raise ValueError("invalid short graph6 order")
    bits: list[int] = []
    for char in text[1:]:
        value = ord(char) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 payload")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    if len(bits) != (needed + 5) // 6 * 6 or any(bits[needed:]):
        raise ValueError("noncanonical or nonzero-padded graph6 record")
    neighbors = [set() for _ in range(n)]
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                neighbors[low].add(high)
                neighbors[high].add(low)
            cursor += 1
    return tuple(frozenset(row) for row in neighbors)


def subsets(vertices: range | tuple[int, ...], size: int):
    yield from (frozenset(group) for group in itertools.combinations(vertices, size))


def independent(graph: Graph, state: VertexSet) -> bool:
    return all(graph[v].isdisjoint(state - {v}) for v in state)


def dominates(graph: Graph, state: VertexSet) -> bool:
    covered = set(state)
    for v in state:
        covered.update(graph[v])
    return len(covered) == len(graph)


def exact_gamma(graph: Graph) -> int:
    vertices = range(len(graph))
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in subsets(vertices, size)):
            return size
    raise AssertionError("finite graph has no dominating set")


def exact_alpha(graph: Graph) -> int:
    vertices = range(len(graph))
    for size in range(len(graph), 0, -1):
        if any(independent(graph, state) for state in subsets(vertices, size)):
            return size
    return 0


def static_full_pairs(graph: Graph) -> tuple[tuple[VertexSet, int], ...]:
    answer: list[tuple[VertexSet, int]] = []
    vertices = range(len(graph))
    for reference in subsets(vertices, 3):
        if not independent(graph, reference):
            continue
        for target in vertices:
            if target in reference or not reference.issubset(graph[target]):
                continue
            if all(
                dominates(graph, (reference - {guard}) | {target})
                for guard in reference
            ):
                answer.append((reference, target))
    return tuple(answer)


def equality_static_filter(graph: Graph, pairs) -> bool:
    if not pairs:
        return False
    vertices = range(len(graph))
    if any(independent(graph, state) for state in subsets(vertices, 4)):
        return False
    if any(dominates(graph, state) for state in subsets(vertices, 2)):
        return False
    if any(dominates(graph, frozenset({v})) for v in vertices):
        return False
    return True


def colored_configuration_digraph(
    graph: Graph, size: int
) -> tuple[
    frozenset[VertexSet],
    dict[VertexSet, dict[int, frozenset[VertexSet]]],
]:
    states = frozenset(
        state
        for state in subsets(range(len(graph)), size)
        if dominates(graph, state)
    )
    arcs: dict[VertexSet, dict[int, frozenset[VertexSet]]] = {}
    all_vertices = frozenset(range(len(graph)))
    for state in states:
        by_attack: dict[int, frozenset[VertexSet]] = {}
        for attack in all_vertices - state:
            by_attack[attack] = frozenset(
                (state - {guard}) | {attack}
                for guard in state
                if attack in graph[guard]
                and (state - {guard}) | {attack} in states
            )
        arcs[state] = by_attack
    return states, arcs


def greatest_family(graph: Graph, size: int) -> frozenset[VertexSet]:
    live, arcs = colored_configuration_digraph(graph, size)
    live_set = set(live)
    while True:
        dead = {
            state
            for state in live_set
            if any(
                successors.isdisjoint(live_set)
                for successors in arcs[state].values()
            )
        }
        if not dead:
            return frozenset(live_set)
        live_set.difference_update(dead)


def response_list(
    graph: Graph,
    family: frozenset[VertexSet],
    reference: VertexSet,
    target: int,
) -> tuple[int, ...]:
    return tuple(
        guard
        for guard in sorted(reference)
        if target in graph[guard]
        and (reference - {guard}) | {target} in family
    )


def literal_family_audit(
    graph: Graph, family: frozenset[VertexSet]
) -> dict[str, int]:
    obligations = 0
    for state in family:
        if not dominates(graph, state):
            raise AssertionError("family contains a nondominating state")
        for attack in set(range(len(graph))) - state:
            obligations += 1
            if not any(
                attack in graph[guard]
                and (state - {guard}) | {attack} in family
                for guard in state
            ):
                raise AssertionError((state, attack))
    return {"states": len(family), "attack_obligations": obligations}


def connected_records(order: int):
    with subprocess.Popen(
        [str(GENG), "-cq", str(order)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ) as process:
        assert process.stdout is not None
        for line in process.stdout:
            record = line.strip()
            if record:
                yield record
        stderr = process.stderr.read() if process.stderr is not None else ""
        code = process.wait()
        if code or stderr:
            raise RuntimeError((code, stderr))


def scan(max_order: int) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for order in range(1, max_order + 1):
        stream_hash = hashlib.sha256()
        graph_count = 0
        raw_pairs = 0
        gamma_alpha_graphs = 0
        gamma_alpha_pairs = 0
        equality_graphs = 0
        equality_pairs = 0
        histogram = {str(i): 0 for i in range(4)}
        full_pairs = 0
        for record in connected_records(order):
            graph_count += 1
            stream_hash.update(record.encode("ascii") + b"\n")
            graph = decode_graph6(record)
            pairs = static_full_pairs(graph)
            raw_pairs += len(pairs)
            if not equality_static_filter(graph, pairs):
                continue
            gamma_alpha_graphs += 1
            gamma_alpha_pairs += len(pairs)
            family = greatest_family(graph, 3)
            if not family:
                continue
            equality_graphs += 1
            equality_pairs += len(pairs)
            for reference, target in pairs:
                listed = response_list(graph, family, reference, target)
                histogram[str(len(listed))] += 1
                if listed == tuple(sorted(reference)):
                    full_pairs += 1
        rows.append(
            {
                "order": order,
                "connected_graphs": graph_count,
                "graph6_stream_sha256": stream_hash.hexdigest(),
                "raw_static_full_pairs": raw_pairs,
                "gamma_alpha_three_graphs_with_static_full_pair": (
                    gamma_alpha_graphs
                ),
                "gamma_alpha_three_static_full_pairs": gamma_alpha_pairs,
                "eternal_three_graphs_among_those_candidates": equality_graphs,
                "equality_static_pairs_in_eternal_graphs": equality_pairs,
                "equality_static_pair_family_list_size_histogram": histogram,
                "greatest_family_full_pairs": full_pairs,
            }
        )
    summed_keys = (
        "connected_graphs",
        "raw_static_full_pairs",
        "gamma_alpha_three_graphs_with_static_full_pair",
        "gamma_alpha_three_static_full_pairs",
        "eternal_three_graphs_among_those_candidates",
        "equality_static_pairs_in_eternal_graphs",
        "greatest_family_full_pairs",
    )
    return {
        "orders": rows,
        "totals": {
            key: sum(int(row[key]) for row in rows)
            for key in summed_keys
        },
        "equality_static_pair_family_list_size_histogram": {
            str(size): sum(
                int(row["equality_static_pair_family_list_size_histogram"][str(size)])
                for row in rows
            )
            for size in range(4)
        },
    }


def graph_isomorphism(first: Graph, second: Graph) -> dict[int, int] | None:
    if len(first) != len(second):
        return None
    n = len(first)
    first_degrees = [len(first[v]) for v in range(n)]
    second_degrees = [len(second[v]) for v in range(n)]
    if sorted(first_degrees) != sorted(second_degrees):
        return None
    order = sorted(
        range(n),
        key=lambda v: (
            sum(first_degrees[u] for u in first[v]),
            first_degrees[v],
        ),
        reverse=True,
    )
    candidates = {
        v: [
            w
            for w in range(n)
            if first_degrees[v] == second_degrees[w]
            and sorted(first_degrees[u] for u in first[v])
            == sorted(second_degrees[u] for u in second[w])
        ]
        for v in range(n)
    }
    mapping: dict[int, int] = {}
    used: set[int] = set()

    def extend(position: int) -> bool:
        if position == n:
            return True
        vertex = order[position]
        for image in candidates[vertex]:
            if image in used:
                continue
            if any(
                ((prior in first[vertex]) != (mapped in second[image]))
                for prior, mapped in mapping.items()
            ):
                continue
            mapping[vertex] = image
            used.add(image)
            if extend(position + 1):
                return True
            used.remove(image)
            del mapping[vertex]
        return False

    return dict(mapping) if extend(0) else None


def order12_control() -> dict[str, object]:
    labeled_record = "Ksv`f\\knJVis"
    canonical_record = "K{eYptMJynEn"
    graph = decode_graph6(labeled_record)
    canonical_graph = decode_graph6(canonical_record)
    mapping = graph_isomorphism(graph, canonical_graph)
    if mapping is None:
        raise AssertionError("labeled and canonical order-12 records differ")

    labelg = subprocess.run(
        [str(LABELG), "-q"],
        input=labeled_record + "\n",
        capture_output=True,
        text=True,
        check=True,
    )
    if labelg.stderr or labelg.stdout.strip() != canonical_record:
        raise AssertionError("pinned labelg control failed")

    gamma = exact_gamma(graph)
    alpha = exact_alpha(graph)
    family = greatest_family(graph, 3)
    family_audit = literal_family_audit(graph, family)
    if gamma != 3 or alpha != 3 or not family:
        raise AssertionError("order-12 equality parameters failed")
    dominating_triples = sum(
        dominates(graph, state) for state in subsets(range(12), 3)
    )
    if len(family) != dominating_triples:
        raise AssertionError("not all dominating triples survive")

    reference = frozenset({1, 2, 3})
    targets = sorted(set(range(12)) - reference)
    lists = {
        str(target): list(response_list(graph, family, reference, target))
        for target in targets
    }
    colorings: list[dict[int, int]] = []
    for colors in itertools.product(*(lists[str(target)] for target in targets)):
        coloring = {1: 1, 2: 2, 3: 3}
        coloring.update(zip(targets, colors))
        if all(
            coloring[u] != coloring[v]
            for u, v in itertools.combinations(range(12), 2)
            if v not in graph[u]
        ):
            colorings.append(coloring)

    partition = (
        frozenset({1, 5, 8, 11}),
        frozenset({2, 6, 7, 10}),
        frozenset({0, 3, 4, 9}),
    )
    if not all(
        all(v in graph[u] for u, v in itertools.combinations(part, 2))
        for part in partition
    ):
        raise AssertionError("order-12 clique partition failed")

    target = 0
    link = sorted(v for v in range(12) if v != target and v not in graph[target])
    link_edges = [
        [u, v]
        for u, v in itertools.combinations(link, 2)
        if v not in graph[u]
    ]
    spokes: dict[str, list[int]] = {}
    witnesses: dict[str, list[int]] = {}
    for anchor in sorted(reference):
        spoke = [v for v in link if v not in graph[anchor]]
        spokes[str(anchor)] = spoke
        for p in spoke:
            witnesses[f"{anchor},{p}"] = [
                y
                for y in range(12)
                if y not in {anchor, p}
                and y not in graph[anchor]
                and y not in graph[p]
            ]
    return {
        "labeled_graph6": labeled_record,
        "canonical_graph6": canonical_record,
        "custom_isomorphism": {str(k): v for k, v in sorted(mapping.items())},
        "pinned_labelg_agrees": True,
        "parameters": {
            "gamma": gamma,
            "alpha": alpha,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "dominating_triples": dominating_triples,
        "greatest_family": family_audit,
        "greatest_family_equals_all_dominating_triples": True,
        "reference": sorted(reference),
        "family_response_lists": lists,
        "full_targets": [
            target
            for target in targets
            if lists[str(target)] == sorted(reference)
        ],
        "compatible_anchored_coloring_count": len(colorings),
        "compatible_colorings": [
            {str(v): coloring[v] for v in range(12)}
            for coloring in colorings
        ],
        "checked_clique_partition": [sorted(part) for part in partition],
        "target_link_vertices": link,
        "target_link_edges": link_edges,
        "spokes": spokes,
        "external_witnesses": witnesses,
    }


def fd_zro_control() -> dict[str, object]:
    graph = decode_graph6("FDzro")
    triples = (
        (0, 1, 2),
        (0, 1, 4),
        (0, 2, 4),
        (0, 2, 6),
        (0, 4, 6),
        (1, 2, 3),
        (1, 2, 4),
        (1, 2, 5),
        (1, 3, 4),
        (1, 4, 5),
        (2, 3, 4),
        (2, 3, 6),
        (2, 4, 5),
        (2, 4, 6),
        (2, 5, 6),
        (3, 4, 6),
        (4, 5, 6),
    )
    family = frozenset(frozenset(state) for state in triples)
    reference = frozenset({0, 1, 2})
    return {
        "parameters": {
            "gamma": exact_gamma(graph),
            "alpha": exact_alpha(graph),
            "gamma_infinity": next(
                size for size in range(1, 8) if greatest_family(graph, size)
            ),
        },
        "family": literal_family_audit(graph, family),
        "greatest_family_size": len(greatest_family(graph, 3)),
        "strict_subfamily": family < greatest_family(graph, 3),
        "lists": {
            str(target): list(response_list(graph, family, reference, target))
            for target in range(3, 7)
        },
    }


def hcqebjw_control() -> dict[str, object]:
    graph = decode_graph6("HCQebjw")
    family = greatest_family(graph, 3)
    reference = frozenset({0, 1, 2})
    target = 8
    static = {
        str(guard): dominates(graph, (reference - {guard}) | {target})
        for guard in sorted(reference)
    }
    partition = (
        frozenset({0, 3, 6}),
        frozenset({1, 4, 8}),
        frozenset({2, 5, 7}),
    )
    if not all(
        all(v in graph[u] for u, v in itertools.combinations(part, 2))
        for part in partition
    ):
        raise AssertionError("HCQebjw partition failed")
    return {
        "parameters": {
            "gamma": exact_gamma(graph),
            "alpha": exact_alpha(graph),
            "gamma_infinity": next(
                size for size in range(1, 10) if greatest_family(graph, size)
            ),
            "theta": 3,
        },
        "static_swaps_dominate": static,
        "greatest_family_size": len(family),
        "family_response_list": list(
            response_list(graph, family, reference, target)
        ),
        "checked_clique_partition": [sorted(part) for part in partition],
    }


def abstract_controls() -> dict[str, object]:
    exchange_states = frozenset(
        {
            (0, 0),
            (1, 1),
            (1, 2),
            (2, 1),
            (2, 4),
            (3, 3),
            (3, 5),
            (3, 6),
            (4, 1),
            (5, 5),
            (6, 3),
            (7, 7),
        }
    )
    exchange_ok = True
    for removed, inserted in exchange_states:
        for target in range(3):
            if inserted & (1 << target):
                continue
            if not any(
                not (removed & (1 << source))
                and (
                    removed | (1 << source),
                    inserted | (1 << target),
                )
                in exchange_states
                for source in range(3)
            ):
                exchange_ok = False
        for source in range(3):
            if not (removed & (1 << source)):
                continue
            if not any(
                inserted & (1 << target)
                and (
                    removed & ~(1 << source),
                    inserted & ~(1 << target),
                )
                in exchange_states
                for target in range(3)
            ):
                exchange_ok = False
    base_orders = [
        list(permutation)
        for permutation in itertools.permutations(range(3))
        if all(
            (
                removed,
                sum(
                    1 << permutation[source]
                    for source in range(3)
                    if removed & (1 << source)
                ),
            )
            in exchange_states
            for removed in range(8)
        )
    ]

    link_edges = {(0, 1), (0, 2), (0, 3)}
    marks = {1: 0, 2: 1, 3: 2}
    link_extensions: dict[str, int] = {}
    for x_color in range(3):
        remaining = tuple(color for color in range(3) if color != x_color)
        count = 0
        for flip in (0, 1):
            colors = {
                vertex: remaining[(0 if vertex == 0 else 1) ^ flip]
                for vertex in range(4)
            }
            if all(colors[vertex] != mark for vertex, mark in marks.items()):
                count += 1
        link_extensions[str(x_color)] = count
    h_edges = {
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (3, 5),
        (3, 6),
        (3, 7),
        (4, 5),
        (4, 6),
        (4, 7),
        (0, 5),
        (1, 6),
        (2, 7),
    }
    graph_neighbors = [set() for _ in range(8)]
    for first, second in itertools.combinations(range(8), 2):
        if (first, second) not in h_edges:
            graph_neighbors[first].add(second)
            graph_neighbors[second].add(first)
    realizing_graph = tuple(frozenset(row) for row in graph_neighbors)
    return {
        "full_column_exchange": {
            "axioms_hold": exchange_ok,
            "first_column_full": all(
                (1 << source, 1) in exchange_states for source in range(3)
            ),
            "base_orderings": base_orders,
        },
        "marked_link_claw": {
            "edges": [list(edge) for edge in sorted(link_edges)],
            "extensions_by_x_color": link_extensions,
            "realizing_graph_parameters": {
                "gamma": exact_gamma(realizing_graph),
                "alpha": exact_alpha(realizing_graph),
                "greatest_eternal_three_family_size": len(
                    greatest_family(realizing_graph, 3)
                ),
            },
        },
    }


def compare_target(replay: dict[str, object]) -> dict[str, object]:
    target = json.loads(TARGET_RESULT.read_text())
    target_scan = target["scan"]
    fields = (
        "connected_graphs",
        "graph6_stream_sha256",
        "raw_static_full_pairs",
        "gamma_alpha_three_graphs_with_static_full_pair",
        "gamma_alpha_three_static_full_pairs",
        "eternal_three_graphs_among_those_candidates",
        "equality_static_pairs_in_eternal_graphs",
        "equality_static_pair_family_list_size_histogram",
        "greatest_family_full_pairs",
    )
    order_matches = []
    for ours, theirs in zip(replay["orders"], target_scan["orders"], strict=True):
        order_matches.append(
            {
                "order": ours["order"],
                "all_compared_fields_match": all(
                    ours[field] == theirs[field] for field in fields
                ),
            }
        )
    return {
        "order_matches": order_matches,
        "totals_match": replay["totals"] == target_scan["totals"],
        "histogram_matches": (
            replay["equality_static_pair_family_list_size_histogram"]
            == target_scan["equality_static_pair_family_list_size_histogram"]
        ),
    }


def run(max_order: int) -> dict[str, object]:
    started = time.monotonic()
    replay = scan(max_order)
    return {
        "status": "INDEPENDENT_REPLAY_COMPLETE",
        "claim_boundary": (
            "Certificate support for the connected-unlabeled finite predicate "
            "only; no universal theorem or counterexample frontier."
        ),
        "max_order": max_order,
        "scan": replay,
        "target_comparison": compare_target(replay),
        "controls": {
            "order12_full_list": order12_control(),
            "FDzro_proper_family": fd_zro_control(),
            "HCQebjw_static_not_family": hcqebjw_control(),
            "abstract": abstract_controls(),
        },
        "source_binding": {
            "target_note_sha256": digest(TARGET_NOTE),
            "target_probe_sha256": digest(TARGET_PROBE),
            "target_result_sha256": digest(TARGET_RESULT),
            "replay_script_sha256": digest(Path(__file__)),
            "geng_sha256": digest(GENG),
            "labelg_sha256": digest(LABELG),
        },
        "elapsed_seconds": time.monotonic() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=9)
    args = parser.parse_args()
    if not 1 <= args.max_order <= 9:
        raise SystemExit("--max-order must be between 1 and 9")
    print(json.dumps(run(args.max_order), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
