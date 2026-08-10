#!/usr/bin/env python3
"""Independent exact support-deck and ordinary-T coherence verifier.

The script derives its cores and repair sets from ``verify_root_probe`` and
never imports project code.  It compares all alternate support presentations
with two extra labelled ports and separately exhausts three-port word-order
reconstruction on every relevant segment count.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, Iterator, Mapping, Optional, Sequence, Tuple

from verify_root_probe import (
    EventCore,
    MixedGraph,
    canonical_json_bytes,
    derive_cycle_event_core,
    derive_theta_event_cores,
    edge_key,
    graph_from_core,
    local_tail_criterion,
    mixed_automorphism_count,
    powerset,
    sha256_bytes,
)


def minimum_repairs(core: EventCore) -> Tuple[FrozenSet[str], ...]:
    segment_ids = sorted(seg.id for seg in core.segments)
    good = []
    for occupied in powerset(segment_ids):
        graph = graph_from_core(core, occupied)
        if graph is not None and local_tail_criterion(graph):
            good.append(occupied)
    minimal = [row for row in good if not any(other < row for other in good)]
    return tuple(sorted(minimal, key=lambda row: (len(row), sorted(row))))


def graph_from_words(
    core: EventCore,
    words: Mapping[str, Sequence[str]],
    sink_labels: Mapping[str, str],
) -> Optional[MixedGraph]:
    graph = MixedGraph({}, {})
    retics = {
        node for node, role in core.node_roles.items()
        if role in {"sink", "branch_retic"}
    }
    for node in core.node_roles:
        graph.add_node(node, reticulation=node in retics)
    for seg in core.segments:
        chain = [seg.tail]
        for position, label in enumerate(words.get(seg.id, ())):
            word_node = f"W:{seg.id}:{position}:{label}"
            leaf = f"L:{label}"
            graph.add_node(word_node)
            graph.add_node(leaf, label=label)
            if not graph.add_edge(word_node, leaf):
                return None
            chain.append(word_node)
        chain.append(seg.head)
        for u, v in zip(chain, chain[1:]):
            marks = (v,) if graph.nodes[v].reticulation else ()
            if not graph.add_edge(u, v, marks):
                return None
    graph.add_node("L:IN", label="IN")
    if not graph.add_edge("S", "L:IN"):
        return None
    for sink, label in sorted(sink_labels.items()):
        leaf = f"L:{label}"
        graph.add_node(leaf, label=label)
        if not graph.add_edge(sink, leaf):
            return None
    return graph


def refine_colours(graph: MixedGraph) -> Dict[str, int]:
    raw = {}
    for node, data in graph.nodes.items():
        raw[node] = (
            "leaf" if data.leaf else ("retic" if data.reticulation else "tree"),
            data.label,
            graph.degree(node),
        )
    palette = {value: i for i, value in enumerate(sorted(set(raw.values()), key=repr))}
    colours = {node: palette[value] for node, value in raw.items()}
    while True:
        enriched = {}
        for node in graph.nodes:
            neighbors = []
            for key, marks in graph.incident(node):
                u, v = key
                other = v if node == u else u
                neighbors.append((node in marks, other in marks, colours[other]))
            enriched[node] = (colours[node], tuple(sorted(neighbors)))
        palette = {value: i for i, value in enumerate(sorted(set(enriched.values()), key=repr))}
        new = {node: palette[value] for node, value in enriched.items()}
        same_partition = all(
            (colours[a] == colours[b]) == (new[a] == new[b])
            for a in graph.nodes for b in graph.nodes
        )
        if same_partition:
            return new
        colours = new


def canonical_mixed_code(graph: MixedGraph) -> str:
    colours = refine_colours(graph)
    cells: Dict[int, list[str]] = defaultdict(list)
    for node, colour in colours.items():
        cells[colour].append(node)
    ordered_cells = [tuple(sorted(cells[colour])) for colour in sorted(cells)]
    best = None
    for moved_cells in itertools.product(*(itertools.permutations(cell) for cell in ordered_cells)):
        order = tuple(node for cell in moved_cells for node in cell)
        mapping = {node: i for i, node in enumerate(order)}
        labels = tuple(sorted((mapping[node], data.label) for node, data in graph.nodes.items() if data.leaf))
        retics = tuple(sorted(mapping[node] for node, data in graph.nodes.items() if data.reticulation))
        edges = []
        for (u, v), marks in graph.edges.items():
            a, b = mapping[u], mapping[v]
            if a > b:
                a, b = b, a
            heads = tuple(sorted(mapping[node] for node in marks))
            edges.append((a, b, heads))
        candidate = (labels, retics, tuple(sorted(edges)))
        if best is None or candidate < best:
            best = candidate
    assert best is not None
    return repr(best)


def underlying_triangles(graph: MixedGraph) -> Tuple[Tuple[str, str, str], ...]:
    internal = sorted(node for node, data in graph.nodes.items() if not data.leaf)
    answer = []
    for a, b, c in itertools.combinations(internal, 3):
        if all(edge_key(u, v) in graph.edges for u, v in ((a, b), (a, c), (b, c))):
            answer.append((a, b, c))
    return tuple(answer)


def eligible_ordinary_triangle(graph: MixedGraph, triangle: Sequence[str]) -> bool:
    tri = frozenset(triangle)
    retics = [node for node in tri if graph.nodes[node].reticulation]
    if len(retics) != 1:
        return False
    retic = retics[0]
    for u, v in itertools.combinations(sorted(tri), 2):
        marks = graph.edges[edge_key(u, v)]
        expected = frozenset({retic}) if retic in (u, v) else frozenset()
        if marks != expected:
            return False
    for node in tri:
        outside = [
            (key, marks) for key, marks in graph.incident(node)
            if not set(key).issubset(tri)
        ]
        if len(outside) != 1 or outside[0][1]:
            return False
    return True


def t_quotient_graph(graph: MixedGraph) -> Tuple[MixedGraph, int]:
    eligible = [tri for tri in underlying_triangles(graph) if eligible_ordinary_triangle(graph, tri)]
    if len(eligible) > 1:
        raise AssertionError("more than one eligible ordinary triangle")
    if not eligible:
        return graph, 0
    tri = frozenset(eligible[0])
    quotient = graph.copy()
    for node in tri:
        data = quotient.nodes[node]
        quotient.nodes[node] = type(data)(reticulation=False, label=data.label)
    for key in list(quotient.edges):
        if set(key).issubset(tri):
            quotient.edges[key] = frozenset()
    return quotient, 1


T_CODE_CACHE: Dict[bytes, Tuple[str, int]] = {}


def t_code(graph: MixedGraph) -> Tuple[str, int]:
    cache_key = canonical_json_bytes(graph.record())
    cached = T_CODE_CACHE.get(cache_key)
    if cached is not None:
        return cached
    quotient, triangle_count = t_quotient_graph(graph)
    answer = canonical_mixed_code(quotient), triangle_count
    T_CODE_CACHE[cache_key] = answer
    return answer


def all_ordered_word_distributions(labels: Sequence[str], segment_ids: Sequence[str]) -> Iterator[Dict[str, Tuple[str, ...]]]:
    for assignment in itertools.product(segment_ids, repeat=len(labels)):
        buckets = {seg: [] for seg in segment_ids}
        for label, seg in zip(labels, assignment):
            buckets[seg].append(label)
        choices = [tuple(itertools.permutations(buckets[seg])) if buckets[seg] else ((),) for seg in segment_ids]
        for orders in itertools.product(*choices):
            yield {seg: tuple(order) for seg, order in zip(segment_ids, orders)}


def anchored_expansions(
    segment_ids: Sequence[str],
    repair_labels: Mapping[str, str],
    extras: Sequence[str],
) -> Iterator[Dict[str, Tuple[str, ...]]]:
    for assignment in itertools.product(segment_ids, repeat=len(extras)):
        buckets = {seg: ([repair_labels[seg]] if seg in repair_labels else []) for seg in segment_ids}
        for label, seg in zip(extras, assignment):
            buckets[seg].append(label)
        choices = [tuple(itertools.permutations(buckets[seg])) if buckets[seg] else ((),) for seg in segment_ids]
        for orders in itertools.product(*choices):
            yield {seg: tuple(order) for seg, order in zip(segment_ids, orders)}


def filtered_words(words: Mapping[str, Sequence[str]], selected: FrozenSet[str]) -> Dict[str, Tuple[str, ...]]:
    return {seg: tuple(label for label in row if label in selected) for seg, row in words.items()}


def abstract_three_label_order_check(segment_count: int) -> dict:
    segments = tuple(f"s{i}" for i in range(segment_count))
    labels = ("a", "b", "c")
    signatures = {}
    collisions = []
    total = 0
    for words in all_ordered_word_distributions(labels, segments):
        total += 1
        location = tuple(next(seg for seg in segments if label in words[seg]) for label in labels)
        comparisons = []
        for a, b in itertools.combinations(labels, 2):
            sa = next(seg for seg in segments if a in words[seg])
            sb = next(seg for seg in segments if b in words[seg])
            if sa == sb:
                comparisons.append((a, b, words[sa].index(a) < words[sa].index(b)))
        signature = (location, tuple(comparisons))
        record = tuple((seg, words[seg]) for seg in segments)
        if signature in signatures and signatures[signature] != record:
            collisions.append({"first": signatures[signature], "second": record})
        signatures[signature] = record
    return {
        "segment_count": segment_count,
        "ordered_word_count": total,
        "distinct_probe_signature_count": len(signatures),
        "collision_count": len(collisions),
        "collisions": collisions[:5],
    }


def audit_probe_decks() -> dict:
    cores = [derive_cycle_event_core(), *derive_theta_event_cores()]
    extras = ("P0", "P1")
    groups: Dict[Tuple[str, str, str, str], set[str]] = defaultdict(set)
    group_examples: Dict[Tuple[str, str, str, str], dict] = {}
    commitment = hashlib.sha256()
    presentation_count = 0
    support_count = 0
    max_eligible_triangles = 0
    support_rows = []
    for core_index, core in enumerate(cores):
        segments = tuple(sorted(seg.id for seg in core.segments))
        sinks = tuple(sorted(node for node, role in core.node_roles.items() if role == "sink"))
        for repair_index, repair in enumerate(minimum_repairs(core)):
            q_labels = tuple(f"Q{i}" for i in range(len(sinks) + len(repair)))
            for assignment in itertools.permutations(q_labels):
                sink_labels = dict(zip(sinks, assignment[: len(sinks)]))
                repair_labels = dict(zip(sorted(repair), assignment[len(sinks) :]))
                support_words = {seg: ((repair_labels[seg],) if seg in repair_labels else ()) for seg in segments}
                support_graph = graph_from_words(core, support_words, sink_labels)
                assert support_graph is not None
                support_code, support_triangles = t_code(support_graph)
                if mixed_automorphism_count(support_graph) != 1:
                    raise AssertionError("non-rigid support")
                support_count += 1
                support_rows.append({
                    "core": f"{core.family}-{core.placement}",
                    "repair_index": repair_index,
                    "repair": sorted(repair),
                    "sink_assignment": sorted(sink_labels.items()),
                    "repair_assignment": sorted(repair_labels.items()),
                    "support_t_code_sha256": sha256_bytes(support_code.encode()),
                    "support_has_ordinary_triangle": bool(support_triangles),
                })
                q_set = frozenset(q_labels)
                for words in anchored_expansions(segments, repair_labels, extras):
                    presentation_count += 1
                    codes = []
                    triangle_counts = []
                    for selected in (
                        q_set | {"P0"},
                        q_set | {"P1"},
                        q_set | {"P0", "P1"},
                    ):
                        graph = graph_from_words(core, filtered_words(words, frozenset(selected)), sink_labels)
                        assert graph is not None
                        code, triangles = t_code(graph)
                        codes.append(code)
                        triangle_counts.append(triangles)
                    max_eligible_triangles = max(max_eligible_triangles, *triangle_counts)
                    key = (support_code, codes[0], codes[1], codes[2])
                    full_code = codes[2]
                    groups[key].add(full_code)
                    row = {
                        "core": f"{core.family}-{core.placement}",
                        "repair": sorted(repair),
                        "sink_labels": sorted(sink_labels.items()),
                        "repair_labels": sorted(repair_labels.items()),
                        "words": sorted((seg, list(words[seg])) for seg in segments),
                        "support_code_sha256": sha256_bytes(support_code.encode()),
                        "one_probe_code_sha256": [sha256_bytes(codes[0].encode()), sha256_bytes(codes[1].encode())],
                        "two_probe_code_sha256": sha256_bytes(codes[2].encode()),
                        "triangle_counts": triangle_counts,
                    }
                    commitment.update(canonical_json_bytes(row))
                    group_examples.setdefault(key, row)
    collisions = []
    # With exactly two extra labels the two-port probe is the full graph, so a
    # disagreement here would expose a canonicalization inconsistency.  The
    # independent three-label check below verifies the nontrivial assembly of
    # all pair orders for longer words.
    for key, full_codes in groups.items():
        if len(full_codes) > 1:
            collisions.append({
                "probe_key_hashes": [sha256_bytes(code.encode()) for code in key],
                "full_code_hashes": sorted(sha256_bytes(code.encode()) for code in full_codes),
                "example": group_examples[key],
            })
    return {
        "support_presentation_count": support_count,
        "two_extra_port_presentation_count": presentation_count,
        "probe_group_count": len(groups),
        "coherence_collision_count": len(collisions),
        "coherence_collisions": collisions[:10],
        "max_eligible_triangle_count_in_any_probe": max_eligible_triangles,
        "presentation_commitment_sha256": commitment.hexdigest(),
        "support_presentations": support_rows,
        "abstract_three_extra_label_checks": [
            abstract_three_label_order_check(m) for m in (2, 5, 6)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("probe_coherence_certificate.json"))
    args = parser.parse_args()
    payload = {
        "schema": "probe-coherence-clean-room-v1",
        **audit_probe_decks(),
    }
    raw = canonical_json_bytes(payload)
    args.output.write_bytes(raw)
    print(json.dumps({
        "output": str(args.output),
        "sha256": sha256_bytes(raw),
        "supports": payload["support_presentation_count"],
        "presentations": payload["two_extra_port_presentation_count"],
        "collisions": payload["coherence_collision_count"],
        "three_label_checks": payload["abstract_three_extra_label_checks"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
