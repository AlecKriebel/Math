#!/usr/bin/env bash
set -euo pipefail

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
CLOSURE="$(CDPATH= cd -- "$HERE/../.." && pwd)"
PYTHON="${STC_JC_PYTHON:-${PYTHON_BIN:-python3}}"

if [[ "$PYTHON" == */* ]]; then
  [[ -x "$PYTHON" ]] || {
    echo "Python interpreter is not executable: $PYTHON" >&2
    exit 2
  }
else
  command -v "$PYTHON" >/dev/null 2>&1 || {
    echo "Python interpreter is not available: $PYTHON" >&2
    exit 2
  }
fi

PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/exact_audit.py" \
  --output "$HERE/exact_audit_certificate.json"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" "$HERE/mutation_tests.py" \
  --output "$HERE/mutation_certificate.json"

if [[ "${1:-}" == "--with-upstream-replay" ]]; then
  PYTHONDONTWRITEBYTECODE=1 "$PYTHON" \
    "$CLOSURE/independent/bridge_cut/verify_bridge.py" \
    --output "$HERE/upstream_bridge_replay.json"
  PYTHONDONTWRITEBYTECODE=1 "$PYTHON" \
    "$CLOSURE/independent/bridge_cut/verify_cut.py" \
    --output "$HERE/upstream_cut_replay.json"
  PYTHONDONTWRITEBYTECODE=1 "$PYTHON" \
    "$CLOSURE/independent/bridge_cut/verify_mutations.py" \
    --output "$HERE/upstream_mutation_replay.json"
  cmp "$CLOSURE/independent/bridge_cut/bridge_certificate.json" \
      "$HERE/upstream_bridge_replay.json"
  cmp "$CLOSURE/independent/bridge_cut/cut_certificate.json" \
      "$HERE/upstream_cut_replay.json"
  cmp "$CLOSURE/independent/bridge_cut/mutation_certificate.json" \
      "$HERE/upstream_mutation_replay.json"
fi

shasum -a 256 \
  "$HERE/exact_audit.py" \
  "$HERE/mutation_tests.py" \
  "$HERE/exact_audit_certificate.json" \
  "$HERE/mutation_certificate.json" \
  "$CLOSURE/independent/bridge_cut/cut_certificate.json"
