#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/usr/bin/python3}
SCRIPT="$SCRIPT_DIR/verify_w5_matrix_tower.py"

"$PYTHON_BIN" "$SCRIPT"

TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/w5-hostile.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

for mutation in \
  cubic_sign \
  reconstruction_y_sign \
  discriminant_sign \
  profile_discriminant \
  profile_leading \
  profile_guard \
  p2_value \
  norm_derivative \
  sheet_path \
  sheet_derivative \
  valuation_split \
  group_stride
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
    sed -n '1,120p' "$log" >&2
    exit 1
  fi
  echo "PASS fail-closed mutation: $mutation"
done

echo "ALL STRICT AND FAULT-GUARD RUNS PASSED"
