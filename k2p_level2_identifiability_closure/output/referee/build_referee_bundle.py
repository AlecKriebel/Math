#!/usr/bin/env python3
"""Build the exact portable evidence bundle committed by RELEASE_LOCK.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath


PROJECT = Path(__file__).resolve().parents[2]
LOCK_RELATIVE = "work/final_theorem_release/RELEASE_LOCK.json"
EXPECTED_LOCK_SHA256 = "528e999243f9c43bf7ac4102607f0024610fcffd71cce66eeb50ca054dbc2970"
EXPECTED_LOCK_PAYLOAD = "ea73c7af4129a8f43a0d78b894a940145f1ec2327be1ea11f53645c3a6c7f1ba"
EXPECTED_FILE_COUNT = 408
EXPECTED_TOTAL_BYTES = 479_376_170
EXPECTED_CONTENT_ROOT = "4a4b1316bf13d16df3ebb5e304b2aa8b0621568a26a6ac63c051c095f5e6fb33"
ARCHIVE_PREFIX = "k2p_principal_d_plus_referee_release"


def fail(message: str) -> None:
    raise SystemExit(message)


def reject_optimized_mode() -> None:
    if not __debug__:
        fail("optimized Python is forbidden")


def safe_relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        fail(f"unsafe relative path: {value!r}")
    return path


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(relative: str) -> dict:
    return json.loads(PROJECT.joinpath(*safe_relative(relative).parts).read_text(encoding="utf-8"))


def add_manifest_paths(paths: set[str], manifest_relative: str, base_relative: str) -> None:
    manifest = PROJECT.joinpath(*safe_relative(manifest_relative).parts)
    base = PurePosixPath(base_relative)
    for ordinal, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if match is None:
            fail(f"invalid manifest line {manifest_relative}:{ordinal}")
        digest, child = match.groups()
        relative = (base / safe_relative(child)).as_posix()
        data = PROJECT.joinpath(*safe_relative(relative).parts).read_bytes()
        if sha256_bytes(data) != digest:
            fail(f"nested manifest hash mismatch: {relative}")
        paths.add(relative)


def collect_ledger() -> dict[str, dict[str, int | str]]:
    lock_path = PROJECT / LOCK_RELATIVE
    lock_bytes = lock_path.read_bytes()
    if sha256_bytes(lock_bytes) != EXPECTED_LOCK_SHA256:
        fail("RELEASE_LOCK byte hash mismatch")
    lock = json.loads(lock_bytes)
    if lock.get("payload_sha256") != EXPECTED_LOCK_PAYLOAD:
        fail("RELEASE_LOCK payload mismatch")
    if lock.get("promotion_ready") is not True or lock.get("blockers") or lock.get("missing_required_files"):
        fail("release is not promotion-ready")

    paths = set(lock.get("files", {}))
    if len(paths) != 231:
        fail("unexpected outer file count")

    add_manifest_paths(
        paths,
        "work/rank_upper_certificates/MANIFEST.sha256",
        "work/rank_upper_certificates",
    )
    add_manifest_paths(
        paths,
        "work/cycle_three_port_closure/MANIFEST.sha256",
        "work/cycle_three_port_closure",
    )

    direct_root = PurePosixPath("package/referee/k2p_offline_sweep_portable")
    for nested_name in ("DIRECT_CLOSURE_LOCK.json", "INPUT_LOCK.json"):
        nested = read_json((direct_root / nested_name).as_posix())
        nested_files = nested.get("files")
        if not isinstance(nested_files, dict):
            fail(f"missing nested file map: {nested_name}")
        for child, digest in nested_files.items():
            relative = (direct_root / safe_relative(child)).as_posix()
            data = PROJECT.joinpath(*safe_relative(relative).parts).read_bytes()
            if sha256_bytes(data) != digest:
                fail(f"nested lock hash mismatch: {relative}")
            paths.add(relative)

    paths.add(LOCK_RELATIVE)
    ledger: dict[str, dict[str, int | str]] = {}
    for relative in sorted(paths):
        path = PROJECT.joinpath(*safe_relative(relative).parts)
        if not path.is_file() or path.is_symlink():
            fail(f"missing or symbolic evidence file: {relative}")
        data = path.read_bytes()
        metadata = {"bytes": len(data), "sha256": sha256_bytes(data)}
        outer = lock.get("files", {}).get(relative)
        if outer is not None and (
            metadata["bytes"] != outer.get("bytes") or metadata["sha256"] != outer.get("sha256")
        ):
            fail(f"outer lock mismatch: {relative}")
        ledger[relative] = metadata

    canonical = json.dumps(ledger, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    total_bytes = sum(int(row["bytes"]) for row in ledger.values())
    content_root = sha256_bytes(canonical)
    if len(ledger) != EXPECTED_FILE_COUNT:
        fail(f"file-count mismatch: {len(ledger)}")
    if total_bytes != EXPECTED_TOTAL_BYTES:
        fail(f"byte-count mismatch: {total_bytes}")
    if content_root != EXPECTED_CONTENT_ROOT:
        fail(f"content-root mismatch: {content_root}")
    return ledger


def write_ledger(path: Path, ledger: dict[str, dict[str, int | str]]) -> None:
    payload = {
        "schema": "k2p-principal-d-plus-referee-content-ledger-v1",
        "release_lock_sha256": EXPECTED_LOCK_SHA256,
        "release_lock_payload_sha256": EXPECTED_LOCK_PAYLOAD,
        "file_count": len(ledger),
        "total_bytes": sum(int(row["bytes"]) for row in ledger.values()),
        "content_ledger_root_sha256": EXPECTED_CONTENT_ROOT,
        "files": ledger,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_zip(path: Path, ledger: dict[str, dict[str, int | str]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in ledger:
            data = PROJECT.joinpath(*safe_relative(relative).parts).read_bytes()
            info = zipfile.ZipInfo(f"{ARCHIVE_PREFIX}/{relative}", date_time=(2026, 8, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return sha256_bytes(path.read_bytes())


def main() -> None:
    reject_optimized_mode()
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.check_only and args.output is None and args.ledger is None:
        parser.error("provide --check-only, --ledger, or --output")

    ledger = collect_ledger()
    if args.ledger is not None:
        write_ledger(args.ledger, ledger)
    result = {
        "content_ledger_root_sha256": EXPECTED_CONTENT_ROOT,
        "file_count": len(ledger),
        "release_lock_sha256": EXPECTED_LOCK_SHA256,
        "total_bytes": sum(int(row["bytes"]) for row in ledger.values()),
    }
    if args.output is not None:
        result["archive_path"] = str(args.output)
        result["archive_sha256"] = write_zip(args.output, ledger)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
