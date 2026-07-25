#!/bin/sh
set -u

audit_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
theorem_directory=$(CDPATH= cd -- "$audit_directory/.." && pwd) || exit 1
wrapper="$theorem_directory/verify_nonbinary_fixed_quadratic_line_pari_strict.sh"
fake_path="$audit_directory/fakebin:$PATH"

run_mode() {
    mode=$1
    expected=$2
    PATH="$fake_path" AUDIT_FIXED_QUADRATIC_FAKE_MODE="$mode" \
        "$wrapper" >/dev/null 2>&1
    status=$?
    if [ "$expected" = "pass" ]; then
        [ "$status" -eq 0 ] || exit 1
    else
        [ "$status" -ne 0 ] || exit 1
    fi
}

run_mode pass pass
run_mode diagnostic fail
run_mode extra fail
run_mode nonzero fail

printf '%s\n' "AUDIT_SUPPLIED_FIXED_QUADRATIC_WRAPPER_SELFTEST_PASS"
