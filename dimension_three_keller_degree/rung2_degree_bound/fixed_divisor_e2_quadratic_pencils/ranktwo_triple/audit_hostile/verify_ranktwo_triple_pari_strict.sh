#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=/opt/homebrew/bin/gp
output_file=$(mktemp "${TMPDIR:-/tmp}/e2-ranktwo-triple-pari.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if [ ! -x "$gp_bin" ]; then
  echo "FAIL: expected PARI/GP executable is unavailable at $gp_bin" >&2
  exit 1
fi

if ! "$gp_bin" -s 1000000000 -fq \
  "$audit_dir/verify_ranktwo_triple_pari.gp" >"$output_file" 2>&1; then
  cat "$output_file"
  exit 1
fi

cat "$output_file"

if grep -E '\*\*\*|FAIL:|syntax error|incorrect type|user error|stack overflow|bug in PARI' \
  "$output_file" >/dev/null; then
  echo "FAIL: PARI/GP emitted an error diagnostic" >&2
  exit 1
fi

for marker in \
  'PASS raw E7: rank 8/nullity 18; five legal gauges plus thirteen normals form the full kernel' \
  'PASS E6: constant pivot makes w3=w5=0 and the K/M split specialization-safe' \
  'PASS K!=0 E5: polynomial left syzygies and exact resultant force w1=w2=0, leaving only S=0' \
  'PASS aligned nonresonant K!=0: E5 localization is exactly (3A-8w4)(3A-4w4), and E4 forces det(L)=0' \
  'PASS 9A=2K: nonzero ends are excluded by z4 after y/z symmetry; the freshly solved aligned rank-drop chart also forces det(L)=0' \
  'PASS 9A=K: B3-localized solve forces det(L)=0; y/z symmetry covers B1-only, and the zero pair lies in the nonresonant aligned chart' \
  'PASS K=0,A!=0: six E5 compatibilities leave only B2, and a fresh A-localized solve zeros four entries of L' \
  'PASS K=A=0 open chart: necessary tail parametrization and an exact localized E5 solve give 4*s^4/27' \
  'PASS K=A=0 rank drops: C=0 is global; r=0 splits safely into B3!=0 cross-multiplied E5 and B3=0 fresh E4 charts' \
  'PASS terminal chart: global literal E5 rows split on a4, and both branches force l32=l33 without the unsafe B1 localization' \
  'ALL HOSTILE PARI/GP RANK-TWO e=2 TRIPLE-COMPANION CHECKS PASSED'
do
  if [ "$(grep -Fxc "$marker" "$output_file")" -ne 1 ]; then
    echo "FAIL: required unique success marker missing: $marker" >&2
    exit 1
  fi
done
