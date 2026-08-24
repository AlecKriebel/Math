#!/usr/bin/env python3
"""Independently inspect rebuilt outer archives and the older inner archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import zipfile
from pathlib import Path
from typing import Any


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect(
    archive_path: Path,
    source_root: Path,
    expected_relatives: list[str],
    prefix: str,
    timestamp: tuple[int, int, int, int, int, int],
    uniform_mode: int | None,
) -> dict[str, Any]:
    problems: list[str] = []
    rows: list[dict[str, Any]] = []
    with zipfile.ZipFile(archive_path, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        expected_names = [f"{prefix}/{relative}" for relative in expected_relatives]
        if names != expected_names:
            problems.append("member list/order mismatch")
        if len(names) != len(set(names)):
            problems.append("duplicate member names")
        bad_crc = archive.testzip()
        if bad_crc is not None:
            problems.append(f"CRC failure: {bad_crc}")
        for info, relative in zip(infos, expected_relatives):
            data = archive.read(info)
            source = source_root / relative
            source_data = source.read_bytes()
            mode = info.external_attr >> 16
            expected_mode = uniform_mode
            if expected_mode is None:
                expected_mode = 0o100755 if source.stat().st_mode & stat.S_IXUSR else 0o100644
            row_problems = []
            if data != source_data:
                row_problems.append("content")
            if info.date_time != timestamp:
                row_problems.append("timestamp")
            if info.compress_type != zipfile.ZIP_DEFLATED:
                row_problems.append("compression")
            if info.create_system != 3:
                row_problems.append("create_system")
            if mode != expected_mode:
                row_problems.append("mode")
            if info.extra or info.comment:
                row_problems.append("extra_or_comment")
            if row_problems:
                problems.append(f"{relative}: {','.join(row_problems)}")
            rows.append(
                {
                    "path": relative,
                    "bytes": len(data),
                    "sha256": sha(data),
                    "compressed_bytes": info.compress_size,
                    "mode": oct(mode),
                    "timestamp": list(info.date_time),
                    "match": not row_problems,
                }
            )
    return {
        "path": str(archive_path.resolve()),
        "bytes": archive_path.stat().st_size,
        "sha256": file_sha(archive_path),
        "members": len(rows),
        "problems": problems,
        "member_checks_retained": "all members checked; only problems are retained in this compact report",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--outer-distributed", type=Path, required=True)
    parser.add_argument("--outer-a", type=Path, required=True)
    parser.add_argument("--outer-b", type=Path, required=True)
    parser.add_argument("--inner", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    handoff = args.handoff.resolve()
    manifest = json.loads((handoff / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    binding = json.loads((handoff / "SUBMISSION_BINDING.json").read_text(encoding="utf-8"))
    outer_relatives = sorted(set(manifest["files"]) | {"PACKAGE_MANIFEST.json"})
    outer_results = [
        inspect(
            path.resolve(),
            handoff,
            outer_relatives,
            "k2p_ai_referee_handoff_2026-08-23",
            (2026, 8, 23, 0, 0, 0),
            None,
        )
        for path in (args.outer_distributed, args.outer_a, args.outer_b)
    ]
    project = handoff / "materials/k2p_principal_d_plus_submission_referee"
    inner_manifest_rel = "proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json"
    inner_manifest = json.loads((project / inner_manifest_rel).read_text(encoding="utf-8"))
    inner_relatives = sorted(
        set(inner_manifest["frozen_evidence"]["files"])
        | set(inner_manifest["submission_sources"]["files"])
        | {inner_manifest_rel}
    )
    inner_result = inspect(
        args.inner.resolve(),
        project,
        inner_relatives,
        "k2p_principal_d_plus_submission_referee",
        (2026, 8, 22, 0, 0, 0),
        0o100644,
    )
    outer_identical = args.outer_distributed.read_bytes() == args.outer_a.read_bytes() == args.outer_b.read_bytes()
    expected_outer_sha = "c681f1984dbd95c7a8095593da339488544e03825232b5f8488050e94cdc27fd"
    outer_hashes = [row["sha256"] for row in outer_results]
    checks = {
        "outer_archives_byte_identical": outer_identical,
        "outer_hashes_expected": outer_hashes == [expected_outer_sha] * 3,
        "outer_member_checks": all(not row["problems"] for row in outer_results),
        "inner_hash_outer_manifest": inner_result["sha256"] == manifest["source_archive_sha256"],
        "inner_hash_submission_binding": inner_result["sha256"]
        == binding["computational_evidence"]["source_archive_sha256"],
        "inner_member_checks": not inner_result["problems"],
        "outer_member_count": all(row["members"] == 493 for row in outer_results),
        "inner_member_count": inner_result["members"] == 448,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    value: dict[str, Any] = {
        "schema": "independent-k2p-archive-audit-v1",
        "status": status,
        "checks": checks,
        "outer_archives": outer_results,
        "inner_archive": inner_result,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "checks": checks, "output": str(args.output.resolve())}, sort_keys=True))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
