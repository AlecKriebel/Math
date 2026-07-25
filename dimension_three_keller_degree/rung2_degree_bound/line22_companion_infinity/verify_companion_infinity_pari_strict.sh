#!/bin/sh

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
gp_bin=${GP_BIN:-/opt/homebrew/bin/gp}

if [ ! -x "$gp_bin" ]; then
    printf '%s\n' "ERROR: PARI/GP executable not found: $gp_bin" >&2
    exit 1
fi

output=$("$gp_bin" -q "$script_directory/verify_companion_infinity_pari.gp" 2>&1)
status=$?

printf '%s\n' "$output"

if [ "$status" -ne 0 ]; then
    exit "$status"
fi

case "$output" in
    *"***"*|*"FAIL"*|*"syntax error"*|*"incorrect type"*)
        exit 1
        ;;
esac

sentinel='PASS: independent PARI line-(2,2) companion-at-infinity certificate'
if [ "$output" != "$sentinel" ]; then
    exit 1
fi
