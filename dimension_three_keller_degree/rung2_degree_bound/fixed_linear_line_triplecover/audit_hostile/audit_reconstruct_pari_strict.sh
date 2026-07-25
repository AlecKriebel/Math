#!/bin/sh
# Fail closed around GP's permissive file reader.

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
output=$(gp -q "$script_directory/audit_reconstruct_pari.gp" 2>&1)
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

if [ "$output" != "AUDIT_FIXED_LINEAR_TRIPLECOVER_PARI_PASS_9B6E20" ]; then
    exit 1
fi
