#!/usr/bin/env python3
"""Independent canonical/duplicate scan of every compressed JSON release file."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
from typing import Any


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise AuditFailure(code if detail is None else f"{code}:{detail}")


def unique_object(label: str):
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for name, value in pairs:
            require(name not in result, "DUPLICATE_NAME", f"{label}:{name!r}")
            result[name] = value
        return result

    return hook


def reject_constant(label: str):
    def reject(token: str) -> None:
        raise AuditFailure(f"NONFINITE_CONSTANT:{label}:{token[:96]}")

    return reject


def finite_float(label: str):
    def parse(token: str) -> float:
        value = float(token)
        require(math.isfinite(value), "NONFINITE_FLOAT", f"{label}:{token[:96]}")
        return value

    return parse


def decode(data: bytes, label: str) -> Any:
    try:
        text = data.decode("utf-8")
        return json.loads(
            text,
            object_pairs_hook=unique_object(label),
            parse_constant=reject_constant(label),
            parse_float=finite_float(label),
        )
    except UnicodeDecodeError as error:
        raise AuditFailure(f"UTF8:{label}:{error.start}") from error
    except json.JSONDecodeError as error:
        raise AuditFailure(f"SYNTAX:{label}:{error.lineno}:{error.colno}") from error


def canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as error:
        raise AuditFailure(f"CANONICAL_ENCODING:{error}") from error


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def scan_document(path: Path, relative: str) -> dict[str, Any]:
    with gzip.open(path, "rb") as handle:
        plain = handle.read()
    value = decode(plain, relative)
    require(isinstance(value, dict), "DOCUMENT_NOT_OBJECT", relative)
    require(plain == canonical(value) + b"\n", "NONCANONICAL_DOCUMENT", relative)
    return {"rows": 1, "plain_bytes": len(plain), "plain_sha256": hashlib.sha256(plain).hexdigest()}


def scan_lines(path: Path, relative: str) -> dict[str, Any]:
    rows = 0
    plain_bytes = 0
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for number, line in enumerate(handle, 1):
            require(line.endswith(b"\n"), "MISSING_NEWLINE", f"{relative}:{number}")
            require(line != b"\n", "BLANK_LINE", f"{relative}:{number}")
            value = decode(line, f"{relative}:{number}")
            require(isinstance(value, dict), "ROW_NOT_OBJECT", f"{relative}:{number}")
            require(line == canonical(value) + b"\n", "NONCANONICAL_ROW", f"{relative}:{number}")
            rows += 1
            plain_bytes += len(line)
            digest.update(line)
    return {"rows": rows, "plain_bytes": plain_bytes, "plain_sha256": digest.hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    require(project.is_dir(), "PROJECT_MISSING", project)
    paths = sorted(
        path
        for path in project.rglob("*")
        if path.is_file() and (path.name.endswith(".json.gz") or path.name.endswith(".jsonl.gz"))
    )
    require(paths, "NO_COMPRESSED_JSON")
    files: dict[str, dict[str, Any]] = {}
    suffix_counts = {"json.gz": 0, "jsonl.gz": 0}
    total_rows = 0
    total_plain_bytes = 0
    for path in paths:
        relative = path.relative_to(project).as_posix()
        if path.name.endswith(".jsonl.gz"):
            row = scan_lines(path, relative)
            suffix_counts["jsonl.gz"] += 1
        else:
            row = scan_document(path, relative)
            suffix_counts["json.gz"] += 1
        row.update({"compressed_bytes": path.stat().st_size, "compressed_sha256": sha_file(path)})
        files[relative] = row
        total_rows += int(row["rows"])
        total_plain_bytes += int(row["plain_bytes"])
    result = {
        "schema": "r5-independent-compressed-json-audit-v1",
        "status": "PASS",
        "file_count": len(files),
        "suffix_counts": suffix_counts,
        "total_rows_or_documents": total_rows,
        "total_decompressed_bytes": total_plain_bytes,
        "duplicate_names": 0,
        "noncanonical_payloads": 0,
        "files": files,
    }
    result["payload_sha256"] = hashlib.sha256(canonical(result)).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "file_count": result["file_count"],
                "rows": total_rows,
                "payload_sha256": result["payload_sha256"],
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except (AuditFailure, OSError, EOFError) as error:
        raise SystemExit(f"R5_COMPRESSED_JSON_AUDIT_FAIL:{error}")
