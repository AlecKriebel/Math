#!/usr/bin/env python3
"""Exact semantic replay of a compact path-bound probe shard.

This is the primary replay.  It reconstructs every child graph and relation
cell; the release additionally requires a clean-room implementation that does
not import any module under ``primary``.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import struct

from atlas_compiler import load_bit_cache, stable_hash
from compact_probe_extension_compiler import (
    CLASS_CODE,
    INDEX_MASK,
    collect_base_paths,
    graph_id,
    inventory_commitment,
    normalized_path,
    resolve,
    sha256,
)
from graph_model import canonical_mixed, sd0
from hard_cover_compiler import (
    exact_poly_hash,
    full_deck,
    load_invariants,
    relation_witness,
)
from probe_extension_compiler import (
    ALLOWED_CHILD,
    SEPARATED,
    admissible_internal_arcs,
    insert_port,
    quotient_transport,
    restricts_to,
    transport_metadata,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
CODE_CLASS = {value: key for key, value in CLASS_CODE.items()}


def stable_bytes(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()


def load_stream(path: Path, key: str):
    rows = {}
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            digest.update(raw)
            row = json.loads(raw)
            identifier = row[key]
            if identifier in rows:
                raise AssertionError((path, "duplicate", identifier))
            rows[identifier] = row
    return rows, digest.hexdigest()


def decode_words(text: str, expected: int) -> list[int]:
    raw = base64.b64decode(text, validate=True) if text else b""
    if len(raw) != 4 * expected:
        raise AssertionError(("packed word length", len(raw), expected))
    if not raw:
        return []
    return list(struct.unpack(f"<{expected}I", raw))


def polynomial_from_row(row: dict):
    return {
        tuple(int(value) for value in exponent): int(coefficient)
        for exponent, coefficient in row["terms"]
    }


def exact_record_id(row: dict, key: str) -> str:
    return stable_hash({name: value for name, value in row.items() if name != key})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary_path = args.summary.resolve()
    summary = json.loads(summary_path.read_text())
    if summary["schema"] != "compact-path-bound-probe-extension-v1":
        raise AssertionError("unexpected compact probe schema")
    if summary["status"] != "EXACTLY_COMPUTED":
        raise AssertionError(("producer status", summary["status"]))
    schema_path = resolve(
        summary["schema_specification"], relative_to=summary_path
    )
    if sha256(schema_path) != summary["schema_specification_sha256"]:
        raise AssertionError("compact schema specification SHA-256")

    for name, expected in summary["input_sha256"].items():
        path = resolve(name, relative_to=summary_path)
        if sha256(path) != expected:
            raise AssertionError((name, "input SHA-256"))
    bit_path = resolve(summary["bit_cache"]["path"], relative_to=summary_path)
    if sha256(bit_path) != summary["bit_cache"]["sha256"]:
        raise AssertionError("bit-cache SHA-256")

    base_paths = [
        resolve(path, relative_to=summary_path) for path in summary["base_summaries"]
    ]
    inventory, commitment_rows, input_hashes = collect_base_paths(base_paths)
    if len(inventory) != int(summary["path_inventory_count"]):
        raise AssertionError("path inventory count")
    if inventory_commitment(commitment_rows) != summary["path_inventory_sha256"]:
        raise AssertionError("path inventory commitment")
    if dict(sorted(input_hashes.items())) != summary["input_sha256"]:
        raise AssertionError("reconstructed input commitment map")

    keys = {
        "paths": "path_index",
        "witnesses": "witness_index",
        "transports": "transport_index",
        "polynomials": "polynomial_id",
    }
    streams = {}
    stream_digests = {}
    for name, key in keys.items():
        metadata = summary["streams"][name]
        path = resolve(metadata["path"], relative_to=summary_path)
        if sha256(path) != metadata["file_sha256"]:
            raise AssertionError((name, "file SHA-256"))
        rows, digest = load_stream(path, key)
        if len(rows) != int(metadata["records"]):
            raise AssertionError((name, "record count"))
        if digest != metadata["sha256"]:
            raise AssertionError((name, "logical stream SHA-256"))
        streams[name] = rows
        stream_digests[name] = digest

    witnesses = streams["witnesses"]
    transports = streams["transports"]
    polynomials = streams["polynomials"]
    if set(witnesses) != set(range(len(witnesses))):
        raise AssertionError("noncontiguous witness indices")
    if set(transports) != set(range(len(transports))):
        raise AssertionError("noncontiguous transport indices")
    for index, row in witnesses.items():
        payload = {
            key: row[key]
            for key in ("classification", "probe_classification", "probe_witness")
        }
        if stable_hash(payload) != row["witness_id"]:
            raise AssertionError((index, "witness content address"))
    for index, row in transports.items():
        payload = {
            key: row[key]
            for key in (
                "classification", "transport", "canonicalization",
                "fourier_coordinate_transport",
            )
        }
        if stable_hash(payload) != row["transport_id"]:
            raise AssertionError((index, "transport content address"))
    polynomial_bodies = {}
    for identifier, row in polynomials.items():
        payload = {
            key: row[key] for key in ("schema", "variable_count", "terms")
        }
        if stable_hash(payload) != identifier:
            raise AssertionError((identifier, "polynomial content address"))
        polynomial_bodies[identifier] = polynomial_from_row(row)

    invariants = load_invariants()
    bit_cache = load_bit_cache(bit_path)
    sign_cache = {}
    counts = Counter()
    used_witnesses = set()
    used_transports = set()

    def expected_polynomial(poly) -> str:
        terms = tuple(
            (tuple(int(value) for value in exponent), int(coefficient))
            for exponent, coefficient in sorted(poly.items())
        )
        payload = {
            "schema": 1,
            "variable_count": len(terms[0][0]) if terms else 0,
            "terms": terms,
        }
        identifier = stable_hash(payload)
        if identifier not in polynomial_bodies:
            raise AssertionError((identifier, "missing polynomial body"))
        if polynomial_bodies[identifier] != poly:
            raise AssertionError((identifier, "polynomial body mismatch"))
        return identifier

    def classify(source, target, p, parent_transport, deck_cache):
        source_id, target_id = graph_id(source), graph_id(target)
        source_key, target_key = (source_id, p), (target_id, p)
        if source_key not in deck_cache:
            deck_cache[source_key] = full_deck(source, p)
        if target_key not in deck_cache:
            deck_cache[target_key] = full_deck(target, p)
        probe, witness = relation_witness(
            deck_cache[source_key], deck_cache[target_key], invariants,
            bit_cache, sign_cache, register_polynomial=expected_polynomial,
            exact_sign=True,
        )
        relation = {"probe_classification": probe, "probe_witness": witness}
        if probe in SEPARATED:
            relation["classification"] = probe
            return relation
        if probe != "equal_invariant_signature":
            relation["classification"] = probe
            return relation
        source_code = canonical_mixed(sd0(source))[0]
        target_code = canonical_mixed(sd0(target))[0]
        try:
            _code, child_transport, canonical = quotient_transport(source, target)
        except ValueError:
            relation["classification"] = "unresolved_equal_non_T"
            return relation
        if not restricts_to(child_transport, parent_transport):
            relation["classification"] = "incoherent_isomorphism_or_T"
            return relation
        relation["classification"] = (
            "labelled_isomorphism" if source_code == target_code else "ordinary_T"
        )
        relation["transport"] = transport_metadata(source, target, child_transport)
        relation["canonicalization"] = canonical
        return relation

    def verify_word(word, relation, context):
        code = word >> 29
        index = word & INDEX_MASK
        if code not in CODE_CLASS:
            raise AssertionError((context, "reserved class code", code))
        classification = CODE_CLASS[code]
        if classification != relation["classification"]:
            raise AssertionError((context, "classification", classification, relation["classification"]))
        if classification in SEPARATED:
            if index not in witnesses:
                raise AssertionError((context, "missing witness", index))
            expected = {
                "classification": relation["classification"],
                "probe_classification": relation["probe_classification"],
                "probe_witness": relation["probe_witness"],
            }
            actual = {
                key: witnesses[index][key]
                for key in ("classification", "probe_classification", "probe_witness")
            }
            if actual != json.loads(json.dumps(expected)):
                raise AssertionError((context, "witness body"))
            used_witnesses.add(index)
        else:
            if index not in transports:
                raise AssertionError((context, "missing transport", index))
            expected = {
                "classification": relation["classification"],
                "transport": relation["transport"],
                "canonicalization": relation["canonicalization"],
                "fourier_coordinate_transport": "identity_on_fixed_port_labels",
            }
            actual = {
                key: transports[index][key]
                for key in (
                    "classification", "transport", "canonicalization",
                    "fourier_coordinate_transport",
                )
            }
            if actual != json.loads(json.dumps(expected)):
                raise AssertionError((context, "transport body"))
            used_transports.add(index)
        counts[classification] += 1

    start, stop = (int(value) for value in summary["path_range"])
    paths = streams["paths"]
    if set(paths) != set(range(start, stop)):
        raise AssertionError(("path shard range", start, stop, sorted(paths)[:3]))
    if len(paths) != int(summary["path_records"]):
        raise AssertionError("path record count")

    for offset, path_index in enumerate(range(start, stop), 1):
        row = paths[path_index]
        if exact_record_id(row, "path_record_id") != row["path_record_id"]:
            raise AssertionError((path_index, "path content address"))
        entry = inventory[path_index]
        for key in (
            "base_summary", "base_run_index", "base_state_id",
            "base_path_binding_id", "fixed_full_root_case_id",
            "selected_port_count", "source_parent_graph_id",
            "target_parent_graph_id", "source_parent_normalized_graph_id",
            "target_parent_normalized_graph_id", "base_dummy_order",
            "base_restored_role_to_label",
        ):
            if row[key] != entry[key]:
                raise AssertionError((path_index, "base binding", key))

        source_parent, target_parent = entry["source"], entry["target"]
        _code, base_transport, base_canonical = quotient_transport(
            source_parent, target_parent
        )
        base_class = (
            "labelled_isomorphism"
            if canonical_mixed(sd0(source_parent))[0]
            == canonical_mixed(sd0(target_parent))[0]
            else "ordinary_T"
        )
        base_expected = {
            "classification": base_class,
            "transport": transport_metadata(source_parent, target_parent, base_transport),
            "canonicalization": base_canonical,
            "fourier_coordinate_transport": "identity_on_fixed_port_labels",
        }
        base_index = int(row["base_transport_index"])
        if base_index not in transports:
            raise AssertionError((path_index, "missing base transport"))
        if {
            key: transports[base_index][key] for key in base_expected
        } != json.loads(json.dumps(base_expected)):
            raise AssertionError((path_index, "base transport"))
        used_transports.add(base_index)

        source_p_arcs = admissible_internal_arcs(source_parent)
        target_p_arcs = admissible_internal_arcs(target_parent)
        if row["source_p_arcs"] != json.loads(json.dumps(source_p_arcs)):
            raise AssertionError((path_index, "source p arcs"))
        if row["target_p_arcs"] != json.loads(json.dumps(target_p_arcs)):
            raise AssertionError((path_index, "target p arcs"))
        p_count = len(source_p_arcs) * len(target_p_arcs)
        if int(row["p_word_count"]) != p_count:
            raise AssertionError((path_index, "p count"))
        p_words = decode_words(row["p_words_base64_le_u32"], p_count)
        q_words = decode_words(
            row["q_words_base64_le_u32"], int(row["q_word_count"])
        )
        allowed_indices = []
        expected_q_shapes = []
        q_cursor = 0
        deck_cache = {}
        p0 = int(entry["selected_port_count"])
        p_label, q_label = f"L_{p0}", f"L_{p0 + 1}"
        p_flat = 0
        for source_arc in source_p_arcs:
            source_p, source_delete = insert_port(source_parent, source_arc, p_label)
            if graph_id(source_p) == graph_id(source_parent):
                raise AssertionError((path_index, "source insertion did not change graph"))
            for target_arc in target_p_arcs:
                target_p, target_delete = insert_port(target_parent, target_arc, p_label)
                relation_p = classify(
                    source_p, target_p, p0 + 1, base_transport, deck_cache
                )
                verify_word(p_words[p_flat], relation_p, (path_index, "p", p_flat))
                if relation_p["classification"] in ALLOWED_CHILD:
                    allowed_indices.append(p_flat)
                    child_transport = tuple(
                        tuple(pair)
                        for pair in relation_p["transport"]["vertex_transport"]
                    )
                    source_q_arcs = admissible_internal_arcs(source_p)
                    target_q_arcs = admissible_internal_arcs(target_p)
                    expected_q_shapes.append((len(source_q_arcs), len(target_q_arcs)))
                    for source_q_arc in source_q_arcs:
                        source_q, _source_q_delete = insert_port(
                            source_p, source_q_arc, q_label
                        )
                        for target_q_arc in target_q_arcs:
                            target_q, _target_q_delete = insert_port(
                                target_p, target_q_arc, q_label
                            )
                            if q_cursor >= len(q_words):
                                raise AssertionError((path_index, "truncated q block"))
                            relation_q = classify(
                                source_q, target_q, p0 + 2,
                                child_transport, deck_cache,
                            )
                            verify_word(
                                q_words[q_cursor], relation_q,
                                (path_index, "q", p_flat, q_cursor),
                            )
                            q_cursor += 1
                p_flat += 1
        if row["allowed_p_flat_indices"] != allowed_indices:
            raise AssertionError((path_index, "allowed p index list"))
        if row["q_shapes"] != json.loads(json.dumps(expected_q_shapes)):
            raise AssertionError((path_index, "q shapes"))
        if q_cursor != len(q_words):
            raise AssertionError((path_index, "trailing q words", q_cursor, len(q_words)))
        if offset % 10 == 0:
            print(json.dumps({
                "compact_probe_replay_progress": {
                    "completed_paths": offset,
                    "shard_paths": stop - start,
                    "global_path_index": path_index,
                    "counts": dict(sorted(counts.items())),
                }
            }, sort_keys=True), flush=True)

    if dict(sorted(counts.items())) != summary["counts"]:
        raise AssertionError(("classification counts", counts, summary["counts"]))
    if used_witnesses != set(witnesses):
        raise AssertionError(("orphan witnesses", sorted(set(witnesses) - used_witnesses)[:5]))
    if used_transports != set(transports):
        raise AssertionError(("orphan transports", sorted(set(transports) - used_transports)[:5]))

    result = {
        "schema": "compact-path-bound-probe-primary-replay-v1",
        "status": "EXACTLY_VERIFIED",
        "summary": normalized_path(summary_path),
        "summary_sha256": sha256(summary_path),
        "path_inventory_count": len(inventory),
        "path_range": [start, stop],
        "counts": dict(sorted(counts.items())),
        "stream_sha256": stream_digests,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
