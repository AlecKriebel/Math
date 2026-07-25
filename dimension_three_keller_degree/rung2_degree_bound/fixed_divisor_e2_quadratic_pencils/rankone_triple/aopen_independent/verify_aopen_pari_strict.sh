#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_file=${1:-"$script_dir/verify_aopen_pari.gp"}
output_file=$(mktemp "${TMPDIR:-/tmp}/aopen-pari.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if ! gp -fq "$gp_file" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

if grep -Fq "***" "$output_file" || grep -Fq "FAIL:" "$output_file"; then
  cat "$output_file"
  echo "FAIL: PARI transcript contains an error diagnostic" >&2
  exit 1
fi

for marker in \
  "PASS normalization and exact four-factor branch cover" \
  "PASS w3=0: W=0 factors the determinant; W!=0 has a literal E4 contradiction" \
  "PASS equal branch: only plus/minus resonances survive; every other leaf has det L=0" \
  "PASS plus resonance: all open and aligned rank-drop charts close" \
  "PASS minus resonance: cubic compatibility reaches the equal factor, and every rank drop closes" \
  "PASS all A!=0 branches excluded exactly in PARI/GP"
do
  if ! grep -Fqx "$marker" "$output_file"; then
    cat "$output_file"
    echo "FAIL: missing PARI success marker: $marker" >&2
    exit 1
  fi
done

cat "$output_file"
