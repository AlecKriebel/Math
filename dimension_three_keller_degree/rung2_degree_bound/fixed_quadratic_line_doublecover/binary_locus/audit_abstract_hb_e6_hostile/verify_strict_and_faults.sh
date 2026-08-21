#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
GP_BIN=${GP_BIN:-/opt/homebrew/bin/gp}
SCRIPT="$SCRIPT_DIR/verify_abstract_hb_e6_pari.gp"

"$GP_BIN" -q "$SCRIPT"

TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/hb-e6-audit.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

for mutation in \
  e7_beta_sign \
  e7_gamma_sign \
  e6_wdv_sign \
  e6_tdu_sign \
  e6_curvature_sign \
  e6_tau_sign \
  e6_det_sum_sign \
  rzero_in_table \
  wedge_drop_g \
  nullity_shift \
  delta0_kernel \
  height_unit \
  power_fibre \
  delta0_shear
do
  log="$TMP_AUDIT/$mutation.log"
  if AUDIT_MUTATION=$mutation "$GP_BIN" -q "$SCRIPT" >"$log" 2>&1
  then
    echo "FAIL: mutation $mutation escaped its guard" >&2
    exit 1
  fi
  if ! grep -q "FAIL \\[$mutation\\]" "$log"
  then
    echo "FAIL: mutation $mutation did not fail through an audit guard" >&2
    sed -n '1,80p' "$log" >&2
    exit 1
  fi
  echo "PASS fail-closed mutation: $mutation"
done

echo "ALL STRICT AND FAULT-GUARD RUNS PASSED"
