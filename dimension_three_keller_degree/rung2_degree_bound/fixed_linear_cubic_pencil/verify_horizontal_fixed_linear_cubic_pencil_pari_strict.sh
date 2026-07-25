#!/bin/sh
# Fail closed around GP's permissive file reader.

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
output=$(gp -q \
    "$script_directory/verify_horizontal_fixed_linear_cubic_pencil_pari.gp" \
    2>&1)
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

if [ "$output" != \
    "horizontal fixed-linear cubic-pencil PARI/GP checks passed" ]; then
    exit 1
fi
