#!/usr/bin/env python3
"""Verify the outer referee package and the canonical proof-core manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


class IntegrityFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise IntegrityFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_relative(value: str) -> str:
    path = PurePosixPath(value)
    require(value and not path.is_absolute() and ".." not in path.parts,
            ("unsafe package path", value))
    normalized = path.as_posix()
    require(normalized == value and value not in {".", ""},
            ("noncanonical package path", value))
    return value


def is_runtime_file(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return (
        relative in {"PACKAGE_MANIFEST.json", "SHA256SUMS"}
        or ".venv" in parts
        or "review_runs" in parts
        or "__pycache__" in parts
        or relative.endswith(".pyc")
        or relative.endswith("/.DS_Store")
        or relative == ".DS_Store"
    )


def observed_payload(root: Path) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if is_runtime_file(relative):
            continue
        result[relative] = {
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
    return result


def verify_outer(root: Path) -> dict[str, object]:
    manifest_path = root / "PACKAGE_MANIFEST.json"
    sums_path = root / "SHA256SUMS"
    require(manifest_path.is_file() and sums_path.is_file(),
            "missing outer package manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    required = {
        "schema", "package_name", "package_builder_commit",
        "proof_source_commit", "canonical_archive_sha256",
        "payload_file_count", "payload_bytes", "payload",
    }
    require(set(manifest) == required and
            manifest.get("schema") == "k3p-independent-referee-package-v1",
            "outer package manifest schema")
    rows = manifest.get("payload")
    require(isinstance(rows, list), "outer package payload rows")
    expected: dict[str, dict[str, object]] = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == {"path", "bytes", "sha256"},
                ("outer payload row", row))
        relative = safe_relative(row["path"])
        require(relative not in expected and isinstance(row["bytes"], int) and
                row["bytes"] >= 0 and isinstance(row["sha256"], str) and
                len(row["sha256"]) == 64,
                ("outer payload row fields", relative))
        expected[relative] = {"bytes": row["bytes"], "sha256": row["sha256"]}
    observed = observed_payload(root)
    require(observed == expected,
            ("outer package payload mismatch",
             sorted(set(expected) - set(observed)),
             sorted(set(observed) - set(expected))))
    require(manifest["payload_file_count"] == len(expected) and
            manifest["payload_bytes"] == sum(row["bytes"] for row in expected.values()),
            "outer payload totals")

    sums: dict[str, str] = {}
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        digest, separator, relative = line.partition("  ")
        require(separator == "  " and len(digest) == 64,
                ("malformed SHA256SUMS line", line))
        safe_relative(relative)
        require(relative not in sums, ("duplicate SHA256SUMS path", relative))
        sums[relative] = digest
    expected_sum_paths = set(expected) | {"PACKAGE_MANIFEST.json"}
    require(set(sums) == expected_sum_paths, "SHA256SUMS path set")
    for relative, digest in sums.items():
        require(sha256_file(root / relative) == digest,
                ("SHA256SUMS mismatch", relative))
    return {
        "payload_file_count": len(expected),
        "payload_bytes": manifest["payload_bytes"],
        "package_builder_commit": manifest["package_builder_commit"],
        "proof_source_commit": manifest["proof_source_commit"],
    }


def verify_inner(root: Path, proof_source_commit: str) -> dict[str, object]:
    proof = root / "proof_package"
    manifest_path = proof / "ARCHIVE_MANIFEST.json"
    require(manifest_path.is_file(), "missing proof-core archive manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(manifest.get("source_commit") == proof_source_commit and
            manifest.get("kind") == "full_reproducibility",
            "proof-core manifest identity")
    rows = manifest.get("members")
    require(isinstance(rows, list) and
            manifest.get("member_count_excluding_manifest") == len(rows),
            "proof-core member count")
    seen: set[str] = set()
    total = 0
    for row in rows:
        require(isinstance(row, dict) and
                set(row) == {"path", "bytes", "mode", "sha256"},
                ("proof-core member row", row))
        relative = safe_relative(row["path"])
        require(relative not in seen, ("duplicate proof-core member", relative))
        seen.add(relative)
        path = proof / relative
        require(path.is_file() and path.stat().st_size == row["bytes"] and
                sha256_file(path) == row["sha256"],
                ("proof-core member mismatch", relative))
        total += row["bytes"]
    return {"core_member_count": len(rows), "core_member_bytes": total}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path,
                        default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    root = args.package_root.resolve()
    try:
        outer = verify_outer(root)
        inner = verify_inner(root, outer["proof_source_commit"])
        print(json.dumps({"status": "PASS", **outer, **inner}, sort_keys=True))
        print("K3P_REFEREE_PACKAGE_INTEGRITY_PASS")
        return 0
    except (IntegrityFailure, OSError, UnicodeError, json.JSONDecodeError,
            TypeError, ValueError) as error:
        print(f"K3P_REFEREE_PACKAGE_INTEGRITY_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
