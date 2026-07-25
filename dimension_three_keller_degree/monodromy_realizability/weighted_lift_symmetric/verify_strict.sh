#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

/usr/bin/python3 "$script_dir/verify_morse_sympy.py"
/usr/bin/python3 "$script_dir/verify_general_seed_sympy.py"

geometric_output=$(gp -q "$script_dir/verify_geometric_branches_pari.gp" 2>&1)
printf '%s\n' "$geometric_output"

case "$geometric_output" in
  *"***"*)
    echo "PARI reported an error in the geometric branch check" >&2
    exit 1
    ;;
esac

geometric_pass_count=$(printf '%s\n' "$geometric_output" | grep -c '^PASS d=')
if [ "$geometric_pass_count" -ne 18 ]; then
  echo "PARI did not certify all eighteen geometric rows" >&2
  exit 1
fi

printf '%s\n' "$geometric_output" |
  grep -q '^PASS: exact geometric branch checks for d=3,...,20$'

pari_output=$(gp -q "$script_dir/verify_specializations_pari.gp" 2>&1)
printf '%s\n' "$pari_output"

case "$pari_output" in
  *"***"*)
    echo "PARI reported an error" >&2
    exit 1
    ;;
esac

pass_count=$(printf '%s\n' "$pari_output" | grep -c '^PASS d=')
if [ "$pass_count" -ne 8 ]; then
  echo "PARI did not certify all eight rows" >&2
  exit 1
fi

printf '%s\n' "$pari_output" |
  grep -q '^PASS: arithmetic S_d specializations for d=3,...,10$'

echo "ALL WEIGHTED-LIFT MONODROMY CHECKS PASSED"
