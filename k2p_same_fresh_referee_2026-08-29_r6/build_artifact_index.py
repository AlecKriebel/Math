#!/usr/bin/env python3
"""Build a deterministic index of the review-owned, commit-sized artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXCLUDED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "execution",
    "isolated",
    "relocations",
    "runtime",
    "tmp",
}
EXCLUDED_FILES = {".DS_Store", "FINAL_ARTIFACT_INDEX.json"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output", type=Path, default=Path("FINAL_ARTIFACT_INDEX.json"))
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output

    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in EXCLUDED_DIRECTORIES for part in relative.parts):
            continue
        if not path.is_file() or path.is_symlink() or path.name in EXCLUDED_FILES:
            continue
        data = path.read_bytes()
        rows.append({"path": relative.as_posix(), "bytes": len(data), "sha256": sha256_bytes(data)})

    payload = {
        "files": rows,
        "file_count": len(rows),
        "total_bytes": sum(int(row["bytes"]) for row in rows),
    }
    document = {
        "schema": "k2p-r6-referee-artifact-index-v1",
        **payload,
        "payload_sha256": sha256_bytes(canonical_bytes(payload)),
    }
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "file_count": document["file_count"],
        "total_bytes": document["total_bytes"],
        "payload_sha256": document["payload_sha256"],
        "file_sha256": sha256_bytes(output.read_bytes()),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
