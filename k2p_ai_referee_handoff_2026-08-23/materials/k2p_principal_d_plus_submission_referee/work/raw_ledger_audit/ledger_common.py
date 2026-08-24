#!/usr/bin/env python3
"""Shared exact utilities for the independent four-port raw ledger audit."""

from __future__ import annotations

import dataclasses
import gzip
import hashlib
import importlib.util
import inspect
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterable


AUDIT_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = AUDIT_ROOT.parents[1]
DEFAULT_PACKAGE_ROOT = (
    PROJECT_ROOT / "package/referee/k2p_offline_sweep_portable"
)


def fail(code: str, detail: object | None = None) -> "None":
    raise SystemExit(code if detail is None else f"{code}: {detail}")


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
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        canonical_data(value), sort_keys=True, separators=(",", ":")
    ).encode()


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_pretty_bytes(value: Any) -> bytes:
    return (json.dumps(canonical_data(value), indent=2, sort_keys=True) + "\n").encode()


def atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with temporary.open("wb") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(path, canonical_pretty_bytes(value))


def deterministic_gzip(path: Path, chunks: Iterable[bytes]) -> tuple[str, int]:
    """Write gzip with fixed metadata; return SHA-256 and uncompressed bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    plain_digest = hashlib.sha256()
    plain_bytes = 0
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as encoded:
            for chunk in chunks:
                plain_digest.update(chunk)
                plain_bytes += len(chunk)
                encoded.write(chunk)
        raw.flush()
        os.fsync(raw.fileno())
    os.replace(temporary, path)
    return plain_digest.hexdigest(), plain_bytes


def load_atlas(package_root: Path):
    module_path = package_root / "atlas/k2p_atlas_core.py"
    module_name = "k2p_raw_ledger_atlas_core"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        fail("RAW_LEDGER_ATLAS_IMPORT_FAIL", module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def canonicalizer_sha256(atlas) -> str:
    source = "\n".join(
        inspect.getsource(getattr(atlas, name))
        for name in (
            "mixed_incidence_graph",
            "mixed_exact_isomorphic",
            "mixed_relation_exact",
            "_mixed_triangle_edges",
            "prepare_mixed_source",
            "mixed_relation_exact_prepared",
        )
    )
    return hashlib.sha256(source.encode()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail("RAW_LEDGER_JSON_FAIL", f"{path}: {exc}")
    if not isinstance(value, dict):
        fail("RAW_LEDGER_JSON_OBJECT_FAIL", path)
    return value

