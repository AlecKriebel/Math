#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
binary_locus_dir=$(CDPATH= cd -- "$certificate_dir/.." && pwd)
gp_bin=${KELLER_PARI_GP:-gp}

contact_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn3-contact.XXXXXX")
hostile_contact_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn3-contact-hostile.XXXXXX")
lower_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn3-lower.XXXXXX")
mutated_script=$(mktemp "${TMPDIR:-/tmp}/d4-dn3-interior-mutated.XXXXXX")
mutated_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn3-interior-mutated-out.XXXXXX")
trap 'rm -f "$contact_output" "$hostile_contact_output" "$lower_output" "$mutated_script" "$mutated_output"' EXIT HUP INT TERM

if ! sh "$binary_locus_dir/d4_dn3_full_rebuild/verify_strict.sh" \
    >"$contact_output" 2>&1; then
    cat "$contact_output"
    exit 1
fi
cat "$contact_output"
grep -Fx "D4_DN3_FULL_E6_ELIMINATION_PASS_TWO_PLANES_18_LOWER" \
    "$contact_output" >/dev/null
grep -Fx "D4_DN3_PARI_FULL_18_LOWER_ATLAS_PASS" \
    "$contact_output" >/dev/null
grep -Fx "D4_DN3_FULL_REBUILD_STRICT_PASS" "$contact_output" >/dev/null

if ! sh "$binary_locus_dir/d4_dn3_full_rebuild/verify_hostile.sh" \
    >"$hostile_contact_output" 2>&1; then
    cat "$hostile_contact_output"
    exit 1
fi
cat "$hostile_contact_output"
grep -Fx "D4_DN3_HOSTILE_AUDIT_STRICT_PASS" \
    "$hostile_contact_output" >/dev/null

if ! sh "$binary_locus_dir/d4_dn3_full_exclusion_audit/verify_strict.sh" \
    >"$lower_output" 2>&1; then
    cat "$lower_output"
    exit 1
fi
cat "$lower_output"
grep -Fx "D4_DN3_CLEANROOM_FULL_EXCLUSION_STRICT_PASS" \
    "$lower_output" >/dev/null

# Mutation guard for the independent transverse-plane identity.  The lower
# boundary wrapper has its own two required-failure mutations.
sed 's/expectedp=3\*(rt-2)/expectedp=4*(rt-2)/' \
    "$certificate_dir/verify_interior_e5_pari.gp" >"$mutated_script"
if cmp -s "$certificate_dir/verify_interior_e5_pari.gp" "$mutated_script"; then
    echo "FAIL: transverse PARI mutation did not change the script" >&2
    exit 1
fi
if "$gp_bin" -s 268000000 -q "$mutated_script" \
    >"$mutated_output" 2>&1; then
    echo "FAIL: mutated transverse obstruction unexpectedly passed" >&2
    cat "$mutated_output" >&2
    exit 1
fi
grep -F "FAIL: [p^3 r^2] E5" "$mutated_output" >/dev/null

printf '%s\n' "D4_DN3_FULL_FAMILY_EXCLUSION_STRICT_PASS"
