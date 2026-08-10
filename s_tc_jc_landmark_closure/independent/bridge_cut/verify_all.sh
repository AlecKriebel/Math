#!/usr/bin/env bash
set -euo pipefail

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ROOT="$(CDPATH= cd -- "$HERE/../../.." && pwd)"
PYTHON="${PYTHON:-$ROOT/.venv/bin/python}"
LOCK="$ROOT/s_tc_jc_landmark_closure/docs/DEFINITIONS_LOCK.md"
LOCK_SHA256="c3382650fa004d90b2122aff1c95524590b31e436d77d4b804293184aa925b09"

ACTUAL_LOCK_SHA256="$(shasum -a 256 "$LOCK" | awk '{print $1}')"
if [[ "$ACTUAL_LOCK_SHA256" != "$LOCK_SHA256" ]]; then
  echo "definitions lock digest mismatch" >&2
  echo "expected: $LOCK_SHA256" >&2
  echo "actual:   $ACTUAL_LOCK_SHA256" >&2
  exit 1
fi

PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/verify_bridge.py" \
  --output "$HERE/bridge_certificate.json"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/verify_cut.py" \
  --output "$HERE/cut_certificate.json"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/verify_mutations.py" \
  --output "$HERE/mutation_certificate.json"

shasum -a 256 \
  "$HERE/verify_bridge.py" \
  "$HERE/verify_cut.py" \
  "$HERE/verify_mutations.py" \
  "$HERE/bridge_certificate.json" \
  "$HERE/cut_certificate.json" \
  "$HERE/mutation_certificate.json" \
  "$LOCK"
