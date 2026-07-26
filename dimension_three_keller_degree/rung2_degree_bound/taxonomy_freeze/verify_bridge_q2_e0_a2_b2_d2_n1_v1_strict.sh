#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
RUNG="$HERE/.."
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
GP_BIN=${GP_BIN:-/opt/homebrew/bin/gp}
CHECK_TMP=$(mktemp -d "${TMPDIR:-/tmp}/conic-embedding-bridge.XXXXXX")
trap 'rm -rf -- "$CHECK_TMP"' EXIT HUP INT TERM

[ -x "$PYTHON_BIN" ] || {
  echo "missing Python interpreter: $PYTHON_BIN" >&2
  exit 1
}
[ -x "$GP_BIN" ] || {
  echo "missing PARI/GP interpreter: $GP_BIN" >&2
  exit 1
}

"$PYTHON_BIN" "$HERE/verify_bridge_q2_e0_a2_b2_d2_n1_v1.py" \
  >"$CHECK_TMP/bridge.out"
grep -Fx "Q2_E0_A2_B2_D2_N1_BRIDGE_PRIMARY_PASS" \
  "$CHECK_TMP/bridge.out" >/dev/null

"$PYTHON_BIN" "$RUNG/verify_conic_doubleline_sympy.py" \
  >"$CHECK_TMP/lower-sympy.out"
grep -Fx "PASS: exact SymPy unique-double-line conic regressions" \
  "$CHECK_TMP/lower-sympy.out" >/dev/null

"$GP_BIN" -q "$RUNG/verify_conic_doubleline_pari.gp" \
  >"$CHECK_TMP/lower-pari.out" 2>&1
if grep -Ei '\*\*\*.*(error|at top-level|in function)|syntax error|skipping file' \
    "$CHECK_TMP/lower-pari.out" >/dev/null
then
  echo "lower PARI emitted an interpreter error" >&2
  exit 1
fi
grep -Fx "PASS: independent PARI unique-double-line conic regressions" \
  "$CHECK_TMP/lower-pari.out" >/dev/null

for mutation in frozen_hash tuple quadratic_extension pivot scope
do
  if "$PYTHON_BIN" "$HERE/verify_bridge_q2_e0_a2_b2_d2_n1_v1.py" \
      --mutation "$mutation" >"$CHECK_TMP/$mutation.out" 2>&1
  then
    echo "required-failure mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -F "AssertionError" "$CHECK_TMP/$mutation.out" >/dev/null
done

if PYTHONOPTIMIZE=1 "$PYTHON_BIN" \
    "$HERE/verify_bridge_q2_e0_a2_b2_d2_n1_v1.py" \
    >"$CHECK_TMP/optimized.out" 2>&1
then
  echo "optimized Python bypassed assertion guard" >&2
  exit 1
fi
grep -F "assertions disabled" "$CHECK_TMP/optimized.out" >/dev/null

echo "Q2_E0_A2_B2_D2_N1_BRIDGE_STRICT_PASS"
