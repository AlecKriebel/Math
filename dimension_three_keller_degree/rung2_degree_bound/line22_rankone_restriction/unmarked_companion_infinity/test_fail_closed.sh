#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch=$(mktemp -d "${TMPDIR:-/tmp}/rankone-infinity.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

if /usr/bin/python3 -O "$script_dir/verify_unmarked_infinity_sympy.py" \
    >"$scratch/optimized.log" 2>&1; then
    printf '%s\n' "FAIL: optimized Python was accepted"
    exit 1
fi
printf '%s\n' "PASS: optimized Python rejected"

sed 's/raw_minor == 1709960483517235200/raw_minor == 1709960483517235201/' \
    "$script_dir/verify_unmarked_infinity_sympy.py" >"$scratch/forged.py"
if /usr/bin/python3 "$scratch/forged.py" >"$scratch/forged-python.log" 2>&1; then
    printf '%s\n' "FAIL: forged SymPy minor was accepted"
    exit 1
fi
printf '%s\n' "PASS: forged SymPy minor rejected"

sed 's/4831838208,\"E6 constant forcing minor\"/4831838209,\"E6 constant forcing minor\"/' \
    "$script_dir/verify_unmarked_infinity_pari.gp" >"$scratch/forged.gp"
if /opt/homebrew/bin/gp -q "$scratch/forged.gp" \
    >"$scratch/forged-gp.log" 2>&1; then
    printf '%s\n' "FAIL: forged PARI minor was accepted"
    exit 1
fi
printf '%s\n' "PASS: forged PARI minor rejected"

"$script_dir/verify_unmarked_infinity_pari_strict.sh" \
    >"$scratch/strict-baseline.log"
printf '%s\n' "PASS: strict PARI baseline accepted"

fake_gp="$scratch/fake-gp"
printf '%s\n' '#!/bin/sh' \
    'printf "%s\n" "ALL UNMARKED COMPANION-INFINITY PARI CERTIFICATES PASSED" "forged diagnostic"' \
    >"$fake_gp"
chmod +x "$fake_gp"
if GP_BIN="$fake_gp" "$script_dir/verify_unmarked_infinity_pari_strict.sh" \
    >"$scratch/fake-transcript.log" 2>&1; then
    printf '%s\n' "FAIL: strict wrapper accepted an extra diagnostic"
    exit 1
fi
printf '%s\n' "PASS: strict wrapper rejected an extra diagnostic"
printf '%s\n' "ALL UNMARKED COMPANION-INFINITY FAIL-CLOSED TESTS PASSED"
