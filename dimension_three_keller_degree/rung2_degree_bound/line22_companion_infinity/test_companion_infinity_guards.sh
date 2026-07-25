#!/bin/sh

set -eu

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if /usr/bin/python3 -O \
    "$script_directory/verify_companion_infinity_sympy.py" \
    >/dev/null 2>&1
then
    printf '%s\n' "FAIL: optimized Python was accepted"
    exit 1
fi

fake_gp="$script_directory/fake_gp_for_guards.sh"
for mode in diagnostic extra badstatus wrong; do
    if GP_BIN="$fake_gp" FAKE_GP_MODE="$mode" \
        "$script_directory/verify_companion_infinity_pari_strict.sh" \
        >/dev/null 2>&1
    then
        printf '%s\n' "FAIL: strict GP wrapper accepted $mode"
        exit 1
    fi
done

GP_BIN="$fake_gp" FAKE_GP_MODE=good \
    "$script_directory/verify_companion_infinity_pari_strict.sh" \
    >/dev/null

printf '%s\n' "PASS: companion-at-infinity verifier guards fail closed"
