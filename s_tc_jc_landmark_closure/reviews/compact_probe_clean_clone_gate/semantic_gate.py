#!/usr/bin/env python3
"""Compact-only semantic replay for the tracked n=3 and theta2-n4 shards.

No verbose ``probe_extension_*`` stream is opened.  The verifier reconstructs
the relation indexed by every packed word directly from the committed
hard-cover parents and compact path row, then regenerates graph insertions,
JC descriptors, invariant pullbacks, exact signs, and unique labelled/T
transports with the already committed clean-room engines.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter, defaultdict
from dataclasses import dataclass
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CERT = PROJECT / "primary" / "certificates"
N4_ENGINE_DIR = PROJECT / "reviews" / "compact_probe_format" / "final_n4_cleanroom"
N3_ENGINE_DIR = PROJECT / "reviews" / "compact_probe_format" / "final_n3_cleanroom"
sys.path.insert(0, str(N4_ENGINE_DIR))
sys.path.insert(0, str(N3_ENGINE_DIR))
sys.path.insert(0, str(HERE))

from engine import (  # noqa: E402
    RootedGraph,
    admissible_internal_arcs,
    class_audit,
    derive_and_validate_transport as derive_n4_transport,
    exact_poly_hash,
    file_sha256,
    insert_port,
    invariant_orbit,
    polynomial_record,
    pullback,
    quartet_descriptor,
    require,
    stable_bytes,
    stable_hash,
    transport_restricts,
)
from engine_n3 import (  # noqa: E402
    derive_and_validate_transport as derive_n3_transport,
    prove_strict_open_cube_sign,
)
from invariant_templates import INVARIANT_TEMPLATES  # noqa: E402


CLASS_BY_CODE = {
    0: "generic_polynomial_separation",
    1: "strict_open_cube_separation",
    2: "labelled_isomorphism",
    3: "ordinary_T",
}
INDEX_MASK = (1 << 29) - 1
SEPARATED = {"generic_polynomial_separation", "strict_open_cube_separation"}
ALLOWED = {"labelled_isomorphism", "ordinary_T"}
ALLOWED_BASE = {
    "support_prefix_labelled_isomorphism": "labelled_isomorphism",
    "support_prefix_ordinary_T": "ordinary_T",
}
LOCKED_SCHEMA = HERE / "COMPACT_PROBE_SCHEMA_LOCKED.md"


@dataclass(frozen=True)
class Family:
    name: str
    summary_pattern: str
    summary_sha256: tuple[str, ...]
    inventory_count: int
    expected_counts: tuple[tuple[str, int], ...]
    expected_stage_counts: tuple[tuple[str, int], ...]
    expected_ranges: tuple[tuple[int, int], ...]
    max_triangles: int
    n3_transport: bool


FAMILIES = {
    "n3": Family(
        "n3",
        "compact_probe_schema3_n3_compact_s{shard}_summary.json",
        (
            "dc7b806f9afc1af9909682f47ea4bdc9ac5a8631d78ce3a6b15d41c4f171ad73",
            "996084af49c3e4ddf63b62cfa951be652a886e3424674f6e34d664b5a4901a37",
            "a8162d2bb136668ce2f204ce2012c85eb4dbb5e42c7037307d974b5f9ebf2286",
            "b246614dafc669784f8ef5e16ef62db79f08929b2afc2a6d14ce7f50bd7b7942",
        ),
        144,
        (
            ("generic_polynomial_separation", 90008),
            ("labelled_isomorphism", 9676),
            ("ordinary_T", 840),
            ("strict_open_cube_separation", 624),
        ),
        (("A_plus_p", 9316), ("A_plus_p_plus_q", 91832)),
        ((0, 36), (36, 72), (72, 108), (108, 144)),
        1,
        True,
    ),
    "theta2_n4": Family(
        "theta2_n4",
        "compact_probe_theta2_compact_n4_s{shard}_summary.json",
        (
            "9649b08315dbd5d9dca8b8e4e1892deefe4cecacd81ea6f1880d994e56bd0863",
            "ea0c7181389d4bb73a7a1332ec396f0223cf0e9746efde9f39bc79d3d3029de1",
            "ab678bcbd268ffd704fa79c45ac8a1eb89e2907132eb5e12a99a625cc606ebbd",
            "ffa5658edfaac800da9614fcaf32a576a09d26d6d1449fc89a2ac66efff551d6",
        ),
        132,
        (("generic_polynomial_separation", 153072),
         ("labelled_isomorphism", 15510)),
        (("A_plus_p", 12906), ("A_plus_p_plus_q", 155676)),
        ((0, 33), (33, 66), (66, 99), (99, 132)),
        0,
        False,
    ),
}


def normalized(path: Path) -> str:
    path = path.resolve()
    try:
        return str(path.relative_to(PROJECT.resolve()))
    except ValueError:
        return str(path)


def resolve(value: str | Path, relative_to: Path | None = None) -> Path:
    path = Path(value)
    if path.is_absolute():
        # Historical summaries may contain absolute producer paths.  Only the
        # basename under the current tracked certificate directory is used.
        candidate = CERT / path.name
        return candidate.resolve() if candidate.exists() else path.resolve()
    candidates = [PROJECT / path]
    if relative_to is not None:
        candidates.append(relative_to.resolve().parent / path)
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
            states, state_logical = keyed_gzip(state_path, "state_id")
            graphs, graph_logical = keyed_gzip(graph_path, "graph_id")
            require(state_logical == cover["relation_stream_sha256"],
                    "hard_cover_relation_logical_sha256")
            require(graph_logical == cover["graph_library_stream_sha256"],
                    "hard_cover_graph_logical_sha256")
            for state_id in sorted(states):
                state = states[state_id]
                terminal = state["terminal_classification"]
                if terminal not in ALLOWED_BASE:
                    continue
                for coverage in sorted(state["raw_coverage"],
                                       key=lambda item: item["path_binding_id"]):
                    source_id = str(coverage["source_graph_id"])
                    target_id = str(coverage["target_graph_id"])
                    require(source_id in graphs and target_id in graphs,
                            "inventory_parent_graph_missing")
                    source_payload = graphs[source_id]["rooted_graph"]
                    target_payload = graphs[target_id]["rooted_graph"]
                    require(graph_original_id(source_payload) == source_id,
                            "historical_source_graph_id")
                    require(graph_original_id(target_payload) == target_id,
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
                        "source_parent_graph_id": source_id,
                        "target_parent_graph_id": target_id,
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
    # The producer summaries bind the pre-clarification schema bytes.  Those
    # exact bytes are vendored in this gate and checked rather than silently
    # accepting the later prose-only revision at the historical path.
    require(file_sha256(LOCKED_SCHEMA) ==
            summary["schema_specification_sha256"],
            "locked_schema_specification_sha256")
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
    logical = {}
    paths = {}
    for name, key in key_map.items():
        rows, digest, path = verify_stream(summary_path,
                                           summary["streams"][name], key)
        streams[name] = rows
        logical[name] = digest
        paths[name] = normalized(path)
    witnesses = {int(row["witness_index"]): row
                 for row in streams["witnesses"]}
    transports = {int(row["transport_index"]): row
                  for row in streams["transports"]}
    polynomials = {str(row["polynomial_id"]): row
                   for row in streams["polynomials"]}
    require(set(witnesses) == set(range(len(witnesses))),
            "witness_contiguity")
    require(set(transports) == set(range(len(transports))),
            "transport_contiguity")
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
        require(stable_hash(body) == identifier,
                "polynomial_content_id", polynomial_id=identifier)
    start, stop = map(int, summary["path_range"])
    require([int(row["path_index"]) for row in streams["paths"]] ==
            list(range(start, stop)), "path_stream_exact_range")
    return {
        "summary": summary, "summary_path": summary_path,
        "paths": streams["paths"], "witnesses": witnesses,
        "transports": transports, "polynomials": polynomials,
        "stream_sha256": logical, "stream_paths": paths,
    }


def load_invariants():
    seventh_payload = json.loads((PROJECT / "primary" /
                                  "seventh_invariant.json").read_text())
    seventh = tuple(
        (tuple(int(index) + 1 for index in monomial), int(coefficient))
        for coefficient, monomial in seventh_payload["invariant"]
    )
    invariants = invariant_orbit((*INVARIANT_TEMPLATES, seventh))
    require(len(invariants) == 84, "invariant_orbit_count",
            actual=len(invariants))
    return invariants


def derive_transport(family: Family, source: RootedGraph,
                     target: RootedGraph, record: dict):
    if family.n3_transport:
        mapping, classification = derive_n3_transport(source, target, record)
        return mapping, classification
    mapping = derive_n4_transport(source, target, record)
    return mapping, "labelled_isomorphism"


def descriptor(caches, graph, port_count, chunk):
    key = (graph.graph_id, port_count, chunk)
    if key not in caches["descriptors"]:
        caches["descriptors"][key] = quartet_descriptor(
            graph, port_count, chunk)
    return caches["descriptors"][key]


def exact_pullback(caches, desc, invariant_index, invariants):
    key = (desc, invariant_index)
    if key not in caches["pullbacks"]:
        caches["pullbacks"][key] = pullback(desc, invariants[invariant_index])
    return caches["pullbacks"][key]


def audit_graph(caches, family: Family, graph: RootedGraph, context):
    if graph.graph_id not in caches["graph_audits"]:
        result = class_audit(graph)
        require(result["triangle_count"] <= family.max_triangles,
                "triangle_bound", context=context, audit=result)
        caches["graph_audits"][graph.graph_id] = result
    return caches["graph_audits"][graph.graph_id]


def evidence_check(*, family, word, compact, source, target, port_count,
                   parent_mapping, invariants, caches, used, context):
    require(port_count <= 10, "ten_port_bound", context=context,
            port_count=port_count)
    code = int(word) >> 29
    index = int(word) & INDEX_MASK
    require(code in CLASS_BY_CODE, "reserved_class_code", context=context,
            code=code)
    classification = CLASS_BY_CODE[code]
    audit_graph(caches, family, source, [*context, "source"])
    audit_graph(caches, family, target, [*context, "target"])

    if classification in SEPARATED:
        require(index in compact["witnesses"], "witness_index",
                context=context, index=index)
        record = compact["witnesses"][index]
        require(record["classification"] == classification and
                record["probe_classification"] == classification,
                "witness_classification", context=context)
        witness = record["probe_witness"]
        chunk = int(witness["quartet_chunk"])
        invariant_index = int(witness["invariant_index"])
        require(0 <= invariant_index < len(invariants), "invariant_index",
                context=context)
        source_desc = descriptor(caches, source, port_count, chunk)
        target_desc = descriptor(caches, target, port_count, chunk)
        source_poly = exact_pullback(
            caches, source_desc, invariant_index, invariants)
        target_poly = exact_pullback(
            caches, target_desc, invariant_index, invariants)
        sign_proof = None
        if classification == "generic_polynomial_separation":
            require(bool(source_poly) and not target_poly,
                    "generic_separator_orientation", context=context)
            require(exact_poly_hash(source_poly) ==
                    witness["source_pullback_exact_sha256"],
                    "source_exact_pullback_sha256", context=context)
            polynomial_id, body = polynomial_record(source_poly)
            require(polynomial_id == witness["source_pullback_id"],
                    "source_pullback_id", context=context)
            require(witness["target_pullback"] == "0",
                    "target_pullback_marker", context=context)
        else:
            require(not source_poly and bool(target_poly),
                    "strict_separator_orientation", context=context)
            require(witness["source_pullback"] == "0",
                    "source_pullback_marker", context=context)
            require(exact_poly_hash(target_poly) ==
                    witness["target_pullback_exact_sha256"],
                    "target_exact_pullback_sha256", context=context)
            polynomial_id, body = polynomial_record(target_poly)
            require(polynomial_id == witness["target_pullback_id"],
                    "target_pullback_id", context=context)
            sign_key = exact_poly_hash(target_poly)
            if sign_key not in caches["sign_proofs"]:
                caches["sign_proofs"][sign_key] = (
                    prove_strict_open_cube_sign(target_poly))
            sign_proof = caches["sign_proofs"][sign_key]
            require(sign_proof["strict_open_sign"] ==
                    int(witness["target_strict_sign"]),
                    "independent_strict_sign", context=context)
            stored_sign = witness["target_sign_certificate"]
            require(stored_sign["certified"] is True and
                    int(stored_sign["strict_sign"]) ==
                    int(witness["target_strict_sign"]),
                    "stored_strict_sign", context=context)
        require(polynomial_id in compact["polynomials"],
                "pullback_body_missing", context=context,
                polynomial_id=polynomial_id)
        stored = compact["polynomials"][polynomial_id]
        require({key: stored[key] for key in body} ==
                json.loads(json.dumps(body)), "pullback_polynomial_body",
                context=context)
        used["witnesses"].add(index)
        used["polynomials"].add(polynomial_id)
        mapping = None
        evidence_id = record["witness_id"]
        descriptor_pair = stable_hash([source_desc, target_desc])
    else:
        require(classification in ALLOWED, "unknown_allowed_class",
                context=context)
        require(index in compact["transports"], "transport_index",
                context=context, index=index)
        record = compact["transports"][index]
        require(record["classification"] == classification,
                "transport_classification", context=context)
        mapping, independent_class = derive_transport(
            family, source, target, record)
        require(independent_class == classification,
                "independent_transport_classification", context=context)
        require(transport_restricts(mapping, parent_mapping),
                "incoherent_child_transport", context=context)
        source_desc = descriptor(caches, source, port_count, 0)
        target_desc = descriptor(caches, target, port_count, 0)
        if classification == "labelled_isomorphism":
            require(source_desc == target_desc,
                    "isomorphism_descriptor_mismatch", context=context)
        used["transports"].add(index)
        evidence_id = record["transport_id"]
        descriptor_pair = stable_hash([source_desc, target_desc])
        sign_proof = None
    return {
        "classification": classification,
        "mapping": mapping,
        "evidence_id": evidence_id,
        "descriptor_pair_sha256": descriptor_pair,
        "sign_proof_sha256": stable_hash(sign_proof) if sign_proof else None,
    }


def update_relation_digest(digest, row):
    digest.update(stable_bytes(row) + b"\n")


def audit_shard(family: Family, compact, inventory, invariants):
    summary = compact["summary"]
    start, stop = map(int, summary["path_range"])
    require(len(inventory) == int(summary["path_inventory_count"]),
            "inventory_count")
    used = {"witnesses": set(), "transports": set(), "polynomials": set()}
    caches = {"descriptors": {}, "pullbacks": {}, "sign_proofs": {},
              "graph_audits": {}}
    counts = Counter()
    stages = Counter()
    triangles = Counter()
    relation_digest = hashlib.sha256()
    max_port_count = 0
    inventory_fields = (
        "base_summary", "base_run_index", "base_state_id",
        "base_path_binding_id", "fixed_full_root_case_id",
        "selected_port_count", "source_parent_graph_id",
        "target_parent_graph_id", "source_parent_normalized_graph_id",
        "target_parent_normalized_graph_id", "base_dummy_order",
        "base_restored_role_to_label",
    )
    for path_offset, row in enumerate(compact["paths"]):
        path_index = start + path_offset
        require(int(row["path_index"]) == path_index, "path_index")
        require(stable_hash({key: value for key, value in row.items()
                             if key != "path_record_id"}) ==
                row["path_record_id"], "path_record_id",
                path_index=path_index)
        entry = inventory[path_index]
        for key in inventory_fields:
            require(row[key] == entry[key], "path_inventory_binding",
                    path_index=path_index, key=key)
        source_parent = entry["source"]
        target_parent = entry["target"]
        require(source_parent.graph_id ==
                row["source_parent_normalized_graph_id"],
                "source_parent_normalized_id")
        require(target_parent.graph_id ==
                row["target_parent_normalized_graph_id"],
                "target_parent_normalized_id")
        audit_graph(caches, family, source_parent,
                    [path_index, "source_parent"])
        audit_graph(caches, family, target_parent,
                    [path_index, "target_parent"])

        base_index = int(row["base_transport_index"])
        require(base_index in compact["transports"], "base_transport_index")
        base_record = compact["transports"][base_index]
        expected_base = ALLOWED_BASE[entry["base_terminal_classification"]]
        require(base_record["classification"] == expected_base,
                "base_transport_classification", path_index=path_index)
        base_mapping, base_class = derive_transport(
            family, source_parent, target_parent, base_record)
        require(base_class == expected_base,
                "independent_base_transport_classification",
                path_index=path_index)
        used["transports"].add(base_index)

        source_p_arcs = admissible_internal_arcs(source_parent)
        target_p_arcs = admissible_internal_arcs(target_parent)
        require(tuple(tuple(x) for x in row["source_p_arcs"]) ==
                source_p_arcs, "source_p_arc_order", path_index=path_index)
        require(tuple(tuple(x) for x in row["target_p_arcs"]) ==
                target_p_arcs, "target_p_arc_order", path_index=path_index)
        p_keys = tuple((s, t) for s in source_p_arcs for t in target_p_arcs)
        require(len(p_keys) == int(row["p_word_count"]), "p_word_count",
                path_index=path_index)
        p_words = decode_words(row["p_words_base64_le_u32"], len(p_keys))
        q_words = decode_words(row["q_words_base64_le_u32"],
                               int(row["q_word_count"]))
        allowed = []
        q_shapes = []
        q_cursor = 0
        p0 = int(row["selected_port_count"])
        require(p0 == entry["selected_port_count"], "selected_port_count")
        require(set(source_parent.label_map.values()) ==
                {f"L_{i}" for i in range(p0)},
                "source_parent_label_order")
        require(set(target_parent.label_map.values()) ==
                {f"L_{i}" for i in range(p0)},
                "target_parent_label_order")

        for p_flat, (source_arc, target_arc) in enumerate(p_keys):
            source_p, source_meta = insert_port(
                source_parent, source_arc, f"L_{p0}")
            target_p, target_meta = insert_port(
                target_parent, target_arc, f"L_{p0}")
            require(tuple(source_meta["subdivided_parent_arc"]) == source_arc and
                    tuple(target_meta["subdivided_parent_arc"]) == target_arc,
                    "p_insertion_arc")
            evidence = evidence_check(
                family=family, word=p_words[p_flat], compact=compact,
                source=source_p, target=target_p, port_count=p0 + 1,
                parent_mapping=base_mapping, invariants=invariants,
                caches=caches, used=used,
                context=[path_index, "p", p_flat])
            classification = evidence["classification"]
            counts[classification] += 1
            stages["A_plus_p"] += 1
            max_port_count = max(max_port_count, p0 + 1)
            triangles[(classification,
                       class_audit(source_p)["triangle_count"],
                       class_audit(target_p)["triangle_count"])] += 1
            update_relation_digest(relation_digest, {
                "path_index": path_index, "stage": "A_plus_p",
                "flat_index": p_flat, "source_arc": source_arc,
                "target_arc": target_arc,
                "source_child_graph_id": source_p.graph_id,
                "target_child_graph_id": target_p.graph_id,
                "classification": classification,
                "evidence_id": evidence["evidence_id"],
                "descriptor_pair_sha256": evidence["descriptor_pair_sha256"],
                "sign_proof_sha256": evidence["sign_proof_sha256"],
            })
            if classification not in ALLOWED:
                continue
            allowed.append(p_flat)
            source_q_arcs = admissible_internal_arcs(source_p)
            target_q_arcs = admissible_internal_arcs(target_p)
            q_shapes.append([len(source_q_arcs), len(target_q_arcs)])
            q_keys = tuple((s, t) for s in source_q_arcs
                           for t in target_q_arcs)
            for q_local, (source_q_arc, target_q_arc) in enumerate(q_keys):
                require(q_cursor < len(q_words), "truncated_q_words",
                        path_index=path_index)
                source_q, source_q_meta = insert_port(
                    source_p, source_q_arc, f"L_{p0 + 1}")
                target_q, target_q_meta = insert_port(
                    target_p, target_q_arc, f"L_{p0 + 1}")
                require(tuple(source_q_meta["subdivided_parent_arc"]) ==
                        source_q_arc and
                        tuple(target_q_meta["subdivided_parent_arc"]) ==
                        target_q_arc, "q_insertion_arc")
                q_evidence = evidence_check(
                    family=family, word=q_words[q_cursor], compact=compact,
                    source=source_q, target=target_q, port_count=p0 + 2,
                    parent_mapping=evidence["mapping"], invariants=invariants,
                    caches=caches, used=used,
                    context=[path_index, "q", p_flat, q_local])
                q_class = q_evidence["classification"]
                counts[q_class] += 1
                stages["A_plus_p_plus_q"] += 1
                max_port_count = max(max_port_count, p0 + 2)
                triangles[(q_class,
                           class_audit(source_q)["triangle_count"],
                           class_audit(target_q)["triangle_count"])] += 1
                update_relation_digest(relation_digest, {
                    "path_index": path_index,
                    "stage": "A_plus_p_plus_q",
                    "parent_p_flat_index": p_flat,
                    "local_flat_index": q_local,
                    "global_q_flat_index": q_cursor,
                    "source_arc": source_q_arc,
                    "target_arc": target_q_arc,
                    "source_child_graph_id": source_q.graph_id,
                    "target_child_graph_id": target_q.graph_id,
                    "classification": q_class,
                    "evidence_id": q_evidence["evidence_id"],
                    "descriptor_pair_sha256":
                        q_evidence["descriptor_pair_sha256"],
                    "sign_proof_sha256":
                        q_evidence["sign_proof_sha256"],
                })
                q_cursor += 1
        require(row["allowed_p_flat_indices"] == allowed,
                "allowed_p_flat_indices", path_index=path_index)
        require(row["q_shapes"] == q_shapes, "q_shape_blocks",
                path_index=path_index)
        require(q_cursor == len(q_words), "q_word_exhaustion",
                path_index=path_index)

    require(dict(sorted(counts.items())) == summary["counts"],
            "classification_counts", actual=dict(sorted(counts.items())),
            expected=summary["counts"])
    require(used["witnesses"] == set(compact["witnesses"]),
            "orphan_witnesses")
    require(used["transports"] == set(compact["transports"]),
            "orphan_transports")
    require(used["polynomials"] == set(compact["polynomials"]),
            "orphan_polynomials")
    return {
        "path_range": [start, stop],
        "counts": dict(sorted(counts.items())),
        "stage_counts": dict(sorted(stages.items())),
        "relations": sum(counts.values()),
        "relation_semantic_sha256": relation_digest.hexdigest(),
        "witnesses_replayed": len(used["witnesses"]),
        "transports_replayed": len(used["transports"]),
        "polynomials_replayed": len(used["polynomials"]),
        "unique_graphs_audited": len(caches["graph_audits"]),
        "descriptors_regenerated": len(caches["descriptors"]),
        "pullbacks_regenerated": len(caches["pullbacks"]),
        "strict_signs_regenerated": len(caches["sign_proofs"]),
        "maximum_probe_port_count": max_port_count,
        "triangle_cell_counts": [
            {"classification": key[0], "source_triangles": key[1],
             "target_triangles": key[2], "count": value}
            for key, value in sorted(triangles.items())
        ],
    }


def verify_family(family: Family):
    compacts = []
    for shard, expected_sha in enumerate(family.summary_sha256):
        path = CERT / family.summary_pattern.format(shard=shard)
        compact = load_compact(path, expected_sha)
        require(tuple(compact["summary"]["path_range"]) ==
                family.expected_ranges[shard], "locked_path_range",
                family=family.name, shard=shard)
        compacts.append(compact)

    first_summary = compacts[0]["summary"]
    base_paths = [resolve(path, compacts[0]["summary_path"])
                  for path in first_summary["base_summaries"]]
    inventory, commitment_rows, input_hashes = build_inventory(base_paths)
    require(len(inventory) == family.inventory_count, "family_inventory_count",
            family=family.name, actual=len(inventory))
    commitment = inventory_commitment(commitment_rows)
    for compact in compacts:
        summary = compact["summary"]
        require(int(summary["path_inventory_count"]) == family.inventory_count,
                "summary_inventory_count", family=family.name)
        require(summary["path_inventory_sha256"] == commitment,
                "inventory_commitment", family=family.name)
        require(summary["input_sha256"] == input_hashes,
                "inventory_input_commitments", family=family.name)
        require(summary["unresolved_classifications"] == [],
                "unresolved_classifications", family=family.name)

    # This independently checks deletion, duplication, and ordering at the
    # path-union level before any per-path semantic work.
    all_indices = [int(row["path_index"]) for compact in compacts
                   for row in compact["paths"]]
    require(all_indices == list(range(family.inventory_count)),
            "gapless_ordered_path_union", family=family.name)

    invariants = load_invariants()
    shards = []
    aggregate_counts = Counter()
    aggregate_stages = Counter()
    family_digest = hashlib.sha256()
    max_ports = 0
    for shard, compact in enumerate(compacts):
        result = audit_shard(family, compact, inventory, invariants)
        shards.append({
            "shard": shard,
            "summary": normalized(compact["summary_path"]),
            "summary_sha256": family.summary_sha256[shard],
            **result,
        })
        aggregate_counts.update(result["counts"])
        aggregate_stages.update(result["stage_counts"])
        max_ports = max(max_ports, result["maximum_probe_port_count"])
        family_digest.update(bytes.fromhex(result["relation_semantic_sha256"]))

    require(tuple(sorted(aggregate_counts.items())) == family.expected_counts,
            "family_classification_counts", family=family.name,
            actual=dict(sorted(aggregate_counts.items())))
    require(tuple(sorted(aggregate_stages.items())) ==
            family.expected_stage_counts, "family_stage_counts",
            family=family.name, actual=dict(sorted(aggregate_stages.items())))
    require(max_ports <= 10, "family_ten_port_bound", family=family.name,
            maximum=max_ports)
    return {
        "status": "VERIFIED",
        "family": family.name,
        "path_inventory_count": family.inventory_count,
        "path_inventory_sha256": commitment,
        "path_range": [0, family.inventory_count],
        "classification_counts": dict(sorted(aggregate_counts.items())),
        "stage_counts": dict(sorted(aggregate_stages.items())),
        "total_relations": sum(aggregate_counts.values()),
        "maximum_probe_port_count": max_ports,
        "ten_port_bound_verified": max_ports <= 10,
        "family_semantic_sha256": family_digest.hexdigest(),
        "shards": shards,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=("all", *FAMILIES), default="all")
    parser.add_argument("--output", type=Path,
                        default=HERE / "certificates" /
                        "compact_only_semantic_replay.json")
    args = parser.parse_args()
    names = tuple(FAMILIES) if args.family == "all" else (args.family,)
    results = [verify_family(FAMILIES[name]) for name in names]
    payload = {
        "schema": "compact-probe-clean-clone-semantic-gate-v1",
        "status": "VERIFIED",
        "scope": (
            "Compact-only exact semantic replay of the tracked n3 and "
            "theta2-n4 path-bound probe shards; no verbose probe-extension "
            "stream is consumed."),
        "families": results,
        "totals": {
            "paths": sum(row["path_inventory_count"] for row in results),
            "relations": sum(row["total_relations"] for row in results),
            "all_four_classes_exercised": any(
                len(row["classification_counts"]) == 4 for row in results),
            "maximum_probe_port_count": max(
                row["maximum_probe_port_count"] for row in results),
        },
        "implementation": {
            "semantic_gate": normalized(Path(__file__)),
            "n4_graph_fourier_engine": normalized(N4_ENGINE_DIR / "engine.py"),
            "n3_T_and_sign_engine": normalized(N3_ENGINE_DIR / "engine_n3.py"),
            "vendored_invariant_templates": normalized(
                HERE / "invariant_templates.py"),
            "imports_primary_code": False,
            "uses_verbose_probe_extension_streams": False,
            "descriptor_cache_used_for_semantics": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"], "families": names,
        "paths": payload["totals"]["paths"],
        "relations": payload["totals"]["relations"],
        "maximum_probe_port_count":
            payload["totals"]["maximum_probe_port_count"],
        "output": normalized(args.output),
        "output_sha256": file_sha256(args.output),
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FALSE", "error": str(exc)},
                         sort_keys=True), file=sys.stderr)
        raise
