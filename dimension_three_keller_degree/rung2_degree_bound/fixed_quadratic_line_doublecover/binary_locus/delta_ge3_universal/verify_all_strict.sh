#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
GP_BIN="${GP_BIN:-/opt/homebrew/bin/gp}"
CHECK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/delta-ge3-universal.XXXXXX")"
trap 'rm -rf -- "$CHECK_DIR"' EXIT

if ! "$PYTHON_BIN" -c 'import sympy' >/dev/null 2>&1; then
  echo "FAIL: $PYTHON_BIN cannot import sympy" >&2
  exit 2
fi
if [[ ! -x "$GP_BIN" ]]; then
  echo "FAIL: PARI/GP executable not found at $GP_BIN" >&2
  exit 2
fi

"$PYTHON_BIN" "$SCRIPT_DIR/verify_manifest.py" \
  >"$CHECK_DIR/manifest.out" 2>&1
grep -Fxq 'DELTA_GE3_MANIFEST_PASS_17_6_1' "$CHECK_DIR/manifest.out"

if DELTA_GE3_MANIFEST_FAULT=drop-id \
  "$PYTHON_BIN" "$SCRIPT_DIR/verify_manifest.py" \
  >"$CHECK_DIR/manifest-fault.out" 2>&1; then
  echo "FAIL: manifest verifier accepted its injected fault" >&2
  exit 1
fi
grep -Fq 'injected manifest fault detected' \
  "$CHECK_DIR/manifest-fault.out"

if "$PYTHON_BIN" -O "$SCRIPT_DIR/verify_incidence_sympy.py" \
  >"$CHECK_DIR/optimized.out" 2>&1; then
  echo "FAIL: symbolic verifier ran with assertions disabled" >&2
  exit 1
fi
grep -Fq 'FAIL: assertions are required' "$CHECK_DIR/optimized.out"

"$PYTHON_BIN" "$SCRIPT_DIR/verify_incidence_sympy.py" \
  >"$CHECK_DIR/sympy.out" 2>&1
grep -Fxq 'DELTA_GE3_UNIVERSAL_SYMPY_PASS_17_6_1' \
  "$CHECK_DIR/sympy.out"
if grep -Eq 'Traceback|(^|[^A-Z])FAIL:' "$CHECK_DIR/sympy.out"; then
  echo "FAIL: symbolic transcript contains an error" >&2
  exit 1
fi

"$GP_BIN" -q "$SCRIPT_DIR/verify_incidence_pari.gp" \
  >"$CHECK_DIR/pari.out" 2>&1
grep -Fxq 'DELTA_GE3_UNIVERSAL_PARI_PASS_17_6_1' \
  "$CHECK_DIR/pari.out"
if grep -Eq '^ *\*\*\*|user error|syntax error|forbidden' \
  "$CHECK_DIR/pari.out"; then
  echo "FAIL: PARI transcript contains an error" >&2
  exit 1
fi

echo "DELTA_GE3_UNIVERSAL_STRICT_PASS_17_6_1"
