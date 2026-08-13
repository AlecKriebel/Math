#!/usr/bin/env python3
"""Generate every bounded selected pattern induced by a full strong factor."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import json
from pathlib import Path
from typing import Iterable

from core_universe import weak_compositions
from graph_model import RootedGraph, mixed_local_strong, rooted_validation, sd0


HERE = Path(__file__).resolve().parent
CORE_CERT = HERE / "certificates" / "core_universe.json"
OUT = HERE / "certificates" / "completion_universe.json"
INCOMING = "INCOMING"


@dataclass(frozen=True)
class Completion:
    core_id: str
    selected_count: int
    selected_labels: tuple[str, ...]
    dummy_labels: tuple[str, ...]
    selected_sink_mask: int
    repair_index: int | None
    words: tuple[tuple[str, ...], ...]
    graph: RootedGraph
    incoming_selected: bool = True


def source_and_sinks(arcs: tuple[tuple[str, str], ...]) -> tuple[str, tuple[str, ...]]:
    indegree = Counter(v for _, v in arcs)
    outdegree = Counter(u for u, _ in arcs)
    vertices = {x for arc in arcs for x in arc}
    sources = [v for v in vertices if indegree[v] == 0]
    if len(sources) != 1:
        raise AssertionError((arcs, sources))
    sinks = tuple(sorted(v for v in vertices if indegree[v] == 2 and outdegree[v] == 0))
    return sources[0], sinks


def build_graph(
    arcs: tuple[tuple[str, str], ...],
    words: tuple[tuple[str, ...], ...],
    sink_labels: dict[str, str],
) -> RootedGraph:
    ids: dict[tuple, int] = {}

    def vertex(key: tuple) -> int:
        if key not in ids:
            ids[key] = len(ids)
        return ids[key]

    vertices = sorted({x for arc in arcs for x in arc})
    for name in vertices:
        vertex(("core", name))
    source, _ = source_and_sinks(arcs)
    root = vertex(("root",))
    incoming_leaf = vertex(("leaf", INCOMING))
    labels = {incoming_leaf: INCOMING}
    directed: list[tuple[int, int]] = [
        (root, vertex(("core", source))),
        (root, incoming_leaf),
    ]
    for arc_index, ((tail, head), word) in enumerate(zip(arcs, words)):
        prior = vertex(("core", tail))
        for position, label in enumerate(word):
            subdivision = vertex(("subdivision", arc_index, position))
            leaf = vertex(("leaf", label))
            labels[leaf] = label
            directed.extend(((prior, subdivision), (subdivision, leaf)))
            prior = subdivision
        directed.append((prior, vertex(("core", head))))
    for sink, label in sorted(sink_labels.items()):
        leaf = vertex(("sink_leaf", sink))
        labels[leaf] = label
        directed.append((vertex(("core", sink)), leaf))
    return RootedGraph(root, tuple(sorted(labels.items())), tuple(directed))


def core_rows() -> list[dict]:
    data = json.loads(CORE_CERT.read_text())
    answer = []
    for row in data["cores"]:
        arcs = tuple((edge["tail"], edge["head"]) for edge in row["segments"])
        answer.append({
            "id": row["id"],
            "arcs": arcs,
            "repairs": tuple(tuple(int(x) for x in repair) for repair in row["minimum_repairs"]),
        })
    return answer


@lru_cache(maxsize=1)
def core_by_id() -> dict[str, dict]:
    return {row["id"]: row for row in core_rows()}


def selected_retains_strong_core(completion: Completion) -> bool:
    """Whether selected ports retain the original core as a strong factor.

    Dummy leaves make the *full completion* binary/strong; they do not by
    themselves decide whether the selected ports retain the primitive core. In
    particular, a dummy inserted for one chosen minimum repair is irrelevant
    when the selected ports already occupy another minimum repair.  This
    predicate uses the complete repair family and selected sink occupancy.

    This is deliberately not called intrinsic ``S_TC`` membership after an
    arbitrary ``red_*`` reduction.  For example, omitting a cycle sink can
    collapse the selected marginal to a smaller strong tree.  Such a marginal
    does not retain the cycle core and belongs to the support-completion gate.
    """
    core = core_by_id()[completion.core_id]
    _source, sinks = source_and_sinks(core["arcs"])
    all_sinks_selected = completion.selected_sink_mask == (1 << len(sinks)) - 1
    occupied = {
        index
        for index, word in enumerate(completion.words)
        if any(not label.startswith("D_") for label in word)
    }
    return all_sinks_selected and any(set(repair) <= occupied for repair in core["repairs"])


def selected_graph(completion: Completion) -> RootedGraph:
    """Build the intrinsic graph on the selected ports only.

    A completion graph may contain zero-character dummy leaves needed to
    realize the selected tensor inside a full strong factor.  Those leaves do
    not belong to the selected topology.  This constructor removes them at
    the primitive-word level, before any graph canonicalization, so topology
    comparisons never mistake a completion witness for the selected graph.

    The result retains the original rooted binary strong core exactly when
    ``selected_retains_strong_core(completion)`` is true.
    """
    core = core_by_id()[completion.core_id]
    _source, sinks = source_and_sinks(core["arcs"])
    words = tuple(
        tuple(label for label in word if not label.startswith("D_"))
        for word in completion.words
    )
    sink_labels = {
        sink: f"SINK_{index}"
        for index, sink in enumerate(sinks)
        if completion.selected_sink_mask & (1 << index)
    }
    return build_graph(core["arcs"], words, sink_labels)


def completions(selected_count: int) -> Iterable[Completion]:
    """Completions with the structural incoming boundary selected.

    ``selected_count`` counts selected outgoing boundaries; the complete
    selected tensor therefore has ``selected_count + 1`` ports.
    """
    for core in core_rows():
        arcs: tuple[tuple[str, str], ...] = core["arcs"]
        _, sinks = source_and_sinks(arcs)
        for sink_mask in range(1 << len(sinks)):
            selected_sinks = {sink for index, sink in enumerate(sinks) if sink_mask & (1 << index)}
            ordinary = selected_count - len(selected_sinks)
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(arcs)):
                labels = iter(f"O_{i}" for i in range(ordinary))
                selected_words = tuple(tuple(next(labels) for _ in range(count)) for count in counts)
                repairs = core["repairs"]
                # At selected_count >= 3 every cycle occupancy already breaks
                # its parallel core, so one presentation is sufficient.
                indexed_repairs = ((None, ()),) if core["id"] == "cycle" else tuple(enumerate(repairs))
                for repair_index, repair in indexed_repairs:
                    full_words = [list(word) for word in selected_words]
                    dummies = []
                    for arc_index in repair:
                        if not full_words[arc_index]:
                            dummy = f"D_REPAIR_{repair_index}_{arc_index}"
                            full_words[arc_index].append(dummy)
                            dummies.append(dummy)
                    sink_labels = {}
                    for index, sink in enumerate(sinks):
                        if sink in selected_sinks:
                            sink_labels[sink] = f"SINK_{index}"
                        else:
                            dummy = f"D_SINK_{index}"
                            sink_labels[sink] = dummy
                            dummies.append(dummy)
                    selected = tuple(sorted(
                        [label for word in selected_words for label in word]
                        + [sink_labels[sink] for sink in selected_sinks]
                    ))
                    graph = build_graph(arcs, tuple(tuple(word) for word in full_words), sink_labels)
                    yield Completion(
                        core["id"], selected_count, selected, tuple(sorted(dummies)),
                        sink_mask, repair_index, tuple(tuple(word) for word in full_words), graph,
                        True,
                    )


def marginal_incoming_completions(selected_total: int) -> Iterable[Completion]:
    """Completions whose rooted incoming boundary is marginalized.

    The selected tensor has ``selected_total`` real boundaries, all carried
    by ordinary path ports or reticulation-sink ports.  The structural
    incoming leaf remains in the full standard-strong witness with character
    zero.  This case is indispensable for standard semi-directed relations:
    the target's admissible incoming boundary need not belong to a selected
    source support.
    """
    for core in core_rows():
        arcs: tuple[tuple[str, str], ...] = core["arcs"]
        _, sinks = source_and_sinks(arcs)
        for sink_mask in range(1 << len(sinks)):
            selected_sinks = {
                sink for index, sink in enumerate(sinks) if sink_mask & (1 << index)
            }
            ordinary = selected_total - len(selected_sinks)
            if ordinary < 0:
                continue
            for counts in weak_compositions(ordinary, len(arcs)):
                labels = iter(f"O_{i}" for i in range(ordinary))
                selected_words = tuple(
                    tuple(next(labels) for _ in range(count)) for count in counts
                )
                repairs = core["repairs"]
                indexed_repairs = (
                    ((None, ()),)
                    if core["id"] == "cycle"
                    else tuple(enumerate(repairs))
                )
                for repair_index, repair in indexed_repairs:
                    full_words = [list(word) for word in selected_words]
                    dummies = [INCOMING]
                    for arc_index in repair:
                        if not full_words[arc_index]:
                            dummy = f"D_REPAIR_{repair_index}_{arc_index}"
                            full_words[arc_index].append(dummy)
                            dummies.append(dummy)
                    sink_labels = {}
                    for index, sink in enumerate(sinks):
                        if sink in selected_sinks:
                            sink_labels[sink] = f"SINK_{index}"
                        else:
                            dummy = f"D_SINK_{index}"
                            sink_labels[sink] = dummy
                            dummies.append(dummy)
                    selected = tuple(sorted(
                        [label for word in selected_words for label in word]
                        + [sink_labels[sink] for sink in selected_sinks]
                    ))
                    graph = build_graph(
                        arcs, tuple(tuple(word) for word in full_words), sink_labels
                    )
                    yield Completion(
                        core["id"], selected_total, selected,
                        tuple(sorted(dummies)), sink_mask, repair_index,
                        tuple(tuple(word) for word in full_words), graph, False,
                    )


def graph_record(completion: Completion) -> dict:
    return {
        "core_id": completion.core_id,
        "selected_count": completion.selected_count,
        "selected_labels": completion.selected_labels,
        "dummy_labels": completion.dummy_labels,
        "selected_sink_mask": completion.selected_sink_mask,
        "repair_index": completion.repair_index,
        "words": completion.words,
        "root": completion.graph.root,
        "labels": completion.graph.labels,
        "arcs": completion.graph.arcs,
    }


def main() -> None:
    expected = {
        3: (831, 824, 7),
        4: (1983, 1974, 9),
        5: (4155, 4144, 11),
        6: (7909, 7896, 13),
    }
    expected_retaining = {3: 15, 4: 78, 5: 257, 6: 652}
    census = {}
    retention_census = {}
    invalid = []
    hashes = []
    for n in range(3, 7):
        rows = list(completions(n))
        kinds = Counter("cycle" if row.core_id == "cycle" else "theta" for row in rows)
        for index, row in enumerate(rows):
            valid, problems = rooted_validation(row.graph)
            try:
                mixed = sd0(row.graph)
                strong = mixed_local_strong(mixed)
            except ValueError as error:
                strong = False
                problems = (*problems, str(error))
            if not valid or not strong:
                invalid.append({"n": n, "index": index, "problems": problems, "strong": strong})
            hashes.append(hashlib.sha256(json.dumps(graph_record(row), sort_keys=True).encode()).hexdigest())
        actual = (len(rows), kinds["theta"], kinds["cycle"])
        retaining = sum(selected_retains_strong_core(row) for row in rows)
        census[str(n)] = {
            "all": actual[0], "theta": actual[1], "cycle": actual[2],
            "expected": expected[n], "matches": actual == expected[n],
        }
        retention_census[str(n)] = {
            "core_retaining": retaining,
            "non_core_retaining": len(rows) - retaining,
            "expected_core_retaining": expected_retaining[n],
            "matches": retaining == expected_retaining[n],
        }
    payload = {
        "schema": 1,
        "generation_rule": (
            "every selected sink subset; every weak composition of selected ordinary ports over directed "
            "segments; every minimal repair; omitted sink and repair ports restored as zero-character dummies"
        ),
        "census": census,
        "selected_core_retention_census": retention_census,
        "all_full_completions_rooted_valid_and_standard_strong": not invalid,
        "failures": invalid[:20],
        "ordered_graph_record_hash": hashlib.sha256("".join(hashes).encode()).hexdigest(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    if (
        invalid
        or not all(row["matches"] for row in census.values())
        or not all(row["matches"] for row in retention_census.values())
    ):
        raise SystemExit("completion census failed")
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
