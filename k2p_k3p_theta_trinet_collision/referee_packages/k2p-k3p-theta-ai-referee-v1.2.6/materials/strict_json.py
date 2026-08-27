#!/usr/bin/env python3
"""Fail-closed JSON loading and canonical certificate-shape checks.

The mathematical verifiers treat certificate values as inputs.  This module
ensures that every raw certificate has a unique parse, contains only standard
JSON constants, and has the exact closed key/container structure audited for
its filename.  Shape hashes depend on object keys, container nesting, array
lengths, and primitive JSON types, but not on mathematical values.
"""
from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable


CANONICAL_SHAPE_SHA256 = {
    # Filled from the canonical v1.2.6 certificate schemas.  These are schema
    # fingerprints, not file-content hashes.
    "certificate_k2p_simple.json":
        "90be49d85ccd80bf4a471d450650f660fba2e495e671728097f2f2d15a7befb4",
    "certificate_k2p_continuous_time.json":
        "370f069ccb43d3acc88ba826f65736d635c5bf0481b0cb0578bd86badcd1485a",
    "certificate_k3p.json":
        "48ce9ef53ae2b72dab024744335ee31a6834bcf509fdf0f80b3347b8bc51af5d",
    "jacobian_certificate_k3p.json":
        "51f159ef706f78f03b7f5aea199a4fd6be24b714c6a3b5deebd64b28ffc07df0",
    "continuous_time_certificate_k3p.json":
        "b93daf3e1559f90ca1e431a5341494466fe0cc5faa93a4a02e3e81bb6a8160c4",
}


def _unique_object(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_constant(token: str) -> None:
    raise ValueError(f"non-standard JSON numeric constant {token!r}")


def _shape(value: Any) -> Any:
    if isinstance(value, dict):
        return ["object", [[key, _shape(value[key])] for key in sorted(value)]]
    if isinstance(value, list):
        # Retain the exact multiset of element shapes. Sorting the encoded
        # shapes makes the fingerprint independent of row order, while the
        # multiplicities prevent same-length substitutions between existing
        # row types. Semantic row order is checked separately where it matters.
        encoded = Counter(
            json.dumps(_shape(item), ensure_ascii=True, separators=(",", ":"))
            for item in value
        )
        return [
            "array",
            len(value),
            [[json.loads(item), encoded[item]] for item in sorted(encoded)],
        ]
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    raise TypeError(f"unsupported parsed JSON value type {type(value).__name__}")


def shape_sha256(value: Any) -> str:
    encoded = json.dumps(
        _shape(value), ensure_ascii=True, separators=(",", ":"), sort_keys=False
    ).encode("ascii")
    return sha256(encoded).hexdigest()


def load_json_strict(path: str | Path, *, expected_shape: str | None = None) -> Any:
    source = Path(path)
    try:
        value = json.loads(
            source.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"strict JSON parse failed for {source.name}: {exc}") from exc
    if expected_shape is not None:
        actual = shape_sha256(value)
        if actual != expected_shape:
            raise ValueError(
                f"closed JSON schema mismatch for {source.name}: "
                f"shape SHA-256 {actual}, expected {expected_shape}"
            )
    return value


def load_canonical_certificate(path: str | Path) -> Any:
    source = Path(path)
    try:
        expected = CANONICAL_SHAPE_SHA256[source.name]
    except KeyError as exc:
        raise ValueError(f"no closed JSON schema registered for {source.name}") from exc
    return load_json_strict(source, expected_shape=expected)
