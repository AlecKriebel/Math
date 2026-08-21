#!/usr/bin/env python3
"""Build or check the separate lock for direct-closure release artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOCK_PATH = ROOT / "DIRECT_CLOSURE_LOCK.json"
TOP_LEVEL_FILES = (
    "INPUT_LOCK.json",
    "README_DIRECT_CLOSURE.md",
    "build_direct_closure_lock.py",
    "test_direct_closure_release_mutations.py",
    "verify_direct_closure_release.py",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def release_files() -> tuple[Path, ...]:
    paths = [ROOT / relative for relative in TOP_LEVEL_FILES]
    for directory in (ROOT / "proofs", ROOT / "results/four_port_release_v4"):
        paths.extend(
            path
            for path in directory.rglob("*")
            if path.is_file()
            and "__pycache__" not in path.parts
            and path.name != ".DS_Store"
            and not path.name.endswith((".pyc", ".pyo"))
        )
    paths = sorted(set(paths), key=lambda path: path.relative_to(ROOT).as_posix())
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise SystemExit(f"missing release files: {missing}")
    return tuple(paths)


def payload() -> dict:
    paths = release_files()
    files = {
        path.relative_to(ROOT).as_posix(): sha256_file(path)
        for path in paths
    }
    return {
        "schema": "k2p-four-port-direct-closure-lock-v1",
        "engine_input_lock_sha256": files["INPUT_LOCK.json"],
        "expected_candidate_record_count": 36,
        "expected_manifest_summary_count": 1931,
        "expected_proof_family_counts": {
            "lower_theta_quartic": 12,
            "theta0_quintic_port_orbit": 22,
            "theta3_cubic": 2,
        },
        "file_count": len(files),
        "total_bytes": sum(path.stat().st_size for path in paths),
        "files": files,
    }


def canonical_bytes(value: dict) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    if not __debug__:
        raise SystemExit("lock qualification requires assertions; do not use python -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = canonical_bytes(payload())
    if args.check:
        if not LOCK_PATH.is_file() or LOCK_PATH.read_bytes() != expected:
            raise SystemExit("DIRECT_CLOSURE_LOCK_MISMATCH")
        print("DIRECT_CLOSURE_LOCK_PASS")
        return
    temporary = LOCK_PATH.with_name(f"{LOCK_PATH.name}.tmp.{os.getpid()}")
    with temporary.open("wb") as handle:
        handle.write(expected)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, LOCK_PATH)
    print(f"DIRECT_CLOSURE_LOCK_WRITTEN files={payload()['file_count']}")


if __name__ == "__main__":
    main()
