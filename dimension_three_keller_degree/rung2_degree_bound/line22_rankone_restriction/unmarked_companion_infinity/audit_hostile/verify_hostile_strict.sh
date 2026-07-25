#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_file=${1:-"$script_dir/verify_unmarked_infinity_pure.py"}
output_file=$(mktemp "${TMPDIR:-/tmp}/unmarked-infinity-hostile.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if ! /usr/bin/python3 -u "$python_file" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

expected='PASS pure raw E7: nonzero rank-18 minor plus eight independent kernel directions prove completeness and the four/four gauge split
PASS pure E6/E5: E6 is exactly a constant rank-10 homogeneous system with full converse; four E5 coefficients force det L=0
ALL HOSTILE PURE-PYTHON UNMARKED-INFINITY CHECKS PASSED'

output=$(cat "$output_file")
if [ "$output" != "$expected" ]; then
  cat "$output_file"
  echo "FAIL: hostile verifier transcript differs from exact whitelist" >&2
  exit 1
fi

cat "$output_file"
