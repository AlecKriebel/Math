#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
rung_dir=$(CDPATH= cd -- "$audit_dir/../.." && pwd)

fail() {
    printf '%s\n' "FAIL: $*" >&2
    exit 1
}

[ -z "${PYTHONOPTIMIZE:-}" ] ||
  fail "caller supplied PYTHONOPTIMIZE; assertion-based legacy checks disabled"

check_hash() {
    expected=$1
    file=$2
    actual=$(shasum -a 256 "$file" | awk '{print $1}')
    [ "$actual" = "$expected" ] || fail "hash mismatch: $file"
}

check_hash \
  41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d \
  "$audit_dir/../FROZEN_TAXONOMY_v1.md"
check_hash \
  5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23 \
  "$audit_dir/../frozen_manifest_v1.json"
check_hash \
  11d3d595e07343b322376d2c1411496498ef63e56e4955bda03a30203c01a530 \
  "$audit_dir/BLINDED_DERIVATION.md"
check_hash \
  c6592cad695183a6d276c9ff83fbe336d051d5549f40ae17d2394dc9280ee6ac \
  "$audit_dir/verify_blinded_bridge_sympy.py"
check_hash \
  8bb253a2a38a6ded034eeb3080702c1f8ab161c837a1951db28051f23a2bee54 \
  "$audit_dir/verify_blinded_bridge_pure.py"

sympy_output=$(/usr/bin/python3 "$audit_dir/verify_blinded_bridge_sympy.py")
expected_sympy='PASS: five conic-pencil charts and composite boundary
  P111: D2 rank/kernel/cokernel=4/2/6; D3=10/0/5
  P11_1: D2 rank/kernel/cokernel=4/2/6; D3=8/2/7
  P2_1: D2 rank/kernel/cokernel=4/2/6; D3=10/0/5
  P21: D2 rank/kernel/cokernel=4/2/6; D3=8/2/7
  P3: D2 rank/kernel/cokernel=4/2/6; D3=10/0/5
PASS: polynomial 45-coefficient frozen-pivot map'
[ "$sympy_output" = "$expected_sympy" ] ||
  fail "unexpected blinded SymPy transcript"

pure_output=$(/usr/bin/python3 "$audit_dir/verify_blinded_bridge_pure.py")
expected_pure='PASS P111: D2 rank/kernel/cokernel=4/2/6; D3=10/0/5
PASS P11_1: D2 rank/kernel/cokernel=4/2/6; D3=8/2/7
PASS P2_1: D2 rank/kernel/cokernel=4/2/6; D3=10/0/5
PASS P21: D2 rank/kernel/cokernel=4/2/6; D3=8/2/7
PASS P3: D2 rank/kernel/cokernel=4/2/6; D3=10/0/5
PASS: dependency-free Fraction/RREF replay of all exact obstruction maps'
[ "$pure_output" = "$expected_pure" ] ||
  fail "unexpected blinded dependency-free transcript"

check_hash \
  0604cba75bf113a149c8eb82e8dcfc9d2cdda8fd7c43c669b3f4a836e97d20c9 \
  "$audit_dir/bridge_exact_data_sympy.json"

cd "$rung_dir"

/usr/bin/python3 verify_line22_doubleline_sympy.py >/dev/null
/usr/bin/python3 audit_quadratic_component_exit/verify_quadratic_component_exit_exact.py >/dev/null

/usr/bin/python3 verify_line_22_finite_outer_critical_sympy.py >/dev/null
./run_verify_line_22_finite_outer_critical_pari.sh >/dev/null
/usr/bin/python3 verify_line_22_fg_resonance_sympy.py >/dev/null
./run_verify_line_22_fg_resonance_pari.sh >/dev/null
/usr/bin/python3 audit_line22_fg/audit_fg_chart_exact.py >/dev/null
/usr/bin/python3 audit_line22_fg/audit_outer_infinity.py >/dev/null

(
  cd line22_marked_critical_infinity
  /usr/bin/python3 verify_line22_marked_critical_infinity_sympy.py >/dev/null
  ./verify_line22_marked_critical_infinity_pari_strict.sh >/dev/null
  /usr/bin/python3 audit_hostile/audit_exact_reconstruct.py >/dev/null
)

(
  cd line22_outer_infinity_remaining
  /usr/bin/python3 verify_line22_outer_infinity_remaining_sympy.py >/dev/null
  ./verify_line22_outer_infinity_remaining_pari_strict.sh >/dev/null
)

(
  cd line22_companion_infinity
  /usr/bin/python3 verify_companion_infinity_sympy.py >/dev/null
  ./verify_companion_infinity_pari_strict.sh >/dev/null
  /usr/bin/python3 audit_hostile/audit_orbits_and_gauges_sympy.py >/dev/null
  ./audit_hostile/verify_resonance_pari_strict.sh >/dev/null
)

(
  cd line22_rankone_restriction
  /usr/bin/python3 verify_rankone_restriction_sympy.py >/dev/null
  ./verify_rankone_restriction_pari_strict.sh >/dev/null
  /usr/bin/python3 audit_hostile/audit_rankone_exact.py >/dev/null
)

(
  cd line22_rankone_restriction/unmarked_triple_c0
  /usr/bin/python3 verify_unmarked_triple_sympy.py >/dev/null
  ./audit_hostile/verify_hostile_pari_strict.sh >/dev/null
)

(
  cd line22_rankone_restriction/marked_mixed_orbits
  /usr/bin/python3 verify_marked_mixed_sympy.py >/dev/null
  ./audit_hostile/verify_marked_mixed_pari_strict.sh >/dev/null
  ./audit_hostile/r_xq/verify_r_xq_pari_strict.sh >/dev/null
)

(
  cd line22_rankone_restriction/marked_triple_orbit
  ./verify_marked_triple_sympy_strict.sh >/dev/null
  ./audit_hostile/independent/verify_marked_triple_pari_strict.sh >/dev/null
)

(
  cd line22_rankone_restriction/unmarked_resonance_c3
  /usr/bin/python3 verify_resonance_c3_sympy.py >/dev/null
  ./verify_resonance_c3_pari_strict.sh >/dev/null
  ./audit_hostile/verify_hostile_pari_strict.sh >/dev/null
)

(
  cd line22_rankone_restriction/unmarked_companion_infinity
  /usr/bin/python3 verify_unmarked_infinity_sympy.py >/dev/null
  ./verify_unmarked_infinity_pari_strict.sh >/dev/null
  /usr/bin/python3 audit_hostile/verify_unmarked_infinity_pure.py >/dev/null
  ./audit_hostile/verify_hostile_strict.sh >/dev/null
)

printf '%s\n' \
  'PASS: strict post-freeze Q2-E0-A2-B2-D1-N2 bridge and full legacy replay'
