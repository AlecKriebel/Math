#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_file=${1:-"$script_dir/verify_a0_pari.gp"}
output_file=$(mktemp "${TMPDIR:-/tmp}/rankone-a0-pari.XXXXXX")
expected_file=$(mktemp "${TMPDIR:-/tmp}/rankone-a0-pari-expected.XXXXXX")
trap 'rm -f "$output_file" "$expected_file"' EXIT HUP INT TERM

if ! gp -fq "$gp_file" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

if grep -Fq "***" "$output_file" || grep -Fq "FAIL:" "$output_file"; then
  cat "$output_file"
  echo "FAIL: PARI transcript contains an error diagnostic" >&2
  exit 1
fi

cat >"$expected_file" <<'EOF'
PARI audit A=0: w3-open branch
PASS A=0,w3-open: tail collapse and all D/a3 charts
PARI audit A=0: origin, including the a3 rank drop
PASS A=0 origin: literal E5 and both a3 charts
PARI audit A=0: legal stabilizer/gauge reduction and xz axis
PASS A=0 xz axis: legal reduction and every rank-drop chart
PARI audit A=0: xy axis and full factor tree
PASS A=0 xy axis: every E5/E4 rank drop and both descendants
all independent PARI A=0 certificates passed
EOF

if ! diff -u "$expected_file" "$output_file"; then
  echo "FAIL: PARI transcript did not match the exact success transcript" >&2
  exit 1
fi

cat "$output_file"
