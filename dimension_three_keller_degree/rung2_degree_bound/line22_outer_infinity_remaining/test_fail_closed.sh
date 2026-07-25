#!/bin/sh

set -eu

script_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}

if "$python_bin" -O "$script_directory/verify_line22_outer_infinity_remaining_sympy.py" >/dev/null 2>&1; then
    printf '%s\n' "FAIL: optimized Python was accepted"
    exit 1
fi

fixture_directory=$(mktemp -d "${TMPDIR:-/tmp}/line22-outer-infinity-guard.XXXXXX")
trap 'rm -rf "$fixture_directory"' EXIT HUP INT TERM

printf '%s\n' \
    '#!/bin/sh' \
    'case "${FAKE_GP_MODE:-}" in' \
    '  diagnostic) printf "%s\n" "*** forged GP diagnostic" ;;' \
    '  wrong) printf "%s\n" "wrong sentinel" ;;' \
    '  badstatus) exit 7 ;;' \
    '  good) printf "%s\n" "line-(2,2) remaining finite-companion outer-infinity PARI/GP checks passed" ;;' \
    'esac' \
    > "$fixture_directory/gp"
chmod +x "$fixture_directory/gp"

for mode in diagnostic wrong badstatus; do
    if PATH="$fixture_directory:$PATH" FAKE_GP_MODE="$mode" \
        "$script_directory/verify_line22_outer_infinity_remaining_pari_strict.sh" \
        >/dev/null 2>&1
    then
        printf '%s\n' "FAIL: strict GP wrapper accepted $mode"
        exit 1
    fi
done

PATH="$fixture_directory:$PATH" FAKE_GP_MODE=good \
    "$script_directory/verify_line22_outer_infinity_remaining_pari_strict.sh" \
    >/dev/null

printf '%s\n' "line-(2,2) remaining outer-infinity fail-closed tests passed"
