#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if /usr/bin/python3 -O "$script_dir/verify_rankone_restriction_sympy.py" \
    >/dev/null 2>&1; then
    printf '%s\n' "ERROR: optimized Python bypassed the assertion guard" >&2
    exit 1
fi

if GP_BIN="$script_dir/fake_gp_diagnostic.sh" \
    "$script_dir/verify_rankone_restriction_pari_strict.sh" \
    >/dev/null 2>&1; then
    printf '%s\n' "ERROR: strict PARI wrapper accepted a diagnostic" >&2
    exit 1
fi

if GP_BIN="$script_dir/audit_hostile/fake_gp_extra.sh" \
    "$script_dir/verify_rankone_restriction_pari_strict.sh" \
    >/dev/null 2>&1; then
    printf '%s\n' "ERROR: strict PARI wrapper accepted unexpected output" >&2
    exit 1
fi

if GP_BIN="$script_dir/fake_gp_missing.sh" \
    "$script_dir/verify_rankone_restriction_pari_strict.sh" \
    >/dev/null 2>&1; then
    printf '%s\n' "ERROR: strict PARI wrapper accepted missing output" >&2
    exit 1
fi

if GP_BIN="$script_dir/fake_gp_nonzero.sh" \
    "$script_dir/verify_rankone_restriction_pari_strict.sh" \
    >/dev/null 2>&1; then
    printf '%s\n' "ERROR: strict PARI wrapper accepted nonzero exit" >&2
    exit 1
fi

printf '%s\n' "PASS: verifier guards fail closed"
