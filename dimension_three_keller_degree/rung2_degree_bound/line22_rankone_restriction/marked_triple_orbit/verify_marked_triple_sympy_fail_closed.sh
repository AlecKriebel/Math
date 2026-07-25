#!/bin/sh
set -eu

artifact_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/marked-triple-sympy-fail.XXXXXX")
trap 'rm -rf "$scratch_dir"' EXIT HUP INT TERM

expect_rejection()
{
  label=$1
  edit=$2
  sed "$edit" "$artifact_dir/verify_marked_triple_sympy.py" \
    >"$scratch_dir/tampered.py"

  if /usr/bin/python3 -u "$scratch_dir/tampered.py" \
    >"$scratch_dir/output.txt" 2>&1; then
    cat "$scratch_dir/output.txt"
    echo "FAIL: corrupted SymPy certificate was accepted: $label" >&2
    exit 1
  fi

  if ! grep -F 'AssertionError' "$scratch_dir/output.txt" >/dev/null; then
    cat "$scratch_dir/output.txt"
    echo "FAIL: corrupted SymPy certificate failed unexpectedly: $label" >&2
    exit 1
  fi

  echo "PASS fail-closed: $label corruption is rejected"
}

expect_rejection \
  "raw E7 minor" \
  's/483729408/483729409/'

expect_rejection \
  "open A=0 E4 leaf" \
  's@coefficient(E4_a0_l32, x\*\*4) - 4 \* w \* ll\[4\]@coefficient(E4_a0_l32, x**4) - 5 * w * ll[4]@'

expect_rejection \
  "resonant free-l13 leaf" \
  's@ae\[3\]: 2 \* le\[2\] / C,@ae[3]: 3 * le[2] / C,@'

expect_rejection \
  "K=A=0 exceptional leaf" \
  's@coefficient(E3_exc, x\*\*3) + 3 \* ae\[3\] \* le\[4\]@coefficient(E3_exc, x**3) + 4 * ae[3] * le[4]@'
