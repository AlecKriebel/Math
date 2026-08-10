#!/usr/bin/env python3
"""Verify and bind a gapless set of compact probe-extension shards.

This is deliberately more than a byte-level concatenation manifest.  It
reconstructs the frozen base-path inventory, decodes every packed relation
word, recomputes all aggregate counts, rejects orphan library records, and
requires one successful primary and one successful independent semantic
replay bound to every exact shard summary.
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

from compact_probe_extension_compiler import (
    CLASS_CODE,
    INDEX_MASK,
    collect_base_paths,
    inventory_commitment,
)


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
CODE_CLASS = {value: key for key, value in CLASS_CODE.items()}
SEPARATED = {"generic_polynomial_separation", "strict_open_cube_separation"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def normalized(path: Path) -> str:
    path = path.resolve()
    try:
        return str(path.relative_to(PROJECT.resolve()))
    except ValueError:
        return str(path)


def resolve(path: str | Path, summary_path: Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate.resolve()
    project_candidate = PROJECT / candidate
    if project_candidate.exists():
        return project_candidate.resolve()
    return (summary_path.resolve().parent / candidate).resolve()


def read_stream(path: Path, key: str):
    rows = {}
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            digest.update(raw)
            row = json.loads(raw)
            identifier = row[key]
            if identifier in rows:
                raise AssertionError((path, "duplicate stream key", identifier))
            rows[identifier] = row
    return rows, digest.hexdigest()


def decode_words(text: str, expected: int) -> tuple[int, ...]:
    raw = base64.b64decode(text, validate=True) if text else b""
    if len(raw) != 4 * expected:
        raise AssertionError(("packed word length", len(raw), expected))
    return tuple(struct.unpack(f"<{expected}I", raw)) if expected else ()


def audit_shard_streams(summary_path: Path, summary: dict) -> dict:
    keys = {
        "paths": "path_index",
        "witnesses": "witness_index",
        "transports": "transport_index",
        "polynomials": "polynomial_id",
    }
    streams = {}
    logical_hashes = {}
    for name, key in keys.items():
        metadata = summary["streams"][name]
        path = resolve(metadata["path"], summary_path)
        if sha256(path) != metadata["file_sha256"]:
            raise AssertionError((summary_path, name, "file digest"))
        rows, logical = read_stream(path, key)
        if logical != metadata["sha256"]:
            raise AssertionError((summary_path, name, "logical digest"))
        if len(rows) != int(metadata["records"]):
            raise AssertionError((summary_path, name, "record count"))
        streams[name] = rows
        logical_hashes[name] = logical

    witnesses = {int(key): row for key, row in streams["witnesses"].items()}
    transports = {int(key): row for key, row in streams["transports"].items()}
    if set(witnesses) != set(range(len(witnesses))):
        raise AssertionError((summary_path, "noncontiguous witness library"))
    if set(transports) != set(range(len(transports))):
        raise AssertionError((summary_path, "noncontiguous transport library"))

    polynomial_ids = set(streams["polynomials"])
    for identifier, row in streams["polynomials"].items():
        body = {key: row[key] for key in ("schema", "variable_count", "terms")}
        if stable_hash(body) != identifier:
            raise AssertionError((summary_path, "polynomial content address", identifier))
    referenced_polynomials = set()
    for index, row in witnesses.items():
        body = {
            key: row[key]
            for key in ("classification", "probe_classification", "probe_witness")
        }
        if stable_hash(body) != row["witness_id"]:
            raise AssertionError((summary_path, "witness content address", index))
        for key in ("source_pullback_id", "target_pullback_id"):
            if key in row["probe_witness"]:
                referenced_polynomials.add(row["probe_witness"][key])
    for index, row in transports.items():
        body = {
            key: row[key]
            for key in (
                "classification", "transport", "canonicalization",
                "fourier_coordinate_transport",
            )
        }
        if stable_hash(body) != row["transport_id"]:
            raise AssertionError((summary_path, "transport content address", index))

    start, stop = (int(value) for value in summary["path_range"])
    paths = {int(key): row for key, row in streams["paths"].items()}
    if set(paths) != set(range(start, stop)):
        raise AssertionError((summary_path, "stream range", start, stop))
    if int(summary["path_records"]) != stop - start:
        raise AssertionError((summary_path, "path record declaration"))

    counts = Counter()
    used_witnesses = set()
    used_transports = set()

    def consume(word: int, context) -> None:
        code = word >> 29
        index = word & INDEX_MASK
        if code not in CODE_CLASS:
            raise AssertionError((summary_path, context, "reserved class code", code))
        classification = CODE_CLASS[code]
        library = witnesses if classification in SEPARATED else transports
        if index not in library:
            raise AssertionError((summary_path, context, "missing library index", index))
        if library[index]["classification"] != classification:
            raise AssertionError((summary_path, context, "library class mismatch"))
        (used_witnesses if classification in SEPARATED else used_transports).add(index)
        counts[classification] += 1

    for index in range(start, stop):
        row = paths[index]
        body = {key: value for key, value in row.items() if key != "path_record_id"}
        if stable_hash(body) != row["path_record_id"]:
            raise AssertionError((summary_path, index, "path content address"))
        base_transport_index = int(row["base_transport_index"])
        if base_transport_index not in transports:
            raise AssertionError((summary_path, index, "missing base transport"))
        if transports[base_transport_index]["classification"] not in {
            "labelled_isomorphism", "ordinary_T",
        }:
            raise AssertionError((summary_path, index, "invalid base transport class"))
        used_transports.add(base_transport_index)
        p_count = int(row["p_word_count"])
        q_count = int(row["q_word_count"])
        p_words = decode_words(row["p_words_base64_le_u32"], p_count)
        q_words = decode_words(row["q_words_base64_le_u32"], q_count)
        allowed = [int(value) for value in row["allowed_p_flat_indices"]]
        if allowed != sorted(set(allowed)) or any(not 0 <= value < p_count for value in allowed):
            raise AssertionError((summary_path, index, "allowed p indices"))
        if len(allowed) != len(row["q_shapes"]):
            raise AssertionError((summary_path, index, "q shape count"))
        expected_q = sum(int(r) * int(c) for r, c in row["q_shapes"])
        if expected_q != q_count:
            raise AssertionError((summary_path, index, "q word declaration", expected_q, q_count))
        for offset, word in enumerate(p_words):
            consume(word, (index, "p", offset))
        for offset, word in enumerate(q_words):
            consume(word, (index, "q", offset))

    if used_witnesses != set(witnesses):
        raise AssertionError((summary_path, "orphan witness records"))
    if used_transports != set(transports):
        raise AssertionError((summary_path, "orphan transport records"))
    if referenced_polynomials != polynomial_ids:
        raise AssertionError((summary_path, "orphan or missing polynomial bodies"))
    if dict(sorted(counts.items())) != summary["counts"]:
        raise AssertionError((summary_path, "recomputed classification counts"))
    if summary.get("unresolved_classifications"):
        raise AssertionError((summary_path, "unresolved classifications"))
    return {
        "counts": dict(sorted(counts.items())),
        "stream_sha256": logical_hashes,
    }


def load_replays(paths: list[Path], *, independent: bool) -> dict[str, tuple[Path, dict]]:
    result = {}
    for path in paths:
        path = path.resolve()
        payload = json.loads(path.read_text())
        status = payload.get("status")
        accepted = {"VERIFIED"} if independent else {"EXACTLY_VERIFIED"}
        if status not in accepted:
            raise AssertionError((path, "replay status", status))
        summary_digest = payload.get("summary_sha256", payload.get("compact_summary_sha256"))
        if not summary_digest:
            raise AssertionError((path, "missing bound summary SHA-256"))
        if summary_digest in result:
            raise AssertionError((path, "duplicate replay for summary", summary_digest))
        result[summary_digest] = path, payload
    return result


def replay_counts(payload: dict) -> dict:
    if "counts" in payload:
        return payload["counts"]
    return payload.get("semantic_comparison", {}).get("classification_counts", {})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="append", type=Path, required=True)
    parser.add_argument("--primary-replay", action="append", type=Path, required=True)
    parser.add_argument("--independent-replay", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    loaded = []
    for path in args.summary:
        path = path.resolve()
        summary = json.loads(path.read_text())
        if summary["schema"] != "compact-path-bound-probe-extension-v1":
            raise AssertionError((path, "schema"))
        if summary["status"] != "EXACTLY_COMPUTED":
            raise AssertionError((path, "status", summary["status"]))
        loaded.append((path, summary))
    loaded.sort(key=lambda item: tuple(int(x) for x in item[1]["path_range"]))

    first_path, first = loaded[0]
    schema_path = resolve(first["schema_specification"], first_path)
    if sha256(schema_path) != first["schema_specification_sha256"]:
        raise AssertionError("schema specification SHA-256")
    bit_path = resolve(first["bit_cache"]["path"], first_path)
    if sha256(bit_path) != first["bit_cache"]["sha256"]:
        raise AssertionError("bit-cache SHA-256")
    base_summaries = [resolve(path, first_path) for path in first["base_summaries"]]
    inventory, commitment_rows, input_hashes = collect_base_paths(base_summaries)
    if len(inventory) != int(first["path_inventory_count"]):
        raise AssertionError("reconstructed path inventory count")
    if inventory_commitment(commitment_rows) != first["path_inventory_sha256"]:
        raise AssertionError("reconstructed path inventory commitment")
    if dict(sorted(input_hashes.items())) != first["input_sha256"]:
        raise AssertionError("reconstructed input commitment map")

    primary_replays = load_replays(args.primary_replay, independent=False)
    independent_replays = load_replays(args.independent_replay, independent=True)
    fixed_keys = (
        "base_summaries", "input_sha256", "bit_cache",
        "path_inventory_count", "path_inventory_sha256",
        "schema_specification", "schema_specification_sha256",
    )
    cursor = 0
    counts = Counter()
    shards = []
    for summary_path, summary in loaded:
        for key in fixed_keys:
            if summary[key] != first[key]:
                raise AssertionError((summary_path, "incompatible shard", key))
        start, stop = (int(x) for x in summary["path_range"])
        if start != cursor or stop < start:
            raise AssertionError((summary_path, "gap or overlap", cursor, start, stop))
        audited = audit_shard_streams(summary_path, summary)
        summary_digest = sha256(summary_path)
        if summary_digest not in primary_replays or summary_digest not in independent_replays:
            raise AssertionError((summary_path, "missing bound replay certificate"))
        primary_path, primary = primary_replays.pop(summary_digest)
        independent_path, independent = independent_replays.pop(summary_digest)
        for label, payload in (("primary", primary), ("independent", independent)):
            declared_range = payload.get("path_range")
            if declared_range is None and stop - start != 1:
                raise AssertionError((summary_path, label, "missing path range"))
            if declared_range is not None and [int(x) for x in declared_range] != [start, stop]:
                raise AssertionError((summary_path, label, "path range"))
            if replay_counts(payload) != audited["counts"]:
                raise AssertionError((summary_path, label, "classification counts"))
        counts.update(audited["counts"])
        shards.append({
            "summary": normalized(summary_path),
            "summary_sha256": summary_digest,
            "path_range": [start, stop],
            "counts": audited["counts"],
            "streams": summary["streams"],
            "primary_replay": normalized(primary_path),
            "primary_replay_sha256": sha256(primary_path),
            "independent_replay": normalized(independent_path),
            "independent_replay_sha256": sha256(independent_path),
        })
        cursor = stop

    if primary_replays or independent_replays:
        raise AssertionError(("orphan replay certificates", sorted(primary_replays), sorted(independent_replays)))
    if cursor != len(inventory):
        raise AssertionError(("incomplete inventory", cursor, len(inventory)))
    payload = {
        "schema": "compact-path-bound-probe-shard-manifest-v2",
        "status": "EXACTLY_VERIFIED",
        **{key: first[key] for key in fixed_keys},
        "path_range": [0, cursor],
        "counts": dict(sorted(counts.items())),
        "shards": shards,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "path_inventory_count": cursor,
        "shards": len(shards),
        "counts": payload["counts"],
        "output": normalized(args.output),
        "sha256": sha256(args.output),
    }, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
