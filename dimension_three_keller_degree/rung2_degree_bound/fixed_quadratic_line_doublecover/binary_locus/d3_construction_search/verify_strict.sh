#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
GP_BIN=${GP_BIN:-/opt/homebrew/bin/gp}
CHECK_TMP=$(mktemp -d "${TMPDIR:-/tmp}/d3-construction-search.XXXXXX")
trap 'rm -rf -- "$CHECK_TMP"' EXIT HUP INT TERM

[ -x "$PYTHON_BIN" ] || {
  echo "missing Python interpreter: $PYTHON_BIN" >&2
  exit 1
}
"$PYTHON_BIN" -c 'import sympy' >/dev/null
[ -x "$GP_BIN" ] || {
  echo "missing PARI/GP interpreter: $GP_BIN" >&2
  exit 1
}

"$PYTHON_BIN" "$HERE/verify_ansatz_obstructions.py" >"$CHECK_TMP/exact.out"
grep -Fx "D3_CONSTRUCTION_EXACT_OBSTRUCTIONS_PASS" \
  "$CHECK_TMP/exact.out" >/dev/null

"$GP_BIN" -q "$HERE/verify_independent_pari.gp" \
  >"$CHECK_TMP/pari.out" 2>&1
if grep -Ei \
    '\*\*\*.*(at top-level|syntax error|error in|error:|not a function|incorrect type|unexpected|stack overflows|bug in PARI)|syntax error|skipping file' \
    "$CHECK_TMP/pari.out" >/dev/null
then
  echo "independent PARI emitted an interpreter error" >&2
  exit 1
fi
grep -Fx "D3_CONSTRUCTION_INDEPENDENT_PARI_PASS" \
  "$CHECK_TMP/pari.out" >/dev/null

if D3_AUDIT_FAULT=1 "$GP_BIN" -q "$HERE/verify_independent_pari.gp" \
    >"$CHECK_TMP/pari-fault.out" 2>&1
then
  echo "independent PARI required-failure mutation unexpectedly passed" >&2
  exit 1
fi
if grep -Fx "D3_CONSTRUCTION_INDEPENDENT_PARI_PASS" \
    "$CHECK_TMP/pari-fault.out" >/dev/null
then
  echo "independent PARI fault reached the terminal marker" >&2
  exit 1
fi
grep -F "FAIL BB full decisive E5 coefficient" \
  "$CHECK_TMP/pari-fault.out" >/dev/null

"$PYTHON_BIN" "$HERE/search_modular.py" >"$CHECK_TMP/modular.out"
grep -Fx "D3_CONSTRUCTION_MODULAR_FROZEN_COUNTS_PASS" \
  "$CHECK_TMP/modular.out" >/dev/null
grep -Fx "D3_CONSTRUCTION_MODULAR_RECON_PASS" \
  "$CHECK_TMP/modular.out" >/dev/null

for mutation in denominator zero_square bs_tangent bs_full bb_tangent origin
do
  if "$PYTHON_BIN" "$HERE/verify_ansatz_obstructions.py" \
      --mutation "$mutation" >"$CHECK_TMP/$mutation.out" 2>&1
  then
    echo "required-failure mutation unexpectedly passed: $mutation" >&2
    exit 1
  fi
  grep -F "AssertionError" "$CHECK_TMP/$mutation.out" >/dev/null
done

if PYTHONOPTIMIZE=1 "$PYTHON_BIN" "$HERE/verify_ansatz_obstructions.py" \
    >"$CHECK_TMP/optimized.out" 2>&1
then
  echo "optimized Python bypassed the assertion guard" >&2
  exit 1
fi
grep -F "assertions must remain enabled" "$CHECK_TMP/optimized.out" >/dev/null

if "$PYTHON_BIN" "$HERE/search_modular.py" \
    --primes 7 --trials 1 --samples 1 >"$CHECK_TMP/bad-prime.out" 2>&1
then
  echo "bad-prime modular mutation unexpectedly passed" >&2
  exit 1
fi
grep -F "use good primes" "$CHECK_TMP/bad-prime.out" >/dev/null

echo "D3_CONSTRUCTION_SEARCH_STRICT_PASS"
