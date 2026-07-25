#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
SCRIPT="$SCRIPT_DIR/verify_vertical_hostile_exact.py"

"$PYTHON_BIN" "$SCRIPT"

TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/vertical-hostile.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

for mutation in \
  valuation_h_shift \
  fibre_modulus \
  orbit_shear_sign \
  companion_collapse \
  orbit_merge_ranks \
  stabilizer_z_shear \
  illegal_square_shear \
  quadratic_kernel \
  kernel_dimension \
  drop_minimality \
  e8_outside
do
  log="$TMP_AUDIT/$mutation.log"
  if AUDIT_MUTATION=$mutation "$PYTHON_BIN" "$SCRIPT" >"$log" 2>&1
  then
    echo "FAIL: mutation $mutation escaped its guard" >&2
    exit 1
  fi
  if ! grep -q "FAIL \\[$mutation\\]" "$log"
  then
    echo "FAIL: mutation $mutation did not fail through an audit guard" >&2
    sed -n '1,100p' "$log" >&2
    exit 1
  fi
  echo "PASS fail-closed mutation: $mutation"
done

echo "ALL STRICT AND FAULT-GUARD RUNS PASSED"
