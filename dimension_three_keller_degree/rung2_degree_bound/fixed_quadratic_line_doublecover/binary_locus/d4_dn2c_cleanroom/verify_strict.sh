#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
keller_python=${KELLER_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}

e7_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-e7.XXXXXX")
e6_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-e6.XXXXXX")
atlas_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-atlas.XXXXXX")
plane_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-plane.XXXXXX")
origin_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-origin.XXXXXX")
overlap_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-overlap.XXXXXX")
optimized_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-opt.XXXXXX")
mutated_script=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-mutant.XXXXXX")
mutated_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn2c-mutant-out.XXXXXX")
trap 'rm -f "$e7_output" "$e6_output" "$atlas_output" "$plane_output" "$origin_output" "$overlap_output" "$optimized_output" "$mutated_script" "$mutated_output"' EXIT HUP INT TERM

cd "$certificate_dir"

"$keller_python" -u derive_e7_matrix.py >"$e7_output"
grep -Fx 'D4_DN2C_E7_MATRIX_KERNEL_PASS' "$e7_output" >/dev/null

"$keller_python" -u derive_e6_projection.py >"$e6_output"
grep -Fx 'D4_DN2C_FULL_LOWER_E6_MATRIX_PASS' "$e6_output" >/dev/null

"$keller_python" -u analyze_e6_elimination.py >"$atlas_output"
grep -Fx 'D4_DN2C_E6_DETERMINANTAL_ELIMINATION_PASS' "$atlas_output" >/dev/null

"$keller_python" -u verify_plane_interiors_e5.py >"$plane_output"
grep -Fx 'D4_DN2C_PLANE_INTERIORS_E5_PASS' "$plane_output" >/dev/null

"$keller_python" -u derive_origin_collapse.py >"$origin_output"
grep -Fx 'D4_DN2C_ORIGIN_COLLAPSE_SCAN_PASS' "$origin_output" >/dev/null

"$keller_python" -u derive_overlap_e3.py >"$overlap_output"
grep -Fx 'D4_DN2C_OVERLAP_E3_SYMBOLIC_PASS' "$overlap_output" >/dev/null

if "$keller_python" -O derive_e7_matrix.py >"$optimized_output" 2>&1; then
    echo 'FAIL: optimized Python was accepted' >&2
    exit 1
fi
grep -F 'FAIL: assertions disabled' "$optimized_output" >/dev/null

sed 's/constant\[row_by_exponent\[(3, 0, 3)\]\] + 6 \* a\*\*2/constant[row_by_exponent[(3, 0, 3)]] + 5 * a**2/' \
    derive_e6_projection.py >"$mutated_script"
if cmp -s derive_e6_projection.py "$mutated_script"; then
    echo 'FAIL: E6 mutation did not alter the script' >&2
    exit 1
fi
if "$keller_python" "$mutated_script" >"$mutated_output" 2>&1; then
    echo 'FAIL: mutated E6 coefficient was accepted' >&2
    exit 1
fi
grep -F 'AssertionError' "$mutated_output" >/dev/null

sed 's/assert common_after_e3 == 0/assert common_after_e3 == 1/' \
    derive_overlap_e3.py >"$mutated_script"
if "$keller_python" "$mutated_script" >"$mutated_output" 2>&1; then
    echo 'FAIL: mutated E3 contradiction was accepted' >&2
    exit 1
fi
grep -F 'AssertionError' "$mutated_output" >/dev/null

printf '%s\n' 'D4_DN2C_CLEANROOM_STRICT_PASS'
