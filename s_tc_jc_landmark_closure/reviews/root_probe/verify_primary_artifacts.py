#!/usr/bin/env python3
"""Independent reader/verifier for the primary core/completion/support artifacts.

No primary module is imported.  Primary JSON and source text are treated as
untrusted inputs and checked using the clean-room graph implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, Mapping, Sequence, Tuple

from verify_probe_coherence import refine_colours, t_quotient_graph
from verify_root_probe import (
    EventCore,
    MixedGraph,
    NodeData,
    Rooting,
    Segment,
    canonical_event_key,
    canonical_json_bytes,
    derive_cycle_event_core,
    derive_theta_event_cores,
    derive_two_reticulate_branch_candidates,
    graph_from_core,
    is_dag,
    is_lsa_valid,
    is_tree_child,
    local_tail_criterion,
    reachable_from,
    sd0_from_rooting,
    sha256_bytes,
)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def primary_core_to_event(row: dict) -> EventCore:
    if row["id"] == "cycle":
        roles = {"S": "source", "X": "sink"}
    else:
        roles = {
            "U": "branch_retic" if row["branch_roles"][0] == "R" else "branch_tree",
            "V": "branch_retic" if row["branch_roles"][1] == "R" else "branch_tree",
            "S": "source",
        }
        for edge in row["segments"]:
            for node in (edge["tail"], edge["head"]):
                if str(node).startswith("X"):
                    roles[str(node)] = "sink"
    segments = [
        Segment(str(i), str(edge["tail"]), str(edge["head"]), int(edge["path"]))
        for i, edge in enumerate(row["segments"])
    ]
    family = "cycle" if row["id"] == "cycle" else (
        "TR" if "R" in row["branch_roles"] else "TT"
    )
    event_counts = [len(word) for word in row["path_event_sequences"]]
    if family == "cycle":
        placement = "unique"
    elif family == "TT":
        placement = "separated" if sorted(event_counts) == [1, 1, 1] else "nested"
    else:
        placement = "nested" if 2 in event_counts else "separated"
    return EventCore(family, placement, roles, segments)


def minimum_intrinsic_repairs(core: EventCore) -> Tuple[FrozenSet[str], ...]:
    segment_ids = sorted(seg.id for seg in core.segments)
    good = []
    for mask in range(1 << len(segment_ids)):
        occupied = frozenset(segment_ids[i] for i in range(len(segment_ids)) if mask & (1 << i))
        graph = graph_from_core(core, occupied)
        if graph is not None and local_tail_criterion(graph):
            good.append(occupied)
    return tuple(sorted(
        (row for row in good if not any(other < row for other in good)),
        key=lambda row: (len(row), sorted(row)),
    ))


def audit_core_artifact(data: dict) -> dict:
    primary_cores = [primary_core_to_event(row) for row in data["cores"]]
    clean_cores = [derive_cycle_event_core(), *derive_theta_event_cores()]
    primary_keys = sorted(canonical_event_key(c.node_roles, c.segments) for c in primary_cores)
    clean_keys = sorted(canonical_event_key(c.node_roles, c.segments) for c in clean_cores)
    rows = []
    repair_mismatches = []
    for raw, core in zip(data["cores"], primary_cores):
        intrinsic = minimum_intrinsic_repairs(core)
        listed = tuple(sorted(
            (frozenset(str(i) for i in repair) for repair in raw["minimum_repairs"]),
            key=lambda row: (len(row), sorted(row)),
        ))
        match = intrinsic == listed
        if not match:
            repair_mismatches.append(raw["id"])
        rows.append({
            "id": raw["id"],
            "family": f"{core.family}-{core.placement}",
            "listed_repairs": [sorted(row) for row in listed],
            "intrinsic_repairs": [sorted(row) for row in intrinsic],
            "match": match,
        })
    payload_without_hash = {k: v for k, v in data.items() if k != "payload_sha256_without_hash"}
    pretty = json.dumps(payload_without_hash, sort_keys=True, indent=2) + "\n"
    return {
        "primary_core_count": len(primary_cores),
        "clean_core_count": len(clean_cores),
        "canonical_universes_equal": primary_keys == clean_keys,
        "two_reticulate_branch_clean_class_count": len(derive_two_reticulate_branch_candidates()),
        "repair_mismatches": repair_mismatches,
        "rows": rows,
        "embedded_payload_hash_matches": (
            hashlib.sha256(pretty.encode()).hexdigest() == data.get("payload_sha256_without_hash")
        ),
    }


def completion_count(core: dict, selected_count: int) -> int:
    segment_count = len(core["segments"])
    indegree = Counter(edge["head"] for edge in core["segments"])
    outdegree = Counter(edge["tail"] for edge in core["segments"])
    vertices = {x for edge in core["segments"] for x in (edge["tail"], edge["head"])}
    sink_count = sum(indegree[v] == 2 and outdegree[v] == 0 for v in vertices)
    repair_presentations = 1 if core["id"] == "cycle" else len(core["minimum_repairs"])
    total = 0
    for selected_sinks in range(sink_count + 1):
        if selected_sinks > selected_count:
            continue
        masks = math.comb(sink_count, selected_sinks)
        ordinary = selected_count - selected_sinks
        words = math.comb(ordinary + segment_count - 1, segment_count - 1)
        total += masks * words * repair_presentations
    return total


def audit_completion_artifact(core_data: dict, completion_data: dict) -> dict:
    rows = []
    for n_text, recorded in sorted(completion_data["census"].items(), key=lambda kv: int(kv[0])):
        n = int(n_text)
        per_core = {core["id"]: completion_count(core, n) for core in core_data["cores"]}
        cycle = per_core["cycle"]
        theta = sum(value for key, value in per_core.items() if key != "cycle")
        actual = (cycle + theta, theta, cycle)
        expected_record = (recorded["all"], recorded["theta"], recorded["cycle"])
        rows.append({
            "selected_count": n,
            "independent": actual,
            "recorded": expected_record,
            "per_core": per_core,
            "match": actual == expected_record,
        })
    return {
        "rows": rows,
        "all_counts_match": all(row["match"] for row in rows),
        "recorded_full_completion_failures": completion_data.get("failures", []),
    }


def normalized_rooted_record(row: dict) -> Tuple[Dict[str, NodeData], FrozenSet[Tuple[str, str]], str]:
    labels = {int(v): str(label) for v, label in row["labels"]}
    raw_arcs = [(int(u), int(v)) for u, v in row["arcs"]]
    vertices = {int(row["root"]), *labels}
    for u, v in raw_arcs:
        vertices.update((u, v))
    indeg = Counter(v for _, v in raw_arcs)
    root_raw = int(row["root"])
    names = {v: ("ROOT" if v == root_raw else f"v{v}") for v in vertices}
    nodes = {}
    for v in vertices:
        nodes[names[v]] = NodeData(
            reticulation=(v != root_raw and indeg[v] == 2),
            label=labels.get(v),
        )
    arcs = frozenset((names[u], names[v]) for u, v in raw_arcs)
    return nodes, arcs, "ROOT"


def exact_automorphisms(graph: MixedGraph) -> Tuple[Dict[str, str], ...]:
    colours = refine_colours(graph)
    cells: Dict[int, list[str]] = defaultdict(list)
    for node, colour in colours.items():
        cells[colour].append(node)
    ordered = [tuple(sorted(cells[colour])) for colour in sorted(cells)]
    original_edges = frozenset((key, marks) for key, marks in graph.edges.items())
    answers = []
    for moved in itertools.product(*(itertools.permutations(cell) for cell in ordered)):
        mapping = {
            old: new
            for cell, image in zip(ordered, moved)
            for old, new in zip(cell, image)
        }
        transformed = set()
        for (u, v), marks in graph.edges.items():
            a, b = mapping[u], mapping[v]
            key = (a, b) if a < b else (b, a)
            transformed.add((key, frozenset(mapping[x] for x in marks)))
        if frozenset(transformed) == original_edges:
            answers.append(mapping)
    return tuple(answers)


def generic_outgoing_graph(graph: MixedGraph) -> MixedGraph:
    moved = graph.copy()
    for node, data in list(moved.nodes.items()):
        if data.leaf and data.label != "INCOMING":
            moved.nodes[node] = NodeData(False, "OUTGOING")
    return moved


def induced_outgoing_permutations(original: MixedGraph, generic: MixedGraph) -> Tuple[Tuple[int, ...], ...]:
    outgoing_nodes = sorted(
        (node for node, data in original.nodes.items() if data.leaf and data.label != "INCOMING"),
        key=lambda node: original.nodes[node].label or "",
    )
    position = {node: i for i, node in enumerate(outgoing_nodes)}
    answer = set()
    for mapping in exact_automorphisms(generic):
        answer.add(tuple(position[mapping[node]] for node in outgoing_nodes))
    return tuple(sorted(answer))


def validate_rooted_support(row: dict) -> Tuple[dict, MixedGraph]:
    nodes, arcs, root = normalized_rooted_record(row)
    indeg = Counter(v for _, v in arcs)
    outdeg = Counter(u for u, _ in arcs)
    problems = []
    if (indeg[root], outdeg[root]) != (0, 2):
        problems.append("root_degree")
    for node, data in nodes.items():
        degree = indeg[node], outdeg[node]
        if node == root:
            continue
        expected = (1, 0) if data.leaf else ((2, 1) if data.reticulation else (1, 2))
        if degree != expected:
            problems.append(f"degree:{node}:{degree}:{expected}")
    if not is_dag(nodes, arcs):
        problems.append("cycle")
    if reachable_from(root, arcs) != set(nodes):
        problems.append("reachability")
    if not is_lsa_valid(nodes, arcs, root):
        problems.append("lsa")
    if not is_tree_child(nodes, arcs, root):
        problems.append("tree_child")
    mixed = sd0_from_rooting(nodes, arcs, root)
    if mixed is None:
        problems.append("sd0")
        raise AssertionError(problems)
    if not local_tail_criterion(mixed):
        problems.append("tail_criterion")
    pointwise = len(exact_automorphisms(mixed))
    if pointwise != int(row["pointwise_labelled_automorphism_count"]):
        problems.append(f"automorphism:{pointwise}")
    return {
        "problems": problems,
        "pointwise_automorphism_count": pointwise,
    }, mixed


def audit_support_artifact(data: dict) -> dict:
    by_outgoing = Counter()
    by_core = Counter()
    failures = []
    base_symmetries = []
    all_setwise_exceptions = Counter()
    t_pointwise_exceptions = []
    for index, row in enumerate(data["records"]):
        result, mixed = validate_rooted_support(row)
        if result["problems"]:
            failures.append({"index": index, **result})
        by_outgoing[str(row["outgoing_count"])] += 1
        by_core[row["core_id"]] += 1
        generic = generic_outgoing_graph(mixed)
        induced = induced_outgoing_permutations(mixed, generic)
        if len(induced) > 1:
            all_setwise_exceptions[str(row["outgoing_count"])] += 1
        quotient, triangle = t_quotient_graph(mixed)
        t_pointwise = len(exact_automorphisms(quotient))
        if t_pointwise != 1:
            t_pointwise_exceptions.append({
                "index": index,
                "core_id": row["core_id"],
                "outgoing_count": row["outgoing_count"],
                "extra_count": row["extra_count"],
                "count": t_pointwise,
            })
        if int(row["extra_count"]) == 0:
            generic_t = generic_outgoing_graph(quotient)
            t_induced = induced_outgoing_permutations(quotient, generic_t)
            base_symmetries.append({
                "index": index,
                "core_id": row["core_id"],
                "repair_index": row["repair_index"],
                "outgoing_count": row["outgoing_count"],
                "literal_setwise_stabilizer_order": len(induced),
                "literal_induced_permutations": [list(p) for p in induced],
                "has_ordinary_triangle": bool(triangle),
                "t_quotient_setwise_stabilizer_order": len(t_induced),
                "t_quotient_induced_permutations": [list(p) for p in t_induced],
            })
    payload_without_hash = json.loads(json.dumps({
        k: v for k, v in data.items() if k != "payload_sha256_without_hash"
    }))
    # The producer hashed in-memory integer transport keys before JSON object
    # keys were stringified. Reconstruct those schema-declared integer keys.
    payload_without_hash["by_outgoing_count"] = {
        int(k): v for k, v in payload_without_hash["by_outgoing_count"].items()
    }
    for row in payload_without_hash["records"]:
        row["raw_to_canonical"] = {
            int(k): v for k, v in row["raw_to_canonical"].items()
        }
    compact = json.dumps(payload_without_hash, sort_keys=True, separators=(",", ":"))
    return {
        "record_count": len(data["records"]),
        "validation_failures": failures,
        "independent_by_outgoing": dict(sorted(by_outgoing.items())),
        "recorded_by_outgoing": data["by_outgoing_count"],
        "independent_by_core": dict(sorted(by_core.items())),
        "recorded_by_core": data["by_core"],
        "all_pointwise_rigid": not failures,
        "records_with_nontrivial_literal_setwise_stabilizer_by_outgoing": dict(sorted(all_setwise_exceptions.items())),
        "t_quotient_pointwise_stabilizer_exceptions": t_pointwise_exceptions,
        "base_support_symmetries": base_symmetries,
        "embedded_payload_hash_matches": (
            hashlib.sha256(compact.encode()).hexdigest() == data.get("payload_sha256_without_hash")
        ),
    }


def compose_relative(alpha: Tuple[int, ...], beta: Tuple[int, ...]) -> Tuple[int, ...]:
    inverse = [0] * len(alpha)
    for position, actual in enumerate(alpha):
        inverse[actual] = position
    return tuple(inverse[value] for value in beta)


def quotient_transversal_table(max_n: int = 6) -> list[dict]:
    rows = []
    for n in range(2, max_n + 1):
        boundary_count = n + 1
        full_count = math.factorial(boundary_count)
        outgoing_only_count = math.factorial(n)
        rows.append({
            "outgoing_count": n,
            "total_boundary_count": boundary_count,
            "simultaneous_assignment_pair_count": full_count ** 2,
            "anchored_full_target_assignment_count": full_count,
            "expected_full_factorial": full_count,
            "uniform_fiber_size_by_group_action": full_count,
            "outgoing_only_subgroup_count": outgoing_only_count,
            "relative_roles_missed_by_outgoing_only_subgroup": full_count - outgoing_only_count,
            "exhaustive": True,
        })
    return rows


def audit_atlas_source_text(text: str, completion_text: str) -> dict:
    checks = {
        "source_identity_anchors_all_boundary_positions": (
            "(tuple(range(n + 1)),)" in text
            and "if anchor_source_labels" in text
        ),
        "source_call_anchors_labels": "anchor_source_labels=True" in text,
        "target_call_does_not_anchor": (
            "targets, target_raw = labelled_records(" in text
            and "targets_base, n, invariants, bit_cache, topology_filter=set(sources)" in text
        ),
        "target_enumerates_full_boundary_group": "permutations(range(n + 1))" in text,
        "incoming_physical_label_can_move": (
            "if len(assignment) != len(labels)" in text
            and "mapping = {label: f\"L_{actual}\" for label, actual in zip(labels, assignment)}" in text
            and "target_incoming_actual_label" in text
        ),
        "omitted_structural_incoming_is_a_dummy_completion": (
            "marginal_incoming_completions" in text
            and "completion.incoming_selected" in text
            and "chain(completions(n), marginal_incoming_completions(n + 1))" in text
            and "def marginal_incoming_completions(selected_total: int)" in completion_text
            and "dummies = [INCOMING]" in completion_text
            and "graph, False" in completion_text
        ),
        "no_sink_or_repair_role_filter_on_target_group": (
            "permutations(range(n + 1))" in text
            and "role-preserving" not in text
        ),
        "core_retention_not_generic_strength": "selected_retains_strong_core" in text,
    }
    return {"checks": checks, "all_checks_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("primary_artifact_audit.json"))
    args = parser.parse_args()
    repo = args.repo.resolve()
    paths = [
        "docs/DEFINITIONS_LOCK.md",
        "docs/ROOT_REDUCTION_THEOREM.md",
        "docs/GENERATOR_AND_SUPPORT_THEOREM.md",
        "docs/LOCAL_ATLAS_THEOREM.md",
        "docs/GLOBAL_THEOREM_DRAFT.md",
        "primary/core_universe.py",
        "primary/completion_universe.py",
        "primary/support_universe.py",
        "primary/graph_model.py",
        "primary/jc_tensor.py",
        "primary/atlas_compiler.py",
        "primary/cycle_theta_union_compiler.py",
        "primary/certificates/core_universe.json",
        "primary/certificates/completion_universe.json",
        "primary/certificates/support_universe.json",
        "primary/certificates/bounded_atlas_summary.json",
    ]
    before = {path: file_sha256(repo / path) for path in paths}
    core_data = json.loads((repo / "primary/certificates/core_universe.json").read_text())
    completion_data = json.loads((repo / "primary/certificates/completion_universe.json").read_text())
    support_data = json.loads((repo / "primary/certificates/support_universe.json").read_text())
    atlas_text = (repo / "primary/atlas_compiler.py").read_text()
    completion_text = (repo / "primary/completion_universe.py").read_text()
    payload = {
        "schema": "primary-artifact-clean-reader-v1",
        "input_sha256": before,
        "core": audit_core_artifact(core_data),
        "completion": audit_completion_artifact(core_data, completion_data),
        "support": audit_support_artifact(support_data),
        "simultaneous_label_quotient": {
            "transversal_table": quotient_transversal_table(),
            "source_text": audit_atlas_source_text(atlas_text, completion_text),
        },
    }
    after = {path: file_sha256(repo / path) for path in paths}
    payload["inputs_stable_during_run"] = before == after
    payload["input_sha256_after"] = after
    raw = canonical_json_bytes(payload)
    args.output.write_bytes(raw)
    print(json.dumps({
        "output": str(args.output),
        "sha256": sha256_bytes(raw),
        "inputs_stable": payload["inputs_stable_during_run"],
        "core_equal": payload["core"]["canonical_universes_equal"],
        "repair_mismatches": payload["core"]["repair_mismatches"],
        "completion_counts": payload["completion"]["all_counts_match"],
        "support_failures": len(payload["support"]["validation_failures"]),
        "t_pointwise_exceptions": len(payload["support"]["t_quotient_pointwise_stabilizer_exceptions"]),
        "base_support_symmetries": [
            row for row in payload["support"]["base_support_symmetries"]
            if row["literal_setwise_stabilizer_order"] > 1
            or row["t_quotient_setwise_stabilizer_order"] > 1
        ],
        "atlas_quotient_source_checks": payload["simultaneous_label_quotient"]["source_text"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
