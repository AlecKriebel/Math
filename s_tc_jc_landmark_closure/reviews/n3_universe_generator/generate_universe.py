#!/usr/bin/env python3
"""Independent theorem-forced generation of the complete n3 relation gate.

This verifier does not import the primary completion, support, relation,
graph, Fourier, invariant, or canonicalization engines.  It reuses only the
already-independent exact four-port algebra routines from the theta-2
referee.  Primitive cores are explicit in that referee module.  The primary
relation stream is read solely as a claim whose normalized raw and merged
multisets must agree exactly with the independently generated ones.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys
from typing import Iterable, Sequence


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent.parent
INDEPENDENT_ENGINE = PROJECT / "reviews/theta2_signature_gate/verify_gate.py"
PRIMARY_RELATIONS = (
    PROJECT
    / "primary/certificates/"
    "bounded_relation_n3_schema3_n3_all_filtered_relations.jsonl.gz"
)
CERTIFICATE = HERE / "n3_universe_certificate.json"
RAW_STREAM = HERE / "n3_normalized_raw_relations.jsonl.gz"
MERGED_STREAM = HERE / "n3_normalized_merged_relations.jsonl.gz"


def load_independent_engine():
    spec = importlib.util.spec_from_file_location("theta2_independent_engine", INDEPENDENT_ENGINE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load independent theta-2 algebra engine")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


E = load_independent_engine()
CORES = E.CORES
INCOMING = E.INCOMING


def stable_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def natural(label: str):
    prefix, _, suffix = label.rpartition("_")
    return prefix, int(suffix) if suffix.isdigit() else -1, label


def source_support_candidates() -> Iterable[dict]:
    """Generate every minimal support with exactly three outgoing ports."""
    for core_name, core in CORES.items():
        arcs = core["arcs"]
        _, sinks = E.source_and_sinks(arcs)
        for repair_index, repair in enumerate(core["repairs"]):
            support_size = len(sinks) + len(repair)
            extras = 3 - support_size
            if extras < 0:
                continue
            for placements in itertools.product(range(len(arcs)), repeat=extras):
                letters = {index: [] for index in range(len(arcs))}
                for position, edge_index in enumerate(repair):
                    letters[edge_index].append(f"Q_REPAIR_{position}")
                for extra_index, edge_index in enumerate(placements):
                    letters[edge_index].append(f"P_{extra_index}")
                order_choices = [
                    tuple(itertools.permutations(values)) if values else ((),)
                    for values in letters.values()
                ]
                for ordered in itertools.product(*order_choices):
                    words = tuple(tuple(row) for row in ordered)
                    sink_labels = {
                        sink: f"Q_SINK_{index}" for index, sink in enumerate(sinks)
                    }
                    graph = E.build_graph(arcs, words, sink_labels)
                    labels = tuple(
                        sorted(
                            (label for _, label in graph.labels if label != INCOMING),
                            key=natural,
                        )
                    ) + (INCOMING,)
                    yield {
                        "core": core_name,
                        "repair_index": repair_index,
                        "words": words,
                        "sink_labels": sink_labels,
                        "graph": graph,
                        "selected_labels": labels,
                    }


def rooted_payload(graph, relabel: dict[str, str] | None = None) -> dict:
    relabel = relabel or {}
    return {
        "root": int(graph.root),
        "labels": [
            [int(vertex), relabel.get(str(label), str(label))]
            for vertex, label in sorted(graph.labels)
        ],
        "arcs": [[int(u), int(v)] for u, v in sorted(graph.arcs)],
    }


def sd0_payload(graph, relabel: dict[str, str] | None = None) -> dict:
    """Independent exact mixed graph used only to quotient source supports."""
    relabel = relabel or {}
    indegree = Counter(v for _, v in graph.arcs)
    retics = {v for v, degree in indegree.items() if degree == 2}
    children = [v for u, v in graph.arcs if u == graph.root]
    if len(children) != 2:
        raise AssertionError("binary root required")
    undirected = set()
    directed = set()
    for u, v in graph.arcs:
        if u == graph.root:
            continue
        if v in retics:
            directed.add((u, v))
        else:
            undirected.add(tuple(sorted((u, v))))
    a, b = children
    if a in retics and b in retics:
        raise AssertionError("root with two reticulation children")
    if a in retics:
        directed.add((b, a))
    elif b in retics:
        directed.add((a, b))
    else:
        undirected.add(tuple(sorted((a, b))))
    labels = {
        int(vertex): relabel.get(str(label), str(label))
        for vertex, label in graph.labels
    }
    vertices = sorted(
        ({u for edge in undirected for u in edge}
         | {u for edge in directed for u in edge}
         | set(labels))
        - {graph.root}
    )
    return {
        "vertices": vertices,
        "labels": labels,
        "undirected": tuple(sorted(undirected)),
        "directed": tuple(sorted(directed)),
    }


def refine_partition(mixed: dict, partition: tuple[tuple[int, ...], ...]):
    undirected = defaultdict(set)
    parents = defaultdict(set)
    children = defaultdict(set)
    for u, v in mixed["undirected"]:
        undirected[u].add(v)
        undirected[v].add(u)
    for u, v in mixed["directed"]:
        children[u].add(v)
        parents[v].add(u)
    current = partition
    while True:
        cell_of = {vertex: index for index, cell in enumerate(current) for vertex in cell}
        split = []
        for cell in current:
            buckets = defaultdict(list)
            for vertex in cell:
                signature = (
                    tuple(sorted(cell_of[x] for x in undirected[vertex])),
                    tuple(sorted(cell_of[x] for x in parents[vertex])),
                    tuple(sorted(cell_of[x] for x in children[vertex])),
                )
                buckets[signature].append(vertex)
            for signature in sorted(buckets, key=repr):
                split.append(tuple(sorted(buckets[signature])))
        moved = tuple(split)
        if moved == current:
            return moved
        current = moved


def canonical_mixed_code(mixed: dict) -> str:
    labels = mixed["labels"]
    indegree = Counter(v for _, v in mixed["directed"])
    outdegree = Counter(u for u, _ in mixed["directed"])
    cells = defaultdict(list)
    for vertex in mixed["vertices"]:
        if vertex in labels:
            colour = ("leaf", labels[vertex])
        else:
            colour = ("internal", indegree[vertex], outdegree[vertex])
        cells[colour].append(vertex)
    initial = tuple(tuple(sorted(cells[key])) for key in sorted(cells, key=repr))
    best = None

    def recurse(partition):
        nonlocal best
        partition = refine_partition(mixed, partition)
        if all(len(cell) == 1 for cell in partition):
            order = [cell[0] for cell in partition]
            moved = {vertex: index for index, vertex in enumerate(order)}
            code = (
                tuple(labels.get(vertex) for vertex in order),
                tuple(sorted(tuple(sorted((moved[u], moved[v]))) for u, v in mixed["undirected"])),
                tuple(sorted((moved[u], moved[v]) for u, v in mixed["directed"])),
            )
            if best is None or code < best:
                best = code
            return
        cell_index = min(
            (index for index, cell in enumerate(partition) if len(cell) > 1),
            key=lambda index: (len(partition[index]), partition[index]),
        )
        cell = partition[cell_index]
        for vertex in cell:
            rest = tuple(x for x in cell if x != vertex)
            moved = partition[:cell_index] + ((vertex,), rest) + partition[cell_index + 1 :]
            recurse(moved)

    recurse(initial)
    if best is None:
        raise AssertionError("canonicalization failed")
    return json.dumps(best, separators=(",", ":"))


def generate_sources() -> tuple[dict, ...]:
    records = {}
    for row in source_support_candidates():
        key = (row["core"], canonical_mixed_code(sd0_payload(row["graph"])))
        provenance_key = (row["repair_index"], row["words"])
        prior = records.get(key)
        if prior is None or provenance_key < (prior["repair_index"], prior["words"]):
            records[key] = row
    answer = tuple(records[key] for key in sorted(records, key=repr))
    if len(answer) != 8:
        raise AssertionError(("source-support-count", len(answer)))
    return answer


def generate_completions() -> Iterable[dict]:
    """All selected-incoming n=3 and marginalized-incoming n=4 witnesses."""
    for incoming_selected, selected_count in ((True, 3), (False, 4)):
        for core_name, core in CORES.items():
            arcs = core["arcs"]
            _, sinks = E.source_and_sinks(arcs)
            for sink_mask in range(1 << len(sinks)):
                selected_sinks = [
                    sink for index, sink in enumerate(sinks) if sink_mask & (1 << index)
                ]
                ordinary = selected_count - len(selected_sinks)
                if ordinary < 0:
                    continue
                for counts in E.weak_compositions(ordinary, len(arcs)):
                    label_iter = iter(f"O_{index}" for index in range(ordinary))
                    selected_words = tuple(
                        tuple(next(label_iter) for _ in range(count)) for count in counts
                    )
                    repair_rows = (
                        ((None, ()),)
                        if core_name == "cycle"
                        else tuple(enumerate(core["repairs"]))
                    )
                    for repair_index, repair in repair_rows:
                        words = [list(word) for word in selected_words]
                        dummies = [INCOMING] if not incoming_selected else []
                        for edge_index in repair:
                            if not words[edge_index]:
                                dummy = f"D_REPAIR_{repair_index}_{edge_index}"
                                words[edge_index].append(dummy)
                                dummies.append(dummy)
                        sink_labels = {}
                        for index, sink in enumerate(sinks):
                            if sink in selected_sinks:
                                sink_labels[sink] = f"SINK_{index}"
                            else:
                                dummy = f"D_SINK_{index}"
                                sink_labels[sink] = dummy
                                dummies.append(dummy)
                        selected = sorted(
                            [label for word in selected_words for label in word]
                            + [sink_labels[sink] for sink in selected_sinks],
                            key=natural,
                        )
                        if incoming_selected:
                            selected.append(INCOMING)
                        final_words = tuple(tuple(word) for word in words)
                        yield {
                            "core": core_name,
                            "sink_mask": sink_mask,
                            "repair_index": repair_index,
                            "words": final_words,
                            # Dummy roles are structural placeholders, not
                            # selected port positions.  The theorem object
                            # orders them lexicographically.
                            "dummy_labels": tuple(sorted(dummies)),
                            "incoming_selected": incoming_selected,
                            "selected_labels": tuple(selected),
                            "graph": E.build_graph(arcs, final_words, sink_labels),
                        }


def descriptor_bits_for_order(graph, labels: Sequence[str], assignment: Sequence[int], invariants, cache, counters):
    inverse = [0] * 4
    for position, actual in enumerate(assignment):
        inverse[actual] = position
    ordered_labels = tuple(labels[inverse[index]] for index in range(4))
    desc = E.descriptor(graph, ordered_labels)
    return E.descriptor_bits(desc, invariants, cache, counters), desc


def relabel_payload(graph, labels: Sequence[str], assignment: Sequence[int]) -> dict:
    relabel = {label: f"L_{actual}" for label, actual in zip(labels, assignment)}
    return rooted_payload(graph, relabel)


def normalized_raw(
    source: dict,
    source_signature: int,
    target: dict,
    target_assignment: Sequence[int],
) -> dict:
    return {
        "direction": "source_precedes_target",
        "selected_outgoing": 3,
        "selected_signature_sha256": hashlib.sha256(str(source_signature).encode()).hexdigest(),
        "source_position_to_label": [0, 1, 2, 3],
        "source_provenance": [
            source["core"],
            source["repair_index"],
            [list(word) for word in source["words"]],
        ],
        "target_provenance": [
            target["core"],
            target["sink_mask"],
            target["repair_index"],
            [list(word) for word in target["words"]],
            list(target["dummy_labels"]),
            target["incoming_selected"],
        ],
        "target_dummy_roles": list(target["dummy_labels"]),
        "target_position_to_label": list(target_assignment),
    }


def relation_payload(source: dict, target: dict, assignment: Sequence[int]) -> dict:
    source_graph = relabel_payload(source["graph"], source["selected_labels"], (0, 1, 2, 3))
    target_graph = relabel_payload(target["graph"], target["selected_labels"], assignment)
    return {
        "direction": "source_precedes_target",
        "selected_outgoing": 3,
        "source_rooted_graph": source_graph,
        "target_completion_rooted_graph": target_graph,
        "port_correspondence": [[index, index] for index in range(4)],
    }


def generate_universe() -> dict:
    invariants = E.invariant_orbit()
    if len(invariants) != 84:
        raise AssertionError("invariant orbit is not 84")
    cache = {}
    counters = Counter()
    sources = generate_sources()
    source_rows = []
    for source in sources:
        bits, desc = descriptor_bits_for_order(
            source["graph"], source["selected_labels"], (0, 1, 2, 3),
            invariants, cache, counters,
        )
        source_rows.append((source, bits, desc))

    completions = tuple(generate_completions())
    mode_counts = Counter(
        "selected-incoming" if row["incoming_selected"] else "marginalized-incoming"
        for row in completions
    )
    raw_counter = Counter()
    merged = defaultdict(list)
    target_signature_counts = Counter()
    for target in completions:
        for assignment in itertools.permutations(range(4)):
            target_bits, _desc = descriptor_bits_for_order(
                target["graph"], target["selected_labels"], assignment,
                invariants, cache, counters,
            )
            target_signature_counts[target_bits] += 1
            for source, source_bits, _source_desc in source_rows:
                if source_bits & ~target_bits:
                    continue
                normalized = normalized_raw(source, source_bits, target, assignment)
                encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
                raw_counter[encoded] += 1
                relation = relation_payload(source, target, assignment)
                relation_key = json.dumps(relation, sort_keys=True, separators=(",", ":"))
                merged[relation_key].append(encoded)

    return {
        "sources": sources,
        "source_rows": source_rows,
        "completions": completions,
        "mode_counts": mode_counts,
        "raw_counter": raw_counter,
        "merged": merged,
        "target_signature_counts": target_signature_counts,
        "descriptor_cache_count": len(cache),
        "algebra_counters": dict(sorted(counters.items())),
    }


def primary_claim() -> dict:
    raw_counter = Counter()
    groups = []
    classifications = Counter()
    with gzip.open(PRIMARY_RELATIONS, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            classifications[row["classification"]] += 1
            coverage = []
            for raw in row["raw_coverage"]:
                target_roles = raw["target_roles"]
                normalized = {
                    "direction": "source_precedes_target",
                    "selected_outgoing": 3,
                    "selected_signature_sha256": row["source_signature_sha256"],
                    "source_position_to_label": list(raw["source_position_to_label"]),
                    "source_provenance": raw["source_roles"],
                    "target_provenance": target_roles,
                    "target_dummy_roles": target_roles[4],
                    "target_position_to_label": list(raw["target_position_to_label"]),
                }
                encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
                raw_counter[encoded] += 1
                coverage.append(encoded)
            groups.append(tuple(sorted(coverage)))
    return {
        "raw_counter": raw_counter,
        "groups": Counter(groups),
        "classifications": classifications,
    }


def write_gzip_jsonl(path: Path, rows: Iterable[dict]) -> str:
    digest = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            for row in rows:
                line = (json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode()
                handle.write(line)
                digest.update(line)
    return digest.hexdigest()


def compare_and_write(universe: dict, *, write_streams: bool = True) -> dict:
    claim = primary_claim()
    independent_groups = Counter(tuple(sorted(values)) for values in universe["merged"].values())
    missing_raw = claim["raw_counter"] - universe["raw_counter"]
    extra_raw = universe["raw_counter"] - claim["raw_counter"]
    missing_groups = claim["groups"] - independent_groups
    extra_groups = independent_groups - claim["groups"]
    checks = {
        "eight_sources_generated_from_grammar": len(universe["sources"]) == 8,
        "target_modes_are_831_and_1983": universe["mode_counts"] == {
            "selected-incoming": 831,
            "marginalized-incoming": 1983,
        },
        "all_10826_raw_relations_regenerated": sum(universe["raw_counter"].values()) == 10826,
        "raw_normalized_multiset_exact": not missing_raw and not extra_raw,
        "all_10466_merged_relations_regenerated": len(universe["merged"]) == 10466,
        "merged_normalized_multiset_exact": not missing_groups and not extra_groups,
        "primary_coverage_is_10106_single_360_double": Counter(
            len(group) for group in claim["groups"].elements()
        ) == {1: 10106, 2: 360},
    }
    if not all(checks.values()):
        raise AssertionError({
            "checks": checks,
            "missing_raw": list(missing_raw.items())[:2],
            "extra_raw": list(extra_raw.items())[:2],
            "missing_groups": len(missing_groups),
            "extra_groups": len(extra_groups),
        })

    raw_stream_sha = None
    merged_stream_sha = None
    if write_streams:
        raw_stream_sha = write_gzip_jsonl(
            RAW_STREAM,
            (
                {"normalized_relation": json.loads(encoded), "multiplicity": multiplicity}
                for encoded, multiplicity in sorted(universe["raw_counter"].items())
            ),
        )
        merged_stream_sha = write_gzip_jsonl(
            MERGED_STREAM,
            (
                {
                    "relation_payload": json.loads(key),
                    "raw_coverage_sha256": stable_hash(sorted(values)),
                    "raw_coverage_count": len(values),
                }
                for key, values in sorted(universe["merged"].items())
            ),
        )

    return {
        "schema": "independent-n3-universe-v1",
        "status": "VERIFIED",
        "independence": {
            "primary_modules_imported": [],
            "primary_relation_stream_use": "claim comparison only",
            "algebra_engine": str(INDEPENDENT_ENGINE.relative_to(PROJECT)),
            "algebra_engine_role": (
                "already-independent displayed-switching, descendant-mask, exact invariant "
                "and polynomial-zero engine; no primary code"
            ),
        },
        "counts": {
            "source_supports": len(universe["sources"]),
            "selected_incoming_completions": universe["mode_counts"]["selected-incoming"],
            "marginalized_incoming_completions": universe["mode_counts"]["marginalized-incoming"],
            "raw_necessary_relations": sum(universe["raw_counter"].values()),
            "canonical_merged_relations": len(universe["merged"]),
            "descriptor_cache": universe["descriptor_cache_count"],
        },
        "checks": checks,
        "classifications_read_only_after_universe_match": dict(sorted(claim["classifications"].items())),
        "hashes": {
            "primary_claim_sha256": file_hash(PRIMARY_RELATIONS),
            "independent_raw_multiset_sha256": stable_hash(sorted(universe["raw_counter"].items())),
            "primary_raw_multiset_sha256": stable_hash(sorted(claim["raw_counter"].items())),
            "independent_merged_multiset_sha256": stable_hash(sorted(independent_groups.items())),
            "primary_merged_multiset_sha256": stable_hash(sorted(claim["groups"].items())),
            "raw_stream_sha256": raw_stream_sha,
            "merged_stream_sha256": merged_stream_sha,
        },
        "algebra_counters": universe["algebra_counters"],
    }


def mutation_suite(universe: dict) -> dict:
    claim = primary_claim()
    results = {}

    def rejected(name: str, candidate_raw: Counter, candidate_groups: Counter | None = None):
        raw_ok = candidate_raw == claim["raw_counter"]
        group_ok = candidate_groups == claim["groups"] if candidate_groups is not None else True
        results[name] = not (raw_ok and group_ok)

    baseline_groups = Counter(tuple(sorted(values)) for values in universe["merged"].values())
    raw = universe["raw_counter"].copy()
    first = min(raw)
    raw[first] -= 1
    if not raw[first]:
        del raw[first]
    rejected("delete_raw_relation", raw)

    raw = universe["raw_counter"].copy()
    raw[first] += 1
    rejected("duplicate_raw_relation", raw)

    raw = universe["raw_counter"].copy()
    moved = json.loads(first)
    moved["direction"] = "target_precedes_source"
    del raw[first]
    raw[json.dumps(moved, sort_keys=True, separators=(",", ":"))] += 1
    rejected("reverse_direction", raw)

    raw = universe["raw_counter"].copy()
    moved = json.loads(first)
    moved["target_position_to_label"] = list(reversed(moved["target_position_to_label"]))
    del raw[first]
    raw[json.dumps(moved, sort_keys=True, separators=(",", ":"))] += 1
    rejected("alter_port_assignment", raw)

    groups = baseline_groups.copy()
    group = next(iter(groups))
    groups[group] -= 1
    if not groups[group]:
        del groups[group]
    rejected("delete_merged_relation", universe["raw_counter"], groups)

    split_group = next(group for group in baseline_groups if len(group) == 2)
    groups = baseline_groups.copy()
    groups[split_group] -= 1
    groups[(split_group[0],)] += 1
    groups[(split_group[1],)] += 1
    rejected("split_duplicate_coverage", universe["raw_counter"], groups)

    if not all(results.values()):
        raise AssertionError({"mutation_failures": [k for k, v in results.items() if not v]})
    return {
        "schema": "independent-n3-universe-mutations-v1",
        "status": "VERIFIED",
        "mutations": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-streams", action="store_true")
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    args = parser.parse_args()
    universe = generate_universe()
    certificate = compare_and_write(universe, write_streams=not args.no_streams)
    certificate["mutations"] = mutation_suite(universe)
    args.certificate.write_text(json.dumps(certificate, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": certificate["status"],
        "raw": certificate["counts"]["raw_necessary_relations"],
        "merged": certificate["counts"]["canonical_merged_relations"],
        "certificate": str(args.certificate),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
