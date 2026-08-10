#!/usr/bin/env python3
"""Write a deterministic hash manifest for this isolated review directory."""

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "MANIFEST.json"


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


rows = []
for path in sorted(HERE.rglob("*")):
    if (not path.is_file() or path == OUTPUT or "__pycache__" in path.parts or
            any(part.startswith("tmp") for part in path.parts)):
        continue
    rows.append({
        "path": str(path.relative_to(HERE)),
        "bytes": path.stat().st_size,
        "sha256": sha(path),
    })
payload = {
    "schema": "isolated-review-manifest-v1",
    "status": "VERIFIED",
    "files": rows,
}
OUTPUT.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
print(json.dumps({"files": len(rows), "manifest_sha256": sha(OUTPUT)},
                 sort_keys=True))
