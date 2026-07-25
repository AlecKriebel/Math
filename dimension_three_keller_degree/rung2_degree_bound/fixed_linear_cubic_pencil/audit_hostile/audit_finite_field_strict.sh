#!/bin/sh

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
output=$(/usr/bin/python3 "$script_directory/audit_finite_field.py" 2>&1)
status=$?

printf '%s\n' "$output"

if [ "$status" -ne 0 ]; then
    exit "$status"
fi

if [ "$output" != "AUDIT_HORIZONTAL_CUBIC_PENCIL_FF_PASS_8D1A77" ]; then
    exit 1
fi
