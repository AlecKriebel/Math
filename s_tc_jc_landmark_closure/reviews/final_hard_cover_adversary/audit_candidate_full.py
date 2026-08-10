#!/usr/bin/env python3
"""Clean-room audit of a final schema-3 fixed-root hard-cover package.

This program imports no primary implementation.  It checks the relation,
graph, polynomial, and root-case streams by content; reconstructs every graph
from each raw fixed relation path; recomputes standard reductions and the
strong tree-child internal-vertex clauses; regenerates every polynomial
pullback from displayed-tree masks; and independently replays factor/Bernstein
strict-sign proofs.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import replace
import argparse
import gzip
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import time

from audit_hard_cover import (
    BIT_CACHE_PATH,
    CORE_PATH,
    INVARIANT_PATH,
    PRODUCER_PATH,
    PROJECT,
    build_inventory,
    file_sha,
    root_key_from_coverage,
    semantic_audit,
    source_graph_for,
    target_graph_for,
)
from cleanroom_core import (
    RootedGraph,
    canonical_json,
    canonical_mixed,
    class_audit,
    descriptor_bits_exact,
    invariant_orbit,
    internal_vertex_audit,
    sd0,
    stable_hash,
    t_quotient,
)


HERE = Path(__file__).resolve().parent
DEFAULT_TAG = "candidate_full"


STATE_REQUIRED = {
    "schema", "state_id", "fixed_full_root_case_id", "selected_port_count",
    "source_mixed_code_sha256",
    "source_graph_id", "target_completion_mixed_code_sha256", "target_graph_id",
    "port_matching", "remaining_target_role_count", "remaining_target_roles",
    "probe_classification", "probe_witness", "raw_coverage", "children",
    "terminal_classification", "binding_sha256",
}
STATE_OPTIONAL = {"terminal_witness"}
ROOT_KEY_FIELDS = {
    "selected_outgoing", "selected_signature_sha256", "source_primitive_id",
    "target_primitive_id", "source_provenance", "target_provenance",
    "source_selected_labels", "target_selected_labels",
    "source_position_to_label", "target_position_to_label", "target_dummy_roles",
    "target_incoming_selected",
}
COVERAGE_EXTRA = {
    "root_case_id", "restoration_path", "source_extended_words",
    "restored_target_roles", "parent_state_id", "parent_path_binding_id",
    "dummy_order", "restored_role_to_label", "source_graph_id", "target_graph_id",
    "source_raw_mixed_vertex_to_canonical",
    "target_raw_mixed_vertex_to_canonical", "canonical_state_id",
    "path_binding_payload_sha256", "path_binding_id", "child_state_ids",
}
ALLOWED_TERMINALS = {
    "generic_polynomial_separation", "strict_open_cube_separation",
    "refined_by_next_restoration", "support_prefix_labelled_isomorphism",
    "support_prefix_ordinary_T",
}


def load_jsonl(path: Path, key: str) -> tuple[dict[str, dict], dict]:
    rows: dict[str, dict] = {}
    failures = []
    uncompressed = hashlib.sha256()
    prior = None
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            uncompressed.update(line.encode())
            row = json.loads(line)
            identifier = row.get(key)
            if not isinstance(identifier, str):
                failures.append({"type": "missing_identifier", "line": line_number, "key": key})
                continue
            if prior is not None and identifier <= prior:
                failures.append({"type": "stream_not_strictly_sorted", "id": identifier})
            prior = identifier
            if identifier in rows:
                failures.append({"type": "duplicate_identifier", "id": identifier})
            rows[identifier] = row
    return rows, {
        "path": str(path.relative_to(PROJECT)),
        "records": len(rows),
        "gzip_sha256": file_sha(path),
        "uncompressed_sha256": uncompressed.hexdigest(),
        "bytes": path.stat().st_size,
        "failures": failures,
    }


def graph_from_row(row: dict) -> RootedGraph:
    rooted = row["rooted_graph"]
    return RootedGraph(
        int(rooted["root"]),
        tuple((int(vertex), str(label)) for vertex, label in rooted["labels"]),
        tuple((int(u), int(v)) for u, v in rooted["arcs"]),
    )


def poly_from_row(row: dict) -> dict[tuple[int, ...], int]:
    return {
        tuple(int(value) for value in exponents): int(coefficient)
        for exponents, coefficient in row["terms"]
    }


def git_tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path.relative_to(PROJECT.parent))],
        cwd=PROJECT.parent,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default=DEFAULT_TAG)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--source-core-id", action="append")
    parser.add_argument("--source-extra-count", action="append", type=int)
    parser.add_argument("--summary", type=Path, default=PROJECT / "primary/certificates/hard_cover_candidate_full_summary.json")
    parser.add_argument("--output", type=Path, default=HERE / "candidate_full_audit_certificate.json")
    parser.add_argument("--use-supplied-bit-cache", action="store_true", help="debug only")
    parser.add_argument("--skip-algebra", action="store_true", help="debug only")
    args = parser.parse_args()
    args.summary = args.summary.resolve()
    args.output = args.output.resolve()
    started = time.monotonic()
    paths = {
        "states": PROJECT / f"primary/certificates/hard_cover_n{args.n}_{args.tag}.jsonl.gz",
        "graphs": PROJECT / f"primary/certificates/hard_cover_graphs_n{args.n}_{args.tag}.jsonl.gz",
        "polynomials": PROJECT / f"primary/certificates/hard_cover_polynomials_n{args.n}_{args.tag}.jsonl.gz",
        "roots": PROJECT / f"primary/certificates/hard_cover_root_cases_n{args.n}_{args.tag}.jsonl.gz",
    }
    missing = [str(path) for path in (*paths.values(), args.summary) if not path.exists()]
    if missing:
        raise SystemExit("candidate_full incomplete: " + ", ".join(missing))

    states, state_stream = load_jsonl(paths["states"], "state_id")
    graphs, graph_stream = load_jsonl(paths["graphs"], "graph_id")
    polynomials, polynomial_stream = load_jsonl(paths["polynomials"], "polynomial_id")
    roots, root_stream = load_jsonl(paths["roots"], "root_case_id")
    failures = [
        failure
        for stream in (state_stream, graph_stream, polynomial_stream, root_stream)
        for failure in stream["failures"]
    ]

    source_core_filter = set(args.source_core_id or ())
    source_extra_filter = set(args.source_extra_count or ())
    inventory = build_inventory(
        selected_outgoing=args.n,
        recompute_all_descriptor_bits=not args.use_supplied_bit_cache,
        source_core_ids=(
            frozenset(source_core_filter) if source_core_filter else None
        ),
        source_extra_counts=(
            frozenset(source_extra_filter) if source_extra_filter else None
        ),
        # Hard-cover roots are defined only over common source/target
        # signatures.  Target-only signatures can never contribute a root;
        # discarding their presentation records is an exact memory reduction,
        # not a restriction of the audited relation universe.
        retain_only_target_signatures_seen_in_source=True,
    )
    expected_roots = {
        root_id: root
        for root_id, root in inventory.root_cases.items()
        if (
            not source_core_filter
            or inventory.sources[root["source_primitive_id"]].core_id in source_core_filter
        )
        and (
            not source_extra_filter
            or inventory.sources[root["source_primitive_id"]].extra_count in source_extra_filter
        )
    }
    inventory = replace(inventory, root_cases=expected_roots)
    core_payload = json.loads(CORE_PATH.read_text())

    # Exact replay of every selected root's full quartet invariant deck.  The
    # finite candidate inventory may be indexed with the supplied cache for
    # speed, but no selected root is accepted on that basis: all descriptors
    # occurring in these roots are recomputed from polynomial pullbacks here.
    root_exact_failures = []
    root_descriptor_bits: dict[tuple, int] = {}
    invariants = invariant_orbit(json.loads(INVARIANT_PATH.read_text()))

    def exact_root_signature(variant, assignment):
        p = args.n + 1
        inverse = [0] * p
        for position, actual in enumerate(assignment):
            inverse[int(actual)] = position
        signature = 0
        deck = variant.deck_map()
        for chunk, actual_quartet in enumerate(combinations(range(p), 4)):
            descriptor = deck[tuple(inverse[value] for value in actual_quartet)]
            if descriptor not in root_descriptor_bits:
                root_descriptor_bits[descriptor] = descriptor_bits_exact(descriptor, invariants)
            signature |= root_descriptor_bits[descriptor] << (len(invariants) * chunk)
        return signature

    if not args.skip_algebra:
        for root_id, root in inventory.root_cases.items():
            source_signature = exact_root_signature(
                inventory.sources[root["source_primitive_id"]],
                root["source_position_to_label"],
            )
            target_signature = exact_root_signature(
                inventory.targets[root["target_primitive_id"]],
                root["target_position_to_label"],
            )
            expected_sha = hashlib.sha256(str(source_signature).encode()).hexdigest()
            if source_signature != target_signature or expected_sha != root["selected_signature_sha256"]:
                root_exact_failures.append({
                    "root_case_id": root_id,
                    "source_signature_sha256": expected_sha,
                    "target_signature_sha256": hashlib.sha256(str(target_signature).encode()).hexdigest(),
                    "recorded_signature_sha256": root["selected_signature_sha256"],
                })
        if root_exact_failures:
            failures.append({"type": "exact_root_invariant_deck_failure", "count": len(root_exact_failures), "examples": root_exact_failures[:20]})

    # Content-address and independent class/reduction verification for every
    # graph, not merely the producer's Boolean fields.
    graph_class_counts = Counter()
    graph_class_failures = []
    graph_leaf_quantifier_failures = []
    for graph_id, row in graphs.items():
        rooted_payload = row["rooted_graph"]
        if stable_hash(rooted_payload) != graph_id:
            failures.append({"type": "graph_content_address_mismatch", "graph_id": graph_id})
        graph = graph_from_row(row)
        result = class_audit(graph)
        internal = internal_vertex_audit(graph)
        required = (
            result.get("rooted_valid") and result.get("root_is_lsa")
            and result.get("rooted_tree_child") and internal.get("passes")
            and internal.get("leaf_vertices_excluded") and result.get("sd0_valid")
            and result.get("standard_strong_local") and result.get("level_at_most_two")
            and int(result.get("triangle_count", 99)) <= 1
        )
        if not required:
            graph_class_failures.append({"graph_id": graph_id, "class_audit": result})
        if internal["checked_vertex_count"] != internal["internal_vertex_count"] or not internal["leaf_vertices_excluded"]:
            graph_leaf_quantifier_failures.append({"graph_id": graph_id, "audit": internal})
        mixed_code, vertex_map = canonical_mixed(sd0(graph))
        t_code, _ = canonical_mixed(t_quotient(sd0(graph)))
        if row.get("standard_mixed_code") != mixed_code:
            failures.append({"type": "graph_standard_code_mismatch", "graph_id": graph_id})
        if row.get("standard_mixed_code_sha256") != hashlib.sha256(mixed_code.encode()).hexdigest():
            failures.append({"type": "graph_standard_hash_mismatch", "graph_id": graph_id})
        if row.get("t_quotient_code") != t_code:
            failures.append({"type": "graph_T_code_mismatch", "graph_id": graph_id})
        if row.get("t_quotient_code_sha256") != hashlib.sha256(t_code.encode()).hexdigest():
            failures.append({"type": "graph_T_hash_mismatch", "graph_id": graph_id})
        recorded_map = tuple((int(a), int(b)) for a, b in row.get("raw_mixed_vertex_to_canonical", ()))
        if recorded_map != tuple(sorted(vertex_map.items())):
            failures.append({"type": "graph_raw_to_canonical_map_mismatch", "graph_id": graph_id})
        graph_class_counts[(result.get("triangle_count"), len(sd0(graph).reticulations()))] += 1
    if graph_class_failures:
        failures.append({"type": "graph_library_class_membership_failure", "count": len(graph_class_failures), "examples": graph_class_failures[:20]})
    if graph_leaf_quantifier_failures:
        failures.append({"type": "leaf_internal_quantifier_failure", "count": len(graph_leaf_quantifier_failures), "examples": graph_leaf_quantifier_failures[:20]})

    # Polynomial stream content addressing.  The graph-to-polynomial
    # association is checked below by semantic_audit, which regenerates each
    # pullback from graph switchings and descendant masks.
    polynomial_exact_hashes = {}
    for polynomial_id, row in polynomials.items():
        payload = {key: row[key] for key in ("schema", "variable_count", "terms")}
        if stable_hash(payload) != polynomial_id:
            failures.append({"type": "polynomial_content_address_mismatch", "polynomial_id": polynomial_id})
        poly = poly_from_row(row)
        if poly and len(next(iter(poly))) != int(row["variable_count"]):
            failures.append({"type": "polynomial_variable_count_mismatch", "polynomial_id": polynomial_id})
        polynomial_exact_hashes[polynomial_id] = hashlib.sha256(
            repr(tuple(sorted(poly.items()))).encode()
        ).hexdigest()

    # State, root, and raw fixed-relation path bindings.
    path_index: dict[str, tuple[str, dict]] = {}
    root_ids_seen = set()
    terminal_counts = Counter()
    probe_counts = Counter()
    for state_id, row in states.items():
        if set(row) - (STATE_REQUIRED | STATE_OPTIONAL):
            failures.append({"type": "unknown_state_fields", "state_id": state_id, "fields": sorted(set(row) - (STATE_REQUIRED | STATE_OPTIONAL))})
        if STATE_REQUIRED - set(row):
            failures.append({"type": "missing_state_fields", "state_id": state_id, "fields": sorted(STATE_REQUIRED - set(row))})
            continue
        if int(row.get("schema", -1)) != 3:
            failures.append({"type": "wrong_state_schema", "state_id": state_id})
        bound = dict(row)
        recorded_binding = bound.pop("binding_sha256")
        if stable_hash(bound) != recorded_binding:
            failures.append({"type": "state_binding_mismatch", "state_id": state_id})
        terminal_counts[row["terminal_classification"]] += 1
        probe_counts[row["probe_classification"]] += 1
        if row["terminal_classification"] not in ALLOWED_TERMINALS:
            failures.append({"type": "unresolved_or_unknown_terminal", "state_id": state_id, "terminal": row["terminal_classification"]})
        p = int(row["selected_port_count"])
        if row["port_matching"] != [[f"L_{index}", f"L_{index}"] for index in range(p)]:
            failures.append({"type": "nonidentity_state_port_matching", "state_id": state_id})
        for side in ("source", "target"):
            graph_id = row[f"{side}_graph_id"]
            graph_row = graphs.get(graph_id)
            if graph_row is None:
                failures.append({"type": "missing_state_graph", "state_id": state_id, "side": side, "graph_id": graph_id})
                continue
            expected_hash = graph_row["standard_mixed_code_sha256"]
            recorded_hash = row["source_mixed_code_sha256"] if side == "source" else row["target_completion_mixed_code_sha256"]
            if recorded_hash != expected_hash:
                failures.append({"type": "state_graph_code_hash_mismatch", "state_id": state_id, "side": side})
        source_code = graphs[row["source_graph_id"]]["standard_mixed_code"]
        target_code = graphs[row["target_graph_id"]]["standard_mixed_code"]
        derived_state_id = stable_hash({
            "fixed_full_root_case_id": row["fixed_full_root_case_id"],
            "selected_port_count": p,
            "source_rooted_graph_id": row["source_graph_id"],
            "target_rooted_graph_id": row["target_graph_id"],
            "source_mixed_code": source_code,
            "target_completion_mixed_code": target_code,
            "remaining_target_roles": row["remaining_target_roles"],
            "port_matching": tuple(range(p)),
        })
        if derived_state_id != state_id:
            failures.append({"type": "state_id_graph_binding_mismatch", "state_id": state_id, "derived": derived_state_id})
        for child in row["children"]:
            if child not in states:
                failures.append({"type": "missing_child_state", "state_id": state_id, "child": child})
        for coverage in row["raw_coverage"]:
            if set(coverage) != ROOT_KEY_FIELDS | COVERAGE_EXTRA:
                failures.append({"type": "coverage_schema_mismatch", "state_id": state_id, "missing": sorted((ROOT_KEY_FIELDS | COVERAGE_EXTRA) - set(coverage)), "extra": sorted(set(coverage) - (ROOT_KEY_FIELDS | COVERAGE_EXTRA))})
            if coverage.get("canonical_state_id") != state_id:
                failures.append({"type": "coverage_state_binding_mismatch", "state_id": state_id})
            root_id = coverage["root_case_id"]
            root_ids_seen.add(root_id)
            if root_id != row["fixed_full_root_case_id"]:
                failures.append({
                    "type": "coverage_crosses_fixed_root_case",
                    "state_id": state_id,
                    "state_root_case_id": row["fixed_full_root_case_id"],
                    "coverage_root_case_id": root_id,
                })
            root_key = root_key_from_coverage(coverage)
            if stable_hash(root_key) != root_id:
                failures.append({"type": "coverage_root_hash_mismatch", "state_id": state_id, "root_case_id": root_id})
            independent_root = inventory.root_cases.get(root_id)
            if independent_root is None or canonical_json(independent_root) != canonical_json(root_key):
                failures.append({"type": "coverage_root_absent_or_mismatch", "state_id": state_id, "root_case_id": root_id})
            stripped = dict(coverage)
            for key in ("path_binding_payload_sha256", "path_binding_id", "child_state_ids"):
                stripped.pop(key, None)
            payload_hash = stable_hash(stripped)
            if coverage.get("path_binding_payload_sha256") != payload_hash or coverage.get("path_binding_id") != payload_hash:
                failures.append({"type": "path_content_address_mismatch", "state_id": state_id, "path_id": coverage.get("path_binding_id")})
            path_id = coverage["path_binding_id"]
            if path_id in path_index:
                failures.append({"type": "duplicate_path_binding_id", "path_id": path_id})
            path_index[path_id] = (state_id, coverage)
            if tuple(sorted(coverage["child_state_ids"])) != tuple(sorted(row["children"])):
                failures.append({"type": "coverage_child_set_not_bound_to_state", "state_id": state_id, "path_id": path_id})
            for child in coverage["child_state_ids"]:
                if child not in states:
                    failures.append({"type": "coverage_missing_child_state", "state_id": state_id, "path_id": path_id, "child": child})
            # Schema 3 deliberately forbids merging distinct rooted
            # presentations even when their standard mixed codes agree.
            # This exact check is the regression guard for the quarantined
            # schema-2 theta-2 stream.
            if coverage.get("source_graph_id") != row["source_graph_id"]:
                failures.append({
                    "type": "coverage_crosses_source_rooted_graph",
                    "state_id": state_id,
                    "state_graph_id": row["source_graph_id"],
                    "coverage_graph_id": coverage.get("source_graph_id"),
                })
            if coverage.get("target_graph_id") != row["target_graph_id"]:
                failures.append({
                    "type": "coverage_crosses_target_rooted_graph",
                    "state_id": state_id,
                    "state_graph_id": row["target_graph_id"],
                    "coverage_graph_id": coverage.get("target_graph_id"),
                })
            source_coverage_graph = graphs.get(coverage["source_graph_id"])
            target_coverage_graph = graphs.get(coverage["target_graph_id"])
            if source_coverage_graph is None or target_coverage_graph is None:
                failures.append({"type": "coverage_graph_missing", "state_id": state_id, "path_id": path_id})
                continue
            if source_coverage_graph["standard_mixed_code_sha256"] != row["source_mixed_code_sha256"] or target_coverage_graph["standard_mixed_code_sha256"] != row["target_completion_mixed_code_sha256"]:
                failures.append({"type": "coverage_graph_not_in_canonical_state", "state_id": state_id, "path_id": path_id})
            if tuple(tuple(pair) for pair in coverage["source_raw_mixed_vertex_to_canonical"]) != tuple(tuple(pair) for pair in source_coverage_graph["raw_mixed_vertex_to_canonical"]):
                failures.append({"type": "coverage_source_transport_mismatch", "state_id": state_id, "path_id": path_id})
            if tuple(tuple(pair) for pair in coverage["target_raw_mixed_vertex_to_canonical"]) != tuple(tuple(pair) for pair in target_coverage_graph["raw_mixed_vertex_to_canonical"]):
                failures.append({"type": "coverage_target_transport_mismatch", "state_id": state_id, "path_id": path_id})

    # Parent chains are checked after all paths are indexed.
    for path_id, (state_id, coverage) in path_index.items():
        parent_path_id = coverage["parent_path_binding_id"]
        if parent_path_id is None:
            if coverage["parent_state_id"] is not None or len(coverage["restoration_path"]) != 1:
                failures.append({"type": "invalid_entry_parent", "state_id": state_id, "path_id": path_id})
        else:
            parent = path_index.get(parent_path_id)
            if parent is None:
                failures.append({"type": "missing_parent_path", "state_id": state_id, "path_id": path_id})
                continue
            parent_state_id, parent_coverage = parent
            if coverage["parent_state_id"] != parent_state_id:
                failures.append({"type": "parent_state_id_mismatch", "state_id": state_id, "path_id": path_id})
            if parent_coverage["root_case_id"] != coverage["root_case_id"]:
                failures.append({"type": "parent_root_changed", "state_id": state_id, "path_id": path_id})
            if parent_coverage["restoration_path"] != coverage["restoration_path"][:-1]:
                failures.append({"type": "incoherent_parent_restoration_prefix", "state_id": state_id, "path_id": path_id})

    # Root-case library and exact entry-state coverage.
    global_indices = set()
    for root_id, row in roots.items():
        if int(row.get("schema", -1)) != 1 or stable_hash(row["root_case"]) != root_id:
            failures.append({"type": "root_case_content_address_mismatch", "root_case_id": root_id})
        independent = inventory.root_cases.get(root_id)
        if independent is None or canonical_json(independent) != canonical_json(row["root_case"]):
            failures.append({"type": "root_case_inventory_mismatch", "root_case_id": root_id})
        global_indices.add(int(row["global_root_case_index"]))
        for entry_state in row["entry_state_ids"]:
            if entry_state not in states:
                failures.append({"type": "root_missing_entry_state", "root_case_id": root_id, "entry_state": entry_state})
            elif not any(
                coverage["root_case_id"] == root_id and coverage["parent_path_binding_id"] is None
                for coverage in states[entry_state]["raw_coverage"]
            ):
                failures.append({"type": "root_entry_state_not_bound", "root_case_id": root_id, "entry_state": entry_state})
    if set(roots) != set(inventory.root_cases) or root_ids_seen != set(inventory.root_cases):
        failures.append({
            "type": "complete_root_coverage_mismatch",
            "library_missing": len(set(inventory.root_cases) - set(roots)),
            "library_extra": len(set(roots) - set(inventory.root_cases)),
            "state_missing": len(set(inventory.root_cases) - root_ids_seen),
            "state_extra": len(root_ids_seen - set(inventory.root_cases)),
        })
    if global_indices != set(range(len(inventory.root_cases))):
        failures.append({"type": "root_global_index_not_complete"})

    # Rebuild every source and target graph from raw provenance, not graph IDs.
    graph_rebuild_failures = []
    for path_id, (state_id, coverage) in path_index.items():
        source_variant = inventory.sources[coverage["source_primitive_id"]]
        target_variant = inventory.targets[coverage["target_primitive_id"]]
        source = source_graph_for(source_variant, coverage, core_payload)
        target = target_graph_for(target_variant, coverage)
        for side, graph in (("source", source), ("target", target)):
            graph_id = coverage[f"{side}_graph_id"]
            library_graph = graph_from_row(graphs[graph_id])
            if graph != library_graph:
                graph_rebuild_failures.append({"path_id": path_id, "state_id": state_id, "side": side, "type": "rooted_graph_bytes"})
            code, mapping = canonical_mixed(sd0(graph))
            if code != graphs[graph_id]["standard_mixed_code"]:
                graph_rebuild_failures.append({"path_id": path_id, "state_id": state_id, "side": side, "type": "standard_code"})
            recorded_map = coverage[f"{side}_raw_mixed_vertex_to_canonical"]
            if tuple(tuple(pair) for pair in recorded_map) != tuple(sorted(mapping.items())):
                graph_rebuild_failures.append({"path_id": path_id, "state_id": state_id, "side": side, "type": "raw_to_canonical_map"})
    if graph_rebuild_failures:
        failures.append({"type": "raw_graph_rebuild_failure", "count": len(graph_rebuild_failures), "examples": graph_rebuild_failures[:20]})

    # This invokes an independently implemented displayed-tree/Fourier engine,
    # exact Jacobian-free signature compiler, and factor/Bernstein checker.
    semantics = semantic_audit(
        states,
        path_index,
        inventory,
        verify_all_algebra=not args.skip_algebra,
    )
    failures.extend(semantics["failures"])

    # Bind graph-derived exact pullbacks to the separate polynomial library.
    referenced_polynomials = set()
    for state_id, row in states.items():
        witness = row["probe_witness"]
        if row["probe_classification"] == "generic_polynomial_separation":
            identifier = witness.get("source_pullback_id")
            exact_hash = witness.get("source_pullback_exact_sha256")
        elif row["probe_classification"] == "strict_open_cube_separation":
            identifier = witness.get("target_pullback_id")
            exact_hash = witness.get("target_pullback_exact_sha256")
        else:
            continue
        referenced_polynomials.add(identifier)
        if identifier not in polynomials:
            failures.append({"type": "witness_polynomial_missing", "state_id": state_id, "polynomial_id": identifier})
        elif polynomial_exact_hashes[identifier] != exact_hash:
            failures.append({"type": "witness_polynomial_library_hash_mismatch", "state_id": state_id, "polynomial_id": identifier})
    if referenced_polynomials != set(polynomials):
        failures.append({"type": "polynomial_library_reference_set_mismatch", "unreferenced": len(set(polynomials) - referenced_polynomials), "missing": len(referenced_polynomials - set(polynomials))})

    # Bind all four streams and terminal totals to the producer summary.
    summary = json.loads(args.summary.read_text())
    run = summary["runs"][0]["hard_cover"]
    summary_checks = {
        "source_core_filter": sorted(summary.get("source_core_filter") or ()) == sorted(source_core_filter),
        "source_extra_count_filter": sorted(summary.get("source_extra_count_filter") or ()) == sorted(source_extra_filter),
        "selected_outgoing": run.get("selected_outgoing") == args.n,
        "all_root_cases": run.get("all_root_cases") == len(inventory.root_cases),
        "selected_root_cases": run.get("selected_root_cases") == len(inventory.root_cases),
        "canonical_restored_relations": run.get("canonical_restored_relations") == len(states),
        "relation_stream_sha256": run.get("relation_stream_sha256") == state_stream["uncompressed_sha256"],
        "graph_stream_sha256": run.get("graph_library_stream_sha256") == graph_stream["uncompressed_sha256"],
        "polynomial_stream_sha256": run.get("polynomial_library_stream_sha256") == polynomial_stream["uncompressed_sha256"],
        "root_stream_sha256": run.get("root_case_stream_sha256") == root_stream["uncompressed_sha256"],
        "terminal_counts": run.get("counts") == dict(sorted(terminal_counts.items())),
        "unresolved_zero": run.get("unresolved") == 0,
        "root_commitment": run.get("root_case_commitment") == stable_hash(sorted(inventory.root_cases.items())),
    }
    for key, passed in summary_checks.items():
        if not passed:
            failures.append({"type": "summary_binding_failure", "check": key})

    input_paths = (*paths.values(), args.summary, CORE_PATH, INVARIANT_PATH, BIT_CACHE_PATH, PRODUCER_PATH)
    payload = {
        "schema": "candidate-full-hard-cover-clean-room-v2",
        "status": "FALSE" if failures else "VERIFIED",
        "scope": f"schema-3 fixed-root {args.tag} n={args.n} hard-cover and its graph/polynomial/root libraries",
        "independence": "no primary module imported; every graph, reduction, tensor pullback, and sign proof regenerated",
        "inputs": {str(path.relative_to(PROJECT)): file_sha(path) for path in input_paths},
        "git_tracked": {str(path.relative_to(PROJECT)): git_tracked(path) for path in input_paths},
        "streams": {
            "states": state_stream,
            "graphs": graph_stream,
            "polynomials": polynomial_stream,
            "roots": root_stream,
        },
        "independent_inventory": {
            "root_cases": len(inventory.root_cases),
            "root_case_commitment_sha256": stable_hash(sorted(inventory.root_cases.items())),
            "source_signatures": inventory.source_signature_count,
            "target_signatures": inventory.target_signature_count,
            "common_signatures": inventory.common_signature_count,
            "descriptor_count_recomputed": len(inventory.descriptor_bits),
            "invariant_orbit_sha256": inventory.invariant_orbit_sha256,
            "selected_root_descriptors_exactly_recomputed": len(root_descriptor_bits),
            "selected_root_exact_failure_count": len(root_exact_failures),
            "source_core_filter": sorted(source_core_filter),
            "source_extra_count_filter": sorted(source_extra_filter),
        },
        "state_counts": {
            "states": len(states), "raw_paths": len(path_index),
            "terminal": dict(sorted(terminal_counts.items())),
            "probe": dict(sorted(probe_counts.items())),
        },
        "graph_audit": {
            "all_graphs_checked": len(graphs),
            "class_strata": {repr(key): value for key, value in sorted(graph_class_counts.items(), key=repr)},
            "class_failure_count": len(graph_class_failures),
            "leaf_quantifier_failure_count": len(graph_leaf_quantifier_failures),
        },
        "summary_checks": summary_checks,
        "semantic_audit": semantics,
        "failure_count": len(failures),
        "failures": failures,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "failure_count": len(failures),
        "roots": len(inventory.root_cases),
        "states": len(states),
        "paths": len(path_index),
        "output": str(args.output),
        "sha256": file_sha(args.output),
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
