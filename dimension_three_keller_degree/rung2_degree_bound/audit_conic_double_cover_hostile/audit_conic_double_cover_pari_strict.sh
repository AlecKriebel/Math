#!/bin/sh
# Fail closed around GP: its file reader can continue after some errors.

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
gp_command=${AUDIT_CONIC_DOUBLE_COVER_GP:-gp}
output=$("$gp_command" -q "$script_directory/audit_conic_double_cover_pari.gp" 2>&1)
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

if [ "$output" != "AUDIT_CONIC_DOUBLE_COVER_PARI_PASS_7E4A91" ]; then
    exit 1
fi
