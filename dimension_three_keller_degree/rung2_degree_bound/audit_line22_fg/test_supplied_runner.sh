#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
package_dir=$(CDPATH= cd -- "$audit_dir/.." && pwd)

chmod +x "$audit_dir/fakebin/gp"

check_runner() {
  runner=$1
  set +e
  output=$(
    PATH="$audit_dir/fakebin:$PATH" \
      "$package_dir/$runner" 2>&1
  )
  status=$?
  set -e

  printf '%s\n' "$output"
  if [ "$status" -eq 0 ]; then
    echo "FAIL: $runner accepted an injected PARI diagnostic" >&2
    exit 1
  fi
  if ! printf '%s\n' "$output" |
      grep -Fq 'FAIL: PARI/GP emitted a parser or runtime diagnostic'; then
    echo "FAIL: $runner failed for an unexpected reason" >&2
    exit 1
  fi
  echo "PASS: $runner rejects an injected diagnostic"
}

check_runner run_verify_line_22_finite_outer_critical_pari.sh
check_runner run_verify_line_22_fg_resonance_pari.sh
