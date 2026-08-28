#!/usr/bin/env python3
"""Independent structural/census attacks for the 2026-08-27 K2P package.

This script intentionally does not import a submitted verifier or classifier.
It reads the sealed data formats directly, recomputes their documented roots,
checks raw-coordinate bijections and parent/transport joins, and uses the graph
grammar only to construct primitive graphs that are then checked by separate
explicit predicates in this file.
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import gzip
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


class AttackFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise AttackFailure(code if detail is None else f"{code}:{detail}")


def canonical_data(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: canonical_data(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        return {
            str(key): canonical_data(item)
            for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [canonical_data(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((canonical_data(item) for item in value), key=repr)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        canonical_data(value), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def unique_object(label: str):
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_NAME", f"{label}:{key}")
            result[key] = value
        return result
    return hook


def load_unique_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object(str(path)),
    )


def safe_relative(relative: str) -> PurePosixPath:
    result = PurePosixPath(relative)
    require(
        bool(result.parts)
        and not result.is_absolute()
        and all(part not in {"", ".", ".."} for part in result.parts),
        "UNSAFE_MANIFEST_PATH",
        relative,
    )
    return result


def scan_json_documents(project: Path) -> dict[str, Any]:
    paths = sorted(project.rglob("*.json"))
    total_bytes = 0
    for path in paths:
        require(path.is_file() and not path.is_symlink(), "JSON_NOT_REGULAR", path)
        load_unique_json(path)
        total_bytes += path.stat().st_size
    return {
        "documents": len(paths),
        "bytes": total_bytes,
        "duplicate_names": 0,
        "malformed": 0,
    }


def validate_outer_manifest(project: Path) -> dict[str, Any]:
    relative = (
        "proof_compression_submission/crosswalk/"
        "REVISED_REFEREE_BUNDLE_MANIFEST.json"
    )
    manifest = load_unique_json(project / relative)
    require(manifest["schema"] == "k2p-revised-referee-bundle-manifest-v2", "MANIFEST_SCHEMA")
    unsigned = dict(manifest)
    payload = unsigned.pop("payload_sha256")
    require(payload == sha_object(unsigned), "MANIFEST_PAYLOAD")

    observed_maps: dict[str, dict[str, dict[str, int | str]]] = {}
    for section in ("frozen_evidence", "submission_sources"):
        declared = manifest[section]
        files = declared["files"]
        observed: dict[str, dict[str, int | str]] = {}
        for child in sorted(files):
            path = project.joinpath(*safe_relative(child).parts)
            require(path.is_file() and not path.is_symlink(), "MANIFEST_MEMBER_NOT_REGULAR", child)
            row = {"bytes": path.stat().st_size, "sha256": sha_file(path)}
            require(row == files[child], "MANIFEST_MEMBER_DRIFT", child)
            observed[child] = row
        require(len(observed) == declared["file_count"], "MANIFEST_SECTION_COUNT", section)
        require(sum(int(row["bytes"]) for row in observed.values()) == declared["total_bytes"], "MANIFEST_SECTION_BYTES", section)
        require(sha_object(observed) == declared["content_ledger_root_sha256"], "MANIFEST_SECTION_ROOT", section)
        observed_maps[section] = observed
    frozen = observed_maps["frozen_evidence"]
    submission = observed_maps["submission_sources"]
    require(not (set(frozen) & set(submission)), "MANIFEST_PARTITIONS_OVERLAP")
    require(
        len(frozen) + len(submission) == manifest["combined_file_count_excluding_manifest"],
        "MANIFEST_COMBINED_COUNT",
    )
    require(
        sha_object({"frozen_evidence": frozen, "submission_sources": submission})
        == manifest["combined_content_root_sha256"],
        "MANIFEST_COMBINED_ROOT",
    )
    return {
        "payload_sha256": payload,
        "frozen_files": len(frozen),
        "submission_files": len(submission),
        "combined_files": len(frozen) + len(submission),
        "combined_content_root_sha256": manifest["combined_content_root_sha256"],
    }


def import_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "IMPORT_SPEC", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def graph_encoding(record: Any) -> tuple[Any, ...]:
    return (
        record.core_id,
        record.incoming_selected,
        record.repair_index,
        record.selected_sink_mask,
        canonical_data(record.words),
        record.selected_labels,
        record.dummy_labels,
        record.source_support,
        record.extra_count,
    )


def explicit_graph_check(graph: Any) -> dict[str, int]:
    # Kahn's algorithm, kept independent of networkx's DAG predicate.
    indegree = {node: graph.in_degree(node) for node in graph.nodes()}
    pending = collections.deque(node for node, degree in indegree.items() if degree == 0)
    visited = 0
    while pending:
        node = pending.popleft()
        visited += 1
        for child in graph.successors(node):
            indegree[child] -= 1
            if indegree[child] == 0:
                pending.append(child)
    require(visited == graph.number_of_nodes(), "PRIMITIVE_CYCLE")
    roles = collections.Counter()
    selected: list[int] = []
    dummy_names: list[str] = []
    for node, data in graph.nodes(data=True):
        role = data.get("role")
        roles[role] += 1
        degree = (graph.in_degree(node), graph.out_degree(node))
        expected = {
            "root": (0, 2), "tree": (1, 2),
            "retic": (2, 1), "leaf": (1, 0),
        }.get(role)
        require(expected is not None and degree == expected, "PRIMITIVE_DEGREE", (role, degree))
        if isinstance(data.get("label"), int):
            selected.append(data["label"])
        if data.get("dummy"):
            dummy_names.append(str(data.get("dummy_name")))
        if role != "leaf":
            require(
                any(graph.nodes[child].get("role") in {"tree", "leaf"} for child in graph.successors(node)),
                "PRIMITIVE_STRONG_TREE_CHILD",
                repr(node),
            )
    require(len(selected) == len(set(selected)), "PRIMITIVE_SELECTED_LABEL_DUPLICATE")
    require(len(dummy_names) == len(set(dummy_names)), "PRIMITIVE_DUMMY_NAME_DUPLICATE")
    require(roles["root"] == 1, "PRIMITIVE_ROOT_COUNT", roles["root"])
    return dict(roles)


def primitive_graph_audit(project: Path) -> dict[str, Any]:
    atlas = import_module(
        project / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py",
        "r4_independent_graph_grammar",
    )
    families = {
        "raw4_sources": tuple(atlas.source_supports()),
        "raw4_targets": tuple(atlas.target_completions(4, True) + atlas.target_completions(4, False)),
        "theta2_sources": tuple(atlas.source_supports(("theta2",))),
        "theta2_targets": tuple(atlas.target_completions(5, True) + atlas.target_completions(5, False)),
        "cycle_sources": tuple(atlas.source_supports(("cycle",))),
        "cycle_targets": tuple(atlas.target_completions(3, True) + atlas.target_completions(3, False)),
    }
    expected = {
        "raw4_sources": 6, "raw4_targets": 2814,
        "theta2_sources": 4, "theta2_targets": 6138,
        "cycle_sources": 2, "cycle_targets": 1120,
    }
    require({key: len(value) for key, value in families.items()} == expected, "PRIMITIVE_FAMILY_CENSUS")
    checked = 0
    encodings = 0
    for name, records in families.items():
        seen = set()
        for record in records:
            explicit_graph_check(record.graph)
            encoding = canonical_bytes(graph_encoding(record))
            require(encoding not in seen, "PRIMITIVE_ENCODING_DUPLICATE", name)
            seen.add(encoding)
            if record.source_support:
                require(record.selected_labels == tuple(range(len(record.selected_labels))), "SOURCE_LABEL_GAP", name)
            else:
                require(record.selected_labels == tuple(range(len(record.selected_labels))), "TARGET_LABEL_GAP", name)
            checked += 1
        encodings += len(seen)

    # A deterministic boundary-spanning slow/fast orbit control.  This is a
    # sample only; the sealed full audit covers all 10,084 archetypes.
    comparison_rows = []
    for name, records in families.items():
        indices = sorted({0, len(records) // 2, len(records) - 1})
        for index in indices:
            slow = atlas.model_descriptor(records[index].graph)
            fast = atlas.model_descriptor_fast2(records[index].graph)
            require(slow == fast, "DESCRIPTOR_SLOW_FAST_SAMPLE", (name, index))
            comparison_rows.append([name, index, sha_object(slow)])
    return {
        "family_counts": expected,
        "primitive_graphs_checked": checked,
        "distinct_encodings": encodings,
        "slow_fast_sample_count": len(comparison_rows),
        "slow_fast_sample_root_sha256": sha_object(comparison_rows),
    }


RAW_LEDGER_SPECS = {
    "raw4": {
        "path": "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz",
        "summary": "work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_summary.json",
        "total": 405_216, "sources": 6, "targets": 2814, "ports": 4,
        "schema": "k2p-raw4-corrected-composite-row-v1",
        "categories": {
            "displayed_quartet_exclusion": 360_408,
            "full_map_Ti_strict_sign": 16_974,
            "exact_rank_exclusion": 23_822,
            "direct_terminal_presentation": 1_472,
            "restoration_member_presentation": 2_540,
        },
        "reasons": {
            "displayed_quartet_exclusion": ("source_target_displayed_quartet_sets_differ", "exact_displayed_quartet_witness"),
            "full_map_Ti_strict_sign": ("whole_map_source_strict_sign_target_zero", "exact_whole_map_Ti_zero_sign_certificate"),
            "exact_rank_exclusion": ("target_exact_generic_rank_below_source", "matched_exact_rank_lower_symbolic_upper"),
            "direct_terminal_presentation": ("direct_terminal_certificate", "exact_terminal_class_and_direct_certificate"),
            "restoration_member_presentation": ("physical_restoration_required", "exact_restoration_parent_and_physical_transport"),
        },
    },
    "theta2": {
        "path": "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_ledger.jsonl.gz",
        "summary": "work/corrected_composite_ledgers/artifacts/theta2_corrected_composite_summary.json",
        "total": 2_946_240, "sources": 4, "targets": 6138, "ports": 5,
        "schema": "k2p-theta2-corrected-composite-row-v1",
        "categories": {
            "displayed_quartet_exclusion": 2_942_592,
            "full_map_Ti_strict_sign": 2_528,
            "exact_rank_exclusion": 800,
            "direct_quadratic_separator": 240,
            "labelled_isomorphism": 80,
        },
        "reasons": {
            "displayed_quartet_exclusion": ("source_target_displayed_quartet_sets_differ", "exact_displayed_quartet_witness"),
            "full_map_Ti_strict_sign": ("whole_map_source_zero_target_strict_sign", "exact_whole_map_Ti_zero_sign_certificate"),
            "exact_rank_exclusion": ("target_exact_generic_rank_below_source", "matched_exact_rank_lower_symbolic_upper"),
            "direct_quadratic_separator": ("exact_quadratic_target_zero_source_nonzero", "exact_multihomogeneous_quadratic_separator"),
            "labelled_isomorphism": ("exact_labelled_graph_isomorphism", "exact_labelled_semi_directed_isomorphism"),
        },
    },
}


def stream_raw_ledger(project: Path, name: str, spec: dict[str, Any]) -> dict[str, Any]:
    path = project / spec["path"]
    summary = load_unique_json(project / spec["summary"])
    permutations = tuple(itertools.permutations(range(spec["ports"])))
    per_source = spec["targets"] * len(permutations)
    counts: collections.Counter[str] = collections.Counter()
    first_ids: dict[str, int] = {}
    last_ids: dict[str, int] = {}
    row_root = hashlib.sha256()
    raw_id_root = hashlib.sha256()
    plain_root = hashlib.sha256()
    plain_bytes = 0
    forbidden_rows = 0
    symbolic_rank_rows = 0
    with gzip.open(path, "rb") as handle:
        for ordinal, line in enumerate(handle):
            require(line.endswith(b"\n"), "RAW_LINE_NEWLINE", (name, ordinal))
            payload = line[:-1]
            row = json.loads(payload, object_pairs_hook=unique_object(f"{name}:{ordinal}"))
            require(payload == canonical_bytes(row), "RAW_NONCANONICAL_ROW", (name, ordinal))
            require(row.get("raw_id") == ordinal, "RAW_ID_ORDER", (name, ordinal, row.get("raw_id")))
            source_index, remainder = divmod(ordinal, per_source)
            target_index, permutation_index = divmod(remainder, len(permutations))
            require(
                row.get("source_index") == source_index
                and row.get("target_index") == target_index
                and row.get("permutation_index") == permutation_index
                and row.get("port_permutation") == list(permutations[permutation_index]),
                "RAW_COORDINATE_BIJECTION",
                (name, ordinal),
            )
            require(row.get("schema") == spec["schema"], "RAW_SCHEMA", (name, ordinal))
            category = row.get("corrected_category")
            require(category in spec["categories"], "RAW_CATEGORY", (name, ordinal, category))
            expected_reason, expected_kind = spec["reasons"][category]
            require(row.get("exact_reason") == expected_reason, "RAW_REASON", (name, ordinal))
            evidence = row.get("evidence_binding")
            require(isinstance(evidence, dict) and evidence.get("kind") == expected_kind, "RAW_EVIDENCE_KIND", (name, ordinal))
            if category == "exact_rank_exclusion":
                allowed_upper_mechanisms = (
                    {
                        "multilinear_lambda_polynomial_vector_fields",
                        "base_fields_plus_primitive_log_field_port_transport",
                    }
                    if name == "raw4"
                    else {"coefficientwise-polynomial-vector-field-kernel"}
                )
                require(
                    evidence.get("target_upper_mechanism") in allowed_upper_mechanisms
                    and "sampled_point_evidence" not in evidence,
                    "SAMPLED_RANK_SUBSTITUTION",
                    (name, ordinal),
                )
                symbolic_rank_rows += 1
            encoded = payload.lower()
            if b"rooted_triple" in encoded or b"rooted_oracle" in encoded:
                forbidden_rows += 1
            counts[category] += 1
            first_ids.setdefault(category, ordinal)
            last_ids[category] = ordinal
            row_root.update(hashlib.sha256(payload).digest())
            raw_id_root.update(hashlib.sha256(canonical_bytes(ordinal)).digest())
            plain_root.update(line)
            plain_bytes += len(line)
    require(ordinal + 1 == spec["total"], "RAW_TOTAL", (name, ordinal + 1))
    require(source_index + 1 == spec["sources"], "RAW_SOURCE_TOTAL", name)
    require(dict(counts) == spec["categories"], "RAW_CATEGORY_CENSUS", (name, dict(counts)))
    require(forbidden_rows == 0, "RAW_FORBIDDEN_ROOTED_REASON", name)
    checks = {
        "ordered_row_hash_root": row_root.hexdigest(),
        "ordered_raw_id_hash_root": raw_id_root.hexdigest(),
        "uncompressed_stream_sha256": plain_root.hexdigest(),
        "uncompressed_bytes": plain_bytes,
        "ledger_sha256": sha_file(path),
    }
    for key, observed in checks.items():
        require(observed == summary[key], "RAW_SUMMARY_ROOT", (name, key))
    require(summary["category_counts"] == spec["categories"], "RAW_SUMMARY_CATEGORY", name)
    return {
        "rows": spec["total"],
        "category_counts": dict(counts),
        "first_raw_id_by_category": first_ids,
        "last_raw_id_by_category": last_ids,
        "symbolic_rank_rows": symbolic_rank_rows,
        "ordered_row_hash_root": checks["ordered_row_hash_root"],
        "ordered_raw_id_hash_root": checks["ordered_raw_id_hash_root"],
        "forbidden_rooted_rows": 0,
    }


def row_hash_without(row: dict[str, Any], field: str) -> str:
    clean = dict(row)
    expected = clean.pop(field)
    observed = sha_object(clean)
    require(expected == observed, "ROW_SELF_HASH", field)
    return observed


def restoration_audit(project: Path) -> dict[str, Any]:
    path = project / "work/restoration_sign_reclassification/corrected_restoration_forest.json"
    document = load_unique_json(path)
    payload = dict(document)
    expected_payload = payload.pop("payload_sha256")
    require(expected_payload == sha_object(payload), "RESTORATION_PAYLOAD")
    first = document["first_coverage"]
    second = document["second_coverage"]
    require(len(first) == 36_568 and len(second) == 256, "RESTORATION_CHILD_CENSUS")
    roots = collections.Counter(row["root_id"] for row in first)
    require(len(roots) == 2_540 and min(roots.values()) > 0, "RESTORATION_ROOT_CENSUS")
    first_hashes = []
    continuations: dict[int, dict[str, Any]] = {}
    proof_counts: collections.Counter[str] = collections.Counter()
    source_transports = document["first_source_transport_certificates"]
    target_transports = document["first_target_transport_certificates"]
    certificate_sets = {
        "displayed_quartet_mismatch": document["quartet_certificates"],
        "exact_multihomogeneous_quadratic": document["algebra_certificates"],
        "inherited_exact_F_2_112_quartic": document["algebra_certificates"],
    }

    def require_certificate_link(row: dict[str, Any], context: Any) -> None:
        proof = row["proof"]
        if proof in certificate_sets:
            require(set(row) >= {"certificate_sha256"}, "RESTORATION_CERTIFICATE_FIELD", context)
            require(
                row["certificate_sha256"] in certificate_sets[proof],
                "RESTORATION_CERTIFICATE_LINK",
                context,
            )
            return
        require(proof == "full_map_Ti_zero_strict_sign", "RESTORATION_UNKNOWN_PROOF", (context, proof))
        cert = row.get("certificate")
        require(isinstance(cert, dict), "RESTORATION_SIGN_CERTIFICATE_FIELD", context)
        signed_hash = cert.get("signed_pullback_sha256")
        require(signed_hash in document["sign_certificates"], "RESTORATION_SIGN_CERTIFICATE_LINK", context)
        registry = document["sign_certificates"][signed_hash]
        for field in (
            "strict_sign",
            "normalized_negative_pullback_sha256",
            "observable_boundary_multidegree",
        ):
            require(cert.get(field) == registry.get(field), "RESTORATION_SIGN_CERTIFICATE_BINDING", (context, field))
        require(
            {cert.get("signed_side"), cert.get("zero_side")} == {"source", "target"},
            "RESTORATION_SIGN_SIDES",
            context,
        )
    for ordinal, row in enumerate(first):
        require(row["ordinal"] == ordinal, "RESTORATION_FIRST_ORDINAL", ordinal)
        first_hashes.append(row_hash_without(row, "row_sha256"))
        require(row["source_parent_transport_id"] in source_transports, "RESTORATION_SOURCE_TRANSPORT", ordinal)
        require(row["target_parent_transport_id"] in target_transports, "RESTORATION_TARGET_TRANSPORT", ordinal)
        require(0 <= row["source_insertion_index"] < 8, "RESTORATION_INSERTION_INDEX", ordinal)
        proof_counts[row["proof"]] += 1
        if row["status"] == "continuation":
            require(row["proof"] == "restore_remaining_physical_role", "RESTORATION_CONTINUATION_PROOF", ordinal)
            require(
                row.get("certificate")
                == {
                    "all_asymmetric_Ti_search": "none",
                    "next_restored_role": row["remaining_roles"][0],
                    "next_restored_label": 5,
                    "expected_source_insertion_children": 8,
                },
                "RESTORATION_CONTINUATION_CERTIFICATE",
                ordinal,
            )
            continuations[ordinal] = row
        else:
            require(row["status"] == "separated", "RESTORATION_FIRST_STATUS", ordinal)
            require_certificate_link(row, ("first", ordinal))
    require(len(set(first_hashes)) == len(first_hashes), "RESTORATION_FIRST_DUPLICATE_HASH")
    require(first_hashes == document["first_row_hashes"], "RESTORATION_FIRST_HASH_LEDGER")
    require(sha_object(first_hashes) == document["first_hash_root"], "RESTORATION_FIRST_HASH_ROOT")
    require(len(continuations) == 32, "RESTORATION_CONTINUATION_CENSUS")

    second_hashes = []
    second_per_parent: collections.Counter[int] = collections.Counter()
    for row in second:
        second_hashes.append(row_hash_without(row, "row_sha256"))
        parent_index = row["parent_first_coverage_index"]
        require(parent_index in continuations, "RESTORATION_SECOND_WRONG_PARENT", parent_index)
        parent = continuations[parent_index]
        require(
            row["parent_first_row_sha256"] == parent["row_sha256"]
            and row["root_id"] == parent["root_id"]
            and row["first_restored_role"] == parent["restored_role"]
            and row["first_restored_label"] == parent["restored_label"],
            "RESTORATION_SECOND_PARENT_BINDING",
            parent_index,
        )
        require(row["status"] == "separated" and not row["remaining_roles"], "RESTORATION_SECOND_TERMINAL")
        require(0 <= row["second_source_insertion_index"] < 8, "RESTORATION_SECOND_INSERTION")
        require_certificate_link(row, ("second", row.get("ordinal")))
        second_per_parent[parent_index] += 1
    require(len(set(second_hashes)) == len(second_hashes), "RESTORATION_SECOND_DUPLICATE_HASH")
    require(second_hashes == document["second_row_hashes"], "RESTORATION_SECOND_HASH_LEDGER")
    require(sha_object(second_hashes) == document["second_hash_root"], "RESTORATION_SECOND_HASH_ROOT")
    require(set(second_per_parent) == set(continuations), "RESTORATION_PARENT_COVERAGE")
    require(set(second_per_parent.values()) == {8}, "RESTORATION_CHILDREN_PER_CONTINUATION")
    leaves = sum(row["status"] == "separated" for row in first) + len(second)
    require(leaves == 36_792, "RESTORATION_LEAF_CENSUS")
    require(document["census"]["forest_edges"] == len(first) + len(second), "RESTORATION_EDGE_CENSUS")
    return {
        "canonical_parents": document["census"]["canonical_restoration_parents"],
        "member_roots": len(roots),
        "first_children": len(first),
        "continuation_parents": len(continuations),
        "second_children": len(second),
        "forest_edges": len(first) + len(second),
        "terminal_leaves": leaves,
        "duplicate_rows": 0,
        "missing_or_wrong_parents": 0,
        "cycles": 0,
        "first_proof_counts": dict(proof_counts),
    }


def iterative_row_root(rows: Iterable[dict[str, Any]]) -> tuple[str, int]:
    root = sha_object([])
    count = 0
    for row in rows:
        root = sha_object({"previous": root, "row_sha256": sha_object(row)})
        count += 1
    return root, count


def load_gzip_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    with gzip.open(path, "rb") as handle:
        for ordinal, line in enumerate(handle):
            require(line.endswith(b"\n"), "GZIP_LEDGER_NEWLINE", (path.name, ordinal))
            row = json.loads(line, object_pairs_hook=unique_object(f"{path.name}:{ordinal}"))
            require(line[:-1] == canonical_bytes(row), "GZIP_LEDGER_NONCANONICAL", (path.name, ordinal))
            rows.append(row)
    return rows


def probe_audit(project: Path) -> dict[str, Any]:
    root = project / "work/probe_coherence_corrected"
    certificate = load_unique_json(root / "probe_coherence_certificate.json")
    payload = dict(certificate)
    expected = payload.pop("payload_sha256")
    require(expected == sha_object(payload), "PROBE_PAYLOAD")
    one = load_gzip_rows(root / "one_port_ledger.jsonl.gz")
    two = load_gzip_rows(root / "two_port_ledger.jsonl.gz")
    parents = load_gzip_rows(root / "two_port_parent_inventory.jsonl.gz")
    transports = load_gzip_rows(root / "exact_transport_ledger.jsonl.gz")
    restrictions = load_gzip_rows(root / "parent_restriction_ledger.jsonl.gz")
    registry = json.load(gzip.open(root / "separation_proof_registry.json.gz", "rt"), object_pairs_hook=unique_object("separation_registry"))

    for rows, section, field in (
        (one, certificate["one_port"], "ordered_ledger"),
        (two, certificate["two_port"], "ordered_ledger"),
        (parents, certificate["two_port"], "ordered_parent_inventory"),
        (transports, certificate["registries"]["exact_transports"], "ordered_records"),
        (restrictions, certificate["registries"]["parent_restrictions"], "ordered_records"),
    ):
        observed_root, count = iterative_row_root(rows)
        require(count == section[field]["rows"], "PROBE_ORDERED_COUNT", field)
        require(observed_root == section[field]["ordered_hash_root"], "PROBE_ORDERED_ROOT", field)

    transport_ids = {row["record_id"] for row in transports}
    restriction_ids = {row["record_id"] for row in restrictions}
    require(len(transport_ids) == len(transports) == 67_741, "PROBE_TRANSPORT_UNIQUENESS")
    require(len(restriction_ids) == len(restrictions) == 4_379, "PROBE_RESTRICTION_UNIQUENESS")
    triangle_transports = 0
    for row in transports:
        record = row["record"]
        require(row["record_kind"] == "exact_labelled_mixed_graph_transport", "PROBE_TRANSPORT_KIND")
        require(row["record_id"] == record["transport_sha256"], "PROBE_TRANSPORT_ID")
        require(record["relation"] in {"isomorphic", "triangle"}, "PROBE_TRANSPORT_RELATION")
        if record["relation"] == "triangle":
            triangle_transports += 1
            require(
                record["ordinary_triangle_arrowhead_witness"] is not None
                and record["source_triangle_edges"] is not None
                and record["target_triangle_edges"] is not None,
                "PROBE_TRIANGLE_WITNESS_MISSING",
            )
        else:
            require(record["ordinary_triangle_arrowhead_witness"] is None, "PROBE_INVENTED_TRIANGLE")
    for row in restrictions:
        record = row["record"]
        require(row["record_kind"] == "exact_parent_marginal_restriction", "PROBE_RESTRICTION_KIND")
        require(row["record_id"] == "R:" + sha_object(record), "PROBE_RESTRICTION_ID")
        require(
            record["exact_labelled_relation"] == "isomorphic"
            and record["parent_mixed_graph_sha256"] == record["restricted_mixed_graph_sha256"]
            and len(record["restriction_transport_sha256"]) == 64
            and all(character in "0123456789abcdef" for character in record["restriction_transport_sha256"]),
            "PROBE_RESTRICTION_SEMANTICS",
        )

    topological = registry["separation_proof_registry"]
    ti = registry["full_map_Ti_registry"]["certificates"]
    one_counts: collections.Counter[str] = collections.Counter()
    equality_parent_ids = set()
    for row in one:
        status = row["status"]
        one_counts[status] += 1
        require(row["source_parent_restriction_id"] in restriction_ids, "PROBE_ONE_SOURCE_RESTRICTION")
        require(row["target_parent_restriction_id"] in restriction_ids, "PROBE_ONE_TARGET_RESTRICTION")
        if status in {"isomorphic", "triangle"}:
            require(row["transport_id"] in transport_ids and row["parent_transport_id"] in transport_ids, "PROBE_ONE_TRANSPORT")
            equality_parent_ids.add(
                f"P1:{row['parent_anchor_id']}:{row['source_site_index']}:{row['target_site_index']}"
            )
        elif status == "displayed_quartet_mismatch":
            require(row["proof_id"] in topological, "PROBE_ONE_QUARTET_PROOF")
        elif status == "full_map_Ti_strict_sign":
            require(row["proof_id"] in ti, "PROBE_ONE_TI_PROOF")
        else:
            raise AttackFailure(f"PROBE_ONE_STATUS:{status}")
    require(dict(one_counts) == certificate["one_port"]["counts"], "PROBE_ONE_COUNTS")
    require(len(one) == 29_964 and len(equality_parent_ids) == 2_107, "PROBE_ONE_CENSUS")

    parent_ids = {row["one_port_parent_id"] for row in parents}
    require(len(parent_ids) == len(parents) == 2_107, "PROBE_PARENT_UNIQUENESS")
    require(parent_ids == equality_parent_ids, "PROBE_PARENT_INVENTORY_JOIN")
    expected_two_rows = sum(row["raw_second_probe_pairs"] for row in parents)
    require(expected_two_rows == len(two) == 544_571, "PROBE_TWO_PARENT_SUM")

    two_counts: collections.Counter[str] = collections.Counter()
    rows_by_parent: collections.Counter[str] = collections.Counter()
    for row in two:
        status = row["status"]
        two_counts[status] += 1
        parent_id = row["one_port_parent_id"]
        require(parent_id in parent_ids, "PROBE_TWO_UNKNOWN_PARENT")
        rows_by_parent[parent_id] += 1
        require(row["source_parent_restriction_id"] in restriction_ids, "PROBE_TWO_SOURCE_RESTRICTION")
        require(row["target_parent_restriction_id"] in restriction_ids, "PROBE_TWO_TARGET_RESTRICTION")
        if status in {"isomorphic", "triangle"}:
            require(row["transport_id"] in transport_ids and row["parent_transport_id"] in transport_ids, "PROBE_TWO_TRANSPORT")
            reverse = row.get("reverse_order_certificate")
            require(
                isinstance(reverse, dict)
                and reverse.get("reverse_parent_transport_id") in transport_ids
                and reverse.get("same_base_anchor_id") == row["base_anchor_id"],
                "PROBE_REVERSE_ORDER_CERTIFICATE",
            )
        elif status == "displayed_quartet_mismatch":
            require(row["proof_id"] in topological, "PROBE_TWO_QUARTET_PROOF")
        elif status == "full_map_Ti_strict_sign":
            require(row["proof_id"] in ti, "PROBE_TWO_TI_PROOF")
        else:
            raise AttackFailure(f"PROBE_TWO_STATUS:{status}")
    require(dict(two_counts) == certificate["two_port"]["counts"], "PROBE_TWO_COUNTS")
    declared_by_parent = {row["one_port_parent_id"]: row["raw_second_probe_pairs"] for row in parents}
    require(dict(rows_by_parent) == declared_by_parent, "PROBE_TWO_PARENT_BLOCK_COUNTS")
    return {
        "anchors": certificate["anchor_inventory"]["anchors"],
        "source_sites": certificate["anchor_inventory"]["source_sites"],
        "target_sites": certificate["anchor_inventory"]["target_sites"],
        "one_port_rows": len(one),
        "one_port_equality_parents": len(equality_parent_ids),
        "two_port_rows": len(two),
        "two_port_equality_rows": two_counts["isomorphic"] + two_counts["triangle"],
        "exact_transports": len(transports),
        "triangle_transports": triangle_transports,
        "parent_restrictions": len(restrictions),
        "missing_parent_or_transport_links": 0,
        "invented_triangle_witnesses": 0,
    }


def cycle_audit(project: Path) -> dict[str, Any]:
    root = project / "work/cycle_three_port_closure/promotion"
    certificate = load_unique_json(root / "cycle_promotion_certificate.json")
    payload = dict(certificate)
    expected = payload.pop("payload_sha256")
    require(expected == sha_object(payload), "CYCLE_PAYLOAD")
    base = load_gzip_rows(root / "cycle_base_authoritative.jsonl.gz")
    full = load_gzip_rows(root / "cycle_full_authoritative.jsonl.gz")
    permutations = tuple(itertools.permutations(range(3)))
    base_counts: collections.Counter[str] = collections.Counter()
    base_hashes = []
    obligations: set[int] = set()
    for ordinal, row in enumerate(base):
        require(row["raw_id"] == ordinal, "CYCLE_BASE_RAW_ID")
        source, remainder = divmod(ordinal, 1120 * 6)
        target, permutation = divmod(remainder, 6)
        require(
            row["source_index"] == source
            and row["target_index"] == target
            and row["permutation_index"] == permutation
            and row["port_permutation"] == list(permutations[permutation]),
            "CYCLE_BASE_COORDINATES",
        )
        base_hashes.append(row_hash_without(row, "authoritative_row_sha256"))
        base_counts[row["terminal_kind"]] += 1
        if row["terminal_kind"] == "fixed_full_restoration_obligation":
            obligations.add(ordinal)
    require(len(base) == 13_440, "CYCLE_BASE_CENSUS")
    require(dict(base_counts) == certificate["base"]["terminal_census"], "CYCLE_BASE_PARTITION")
    require(sha_object(base_hashes) == certificate["base"]["ordered_authoritative_row_hash_root"], "CYCLE_BASE_HASH_ROOT")
    require(len(obligations) == 5_964, "CYCLE_OBLIGATION_CENSUS")

    full_counts: collections.Counter[str] = collections.Counter()
    full_hashes = []
    child_roots: collections.Counter[str] = collections.Counter()
    root_base: dict[str, int] = {}
    for ordinal, row in enumerate(full):
        require(row["raw_id"] == ordinal, "CYCLE_FULL_RAW_ID")
        require(row["base_raw_id"] in obligations, "CYCLE_FULL_UNKNOWN_BASE")
        require(row["port_count"] == 3 + len(row["dummy_roles_in_label_order"]), "CYCLE_PORT_COUNT")
        require(len(row["source_placement_path"]) == len(row["dummy_roles_in_label_order"]), "CYCLE_PLACEMENT_WORD")
        full_hashes.append(row_hash_without(row, "authoritative_row_sha256"))
        full_counts[row["terminal_kind"]] += 1
        child_roots[row["root_id"]] += 1
        prior = root_base.setdefault(row["root_id"], row["base_raw_id"])
        require(prior == row["base_raw_id"], "CYCLE_ROOT_MULTIPLE_BASES")
    require(len(full) == 536_364, "CYCLE_FULL_CENSUS")
    require(dict(full_counts) == certificate["full"]["terminal_census"], "CYCLE_FULL_PARTITION")
    require(sha_object(full_hashes) == certificate["full"]["ordered_authoritative_row_hash_root"], "CYCLE_FULL_HASH_ROOT")
    require(len(child_roots) == 5_964 and min(child_roots.values()) > 0, "CYCLE_ROOT_CHILD_COVERAGE")
    require(set(root_base.values()) == obligations, "CYCLE_BASE_ROOT_COVERAGE")
    return {
        "base_rows": len(base),
        "base_partition": dict(base_counts),
        "restoration_roots": len(obligations),
        "full_children": len(full),
        "full_partition": dict(full_counts),
        "roots_with_zero_children": 0,
        "wrong_base_or_parent_links": 0,
    }


def main() -> None:
    require(__debug__, "OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    require(project.is_dir(), "PROJECT_MISSING", project)
    result = {
        "schema": "k2p-r4-independent-semantic-attack-v1",
        "status": "PASS",
        "independence": (
            "Direct standard-library parsing, hashing, raw-coordinate reconstruction, "
            "parent/transport joins, and explicit graph predicates; no submitted "
            "classifier or release verifier is invoked."
        ),
        "outer_manifest": validate_outer_manifest(project),
        "json_unique_name_scan": scan_json_documents(project),
        "primitive_graphs": primitive_graph_audit(project),
        "raw_ledgers": {
            name: stream_raw_ledger(project, name, spec)
            for name, spec in RAW_LEDGER_SPECS.items()
        },
        "restoration": restoration_audit(project),
        "probe": probe_audit(project),
        "cycle": cycle_audit(project),
    }
    result["payload_sha256"] = sha_object(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "payload_sha256": result["payload_sha256"],
        "raw_rows": sum(row["rows"] for row in result["raw_ledgers"].values()),
        "probe_rows": result["probe"]["one_port_rows"] + result["probe"]["two_port_rows"],
        "cycle_rows": result["cycle"]["base_rows"] + result["cycle"]["full_children"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except AttackFailure as error:
        print(f"R4_INDEPENDENT_ATTACK_FAIL:{error}", file=sys.stderr)
        raise SystemExit(1)
