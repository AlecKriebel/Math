#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch=$(mktemp -d "${TMPDIR:-/tmp}/rankone-c3.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

if /usr/bin/python3 -O "$script_dir/verify_resonance_c3_sympy.py" \
    >"$scratch/optimized.log" 2>&1; then
    printf '%s\n' "FAIL: optimized Python was accepted"
    exit 1
fi
printf '%s\n' "PASS: optimized Python rejected"

sed 's/-1039973956284579840/-1039973956284579841/' \
    "$script_dir/verify_resonance_c3_sympy.py" >"$scratch/forged.py"
if /usr/bin/python3 "$scratch/forged.py" \
    >"$scratch/forged-python.log" 2>&1; then
    printf '%s\n' "FAIL: forged SymPy minor was accepted"
    exit 1
fi
printf '%s\n' "PASS: forged SymPy minor rejected"

sed 's|16/3\*l7\^2|17/3*l7^2|' \
    "$script_dir/verify_resonance_c3_pari.gp" >"$scratch/forged.gp"
if /opt/homebrew/bin/gp -q -s 128M "$scratch/forged.gp" \
    >"$scratch/forged-gp.log" 2>&1; then
    printf '%s\n' "FAIL: forged PARI E4 pivot was accepted"
    exit 1
fi
printf '%s\n' "PASS: forged PARI E4 pivot rejected"

"$script_dir/verify_resonance_c3_pari_strict.sh" \
    >"$scratch/strict-baseline.log"
printf '%s\n' "PASS: strict PARI baseline accepted"

fake_gp="$scratch/fake-gp"
printf '%s\n' '#!/bin/sh' \
    'printf "%s\n" "ALL UNMARKED c=3 RESONANCE PARI CERTIFICATES PASSED" "forged diagnostic"' \
    >"$fake_gp"
chmod +x "$fake_gp"
if GP_BIN="$fake_gp" "$script_dir/verify_resonance_c3_pari_strict.sh" \
    >"$scratch/fake-transcript.log" 2>&1; then
    printf '%s\n' "FAIL: strict wrapper accepted an extra diagnostic"
    exit 1
fi
printf '%s\n' "PASS: strict wrapper rejected an extra diagnostic"
printf '%s\n' "ALL UNMARKED c=3 RESONANCE FAIL-CLOSED TESTS PASSED"
