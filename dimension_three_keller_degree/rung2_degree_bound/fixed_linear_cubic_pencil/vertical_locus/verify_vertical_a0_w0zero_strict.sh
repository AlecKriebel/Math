#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
SCRIPT="$SCRIPT_DIR/verify_vertical_a0_w0zero_sympy.py"

"$PYTHON_BIN" "$SCRIPT"

TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/a0-w0-zero.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

for mutation in \
  e6_minor \
  squarefree_e5_u \
  triple_c_e5_u \
  triple_b_e4_third \
  triple_e_e4_second \
  zero_e4_e_a10
do
  log="$TMP_AUDIT/$mutation.log"
  if A0_W0_ZERO_MUTATION="$mutation" "$PYTHON_BIN" "$SCRIPT" >"$log" 2>&1
  then
    echo "FAIL: mutation $mutation escaped" >&2
    exit 1
  fi
  grep -q "FAIL:" "$log"
  echo "PASS mutation rejected: $mutation"
done

if "$PYTHON_BIN" -O "$SCRIPT" >"$TMP_AUDIT/optimized.log" 2>&1
then
  echo "FAIL: optimized Python escaped" >&2
  exit 1
fi
grep -q "refusing optimized Python" "$TMP_AUDIT/optimized.log"

echo "VERTICAL_A0_W0_ZERO_STRICT_PASS_91D42B"
