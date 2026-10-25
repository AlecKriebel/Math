#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "$0")" && pwd)"
PYTHON_BIN="${BIMOL_PYTHON:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Python executable not found: $PYTHON_BIN" >&2
    exit 2
fi

"$PYTHON_BIN" - <<'PY'
import sys

if sys.version_info < (3, 11):
    raise SystemExit(
        f"Python 3.11 or newer is required; found {sys.version.split()[0]}"
    )
PY

BIMOL_TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/bimolecular-pr.XXXXXX")"
cleanup() {
    if [[ -n "$BIMOL_TMP_DIR" && -d "$BIMOL_TMP_DIR" ]]; then
        rm -r -- "$BIMOL_TMP_DIR"
    fi
}
trap cleanup EXIT

export PYTHONPATH="$PACKAGE_ROOT/src"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0

"$PYTHON_BIN" -m unittest discover -s "$PACKAGE_ROOT/tests" -v

"$PYTHON_BIN" -m bimolecular_pr.verification \
    --root "$PACKAGE_ROOT" \
    --output "$BIMOL_TMP_DIR/run-1.json" \
    --provenance-output "$BIMOL_TMP_DIR/provenance.json"
"$PYTHON_BIN" -m bimolecular_pr.verification \
    --root "$PACKAGE_ROOT" \
    --output "$BIMOL_TMP_DIR/run-2.json"

if ! cmp -s "$BIMOL_TMP_DIR/run-1.json" "$BIMOL_TMP_DIR/run-2.json"; then
    echo "ERROR: two verifier runs produced different canonical JSON." >&2
    exit 1
fi

if ! cmp -s "$BIMOL_TMP_DIR/run-1.json" "$PACKAGE_ROOT/verification_report.json"; then
    echo "ERROR: regenerated canonical JSON differs from verification_report.json." >&2
    echo "The committed golden report was not overwritten." >&2
    exit 1
fi

"$PYTHON_BIN" - "$PACKAGE_ROOT/verification_report.json" "$BIMOL_TMP_DIR/provenance.json" <<'PY'
from hashlib import sha256
import json
from pathlib import Path
import sys

report = Path(sys.argv[1])
provenance = json.loads(Path(sys.argv[2]).read_text())
print(f"verification_report.json sha256: {sha256(report.read_bytes()).hexdigest()}")
print(
    "environment (not part of the canonical report): "
    f"{provenance['python_implementation']} {provenance['python_version']} on "
    f"{provenance['platform']}"
)
print("PASS: tests, repeated generation, and committed golden comparison all agree.")
PY
