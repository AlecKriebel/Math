#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_file=${1:-"$script_dir/verify_a0_external_pari.gp"}
output_file=$(mktemp "${TMPDIR:-/tmp}/rankone-a0-external.XXXXXX")
expected_file=$(mktemp "${TMPDIR:-/tmp}/rankone-a0-external-expected.XXXXXX")
trap 'rm -f "$output_file" "$expected_file"' EXIT HUP INT TERM

if ! gp -fq "$gp_file" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

cat >"$expected_file" <<'EOF'
External PARI audit: raw E7 and effective gauges
PASS raw E7: rank 8/nullity 18 and exactly four independent legal gauges
External PARI audit: A=0 E6 branch cover
PASS A=0 E6: w4=w5=0 and w3*w1=w3*(w3-w2)=0 exhaust the cover
External PARI audit: w3-open and origin
PASS w3-open and origin: all D, r=a3, and square rank drops close
External PARI audit: q-shear and xz axis
PASS xz axis: shear is legal and every E5 pivot drop is rebuilt
External PARI audit: xy axis and complete h/G/factor tree
PASS xy axis: h=0, both E4 factors, G split, and every intersection close
ALL EXTERNAL PARI A=0 HOSTILE CHECKS PASSED
EOF

if ! diff -u "$expected_file" "$output_file"; then
  echo "FAIL: external PARI transcript did not match exactly" >&2
  exit 1
fi

cat "$output_file"
