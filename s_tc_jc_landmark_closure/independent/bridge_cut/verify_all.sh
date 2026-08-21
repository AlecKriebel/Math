#!/usr/bin/env bash
set -euo pipefail

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(CDPATH= cd -- "$HERE/../../.." && pwd)"
PYTHON="${PYTHON:-$ROOT/.venv/bin/python}"
LOCK="$ROOT/s_tc_jc_landmark_closure/docs/DEFINITIONS_LOCK.md"
LOCK_SHA256="5ba5a4c9bbd66553d3cb98915b2c1afeacb98034bf89471b881f06dc591b3005"

ACTUAL_LOCK_SHA256="$(shasum -a 256 "$LOCK" | awk '{print $1}')"
if [[ "$ACTUAL_LOCK_SHA256" != "$LOCK_SHA256" ]]; then
  echo "definitions lock digest mismatch" >&2
  echo "expected: $LOCK_SHA256" >&2
  echo "actual:   $ACTUAL_LOCK_SHA256" >&2
  exit 1
fi

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/verify_bridge.py" \
  --output "$HERE/bridge_certificate.json"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/verify_palette_reduction.py" \
  --output "$HERE/palette_reduction_certificate.json"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/verify_cut.py" \
  --output "$HERE/cut_certificate.json"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/verify_mutations.py" \
  --output "$HERE/mutation_certificate.json"

shasum -a 256 \
  "$HERE/verify_bridge.py" \
  "$HERE/verify_palette_reduction.py" \
  "$HERE/verify_cut.py" \
  "$HERE/verify_mutations.py" \
  "$HERE/PROOF.md" \
  "$HERE/CUT_PALETTE_REDUCTION.md" \
  "$HERE/bridge_certificate.json" \
  "$HERE/palette_reduction_certificate.json" \
  "$HERE/cut_certificate.json" \
  "$HERE/mutation_certificate.json" \
  "$LOCK"

(cd "$ROOT" && shasum -a 256 -c \
  s_tc_jc_landmark_closure/independent/bridge_cut/MANIFEST.sha256)
