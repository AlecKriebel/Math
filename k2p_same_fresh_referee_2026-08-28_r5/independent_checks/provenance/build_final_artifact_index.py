#!/usr/bin/env python3
"""Build a deterministic index of retained review-owned R5 artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "FINAL_ARTIFACT_INDEX.json"
EXCLUDED_TOP = {"isolated", "execution", "tmp", "pdf_render"}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()


def main() -> None:
    files: dict[str, dict[str, object]] = {}
    for path in sorted(ROOT.rglob("*")):
        relative = path.relative_to(ROOT)
        if not relative.parts or relative.parts[0] in EXCLUDED_TOP:
            continue
        if path == OUTPUT or "__pycache__" in relative.parts or path.name == ".DS_Store":
            continue
        if path.is_symlink():
            raise SystemExit(f"symbolic review artifact forbidden: {relative}")
        if not path.is_file():
            continue
        data = path.read_bytes()
        files[relative.as_posix()] = {"bytes": len(data), "sha256": sha256(data)}
    result = {
        "schema": "k2p-r5-review-artifact-index-v1",
        "scope": (
            "retained review-owned files; excludes isolated/execution/tmp/"
            "pdf_render and this index"
        ),
        "file_count": len(files),
        "total_bytes": sum(int(row["bytes"]) for row in files.values()),
        "content_root_sha256": sha256(canonical(files)),
        "files": files,
    }
    result["payload_sha256"] = sha256(canonical(result))
    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "file_count",
                    "total_bytes",
                    "content_root_sha256",
                    "payload_sha256",
                )
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
