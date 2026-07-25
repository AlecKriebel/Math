#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
package_dir=$(CDPATH= cd -- "$audit_dir/.." && pwd)

check_fail_closed() {
  script=$1
  output_file=$(mktemp "${TMPDIR:-/tmp}/line22-python-opt.XXXXXX")
  trap 'rm -f "$output_file"' EXIT HUP INT TERM

  set +e
  /usr/bin/python3 -O "$package_dir/$script" >"$output_file" 2>&1
  status=$?
  set -e

  if [ "$status" -eq 0 ]; then
    cat "$output_file"
    echo "FAIL AUDIT: $script accepted optimized mode" >&2
    exit 1
  fi
  if ! grep -Fq \
      'RuntimeError: verification requires assertions; do not use -O' \
      "$output_file"; then
    cat "$output_file"
    echo "FAIL AUDIT: $script rejected -O for an unexpected reason" >&2
    exit 1
  fi
  echo "PASS: $script rejects optimized mode before verification"

  rm -f "$output_file"
  trap - EXIT HUP INT TERM
}

check_fail_closed verify_line_22_finite_outer_critical_sympy.py
check_fail_closed verify_line_22_fg_resonance_sympy.py

echo "PASS AUDIT: optimized-mode fail-closed guards verified"
