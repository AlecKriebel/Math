#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
SCRIPT="$SCRIPT_DIR/verify_vertical_triple_gamma0_reduction_sympy.py"

"$PYTHON_BIN" "$SCRIPT"

TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/gamma0-reduction.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

for chart in quadratic_y mixed_xy linear_y
do
  for stage in v u
  do
    mutation="${chart}_${stage}"
    log="$TMP_AUDIT/$mutation.log"
    if GAMMA0_REDUCTION_MUTATION="$mutation" "$PYTHON_BIN" "$SCRIPT" >"$log" 2>&1
    then
      echo "FAIL: mutation $mutation escaped" >&2
      exit 1
    fi
    grep -q "FAIL:" "$log"
    echo "PASS mutation rejected: $mutation"
  done
done

echo "VERTICAL_TRIPLE_GAMMA0_REDUCTION_STRICT_PASS_8A3D64"
