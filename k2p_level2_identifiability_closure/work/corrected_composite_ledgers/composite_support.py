#!/usr/bin/env python3
"""Small deterministic helpers for the corrected primitive composites.

This module contains serialization and hashing only.  It deliberately does
not contain classification logic so the producer and independent verifier can
implement that logic separately.
"""

from __future__ import annotations

import dataclasses
import gzip
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ARTIFACTS = HERE / "artifacts"
PACKAGE = PROJECT / "package/referee/k2p_offline_sweep_portable"

SERIALIZATION = {
    "format": "gzip-jsonl-canonical-v1",
    "gzip_mtime": 0,
    "json_key_order": "lexicographic",
    "json_separators": [",", ":"],
    "line_ending": "LF",
    "final_newline": True,
    "row_order": "raw_id_ascending",
}


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
        canonical_data(value), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(canonical_data(value), indent=2, sort_keys=True) + "\n").encode()


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with temporary.open("wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(path, pretty_bytes(value))


def with_payload_hash(value: dict[str, Any]) -> dict[str, Any]:
    result = dict(value)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = sha_object(result)
    return result


class StreamRoots:
    """Streaming SHA roots with a fully specified concatenation convention."""

    def __init__(self) -> None:
        self.row_root = hashlib.sha256()
        self.raw_id_root = hashlib.sha256()
        self.plain = hashlib.sha256()
        self.plain_bytes = 0
        self.rows = 0

    def update(self, raw_id: int, row_payload: bytes) -> None:
        row_digest = hashlib.sha256(row_payload).digest()
        self.row_root.update(row_digest)
        self.raw_id_root.update(hashlib.sha256(canonical_bytes(raw_id)).digest())
        line = row_payload + b"\n"
        self.plain.update(line)
        self.plain_bytes += len(line)
        self.rows += 1

    def record(self) -> dict[str, Any]:
        return {
            "ordered_row_hash_root": self.row_root.hexdigest(),
            "ordered_raw_id_hash_root": self.raw_id_root.hexdigest(),
            "uncompressed_stream_sha256": self.plain.hexdigest(),
            "uncompressed_bytes": self.plain_bytes,
            "row_hash_root_algorithm": "sha256(concat(binary_sha256(canonical_row_json)))",
            "raw_id_hash_root_algorithm": "sha256(concat(binary_sha256(canonical_raw_id_json)))",
        }


def deterministic_jsonl_gzip(path: Path, rows: Iterable[dict[str, Any]]) -> StreamRoots:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    roots = StreamRoots()
    with temporary.open("wb") as raw:
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=6
        ) as encoded:
            for row in rows:
                payload = canonical_bytes(row)
                roots.update(int(row["raw_id"]), payload)
                encoded.write(payload)
                encoded.write(b"\n")
        raw.flush()
        os.fsync(raw.fileno())
    os.replace(temporary, path)
    return roots


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected gzip JSON object: {path}")
    return value
