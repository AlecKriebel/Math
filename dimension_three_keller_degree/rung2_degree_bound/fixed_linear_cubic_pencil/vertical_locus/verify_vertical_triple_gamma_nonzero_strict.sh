#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
SCRIPT="$SCRIPT_DIR/verify_vertical_triple_gamma_nonzero_sympy.py"

"$PYTHON_BIN" "$SCRIPT"

TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/gamma-nonzero.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

for mutation in quadratic_y mixed_xy_first mixed_xy_second linear_y
do
  log="$TMP_AUDIT/$mutation.log"
  if GAMMA_NONZERO_MUTATION="$mutation" "$PYTHON_BIN" "$SCRIPT" >"$log" 2>&1
  then
    echo "FAIL: mutation $mutation escaped" >&2
    exit 1
  fi
  grep -q "FAIL:" "$log"
  echo "PASS mutation rejected: $mutation"
done

echo "VERTICAL_TRIPLE_GAMMA_NONZERO_STRICT_PASS_0A6B35"
