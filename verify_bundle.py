#!/usr/bin/env python3
"""Verify the compact endpoint-capacity release without external packages."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "BUNDLE_MANIFEST.json"
FROZEN_CHECK = (
    ROOT
    / "results/verification/"
    "branch18_regular_endpoint_capacity_cover_v1.check.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def confined(relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute():
        raise ValueError(f"absolute bundle path: {relative}")
    resolved = (ROOT / candidate).resolve()
    resolved.relative_to(ROOT)
    return resolved


def check_bundle_files() -> dict[str, object]:
    payload = MANIFEST.read_bytes()
    loaded = json.loads(payload)
    if not isinstance(loaded, dict):
        raise ValueError("bundle manifest is not an object")
    files = loaded.get("files")
    if not isinstance(files, list):
        raise ValueError("bundle manifest files is not a list")

    seen: set[str] = set()
    checked = 0
    checked_bytes = 0
    for item in files:
        if not isinstance(item, dict):
            raise ValueError("bundle manifest file entry is not an object")
        relative = item.get("path")
        expected_bytes = item.get("bytes")
        expected_sha256 = item.get("sha256")
        if (
            not isinstance(relative, str)
            or not isinstance(expected_bytes, int)
            or not isinstance(expected_sha256, str)
        ):
            raise ValueError("malformed bundle file entry")
        if relative in seen:
            raise ValueError(f"duplicate bundle path: {relative}")
        seen.add(relative)
        path = confined(relative)
        actual_bytes = path.stat().st_size
        actual_sha256 = sha256(path)
        if actual_bytes != expected_bytes:
            raise ValueError(f"byte mismatch: {relative}")
        if actual_sha256 != expected_sha256:
            raise ValueError(f"SHA-256 mismatch: {relative}")
        checked += 1
        checked_bytes += actual_bytes

    actual_files = {
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file() and path != MANIFEST
    }
    if seen != actual_files:
        missing = sorted(actual_files - seen)
        extra = sorted(seen - actual_files)
        raise ValueError(
            f"bundle manifest file-set mismatch: "
            f"unlisted={missing}, absent={extra}"
        )

    return {
        "file_count": checked,
        "byte_count": checked_bytes,
        "bundle_manifest_sha256": hashlib.sha256(payload).hexdigest(),
    }


def run_checked(
    command: list[str], *, cwd: Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def main() -> int:
    try:
        file_summary = check_bundle_files()
        frozen_manifest = (
            ROOT
            / "results/benchmark_plans/"
            "branch18_regular_endpoint_capacity_cover_v1.json"
        ).read_bytes()
        frozen_classification = (
            ROOT
            / "certificates/"
            "branch18_regular_endpoint_capacity_cover_v1.pairs"
        ).read_bytes()
        with tempfile.TemporaryDirectory(
            prefix="endpoint-capacity-bundle-"
        ) as temporary:
            replay_root = Path(temporary) / "bundle"
            shutil.copytree(ROOT, replay_root)
            run_checked(
                [
                    sys.executable,
                    str(
                        replay_root
                        / "src/"
                        "branch18_regular_endpoint_capacity_cover.py"
                    ),
                    "--root",
                    str(replay_root),
                ],
                cwd=replay_root,
            )
            replay_manifest = (
                replay_root
                / "results/benchmark_plans/"
                "branch18_regular_endpoint_capacity_cover_v1.json"
            )
            replay_classification = (
                replay_root
                / "certificates/"
                "branch18_regular_endpoint_capacity_cover_v1.pairs"
            )
            if replay_manifest.read_bytes() != frozen_manifest:
                raise ValueError(
                    "regenerated manifest differs from frozen manifest"
                )
            if replay_classification.read_bytes() != frozen_classification:
                raise ValueError(
                    "regenerated classification differs from frozen stream"
                )

            replay = (
                replay_root
                / "results/verification/"
                "branch18_regular_endpoint_capacity_cover_v1.check.json"
            )
            run_checked(
                [
                    sys.executable,
                    str(
                        replay_root
                        / "verify/"
                        "branch18_regular_endpoint_capacity_cover_check.py"
                    ),
                    "--root",
                    str(replay_root),
                ],
                cwd=replay_root,
            )
            checker_report = json.loads(replay.read_bytes())
            if not checker_report.get("valid"):
                raise ValueError("independent checker reported invalid")
            if replay.read_bytes() != FROZEN_CHECK.read_bytes():
                raise ValueError("replayed check differs from frozen check")

            run_checked(
                [
                    sys.executable,
                    str(
                        replay_root
                        / "tests/"
                        "branch18_regular_endpoint_capacity_cover_tests.py"
                    ),
                ],
                cwd=replay_root,
            )
        result = {
            "schema": "ramsey55.endpoint_capacity_bundle_check.v1",
            "valid": True,
            "files": file_summary,
            "producer_reproduced_frozen_artifacts": True,
            "independent_checker_valid": True,
            "frozen_check_sha256": sha256(FROZEN_CHECK),
            "focused_test_count": 17,
            "focused_tests_passed": True,
        }
    except Exception as exc:
        result = {
            "schema": "ramsey55.endpoint_capacity_bundle_check.v1",
            "valid": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
