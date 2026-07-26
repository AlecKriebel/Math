#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SCRIPT="$HERE/verify_bs_n2_z_hostile.gp"
GP=/opt/homebrew/bin/gp
if [ ! -x "$GP" ]; then
  GP=$(command -v gp || true)
fi
if [ -z "$GP" ] || [ ! -x "$GP" ]; then
  echo "FAIL: PARI/GP is required" >&2
  exit 1
fi

AUDIT_TMP=$(mktemp -d)
trap 'rm -rf "$AUDIT_TMP"' EXIT HUP INT TERM

has_interpreter_error() {
  grep -Eiq '(^|[[:space:]])\*\*\*|syntax error|unexpected|skipping file|at top-level|incorrect type|user error|^FAIL ' "$1"
}

"$GP" -q "$SCRIPT" >"$AUDIT_TMP/base.log" 2>&1
if has_interpreter_error "$AUDIT_TMP/base.log"; then
  echo "FAIL: GP baseline emitted an interpreter or assertion error" >&2
  sed -n '1,120p' "$AUDIT_TMP/base.log" >&2
  exit 1
fi
if [ "$(grep -c '^D3_BS_N2_Z_HOSTILE_EXACT_PASS$' "$AUDIT_TMP/base.log")" -ne 1 ]; then
  echo "FAIL: exact terminal marker missing or duplicated" >&2
  exit 1
fi
if [ "$(tail -n 1 "$AUDIT_TMP/base.log")" != "D3_BS_N2_Z_HOSTILE_EXACT_PASS" ]; then
  echo "FAIL: exact terminal marker is not the final line" >&2
  exit 1
fi

set +e
D3_BS_AUDIT_FAULT=1 "$GP" -q "$SCRIPT" >"$AUDIT_TMP/fault.log" 2>&1
FAULT_STATUS=$?
set -e
if [ "$FAULT_STATUS" -eq 0 ]; then
  echo "FAIL: corrupted E3 certificate was accepted" >&2
  exit 1
fi
if grep -q '^D3_BS_N2_Z_HOSTILE_EXACT_PASS$' "$AUDIT_TMP/fault.log"; then
  echo "FAIL: corrupted run reached the success marker" >&2
  exit 1
fi
if ! grep -q '^FAIL Chart II d!=0 E3 cube:' "$AUDIT_TMP/fault.log"; then
  echo "FAIL: corrupted run did not fail at the intended certificate" >&2
  sed -n '1,120p' "$AUDIT_TMP/fault.log" >&2
  exit 1
fi

# Parser self-test: a forged marker accompanied by a GP syntax error must
# never be accepted as a clean log.
{
  echo '  *** syntax error, unexpected token'
  echo 'D3_BS_N2_Z_HOSTILE_EXACT_PASS'
} >"$AUDIT_TMP/forged.log"
if ! has_interpreter_error "$AUDIT_TMP/forged.log"; then
  echo "FAIL: interpreter-error parser accepted a forged log" >&2
  exit 1
fi

echo "D3_BS_N2_Z_HOSTILE_STRICT_PASS"
