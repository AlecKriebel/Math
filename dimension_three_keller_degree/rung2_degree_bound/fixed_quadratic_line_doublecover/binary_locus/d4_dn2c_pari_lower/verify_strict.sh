#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
gp_bin=${KELLER_PARI_GP:-gp}

contact_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-contact.XXXXXX")
plane_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-plane.XXXXXX")
boundary_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-boundary.XXXXXX")
contact_mutant=$(mktemp "${TMPDIR:-/tmp}/dn2c-contact-mutant.XXXXXX")
contact_mutant_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-contact-mutant-out.XXXXXX")
plane_mutant=$(mktemp "${TMPDIR:-/tmp}/dn2c-plane-mutant.XXXXXX")
plane_mutant_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-plane-mutant-out.XXXXXX")
e3_mutant=$(mktemp "${TMPDIR:-/tmp}/dn2c-e3-mutant.XXXXXX")
e3_mutant_output=$(mktemp "${TMPDIR:-/tmp}/dn2c-e3-mutant-out.XXXXXX")
trap 'rm -f "$contact_output" "$plane_output" "$boundary_output" "$contact_mutant" "$contact_mutant_output" "$plane_mutant" "$plane_mutant_output" "$e3_mutant" "$e3_mutant_output"' EXIT HUP INT TERM

if ! "$gp_bin" -s 536000000 -q \
    "$certificate_dir/explore_contact_atlas_pari.gp" \
    >"$contact_output" 2>&1; then
  cat "$contact_output"
  exit 1
fi
if grep -Eq 'FAIL:|\*\*\*|syntax error|user error|at top-level|in function' \
    "$contact_output"; then
  cat "$contact_output"
  exit 1
fi
grep -Fx "D4_DN2C_PARI_E7_KERNEL_PASS_0_2_4" \
    "$contact_output" >/dev/null
grep -Fx "D4_DN2C_PARI_E6_RADICAL_TWO_PLANES_PASS" \
    "$contact_output" >/dev/null
grep -Fx "D4_DN2C_DIRECT_PARI_CONTACT_ATLAS_PASS" \
    "$contact_output" >/dev/null

if ! "$gp_bin" -s 536000000 -q "$certificate_dir/explore_plane_pari.gp" \
    >"$plane_output" 2>&1; then
  cat "$plane_output"
  exit 1
fi
if grep -Eq 'FAIL:|\*\*\*|syntax error|user error|at top-level|in function' \
    "$plane_output"; then
  cat "$plane_output"
  exit 1
fi
grep -Fx "D4_DN2C_PLUS_PLANE_E5_PROBE_PASS" "$plane_output" >/dev/null
grep -Fx "D4_DN2C_TRANSVERSE_INTERIORS_E5_EXCLUDED" "$plane_output" >/dev/null

if ! "$gp_bin" -s 536000000 -q "$certificate_dir/explore_boundary_pari.gp" \
    >"$boundary_output" 2>&1; then
  cat "$boundary_output"
  exit 1
fi
if grep -Eq 'FAIL:|\*\*\*|syntax error|user error|at top-level|in function' \
    "$boundary_output"; then
  cat "$boundary_output"
  exit 1
fi
grep -Fx "D4_DN2C_PUNCTURED_INTERSECTION_EXCLUDED" \
    "$boundary_output" >/dev/null
grep -Fx "D4_DN2C_ORIGIN_BINARY_COLLAPSE_PLANE_EXIT" \
    "$boundary_output" >/dev/null
grep -Fx "D4_DN2C_BOUNDARY_E5_PROBE_PASS" "$boundary_output" >/dev/null

# Required-failure mutation 1: corrupt the doubled contact hyperplane.
sed 's|res61\[1\]-2\*gcontact\^2/3|res61[1]-3*gcontact^2/3|' \
    "$certificate_dir/explore_contact_atlas_pari.gp" >"$contact_mutant"
if cmp -s "$certificate_dir/explore_contact_atlas_pari.gp" \
    "$contact_mutant"; then
  echo "FAIL: contact mutation did not alter the script" >&2
  exit 1
fi
if "$gp_bin" -s 536000000 -q "$contact_mutant" \
    >"$contact_mutant_output" 2>&1; then
  echo "FAIL: corrupted contact radical unexpectedly passed" >&2
  exit 1
fi
grep -F "FAIL: contact doubled hyperplane" \
    "$contact_mutant_output" >/dev/null

# Required-failure mutation 2: corrupt the exact projective gcd.
sed 's|tt/162+1/243|tt/162+2/243|' \
    "$certificate_dir/explore_plane_pari.gp" >"$plane_mutant"
if cmp -s "$certificate_dir/explore_plane_pari.gp" "$plane_mutant"; then
  echo "FAIL: transverse mutation did not alter the script" >&2
  exit 1
fi
if "$gp_bin" -s 536000000 -q "$plane_mutant" \
    >"$plane_mutant_output" 2>&1; then
  echo "FAIL: corrupted transverse gcd unexpectedly passed" >&2
  exit 1
fi
grep -F "FAIL: plus-plane exact projective gcd" \
    "$plane_mutant_output" >/dev/null

# Required-failure mutation 3: corrupt the decisive E3 square.
sed 's|res3H\[2\]+k\*Wcompat\^2/2|res3H[2]+k*Wcompat^2/3|' \
    "$certificate_dir/explore_boundary_pari.gp" >"$e3_mutant"
if cmp -s "$certificate_dir/explore_boundary_pari.gp" "$e3_mutant"; then
  echo "FAIL: E3 mutation did not alter the script" >&2
  exit 1
fi
if "$gp_bin" -s 536000000 -q "$e3_mutant" \
    >"$e3_mutant_output" 2>&1; then
  echo "FAIL: corrupted E3 square unexpectedly passed" >&2
  exit 1
fi
grep -F "FAIL: intersection H E3 residual 2 forces W" \
    "$e3_mutant_output" >/dev/null

printf '%s\n' "D4_DN2C_DIRECT_PARI_LOWER_STRICT_PASS"
printf '%s\n' "D4_DN2C_DIRECT_PARI_CONTACT_ATLAS_STRICT_PASS"
printf '%s\n' "D4_DN2C_DIRECT_PARI_FULL_FAMILY_STRICT_PASS"
