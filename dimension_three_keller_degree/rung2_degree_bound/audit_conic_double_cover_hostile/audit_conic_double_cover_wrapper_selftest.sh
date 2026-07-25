#!/bin/sh
set -u

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
wrapper="$script_directory/audit_conic_double_cover_pari_strict.sh"
fake_gp="$script_directory/audit_conic_double_cover_fake_gp.sh"

run_mode() {
    mode=$1
    expected=$2
    AUDIT_CONIC_DOUBLE_COVER_GP="$fake_gp" \
    AUDIT_CONIC_DOUBLE_COVER_FAKE_MODE="$mode" \
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

printf '%s\n' "AUDIT_CONIC_DOUBLE_COVER_WRAPPER_SELFTEST_PASS"
