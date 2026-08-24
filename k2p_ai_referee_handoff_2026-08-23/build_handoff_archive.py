#!/usr/bin/env python3
"""Build a deterministic ZIP from the sealed outer handoff manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "PACKAGE_MANIFEST.json"
PREFIX = "k2p_ai_referee_handoff_2026-08-23"
TIMESTAMP = (2026, 8, 23, 0, 0, 0)


def main() -> None:
    if not __debug__:
        raise SystemExit("optimized Python is forbidden")
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    unsigned = dict(manifest)
    payload = unsigned.pop("payload_sha256", None)
    encoded = json.dumps(unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    if payload != hashlib.sha256(encoded).hexdigest():
        raise SystemExit("outer manifest payload mismatch")
    paths = sorted(set(manifest["files"]) | {"PACKAGE_MANIFEST.json"})
    output = args.output.resolve()
    try:
        output.relative_to(ROOT)
    except ValueError:
        pass
    else:
        raise SystemExit("archive output must be outside the immutable handoff folder")
    for relative, row in manifest["files"].items():
        source = ROOT / relative
        data = source.read_bytes()
        if row != {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}:
            raise SystemExit(f"stale manifest binding: {relative}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in paths:
            source = ROOT / relative
            data = source.read_bytes()
            info = zipfile.ZipInfo(f"{PREFIX}/{relative}", date_time=TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o100755 if source.stat().st_mode & 0o111 else 0o100644
            info.external_attr = mode << 16
            info.create_system = 3
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    data = output.read_bytes()
    print(json.dumps({
        "status": "PASS",
        "path": str(output),
        "bytes": len(data),
        "members": len(paths),
        "sha256": hashlib.sha256(data).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
