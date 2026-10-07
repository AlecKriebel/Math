#!/usr/bin/env python3
"""Build a deterministic, explicitly whitelisted research archive.

This program neither validates a theorem nor uploads anything. No directory
walk is used to choose package contents, and symlinks are rejected.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CONFIG = Path(__file__).with_name("package_files.json")


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def safe_path(name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name or not name:
        raise ValueError(f"Unsafe package path: {name!r}")
    source = ROOT.joinpath(*path.parts)
    if any(part.is_symlink() for part in [source, *source.parents] if part != ROOT.parent):
        raise ValueError(f"Symlink in package path: {name}")
    if not source.is_file():
        raise FileNotFoundError(source)
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New ZIP path; existing output is never overwritten")
    parser.add_argument("--release", action="store_true", help="Require every explicit publication clearance gate")
    args = parser.parse_args()
    config = json.loads(CONFIG.read_text())
    names = config["files"]
    if names != sorted(set(names)):
        raise ValueError("Whitelist must be sorted and contain no duplicate paths")
    control = ROOT / "publication/support/RELEASE_STATUS.json"
    status = json.loads(control.read_text()) if control.exists() else {"state": "uncleared", "gates": {}}
    if args.release:
        if status["state"] != "cleared" or not status["gates"] or not all(value is True for value in status["gates"].values()):
            raise ValueError("Publication clearance is incomplete; a draft archive can still be built without --release")
    forbidden_parts = {".git", "runtime", "upstream_090", "__pycache__", ".venv"}
    payloads = {}
    entries = []
    for name in names:
        if forbidden_parts.intersection(PurePosixPath(name).parts) or "sources" in PurePosixPath(name).parts:
            raise ValueError(f"Forbidden source/runtime path: {name}")
        content = safe_path(name).read_bytes()
        if len(content) > 50 * 1024 * 1024:
            raise ValueError(f"Unexpectedly large package file: {name}")
        payloads[name] = content
        entries.append({"path": name, "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
    identity = hashlib.sha256(canonical(entries)).hexdigest()
    manifest = {
        "schema": "openai-wreath-planar-package-v1",
        "identity_algorithm": "SHA256 of canonical JSON file inventory (sorted keys, compact separators, UTF-8)",
        "package_identity_sha256": identity,
        "release_state": "verification-materials",
        "files": entries,
        "manifest_self_inclusion": False,
    }
    payloads["PACKAGE_MANIFEST.json"] = json.dumps(manifest, indent=2, sort_keys=True).encode() + b"\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(args.output, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(payloads.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    print(json.dumps({"package_identity_sha256": identity, "archive": str(args.output), "archive_bytes": args.output.stat().st_size, "archive_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest(), "file_count": len(entries), "release_state": "verification-materials"}, indent=2))


if __name__ == "__main__":
    main()
