#!/usr/bin/env python3
"""Adversarial combinatorial audit of the proposed arbitrary-port closure.

For every topology-permitting hard-cover terminal this script inserts a new
port p on every and only internal blob arc on both sides.  From each p-pair
that is still labelled-isomorphic or ordinary-T-related it performs the same
exhaustion for q.  The construction is tied to every originating root/path
coverage and explicitly tests triangle-edge subdivisions, same-segment order,
and forbidden root/pendant/sink arcs.

This is deliberately not an algebraic repair.  If primary does not contain
pair-bound graph-to-polynomial records for the generated probes, the theorem
gate remains UNRESOLVED even when this combinatorial census passes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import argparse
import hashlib
import json
from pathlib import Path
import time

from audit_candidate_full import PROJECT, file_sha, graph_from_row, load_jsonl
from cleanroom_core import (
    RootedGraph,
    biconnected_blocks,
    canonical_mixed,
    class_audit,
    sd0,
    stable_hash,
    t_quotient,
    underlying_triangles,
)


HERE = Path(__file__).resolve().parent
ALLOWED = {"support_prefix_labelled_isomorphism", "support_prefix_ordinary_T"}


def arc_partition(graph: RootedGraph) -> dict[str, tuple[int, ...]]:
    indegree, _ = graph.degrees()
    labels = set(graph.label_map)
    mixed = sd0(graph)
    nontrivial_blocks = tuple(block for block in biconnected_blocks(mixed) if len(block) >= 3)
    buckets: dict[str, list[int]] = defaultdict(list)
    for index, (u, v) in enumerate(graph.arcs):
        if u == graph.root:
            buckets["root"].append(index)
        elif v in labels:
            buckets["sink" if indegree[u] == 2 else "pendant"].append(index)
        elif any(u in block and v in block for block in nontrivial_blocks):
            buckets["internal_blob"].append(index)
        else:
            buckets["internal_nonblob"].append(index)
    return {key: tuple(value) for key, value in buckets.items()}


def triangle_arc_indices(graph: RootedGraph) -> tuple[int, ...]:
    triangles = underlying_triangles(sd0(graph))
    edges = {
        frozenset((u, v))
        for triangle in triangles
        for u, v in ((triangle[0], triangle[1]), (triangle[0], triangle[2]), (triangle[1], triangle[2]))
    }
    return tuple(
        index for index, (u, v) in enumerate(graph.arcs)
        if u != graph.root and frozenset((u, v)) in edges
    )


def insert_port(graph: RootedGraph, arc_index: int, label: str) -> RootedGraph:
    if label in graph.label_map.values():
        raise ValueError("duplicate inserted label")
    eligible = set(arc_partition(graph).get("internal_blob", ()))
    if arc_index not in eligible:
        raise ValueError("insertion is not on an internal blob arc")
    u, v = graph.arcs[arc_index]
    subdivision = max(graph.vertices) + 1
    leaf = subdivision + 1
    arcs = list(graph.arcs)
    arcs[arc_index:arc_index + 1] = [(u, subdivision), (subdivision, v), (subdivision, leaf)]
    return RootedGraph(
        graph.root,
        tuple(sorted((*graph.labels, (leaf, label)))),
        tuple(arcs),
    )


def relation_codes(source: RootedGraph, target: RootedGraph) -> tuple[str, str, bool]:
    source_t = canonical_mixed(t_quotient(sd0(source)))[0]
    target_t = canonical_mixed(t_quotient(sd0(target)))[0]
    return source_t, target_t, source_t == target_t


def graph_id(graph: RootedGraph) -> str:
    return stable_hash({"root": graph.root, "labels": graph.labels, "arcs": graph.arcs})


def locked_class(graph: RootedGraph) -> bool:
    row = class_audit(graph)
    return bool(
        row.get("rooted_valid") and row.get("root_is_lsa")
        and row.get("rooted_tree_child")
        and row.get("internal_vertex_audit", {}).get("passes")
        and row.get("internal_vertex_audit", {}).get("leaf_vertices_excluded")
        and row.get("sd0_valid") and row.get("standard_strong_local")
        and row.get("level_at_most_two") and int(row.get("triangle_count", 99)) <= 1
    )


def pair_id(base_state_id: str, source_arc: int, target_arc: int, source: RootedGraph, target: RootedGraph, stage: str) -> str:
    return stable_hash({
        "stage": stage,
        "base_state_id": base_state_id,
        "source_arc_index": source_arc,
        "target_arc_index": target_arc,
        "source_graph_id": graph_id(source),
        "target_graph_id": graph_id(target),
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="candidate_full")
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--output", type=Path, default=HERE / "probe_closure_certificate.json")
    args = parser.parse_args()
    started = time.monotonic()
    state_path = PROJECT / f"primary/certificates/hard_cover_n{args.n}_{args.tag}.jsonl.gz"
    graph_path = PROJECT / f"primary/certificates/hard_cover_graphs_n{args.n}_{args.tag}.jsonl.gz"
    if not state_path.exists() or not graph_path.exists():
        raise SystemExit("candidate_full streams are not complete")
    states, state_meta = load_jsonl(state_path, "state_id")
    graphs, graph_meta = load_jsonl(graph_path, "graph_id")
    allowed_states = {
        state_id: row for state_id, row in states.items()
        if row["terminal_classification"] in ALLOWED
    }

    failures = []
    base_rows = []
    all_p_ids = set()
    allowed_p_records = []
    all_q_ids = set()
    allowed_q_ids = set()
    triangle_p_checks = 0
    same_segment_order_checks = 0

    for state_id, state in sorted(allowed_states.items()):
        # Schema 3 permits no merge across fixed roots or exact rooted graph
        # IDs.  Check that before using any terminal as a probe base.
        for coverage in state["raw_coverage"]:
            path_id = coverage["path_binding_id"]
            if coverage.get("root_case_id") != state.get("fixed_full_root_case_id"):
                failures.append({"type": "probe_base_crosses_fixed_root", "state_id": state_id, "path_id": path_id})
            if coverage.get("source_graph_id") != state.get("source_graph_id"):
                failures.append({"type": "probe_base_crosses_source_rooted_graph", "state_id": state_id, "path_id": path_id})
            if coverage.get("target_graph_id") != state.get("target_graph_id"):
                failures.append({"type": "probe_base_crosses_target_rooted_graph", "state_id": state_id, "path_id": path_id})
            base_binding_id = stable_hash({
                "state_id": state_id,
                "root_case_id": coverage["root_case_id"],
                "path_binding_id": path_id,
                "source_graph_id": coverage["source_graph_id"],
                "target_graph_id": coverage["target_graph_id"],
            })
            source0 = graph_from_row(graphs[coverage["source_graph_id"]])
            target0 = graph_from_row(graphs[coverage["target_graph_id"]])
            source_partition = arc_partition(source0)
            target_partition = arc_partition(target0)
            source_arcs = source_partition.get("internal_blob", ())
            target_arcs = target_partition.get("internal_blob", ())
            if source_partition.get("internal_nonblob") or target_partition.get("internal_nonblob"):
                failures.append({"type": "unexpected_internal_nonblob_arc", "state_id": state_id, "path_id": path_id})
            source_triangle = set(triangle_arc_indices(source0))
            target_triangle = set(triangle_arc_indices(target0))
            p_expected = len(source_arcs) * len(target_arcs)
            p_records = []
            allowed_for_source = Counter()
            allowed_for_target = Counter()
            for source_arc in source_arcs:
                for target_arc in target_arcs:
                    source_p = insert_port(source0, source_arc, "PROBE_p")
                    target_p = insert_port(target0, target_arc, "PROBE_p")
                    if not locked_class(source_p) or not locked_class(target_p):
                        failures.append({"type": "p_insertion_left_locked_class", "state_id": state_id, "path_id": path_id, "source_arc": source_arc, "target_arc": target_arc})
                    source_t, target_t, allowed = relation_codes(source_p, target_p)
                    identifier = pair_id(base_binding_id, source_arc, target_arc, source_p, target_p, "p")
                    if identifier in all_p_ids:
                        failures.append({"type": "duplicate_p_relation_id", "pair_id": identifier})
                    all_p_ids.add(identifier)
                    record = {
                        "pair_id": identifier,
                        "base_binding_id": base_binding_id,
                        "base_state_id": state_id,
                        "base_root_case_id": coverage["root_case_id"],
                        "base_path_binding_id": path_id,
                        "base_source_internal_arc_count": len(source_arcs),
                        "base_target_internal_arc_count": len(target_arcs),
                        "source_arc_index": source_arc,
                        "target_arc_index": target_arc,
                        "source_graph_id": graph_id(source_p),
                        "target_graph_id": graph_id(target_p),
                        "source_T_sha256": hashlib.sha256(source_t.encode()).hexdigest(),
                        "target_T_sha256": hashlib.sha256(target_t.encode()).hexdigest(),
                        "allowed_topology_terminal": allowed,
                        "source_triangle_edge_subdivided": source_arc in source_triangle,
                        "target_triangle_edge_subdivided": target_arc in target_triangle,
                    }
                    p_records.append(record)
                    if allowed:
                        allowed_for_source[source_arc] += 1
                        allowed_for_target[target_arc] += 1
                        allowed_p_records.append((record, source_p, target_p))
                    if source_arc in source_triangle or target_arc in target_triangle:
                        triangle_p_checks += 1
            if len(p_records) != p_expected:
                failures.append({"type": "p_cartesian_coverage_mismatch", "state_id": state_id, "path_id": path_id})
            if set(allowed_for_source) != set(source_arcs) or set(allowed_for_target) != set(target_arcs):
                failures.append({
                    "type": "p_probe_not_bidirectionally_covering",
                    "state_id": state_id,
                    "path_id": path_id,
                    "source_missing": sorted(set(source_arcs) - set(allowed_for_source)),
                    "target_missing": sorted(set(target_arcs) - set(allowed_for_target)),
                })
            base_rows.append({
                "state_id": state_id,
                "root_case_id": coverage["root_case_id"],
                "path_binding_id": path_id,
                "base_binding_id": base_binding_id,
                "terminal": state["terminal_classification"],
                "source_arc_partition": {key: len(value) for key, value in sorted(source_partition.items())},
                "target_arc_partition": {key: len(value) for key, value in sorted(target_partition.items())},
                "source_triangle_internal_arcs": sorted(source_triangle),
                "target_triangle_internal_arcs": sorted(target_triangle),
                "p_pair_count": len(p_records),
                "p_allowed_count": sum(record["allowed_topology_terminal"] for record in p_records),
                "p_pair_commitment_sha256": stable_hash(p_records),
            })

    # Add q after every topologically allowed p relation.  Inserting p replaces
    # one internal arc by two, so every side must have exactly one more legal
    # internal position.  Choosing either child arc gives the two orders on the
    # same original segment; choosing any other arc gives distinct segments.
    q_rows = []
    for p_record, source_p, target_p in allowed_p_records:
        source_arcs = arc_partition(source_p).get("internal_blob", ())
        target_arcs = arc_partition(target_p).get("internal_blob", ())
        if len(source_arcs) != p_record["base_source_internal_arc_count"] + 1:
            failures.append({"type": "p_did_not_create_two_source_order_intervals", "p_pair_id": p_record["pair_id"]})
        if len(target_arcs) != p_record["base_target_internal_arc_count"] + 1:
            failures.append({"type": "p_did_not_create_two_target_order_intervals", "p_pair_id": p_record["pair_id"]})
        source_allowed = Counter()
        target_allowed = Counter()
        local_ids = []
        for source_arc in source_arcs:
            for target_arc in target_arcs:
                source_q = insert_port(source_p, source_arc, "PROBE_q")
                target_q = insert_port(target_p, target_arc, "PROBE_q")
                if not locked_class(source_q) or not locked_class(target_q):
                    failures.append({"type": "q_insertion_left_locked_class", "p_pair_id": p_record["pair_id"], "source_arc": source_arc, "target_arc": target_arc})
                _source_t, _target_t, allowed = relation_codes(source_q, target_q)
                identifier = pair_id(p_record["pair_id"], source_arc, target_arc, source_q, target_q, "q")
                if identifier in all_q_ids:
                    failures.append({"type": "duplicate_q_relation_id", "pair_id": identifier})
                all_q_ids.add(identifier)
                local_ids.append(identifier)
                if allowed:
                    allowed_q_ids.add(identifier)
                    source_allowed[source_arc] += 1
                    target_allowed[target_arc] += 1
        if set(source_allowed) != set(source_arcs) or set(target_allowed) != set(target_arcs):
            failures.append({
                "type": "q_probe_not_bidirectionally_covering",
                "p_pair_id": p_record["pair_id"],
                "source_missing": sorted(set(source_arcs) - set(source_allowed)),
                "target_missing": sorted(set(target_arcs) - set(target_allowed)),
            })
        # At least two source insertion sites adjacent to PROBE_p must exist;
        # they encode q-before-p and p-before-q on the original segment.
        p_leaf_source = next(vertex for vertex, label in source_p.labels if label == "PROBE_p")
        p_parent_source = next(u for u, v in source_p.arcs if v == p_leaf_source)
        adjacent_source = [
            index for index, (u, v) in enumerate(source_p.arcs)
            if p_parent_source in (u, v) and v != p_leaf_source and index in source_arcs
        ]
        if len(adjacent_source) != 2:
            failures.append({"type": "same_segment_two_order_failure", "p_pair_id": p_record["pair_id"], "side": "source"})
        else:
            same_segment_order_checks += 2
        q_rows.append({
            "p_pair_id": p_record["pair_id"],
            "source_q_positions": len(source_arcs),
            "target_q_positions": len(target_arcs),
            "q_pair_count": len(local_ids),
            "q_pair_commitment_sha256": stable_hash(sorted(local_ids)),
        })

    # Mutation-sensitive exact-set validators.  These mutate only reviewer
    # records; primary is never changed.
    mutations = []
    expected_p = set(all_p_ids)
    expected_q = set(all_q_ids)

    def mutation(name: str, detected: bool, reason: str):
        mutations.append({"mutation": name, "rejected": bool(detected), "reason": reason})
        if not detected:
            failures.append({"type": "mutation_not_rejected", "mutation": name})

    if expected_p:
        deleted = set(expected_p)
        deleted.remove(min(deleted))
        mutation("delete_p_insertion_position", deleted != expected_p, "exact p relation-ID set changed")
        duplicated = [*sorted(expected_p), min(expected_p)]
        mutation("duplicate_p_insertion_position", len(duplicated) != len(set(duplicated)), "duplicate relation ID detected")
    if expected_q:
        deleted_q = set(expected_q)
        deleted_q.remove(min(deleted_q))
        mutation("delete_q_insertion_position", deleted_q != expected_q, "exact q relation-ID set changed")
    if allowed_p_records:
        record, source_p, target_p = allowed_p_records[0]
        swapped_id = pair_id(
            record["base_binding_id"], record["target_arc_index"], record["source_arc_index"],
            source_p, target_p, "p",
        )
        mutation("swap_source_target_insertion_positions", swapped_id != record["pair_id"], "content-addressed arc roles changed")
        bad_path = "0" * 64
        mutation("inconsistent_base_parent_path", bad_path != record["base_path_binding_id"], "root/path commitment changed")
    if allowed_states:
        state_id, state = next(iter(sorted(allowed_states.items())))
        graph = graph_from_row(graphs[state["source_graph_id"]])
        forbidden = tuple(
            index
            for kind, indices in arc_partition(graph).items()
            if kind != "internal_blob"
            for index in indices
        )
        if forbidden:
            try:
                insert_port(graph, forbidden[0], "PROBE_bad")
            except ValueError:
                detected = True
            else:
                detected = False
            mutation("insert_on_root_pendant_or_sink_arc", detected, "insertion constructor rejects forbidden arc")

    primary_probe_candidates = tuple(sorted(
        path for path in (PROJECT / "primary/certificates").glob("*probe*closure*")
        if path.is_file()
    ))
    algebraically_bound = bool(primary_probe_candidates)
    unresolved_reasons = []
    if not algebraically_bound:
        unresolved_reasons.append(
            "no primary pair-bound probe-closure relation/sign stream exists; combinatorial T-code coverage is not a JC stochastic-containment certificate"
        )
    if not (PROJECT / "primary/certificates/bounded_relations_n4.jsonl.gz").exists():
        unresolved_reasons.append(
            "support-plus-one/two algebra cannot be inherited from the n=4 bounded atlas because its pair-level relation stream is absent"
        )
    if triangle_p_checks == 0:
        unresolved_reasons.append(
            "this terminal stream contains no triangle edge, so it cannot certify the requested ordinary-T edge-subdivision probe case"
        )

    payload = {
        "schema": "hard-cover-probe-closure-adversary-v1",
        "status": "FALSE" if failures else ("VERIFIED" if not unresolved_reasons else "UNRESOLVED"),
        "scope": "all topology-permitting candidate_full terminals; all p and conditional q internal-blob insertions",
        "inputs": {
            str(state_path.relative_to(PROJECT)): file_sha(state_path),
            str(graph_path.relative_to(PROJECT)): file_sha(graph_path),
        },
        "base_terminal_count": len(allowed_states),
        "base_raw_path_binding_count": len(base_rows),
        "base_rows": base_rows,
        "p_relation_count": len(all_p_ids),
        "p_allowed_topology_relation_count": len(allowed_p_records),
        "p_relation_commitment_sha256": stable_hash(sorted(all_p_ids)),
        "q_relation_count": len(all_q_ids),
        "q_allowed_topology_relation_count": len(allowed_q_ids),
        "q_relation_commitment_sha256": stable_hash(sorted(all_q_ids)),
        "q_parent_rows_commitment_sha256": stable_hash(q_rows),
        "triangle_edge_probe_checks": triangle_p_checks,
        "same_segment_order_checks": same_segment_order_checks,
        "forbidden_arc_policy": "root arcs, all pendant arcs, and reticulation-sink leaf arcs excluded; only arcs internal to a nontrivial biconnected block admitted",
        "mutation_tests": mutations,
        "mutation_rejection_count": sum(row["rejected"] for row in mutations),
        "mutation_count": len(mutations),
        "primary_probe_artifacts": [str(path.relative_to(PROJECT)) for path in primary_probe_candidates],
        "unresolved_reasons": unresolved_reasons,
        "failure_count": len(failures),
        "failures": failures,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "bases": len(allowed_states),
        "p_relations": len(all_p_ids),
        "p_allowed": len(allowed_p_records),
        "q_relations": len(all_q_ids),
        "q_allowed": len(allowed_q_ids),
        "mutations_rejected": f"{payload['mutation_rejection_count']}/{payload['mutation_count']}",
        "failure_count": len(failures),
        "output": str(args.output),
        "sha256": file_sha(args.output),
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
