#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch=$(mktemp -d "${TMPDIR:-/tmp}/marked-mixed-audit.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

"$audit_dir/verify_marked_mixed_pari_strict.sh" \
    >"$scratch/strict-baseline.log"
printf '%s\n' "PASS: strict PARI baseline accepted"

sed 's/2717908992/2717908993/' \
    "$audit_dir/verify_marked_mixed_pari.gp" >"$scratch/forged.gp"
if /opt/homebrew/bin/gp -q -s 256M "$scratch/forged.gp" \
    >"$scratch/forged-gp.log" 2>&1; then
    printf '%s\n' "FAIL: forged distinct-orbit E6 minor was accepted"
    exit 1
fi
printf '%s\n' "PASS: forged distinct-orbit E6 minor rejected"

fake_gp="$scratch/fake-gp"
printf '%s\n' '#!/bin/sh' \
    'printf "%s\n" "PASS R=xq raw E7: complete five-gauge/three-normal kernel and exact quotient" "PASS R=x(p-q) raw E7: complete five-gauge/three-normal kernel and exact quotient" "PASS R=xq E6/E5: complete constant-pivot converses, including d=0, and det L=0" "PASS R=x(p-q) E6/E5: complete constant-pivot converses, including d=0, and det L=0" "ALL HOSTILE PARI/GP MARKED-MIXED AUDIT CHECKS PASSED" "forged diagnostic"' \
    >"$fake_gp"
chmod +x "$fake_gp"
if GP_BIN="$fake_gp" "$audit_dir/verify_marked_mixed_pari_strict.sh" \
    >"$scratch/fake-transcript.log" 2>&1; then
    printf '%s\n' "FAIL: strict wrapper accepted an extra diagnostic"
    exit 1
fi
printf '%s\n' "PASS: strict wrapper rejected an extra diagnostic"
printf '%s\n' "ALL MARKED-MIXED HOSTILE FAIL-CLOSED TESTS PASSED"
