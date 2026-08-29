#!/usr/bin/env python3
"""Independently verify the retained R5 artifact index."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "FINAL_ARTIFACT_INDEX.json"
EXCLUDED_TOP = {"isolated", "execution", "tmp", "pdf_render"}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    answer: dict[str, Any] = {}
    for key, value in pairs:
        if key in answer:
            raise ValueError(f"duplicate JSON member: {key}")
        answer[key] = value
    return answer


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def main() -> None:
    index = json.loads(INDEX.read_bytes(), object_pairs_hook=unique_object)
    payload = index.pop("payload_sha256")
    if digest(encoded(index)) != payload:
        raise SystemExit("artifact-index payload mismatch")
    expected = index["files"]
    actual: dict[str, dict[str, object]] = {}
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if not relative.parts or relative.parts[0] in EXCLUDED_TOP:
            continue
        if path == INDEX or "__pycache__" in relative.parts or path.name == ".DS_Store":
            continue
        if path.is_symlink():
            raise SystemExit(f"symbolic review artifact forbidden: {relative}")
        if path.is_file():
            data = path.read_bytes()
            actual[relative.as_posix()] = {
                "bytes": len(data),
                "sha256": digest(data),
            }
    if actual != expected:
        raise SystemExit("artifact-index file inventory mismatch")
    if index["file_count"] != len(actual):
        raise SystemExit("artifact-index count mismatch")
    if index["total_bytes"] != sum(int(row["bytes"]) for row in actual.values()):
        raise SystemExit("artifact-index byte-count mismatch")
    if index["content_root_sha256"] != digest(encoded(actual)):
        raise SystemExit("artifact-index content-root mismatch")
    print(
        json.dumps(
            {
                "status": "PASS",
                "file_count": len(actual),
                "content_root_sha256": index["content_root_sha256"],
                "payload_sha256": payload,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
