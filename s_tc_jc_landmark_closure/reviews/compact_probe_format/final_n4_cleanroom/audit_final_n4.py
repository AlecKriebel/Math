#!/usr/bin/env python3
"""Clean-room audit of the four final complement-normalized n=4 shards.

This program imports only :mod:`engine` from this review directory plus
general-purpose libraries.  In particular it imports no producer, verifier,
graph, canonicalization, descriptor, invariant, or separator module under
``primary``.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys

from engine import (
    RootedGraph,
    admissible_internal_arcs,
    class_audit,
    derive_and_validate_transport,
    exact_poly_hash,
    file_sha256,
    insert_port,
    load_invariants,
    polynomial_record,
    pullback,
    quartet_descriptor,
    require,
    stable_bytes,
    stable_hash,
    transport_restricts,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
PRIMARY = PROJECT / "primary"
CERT = PRIMARY / "certificates"

EXPECTED_COMPACT = {
    "s0": "9649b08315dbd5d9dca8b8e4e1892deefe4cecacd81ea6f1880d994e56bd0863",
    "s1": "ea0c7181389d4bb73a7a1332ec396f0223cf0e9746efde9f39bc79d3d3029de1",
    "s2": "ab678bcbd268ffd704fa79c45ac8a1eb89e2907132eb5e12a99a625cc606ebbd",
    "s3": "ffa5658edfaac800da9614fcaf32a576a09d26d6d1449fc89a2ac66efff551d6",
}
EXPECTED_VERBOSE = "7e1c06223a683b888c365b4fa0fbe0568896a3c4e466be9b382f8d0fd7066c7a"
CLASS_BY_CODE = {
    0: "generic_polynomial_separation",
    1: "strict_open_cube_separation",
    2: "labelled_isomorphism",
    3: "ordinary_T",
}
SEPARATED = {"generic_polynomial_separation", "strict_open_cube_separation"}
ALLOWED_CHILD = {"labelled_isomorphism", "ordinary_T"}
ALLOWED_BASE = {
    "support_prefix_labelled_isomorphism": "labelled_isomorphism",
    "support_prefix_ordinary_T": "ordinary_T",
}
INDEX_MASK = (1 << 29) - 1


def normalized(path: Path) -> str:
    path = path.resolve()
    try:
        return str(path.relative_to(PROJECT))
    except ValueError:
        return str(path)


def resolve(value: str | Path, relative_to: Path | None = None) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    candidates = [PROJECT / path]
    if relative_to is not None:
        candidates.append(relative_to.resolve().parent / path)
    candidates.append(path)
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return candidates[0].resolve()


def read_gzip(path: Path, key: str | None = None):
    rows = []
    seen = set()
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for line_number, raw in enumerate(handle, 1):
            digest.update(raw)
            row = json.loads(raw)
            if key is not None:
                identifier = row[key]
                require(identifier not in seen, "duplicate_stream_key",
                        path=normalized(path), line=line_number,
                        identifier=identifier)
                seen.add(identifier)
            rows.append(row)
    return rows, digest.hexdigest()


def keyed_gzip(path: Path, key: str):
    rows, digest = read_gzip(path, key)
    return {row[key]: row for row in rows}, digest


def graph_original_id(payload: dict) -> str:
    return stable_hash(payload)


def inventory_commitment(rows) -> str:
    digest = hashlib.sha256()
    for row in rows:
        digest.update(stable_bytes(row) + b"\n")
    return digest.hexdigest()


def build_inventory(base_summaries: list[Path]):
    inventory = []
    inputs = {}
    for summary_path in sorted((p.resolve() for p in base_summaries),
                               key=normalized):
        summary = json.loads(summary_path.read_text())
        inputs[normalized(summary_path)] = file_sha256(summary_path)
        for run_index, run in enumerate(summary["runs"]):
            cover = run["hard_cover"]
            state_path = resolve(cover["relation_path"], summary_path)
            graph_path = resolve(cover["graph_library_path"], summary_path)
            inputs[normalized(state_path)] = file_sha256(state_path)
            inputs[normalized(graph_path)] = file_sha256(graph_path)
            states, _ = keyed_gzip(state_path, "state_id")
            graph_rows, _ = keyed_gzip(graph_path, "graph_id")
            for state_id in sorted(states):
                state = states[state_id]
                terminal = state["terminal_classification"]
                if terminal not in ALLOWED_BASE:
                    continue
                for coverage in sorted(state["raw_coverage"],
                                       key=lambda item: item["path_binding_id"]):
                    source_historical = str(coverage["source_graph_id"])
                    target_historical = str(coverage["target_graph_id"])
                    require(source_historical in graph_rows and
                            target_historical in graph_rows,
                            "inventory_parent_graph_missing")
                    source_payload = graph_rows[source_historical]["rooted_graph"]
                    target_payload = graph_rows[target_historical]["rooted_graph"]
                    require(graph_original_id(source_payload) == source_historical,
                            "historical_source_graph_id")
                    require(graph_original_id(target_payload) == target_historical,
                            "historical_target_graph_id")
                    source = RootedGraph.from_payload(source_payload)
                    target = RootedGraph.from_payload(target_payload)
                    inventory.append({
                        "base_summary": normalized(summary_path),
                        "base_run_index": run_index,
                        "base_state_id": state_id,
                        "base_terminal_classification": terminal,
                        "base_path_binding_id": str(coverage["path_binding_id"]),
                        "fixed_full_root_case_id": str(coverage["root_case_id"]),
                        "selected_port_count": int(state["selected_port_count"]),
                        "source_parent_graph_id": source_historical,
                        "target_parent_graph_id": target_historical,
                        "source_parent_normalized_graph_id": source.graph_id,
                        "target_parent_normalized_graph_id": target.graph_id,
                        "base_dummy_order": coverage["dummy_order"],
                        "base_restored_role_to_label":
                            coverage["restored_role_to_label"],
                        "source": source,
                        "target": target,
                    })
    inventory.sort(key=lambda item: (
        item["base_summary"], item["base_run_index"], item["base_state_id"],
        item["base_path_binding_id"],
    ))
    fields = (
        "base_summary", "base_run_index", "base_state_id",
        "base_path_binding_id", "fixed_full_root_case_id",
        "selected_port_count", "source_parent_graph_id",
        "target_parent_graph_id", "source_parent_normalized_graph_id",
        "target_parent_normalized_graph_id", "base_dummy_order",
        "base_restored_role_to_label",
    )
    commitment = [
        {"path_index": index, **{key: item[key] for key in fields}}
        for index, item in enumerate(inventory)
    ]
    return inventory, commitment, dict(sorted(inputs.items()))


def decode_words(text: str, expected: int):
    raw = base64.b64decode(text, validate=True) if text else b""
    require(len(raw) == expected * 4, "packed_word_length",
            actual=len(raw), expected=expected * 4)
    return tuple(struct.unpack(f"<{expected}I", raw)) if expected else ()


def verify_stream(summary_path: Path, metadata: dict, key: str):
    path = resolve(metadata["path"], summary_path)
    require(file_sha256(path) == metadata["file_sha256"],
            "stream_file_sha256", stream=key)
    rows, logical = read_gzip(path, key)
    require(logical == metadata["sha256"], "stream_logical_sha256", stream=key)
    require(len(rows) == int(metadata["records"]), "stream_record_count",
            stream=key)
    return rows, logical, path


def load_compact(summary_path: Path, expected_sha: str):
    require(file_sha256(summary_path) == expected_sha, "compact_summary_sha256",
            summary=normalized(summary_path))
    summary = json.loads(summary_path.read_text())
    require(summary["schema"] == "compact-path-bound-probe-extension-v1",
            "compact_schema")
    require(summary["status"] == "EXACTLY_COMPUTED", "compact_status")
    schema_path = resolve(summary["schema_specification"], summary_path)
    require(file_sha256(schema_path) == summary["schema_specification_sha256"],
            "schema_specification_sha256")
    for name, expected in summary["input_sha256"].items():
        require(file_sha256(resolve(name, summary_path)) == expected,
                "compact_input_sha256", input=name)
    bit_path = resolve(summary["bit_cache"]["path"], summary_path)
    require(file_sha256(bit_path) == summary["bit_cache"]["sha256"],
            "bit_cache_sha256")
    key_map = {
        "paths": "path_index", "witnesses": "witness_index",
        "transports": "transport_index", "polynomials": "polynomial_id",
    }
    streams = {}
    digests = {}
    paths = {}
    for name, key in key_map.items():
        rows, digest, path = verify_stream(summary_path,
                                           summary["streams"][name], key)
        streams[name] = rows
        digests[name] = digest
        paths[name] = path
    witnesses = {int(row["witness_index"]): row for row in streams["witnesses"]}
    transports = {int(row["transport_index"]): row for row in streams["transports"]}
    polynomials = {str(row["polynomial_id"]): row for row in streams["polynomials"]}
    require(set(witnesses) == set(range(len(witnesses))), "witness_contiguity")
    require(set(transports) == set(range(len(transports))), "transport_contiguity")
    for index, row in witnesses.items():
        body = {key: row[key] for key in
                ("classification", "probe_classification", "probe_witness")}
        require(stable_hash(body) == row["witness_id"],
                "witness_content_id", index=index)
    for index, row in transports.items():
        body = {key: row[key] for key in
                ("classification", "transport", "canonicalization",
                 "fourier_coordinate_transport")}
        require(stable_hash(body) == row["transport_id"],
                "transport_content_id", index=index)
    for identifier, row in polynomials.items():
        body = {key: row[key] for key in ("schema", "variable_count", "terms")}
        require(stable_hash(body) == identifier, "polynomial_content_id",
                polynomial_id=identifier)
    start, stop = map(int, summary["path_range"])
    require([int(row["path_index"]) for row in streams["paths"]] ==
            list(range(start, stop)), "path_stream_exact_range")
    return {
        "summary": summary, "summary_path": summary_path,
        "summary_sha256": expected_sha,
        "paths": streams["paths"], "witnesses": witnesses,
        "transports": transports, "polynomials": polynomials,
        "stream_sha256": digests, "stream_paths": paths,
    }


def verify_verbose_stream(summary_path: Path, summary: dict, name: str, key: str):
    metadata = summary["streams"][name]
    path = resolve(metadata["path"], summary_path)
    rows, logical = read_gzip(path, key)
    require(logical == metadata["sha256"], "verbose_stream_sha256", stream=name)
    require(len(rows) == int(metadata["records"]), "verbose_stream_count", stream=name)
    return rows, logical, path


def load_verbose(summary_path: Path):
    require(file_sha256(summary_path) == EXPECTED_VERBOSE,
            "verbose_summary_sha256")
    summary = json.loads(summary_path.read_text())
    require(summary["schema"] == "path-bound-common-anchor-probe-extension-v1",
            "verbose_schema")
    require(summary["status"] == "EXACTLY_COMPUTED", "verbose_status")
    loaded = {}
    digests = {}
    paths = {}
    for name, key in (("bindings", "probe_path_binding_id"),
                      ("states", "state_id"),
                      ("graphs", "graph_id"),
                      ("polynomials", "polynomial_id")):
        rows, digest, path = verify_verbose_stream(summary_path, summary, name, key)
        loaded[name] = rows
        digests[name] = digest
        paths[name] = path
    bindings = loaded["bindings"]
    states = {str(row["state_id"]): row for row in loaded["states"]}
    graphs = {str(row["graph_id"]): row for row in loaded["graphs"]}
    polynomials = {str(row["polynomial_id"]): row
                   for row in loaded["polynomials"]}
    for binding in bindings:
        body = {key: value for key, value in binding.items()
                if key not in {"schema", "probe_path_binding_id"}}
        require(stable_hash(body) == binding["probe_path_binding_id"],
                "verbose_binding_content_id")
    for identifier, state in states.items():
        body = {key: value for key, value in state.items()
                if key not in {"schema", "state_id"}}
        require(stable_hash(body) == identifier, "verbose_state_content_id")
    for identifier, row in graphs.items():
        require(graph_original_id(row["rooted_graph"]) == identifier,
                "verbose_graph_content_id", graph_id=identifier)
    for identifier, row in polynomials.items():
        body = {key: row[key] for key in ("schema", "variable_count", "terms")}
        require(stable_hash(body) == identifier, "verbose_polynomial_content_id")
    by_base = defaultdict(list)
    for binding in bindings:
        by_base[str(binding["base_path_binding_id"])].append(binding)
    return {
        "summary": summary, "summary_path": summary_path,
        "summary_sha256": EXPECTED_VERBOSE,
        "bindings": bindings, "bindings_by_base": by_base,
        "states": states, "graphs": graphs, "polynomials": polynomials,
        "stream_sha256": digests, "stream_paths": paths,
    }


class RelationWriter:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.raw = path.open("wb")
        self.gz = gzip.GzipFile(filename="", mode="wb", fileobj=self.raw, mtime=0)
        self.digest = hashlib.sha256()
        self.records = 0

    def write(self, row):
        raw = stable_bytes(row) + b"\n"
        self.gz.write(raw)
        self.digest.update(raw)
        self.records += 1

    def close(self):
        self.gz.close(); self.raw.close()
        return {
            "path": normalized(self.path), "records": self.records,
            "sha256": self.digest.hexdigest(),
            "file_sha256": file_sha256(self.path),
        }


def graph_library_check(verbose, identifier: str, expected: RootedGraph,
                        arcs=None):
    require(identifier == expected.graph_id, "generated_child_graph_id")
    require(identifier in verbose["graphs"], "verbose_graph_missing",
            graph_id=identifier)
    row = verbose["graphs"][identifier]
    require(RootedGraph.from_payload(row["rooted_graph"]) == expected,
            "verbose_graph_body", graph_id=identifier)
    require(row["rooted_valid"] is True and row["standard_strong_local"] is True,
            "verbose_graph_flags", graph_id=identifier)
    if arcs is not None:
        require(tuple(tuple(x) for x in row["admissible_internal_arcs"]) == arcs,
                "verbose_admissible_arcs", graph_id=identifier)


def binding_common(binding, state, row, *, stage, selected_count,
                   source_parent, target_parent, source_child, target_child,
                   source_insertion, target_insertion):
    require(binding["stage"] == stage and state["stage"] == stage,
            "verbose_stage")
    require(int(state["selected_port_count"]) == selected_count,
            "verbose_selected_port_count")
    for key in ("base_summary", "base_state_id", "base_path_binding_id",
                "base_dummy_order", "base_restored_role_to_label"):
        require(binding[key] == row[key], "verbose_base_provenance", key=key)
    require(binding["restoration_root_id"] == row["fixed_full_root_case_id"],
            "verbose_root_provenance")
    expected = {
        "source_parent_graph_id": source_parent,
        "target_parent_graph_id": target_parent,
        "source_child_graph_id": source_child,
        "target_child_graph_id": target_child,
    }
    for key, value in expected.items():
        require(binding[key] == value, "verbose_graph_direction", key=key)
    require(binding["source_insertion"] == source_insertion,
            "verbose_source_insertion")
    require(binding["target_insertion"] == target_insertion,
            "verbose_target_insertion")
    require(binding["source_deletion_exact_parent"] is True and
            binding["target_deletion_exact_parent"] is True,
            "verbose_deletion_flags")
    require(state["source_graph_id"] == source_child and
            state["target_graph_id"] == target_child,
            "verbose_state_graph_direction")
    require(binding["state_id"] == state["state_id"],
            "verbose_binding_state_link")


def evidence_check(word, compact, verbose_state, source: RootedGraph,
                   target: RootedGraph, port_count: int, parent_transport,
                   invariants, caches, used, context):
    code = int(word) >> 29
    index = int(word) & INDEX_MASK
    require(code in CLASS_BY_CODE, "reserved_class_code", context=context, code=code)
    classification = CLASS_BY_CODE[code]
    require(classification == verbose_state["classification"],
            "compact_verbose_classification", context=context)
    source_audit = class_audit(source); target_audit = class_audit(target)
    require(source_audit["triangle_count"] == 0 and
            target_audit["triangle_count"] == 0,
            "triangle_in_n4_base", context=context)
    caches["graphs"].update((source.graph_id, target.graph_id))
    if classification in SEPARATED:
        require(classification == "generic_polynomial_separation",
                "unexpected_strict_class", context=context)
        require(index in compact["witnesses"], "witness_index", context=context)
        record = compact["witnesses"][index]
        expected_verbose = {
            "classification": verbose_state["classification"],
            "probe_classification": verbose_state["probe_classification"],
            "probe_witness": verbose_state["probe_witness"],
        }
        require({key: record[key] for key in expected_verbose} == expected_verbose,
                "compact_verbose_witness", context=context)
        witness = record["probe_witness"]
        chunk = int(witness["quartet_chunk"])
        invariant_index = int(witness["invariant_index"])
        require(0 <= invariant_index < len(invariants), "invariant_index")
        descriptor_key_s = (source.graph_id, port_count, chunk)
        descriptor_key_t = (target.graph_id, port_count, chunk)
        if descriptor_key_s not in caches["descriptors"]:
            caches["descriptors"][descriptor_key_s] = quartet_descriptor(
                source, port_count, chunk)
        if descriptor_key_t not in caches["descriptors"]:
            caches["descriptors"][descriptor_key_t] = quartet_descriptor(
                target, port_count, chunk)
        source_descriptor = caches["descriptors"][descriptor_key_s]
        target_descriptor = caches["descriptors"][descriptor_key_t]
        pull_key_s = (source_descriptor, invariant_index)
        pull_key_t = (target_descriptor, invariant_index)
        if pull_key_s not in caches["pullbacks"]:
            caches["pullbacks"][pull_key_s] = pullback(
                source_descriptor, invariants[invariant_index])
        if pull_key_t not in caches["pullbacks"]:
            caches["pullbacks"][pull_key_t] = pullback(
                target_descriptor, invariants[invariant_index])
        source_poly = caches["pullbacks"][pull_key_s]
        target_poly = caches["pullbacks"][pull_key_t]
        require(bool(source_poly) and not target_poly,
                "generic_separator_orientation", context=context)
        require(exact_poly_hash(source_poly) ==
                witness["source_pullback_exact_sha256"],
                "exact_pullback_sha256", context=context)
        polynomial_id, body = polynomial_record(source_poly)
        require(polynomial_id == witness["source_pullback_id"],
                "pullback_polynomial_id", context=context)
        require(witness["target_pullback"] == "0", "target_pullback_marker")
        require(polynomial_id in compact["polynomials"],
                "pullback_body_missing", polynomial_id=polynomial_id)
        stored = compact["polynomials"][polynomial_id]
        require({key: stored[key] for key in body} ==
                json.loads(json.dumps(body)), "pullback_polynomial_body")
        require(polynomial_id in verbose_state["probe_witness"].values(),
                "verbose_pullback_reference")
        used["witnesses"].add(index); used["polynomials"].add(polynomial_id)
        evidence_id = record["witness_id"]
        descriptor_pair = stable_hash([source_descriptor, target_descriptor])
    else:
        require(classification == "labelled_isomorphism",
                "unexpected_T_class", context=context)
        require(index in compact["transports"], "transport_index", context=context)
        record = compact["transports"][index]
        expected_verbose = {
            "classification": verbose_state["classification"],
            "transport": verbose_state["transport"],
            "canonicalization": verbose_state["canonicalization"],
            "fourier_coordinate_transport": "identity_on_fixed_port_labels",
        }
        require({key: record[key] for key in expected_verbose} == expected_verbose,
                "compact_verbose_transport", context=context)
        mapping = derive_and_validate_transport(source, target, record)
        require(transport_restricts(mapping, parent_transport),
                "incoherent_child_transport", context=context)
        # Independently exercise the zero-sum descriptor engine on each
        # isomorphism class; labelled isomorphism must preserve every quartet.
        probe_key_s = (source.graph_id, port_count, 0)
        probe_key_t = (target.graph_id, port_count, 0)
        if probe_key_s not in caches["descriptors"]:
            caches["descriptors"][probe_key_s] = quartet_descriptor(
                source, port_count, 0)
        if probe_key_t not in caches["descriptors"]:
            caches["descriptors"][probe_key_t] = quartet_descriptor(
                target, port_count, 0)
        require(caches["descriptors"][probe_key_s] ==
                caches["descriptors"][probe_key_t],
                "isomorphism_descriptor_mismatch", context=context)
        used["transports"].add(index)
        evidence_id = record["transport_id"]
        descriptor_pair = stable_hash([
            caches["descriptors"][probe_key_s],
            caches["descriptors"][probe_key_t],
        ])
    return classification, evidence_id, mapping if classification in ALLOWED_CHILD else None, descriptor_pair


def audit_shard(compact, inventory, verbose, invariants, writer):
    summary = compact["summary"]
    start, stop = map(int, summary["path_range"])
    require(len(inventory) == int(summary["path_inventory_count"]),
            "inventory_count")
    used = {"witnesses": set(), "transports": set(), "polynomials": set(),
            "bindings": set()}
    caches = {"descriptors": {}, "pullbacks": {}, "graphs": set()}
    counts = Counter(); stage_counts = Counter()
    inventory_fields = (
        "base_summary", "base_run_index", "base_state_id",
        "base_path_binding_id", "fixed_full_root_case_id",
        "selected_port_count", "source_parent_graph_id",
        "target_parent_graph_id", "source_parent_normalized_graph_id",
        "target_parent_normalized_graph_id", "base_dummy_order",
        "base_restored_role_to_label",
    )
    total_verbose = set()
    for path_offset, row in enumerate(compact["paths"]):
        path_index = start + path_offset
        require(int(row["path_index"]) == path_index, "path_index")
        require(stable_hash({key: value for key, value in row.items()
                             if key != "path_record_id"}) == row["path_record_id"],
                "path_record_id", path_index=path_index)
        entry = inventory[path_index]
        for key in inventory_fields:
            require(row[key] == entry[key], "path_inventory_binding",
                    path_index=path_index, key=key)
        source_parent = entry["source"]; target_parent = entry["target"]
        require(source_parent.graph_id == row["source_parent_normalized_graph_id"],
                "source_parent_normalized_id")
        require(target_parent.graph_id == row["target_parent_normalized_graph_id"],
                "target_parent_normalized_id")
        for parent in (source_parent, target_parent):
            audit = class_audit(parent)
            require(audit["triangle_count"] == 0, "triangle_in_parent")
            caches["graphs"].add(parent.graph_id)

        base_index = int(row["base_transport_index"])
        require(base_index in compact["transports"], "base_transport_index")
        base_record = compact["transports"][base_index]
        require(base_record["classification"] ==
                ALLOWED_BASE[entry["base_terminal_classification"]],
                "base_transport_classification")
        require(base_record["classification"] == "labelled_isomorphism",
                "triangle_free_base_not_isomorphism")
        base_mapping = derive_and_validate_transport(
            source_parent, target_parent, base_record)
        used["transports"].add(base_index)

        source_p_arcs = admissible_internal_arcs(source_parent)
        target_p_arcs = admissible_internal_arcs(target_parent)
        require(tuple(tuple(x) for x in row["source_p_arcs"]) == source_p_arcs,
                "source_p_arc_order")
        require(tuple(tuple(x) for x in row["target_p_arcs"]) == target_p_arcs,
                "target_p_arc_order")
        p_keys = tuple((s, t) for s in source_p_arcs for t in target_p_arcs)
        require(len(p_keys) == int(row["p_word_count"]), "p_word_count")
        p_words = decode_words(row["p_words_base64_le_u32"], len(p_keys))
        q_words = decode_words(row["q_words_base64_le_u32"],
                               int(row["q_word_count"]))
        path_bindings = verbose["bindings_by_base"][row["base_path_binding_id"]]
        total_verbose.update(b["probe_path_binding_id"] for b in path_bindings)
        p_bindings = [b for b in path_bindings if b["stage"] == "A_plus_p"]
        q_bindings = [b for b in path_bindings if b["stage"] == "A_plus_p_plus_q"]
        p_by_arcs = {}
        for binding in p_bindings:
            key = (tuple(binding["source_insertion"]["subdivided_parent_arc"]),
                   tuple(binding["target_insertion"]["subdivided_parent_arc"]))
            require(key not in p_by_arcs, "duplicate_verbose_p_relation")
            p_by_arcs[key] = binding
        require(set(p_by_arcs) == set(p_keys), "p_relation_bijection",
                expected=len(p_keys), actual=len(p_by_arcs))

        allowed = []; q_shapes = []; q_cursor = 0
        p0 = int(row["selected_port_count"])
        for p_flat, (source_arc, target_arc) in enumerate(p_keys):
            source_p, source_meta = insert_port(source_parent, source_arc, f"L_{p0}")
            target_p, target_meta = insert_port(target_parent, target_arc, f"L_{p0}")
            binding = p_by_arcs[(source_arc, target_arc)]
            state = verbose["states"][binding["state_id"]]
            binding_common(
                binding, state, row, stage="A_plus_p", selected_count=p0 + 1,
                source_parent=source_parent.graph_id,
                target_parent=target_parent.graph_id,
                source_child=source_p.graph_id, target_child=target_p.graph_id,
                source_insertion=source_meta, target_insertion=target_meta)
            require(binding["parent_probe_path_binding_id"] is None,
                    "p_parent_binding")
            require(binding["base_transport"] == base_record["transport"] and
                    binding["base_canonicalization"] ==
                    base_record["canonicalization"], "verbose_base_transport")
            graph_library_check(verbose, source_p.graph_id, source_p,
                                admissible_internal_arcs(source_p))
            graph_library_check(verbose, target_p.graph_id, target_p,
                                admissible_internal_arcs(target_p))
            classification, evidence_id, child_mapping, descriptor_pair = evidence_check(
                p_words[p_flat], compact, state, source_p, target_p, p0 + 1,
                base_mapping, invariants, caches, used,
                [path_index, "p", p_flat])
            used["bindings"].add(binding["probe_path_binding_id"])
            counts[classification] += 1; stage_counts["A_plus_p"] += 1
            writer.write({
                "path_index": path_index, "stage": "A_plus_p",
                "flat_index": p_flat,
                "source_parent_graph_id": source_parent.graph_id,
                "target_parent_graph_id": target_parent.graph_id,
                "source_arc": source_arc, "target_arc": target_arc,
                "source_child_graph_id": source_p.graph_id,
                "target_child_graph_id": target_p.graph_id,
                "classification": classification,
                "evidence_id": evidence_id,
                "descriptor_pair_sha256": descriptor_pair,
                "verbose_binding_id": binding["probe_path_binding_id"],
                "verbose_state_id": state["state_id"],
            })
            if classification not in ALLOWED_CHILD:
                require(not any(q["parent_probe_path_binding_id"] ==
                                binding["probe_path_binding_id"]
                                for q in q_bindings), "q_under_separated_p")
                continue
            allowed.append(p_flat)
            source_q_arcs = admissible_internal_arcs(source_p)
            target_q_arcs = admissible_internal_arcs(target_p)
            q_shapes.append([len(source_q_arcs), len(target_q_arcs)])
            q_keys = tuple((s, t) for s in source_q_arcs for t in target_q_arcs)
            q_group = [q for q in q_bindings
                       if q["parent_probe_path_binding_id"] ==
                       binding["probe_path_binding_id"]]
            q_by_arcs = {}
            for q_binding in q_group:
                key = (tuple(q_binding["source_insertion"]["subdivided_parent_arc"]),
                       tuple(q_binding["target_insertion"]["subdivided_parent_arc"]))
                require(key not in q_by_arcs, "duplicate_verbose_q_relation")
                q_by_arcs[key] = q_binding
            require(set(q_by_arcs) == set(q_keys), "q_relation_bijection",
                    expected=len(q_keys), actual=len(q_by_arcs))
            for q_local, (source_q_arc, target_q_arc) in enumerate(q_keys):
                require(q_cursor < len(q_words), "truncated_q_words")
                source_q, source_q_meta = insert_port(
                    source_p, source_q_arc, f"L_{p0 + 1}")
                target_q, target_q_meta = insert_port(
                    target_p, target_q_arc, f"L_{p0 + 1}")
                q_binding = q_by_arcs[(source_q_arc, target_q_arc)]
                q_state = verbose["states"][q_binding["state_id"]]
                binding_common(
                    q_binding, q_state, row, stage="A_plus_p_plus_q",
                    selected_count=p0 + 2,
                    source_parent=source_p.graph_id,
                    target_parent=target_p.graph_id,
                    source_child=source_q.graph_id,
                    target_child=target_q.graph_id,
                    source_insertion=source_q_meta,
                    target_insertion=target_q_meta)
                require(q_binding["parent_transport"] == state["transport"],
                        "verbose_q_parent_transport")
                graph_library_check(verbose, source_q.graph_id, source_q,
                                    admissible_internal_arcs(source_q))
                graph_library_check(verbose, target_q.graph_id, target_q,
                                    admissible_internal_arcs(target_q))
                q_class, q_evidence, _q_mapping, q_descriptor_pair = evidence_check(
                    q_words[q_cursor], compact, q_state, source_q, target_q,
                    p0 + 2, child_mapping, invariants, caches, used,
                    [path_index, "q", p_flat, q_local])
                used["bindings"].add(q_binding["probe_path_binding_id"])
                counts[q_class] += 1; stage_counts["A_plus_p_plus_q"] += 1
                writer.write({
                    "path_index": path_index, "stage": "A_plus_p_plus_q",
                    "parent_p_flat_index": p_flat,
                    "local_flat_index": q_local,
                    "global_q_flat_index": q_cursor,
                    "source_parent_graph_id": source_p.graph_id,
                    "target_parent_graph_id": target_p.graph_id,
                    "source_arc": source_q_arc, "target_arc": target_q_arc,
                    "source_child_graph_id": source_q.graph_id,
                    "target_child_graph_id": target_q.graph_id,
                    "classification": q_class,
                    "evidence_id": q_evidence,
                    "descriptor_pair_sha256": q_descriptor_pair,
                    "verbose_binding_id": q_binding["probe_path_binding_id"],
                    "verbose_state_id": q_state["state_id"],
                })
                q_cursor += 1
        require(row["allowed_p_flat_indices"] == allowed,
                "allowed_p_flat_indices")
        require(row["q_shapes"] == q_shapes, "q_shape_blocks")
        require(q_cursor == len(q_words), "q_word_exhaustion")
        require(len(path_bindings) == len(p_bindings) + len(q_bindings),
                "unknown_verbose_stage")
        require(set(b["probe_path_binding_id"] for b in path_bindings) <=
                used["bindings"], "unconsumed_verbose_path_binding")

    require(used["bindings"] == total_verbose, "verbose_binding_bijection",
            used=len(used["bindings"]), expected=len(total_verbose))
    require(dict(sorted(counts.items())) == summary["counts"],
            "classification_counts", actual=dict(sorted(counts.items())),
            expected=summary["counts"])
    require(used["witnesses"] == set(compact["witnesses"]),
            "orphan_witnesses")
    require(used["transports"] == set(compact["transports"]),
            "orphan_transports")
    require(used["polynomials"] == set(compact["polynomials"]),
            "orphan_polynomials")
    for identifier, row in compact["polynomials"].items():
        require(identifier in verbose["polynomials"],
                "verbose_polynomial_missing", polynomial_id=identifier)
        require(row == verbose["polynomials"][identifier],
                "compact_verbose_polynomial_body", polynomial_id=identifier)
    return {
        "counts": dict(sorted(counts.items())),
        "stage_counts": dict(sorted(stage_counts.items())),
        "verbose_bindings_compared": len(used["bindings"]),
        "witnesses_replayed": len(used["witnesses"]),
        "transports_replayed": len(used["transports"]),
        "polynomials_replayed": len(used["polynomials"]),
        "unique_exact_rooted_graphs_audited": len(caches["graphs"]),
        "zero_sum_descriptors_regenerated": len(caches["descriptors"]),
        "exact_pullbacks_regenerated": len(caches["pullbacks"]),
        "ordinary_T_cells": counts.get("ordinary_T", 0),
        "strict_open_cube_cells": counts.get("strict_open_cube_separation", 0),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--shard", choices=tuple(EXPECTED_COMPACT), required=True)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--verbose", type=Path,
                        default=CERT / "probe_extension_theta2_schema3_final_summary.json")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--relations", type=Path)
    args = parser.parse_args()
    summary_path = (args.summary or CERT /
                    f"compact_probe_theta2_compact_n4_{args.shard}_summary.json").resolve()
    output = (args.output or HERE / "certificates" /
              f"independent_{args.shard}.json").resolve()
    relation_path = (args.relations or HERE / "certificates" /
                     f"normalized_relations_{args.shard}.jsonl.gz").resolve()
    compact = load_compact(summary_path, EXPECTED_COMPACT[args.shard])
    base_paths = [resolve(path, summary_path)
                  for path in compact["summary"]["base_summaries"]]
    inventory, commitment_rows, input_hashes = build_inventory(base_paths)
    require(len(inventory) == int(compact["summary"]["path_inventory_count"]),
            "inventory_count")
    require(inventory_commitment(commitment_rows) ==
            compact["summary"]["path_inventory_sha256"],
            "inventory_commitment")
    require(input_hashes == compact["summary"]["input_sha256"],
            "inventory_input_commitments")
    verbose = load_verbose(args.verbose.resolve())
    invariants = load_invariants(
        PROJECT.parent / "strong_level2_phylo_identifiability/src/jc_root_spanning_atlas_data.py",
        PRIMARY / "seventh_invariant.json")
    writer = RelationWriter(relation_path)
    try:
        audit = audit_shard(compact, inventory, verbose, invariants, writer)
    except Exception:
        writer.gz.close(); writer.raw.close()
        raise
    relation_metadata = writer.close()
    require(relation_metadata["records"] == audit["verbose_bindings_compared"],
            "normalized_relation_record_count")
    payload = {
        "schema": "compact-probe-final-n4-cleanroom-replay-v1",
        "status": "VERIFIED",
        "scope": "one exact final complement-normalized n=4 compact shard",
        "shard": args.shard,
        "summary": normalized(summary_path),
        "summary_sha256": EXPECTED_COMPACT[args.shard],
        "path_range": compact["summary"]["path_range"],
        "path_inventory_count": len(inventory),
        "path_inventory_sha256": compact["summary"]["path_inventory_sha256"],
        "schema_specification_sha256":
            compact["summary"]["schema_specification_sha256"],
        "verbose_summary": normalized(args.verbose.resolve()),
        "verbose_summary_sha256": EXPECTED_VERBOSE,
        "compact_stream_sha256": compact["stream_sha256"],
        "verbose_stream_sha256": verbose["stream_sha256"],
        "semantic_comparison": audit,
        "counts": audit["counts"],
        "normalized_relation_stream": relation_metadata,
        "independent_implementation": {
            "audit_script": normalized(Path(__file__)),
            "audit_script_sha256": file_sha256(Path(__file__)),
            "engine": normalized(HERE / "engine.py"),
            "engine_sha256": file_sha256(HERE / "engine.py"),
            "imports_primary_modules": False,
            "descriptor_normalization":
                "minimum of quartet side and complement after zero-sum restriction",
        },
        "scope_limitations": {
            "base_is_triangle_free": True,
            "ordinary_T_cells_present": False,
            "strict_open_cube_cells_present": False,
            "claim": "No T or strict-separation format branch is exercised by this n=4 base.",
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "shard": args.shard,
        "summary_sha256": payload["summary_sha256"],
        "path_range": payload["path_range"], "counts": payload["counts"],
        "relations": relation_metadata["records"],
        "output": normalized(output), "output_sha256": file_sha256(output),
    }, sort_keys=True), flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FALSE", "error": str(exc)}, sort_keys=True),
              file=sys.stderr, flush=True)
        raise
