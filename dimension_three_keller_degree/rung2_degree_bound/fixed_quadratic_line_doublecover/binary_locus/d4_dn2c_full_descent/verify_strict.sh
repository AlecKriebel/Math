#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${KELLER_DN2C_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
baseline_output=$(mktemp)
optimized_output=$(mktemp)
interior_mutant=$(mktemp "$certificate_dir/.dn2c-interior-mutant.XXXXXX")
interior_output=$(mktemp)
origin_mutant=$(mktemp "$certificate_dir/.dn2c-origin-mutant.XXXXXX")
origin_output=$(mktemp)
pari_output=$(mktemp)
trap 'rm -f "$baseline_output" "$optimized_output" "$interior_mutant" "$interior_output" "$origin_mutant" "$origin_output" "$pari_output"' EXIT HUP INT TERM

cd "$certificate_dir"

"$python_bin" -u verify_full_exclusion_sympy.py | tee "$baseline_output"
grep -Fx "D4_DN2C_INTERIORS_E5_PASS_NO_COMMON_ZERO" "$baseline_output" >/dev/null
grep -Fx "D4_DN2C_INTERSECTION_PASS_E5_AB_SPLIT_E4_E3_DETL" "$baseline_output" >/dev/null
grep -Fx "D4_DN2C_ORIGIN_PASS_ALL_SIX_COLLAPSE_PLANE_MOH_EXIT" "$baseline_output" >/dev/null
grep -Fx "D4_DN2C_FULL_EXCLUSION_SYMPY_PASS" "$baseline_output" >/dev/null

if "$python_bin" -O verify_full_exclusion_sympy.py >"$optimized_output" 2>&1; then
    echo "FAIL: optimized Python was accepted" >&2
    exit 1
fi
grep -F "FAIL: assertions disabled" "$optimized_output" >/dev/null

# Required-failure mutation 1: corrupt the certified first interior E5
# denominator.  The exact-coefficient assertion must reject it.
sed 's/sp.Integer(162)/sp.Integer(161)/' \
    verify_full_exclusion_sympy.py >"$interior_mutant"
grep -F "sp.Integer(161)" "$interior_mutant" >/dev/null
if "$python_bin" "$interior_mutant" >"$interior_output" 2>&1; then
    cat "$interior_output"
    echo "FAIL: interior coefficient mutation was accepted" >&2
    exit 1
fi
if grep -F "D4_DN2C_FULL_EXCLUSION_SYMPY_PASS" "$interior_output" >/dev/null; then
    echo "FAIL: interior mutant reached terminal marker" >&2
    exit 1
fi
grep -F "AssertionError" "$interior_output" >/dev/null

# Required-failure mutation 2: corrupt the origin square.  This independently
# checks that the all-six collapse is not marker-only.
sed 's/origin_p3r + 3 \* base.bc\[4\] \*\* 2/origin_p3r + 5 * base.bc[4] ** 2/' \
    verify_full_exclusion_sympy.py >"$origin_mutant"
grep -F "origin_p3r + 5 * base.bc[4] ** 2" "$origin_mutant" >/dev/null
if "$python_bin" "$origin_mutant" >"$origin_output" 2>&1; then
    cat "$origin_output"
    echo "FAIL: origin-square mutation was accepted" >&2
    exit 1
fi
if grep -F "D4_DN2C_FULL_EXCLUSION_SYMPY_PASS" "$origin_output" >/dev/null; then
    echo "FAIL: origin mutant reached terminal marker" >&2
    exit 1
fi
grep -F "AssertionError" "$origin_output" >/dev/null

# Independent direct PARI/GP reconstruction.  This rebuilds the raw E7
# kernel, the complete all-18-variable E6 contact atlas, every lower chart,
# and the adjugate verification of the origin plane normalization.  Its
# wrapper also contains three required-failure mutations.
if ! sh "$certificate_dir/../d4_dn2c_pari_lower/verify_strict.sh" \
    >"$pari_output" 2>&1; then
    cat "$pari_output"
    echo "FAIL: independent direct PARI lower descent failed" >&2
    exit 1
fi
cat "$pari_output"
grep -Fx "D4_DN2C_DIRECT_PARI_FULL_FAMILY_STRICT_PASS" \
    "$pari_output" >/dev/null

echo "D4_DN2C_FULL_DESCENT_STRICT_PASS"
