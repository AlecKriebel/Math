#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp)
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if ! gp -q "$script_dir/audit_exact_pari.gp" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

if grep -E '(^|[^A-Z])FAIL([ :]|$)|\*\*\*|at top-level|syntax error' \
    "$output_file" >/dev/null 2>&1; then
  cat "$output_file"
  exit 1
fi

expected='PASS: hostile exact PARI normal-form and kernel reconstruction'
last_line=$(tail -n 1 "$output_file")
if [ "$last_line" != "$expected" ]; then
  cat "$output_file"
  exit 1
fi

cat "$output_file"
