#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch=$(mktemp -d "${TMPDIR:-/tmp}/unmarked-c3-hostile.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

sed 's|16/3\*l32\^2|17/3*l32^2|' \
    "$audit_dir/verify_hostile_pari.gp" >"$scratch/bad-e4.gp"
if cmp -s "$audit_dir/verify_hostile_pari.gp" "$scratch/bad-e4.gp"; then
    printf '%s\n' "FAIL: final E4 mutation was not applied"
    exit 1
fi
if /opt/homebrew/bin/gp -q -s 192M "$scratch/bad-e4.gp" \
    >"$scratch/bad-e4.log" 2>&1; then
    printf '%s\n' "FAIL: corrupted final E4 pivot was accepted"
    exit 1
fi
printf '%s\n' "PASS: corrupted final E4 pivot rejected"

sed 's|Rm3=x\*(p+3\*q)|Rm3=x*(p+4*q)|' \
    "$audit_dir/verify_hostile_pari.gp" >"$scratch/bad-sign.gp"
if cmp -s "$audit_dir/verify_hostile_pari.gp" "$scratch/bad-sign.gp"; then
    printf '%s\n' "FAIL: c=-3 mutation was not applied"
    exit 1
fi
if /opt/homebrew/bin/gp -q -s 192M "$scratch/bad-sign.gp" \
    >"$scratch/bad-sign.log" 2>&1; then
    printf '%s\n' "FAIL: corrupted c=-3 symmetry was accepted"
    exit 1
fi
printf '%s\n' "PASS: corrupted c=-3 symmetry rejected"

sed 's|-6\*AA+3\*BB+48\*ee+16\*ww|-5*AA+3*BB+48*ee+16*ww|' \
    "$audit_dir/verify_hostile_pari.gp" >"$scratch/bad-resonance.gp"
if cmp -s "$audit_dir/verify_hostile_pari.gp" "$scratch/bad-resonance.gp"; then
    printf '%s\n' "FAIL: resonance mutation was not applied"
    exit 1
fi
if /opt/homebrew/bin/gp -q -s 192M "$scratch/bad-resonance.gp" \
    >"$scratch/bad-resonance.log" 2>&1; then
    printf '%s\n' "FAIL: corrupted resonance divisor was accepted"
    exit 1
fi
printf '%s\n' "PASS: corrupted resonance divisor rejected"

"$audit_dir/verify_hostile_pari_strict.sh" >"$scratch/baseline.log"
printf '%s\n' "PASS: strict hostile baseline accepted"

fake_gp="$scratch/fake-gp"
printf '%s\n' '#!/bin/sh' \
    'printf "%s\n" "ALL HOSTILE UNMARKED c^2=9 PARI AUDIT CHECKS PASSED" "forged extra line"' \
    >"$fake_gp"
chmod +x "$fake_gp"
if GP_BIN="$fake_gp" "$audit_dir/verify_hostile_pari_strict.sh" \
    >"$scratch/fake.log" 2>&1; then
    printf '%s\n' "FAIL: strict wrapper accepted a forged extra line"
    exit 1
fi
printf '%s\n' "PASS: strict wrapper rejected a forged extra line"
printf '%s\n' "ALL HOSTILE UNMARKED c^2=9 FAIL-CLOSED TESTS PASSED"
