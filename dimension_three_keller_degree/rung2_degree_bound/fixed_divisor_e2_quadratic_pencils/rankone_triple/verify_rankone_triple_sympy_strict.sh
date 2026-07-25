#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_file=${1:-"$script_dir/verify_rankone_triple_sympy.py"}
output_file=$(mktemp "${TMPDIR:-/tmp}/rankone-sympy.XXXXXX")
expected_file=$(mktemp "${TMPDIR:-/tmp}/rankone-sympy-expected.XXXXXX")
trap 'rm -f "$output_file" "$expected_file"' EXIT HUP INT TERM

if ! /usr/bin/python3 "$python_file" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

cat >"$expected_file" <<'EOF'
PASS raw E7: rank 8/nullity 18, complete four-gauge normal
PASS E6: w4=w5=0 and the four reduced compatibility equations
PASS A=0,w3!=0: E5 tail collapse; D=0 exits at E5 and both D!=0 a3 charts exit at E3
PASS A=0 origin: explicit a3=0 and a3!=0 rank-drop exits
PASS A=0 xz axis: all E5 rank drops, then literal E4 exit
PASS A=0 xy axis: every E5/E4 rank drop and both E4-factor descendants
PASS A!=0 top cover and w3=0: W=0 factor or literal E4 exit
PASS A!=0 equal branch away from plus/minus: both D charts singular
PASS A!=0 minus resonance: all D and w rank drops
PASS A!=0 plus resonance: every open and aligned D chart
all rank-one e=2 triple-companion certificates passed
EOF

if ! diff -u "$expected_file" "$output_file"; then
  echo "FAIL: SymPy transcript did not match the exact success transcript" >&2
  exit 1
fi

cat "$output_file"
