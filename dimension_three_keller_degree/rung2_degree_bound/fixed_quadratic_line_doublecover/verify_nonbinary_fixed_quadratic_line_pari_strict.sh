#!/bin/sh
# Fail closed around GP, whose file reader can continue after runtime errors.

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
output=$(gp -q "$script_directory/verify_nonbinary_fixed_quadratic_line_pari.gp" 2>&1)
status=$?

printf '%s\n' "$output"

if [ "$status" -ne 0 ]; then
    exit "$status"
fi

case "$output" in
    *"***"*)
        exit 1
        ;;
esac

if [ "$output" != "nonbinary fixed-quadratic line-cover PARI/GP checks passed" ]; then
    exit 1
fi
