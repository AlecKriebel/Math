#!/usr/bin/env python3
"""Seal this assigned public review tree; never reads or writes other trees."""
from pathlib import Path
import datetime as dt
import hashlib
import json

ROOT = Path(__file__).resolve().parent
EXCLUDED = {"AUTHORED_FILE_MANIFEST.json", "AUTHORED_FILE_MANIFEST.sha256"}


def main():
    files = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_symlink():
            raise RuntimeError("Symlink in review tree")
        if path.is_dir():
            continue
        if not path.is_file():
            raise RuntimeError("Unexpected review filesystem object")
        name = path.relative_to(ROOT).as_posix()
        if name in EXCLUDED:
            continue
        data = path.read_bytes()
        files.append({"path": name, "bytes": len(data),
                      "sha256": hashlib.sha256(data).hexdigest()})
    manifest = {"schema": 1,
                "sealed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                "review_completion_percent": 100,
                "scope": "All assigned authored review artifacts, derivations, code and receipts; third-party full source bodies and disposable original/mutated replay trees remain in ignored private custody. Only this manifest and its checksum are excluded from their own entries.",
                "files": files}
    target = ROOT / "AUTHORED_FILE_MANIFEST.json"
    target.write_text(json.dumps(manifest, indent=2) + "\n")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (ROOT / "AUTHORED_FILE_MANIFEST.sha256").write_text(digest + "  AUTHORED_FILE_MANIFEST.json\n")
    print(json.dumps({"files": len(files), "manifest_sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
