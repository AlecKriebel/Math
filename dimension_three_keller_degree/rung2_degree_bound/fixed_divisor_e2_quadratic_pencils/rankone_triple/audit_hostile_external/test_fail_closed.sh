#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
scratch_dir=$(mktemp -d "${TMPDIR:-/tmp}/rankone-a0-external-fail.XXXXXX")
trap 'rm -rf "$scratch_dir"' EXIT HUP INT TERM

check_rejected()
{
  label=$1
  edit=$2
  forged="$scratch_dir/$label.gp"
  sed "$edit" "$script_dir/verify_a0_external_pari.gp" >"$forged"
  if "$script_dir/verify_a0_external_pari_strict.sh" "$forged" \
      >/dev/null 2>&1; then
    echo "FAIL: forged external certificate was accepted: $label" >&2
    exit 1
  fi
  echo "PASS external fail-closed rejection: $label"
}

check_rejected raw_minor \
  's/-7558272/-7558271/'
check_rejected e6_branch \
  's/w3\*(w3-w2)/w3*(w3-2*w2)/'
check_rejected rzero_pivot \
  's/s^8),"w3 D-open r=0 E4 pivot"/s^7),"w3 D-open r=0 E4 pivot"/'
check_rejected shear_compensation \
  's/resk\*tx\[3\]\/3/resk*tx[3]\/2/'
check_rejected xz_terminal \
  's/-8\/27\*s^4/-7\/27*s^4/'
check_rejected xy_factor \
  's/75\*hh^2/74*hh^2/'
check_rejected final_marker \
  '/ALL EXTERNAL PARI A=0 HOSTILE CHECKS PASSED/d'

echo "ALL EXTERNAL PARI FAIL-CLOSED MUTATIONS REJECTED"
