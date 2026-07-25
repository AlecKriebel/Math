#!/bin/sh
# Fail closed around GP's permissive file reader.

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
output=$(gp -q -s 256M "$script_directory/audit_reconstruct_pari.gp" 2>&1)
status=$?

printf '%s\n' "$output"

if [ "$status" -ne 0 ]; then
    exit "$status"
fi

case "$output" in
    *"***"*|*"FAIL:"*)
        exit 1
        ;;
esac

if [ "$output" != "AUDIT_FIXED_QUADRATIC_LINE_PARI_PASS_41D8C2" ]; then
    exit 1
fi
