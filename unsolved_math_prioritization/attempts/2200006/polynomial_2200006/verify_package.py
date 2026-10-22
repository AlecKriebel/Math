#!/usr/bin/env python3
"""Read-only strict inventory/hash verification and portable exact replay."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    expected = {item["path"] for item in manifest["files"]} | {"MANIFEST.json"}
    actual = set()
    for p in root.rglob("*"):
        if p.is_symlink() or not p.is_file():
            raise ValueError("Unexpected non-regular entry: " + str(p.relative_to(root)))
        actual.add(p.relative_to(root).as_posix())
    if actual != expected:
        raise ValueError("Inventory mismatch: " + repr(actual ^ expected))
    for item in manifest["files"]:
        rel = Path(item["path"])
        if rel.is_absolute() or ".." in rel.parts:
            raise ValueError("Unsafe manifest path")
        data = (root / rel).read_bytes()
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            raise ValueError("Hash or size mismatch: " + str(rel))
    output = subprocess.run([sys.executable, "-B", str(root / "verify_math.py")],
                            check=True, stdout=subprocess.PIPE).stdout
    if output != (root / "results.json").read_bytes():
        raise ValueError("Exact replay differs from frozen receipt")
    print(json.dumps({"inventory": "PASS", "hashes": "PASS", "replay": "PASS",
                      "manifest_sha256": hashlib.sha256((root / "MANIFEST.json").read_bytes()).hexdigest(),
                      "files": len(expected),
                      "assertions": json.loads(output)["assertions"]}, sort_keys=True))


if __name__ == "__main__":
    main()
