#!/usr/bin/env python3
"""Rebuild the referee ZIP without importing the submitted archive builder."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


MANIFEST_RELATIVE = (
    "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
)
PREFIX = "k2p_principal_d_plus_submission_referee"
TIMESTAMP = (2026, 8, 27, 0, 0, 0)


def fail(message: str) -> None:
    raise SystemExit(f"INDEPENDENT_ARCHIVE_REBUILD_FAIL:{message}")


def strict_json(data: bytes, label: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                fail(f"duplicate JSON name:{label}:{key}")
            result[key] = value
        return result

    def reject_constant(token: str) -> None:
        fail(f"nonfinite JSON number:{label}:{token}")

    def finite_float(token: str) -> float:
        value = float(token)
        if not math.isfinite(value):
            reject_constant(token)
        return value

    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
            parse_float=finite_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        fail(f"JSON decode:{label}:{error}")


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        fail(f"unsafe relative path:{value!r}")
    return path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    manifest_path = project.joinpath(*PurePosixPath(MANIFEST_RELATIVE).parts)
    manifest = strict_json(manifest_path.read_bytes(), MANIFEST_RELATIVE)
    if not isinstance(manifest, dict):
        fail("manifest is not an object")
    frozen = manifest.get("frozen_evidence", {}).get("files")
    submission = manifest.get("submission_sources", {}).get("files")
    if not isinstance(frozen, dict) or not isinstance(submission, dict):
        fail("manifest ledgers are absent")
    overlap = set(frozen) & set(submission)
    if overlap:
        fail(f"ledger overlap:{sorted(overlap)[:3]}")
    relatives = sorted(set(frozen) | set(submission) | {MANIFEST_RELATIVE})
    if len(relatives) != 495:
        fail(f"unexpected file count:{len(relatives)}")
    if args.output.exists():
        fail(f"output already exists:{args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(
        args.output,
        "x",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
    ) as archive:
        for relative in relatives:
            safe = safe_relative(relative)
            path = project.joinpath(*safe.parts)
            if not path.is_file() or path.is_symlink():
                fail(f"missing or symbolic member:{relative}")
            data = path.read_bytes()
            declared = frozen.get(relative, submission.get(relative))
            if relative != MANIFEST_RELATIVE:
                if (
                    not isinstance(declared, dict)
                    or declared.get("bytes") != len(data)
                    or declared.get("sha256")
                    != hashlib.sha256(data).hexdigest()
                ):
                    fail(f"declared member binding mismatch:{relative}")
            info = zipfile.ZipInfo(f"{PREFIX}/{relative}", date_time=TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(
                info,
                data,
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )
    print(
        json.dumps(
            {
                "bytes": args.output.stat().st_size,
                "file_count": len(relatives),
                "output": str(args.output),
                "sha256": sha256(args.output),
                "status": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
