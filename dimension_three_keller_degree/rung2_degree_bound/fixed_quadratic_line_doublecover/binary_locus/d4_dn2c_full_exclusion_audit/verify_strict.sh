#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
binary_dir=$(CDPATH= cd -- "$audit_dir/.." && pwd)
contact_dir="$binary_dir/d4_dn2c_full_rebuild"
primary_dir="$binary_dir/d4_dn2c_full_descent"
pari_dir="$binary_dir/d4_dn2c_pari_lower"
gp_bin=${KELLER_PARI_GP:-gp}

contact_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-audit-contact.XXXXXX")
primary_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-audit-primary.XXXXXX")
pari_contact_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-audit-pari-contact.XXXXXX")
scope_mutant=$(mktemp "${TMPDIR:-/tmp}/dn2c-audit-scope.XXXXXX")
contact_mutant=$(mktemp "${TMPDIR:-/tmp}/dn2c-audit-contact-mutant.XXXXXX")
contact_mutant_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-audit-contact-mutant-out.XXXXXX")
trap 'rm -f "$contact_output" "$primary_output" "$pari_contact_output" "$scope_mutant" "$contact_mutant" "$contact_mutant_output"' EXIT HUP INT TERM

check_scope()
{
  note=$1
  grep -F 'one frozen normalized quartic family only' "$note" >/dev/null ||
    return 1
  grep -F 'quartic-wide degree bound.' "$note" >/dev/null || return 1
  grep -F 'Work over \(\mathbb C\).' "$note" >/dev/null || return 1
  grep -F 'F=L(p,q,r)^t+H_2+H_3+H_4,' "$note" >/dev/null || return 1
  grep -F 'H_4=(P,Q,0),\qquad H_3=(U,V,R),\qquad H_2=(A,B,T),' \
    "$note" >/dev/null || return 1
  grep -F 'For a Keller map, \(\det L\) is its nonzero constant Jacobian.' \
    "$note" >/dev/null || return 1
  grep -F 'No quartic Keller counterexample has this frozen `D4-DN-2C` binary top' \
    "$note" >/dev/null || return 1
  if grep -F 'all quartic Keller maps' "$note" >/dev/null; then
    return 1
  fi
  if grep -F 'universal degree bound' "$note" >/dev/null; then
    return 1
  fi
  return 0
}

# Frozen atlas, primary descent (which itself invokes the direct lower PARI
# replay), and the independent direct-PARI contact-exhaustiveness audit.
sh "$contact_dir/verify_strict.sh" >"$contact_output" 2>&1
grep -Fx 'D4_DN2C_FULL_REBUILD_STRICT_PASS' "$contact_output" >/dev/null
printf '%s\n' 'AUDIT_STAGE_CONTACT_SYMPY_PASS'

sh "$primary_dir/verify_strict.sh" >"$primary_output" 2>&1
grep -Fx 'D4_DN2C_FULL_DESCENT_STRICT_PASS' "$primary_output" >/dev/null
grep -Fx 'D4_DN2C_DIRECT_PARI_LOWER_STRICT_PASS' "$primary_output" >/dev/null
grep -Fx 'D4_DN2C_DIRECT_PARI_CONTACT_ATLAS_STRICT_PASS' \
  "$primary_output" >/dev/null
grep -Fx 'D4_DN2C_DIRECT_PARI_FULL_FAMILY_STRICT_PASS' \
  "$primary_output" >/dev/null
printf '%s\n' 'AUDIT_STAGE_PRIMARY_AND_SOURCE_PARI_PASS'

"$gp_bin" -s 536000000 -q "$audit_dir/verify_contact_exhaustiveness_pari.gp" \
  >"$pari_contact_output" 2>&1
if grep -Eq 'FAIL:|\*\*\*|syntax error|user error|at top-level|in function|sorry,' \
    "$pari_contact_output"; then
  cat "$pari_contact_output"
  exit 1
fi
grep -Fx 'D4_DN2C_CONTACT_EXHAUSTIVENESS_DIRECT_PARI_PASS' \
  "$pari_contact_output" >/dev/null
printf '%s\n' 'AUDIT_STAGE_SECOND_PARI_CONTACT_PASS'

# Documentation-to-certificate consistency.  These are the signs that were
# missing in the first hostile read.
note="$primary_dir/NOTE.md"
check_scope "$note"
grep -F 'over \(\mathbb C(k)\)' "$note" >/dev/null
! grep -F 'over \(K(k)\)' "$note" >/dev/null
grep -F '&+3v_1^2-12v_1v_2+18v_1v_3\\' "$note" >/dev/null
grep -F '&+8t_2v_1-16t_2v_2+24t_2v_3\\' "$note" >/dev/null
grep -F '&+9u_3v_1-18u_3v_2+27u_3v_3\\' "$note" >/dev/null
grep -F '&+24v_2^2-72v_2v_3+54v_3^2 .' "$note" >/dev/null
grep -F 'second factor is computed exactly in the verifier' "$note" >/dev/null
grep -F 'assert H_b_denominator == 1' \
  "$primary_dir/verify_full_exclusion_sympy.py" >/dev/null
grep -F 'assert H_a_denominator == 1' \
  "$primary_dir/verify_full_exclusion_sympy.py" >/dev/null
grep -F 'assert actual_e5_ideal == expected_e5_ideal' \
  "$primary_dir/verify_full_exclusion_sympy.py" >/dev/null
printf '%s\n' 'AUDIT_STAGE_SCOPE_AND_TRANSCRIPTION_PASS'

# Required-failure mutation 1: turn the family-only scope into a quartic-wide
# claim.  The audit must reject the mutated note.
sed 's/one frozen normalized quartic family only/all quartic Keller maps/' \
  "$note" >"$scope_mutant"
grep -F 'all quartic Keller maps' "$scope_mutant" >/dev/null
if check_scope "$scope_mutant"; then
  echo 'FAIL: quartic-wide scope mutation was accepted' >&2
  exit 1
fi
printf '%s\n' 'AUDIT_STAGE_SCOPE_MUTATION_REJECTED'

# Required-failure mutation 2: corrupt the independently reconstructed contact
# quadratic.  This guards the atlas-exhaustiveness bridge, not only a marker.
sed 's/f0=8/f0=7/' \
  "$audit_dir/verify_contact_exhaustiveness_pari.gp" >"$contact_mutant"
grep -F 'f0=7*aa^2' "$contact_mutant" >/dev/null
if cmp -s "$audit_dir/verify_contact_exhaustiveness_pari.gp" "$contact_mutant"; then
  echo 'FAIL: contact mutation did not alter the PARI script' >&2
  exit 1
fi
if "$gp_bin" -s 536000000 -q "$contact_mutant" \
    >"$contact_mutant_output" 2>&1; then
  echo 'FAIL: corrupted contact quadratic unexpectedly passed' >&2
  exit 1
fi
grep -F 'FAIL: contact quadratic row 4' "$contact_mutant_output" >/dev/null
if grep -F 'D4_DN2C_CONTACT_EXHAUSTIVENESS_DIRECT_PARI_PASS' \
    "$contact_mutant_output" >/dev/null; then
  echo 'FAIL: contact mutant reached terminal marker' >&2
  exit 1
fi
printf '%s\n' 'AUDIT_STAGE_CONTACT_MUTATION_REJECTED'

printf '%s\n' 'D4_DN2C_FULL_EXCLUSION_HOSTILE_AUDIT_STRICT_PASS'
