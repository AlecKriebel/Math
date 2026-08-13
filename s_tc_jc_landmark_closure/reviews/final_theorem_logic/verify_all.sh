#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
python3 "$HERE/structural_checks.py"
python3 "$HERE/n4_support_check.py"

python3 - "$HERE" <<'PY'
import hashlib
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
manifest = root / "MANIFEST.sha256"
for line in manifest.read_text().splitlines():
    if not line.strip():
        continue
    expected, name = line.split("  ", 1)
    actual = hashlib.sha256((root / name).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"manifest mismatch for {name}: {actual} != {expected}")
print("manifest: VERIFIED")
PY
