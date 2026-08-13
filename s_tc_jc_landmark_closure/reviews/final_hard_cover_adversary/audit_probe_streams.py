#!/usr/bin/env python3
"""Clean-room audit of the actual schema-3 theta-2 p/q probe streams.

No primary module is imported.  The verifier checks complete path coverage,
exact parent deletion, standard-strong graph membership, rigid quotient
transports, graph-derived JC witnesses, content hashes, and one-root/one-path
state use.  It emits a fail-closed certificate for the frozen input bytes.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import time

from audit_candidate_full import file_sha, graph_from_row, poly_from_row
from audit_probe_closure import arc_partition
from cleanroom_core import (
    MixedEdge,
    RootedGraph,
    canonical_json,
    canonical_mixed,
    canonical_mixed_with_multiplicity,
    class_audit,
    exact_poly_hash,
    invariant_orbit,
    pullback,
    quartet_descriptor,
    sd0,
    stable_hash,
    t_quotient,
)
from audit_hard_cover import INVARIANT_PATH, PROJECT


HERE = Path(__file__).resolve().parent
SUMMARY = PROJECT / "primary/certificates/probe_extension_theta2_schema3_summary.json"
BASE_SUMMARY = PROJECT / "primary/certificates/hard_cover_schema3_theta2_full_summary.json"

GRAPH_FIELDS = {
    "schema", "graph_id", "rooted_graph", "rooted_valid",
    "rooted_validation_problems", "standard_strong_local",
    "standard_mixed_code", "t_quotient_code",
    "raw_mixed_vertex_to_canonical",
    "raw_t_quotient_vertex_to_canonical", "admissible_internal_arcs",
}
STATE_FIELDS = {
    "schema", "state_id", "stage", "selected_port_count",
    "source_graph_id", "target_graph_id", "classification",
    "probe_classification", "probe_witness", "transport",
    "canonicalization",
}
P_BINDING_FIELDS = {
    "schema", "probe_path_binding_id", "stage", "base_summary",
    "base_state_id", "base_path_binding_id", "restoration_root_id",
    "parent_probe_path_binding_id", "state_id",
    "source_parent_graph_id", "target_parent_graph_id",
    "source_child_graph_id", "target_child_graph_id",
    "source_insertion", "target_insertion",
    "source_deletion_exact_parent", "target_deletion_exact_parent",
    "base_dummy_order", "base_restored_role_to_label",
    "base_transport", "base_canonicalization",
}
Q_BINDING_FIELDS = (
    P_BINDING_FIELDS
    - {"base_transport", "base_canonicalization"}
    | {"parent_transport"}
)
ALLOWED = {"labelled_isomorphism", "ordinary_T"}
SEPARATED = {"generic_polynomial_separation", "strict_open_cube_separation"}


def stream_rows(path: Path):
    digest = hashlib.sha256()
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            digest.update(line.encode())
            yield number, json.loads(line)
    stream_rows.last_digest = digest.hexdigest()


stream_rows.last_digest = ""


def graph_payload(graph: RootedGraph) -> dict:
    return {
        "root": int(graph.root),
        "labels": tuple(sorted(
            (int(vertex), str(label)) for vertex, label in graph.labels
        )),
        "arcs": tuple(sorted((int(u), int(v)) for u, v in graph.arcs)),
    }


def probe_graph_id(graph: RootedGraph) -> str:
    return stable_hash(graph_payload(graph))


def admissible_arcs(graph: RootedGraph) -> tuple[tuple[int, int], ...]:
    indices = arc_partition(graph).get("internal_blob", ())
    return tuple(sorted(graph.arcs[index] for index in indices))


def normalized_graph(graph: RootedGraph) -> RootedGraph:
    payload = graph_payload(graph)
    return RootedGraph(
        payload["root"], payload["labels"], payload["arcs"]
    )


def delete_inserted_port(child: RootedGraph, insertion: dict) -> RootedGraph | None:
    try:
        u, v = (int(value) for value in insertion["subdivided_parent_arc"])
        tree = int(insertion["inserted_tree_vertex"])
        leaf = int(insertion["inserted_leaf_vertex"])
        label = str(insertion["inserted_label"])
    except Exception:
        return None
    required = {(u, tree), (tree, v), (tree, leaf)}
    if not required <= set(child.arcs) or (leaf, label) not in child.labels:
        return None
    arcs = [arc for arc in child.arcs if arc not in required]
    arcs.append((u, v))
    labels = [row for row in child.labels if row != (leaf, label)]
    return RootedGraph(child.root, tuple(sorted(labels)), tuple(sorted(arcs)))


def exact_transport(source: RootedGraph, target: RootedGraph) -> tuple[dict, dict] | None:
    source_mixed = sd0(source)
    target_mixed = sd0(target)
    source_q = t_quotient(source_mixed)
    target_q = t_quotient(target_mixed)
    source_code, source_map, source_multiplicity = canonical_mixed_with_multiplicity(source_q)
    target_code, target_map, target_multiplicity = canonical_mixed_with_multiplicity(target_q)
    if source_code != target_code or source_multiplicity != 1 or target_multiplicity != 1:
        return None
    canonical_to_target = {canonical: raw for raw, canonical in target_map.items()}
    mapping = {
        raw: canonical_to_target[canonical]
        for raw, canonical in source_map.items()
    }
    target_edge_index = {edge: index for index, edge in enumerate(target_q.edges)}
    edge_permutation = []
    for index, edge in enumerate(source_q.edges):
        moved = MixedEdge.make(
            mapping[edge.u], mapping[edge.v],
            (mapping[head] for head in edge.heads()),
        )
        if moved not in target_edge_index:
            return None
        edge_permutation.append((index, target_edge_index[moved]))
    port_transport = tuple(sorted(
        (label, target_q.label_map[mapping[vertex]])
        for vertex, label in source_q.labels
    ))
    source_retics = set(source_mixed.reticulations())
    target_retics = set(target_mixed.reticulations())
    transport = {
        "vertex_transport": tuple(sorted(mapping.items())),
        "t_quotient_edge_permutation": tuple(edge_permutation),
        "port_transport": port_transport,
        "reticulation_vertices_source": tuple(sorted(source_retics)),
        "reticulation_vertices_target": tuple(sorted(target_retics)),
        "reticulation_transport_outside_redirected_triangle": tuple(sorted(
            (vertex, mapping[vertex]) for vertex in source_retics
            if mapping[vertex] in target_retics
        )),
    }
    canonicalization = {
        "source_raw_to_canonical": tuple(sorted(source_map.items())),
        "target_raw_to_canonical": tuple(sorted(target_map.items())),
    }
    return transport, canonicalization


def restricts(child_transport: dict, parent_transport: dict) -> bool:
    child = dict(child_transport["vertex_transport"])
    return all(
        child.get(int(source)) == int(target)
        for source, target in parent_transport["vertex_transport"]
    )


def load_base() -> tuple[dict[str, dict], dict[str, RootedGraph], dict[str, dict], dict]:
    summary = json.loads(BASE_SUMMARY.read_text())
    cover = summary["runs"][0]["hard_cover"]
    state_path = PROJECT / cover["relation_path"]
    graph_path = PROJECT / cover["graph_library_path"]
    base_graphs = {}
    for _, row in stream_rows(graph_path):
        base_graphs[row["graph_id"]] = graph_from_row(row)
    base_states = {}
    paths = {}
    for _, row in stream_rows(state_path):
        base_states[row["state_id"]] = row
        if row["terminal_classification"] not in {
            "support_prefix_labelled_isomorphism",
            "support_prefix_ordinary_T",
        }:
            continue
        for coverage in row["raw_coverage"]:
            paths[coverage["path_binding_id"]] = {
                "state": row,
                "coverage": coverage,
                "source": base_graphs[coverage["source_graph_id"]],
                "target": base_graphs[coverage["target_graph_id"]],
            }
    return base_states, base_graphs, paths, cover


def main() -> int:
    started = time.monotonic()
    summary = json.loads(SUMMARY.read_text())
    stream_paths = {
        name: PROJECT / row["path"]
        for name, row in summary["streams"].items()
    }
    failures = []
    stream_meta = {}
    base_states, base_graphs, base_paths, base_cover = load_base()

    # Exact input-byte binding in the producer summary.
    expected_base_inputs = {
        str(BASE_SUMMARY): file_sha(BASE_SUMMARY),
        str(PROJECT / base_cover["relation_path"]): file_sha(PROJECT / base_cover["relation_path"]),
        str(PROJECT / base_cover["graph_library_path"]): file_sha(PROJECT / base_cover["graph_library_path"]),
    }
    normalized_recorded_inputs = {
        str((PROJECT / key).resolve()) if not Path(key).is_absolute() else str(Path(key).resolve()): value
        for key, value in summary["input_sha256"].items()
    }
    if normalized_recorded_inputs != expected_base_inputs:
        failures.append({"type": "base_input_hash_binding_mismatch"})

    graphs: dict[str, RootedGraph] = {}
    graph_rows: dict[str, dict] = {}
    graph_admissible: dict[str, tuple[tuple[int, int], ...]] = {}
    graph_failures = []
    graph_class_counts = Counter()
    prior = None
    graph_count = 0
    for number, row in stream_rows(stream_paths["graphs"]):
        graph_count += 1
        graph_id = row.get("graph_id")
        if prior is not None and graph_id <= prior:
            failures.append({"type": "graph_stream_not_strictly_sorted", "line": number})
        prior = graph_id
        if set(row) != GRAPH_FIELDS:
            graph_failures.append({"graph_id": graph_id, "type": "closed_schema", "fields": sorted(set(row) ^ GRAPH_FIELDS)})
        graph = graph_from_row(row)
        if probe_graph_id(graph) != graph_id:
            graph_failures.append({"graph_id": graph_id, "type": "content_address"})
        result = class_audit(graph)
        required = (
            result.get("rooted_valid") and result.get("root_is_lsa")
            and result.get("rooted_tree_child")
            and result.get("internal_vertex_audit", {}).get("passes")
            and result.get("internal_vertex_audit", {}).get("leaf_vertices_excluded")
            and result.get("sd0_valid") and result.get("standard_strong_local")
            and result.get("level_at_most_two")
            and int(result.get("triangle_count", 99)) <= 1
        )
        if not required:
            graph_failures.append({"graph_id": graph_id, "type": "class_membership", "audit": result})
        mixed_code, mixed_map = canonical_mixed(sd0(graph))
        t_code, t_map = canonical_mixed(t_quotient(sd0(graph)))
        if row.get("standard_mixed_code") != mixed_code:
            graph_failures.append({"graph_id": graph_id, "type": "mixed_code"})
        if row.get("t_quotient_code") != t_code:
            graph_failures.append({"graph_id": graph_id, "type": "T_code"})
        if tuple(map(tuple, row.get("raw_mixed_vertex_to_canonical", ()))) != tuple(sorted(mixed_map.items())):
            graph_failures.append({"graph_id": graph_id, "type": "mixed_transport"})
        if tuple(map(tuple, row.get("raw_t_quotient_vertex_to_canonical", ()))) != tuple(sorted(t_map.items())):
            graph_failures.append({"graph_id": graph_id, "type": "T_transport"})
        independently_admissible = admissible_arcs(graph)
        if tuple(map(tuple, row.get("admissible_internal_arcs", ()))) != independently_admissible:
            graph_failures.append({"graph_id": graph_id, "type": "admissible_arc_set"})
        graph_class_counts[(result.get("triangle_count"), len(sd0(graph).reticulations()))] += 1
        if graph_id in graphs:
            failures.append({"type": "duplicate_graph_id", "graph_id": graph_id})
        graphs[graph_id] = graph
        graph_rows[graph_id] = row
        graph_admissible[graph_id] = independently_admissible
    graph_stream_sha = stream_rows.last_digest
    if graph_failures:
        failures.append({"type": "graph_audit_failures", "count": len(graph_failures), "examples": graph_failures[:50]})

    polynomials = {}
    prior = None
    polynomial_count = 0
    for number, row in stream_rows(stream_paths["polynomials"]):
        polynomial_count += 1
        identifier = row.get("polynomial_id")
        if prior is not None and identifier <= prior:
            failures.append({"type": "polynomial_stream_not_strictly_sorted", "line": number})
        prior = identifier
        payload = {key: row[key] for key in ("schema", "variable_count", "terms")}
        if stable_hash(payload) != identifier:
            failures.append({"type": "polynomial_content_address", "polynomial_id": identifier})
        if identifier in polynomials:
            failures.append({"type": "duplicate_polynomial_id", "polynomial_id": identifier})
        polynomials[identifier] = poly_from_row(row)
    polynomial_stream_sha = stream_rows.last_digest

    invariants = invariant_orbit(json.loads(INVARIANT_PATH.read_text()))
    state_info = {}
    state_counts = Counter()
    descriptor_cache = {}
    pullback_cache = {}
    transport_cache = {}
    algebra_failures = []
    prior = None
    state_count = 0

    def descriptor(graph_id: str, p: int, quartet: tuple[int, ...]):
        key = graph_id, p, quartet
        if key not in descriptor_cache:
            descriptor_cache[key] = quartet_descriptor(
                graphs[graph_id], tuple(f"L_{index}" for index in range(p)), quartet
            )
        return descriptor_cache[key]

    def exact_pullback(desc, invariant_index):
        key = desc, invariant_index
        if key not in pullback_cache:
            pullback_cache[key] = pullback(desc, invariants[invariant_index])
        return pullback_cache[key]

    def transport_for(source_graph_id: str, target_graph_id: str):
        key = source_graph_id, target_graph_id
        if key not in transport_cache:
            transport_cache[key] = exact_transport(
                graphs[source_graph_id], graphs[target_graph_id]
            )
        return transport_cache[key]

    for number, row in stream_rows(stream_paths["states"]):
        state_count += 1
        state_id = row.get("state_id")
        if prior is not None and state_id <= prior:
            failures.append({"type": "state_stream_not_strictly_sorted", "line": number})
        prior = state_id
        if set(row) != STATE_FIELDS:
            failures.append({"type": "state_closed_schema", "state_id": state_id, "fields": sorted(set(row) ^ STATE_FIELDS)})
        payload = {key: row[key] for key in row if key not in {"schema", "state_id"}}
        if stable_hash(payload) != state_id:
            failures.append({"type": "state_content_address", "state_id": state_id})
        if row["source_graph_id"] not in graphs or row["target_graph_id"] not in graphs:
            failures.append({"type": "state_missing_graph", "state_id": state_id})
            continue
        p = int(row["selected_port_count"])
        expected_labels = {f"L_{index}" for index in range(p)}
        if set(graphs[row["source_graph_id"]].label_map.values()) != expected_labels or set(graphs[row["target_graph_id"]].label_map.values()) != expected_labels:
            failures.append({"type": "state_port_label_set", "state_id": state_id})
        classification = row["classification"]
        state_counts[(row["stage"], classification)] += 1
        if classification in SEPARATED:
            witness = row["probe_witness"]
            try:
                quartet = tuple(combinations(range(p), 4))[int(witness["quartet_chunk"])]
                invariant_index = int(witness["invariant_index"])
                source_poly = exact_pullback(descriptor(row["source_graph_id"], p, quartet), invariant_index)
                target_poly = exact_pullback(descriptor(row["target_graph_id"], p, quartet), invariant_index)
            except Exception as exc:
                algebra_failures.append({"state_id": state_id, "type": "witness_reconstruction", "error": repr(exc)})
            else:
                if classification == "generic_polynomial_separation":
                    identifier = witness.get("source_pullback_id")
                    valid = (
                        bool(source_poly) and not target_poly
                        and identifier in polynomials
                        and exact_poly_hash(source_poly) == witness.get("source_pullback_exact_sha256")
                        and polynomials.get(identifier) == source_poly
                    )
                    if not valid:
                        algebra_failures.append({"state_id": state_id, "type": "generic_graph_polynomial_association"})
                else:
                    algebra_failures.append({"state_id": state_id, "type": "unexpected_strict_row_requires_separate_sign_replay"})
            if row.get("transport") is not None or row.get("canonicalization") is not None:
                algebra_failures.append({"state_id": state_id, "type": "separated_state_has_transport"})
        elif classification in ALLOWED:
            derived = transport_for(row["source_graph_id"], row["target_graph_id"])
            if derived is None:
                algebra_failures.append({"state_id": state_id, "type": "allowed_state_not_rigid_T_equivalent"})
            else:
                transport, canonicalization = derived
                source_code = canonical_mixed(sd0(graphs[row["source_graph_id"]]))[0]
                target_code = canonical_mixed(sd0(graphs[row["target_graph_id"]]))[0]
                expected_class = "labelled_isomorphism" if source_code == target_code else "ordinary_T"
                if classification != expected_class:
                    algebra_failures.append({"state_id": state_id, "type": "allowed_classification_mismatch"})
                if canonical_json(row.get("transport")) != canonical_json(transport):
                    algebra_failures.append({"state_id": state_id, "type": "transport_mismatch"})
                if canonical_json(row.get("canonicalization")) != canonical_json(canonicalization):
                    algebra_failures.append({"state_id": state_id, "type": "canonicalization_mismatch"})
        else:
            algebra_failures.append({"state_id": state_id, "type": "unresolved_or_unknown_classification", "classification": classification})
        if state_id in state_info:
            failures.append({"type": "duplicate_state_id", "state_id": state_id})
        state_info[state_id] = {
            "stage": row["stage"], "p": p,
            "source_graph_id": row["source_graph_id"],
            "target_graph_id": row["target_graph_id"],
            "classification": classification,
            "transport": row.get("transport"),
            "probe_witness": row.get("probe_witness"),
        }
    state_stream_sha = stream_rows.last_digest
    if algebra_failures:
        failures.append({"type": "state_algebra_or_transport_failures", "count": len(algebra_failures), "examples": algebra_failures[:50]})

    # Expected complete p universe from every exact base path.
    expected_p = set()
    base_transport_by_path = {}
    for path_id, base in base_paths.items():
        source_base = normalized_graph(base["source"])
        target_base = normalized_graph(base["target"])
        base_transport_by_path[path_id] = exact_transport(source_base, target_base)
        for source_arc in admissible_arcs(source_base):
            for target_arc in admissible_arcs(target_base):
                expected_p.add(stable_hash({
                    "stage": "A_plus_p", "base_path_binding_id": path_id,
                    "source_arc": source_arc, "target_arc": target_arc,
                }))

    binding_info = {}
    state_to_bindings = defaultdict(list)
    state_to_roots = defaultdict(set)
    actual_p = set()
    actual_q = set()
    binding_failures = []
    prior = None
    binding_count = 0
    for number, row in stream_rows(stream_paths["bindings"]):
        binding_count += 1
        binding_id = row.get("probe_path_binding_id")
        if prior is not None and binding_id <= prior:
            failures.append({"type": "binding_stream_not_strictly_sorted", "line": number})
        prior = binding_id
        expected_fields = P_BINDING_FIELDS if row.get("stage") == "A_plus_p" else Q_BINDING_FIELDS
        if set(row) != expected_fields:
            binding_failures.append({"binding_id": binding_id, "type": "closed_schema", "fields": sorted(set(row) ^ expected_fields)})
        payload = {key: row[key] for key in row if key not in {"schema", "probe_path_binding_id"}}
        if stable_hash(payload) != binding_id:
            binding_failures.append({"binding_id": binding_id, "type": "content_address"})
        state = state_info.get(row.get("state_id"))
        if state is None:
            binding_failures.append({"binding_id": binding_id, "type": "missing_state"})
            continue
        if row["stage"] != state["stage"]:
            binding_failures.append({"binding_id": binding_id, "type": "state_stage"})
        if row["source_child_graph_id"] != state["source_graph_id"] or row["target_child_graph_id"] != state["target_graph_id"]:
            binding_failures.append({"binding_id": binding_id, "type": "state_child_graph"})
        base = base_paths.get(row["base_path_binding_id"])
        if base is None:
            binding_failures.append({"binding_id": binding_id, "type": "missing_base_path"})
            continue
        coverage = base["coverage"]
        if row["base_state_id"] != base["state"]["state_id"] or row["restoration_root_id"] != coverage["root_case_id"]:
            binding_failures.append({"binding_id": binding_id, "type": "base_state_or_root"})
        if row["base_summary"] != str(BASE_SUMMARY.relative_to(PROJECT)):
            binding_failures.append({"binding_id": binding_id, "type": "base_summary_path"})
        if canonical_json(row["base_dummy_order"]) != canonical_json(coverage["dummy_order"]) or canonical_json(row["base_restored_role_to_label"]) != canonical_json(coverage["restored_role_to_label"]):
            binding_failures.append({"binding_id": binding_id, "type": "base_role_binding"})
        source_parent = graphs.get(row["source_parent_graph_id"])
        target_parent = graphs.get(row["target_parent_graph_id"])
        source_child = graphs.get(row["source_child_graph_id"])
        target_child = graphs.get(row["target_child_graph_id"])
        if None in (source_parent, target_parent, source_child, target_child):
            binding_failures.append({"binding_id": binding_id, "type": "missing_binding_graph"})
            continue
        for side, parent, child in (
            ("source", source_parent, source_child),
            ("target", target_parent, target_child),
        ):
            insertion = row[f"{side}_insertion"]
            deleted = delete_inserted_port(child, insertion)
            if deleted != normalized_graph(parent):
                binding_failures.append({"binding_id": binding_id, "type": f"{side}_deletion_parent"})
            if tuple(insertion["subdivided_parent_arc"]) not in graph_admissible[row[f"{side}_parent_graph_id"]]:
                binding_failures.append({"binding_id": binding_id, "type": f"{side}_forbidden_insertion_arc"})
            if insertion["inserted_label"] != f"L_{state['p'] - 1}":
                binding_failures.append({"binding_id": binding_id, "type": f"{side}_inserted_label"})
            if row.get(f"{side}_deletion_exact_parent") is not True:
                binding_failures.append({"binding_id": binding_id, "type": f"{side}_recorded_deletion_flag"})

        if row["stage"] == "A_plus_p":
            if row["parent_probe_path_binding_id"] is not None:
                binding_failures.append({"binding_id": binding_id, "type": "p_has_parent_probe"})
            if normalized_graph(source_parent) != normalized_graph(base["source"]) or normalized_graph(target_parent) != normalized_graph(base["target"]):
                binding_failures.append({"binding_id": binding_id, "type": "p_parent_not_exact_base"})
            base_transport = base_transport_by_path[row["base_path_binding_id"]]
            if base_transport is None:
                binding_failures.append({"binding_id": binding_id, "type": "base_transport_not_rigid"})
            else:
                if canonical_json(row["base_transport"]) != canonical_json(base_transport[0]) or canonical_json(row["base_canonicalization"]) != canonical_json(base_transport[1]):
                    binding_failures.append({"binding_id": binding_id, "type": "base_transport_or_canonicalization"})
                if state["classification"] in ALLOWED and not restricts(state["transport"], base_transport[0]):
                    binding_failures.append({"binding_id": binding_id, "type": "p_transport_not_restricting_base"})
            semantic = stable_hash({
                "stage": "A_plus_p",
                "base_path_binding_id": row["base_path_binding_id"],
                "source_arc": tuple(row["source_insertion"]["subdivided_parent_arc"]),
                "target_arc": tuple(row["target_insertion"]["subdivided_parent_arc"]),
            })
            if semantic in actual_p:
                binding_failures.append({"binding_id": binding_id, "type": "duplicate_semantic_p"})
            actual_p.add(semantic)
        else:
            semantic = stable_hash({
                "stage": "A_plus_p_plus_q",
                "parent_probe_path_binding_id": row["parent_probe_path_binding_id"],
                "source_arc": tuple(row["source_insertion"]["subdivided_parent_arc"]),
                "target_arc": tuple(row["target_insertion"]["subdivided_parent_arc"]),
            })
            if semantic in actual_q:
                binding_failures.append({"binding_id": binding_id, "type": "duplicate_semantic_q"})
            actual_q.add(semantic)
        state_to_bindings[row["state_id"]].append(binding_id)
        state_to_roots[row["state_id"]].add(row["restoration_root_id"])
        binding_info[binding_id] = {
            "stage": row["stage"], "state_id": row["state_id"],
            "base_path_binding_id": row["base_path_binding_id"],
            "root": row["restoration_root_id"],
            "parent": row["parent_probe_path_binding_id"],
            "source_parent_graph_id": row["source_parent_graph_id"],
            "target_parent_graph_id": row["target_parent_graph_id"],
            "source_child_graph_id": row["source_child_graph_id"],
            "target_child_graph_id": row["target_child_graph_id"],
            "source_arc": tuple(row["source_insertion"]["subdivided_parent_arc"]),
            "target_arc": tuple(row["target_insertion"]["subdivided_parent_arc"]),
            "parent_transport": row.get("parent_transport"),
        }
    binding_stream_sha = stream_rows.last_digest

    # Second-pass q-parent and complete q Cartesian cover checks.
    expected_q = set()
    for binding_id, binding in binding_info.items():
        if binding["stage"] != "A_plus_p":
            continue
        state = state_info[binding["state_id"]]
        if state["classification"] not in ALLOWED:
            continue
        for source_arc in graph_admissible[binding["source_child_graph_id"]]:
            for target_arc in graph_admissible[binding["target_child_graph_id"]]:
                expected_q.add(stable_hash({
                    "stage": "A_plus_p_plus_q",
                    "parent_probe_path_binding_id": binding_id,
                    "source_arc": source_arc,
                    "target_arc": target_arc,
                }))
    for binding_id, binding in binding_info.items():
        if binding["stage"] != "A_plus_p_plus_q":
            continue
        parent = binding_info.get(binding["parent"])
        if parent is None or parent["stage"] != "A_plus_p":
            binding_failures.append({"binding_id": binding_id, "type": "q_missing_p_parent"})
            continue
        if (
            binding["base_path_binding_id"] != parent["base_path_binding_id"]
            or binding["root"] != parent["root"]
            or binding["source_parent_graph_id"] != parent["source_child_graph_id"]
            or binding["target_parent_graph_id"] != parent["target_child_graph_id"]
        ):
            binding_failures.append({"binding_id": binding_id, "type": "q_parent_path_or_graph_incoherent"})
        parent_state = state_info[parent["state_id"]]
        if parent_state["classification"] not in ALLOWED:
            binding_failures.append({"binding_id": binding_id, "type": "q_descends_from_separated_p"})
        if canonical_json(binding["parent_transport"]) != canonical_json(parent_state["transport"]):
            binding_failures.append({"binding_id": binding_id, "type": "q_parent_transport_mismatch"})
        state = state_info[binding["state_id"]]
        if state["classification"] in ALLOWED and not restricts(state["transport"], parent_state["transport"]):
            binding_failures.append({"binding_id": binding_id, "type": "q_transport_not_restricting_parent"})

    if actual_p != expected_p:
        binding_failures.append({
            "type": "incomplete_p_cover", "missing": len(expected_p - actual_p),
            "extra": len(actual_p - expected_p),
        })
    if actual_q != expected_q:
        binding_failures.append({
            "type": "incomplete_q_cover", "missing": len(expected_q - actual_q),
            "extra": len(actual_q - expected_q),
        })
    if binding_failures:
        failures.append({"type": "binding_or_coverage_failures", "count": len(binding_failures), "examples": binding_failures[:100]})

    # Schema-3 rooted-identity regression: actual use must remain one exact
    # path/root per state even though algebra bodies are separately reusable.
    multiply_bound_states = {
        state_id: paths for state_id, paths in state_to_bindings.items()
        if len(paths) != 1 or len(state_to_roots[state_id]) != 1
    }
    if multiply_bound_states:
        failures.append({
            "type": "probe_state_merged_across_paths_or_roots",
            "count": len(multiply_bound_states),
            "examples": list(multiply_bound_states.items())[:20],
        })
    if set(state_info) != set(state_to_bindings):
        failures.append({
            "type": "state_binding_bijection_failure",
            "states_without_binding": len(set(state_info) - set(state_to_bindings)),
            "binding_unknown_states": len(set(state_to_bindings) - set(state_info)),
        })

    # Summary stream and count commitments.
    observed_streams = {
        "states": (state_count, state_stream_sha),
        "bindings": (binding_count, binding_stream_sha),
        "graphs": (graph_count, graph_stream_sha),
        "polynomials": (polynomial_count, polynomial_stream_sha),
    }
    for name, (count, digest) in observed_streams.items():
        if summary["streams"][name]["records"] != count or summary["streams"][name]["sha256"] != digest:
            failures.append({"type": "summary_stream_binding", "stream": name})
    observed_counts = {
        f"{stage}::{classification}": count
        for (stage, classification), count in sorted(state_counts.items())
    }
    if observed_counts != summary["counts"]:
        failures.append({"type": "summary_terminal_counts"})
    if summary.get("base_terminal_paths") != len(base_paths):
        failures.append({"type": "summary_base_path_count"})

    payload = {
        "schema": "theta2-schema3-probe-clean-room-v1",
        "status": "FALSE" if failures else "VERIFIED",
        "scope": "actual theta2_schema3 A+p and conditional A+p+q streams",
        "independence": (
            "no primary module imported; graph reduction, admissible arcs, "
            "deletion, transports, JC pullbacks, and Cartesian covers regenerated"
        ),
        "inputs": {
            str(path.relative_to(PROJECT)): file_sha(path)
            for path in (SUMMARY, BASE_SUMMARY, *stream_paths.values())
        },
        "counts": {
            "base_paths": len(base_paths),
            "states": state_count, "bindings": binding_count,
            "graphs": graph_count, "polynomials": polynomial_count,
            "expected_p": len(expected_p), "actual_p": len(actual_p),
            "expected_q": len(expected_q), "actual_q": len(actual_q),
            "state_classes": observed_counts,
            "descriptor_cache": len(descriptor_cache),
            "pullback_cache": len(pullback_cache),
            "multiply_bound_states": len(multiply_bound_states),
        },
        "graph_class_counts": {
            repr(key): value for key, value in sorted(graph_class_counts.items(), key=repr)
        },
        "jacobian_scope": (
            "not applicable: these are separator/isomorphism probe relations; "
            "the schema contains no Jacobian claim or field"
        ),
        "failure_count": len(failures),
        "failures": failures,
        "elapsed_seconds": time.monotonic() - started,
    }
    output = HERE / "schema3_theta2_probe_stream_audit.json"
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "failure_count": len(failures),
        "counts": payload["counts"], "output": str(output),
        "sha256": file_sha(output), "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
