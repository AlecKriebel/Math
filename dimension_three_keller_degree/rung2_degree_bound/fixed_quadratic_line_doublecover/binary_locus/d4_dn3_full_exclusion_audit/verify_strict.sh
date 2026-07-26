#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
binary_locus_dir=$(CDPATH= cd -- "$audit_dir/.." && pwd)
python_bin=${KELLER_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
gp_bin=${KELLER_PARI_GP:-gp}

plus_output=$(mktemp)
minus_output=$(mktemp)
intersection_output=$(mktemp)
origin_output=$(mktemp)
optimized_output=$(mktemp)
pari_interior_output=$(mktemp)
trap 'rm -f "$plus_output" "$minus_output" "$intersection_output" "$origin_output" "$optimized_output" "$pari_interior_output"' EXIT HUP INT TERM

run_chart()
{
    sign=$1
    chart=$2
    marker=$3
    output_file=$4
    if ! "$python_bin" "$audit_dir/derive_cleanroom_sympy.py" \
        --sign "$sign" --chart "$chart" >"$output_file" 2>&1; then
        cat "$output_file"
        exit 1
    fi
    grep -Fx "$marker" "$output_file" >/dev/null
    printf '%s\n' "$marker"
}

run_chart plus interior \
    D4_DN3_CLEANROOM_PLUS_INTERIOR_E5_PASS "$plus_output"
run_chart minus interior \
    D4_DN3_CLEANROOM_MINUS_INTERIOR_E5_PASS "$minus_output"
run_chart plus intersection \
    D4_DN3_CLEANROOM_INTERSECTION_DETL_PASS "$intersection_output"
run_chart plus origin \
    D4_DN3_CLEANROOM_ORIGIN_MOH_EXIT_PASS "$origin_output"

if "$python_bin" -O "$audit_dir/derive_cleanroom_sympy.py" \
    --sign plus --chart origin >"$optimized_output" 2>&1; then
    echo "FAIL: optimized clean-room Python unexpectedly passed" >&2
    exit 1
fi
grep -F "FAIL: assertions disabled" "$optimized_output" >/dev/null

if ! "$gp_bin" -s 268000000 -q \
    "$binary_locus_dir/d4_dn3_full_descent/verify_interior_e5_pari.gp" \
    >"$pari_interior_output" 2>&1; then
    cat "$pari_interior_output"
    exit 1
fi
grep -Fx "D4_DN3_TRANSVERSE_E5_PARI_PASS" \
    "$pari_interior_output" >/dev/null
printf '%s\n' "D4_DN3_TRANSVERSE_E5_PARI_PASS"

KELLER_PARI_GP="$gp_bin" \
    "$binary_locus_dir/d4_dn3_full_descent/pari_boundary_audit/verify_strict.sh"

printf '%s\n' "D4_DN3_CLEANROOM_FULL_EXCLUSION_STRICT_PASS"
